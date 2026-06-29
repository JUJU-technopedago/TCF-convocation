#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module de génération de PDF robuste pour les convocations d'examens
Compatible avec tous les systèmes sans dépendances externes
"""

import os
import pandas as pd
from pathlib import Path
from datetime import datetime, date
import traceback

# Toujours utiliser xhtml2pdf qui est garanti disponible avec pip
from xhtml2pdf import pisa
from jinja2 import Template, FileSystemLoader, Environment

# Indicateur de moteur PDF
PDF_ENGINE = 'xhtml2pdf'
try:
    print("✅ Utilisation de xhtml2pdf (moteur robuste compatible)")
except UnicodeEncodeError:
    print("[OK] Utilisation de xhtml2pdf (moteur robuste compatible)")

class PDFGenerator:
    def __init__(self, excel_path, template_path, logo_af_path='assets/logoAF.png', logo_delf_path='assets/logoDELF.png', output_dir='output', access_code='', qrcode_path=None, image_a1_path='', image_a2_path='', image_b1_path='', image_b2_path='', image_c1_path='', image_c2_path=''):
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
            image_a1_path (str): Chemin vers l'image du niveau A1
            image_a2_path (str): Chemin vers l'image du niveau A2
            image_b1_path (str): Chemin vers l'image du niveau B1
            image_b2_path (str): Chemin vers l'image du niveau B2
            image_c1_path (str): Chemin vers l'image du niveau C1
            image_c2_path (str): Chemin vers l'image du niveau C2
        """
        self.excel_path = excel_path
        self.logo_af_path = logo_af_path
        self.logo_delf_path = logo_delf_path
        self.output_dir = output_dir
        self.access_code = access_code
        self.qrcode_path = qrcode_path
        self.image_a1_path = image_a1_path
        self.image_a2_path = image_a2_path
        self.image_b1_path = image_b1_path
        self.image_b2_path = image_b2_path
        self.image_c1_path = image_c1_path
        self.image_c2_path = image_c2_path
        self.salle_collective = "1"
        self.salle_individuelle = "1"
        self.template_base_path = template_path  # Garder le chemin de base
        
        # Créer le répertoire de sortie s'il n'existe pas
        os.makedirs(output_dir, exist_ok=True)
        
        # Vérifier si le template est un fichier DOCX ou HTML
        _, ext = os.path.splitext(template_path)
        if ext.lower() == '.docx':
            # Convertir le fichier DOCX en HTML
            try:
                from docx_to_html import docx_to_html
                templates_dir = os.path.join(output_dir, 'templates')
                os.makedirs(templates_dir, exist_ok=True)
                self.template_path = docx_to_html(template_path, templates_dir)
                print(f"Template DOCX converti en HTML: {self.template_path}")
            except Exception as e:
                print(f"Erreur lors de la conversion du template DOCX: {e}")
                # Créer un template HTML de base
                self.template_path = os.path.join(output_dir, 'template_error.html')
                with open(self.template_path, 'w', encoding='utf-8') as f:
                    f.write("""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Convocation</title>
</head>
<body>
    <h1>Convocation DELF/DALF</h1>
    <p>Erreur: Le template n'a pas pu être chargé correctement.</p>
    <p>Nom: {{nom}} {{prenom}}</p>
    <p>Numéro de candidat: {{numero_candidat}}</p>
    <p>Date d'examen: {{date_examen}}</p>
</body>
</html>""")
        else:
            # Utiliser directement le fichier HTML
            self.template_path = template_path
        
        # Charger le template Jinja2
        template_dir = os.path.dirname(self.template_path)
        template_name = os.path.basename(self.template_path)
        
        self.env = Environment(loader=FileSystemLoader(template_dir))
        
        try:
            self.template = self.env.get_template(template_name)
            print(f"✅ Template chargé avec succès: {template_name}")
        except Exception as e:
            print(f"❌ ERREUR lors du chargement du template: {e}")
            print(f"Template path: {self.template_path}")
            print(f"Template dir: {template_dir}")
            print(f"Template name: {template_name}")
            # Créer un template simple en mémoire
            self.template = Template("""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Convocation (Secours)</title>
</head>
<body>
    <h1>Convocation DELF/DALF (Template de secours)</h1>
    <p>Nom: {{nom}} {{prenom}}</p>
    <p>Numéro de candidat: {{numero_candidat}}</p>
    <p>Niveau: {{niveau}}</p>
    <p>Date d'examen collectif: {{date_ep_coll}}</p>
    <p>Heure: {{debut_ep_coll}}</p>
    <p>Salle: {{salle_collective}}</p>
    <p>Date d'examen individuel: {{date_ep_ind}}</p>
    <p>Heure: {{heure_preparation}}</p>
    <p>Salle: {{salle_individuelle}}</p>
</body>
</html>""")
        
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
                return " (Rez-de-chaussée)"
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
        """Formate une date au format français avec nom du jour et du mois (ex: le jeudi 28 février 2026)"""
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
                # Gérer les objets date et datetime
                if hasattr(date_value, 'date'):
                    # C'est un datetime, extraire la date
                    date_obj = date_value
                else:
                    # C'est un objet date, convertir en datetime
                    from datetime import date
                    if isinstance(date_value, date):
                        date_obj = datetime.combine(date_value, datetime.min.time())
                    else:
                        date_obj = date_value
            else:
                return str(date_value)
            
            # Formatter en français avec "le" devant
            try:
                jour_semaine = jours_francais[date_obj.weekday()]
                jour = date_obj.day
                mois = mois_francais[date_obj.month]
                annee = date_obj.year
                
                return f"le {jour_semaine} {jour:02d} {mois} {annee}"
            except Exception as e:
                print(f"Erreur lors du formatage de la date (après parsing): {e}")
                # Fallback: format simple
                return date_obj.strftime('%d/%m/%Y')
            
        except Exception as e:
            print(f"Erreur lors du formatage de la date française: {e}")
            print(f"Détails: {traceback.format_exc()}")
            return str(date_value)
    
    def _format_duration(self, duration_str):
        """Formate les durées pour un affichage harmonisé"""
        if not duration_str:
            return ''
        
        duration_str = str(duration_str).strip()
        
        # Si c'est déjà au format "XX minutes", garder tel quel
        if 'minutes' in duration_str.lower() and not ':' in duration_str:
            return duration_str
        
        # Si c'est au format HH:MM:SS ou HH:MM
        if ':' in duration_str:
            try:
                time_parts = duration_str.split(':')
                if len(time_parts) >= 2:
                    hours = int(time_parts[0])
                    minutes = int(time_parts[1])
                    
                    # Formater selon le format demandé (avec accord singulier/pluriel correct)
                    if hours > 0:
                        if minutes > 0:
                            hour_word = "heure" if hours == 1 else "heures"
                            minute_word = "minute" if minutes == 1 else "minutes"
                            return f"{hours} {hour_word} {minutes} {minute_word}"
                        else:
                            hour_word = "heure" if hours == 1 else "heures"
                            return f"{hours} {hour_word}"
                    else:
                        minute_word = "minute" if minutes == 1 else "minutes"
                        return f"{minutes} {minute_word}"
            except (ValueError, IndexError):
                pass
        
        # Si rien ne correspond, retourner tel quel
        return duration_str
            
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
        data['heure_debut'] = self._ensure_string(row.get('heure_debut', ''))
        data['heure_fin'] = self._ensure_string(row.get('heure_fin', ''))
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
        data['logo_tcf_path'] = os.path.abspath(self.logo_delf_path)  # Alias pour TCF
        
        # Chemins absolus pour les images de niveau
        data['image_a1_path'] = os.path.abspath(self.image_a1_path) if self.image_a1_path and os.path.exists(self.image_a1_path) else ''
        data['image_a2_path'] = os.path.abspath(self.image_a2_path) if self.image_a2_path and os.path.exists(self.image_a2_path) else ''
        data['image_b1_path'] = os.path.abspath(self.image_b1_path) if self.image_b1_path and os.path.exists(self.image_b1_path) else ''
        data['image_b2_path'] = os.path.abspath(self.image_b2_path) if self.image_b2_path and os.path.exists(self.image_b2_path) else ''
        data['image_c1_path'] = os.path.abspath(self.image_c1_path) if self.image_c1_path and os.path.exists(self.image_c1_path) else ''
        data['image_c2_path'] = os.path.abspath(self.image_c2_path) if self.image_c2_path and os.path.exists(self.image_c2_path) else ''
        
        # Données spécifiques DELF/DALF
        niveau = str(row.get('niveau', 'B2')).upper()
        data['niveau'] = niveau
        
        # Déterminer le type d'examen selon le niveau
        if niveau in ['C1', 'C2']:
            data['exam_type'] = 'DALF'
        else:
            data['exam_type'] = 'DELF'
        
        # Variables pour compatibilité avec le template TCF
        # TCF TP EO n'a pas d'épreuve collective - ne pas formater les dates collectives
        tcf_type = row.get('tcf_type', '')
        
        if tcf_type == 'TCF TP EO':
            # Pas d'épreuve collective pour TCF TP EO - tout mettre à None
            data['date_ep_coll'] = None
            data['debut_ep_coll'] = None
            data['date_collective'] = None
            data['date_collective_format'] = None
            data['date_collective_raw'] = None
            data['heure_collective'] = None
            data['salle_collective'] = None
        else:
            # Utiliser le format français pour les dates d'examen collectives
            date_coll_raw = row.get('date_ep_coll', row.get('date_examen', ''))
            data['date_ep_coll'] = self._format_date_french(date_coll_raw)
            data['debut_ep_coll'] = self._ensure_string(row.get('debut_ep_coll', row.get('heure_debut', '')))
            data['date_collective'] = data['date_ep_coll']
            data['date_collective_format'] = data['date_ep_coll']
            data['date_collective_raw'] = date_coll_raw  # Raw datetime for comparison
            data['heure_collective'] = data['debut_ep_coll']
        
        # Dates individuelles (pour tous les types TCF)
        date_ind_raw = row.get('date_ep_ind', row.get('date_examen', ''))
        data['date_ep_ind'] = self._format_date_french(date_ind_raw)
        data['heure_preparation'] = self._ensure_string(row.get('heure_preparation', row.get('heure_debut', '')))
        data['date_individual'] = data['date_ep_ind']
        data['date_individual_format'] = data['date_ep_ind']
        data['date_individual_raw'] = date_ind_raw  # Raw datetime for comparison
        data['heure_individual'] = data['heure_preparation']
        
        # Nettoyer les heures pour enlever les secondes
        if data['debut_ep_coll'] and ':' in str(data['debut_ep_coll']):
            try:
                time_parts = str(data['debut_ep_coll']).split(':')
                if len(time_parts) >= 2:
                    # S'assurer que ce sont des nombres valides
                    hours = str(time_parts[0]).zfill(2)
                    minutes = str(time_parts[1]).zfill(2)
                    data['debut_ep_coll'] = f"{hours}:{minutes}"
                    data['heure_collective'] = data['debut_ep_coll']
            except Exception as e:
                print(f"Erreur formatage heure collective: {e}")
        
        if data['heure_preparation'] and ':' in str(data['heure_preparation']):
            try:
                time_parts = str(data['heure_preparation']).split(':')
                if len(time_parts) >= 2:
                    # S'assurer que ce sont des nombres valides
                    hours = str(time_parts[0]).zfill(2)
                    minutes = str(time_parts[1]).zfill(2)
                    data['heure_preparation'] = f"{hours}:{minutes}"
                    data['heure_individual'] = data['heure_preparation']
            except Exception as e:
                print(f"Erreur formatage heure individuelle: {e}")
        
        # DEBUG: Afficher le formatage des dates
        print(f"🔍 DEBUG: Formatage des dates pour {data.get('nom', 'inconnu')}:")
        print(f"  - date_ep_coll brute: {row.get('date_ep_coll', 'N/A')}")
        print(f"  - date_ep_coll formatée: {data['date_ep_coll']}")
        print(f"  - date_collective_format: {data['date_collective_format']}")
        print(f"  - date_individual_format: {data['date_individual_format']}")
        print(f"  - heure_collective: {data['heure_collective']}")
        print(f"  - heure_individual: {data['heure_individual']}")
        
        # Variables pour les candidats à besoins spéciaux
        data['tiers_temps'] = row.get('tiers_temps', False)
        data['fin_ep_coll_affichage'] = self._ensure_string(row.get('fin_ep_coll_affichage', row.get('fin_ep_coll', '')))
        
        # Données spécifiques TCF
        data['tcf_type'] = row.get('tcf_type', 'TCF TP COMPLET')  # Défaut
        data['type_tcf'] = data['tcf_type']  # Alias pour compatibilité template
        
        # DEBUG: Vérifier que les bonnes variables sont créées
        print(f"🔍 DEBUG: Variables TCF créées:")
        print(f"  - tcf_type: {data['tcf_type']}")
        print(f"  - type_tcf: {data['type_tcf']}")
        
        # ====== GESTION DES CANDIDATS MULTI-ÉPREUVES ======
        if row.get('is_multi_exam', False) and 'exams' in row:
            print(f"🔄 MULTI-ÉPREUVE détecté pour {data['nom']} {data['prenom']}")
            exams = row['exams']
            
            # Marquer comme multi-épreuves dans le template
            data['tcf_type'] = 'TCF TP MULTI'
            data['type_tcf'] = 'TCF TP MULTI'
            
            # Première épreuve (déjà triée chronologiquement)
            first_exam = exams[0]
            data['primary_exam_type'] = first_exam['tcf_type']
            data['first_exam_date'] = first_exam.get('exam_date')
            data['first_exam_date_format'] = self._format_date_french(first_exam.get('exam_date')) if first_exam.get('exam_date') else 'N/A'
            
            # Déterminer si c'est une épreuve individuelle ou collective
            if first_exam['tcf_type'] == 'TCF TP EO':
                data['first_exam_is_individual'] = True
                data['first_exam_time'] = first_exam.get('time_individual', 'N/A')
                data['first_exam_duration'] = first_exam.get('individual_duration', '12 minutes')
            else:
                data['first_exam_is_individual'] = False
                data['first_exam_time'] = first_exam.get('time_collective', 'N/A')
                data['first_exam_duration'] = first_exam.get('collective_duration', 'N/A')
            
            # Ajouter l'info d'étage à la salle
            salle_num = first_exam.get('exam_location', 'N/A')
            data['first_exam_salle'] = salle_num + self._get_floor_info(salle_num) if salle_num != 'N/A' else 'N/A'
            
            # Deuxième épreuve (si existe)
            if len(exams) > 1:
                second_exam = exams[1]
                data['secondary_exam_type'] = second_exam['tcf_type']
                data['second_exam_date'] = second_exam.get('exam_date')
                data['second_exam_date_format'] = self._format_date_french(second_exam.get('exam_date')) if second_exam.get('exam_date') else 'N/A'
                
                if second_exam['tcf_type'] == 'TCF TP EO':
                    data['second_exam_is_individual'] = True
                    data['second_exam_time'] = second_exam.get('time_individual', 'N/A')
                    data['second_exam_duration'] = second_exam.get('individual_duration', '12 minutes')
                else:
                    data['second_exam_is_individual'] = False
                    data['second_exam_time'] = second_exam.get('time_collective', 'N/A')
                    data['second_exam_duration'] = second_exam.get('collective_duration', 'N/A')
                
                # Ajouter l'info d'étage à la salle
                salle_num = second_exam.get('exam_location', 'N/A')
                data['second_exam_salle'] = salle_num + self._get_floor_info(salle_num) if salle_num != 'N/A' else 'N/A'
                
                print(f"  ✅ Première épreuve: {data['primary_exam_type']} à {data['first_exam_time']}")
                print(f"  ✅ Deuxième épreuve: {data['secondary_exam_type']} à {data['second_exam_time']}")
            else:
                data['secondary_exam_type'] = None
        
        # ====== GESTION DES CANDIDATS MONO-ÉPREUVE (logique existante) ======
        else:
            # Autres données spécifiques TCF avec formatage des durées
            if tcf_type == 'TCF TP EO':
                data['duree_collective'] = None
                data['duree_individuelle'] = self._format_duration(row.get('duree_individuelle', '12 minutes'))
                data['has_individual_exam'] = True
            elif tcf_type == 'TCF TP OBLIGATOIRE':
                data['duree_collective'] = self._format_duration(row.get('duree_collective', '1h35'))
                data['duree_individuelle'] = None
                data['has_individual_exam'] = False
            elif tcf_type == 'TCF TP EE':
                data['duree_collective'] = self._format_duration(row.get('duree_collective', '1h00'))
                data['duree_individuelle'] = None
                data['has_individual_exam'] = False
            else:
                data['duree_collective'] = self._format_duration(row.get('duree_collective', '2h30'))
                data['duree_individuelle'] = self._format_duration(row.get('duree_individuelle', '12 minutes'))
                data['has_individual_exam'] = row.get('has_individual_exam', True)
        
        # Code d'accès aux locaux
        data['access_code'] = self.access_code
        
        # Chemin vers l'image QR code
        data['qrcode_path'] = self.qrcode_path if (self.qrcode_path and os.path.exists(self.qrcode_path)) else None
        
        return data
    
    def _select_template(self, tcf_type):
        """Retourne toujours le template de base (modèle unique)"""
        # Utiliser toujours le template de base chargé à l'initialisation
        return self.template
        
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
            
            # Sélectionner le bon template selon le type TCF
            tcf_type = candidate_data.get('tcf_type', '')
            template_to_use = self._select_template(tcf_type)
            
            # Générer le HTML
            html_content = template_to_use.render(**template_data)
            
            # DEBUG: Afficher des informations sur le rendu
            print(f"🔍 DEBUG: Template data pour {template_data.get('nom', 'inconnu')}:")
            print(f"  - type_tcf: {template_data.get('type_tcf', 'N/A')}")
            print(f"  - niveau: {template_data.get('niveau', 'N/A')}")
            print(f"  - Début HTML généré: {html_content[:200]}...")
            
            # Si c'est un examen TCF, vérifier que le bon titre apparaît
            if 'tcf' in self.template_path.lower():
                if 'TCF CANADA' in html_content:
                    print("✅ TCF CANADA détecté dans le HTML")
                elif 'TCF TP COMPLET' in html_content:
                    print("✅ TCF TP COMPLET détecté dans le HTML")
                elif 'TCF IRN' in html_content:
                    print("✅ TCF IRN détecté dans le HTML")
                elif 'Examen TCF' in html_content:
                    print("⚠️ Examen TCF générique détecté - problème avec les conditions du template")
                else:
                    print("❌ Aucun titre TCF détecté dans le HTML")
            
            # Nom du fichier de sortie
            if not output_filename:
                try:
                    # Obtenir les données nom et prénom
                    nom = template_data.get('nom', '').strip().upper()  # Nom en majuscules
                    prenom = template_data.get('prenom', '').strip().capitalize()  # Prénom avec première lettre en majuscule
                    numero = template_data.get('numero_candidat', '').strip()
                    niveau = template_data.get('niveau', '').strip()
                    
                    # Nettoyer le nom et prénom pour le nom de fichier
                    safe_nom = nom.replace(' ', '')
                    safe_prenom = prenom.replace(' ', '')
                    
                    # Version plus simple et robuste pour les caractères spéciaux
                    def clean_text(text):
                        safe_chars = []
                        for c in text:
                            if c.isalnum() or c in '_-':
                                safe_chars.append(c)
                            # Certains caractères spéciaux peuvent être conservés
                            elif c in 'ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖØÙÚÛÜÝÞßàáâãäåæçèéêëìíîïðñòóôõöøùúûüýþÿĞğİıŞşÇçÜüÖö':
                                safe_chars.append(c)
                        return ''.join(safe_chars)
                    
                    safe_nom = clean_text(safe_nom)
                    safe_prenom = clean_text(safe_prenom)
                    safe_name = f"{safe_nom}_{safe_prenom}"
                    
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
                
                # S'assurer que html_content est bien une chaîne de caractères
                if not isinstance(html_content, str):
                    html_content = str(html_content)
                
                # Ouvrir le fichier en mode binaire (important pour PDF)
                with open(output_path, "w+b") as result_file:
                    try:
                        pisa_status = pisa.CreatePDF(
                            src=html_content,         # Contenu HTML source
                            dest=result_file,         # Fichier de destination
                            encoding='utf-8'          # Encodage UTF-8 pour les caractères spéciaux
                            # Suppression du paramètre path qui peut causer des problèmes
                        )
                    except (TypeError, ValueError) as te:
                        print(f"Erreur de type dans pisa.CreatePDF: {te}")
                        # Réessayer en convertissant explicitement le HTML en string
                        html_content_str = str(html_content) if html_content else ""
                        pisa_status = pisa.CreatePDF(
                            src=html_content_str,
                            dest=result_file,
                            encoding='utf-8'
                        )
                    
                if pisa_status.err:
                    print(f"Détails de l'erreur pisa: {pisa_status.err}")
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
                        safe_nom = nom.upper().replace(' ', '')
                        safe_prenom = prenom.capitalize().replace(' ', '')
                        
                        def clean_text(text):
                            return ''.join(c for c in text if c.isalnum() or c in '_-' or c in 'ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖØÙÚÛÜÝÞßàáâãäåæçèéêëìíîïðñòóôõöøùúûüýþÿĞğİıŞşÇçÜüÖö')
                        
                        safe_nom = clean_text(safe_nom)
                        safe_prenom = clean_text(safe_prenom)
                        safe_name = f"{safe_nom}_{safe_prenom}"
                        output_filename = f"convocation_TCF_{safe_name}_{numero_candidat}_{niveau}.pdf"
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
                progress_callback(f"\n=== RÉSUMÉ ===")
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
            
    def _ensure_string(self, value):
        """Garantit qu'une valeur est une chaîne de caractères"""
        if value is None:
            return ''
        if isinstance(value, (int, float)):
            return str(value)
        if isinstance(value, datetime):
            return value.strftime('%H:%M')
        return str(value)
            
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
        print(f"\nTerminé! {count} PDF générés.")
    except Exception as e:
        print(f"Erreur: {e}")

    def _ensure_string(self, value):
        """Garantit qu'une valeur est une chaîne de caractères"""
        if value is None:
            return ''
        if isinstance(value, (int, float)):
            return str(value)
        if isinstance(value, datetime):
            return value.strftime('%H:%M')
        return str(value)
    