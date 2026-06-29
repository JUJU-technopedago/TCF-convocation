#!/usr/bin/env python3
"""
Test du système de chargement mailjet_bridge sans cryptography
"""

import pandas as pd
import logging
import os

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class TestMailjetBridge:
    def __init__(self, excel_path: str):
        self.excel_path = excel_path
        self.logger = logging.getLogger(__name__)
    
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
    
    def _is_jury_file(self) -> bool:
        """Vérifie si le fichier Excel est un fichier de jurys DELF/DALF"""
        try:
            xl = pd.ExcelFile(self.excel_path)
            sheet_names = [sheet.strip().upper() for sheet in xl.sheet_names]
            
            # Vérifier la présence d'un onglet ADMIN et de niveaux DELF
            has_admin_sheet = 'ADMIN' in sheet_names
            niveau_sheets = [s for s in sheet_names if any(niveau in s for niveau in ['A1', 'A2', 'B1', 'B2', 'C1', 'C2'])]
            
            # Minimum 2 niveaux et un onglet ADMIN
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
                # Pour l'instant, pas d'implémentation TCF dans ce test
                return pd.DataFrame()
                
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

if __name__ == "__main__":
    excel_file = 'juries_20250919_162205.xlsx'
    
    # Test du système
    bridge = TestMailjetBridge(excel_file)
    
    print(f"Test avec: {excel_file}")
    print(f"Est fichier TCF: {bridge._is_tcf_file()}")
    print(f"Est fichier de jurys: {bridge._is_jury_file()}")
    
    try:
        data = bridge._load_excel_data()
        print(f"\n✅ Chargement réussi: {len(data)} candidats")
        
        if len(data) > 0:
            print("Colonnes:", list(data.columns))
            print("\nPremiers candidats:")
            for i, row in data.head(5).iterrows():
                print(f"{i+1}. {row.get('nom', '')} {row.get('prenom', '')} - {row.get('email', '')} ({row.get('niveau', '')})")
    except Exception as e:
        print(f"❌ Erreur: {e}")