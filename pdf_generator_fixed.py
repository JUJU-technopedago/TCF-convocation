#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module de génération de PDF robuste pour les convocations d'examens
Compatible avec tous les systèmes sans dépendances externes
"""

import os
import pandas as pd
from pathlib import Path
from datetime import datetime
import traceback

# Toujours utiliser xhtml2pdf qui est garanti disponible avec pip
from xhtml2pdf import pisa
from jinja2 import Template, FileSystemLoader, Environment

# Indicateur de moteur PDF
PDF_ENGINE = 'xhtml2pdf'
print("✅ Utilisation de xhtml2pdf (moteur robuste compatible)")

class PDFGenerator:
    def __init__(self, excel_path, template_path, logo_af_path='assets/logoAF.png', logo_delf_path='assets/logoDELF.png', output_dir='output', access_code='', qrcode_path=None):
        """
        Initialise le générateur de PDF
        
        Args:
            excel_path (str): Chemin vers le fichier Excel
            template_path (str): Chemin vers le template HTML
            logo_af_path (str): Chemin vers le logo Alliance Française
            logo_delf_path (str): Chemin vers le logo DELF
            output_dir (str): Répertoire de sortie pour les PDF
            access_code (str): Code d'accès aux locaux
            qrcode_path (str): Chemin vers l'image QR code
        """
        self.excel_path = excel_path
        self.template_path = template_path
        self.logo_af_path = logo_af_path
        self.logo_delf_path = logo_delf_path
        self.output_dir = output_dir
        self.access_code = access_code
        self.qrcode_path = qrcode_path
        self.salle_collective = "1"
        self.salle_individuelle = "1"
        
        # Créer le répertoire de sortie s'il n'existe pas
        os.makedirs(output_dir, exist_ok=True)
        
        # Charger le template Jinja2
        template_dir = os.path.dirname(template_path)
        template_name = os.path.basename(template_path)
        
        self.env = Environment(loader=FileSystemLoader(template_dir))
        self.template = self.env.get_template(template_name)
        
        # Vérifier que les logos existent
        if not os.path.exists(self.logo_af_path):
            print(f"Attention: Logo AF non trouvé à {self.logo_af_path}")
        if not os.path.exists(self.logo_delf_path):
            print(f"Attention: Logo DELF non trouvé à {self.logo_delf_path}")
        
    def _get_floor_info(self, salle_number):
        """Retourne l'information d'étage en fonction du numéro de salle"""
        try:
            num_salle = int(salle_number)
            if 1 <= num_salle <= 14:
                return " (rez-de-chaussée)"
            elif 15 <= num_salle <= 22:
                return " (1<sup>er</sup> étage)"
            else:
                return ""
        except ValueError:
            return ""
        
    def _load_logo(self, logo_path):
        """Charge le logo SVG et le retourne comme string"""
        try:
            if os.path.exists(logo_path):
                with open(logo_path, 'r', encoding='utf-8') as f:
                    return f.read()
            else:
                return None
        except Exception as e:
            print(f"Erreur lors du chargement du logo {logo_path}: {e}")
            return None
            
    def _load_excel_data(self):
        """Charge les données depuis le fichier Excel"""
        try:
            # Vérifier si c'est un fichier de jurys DELF (structure spéciale)
            if self._is_jury_excel_file():
                # Utiliser le processeur de jurys
                from jury_excel_processor import JuryExcelProcessor
                processor = JuryExcelProcessor(self.excel_path)
                candidates = processor.get_all_candidates()
                
                if not candidates:
                    raise Exception("Aucun candidat trouvé dans le fichier de jurys")
                
                # Convertir en DataFrame
                df = pd.DataFrame(candidates)
                return df
            
            else:
                # Traitement standard pour les fichiers Excel classiques
                try:
                    df = pd.read_excel(self.excel_path, engine='openpyxl')
                except:
                    df = pd.read_excel(self.excel_path, engine='xlrd')
                    
                # Nettoyer les noms de colonnes (supprimer espaces, caractères spéciaux)
                df.columns = df.columns.str.strip().str.lower()
                df.columns = df.columns.str.replace(' ', '_').str.replace('é', 'e').str.replace('è', 'e')
                df.columns = df.columns.str.replace('à', 'a').str.replace('ç', 'c').str.replace('ù', 'u')
                
                # Remplacer les valeurs NaN par des chaînes vides
                df = df.fillna('')
                
                return df
            
        except Exception as e:
            raise Exception(f"Erreur lors de la lecture du fichier Excel: {e}")
    
    def _is_jury_excel_file(self):
        """Détecte si le fichier Excel est un fichier de jurys DELF"""
        try:
            # Lire les noms des feuilles
            excel_file = pd.ExcelFile(self.excel_path, engine='openpyxl')
            sheet_names = excel_file.sheet_names
            
            # Vérifier si on a des feuilles avec "Niveau" dans le nom
            niveau_sheets = [name for name in sheet_names if name.startswith('Niveau ')]
            
            # Si on a au moins 2 feuilles de niveau, c'est probablement un fichier de jurys
            return len(niveau_sheets) >= 2
            
        except Exception as e:
            # En cas d'erreur, traiter comme un fichier standard
            return False
            
    def _format_date(self, date_value):
        """Formate une date pour l'affichage"""
        if pd.isna(date_value) or date_value == '':
            return ''
            
        try:
            if isinstance(date_value, str):
                # Essayer différents formats de date
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

    def _format_birth_date(self, date_value):
        """Formate une date de naissance au format '12 février 1997'"""
        if pd.isna(date_value) or date_value == '':
            return ''

        mois_francais = {
            1: 'janvier', 2: 'février', 3: 'mars', 4: 'avril', 5: 'mai', 6: 'juin',
            7: 'juillet', 8: 'août', 9: 'septembre', 10: 'octobre', 11: 'novembre', 12: 'décembre'
        }

        try:
            if isinstance(date_value, str) and any(mois in date_value.lower() for mois in mois_francais.values()):
                return date_value

            date_obj = pd.to_datetime(date_value, errors='coerce', dayfirst=True)
            if pd.isna(date_obj):
                return str(date_value)

            return f"{date_obj.day:02d} {mois_francais[date_obj.month]} {date_obj.year}"
        except Exception:
            return str(date_value)
    
    def _format_date_french(self, date_value):
        """Formate une date au format français avec nom du jour et du mois (ex: lundi 01 janvier 2000)"""
        if pd.isna(date_value) or date_value == '':
            return ''
            
        # Dictionnaire des mois en français
        mois_francais = {
            1: 'janvier', 2: 'février', 3: 'mars', 4: 'avril', 5: 'mai', 6: 'juin',
            7: 'juillet', 8: 'août', 9: 'septembre', 10: 'octobre', 11: 'novembre', 12: 'décembre'
        }
        
        # Dictionnaire des jours en français
        jours_francais = {
            0: 'lundi', 1: 'mardi', 2: 'mercredi', 3: 'jeudi', 4: 'vendredi', 5: 'samedi', 6: 'dimanche'
        }
        
        try:
            # Vérifier si c'est une date déjà formatée en français
            if isinstance(date_value, str) and any(jour in date_value.lower() for jour in jours_francais.values()):
                return date_value  # Déjà au format français
                
            date_obj = None
            
            if isinstance(date_value, str):
                # Essayer différents formats de date
                for fmt in ['%Y-%m-%d', '%d/%m/%Y', '%d-%m-%Y']:
                    try:
                        date_obj = datetime.strptime(date_value, fmt)
                        break
                    except Exception:
                        continue
                        
                if date_obj is None:
                    return str(date_value)
                    
            elif hasattr(date_value, 'strftime'):
                date_obj = date_value
            else:
                return str(date_value)
            
            # Formatter en français
            try:
                jour_semaine = jours_francais[date_obj.weekday()]
                jour = date_obj.day
                mois = mois_francais[date_obj.month]
                annee = date_obj.year
                
                return f"{jour_semaine} {jour:02d} {mois} {annee}"
            except Exception as e:
                print(f"Erreur lors du formatage de la date (après parsing): {e}")
                # Fallback: format simple
                return date_obj.strftime('%d/%m/%Y')
            
        except Exception as e:
            print(f"Erreur lors du formatage de la date française: {e}")
            print(f"Détails: {traceback.format_exc()}")
            return str(date_value)
            
    def _prepare_template_data(self, row):
        """Prépare les données pour le template"""
        data = {}
        
        # Données du candidat (colonnes obligatoires)
        data['nom'] = str(row.get('nom', ''))
        data['prenom'] = str(row.get('prenom', ''))
        data['numero_candidat'] = str(row.get('numero_candidat', ''))
        data['email'] = str(row.get('email', ''))
        data['date_naissance'] = self._format_birth_date(row.get('date_naissance', ''))
        data['telephone'] = str(row.get('telephone', ''))
        
        # Données de l'examen (colonnes obligatoires)
        data['matiere'] = str(row.get('matiere', ''))
        data['date_examen'] = self._format_date(row.get('date_examen', ''))
        data['heure_debut'] = str(row.get('heure_debut', ''))
        data['heure_fin'] = str(row.get('heure_fin', ''))
        data['duree'] = str(row.get('duree', ''))
        data['salle'] = str(row.get('salle', ''))
        
        # Récupérer les numéros de salle et ajouter les informations d'étage
        salle_coll = str(row.get('salle_collective', self.salle_collective))
        salle_ind = str(row.get('salle_individuelle', self.salle_individuelle))
        
        # Formater les salles avec l'information d'étage
        data['salle_collective'] = salle_coll + self._get_floor_info(salle_coll)
        data['salle_individuelle'] = salle_ind + self._get_floor_info(salle_ind)
        
        # Données optionnelles
        data['batiment'] = str(row.get('batiment', ''))
        data['surveillant'] = str(row.get('surveillant', ''))
        data['materiel_autorise'] = str(row.get('materiel_autorise', ''))
        data['instructions_supplementaires'] = str(row.get('instructions_supplementaires', ''))
        data['temps_sortie_min'] = str(row.get('temps_sortie_min', '1 heure'))
        
        # Données de l'institution
        data['institution_name'] = str(row.get('institution_name', 'ÉTABLISSEMENT D\'ENSEIGNEMENT'))
        data['institution_address'] = str(row.get('institution_address', ''))
        data['institution_city'] = str(row.get('institution_city', ''))
        data['institution_postal'] = str(row.get('institution_postal', ''))
        data['institution_phone'] = str(row.get('institution_phone', ''))
        data['contact_urgence'] = str(row.get('contact_urgence', ''))
        
        # Données système
        data['date_generation'] = datetime.now().strftime('%d/%m/%Y à %H:%M')
        data['reference'] = f"CONV-{data['numero_candidat']}-{datetime.now().strftime('%Y%m%d')}"
        
        # Chemins absolus pour les logos (nécessaire pour xhtml2pdf)
        data['logo_af_path'] = os.path.abspath(self.logo_af_path)
        data['logo_delf_path'] = os.path.abspath(self.logo_delf_path)
        
        # Données spécifiques DELF/DALF
        niveau = str(row.get('niveau', 'B2')).upper()
        data['niveau'] = niveau
        
        # Déterminer le type d'examen selon le niveau
        if niveau in ['C1', 'C2']:
            data['exam_type'] = 'DALF'
        else:
            data['exam_type'] = 'DELF'
        
        # Utiliser le format français pour les dates d'examen dans les convocations
        data['date_ep_coll'] = self._format_date_french(row.get('date_ep_coll', row.get('date_examen', '')))
        data['debut_ep_coll'] = str(row.get('debut_ep_coll', row.get('heure_debut', '')))
        data['date_ep_ind'] = self._format_date_french(row.get('date_ep_ind', row.get('date_examen', '')))
        data['heure_preparation'] = str(row.get('heure_preparation', row.get('heure_debut', '')))
        
        # Variables pour les candidats à besoins spéciaux
        data['tiers_temps'] = row.get('tiers_temps', False)
        data['fin_ep_coll_affichage'] = row.get('fin_ep_coll_affichage', row.get('fin_ep_coll', ''))
        
        # Code d'accès aux locaux
        data['access_code'] = self.access_code
        
        # Chemin vers l'image QR code
        data['qrcode_path'] = self.qrcode_path if (self.qrcode_path and os.path.exists(self.qrcode_path)) else None
        
        return data
        
    def generate_pdf(self, candidate_data, output_filename=None):
        """
        Génère un PDF pour un candidat
        
        Args:
            candidate_data (dict): Données du candidat
            output_filename (str): Nom du fichier de sortie (optionnel)
            
        Returns:
            str: Chemin vers le fichier PDF généré
        """
        try:
            # Préparer les données pour le template
            template_data = self._prepare_template_data(candidate_data)
            
            # Générer le HTML
            html_content = self.template.render(**template_data)
            
            # Nom du fichier de sortie
            if not output_filename:
                try:
                    # Obtenir les données nom et prénom
                    nom = template_data.get('nom', '').strip()
                    prenom = template_data.get('prenom', '').strip()
                    numero = template_data.get('numero_candidat', '').strip()
                    niveau = template_data.get('niveau', '').strip()
                    
                    # Nettoyer le nom et prénom pour le nom de fichier
                    safe_name = f"{nom}_{prenom}".replace(' ', '_')
                    
                    # Version plus simple et robuste pour les caractères spéciaux
                    safe_chars = []
                    for c in safe_name:
                        if c.isalnum() or c in '_-':
                            safe_chars.append(c)
                        # Certains caractères spéciaux peuvent être conservés
                        elif c in 'ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖØÙÚÛÜÝÞßàáâãäåæçèéêëìíîïðñòóôõöøùúûüýþÿĞğİıŞşÇçÜüÖö':
                            safe_chars.append(c)
                    
                    safe_name = ''.join(safe_chars)
                    
                    # Fallback si le nom est vide après nettoyage
                    if not safe_name:
                        safe_name = f"candidat_{numero}"
                    
                    output_filename = f"convocation_{safe_name}_{numero}.pdf"
                    
                    # Vérifier la longueur du nom de fichier (max 255 caractères)
                    if len(output_filename) > 250:
                        # Tronquer le nom si nécessaire
                        output_filename = output_filename[:240] + ".pdf"
                    
                except Exception as e:
                    print(f"Erreur lors de la génération du nom de fichier: {e}")
                    # Fallback: nom de fichier sans caractères spéciaux
                    output_filename = f"convocation_{template_data.get('numero_candidat', 'inconnu')}.pdf"
            
            output_path = os.path.join(self.output_dir, output_filename)
            
            # Générer le PDF avec xhtml2pdf (solution robuste)
            print(f"Génération PDF avec xhtml2pdf...")
            
            try:
                # Créer un chemin absolu pour les ressources du template
                base_path = os.path.dirname(os.path.abspath(self.template_path))
                
                # Ouvrir le fichier en mode binaire (important pour PDF)
                with open(output_path, "w+b") as result_file:
                    pisa_status = pisa.CreatePDF(
                        src=html_content,         # Contenu HTML source
                        dest=result_file,         # Fichier de destination
                        encoding='utf-8',         # Encodage UTF-8 pour les caractères spéciaux
                        path=base_path            # Chemin pour les ressources relatives
                    )
                    
                if pisa_status.err:
                    raise Exception(f"Erreur xhtml2pdf: {pisa_status.err}")
                
                print(f"✅ PDF généré avec succès: {output_path}")
                return output_path
                
            except Exception as e:
                raise Exception(f"Erreur lors de la génération PDF: {e}")
            
        except Exception as e:
            raise Exception(f"Erreur lors de la génération du PDF pour {candidate_data.get('nom', 'candidat inconnu')}: {e}")
            
    def _detect_duplicate_candidates(self, df):
        """
        Détecte les candidats en double inscription (même nom, date de naissance, numéro de candidat)
        
        Args:
            df (DataFrame): Données des candidats
            
        Returns:
            dict: Dictionnaire des candidats dupliqués avec leurs niveaux
        """
        duplicates = {}
        
        # Grouper par identifiant unique (nom, prenom, date_naissance, numero_candidat)
        for index, row in df.iterrows():
            nom = str(row.get('nom', '')).upper().strip()
            prenom = str(row.get('prenom', '')).strip()
            date_naissance = str(row.get('date_naissance', '')).strip()
            numero_candidat = str(row.get('numero_candidat', '')).strip()
            niveau = str(row.get('niveau', 'B2')).upper()
            
            # Créer une clé unique pour identifier le candidat
            candidate_key = f"{nom}_{prenom}_{date_naissance}_{numero_candidat}"
            
            if candidate_key not in duplicates:
                duplicates[candidate_key] = {
                    'count': 0,
                    'niveaux': [],
                    'rows': []
                }
            
            duplicates[candidate_key]['count'] += 1
            duplicates[candidate_key]['niveaux'].append(niveau)
            duplicates[candidate_key]['rows'].append(index)
        
        # Retourner seulement les vrais doublons (count > 1)
        real_duplicates = {k: v for k, v in duplicates.items() if v['count'] > 1}
        
        return real_duplicates

    def generate_all_pdfs(self, progress_callback=None):
        """
        Génère tous les PDF à partir du fichier Excel
        
        Args:
            progress_callback (function): Fonction de callback pour le suivi de progression
            
        Returns:
            int: Nombre de PDF générés avec succès
        """
        try:
            # Charger les données Excel
            if progress_callback:
                progress_callback("Chargement des données Excel...")
            
            df = self._load_excel_data()
            total_candidates = len(df)
            
            if progress_callback:
                progress_callback(f"Trouvé {total_candidates} candidats dans le fichier Excel")
            
            # Détecter les candidats en double inscription
            duplicates = self._detect_duplicate_candidates(df)
            
            if duplicates:
                duplicate_count = sum(v['count'] for v in duplicates.values())
                unique_duplicates = len(duplicates)
                if progress_callback:
                    progress_callback(f"Détecté {unique_duplicates} candidats avec double inscription ({duplicate_count} inscriptions au total)")
                    for candidate_key, info in duplicates.items():
                        parts = candidate_key.split('_')
                        if len(parts) >= 2:
                            nom, prenom = parts[0], parts[1]
                            niveaux = ', '.join(info['niveaux'])
                            progress_callback(f"  - {nom} {prenom}: niveaux {niveaux}")
            
            success_count = 0
            errors = []
            
            # Générer un PDF pour chaque candidat
            for index, row in df.iterrows():
                try:
                    if progress_callback:
                        progress_callback(f"Génération PDF {index + 1}/{total_candidates}: {row.get('nom', '')} {row.get('prenom', '')}")
                    
                    # Déterminer si ce candidat a une double inscription
                    nom = str(row.get('nom', '')).upper().strip()
                    prenom = str(row.get('prenom', '')).strip()
                    date_naissance = str(row.get('date_naissance', '')).strip()
                    numero_candidat = str(row.get('numero_candidat', '')).strip()
                    niveau = str(row.get('niveau', 'B2')).upper()
                    
                    candidate_key = f"{nom}_{prenom}_{date_naissance}_{numero_candidat}"
                    
                    # Générer le nom de fichier approprié
                    if candidate_key in duplicates:
                        # Candidat en double inscription - ajouter le niveau
                        safe_name = f"{nom}_{prenom}".replace(' ', '_')
                        safe_name = ''.join(c for c in safe_name if c.isalnum() or c in '_-' or c in 'ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖØÙÚÛÜÝÞßàáâãäåæçèéêëìíîïðñòóôõöøùúûüýþÿĞğİıŞşÇçÜüÖö')
                        output_filename = f"convocation_{safe_name}_{numero_candidat}_{niveau}.pdf"
                    else:
                        # Candidat unique - nom de fichier standard
                        output_filename = None  # Utiliser le système par défaut
                    
                    pdf_path = self.generate_pdf(row, output_filename)
                    success_count += 1
                    
                    if progress_callback:
                        progress_callback(f"✓ PDF généré: {os.path.basename(pdf_path)}")
                        
                except Exception as e:
                    error_msg = f"Erreur pour {row.get('nom', '')} {row.get('prenom', '')}: {e}"
                    errors.append(error_msg)
                    if progress_callback:
                        progress_callback(f"✗ {error_msg}")
            
            # Résumé
            if progress_callback:
                progress_callback(f"
=== RÉSUMÉ ===")
                progress_callback(f"PDF générés avec succès: {success_count}/{total_candidates}")
                if duplicates:
                    progress_callback(f"Candidats avec double inscription: {len(duplicates)}")
                if errors:
                    progress_callback(f"Erreurs: {len(errors)}")
                    for error in errors:
                        progress_callback(f"  - {error}")
            
            return success_count
            
        except Exception as e:
            if progress_callback:
                progress_callback(f"Erreur critique: {e}")
            raise
            
    def get_candidate_list(self):
        """
        Retourne la liste des candidats du fichier Excel
        
        Returns:
            list: Liste des dictionnaires contenant les données des candidats
        """
        try:
            df = self._load_excel_data()
            return df.to_dict('records')
        except Exception as e:
            raise Exception(f"Erreur lors de la lecture des candidats: {e}")

if __name__ == "__main__":
    # Test du générateur
    generator = PDFGenerator(
        excel_path="exemple_candidats.xlsx",
        template_path="templates/convocation_template.html",
        logo_path="assets/logo.svg",
        output_dir="output"
    )
    
    def print_progress(message):
        print(message)
    
    try:
        count = generator.generate_all_pdfs(print_progress)
        print(f"
Terminé! {count} PDF générés.")
    except Exception as e:
        print(f"Erreur: {e}")
