#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bridge sécurisé pour Mailjet avec support HTTPS
Module d'envoi d'emails via l'API Mailjet pour les convocations d'examens
"""

import os
import json
import base64
import hashlib
import pandas as pd
from pathlib import Path
from datetime import datetime
import time
import logging
import html
from typing import Dict, List, Optional, Tuple, Union

# Import du registre sécurisé pour association fiable
from candidate_pdf_registry import CandidatePDFRegistry

try:
    # Essayer d'importer depuis l'installation locale d'abord
    import sys
    import os
    
    # Ajouter le dossier mailjet au path si nécessaire
    mailjet_path = os.path.join(os.path.dirname(__file__), 'mailjet')
    if mailjet_path not in sys.path:
        sys.path.insert(0, mailjet_path)
    
    from mailjet_rest import Client
except ImportError:
    try:
        # Fallback vers l'installation pip
        from mailjet_rest import Client
    except ImportError:
        raise ImportError("Mailjet REST API non trouvé. Le module local mailjet/ est présent mais ne fonctionne pas correctement.")

import requests
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# Import pour les corrections 400
from mailjet_400_fixes import Mailjet400Fixer

# Import pour le processeur de jurys
try:
    from jury_file_processor import JuryFileProcessor
except ImportError:
    JuryFileProcessor = None

class MailjetSecurityManager:
    """Gestionnaire de sécurité pour les credentials Mailjet"""
    
    def __init__(self, config_file: str = "mailjet_config.json"):
        self.config_file = config_file
        self.key_file = "mailjet.key"
        
    def _generate_key(self, password: str) -> bytes:
        """Génère une clé de chiffrement à partir d'un mot de passe"""
        password_bytes = password.encode()
        salt = b'mailjet_secure_salt_2024'  # En production, utilisez un salt aléatoire
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password_bytes))
        return key
    
    def encrypt_credentials(self, api_key: str, secret_key: str, password: str) -> None:
        """Chiffre et sauvegarde les credentials Mailjet"""
        key = self._generate_key(password)
        f = Fernet(key)
        
        credentials = {
            "api_key": api_key,
            "secret_key": secret_key,
            "created_at": datetime.now().isoformat()
        }
        
        encrypted_data = f.encrypt(json.dumps(credentials).encode())
        
        with open(self.config_file, 'wb') as file:
            file.write(encrypted_data)
            
        # Sauvegarder un hash du mot de passe pour vérification
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        with open(self.key_file, 'w') as file:
            json.dump({"password_hash": password_hash}, file)
            
    def decrypt_credentials(self, password: str) -> Dict[str, str]:
        """Déchiffre et récupère les credentials Mailjet"""
        if not os.path.exists(self.config_file) or not os.path.exists(self.key_file):
            raise FileNotFoundError("Fichiers de configuration non trouvés")
            
        # Vérifier le mot de passe
        with open(self.key_file, 'r') as file:
            key_data = json.load(file)
            
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        if password_hash != key_data["password_hash"]:
            raise ValueError("Mot de passe incorrect")
            
        # Déchiffrer les credentials
        key = self._generate_key(password)
        f = Fernet(key)
        
        with open(self.config_file, 'rb') as file:
            encrypted_data = file.read()
            
        decrypted_data = f.decrypt(encrypted_data)
        credentials = json.loads(decrypted_data.decode())
        
        return credentials

class MailjetBridge:
    """Bridge sécurisé pour l'API Mailjet avec support HTTPS"""
    
    def __init__(self, excel_path: str, pdf_dir: str, 
                 sender_email: str = "", sender_name: str = "",
                 config_password: str = ""):
        """
        Initialise le bridge Mailjet
        
        Args:
            excel_path (str): Chemin vers le fichier Excel des candidats
            pdf_dir (str): Répertoire contenant les PDF des convocations
            sender_email (str): Adresse email de l'expéditeur
            sender_name (str): Nom de l'expéditeur
            config_password (str): Mot de passe pour déchiffrer la configuration
        """
        self.excel_path = excel_path
        self.pdf_dir = pdf_dir
        self.sender_email = sender_email
        self.sender_name = sender_name or "Service des Examens"
        
        # Configuration de logging avec UTF-8
        self.logger = logging.getLogger(__name__)
        
        # Configurer le handler avec UTF-8 si pas déjà fait
        if not self.logger.handlers:
            handler = logging.StreamHandler(sys.stdout)
            handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
            if hasattr(handler.stream, 'reconfigure'):
                handler.stream.reconfigure(encoding='utf-8')
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)
        
        # Gestionnaire de sécurité
        self.security_manager = MailjetSecurityManager()
        
        # Client Mailjet (sera initialisé après authentification)
        self.mailjet_client = None
        self.api_key = None
        self.secret_key = None
        
        # Configuration HTTPS
        self.session = requests.Session()
        self.session.verify = True  # Vérification SSL obligatoire
        
        # 🔒 REGISTRE SÉCURISÉ pour association 100% fiable candidat-PDF-email
        self.pdf_registry = CandidatePDFRegistry(self.pdf_dir)
        self.logger.info("🔒 MAILJET: Registre sécurisé initialisé pour association fiable PDF")
        
        # Correcteur pour erreurs 400
        self.error_fixer = Mailjet400Fixer()

        if config_password:
            self._authenticate(config_password)
            
    def _safe_log(self, message, level='info'):
        """Méthode de logging sécurisée qui évite les erreurs d'encodage"""
        try:
            # Nettoyer le message des caractères problématiques
            safe_message = message.replace('✓', '[OK]').replace('✗', '[ERREUR]').replace('⚠️', '[ATTENTION]')
            safe_message = safe_message.replace('🚀', '[DEMARRAGE]').replace('🎉', '[SUCCES]').replace('❌', '[ECHEC]')
            
            if level == 'info':
                self.logger.info(safe_message)
            elif level == 'error':
                self.logger.error(safe_message)
            elif level == 'warning':
                self.logger.warning(safe_message)
        except Exception as e:
            # En dernier recours, utiliser print
            print(f"[LOG-ERROR] {message} (Erreur logging: {e})")

    def setup_credentials(self, api_key: str, secret_key: str, password: str) -> None:
        """Configure et chiffre les credentials Mailjet"""
        try:
            # Tester la connexion avec les credentials en utilisant l'endpoint v3 (pour account info)
            test_client = Client(auth=(api_key, secret_key), version='v3')
            result = test_client.user.get()
            
            if result.status_code == 200:
                self.security_manager.encrypt_credentials(api_key, secret_key, password)
                self.logger.info("Credentials Mailjet configurés et chiffrés avec succès")
            else:
                error_detail = ""
                try:
                    error_data = result.json()
                    error_detail = f" - Détails: {error_data}"
                except:
                    pass
                raise ValueError(f"Credentials Mailjet invalides (Status: {result.status_code}){error_detail}")
                
        except Exception as e:
            if "Credentials Mailjet invalides" in str(e):
                raise
            raise Exception(f"Erreur lors de la configuration des credentials: {e}")
            
    def _authenticate(self, password: str) -> None:
        """Authentifie et initialise le client Mailjet"""
        try:
            credentials = self.security_manager.decrypt_credentials(password)
            self.api_key = credentials["api_key"]
            self.secret_key = credentials["secret_key"]
            
            # Initialiser le client Mailjet avec HTTPS forcé
            self.mailjet_client = Client(
                auth=(self.api_key, self.secret_key),
                version='v3.1'
            )
            
            # Tester la connexion avec l'endpoint v3 pour validation
            test_client = Client(auth=(self.api_key, self.secret_key), version='v3')
            result = test_client.user.get()
            if result.status_code != 200:
                error_detail = ""
                try:
                    error_data = result.json()
                    error_detail = f" - Détails: {error_data}"
                except:
                    pass
                raise Exception(f"Échec de l'authentification Mailjet (Status: {result.status_code}){error_detail}")
                
            self.logger.info("Authentification Mailjet réussie")
            
        except Exception as e:
            raise Exception(f"Erreur d'authentification: {e}")
            
    def _is_tcf_file(self) -> bool:
        """Vérifie si le fichier Excel contient des onglets TCF"""
        try:
            xl = pd.ExcelFile(self.excel_path)
            sheet_names = [sheet.strip().upper() for sheet in xl.sheet_names]
            
            # Vérifier les mots-clés TCF spécifiques
            tcf_keywords = ['TCF', 'TCF-TP', 'TCF-TOUT', 'TCF_TP', 'TCF_TOUT']
            has_tcf = any(keyword in name for name in sheet_names for keyword in tcf_keywords)
            
            # Vérifier si c'est plutôt un fichier DELF/DALF (niveaux A1, A2, B1, B2, C1, C2)
            delf_levels = ['A1', 'A2', 'B1', 'B2', 'C1', 'C2']
            has_delf_levels = any(level in name for name in sheet_names for level in delf_levels)
            
            self.logger.debug(f"Onglets détectés: {xl.sheet_names}")
            self.logger.debug(f"TCF détecté: {has_tcf}, DELF détecté: {has_delf_levels}")
            
            return has_tcf and not has_delf_levels  # Seulement TCF si pas de niveaux DELF
        except Exception as e:
            self.logger.warning(f"⚠️ Erreur lors de la vérification TCF: {e}")
            return False
    
    def _load_tcf_data(self) -> pd.DataFrame:
        """Charge les données TCF en utilisant la structure TCF standard"""
        try:
            xl = pd.ExcelFile(self.excel_path)
            all_candidates = []
            
            # Parcourir tous les onglets TCF
            for sheet_name in xl.sheet_names:
                if sheet_name.upper() == 'ADMIN':
                    continue
                    
                # Vérifier si c'est un onglet TCF
                if 'TCF' in sheet_name.upper():
                    self.logger.info(f"📋 Traitement de l'onglet TCF: {sheet_name}")
                    
                    try:
                        df_sheet = pd.read_excel(self.excel_path, sheet_name=sheet_name, engine='openpyxl')
                        
                        # Chercher la ligne d'en-tête (qui contient "Email")
                        header_row = None
                        for idx, row in df_sheet.iterrows():
                            row_values = row.tolist()
                            if any('Email' in str(cell) for cell in row_values if pd.notna(cell)):
                                header_row = idx
                                self.logger.debug(f"En-tête trouvé à la ligne {idx}: {row_values}")
                                break
                        
                        if header_row is not None:
                            # Traiter chaque ligne après l'en-tête
                            for idx in range(header_row + 1, len(df_sheet)):
                                row = df_sheet.iloc[idx]
                                row_values = row.tolist()
                                
                                # Structure TCF: ['Pass.', 'NOM et Prénom', 'Date de naissance', 'Email']
                                if len(row_values) >= 4:
                                    heure_pass = str(row_values[0]) if pd.notna(row_values[0]) else ''
                                    nom_prenom = str(row_values[1]) if pd.notna(row_values[1]) else ''
                                    date_naissance = str(row_values[2]) if pd.notna(row_values[2]) else ''
                                    email = str(row_values[3]) if pd.notna(row_values[3]) else ''
                                    
                                    # Ignorer les lignes vides ou d'en-tête
                                    if not nom_prenom or nom_prenom == 'NOM et Prénom' or email == 'Email':
                                        continue
                                    
                                    # Séparer nom et prénom
                                    if ' ' in nom_prenom:
                                        parts = nom_prenom.split(' ', 1)
                                        nom = parts[0]
                                        prenom = parts[1] if len(parts) > 1 else ''
                                    else:
                                        nom = nom_prenom
                                        prenom = ''
                                    
                                    # Vérifier que l'email est valide
                                    if email and email.strip() and '@' in email and email.strip() != 'nan':
                                        candidate_data = {
                                            'nom': nom,
                                            'prenom': prenom,
                                            'email': email.strip(),
                                            'date_naissance': date_naissance,
                                            'heure_passation': heure_pass,
                                            'type_tcf': sheet_name,
                                            'type_examen': 'TCF',
                                            'date_examen': '',
                                            'heure_examen': heure_pass,
                                            'salle': ''
                                        }
                                        
                                        all_candidates.append(candidate_data)
                                        self.logger.debug(f"✅ Candidat TCF ajouté: {nom} {prenom} - {email} ({sheet_name})")
                                    else:
                                        if nom_prenom:  # Seulement afficher si il y a un nom
                                            self.logger.warning(f"⚠️ Email manquant pour: {nom_prenom} (email='{email}')")
                        else:
                            self.logger.warning(f"⚠️ En-tête 'Email' non trouvé dans {sheet_name}")
                    
                    except Exception as e:
                        self.logger.error(f"❌ Erreur lors du traitement de l'onglet {sheet_name}: {e}")
            
            # Convertir en DataFrame
            if all_candidates:
                df = pd.DataFrame(all_candidates)
                self.logger.info(f"✅ {len(df)} candidats TCF chargés avec emails valides")
                return df
            else:
                self.logger.error("❌ Aucun candidat TCF trouvé avec email valide")
                return pd.DataFrame()
                
        except Exception as e:
            self.logger.error(f"❌ Erreur lors du chargement TCF: {e}")
            return pd.DataFrame()

    def _is_jury_file(self) -> bool:
        """Détecte si le fichier Excel est un fichier de jurys"""
        try:
            # Lire les noms des feuilles
            excel_file = pd.ExcelFile(self.excel_path)
            sheet_names = excel_file.sheet_names
            
            # Vérifier si on a des feuilles de type "Niveau X"
            niveau_sheets = [name for name in sheet_names if name.startswith('Niveau ')]
            has_admin_sheet = 'ADMIN' in sheet_names
            
            # C'est un fichier de jurys si on a au moins 2 feuilles "Niveau" et une feuille ADMIN
            return len(niveau_sheets) >= 2 and has_admin_sheet
            
        except Exception:
            return False
    
    def _convert_jury_file_to_candidates(self) -> pd.DataFrame:
        """Convertit un fichier de jurys DELF/DALF en format candidats avec emails extraits"""
        try:
            xl = pd.ExcelFile(self.excel_path)
            all_candidates = []
            
            for sheet_name in xl.sheet_names:
                if sheet_name.upper() == 'ADMIN':
                    continue
                    
                self.logger.info(f"📋 Traitement de l'onglet: {sheet_name}")
                
                try:
                    # Lire l'onglet
                    df = pd.read_excel(self.excel_path, sheet_name=sheet_name, engine='openpyxl')
                    
                    # Chercher la ligne d'en-tête (qui contient "Email")
                    header_row = None
                    for idx, row in df.iterrows():
                        row_values = row.tolist()
                        if any('Email' in str(cell) for cell in row_values):
                            header_row = idx
                            self.logger.debug(f"En-tête trouvé à la ligne {idx}")
                            break
                    
                    if header_row is not None:
                        # Lire à partir de la ligne d'en-tête
                        df_data = pd.read_excel(self.excel_path, sheet_name=sheet_name, 
                                              header=header_row, engine='openpyxl')
                        
                        # Les emails sont dans la colonne 5 (index 5) selon la structure observée
                        # Structure: ['Prép.', 'Pass.', 'Numéro de candidat', 'NOM et Prénom', 'Date de naissance', 'Email', 'Besoins spéciaux']
                        email_col_idx = 5  # Index de la colonne Email
                        nom_prenom_idx = 3  # Index de la colonne "NOM et Prénom"
                        
                        if len(df_data.columns) > email_col_idx:
                            candidates_count = 0
                            
                            # Traiter chaque ligne de données
                            for idx, row in df_data.iterrows():
                                row_values = row.tolist()
                                
                                # Extraire les données
                                if len(row_values) > email_col_idx:
                                    email = str(row_values[email_col_idx]) if pd.notna(row_values[email_col_idx]) else ''
                                    nom_prenom = str(row_values[nom_prenom_idx]) if len(row_values) > nom_prenom_idx and pd.notna(row_values[nom_prenom_idx]) else ''
                                    
                                    # Ignorer la ligne d'en-tête (contient "Email" ou "NOM et Prénom")
                                    if email == 'Email' or nom_prenom == 'NOM et Prénom':
                                        continue
                                    
                                    # Séparer nom et prénom si possible
                                    if nom_prenom and ' ' in nom_prenom:
                                        parts = nom_prenom.split(' ', 1)
                                        nom = parts[0]
                                        prenom = parts[1] if len(parts) > 1 else ''
                                    else:
                                        nom = nom_prenom
                                        prenom = ''
                                    
                                    # Vérifier que l'email est valide
                                    if email and email.strip() and '@' in email and email.strip() != 'nan':
                                        candidate_data = {
                                            'nom': nom,
                                            'prenom': prenom,
                                            'email': email.strip(),
                                            'niveau': sheet_name,
                                            'type_examen': 'DELF',
                                            'date_examen': '',
                                            'heure_examen': '',
                                            'salle': ''
                                        }
                                        
                                        all_candidates.append(candidate_data)
                                        candidates_count += 1
                                        self.logger.debug(f"✅ Candidat ajouté: {nom} {prenom} - {email}")
                            
                            self.logger.info(f"✅ {candidates_count} candidats trouvés dans {sheet_name}")
                        else:
                            self.logger.warning(f"⚠️ Pas assez de colonnes dans {sheet_name}")
                    else:
                        self.logger.warning(f"⚠️ En-tête 'Email' non trouvé dans {sheet_name}")
                        
                except Exception as e:
                    self.logger.error(f"❌ Erreur lors du traitement de l'onglet {sheet_name}: {e}")
            
            if all_candidates:
                df = pd.DataFrame(all_candidates)
                
                # Nettoyer les noms de colonnes pour compatibilité
                df.columns = df.columns.str.strip().str.lower()
                df.columns = df.columns.str.replace(' ', '_').str.replace('é', 'e').str.replace('è', 'e')
                df.columns = df.columns.str.replace('à', 'a').str.replace('ç', 'c').str.replace('ù', 'u')
                
                # Remplacer les valeurs NaN par des chaînes vides
                df = df.fillna('')
                
                self.logger.info(f"✅ Total: {len(df)} candidats avec emails valides chargés depuis le fichier de jurys")
                return df
            else:
                self.logger.error("❌ Aucun candidat trouvé avec email valide dans le fichier de jurys")
                return pd.DataFrame()
                
        except Exception as e:
            self.logger.error(f"❌ Erreur lors de la conversion du fichier de jurys: {e}")
            return pd.DataFrame()

    def _load_excel_data(self) -> pd.DataFrame:
        """Charge les données depuis le fichier Excel (avec détection automatique des fichiers de jurys et TCF)"""
        try:
            # Vérifier si c'est un fichier TCF (contient des onglets TCF)
            if self._is_tcf_file():
                self.logger.info("📋 Fichier TCF détecté - Utilisation du processeur TCF")
                return self._load_tcf_data()
                
            # Détecter si c'est un fichier de jurys
            if self._is_jury_file():
                self.logger.info("📋 Fichier de jurys détecté - Conversion automatique activée")
                return self._convert_jury_file_to_candidates()
            
            # Sinon, traitement normal pour fichier candidats standard
            try:
                df = pd.read_excel(self.excel_path, engine='openpyxl')
            except:
                df = pd.read_excel(self.excel_path, engine='xlrd')
                
            # Nettoyer les noms de colonnes
            df.columns = df.columns.str.strip().str.lower()
            df.columns = df.columns.str.replace(' ', '_').str.replace('é', 'e').str.replace('è', 'e')
            df.columns = df.columns.str.replace('à', 'a').str.replace('ç', 'c').str.replace('ù', 'u')
            
            # Remplacer les valeurs NaN par des chaînes vides
            df = df.fillna('')
            
            return df
            
        except Exception as e:
            raise Exception(f"Erreur lors de la lecture du fichier Excel: {e}")
            
    def _find_pdf_file(self, candidate_data: Dict) -> Optional[str]:
        """
        Trouve le fichier PDF correspondant au candidat via le registre sécurisé
        🔒 GARANTIT l'association correcte candidat-PDF-email
        
        Args:
            candidate_data (Dict): Données du candidat
            
        Returns:
            str: Chemin vers le fichier PDF ou None si non trouvé
        """
        
        # LOG: Afficher le répertoire de recherche
        self.logger.info(f"🔍 RECHERCHE PDF dans: {self.pdf_dir}")
        
        # 🔒 UTILISER LE REGISTRE SÉCURISÉ EN PRIORITÉ ABSOLUE
        try:
            pdf_path, pdf_filename = self.pdf_registry.find_pdf_for_candidate(candidate_data)
            
            if pdf_path and pdf_filename:
                candidate_id = self.pdf_registry.generate_candidate_id(candidate_data)
                self.logger.info(f"🔒 MAILJET REGISTRE: PDF trouvé pour {candidate_data.get('prenom', '')} {candidate_data.get('nom', '')}")
                self.logger.info(f"   🆔 ID: {candidate_id}")
                self.logger.info(f"   📄 Fichier: {pdf_filename}")
                self.logger.info(f"   📂 Chemin: {pdf_path}")
                
                # VÉRIFICATION: Le fichier existe-t-il vraiment ?
                if os.path.exists(pdf_path):
                    return pdf_path
                else:
                    self.logger.warning(f"⚠️ MAILJET: Fichier enregistré mais manquant: {pdf_path}")
            else:
                candidate_id = self.pdf_registry.generate_candidate_id(candidate_data)
                self.logger.warning(f"❌ MAILJET REGISTRE: Aucun PDF enregistré pour {candidate_data.get('prenom', '')} {candidate_data.get('nom', '')} (ID: {candidate_id})")
        except Exception as registry_error:
            self.logger.error(f"⚠️ MAILJET: Erreur registre sécurisé: {registry_error}")
        
        # 🔄 FALLBACK: Recherche traditionnelle si pas trouvé dans le registre
        self.logger.warning(f"🔄 MAILJET FALLBACK: Recherche traditionnelle pour {candidate_data.get('prenom', '')} {candidate_data.get('nom', '')}")
        
        nom = str(candidate_data.get('nom', '')).replace(' ', '_')
        prenom = str(candidate_data.get('prenom', '')).replace(' ', '_')
        numero = str(candidate_data.get('numero_candidat', ''))
        
        # Nettoyer les noms pour les noms de fichiers
        safe_nom = ''.join(c for c in nom if c.isalnum() or c in '_-')
        safe_prenom = ''.join(c for c in prenom if c.isalnum() or c in '_-')
        
        # Patterns de noms de fichiers possibles (incluant le nouveau format simplifié)
        possible_names = [
            # Nouveau format simplifié
            f"convocation_TCF_{safe_nom.upper()}_{safe_prenom.upper()}_*.pdf",
            # Anciens formats
            f"convocation_{safe_nom}_{safe_prenom}_{numero}.pdf",
            f"convocation_{safe_nom}_{safe_prenom}.pdf",
            f"{safe_nom}_{safe_prenom}_{numero}.pdf",
            f"{safe_nom}_{safe_prenom}.pdf",
            f"convocation_{numero}.pdf"
        ]
        
        import glob
        
        # Chercher le fichier avec patterns
        for pattern in possible_names:
            if '*' in pattern:
                # Pattern avec wildcard
                search_path = os.path.join(self.pdf_dir, pattern)
                matches = glob.glob(search_path)
                if matches:
                    filepath = matches[0]  # Prendre le premier match
                    if os.path.exists(filepath):
                        self.logger.info(f"📄 MAILJET FALLBACK: Trouvé par pattern {pattern} -> {os.path.basename(filepath)}")
                        return filepath
            else:
                # Pattern exact
                filepath = os.path.join(self.pdf_dir, pattern)
                if os.path.exists(filepath):
                    self.logger.info(f"📄 MAILJET FALLBACK: Trouvé {pattern}")
                    return filepath
                
        # Si aucun fichier trouvé, lister les fichiers disponibles pour recherche partielle
        try:
            available_files = [f for f in os.listdir(self.pdf_dir) if f.endswith('.pdf')]
            
            # Essayer de trouver par correspondance partielle
            for available_file in available_files:
                if (safe_nom.lower() in available_file.lower() and 
                    safe_prenom.lower() in available_file.lower()) or \
                   (numero and numero in available_file):
                    filepath = os.path.join(self.pdf_dir, available_file)
                    self.logger.info(f"📄 MAILJET FALLBACK: Trouvé par correspondance partielle {available_file}")
                    return filepath
        except Exception as e:
            self.logger.error(f"❌ MAILJET: Erreur liste fichiers: {e}")
                
        self.logger.error(f"❌ MAILJET: AUCUN PDF trouvé pour {candidate_data.get('prenom', '')} {candidate_data.get('nom', '')}")
        return None
        
    def _format_date(self, date_value: Union[str, datetime]) -> str:
        """Formate une date pour l'affichage dans l'email"""
        if pd.isna(date_value) or date_value == '':
            return ''
            
        try:
            if isinstance(date_value, str):
                for fmt in ['%Y-%m-%d', '%d/%m/%Y', '%d-%m-%Y']:
                    try:
                        date_obj = datetime.strptime(date_value, fmt)
                        return date_obj.strftime('%d/%m/%Y')
                    except:
                        continue
                return str(date_value)
            elif hasattr(date_value, 'strftime'):
                return date_value.strftime('%d/%m/%Y')
            else:
                return str(date_value)
        except:
            return str(date_value)
            
    def _clean_html_entities(self, text: str) -> str:
        """
        Nettoie les entités HTML dans le texte
        
        Args:
            text (str): Texte pouvant contenir des entités HTML
            
        Returns:
            str: Texte avec les entités HTML décodées
        """
        try:
            # Décoder les entités HTML comme &#39; -> '
            return html.unescape(text)
        except Exception:
            return text
    
    def _format_french_date(self, date_value: Union[str, datetime]) -> str:
        """Formate une date en français avec jour de la semaine"""
        if pd.isna(date_value) or date_value == '':
            return ''
            
        try:
            # Dictionnaire des jours et mois en français
            jours = ['lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi', 'dimanche']
            mois = ['janvier', 'février', 'mars', 'avril', 'mai', 'juin',
                   'juillet', 'août', 'septembre', 'octobre', 'novembre', 'décembre']
            
            if isinstance(date_value, str):
                for fmt in ['%Y-%m-%d', '%d/%m/%Y', '%d-%m-%Y']:
                    try:
                        date_obj = datetime.strptime(date_value, fmt)
                        break
                    except:
                        continue
                else:
                    return str(date_value)
            elif hasattr(date_value, 'strftime'):
                date_obj = date_value
            else:
                return str(date_value)
                
            # Formater en français: "lundi 15 janvier 2025"
            jour_semaine = jours[date_obj.weekday()]
            jour = date_obj.day
            mois_nom = mois[date_obj.month - 1]
            annee = date_obj.year
            
            return f"{jour_semaine} {jour} {mois_nom} {annee}"
        except:
            return str(date_value)

    def _create_email_content(self, candidate_data: Dict) -> Tuple[str, str, str]:
        """
        Crée le contenu de l'email au format DELF/DALF ou TCF
        
        Args:
            candidate_data (Dict): Données du candidat
            
        Returns:
            tuple: (subject, body_html, body_text)
        """
        nom = str(candidate_data.get('nom', '')).upper()  # NOM en majuscules
        prenom = str(candidate_data.get('prenom', '')).title()
        matiere = str(candidate_data.get('matiere', ''))
        
        # Détecter le type d'examen (TCF ou DELF/DALF)
        is_tcf = 'TCF' in matiere.upper() or candidate_data.get('tcf_type', '').upper().startswith('TCF')
        
        if is_tcf:
            # Gestion pour TCF
            tcf_type = candidate_data.get('tcf_type', matiere)
            date_examen = self._format_french_date(candidate_data.get('date_collective_format', candidate_data.get('date_examen', '')))
            
            # Nettoyer la date pour enlever "le" au début si présent
            if date_examen.startswith('le '):
                date_examen_clean = date_examen[3:]  # Enlever "le "
            else:
                date_examen_clean = date_examen
            
            # Déterminer la déclinaison TCF
            if 'CANADA' in tcf_type.upper():
                declinaison_tcf = "CANADA"
            elif 'TP COMPLET' in tcf_type.upper():
                declinaison_tcf = "TOUT PUBLIC"
            elif 'TP OBLIGATOIRE' in tcf_type.upper():
                declinaison_tcf = "TOUT PUBLIC"
            elif 'IRN' in tcf_type.upper():
                declinaison_tcf = "INTÉGRATION, RÉSIDENCE & NATIONALITÉ"
            else:
                declinaison_tcf = "TOUT PUBLIC"
            
            # Sujet de l'email pour TCF
            subject = "Votre examen TCF"
            subject = self._clean_html_entities(subject)
            
            # Corps de l'email en HTML pour TCF (sobre)
            body_html = f"""
            <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                    <p>Bonjour <strong>{prenom} {nom}</strong>,</p>
                    
                    <p>Vous trouverez en pièce jointe votre convocation à l'examen TCF {declinaison_tcf}.</p>
                    
                    <p>L'examen aura lieu sur ordinateur.</p>
                    
                    <div style="background-color: transparent; border: 2px solid #da002e; border-radius: 8px; padding: 15px; margin: 25px 0;">
                        <h4 style="color: #da002e; font-weight: bold; margin-top: 0;">[IMPORTANT]</h4>
                        <ul style="margin: 10px 0; padding-left: 20px;">
                            <li style="margin-bottom: 8px;">Présentez-vous <strong>30 minutes avant</strong> le début de l'épreuve.</li>
                            <li style="margin-bottom: 8px;">Munissez-vous impérativement d'une <strong>pièce d'identité officielle avec photo, en cours de validité</strong>.</li>
                            <li style="margin-bottom: 8px;">Apportez votre <strong>convocation imprimée</strong> (en pièce jointe).</li>
                            <li style="margin-bottom: 8px;">L'usage des téléphones portables et autres appareils connectés est <strong>strictement interdit</strong>.</li>
                            <li style="margin-bottom: 8px;"><strong>Toute tentative de fraude est passible d'une interdiction à se présenter à des examens d'état pendant plusieurs années, voire de sanctions pénales pour les cas les plus graves.</strong></li>
                        </ul>
                    </div>
                    
                    <p style="margin-top: 30px;">
                        Cordialement,<br>
                        <strong>L'Alliance Française de Bruxelles-Europe</strong><br>
                        <strong>Pôle des Certifications DELF, DALF, TCF et DFP</strong>
                    </p>
                    
                    <hr style="border: none; border-top: 1px solid #dee2e6; margin: 30px 0;">
                    <p style="font-size: 12px; color: #666;">
                        Cet email a été généré automatiquement le {datetime.now().strftime('%d/%m/%Y à %H:%M')}.<br>
                        Merci de ne pas répondre à cet email automatique. Pour toute question, <a href="mailto:examens@alliancefr.be">nous contacter</a>.
                    </p>
                </div>
            </body>
            </html>
            """
            
            # Version texte pour TCF
            body_text = f"""
            Bonjour {prenom} {nom},
            
            Vous trouverez en pièce jointe votre convocation à l'examen TCF {declinaison_tcf}.
            
            L'examen aura lieu sur ordinateur.
            
            [IMPORTANT]
            - Présentez-vous 30 minutes avant le début de l'épreuve.
            - Munissez-vous impérativement d'une pièce d'identité officielle avec photo, en cours de validité.
            - Apportez votre convocation imprimée (en pièce jointe).
            - L'usage des téléphones portables et autres appareils connectés est strictement interdit.
            - Toute tentative de fraude est passible d'une interdiction à se présenter à des examens d'état pendant plusieurs années, voire de sanctions pénales pour les cas les plus graves.
            
            Cordialement,
            L'Alliance Française de Bruxelles-Europe
            Pôle des Certifications DELF, DALF, TCF et DFP
            
            Cet email a été généré automatiquement le {datetime.now().strftime('%d/%m/%Y à %H:%M')}.
            Merci de ne pas répondre à cet email automatique. Pour toute question, nous contacter (examens@alliancefr.be).
            """
            
        else:
            # Gestion pour DELF/DALF (code existant) - MAIS TOUT DOIT ÊTRE TCF !
            # Extraire le niveau (A1, A2, B1, B2, C1, C2)
            niveau = matiere.replace('DELF ', '').replace('DALF ', '')
            type_examen = 'TCF'  # TOUT EST TCF MAINTENANT !
            
            # Dates et heures (utilisent les mêmes noms de champs que pdf_generator.py)
            date_collective = self._format_french_date(candidate_data.get('date_ep_coll', candidate_data.get('date_examen', '')))
            heure_collective = str(candidate_data.get('debut_ep_coll', candidate_data.get('heure_debut', '')))
            
            date_individuelle = self._format_french_date(candidate_data.get('date_ep_ind', candidate_data.get('date_examen', '')))
            heure_individuelle = str(candidate_data.get('heure_preparation', candidate_data.get('heure_debut', '')))
            
            # Sujet de l'email - TOUT EST TCF maintenant, sans date
            subject = "Votre examen TCF"
            subject = self._clean_html_entities(subject)
            
            # Corps de l'email en HTML
            body_html = f"""
            <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                    <h2 style="color: #da002e; margin-bottom: 20px;">
                        Convocation d'examen
                    </h2>
                    
                    <p>Bonjour <strong>{prenom} {nom}</strong>,</p>
                    
                    <p>Voici votre convocation concernant la passation des épreuves de l'examen {niveau}.</p>
                    
                    <div style="background-color: transparent; border: 2px solid #da002e; border-radius: 8px; padding: 15px; margin: 25px 0;">
                        <h4 style="color: #da002e; font-weight: bold; margin-top: 0;">[IMPORTANT]</h4>
                        <ul style="margin: 10px 0; padding-left: 20px;">
                            <li style="margin-bottom: 8px;">Présentez-vous <strong>30 minutes avant</strong> le début de l'épreuve.</li>
                            <li style="margin-bottom: 8px;">Munissez-vous impérativement d'une <strong>pièce d'identité officielle avec photo, en cours de validité</strong>.</li>
                            <li style="margin-bottom: 8px;">Apportez votre <strong>convocation imprimée</strong> (en pièce jointe).</li>
                            <li style="margin-bottom: 8px;">L'usage des téléphones portables et autres appareils connectés est <strong>strictement interdit</strong>.</li>
                            <li style="margin-bottom: 8px;"><strong>Toute tentative de fraude est passible d'une interdiction à se présenter à des examens d'état pendant plusieurs années, voire de sanctions pénales pour les cas les plus graves.</strong></li>
                        </ul>
                    </div>
                    
                    <p>Vous trouverez votre convocation officielle en pièce jointe de cet email. 
                    Veuillez l'imprimer et la présenter le jour de l'examen.</p>
                    
                    <p>En cas de question ou d'empêchement, veuillez <a href="mailto:examens@alliancefr.be">nous contacter</a> rapidement.</p>
                    
                    <p style="margin-top: 30px;">
                        Cordialement,<br>
                        <strong>L'Alliance Française de Bruxelles-Europe</strong><br>
                        <strong>Pôle des Certifications DELF, DALF, TCF et DFP</strong>
                    </p>
                    
                    <hr style="border: none; border-top: 1px solid #dee2e6; margin: 30px 0;">
                    <p style="font-size: 12px; color: #666;">
                        Cet email a été généré automatiquement le {datetime.now().strftime('%d/%m/%Y à %H:%M')}.
                        Merci de ne pas répondre à cet email automatique.
                    </p>
                </div>
            </body>
            </html>
            """
            
            # Version texte pour compatibilité
            body_text = f"""
            Convocation d'examen
            
            Bonjour {prenom} {nom},
            
            Voici votre convocation concernant la passation des épreuves de l'examen {niveau}.
            
            [IMPORTANT]
            - Présentez-vous 30 minutes avant le début de l'épreuve.
            - Munissez-vous impérativement d'une pièce d'identité officielle avec photo, en cours de validité.
            - Apportez votre convocation imprimée (en pièce jointe).
            - L'usage des téléphones portables et autres appareils connectés est strictement interdit.
            - Toute tentative de fraude est passible d'une interdiction à se présenter à des examens d'état pendant plusieurs années, voire de sanctions pénales pour les cas les plus graves.
            
            Vous trouverez votre convocation officielle en pièce jointe de cet email.
            Veuillez l'imprimer et la présenter le jour de l'examen.
            
            En cas de question ou d'empêchement, veuillez nous contacter rapidement (examens@alliancefr.be).
            
            Cordialement,
            L'Alliance Française de Bruxelles-Europe
            Pôle des Certifications DELF, DALF, TCF et DFP
            
            Cet email a été généré automatiquement le {datetime.now().strftime('%d/%m/%Y à %H:%M')}.
            Merci de ne pas répondre à cet email automatique.
            """
        
        return subject, body_html, body_text
        
    def _encode_attachment(self, file_path: str) -> Tuple[str, str]:
        """
        Encode un fichier en base64 pour l'attachement Mailjet
        
        Args:
            file_path (str): Chemin vers le fichier
            
        Returns:
            tuple: (content_base64, filename)
        """
        with open(file_path, 'rb') as f:
            content = f.read()
            
        content_base64 = base64.b64encode(content).decode('utf-8')
        filename = os.path.basename(file_path)
        
        return content_base64, filename
        
    def send_email(self, candidate_data: Dict, progress_callback=None) -> bool:
        """
        Envoie un email à un candidat via Mailjet
        
        Args:
            candidate_data (Dict): Données du candidat
            progress_callback (function): Fonction de callback pour le suivi
            
        Returns:
            bool: True si l'email a été envoyé avec succès
        """
        if not self.mailjet_client:
            raise Exception("Client Mailjet non initialisé. Authentifiez-vous d'abord.")
            
        try:
            email = str(candidate_data.get('email', '')).strip()
            if not email or '@' not in email:
                raise Exception("Adresse email invalide ou manquante")
                
            # Trouver le fichier PDF
            pdf_path = self._find_pdf_file(candidate_data)
            if not pdf_path:
                raise Exception("Fichier PDF de convocation non trouvé")
                
            # Créer le contenu de l'email
            subject, body_html, body_text = self._create_email_content(candidate_data)
            
            # Encoder la pièce jointe
            attachment_content, attachment_filename = self._encode_attachment(pdf_path)
            
            # Préparer les données pour Mailjet
            data = {
                'Messages': [
                    {
                        "From": {
                            "Email": self.sender_email,
                            "Name": self.sender_name
                        },
                        "To": [
                            {
                                "Email": email,
                                "Name": f"{candidate_data.get('prenom', '')} {candidate_data.get('nom', '')}"
                            }
                        ],
                        "Bcc": [
                            {
                                "Email": "no-reply@alliancefr.be",
                                "Name": "Archive TCF"
                            }
                        ],
                        "Subject": subject,
                        "TextPart": body_text,
                        "HTMLPart": body_html,
                        "Attachments": [
                            {
                                "ContentType": "application/pdf",
                                "Filename": attachment_filename,
                                "Base64Content": attachment_content
                            }
                        ]
                    }
                ]
            }
            
            # Créer des données sécurisées avec le fixer
            safe_data = self.error_fixer.create_safe_mailjet_data(
                candidate_data, self.sender_email, self.sender_name,
                subject, body_html, body_text, pdf_path
            )
            
            # Log pour debug
            self.logger.info(f"📤 Envoi email à {email}")
            self.logger.debug(f"API Key présente: {bool(self.api_key)}")
            self.logger.debug(f"Client Mailjet initialisé: {bool(self.mailjet_client)}")
            
            # Envoyer avec retry
            send_result = self.error_fixer.send_with_retry(self.mailjet_client, safe_data)
            
            if send_result["success"]:
                result = send_result["result"]
                self.logger.info(f"✅ Réponse Mailjet: Status {result.status_code}")
            else:
                raise Exception(send_result["error"])
            
            if result.status_code == 200:
                if progress_callback:
                    progress_callback(f"[OK] Email envoyé à {email} via Mailjet")
                self.logger.info(f"Email envoyé avec succès à {email}")
                return True
            else:
                # Gestion sécurisée des erreurs JSON
                try:
                    error_data = result.json()
                    error_msg = f"Erreur Mailjet {result.status_code}: {error_data}"
                except (ValueError, Exception):
                    # Si la réponse n'est pas du JSON valide
                    error_msg = f"Erreur Mailjet {result.status_code}: {result.text[:200] if hasattr(result, 'text') else 'Réponse non-JSON'}"
                raise Exception(error_msg)
                
        except Exception as e:
            if progress_callback:
                progress_callback(f"[ERREUR] Erreur pour {candidate_data.get('email', 'email inconnu')}: {e}")
            self.logger.error(f"Erreur envoi email: {e}")
            raise
            
    def send_all_emails(self, progress_callback=None) -> int:
        """
        Envoie tous les emails aux candidats
        
        Args:
            progress_callback (function): Fonction de callback pour le suivi
            
        Returns:
            int: Nombre d'emails envoyés avec succès
        """
        if not self.mailjet_client:
            raise Exception("Client Mailjet non initialisé. Authentifiez-vous d'abord.")
            
        try:
            # Charger les candidats depuis le registre JSON (dans le dossier output)
            if progress_callback:
                progress_callback("Chargement des candidats depuis le registre...")
            
            import json
            registry_path = os.path.join(self.pdf_dir, "candidate_pdf_registry.json")
            
            if not os.path.exists(registry_path):
                raise Exception(f"Registre non trouvé: {registry_path}")
            
            with open(registry_path, 'r', encoding='utf-8') as f:
                registry = json.load(f)
            
            # Extraire les candidats du registre
            candidates = []
            for candidate_id, info in registry.items():
                candidate_data = info.get('candidate_info', {})
                if candidate_data.get('email'):  # Uniquement ceux avec email
                    candidates.append(candidate_data)
            
            total_candidates = len(candidates)
            
            if progress_callback:
                progress_callback(f"Trouvé {total_candidates} candidats avec email dans le registre")
                progress_callback("Envoi des emails via Mailjet (HTTPS sécurisé)...")
                
            success_count = 0
            errors = []
            
            # Envoyer un email pour chaque candidat
            for index, candidate_data in enumerate(candidates):
                try:
                    nom = str(candidate_data.get('nom', ''))
                    prenom = str(candidate_data.get('prenom', ''))
                    email = str(candidate_data.get('email', ''))
                    
                    if progress_callback:
                        progress_callback(f"Envoi email {index + 1}/{total_candidates}: {nom} {prenom} ({email})")
                    
                    self.send_email(candidate_data, progress_callback)
                    success_count += 1
                    
                    # Petite pause pour respecter les limites de l'API
                    time.sleep(0.5)
                    
                except Exception as e:
                    error_msg = f"Erreur pour {nom} {prenom} ({email}): {e}"
                    errors.append(error_msg)
                    if progress_callback:
                        progress_callback(f"[ERREUR] {error_msg}")
            
            # Résumé
            if progress_callback:
                progress_callback(f"\n=== RÉSUMÉ ENVOI EMAILS MAILJET ===")
                progress_callback(f"Emails envoyés avec succès: {success_count}/{total_candidates}")
                if errors:
                    progress_callback(f"Erreurs: {len(errors)}")
                    for error in errors:
                        progress_callback(f"  - {error}")
            
            return success_count
            
        except Exception as e:
            if progress_callback:
                progress_callback(f"Erreur critique lors de l'envoi des emails: {e}")
            raise
            
    def test_connection(self) -> bool:
        """
        Test la connexion à l'API Mailjet
        
        Returns:
            bool: True si la connexion fonctionne
        """
        if not self.mailjet_client:
            raise Exception("Client Mailjet non initialisé")
            
        try:
            # Utiliser v3 pour tester la connexion (user endpoint)
            test_client = Client(auth=(self.api_key, self.secret_key), version='v3')
            result = test_client.user.get()
            self.logger.info(f"Test de connexion: Status {result.status_code}")
            return result.status_code == 200
        except Exception as e:
            self.logger.error(f"Test de connexion échoué: {e}")
            return False
            
    def get_account_info(self) -> Dict:
        """
        Récupère les informations du compte Mailjet
        
        Returns:
            Dict: Informations du compte
        """
        if not self.mailjet_client:
            raise Exception("Client Mailjet non initialisé")
            
        try:
            # Utiliser v3 pour récupérer les infos du compte
            test_client = Client(auth=(self.api_key, self.secret_key), version='v3')
            result = test_client.user.get()
            if result.status_code == 200:
                return result.json()
            else:
                raise Exception(f"Erreur lors de la récupération des infos: {result.status_code}")
        except Exception as e:
            self.logger.error(f"Erreur récupération infos compte: {e}")
            raise

if __name__ == "__main__":
    # Test du bridge Mailjet
    import getpass
    
    try:
        bridge = MailjetBridge(
            excel_path="exemple_candidats.xlsx",
            pdf_dir="output",
            sender_email="votre-email@domaine.com",
            sender_name="Service des Examens"
        )
        
        def print_progress(message):
            print(message)
            
        # Configuration initiale (à faire une seule fois)
        setup_new_credentials = input("Configurer de nouveaux credentials Mailjet? (o/N): ").lower() == 'o'
        
        if setup_new_credentials:
            api_key = input("Clé API Mailjet: ")
            secret_key = getpass.getpass("Clé secrète Mailjet: ")
            password = getpass.getpass("Mot de passe pour chiffrer les credentials: ")
            
            bridge.setup_credentials(api_key, secret_key, password)
            print("Credentials configurés avec succès!")
        
        # Authentification
        password = getpass.getpass("Mot de passe de configuration: ")
        bridge._authenticate(password)
        
        # Test de connexion
        print("Test de connexion Mailjet...")
        if bridge.test_connection():
            print("✓ Connexion Mailjet OK")
        else:
            print("✗ Échec de la connexion Mailjet")
            exit(1)
        
        # Afficher les infos du compte
        try:
            account_info = bridge.get_account_info()
            print(f"Compte Mailjet: {account_info}")
        except:
            print("Impossible de récupérer les infos du compte")
        
        # Envoyer les emails
        confirm = input("Envoyer tous les emails? (o/N): ").lower() == 'o'
        if confirm:
            count = bridge.send_all_emails(print_progress)
            print(f"\nTerminé! {count} emails envoyés via Mailjet.")
        
    except Exception as e:
        print(f"Erreur: {e}")
