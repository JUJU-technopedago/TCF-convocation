#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Processeur Excel spécialisé pour les fichiers TCF
Gère la structure spécifique des jurys TCF avec épreuves collectives et individuelles
"""

import pandas as pd
import re
from datetime import datetime, time, timedelta
import logging

class TCFExcelProcessor:
    """
    Processeur pour les fichiers Excel TCF avec structure jury/candidats
    """
    
    # Durées des épreuves par déclinaison TCF
    TCF_DURATIONS = {
        'TCF CANADA': {
            'collective_duration': '2h47',
            'individual_duration': '12 minutes',
            'has_individual': True
        },
        'TCF TP COMPLET': {
            'collective_duration': '2h35', 
            'individual_duration': '12 minutes',
            'has_individual': True
        },
        'TCF TP OBLIGATOIRE': {
            'collective_duration': '1h35',
            'individual_duration': None,
            'has_individual': False
        },
        'TCF TP EE': {
            'collective_duration': '1h00',
            'individual_duration': None,
            'has_individual': False,
            'is_optional': True,
            'full_name': 'TCF TP Expression Écrite'
        },
        'TCF TP EO': {
            'collective_duration': None,
            'individual_duration': '12 minutes',
            'has_individual': True,
            'is_optional': True,
            'full_name': 'TCF TP Expression Orale'
        },
        'TCF IRN': {
            'collective_duration': '1h35',
            'individual_duration': '10 minutes', 
            'has_individual': True
        }
    }
    
    def __init__(self, excel_path):
        """
        Initialise le processeur TCF
        
        Args:
            excel_path (str): Chemin vers le fichier Excel TCF
        """
        self.excel_path = excel_path
        self.candidates = []
        self.jurys_data = {}
        
        # Configuration du logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def _format_birth_date(self, date_value):
        """Formate une date de naissance au format '12 février 1997'"""
        if date_value is None:
            return ""

        date_text = str(date_value).strip()
        if not date_text or date_text.lower() == 'nan':
            return ""

        mois_francais = {
            1: 'janvier', 2: 'février', 3: 'mars', 4: 'avril', 5: 'mai', 6: 'juin',
            7: 'juillet', 8: 'août', 9: 'septembre', 10: 'octobre', 11: 'novembre', 12: 'décembre'
        }

        if any(mois in date_text.lower() for mois in mois_francais.values()):
            return date_text

        parsed_date = pd.to_datetime(date_text, errors='coerce', dayfirst=True)
        if pd.isna(parsed_date):
            return date_text

        return f"{parsed_date.day:02d} {mois_francais[parsed_date.month]} {parsed_date.year}"

    def _format_room_display(self, room_value):
        """Formate un numéro de salle avec son étage, ex: '22 (1er étage)'"""
        if room_value is None:
            return ""

        room_text = str(room_value).strip()
        if not room_text or room_text.lower() == 'nan':
            return ""

        if '(' in room_text:
            return room_text

        room_number = room_text.split()[0]
        try:
            num = int(room_number)
        except ValueError:
            return room_text

        if 1 <= num <= 14:
            return f"{room_number} (rez-de-chaussée)"
        if 15 <= num <= 22:
            return f"{room_number} (1er étage)"

        return room_text
        
    def load_tcf_data(self):
        """
        Charge toutes les données TCF depuis le fichier Excel
        """
        try:
            excel_file = pd.ExcelFile(self.excel_path, engine='openpyxl')
            
            # D'abord, charger les durées depuis l'onglet ADMIN
            self._load_admin_durations(excel_file)
            
            # Traiter chaque feuille de déclinaison TCF
            for sheet_name in excel_file.sheet_names:
                if sheet_name in self.TCF_DURATIONS:
                    self.logger.info(f"Traitement de la feuille: {sheet_name}")
                    self._process_tcf_sheet(sheet_name)
            
            # Fusionner les candidats multi-épreuves
            self._merge_multi_exam_candidates()
                    
            self.logger.info(f"Total candidats chargés: {len(self.candidates)}")
            return True
            
        except Exception as e:
            self.logger.error(f"Erreur lors du chargement des données TCF: {e}")
            return False
    
    def _load_admin_durations(self, excel_file):
        """
        Charge les durées depuis l'onglet ADMIN du fichier Excel
        """
        try:
            if 'ADMIN' in excel_file.sheet_names:
                print("🔍 DEBUG: Lecture de l'onglet ADMIN pour les durées")
                admin_df = pd.read_excel(self.excel_path, sheet_name='ADMIN', header=None, engine='openpyxl')
                
                # Initialiser les dictionnaires de durées
                self.durees_collectives = {}
                self.durees_individuelles = {}
                
                # Recherche des durées collectives (lignes 4-8, colonne B)
                for i in range(3, 8):  # lignes 4 à 8 (index 3 à 7)
                    if i < len(admin_df):
                        type_tcf = admin_df.iloc[i, 0]  # colonne A
                        duree = admin_df.iloc[i, 1]     # colonne B
                        
                        if pd.notna(type_tcf) and pd.notna(duree):
                            type_str = str(type_tcf).strip()
                            duree_str = str(duree).strip()
                            
                            if 'TCF CANADA' in type_str:
                                self.durees_collectives['TCF CANADA'] = duree_str
                                print(f"  ✓ TCF CANADA durée collective: {duree_str}")
                            elif 'TCF TP COMPLET' in type_str:
                                self.durees_collectives['TCF TP COMPLET'] = duree_str
                                print(f"  ✓ TCF TP COMPLET durée collective: {duree_str}")
                            elif 'TCF TP OBLIGATOIRE' in type_str:
                                self.durees_collectives['TCF TP OBLIGATOIRE'] = duree_str
                                print(f"  ✓ TCF TP OBLIGATOIRE durée collective: {duree_str}")
                            elif 'TCF TP EE' in type_str or 'TCP TP EE' in type_str or 'Expression Écrite' in type_str or 'Expression Ecrite' in type_str:
                                self.durees_collectives['TCF TP EE'] = duree_str
                                print(f"  ✓ TCF TP EE durée collective (B8): {duree_str}")
                            elif 'TCF TP EO' in type_str or 'Expression Orale' in type_str:
                                # TCF TP EO n'a pas d'épreuve collective, seulement individuelle
                                pass
                            elif 'TCF IRN' in type_str:
                                self.durees_collectives['TCF IRN'] = duree_str
                                print(f"  ✓ TCF IRN durée collective: {duree_str}")
                
                # Recherche des durées individuelles (lignes 11-15, colonne B)
                for i in range(10, 15):  # lignes 11 à 15 (index 10 à 14)
                    if i < len(admin_df):
                        type_tcf = admin_df.iloc[i, 0]  # colonne A
                        duree = admin_df.iloc[i, 1]     # colonne B
                        
                        if pd.notna(type_tcf) and pd.notna(duree):
                            type_str = str(type_tcf).strip()
                            duree_str = f"{str(duree).strip()} minutes"
                            
                            if 'TCF CANADA' in type_str:
                                self.durees_individuelles['TCF CANADA'] = duree_str
                                print(f"  ✓ TCF CANADA durée individuelle: {duree_str}")
                            elif 'TCF TP COMPLET' in type_str:
                                self.durees_individuelles['TCF TP COMPLET'] = duree_str
                                print(f"  ✓ TCF TP COMPLET durée individuelle: {duree_str}")
                            elif 'TCF TP OBLIGATOIRE' in type_str:
                                self.durees_individuelles['TCF TP OBLIGATOIRE'] = duree_str
                                print(f"  ✓ TCF TP OBLIGATOIRE durée individuelle: {duree_str}")
                            elif 'TCF TP EE' in type_str or 'Expression Écrite' in type_str or 'Expression Ecrite' in type_str:
                                # TCF TP EE n'a pas d'épreuve individuelle, seulement collective
                                pass
                            elif 'TCF TP EO' in type_str or 'Expression Orale' in type_str:
                                self.durees_individuelles['TCF TP EO'] = duree_str
                                print(f"  ✓ TCF TP EO durée individuelle (B15): {duree_str}")
                            elif 'TCF IRN' in type_str:
                                self.durees_individuelles['TCF IRN'] = duree_str
                                print(f"  ✓ TCF IRN durée individuelle: {duree_str}")
                
                print(f"📊 Durées collectives chargées: {self.durees_collectives}")
                print(f"📊 Durées individuelles chargées: {self.durees_individuelles}")
                
            else:
                print("⚠️ Onglet ADMIN non trouvé, utilisation des valeurs par défaut")
                self.durees_collectives = {}
                self.durees_individuelles = {}
                
        except Exception as e:
            print(f"⚠️ Erreur lors de la lecture de l'onglet ADMIN: {e}")
            self.logger.warning(f"Impossible de lire l'onglet ADMIN: {e}")
            self.durees_collectives = {}
            self.durees_individuelles = {}
    
    def _merge_multi_exam_candidates(self):
        """
        Fusionne les candidats inscrits à plusieurs épreuves TCF TP
        (ex: TCF TP EE + TCF TP EO, TCF TP OBLIGATOIRE + TCF TP EO)
        en une seule entrée avec toutes les informations d'examen
        """
        # Grouper les candidats par identité unique
        candidate_groups = {}
        
        for candidate in self.candidates:
            # Clé unique basée sur nom, prénom, date de naissance, email
            key = (
                candidate.get('nom', '').strip().upper(),
                candidate.get('prenom', '').strip().upper(),
                str(candidate.get('date_naissance', '')),
                candidate.get('email', '').strip().lower()
            )
            
            if key not in candidate_groups:
                candidate_groups[key] = []
            candidate_groups[key].append(candidate)
        
        # Identifier et fusionner les candidats multi-épreuves
        merged_candidates = []
        multi_exam_count = 0
        
        for key, group in candidate_groups.items():
            if len(group) == 1:
                # Candidat unique, garder tel quel
                merged_candidates.append(group[0])
            else:
                # Candidat multi-épreuves, fusionner
                multi_exam_count += 1
                merged = self._merge_candidate_group(group)
                merged_candidates.append(merged)
                
                # Log pour debug
                nom_prenom = f"{merged['nom']} {merged['prenom']}"
                types = ' + '.join([c['tcf_type'] for c in group])
                self.logger.info(f"✅ Fusion multi-épreuves: {nom_prenom} ({types})")
        
        # Remplacer la liste de candidats
        original_count = len(self.candidates)
        self.candidates = merged_candidates
        
        if multi_exam_count > 0:
            self.logger.info(f"🔄 Fusion terminée: {multi_exam_count} candidats multi-épreuves fusionnés")
            self.logger.info(f"   {original_count} entrées → {len(self.candidates)} candidats uniques")
    
    def _merge_candidate_group(self, group):
        """
        Fusionne les données de plusieurs épreuves pour un même candidat
        
        Args:
            group (list): Liste des entrées candidat à fusionner
            
        Returns:
            dict: Candidat fusionné avec toutes les épreuves
        """
        # Prendre le premier candidat comme base
        merged = group[0].copy()
        
        # Collecter toutes les épreuves
        exams = []
        for candidate in group:
            # Déterminer l'heure principale selon le type d'épreuve
            if candidate['tcf_type'] == 'TCF TP EO':
                # EO : seulement épreuve individuelle
                main_time = candidate.get('heure_individuelle', candidate.get('heure_preparation'))
            else:
                # EE/OBLIGATOIRE : épreuve collective
                main_time = candidate.get('debut_ep_coll')
            
            # Formater les heures et durées sans secondes
            def format_time_no_seconds(time_val):
                if not time_val:
                    return None
                time_str = str(time_val)
                # Format: "HH:MM:SS" -> "HH:MM" ou "HH:MM" -> "HH:MM"
                if ':' in time_str:
                    parts = time_str.split(':')
                    return f"{parts[0]}:{parts[1]}"
                return time_str
            
            def format_duration_no_seconds(duration_val):
                if not duration_val:
                    return None
                duration_str = str(duration_val)
                # Format: "01:25:00" -> "01h25" ou "2h30" -> "2h30"
                if ':' in duration_str:
                    parts = duration_str.split(':')
                    return f"{parts[0]}h{parts[1]}"
                return duration_str
            
            exam_info = {
                'tcf_type': candidate['tcf_type'],
                'exam_date': candidate.get('date_examen'),
                'date_collective': candidate.get('date_ep_coll'),
                'date_individual': candidate.get('date_ep_ind'),
                'time_collective': format_time_no_seconds(candidate.get('debut_ep_coll')),
                'time_individual': format_time_no_seconds(candidate.get('heure_individuelle') or candidate.get('heure_preparation')),
                'collective_duration': format_duration_no_seconds(candidate.get('duree_collective')),
                'individual_duration': format_duration_no_seconds(candidate.get('duree_individuelle')),
                'collective_start': candidate.get('debut_ep_coll'),
                'collective_end': candidate.get('fin_ep_coll'),
                'exam_location': candidate.get('salle_collective') or candidate.get('salle_individuelle'),
                'jury_name': candidate.get('jury_name'),
                'main_time': main_time  # Pour le tri
            }
            exams.append(exam_info)
        
        # Trier les épreuves par ordre chronologique
        # Priorité: date d'examen, puis heure principale (collective ou individuelle)
        def exam_sort_key(exam):
            # Date d'examen
            exam_date = exam.get('exam_date')
            if not exam_date:
                exam_date = datetime(2099, 1, 1).date()
            elif not hasattr(exam_date, 'strftime'):
                # Si c'est une chaîne, essayer de la parser
                try:
                    exam_date = datetime.strptime(str(exam_date), '%d/%m/%Y').date()
                except:
                    exam_date = datetime(2099, 1, 1).date()
            
            # Heure principale
            main_time = exam.get('main_time')
            if not main_time:
                exam_time = time(23, 59)
            elif isinstance(main_time, str):
                try:
                    # Format: "HH:MM:SS" ou "HH:MM"
                    parts = main_time.replace('h', ':').split(':')
                    hour = int(parts[0])
                    minute = int(parts[1]) if len(parts) > 1 else 0
                    exam_time = time(hour, minute)
                except:
                    exam_time = time(23, 59)
            elif hasattr(main_time, 'hour'):
                # C'est déjà un objet time
                exam_time = main_time
            else:
                exam_time = time(23, 59)
            
            return (exam_date, exam_time)
        
        exams.sort(key=exam_sort_key)
        
        # Marquer comme multi-épreuves
        merged['is_multi_exam'] = True
        merged['exams'] = exams
        merged['tcf_type'] = ' + '.join([e['tcf_type'] for e in exams])
        
        # Utiliser les infos de la première épreuve chronologiquement
        first_exam = exams[0]
        merged['exam_date'] = first_exam['exam_date']
        merged['exam_location'] = first_exam['exam_location']
        
        return merged
    
    def _process_tcf_sheet(self, sheet_name):
        """
        Traite une feuille de déclinaison TCF spécifique
        
        Args:
            sheet_name (str): Nom de la feuille (ex: 'TCF CANADA')
        """
        try:
            # Lire la feuille sans header pour analyser la structure
            df = pd.read_excel(self.excel_path, sheet_name=sheet_name, header=None, engine='openpyxl')
            
            current_jury = None
            current_jury_data = None
            
            print(f"🔍 DEBUG: Traitement de la feuille {sheet_name}")
            print(f"  - Nombre de lignes: {len(df)}")
            
            for index, row in df.iterrows():
                row_values = row.tolist()
                
                # DEBUG: Afficher chaque ligne pour diagnostic
                first_col = str(row_values[0]).strip() if row_values[0] is not None else ""
                if first_col:  # Seulement les lignes non vides
                    print(f"  - Ligne {index}: {row_values[:4]}...")  # 4 premières colonnes
                    if first_col.startswith("Jury"):
                        print(f"    → JURY détecté!")
                
                # Détecter une ligne de jury (commence par "Jury")
                if self._is_jury_line(row_values):
                    current_jury, current_jury_data = self._parse_jury_line(row_values, sheet_name)
                    self.logger.info(f"Jury détecté: {current_jury}")
                    
                # Détecter les candidats (avoir une heure de passage)
                elif self._is_candidate_line(row_values) and current_jury_data:
                    candidate = self._parse_candidate_line(row_values, current_jury_data, sheet_name)
                    if candidate:
                        self.candidates.append(candidate)
                        
        except Exception as e:
            self.logger.error(f"Erreur lors du traitement de la feuille {sheet_name}: {e}")
    
    def _is_jury_line(self, row_values):
        """
        Détermine si une ligne contient des informations de jury
        
        Args:
            row_values (list): Valeurs de la ligne
            
        Returns:
            bool: True si c'est une ligne de jury
        """
        if not row_values or len(row_values) < 2:
            return False
            
        first_col = str(row_values[0]).strip() if row_values[0] is not None else ""
        return first_col.startswith("Jury")
    
    def _is_candidate_line(self, row_values):
        """
        Détermine si une ligne contient un candidat
        
        Args:
            row_values (list): Valeurs de la ligne
            
        Returns:
            bool: True si c'est une ligne de candidat
        """
        if not row_values or len(row_values) < 2:
            return False
            
        # Colonne 0: heure de passage (peut être vide pour TCF TP EE)
        time_col = str(row_values[0]).strip() if row_values[0] is not None and str(row_values[0]).strip() != 'nan' else ""
        # Colonne 1: NOM (obligatoire)
        nom_col = str(row_values[1]).strip() if row_values[1] is not None else ""
        # Colonne 2: Prénom (obligatoire)
        prenom_col = str(row_values[2]).strip() if len(row_values) > 2 and row_values[2] is not None else ""
        
        # Filtrer les en-têtes et lignes vides
        if not nom_col or nom_col in ["NOM", "Pass.", "Jury", "nan"]:
            return False
        if not prenom_col or prenom_col in ["Prénom", "nan"]:
            return False
        
        # Format heure TCF: "14h00", "15h30", etc.
        time_pattern = r'^\d{1,2}h\d{2}$'
        
        # Un candidat valide a soit:
        # 1. Une heure ET un nom/prénom (cas général: TCF TP EO, TCF TP OBLIGATOIRE, TCF CANADA, etc.)
        # 2. Juste un nom/prénom valide sans heure (cas TCF TP EE)
        has_time = bool(re.match(time_pattern, time_col))
        has_valid_nom = len(nom_col) > 1  # Nom significatif
        has_valid_prenom = len(prenom_col) > 1  # Prénom significatif
        
        return has_valid_nom and has_valid_prenom and (has_time or not time_col)
    
    def _parse_jury_line(self, row_values, sheet_name):
        """
        Parse une ligne de jury pour extraire les informations
        
        Args:
            row_values (list): Valeurs de la ligne de jury
            sheet_name (str): Nom de la feuille TCF
            
        Returns:
            tuple: (jury_name, jury_data)
        """
        try:
            jury_name = str(row_values[0]).strip()
            
            # DEBUG: Afficher les valeurs de la ligne de jury
            print(f"🔍 DEBUG: Ligne de jury détectée:")
            print(f"  - Sheet: {sheet_name}")
            print(f"  - Colonne A (jury): {row_values[0]}")
            print(f"  - Colonne B (date): {row_values[1] if len(row_values) > 1 else 'N/A'}")
            print(f"  - Type de la date: {type(row_values[1]) if len(row_values) > 1 else 'N/A'}")
            print(f"  - Toutes les colonnes: {row_values[:6]}")  # Afficher les 6 premières colonnes
            
            # Lire la date depuis la colonne B de la ligne jury
            exam_date = None
            if len(row_values) > 1 and row_values[1] is not None:
                date_value = row_values[1]
                print(f"  - Valeur date brute: {date_value}")
                
                if isinstance(date_value, str):
                    # Essayer de parser la date si c'est une chaîne
                    try:
                        exam_date = datetime.strptime(date_value, '%d/%m/%Y').date()
                        print(f"  - Date parsée (string): {exam_date}")
                    except Exception as e:
                        print(f"  - Erreur parsing string: {e}")
                        # Essayer d'autres formats
                        for fmt in ['%Y-%m-%d', '%d-%m-%Y', '%m/%d/%Y']:
                            try:
                                exam_date = datetime.strptime(date_value, fmt).date()
                                print(f"  - Date parsée (format {fmt}): {exam_date}")
                                break
                            except:
                                continue
                elif hasattr(date_value, 'date'):
                    # Si c'est déjà un objet datetime
                    exam_date = date_value.date()
                    print(f"  - Date extraite (datetime): {exam_date}")
                elif hasattr(date_value, 'strftime'):
                    # Si c'est déjà un objet date
                    exam_date = date_value
                    print(f"  - Date utilisée directement: {exam_date}")
                else:
                    print(f"  - Type de date non géré: {type(date_value)}")
            
            print(f"  - Date finale: {exam_date}")
            
            # Extraire les heures de début et fin (colonnes 3 et 5)
            start_time = None
            end_time = None
            
            if len(row_values) > 3 and row_values[3] is not None:
                if isinstance(row_values[3], time):
                    start_time = row_values[3]
                elif isinstance(row_values[3], str):
                    try:
                        start_time = datetime.strptime(row_values[3], '%H:%M:%S').time()
                    except:
                        pass
            
            if len(row_values) > 5 and row_values[5] is not None:
                if isinstance(row_values[5], time):
                    end_time = row_values[5]
                elif isinstance(row_values[5], str):
                    try:
                        end_time = datetime.strptime(row_values[5], '%H:%M:%S').time()
                    except:
                        pass
            
            jury_data = {
                'jury_name': jury_name,
                'exam_date': exam_date,
                'collective_start': start_time,
                'collective_end': end_time,
                'tcf_type': sheet_name,
                'duration_info': self.TCF_DURATIONS.get(sheet_name, {}),
                'duree_collective': self.durees_collectives.get(sheet_name, '2h30'),
                'duree_individuelle': self.durees_individuelles.get(sheet_name, '12 minutes')
            }
            
            self.jurys_data[jury_name] = jury_data
            return jury_name, jury_data
            
        except Exception as e:
            self.logger.error(f"Erreur lors du parsing de la ligne jury: {e}")
            return None, None
    
    def _parse_candidate_line(self, row_values, jury_data, sheet_name):
        """
        Parse une ligne de candidat
        
        Args:
            row_values (list): Valeurs de la ligne candidat
            jury_data (dict): Données du jury associé
            sheet_name (str): Nom de la feuille TCF
            
        Returns:
            dict: Données du candidat ou None
        """
        try:
            # Extraire les informations de base
            individual_time_str = str(row_values[0]).strip() if row_values[0] and str(row_values[0]).strip() != 'nan' else ""
            nom = str(row_values[1]).strip() if len(row_values) > 1 and row_values[1] else ""
            prenom = str(row_values[2]).strip() if len(row_values) > 2 and row_values[2] else ""
            birth_date = self._format_birth_date(row_values[3]) if len(row_values) > 3 else ""
            
            # FIX v2 - FORCER LE RECHARGEMENT 2026-01-12 20:00
            email = ""
            if len(row_values) > 4 and row_values[4] is not None:
                # IMPORTANT: Ne PAS convertir directement avec str() si c'est NaN
                if pd.isna(row_values[4]):
                    email = ""
                    print(f"    [EMAIL DEBUG] Email est NaN pandas pour {nom}")
                else:
                    email_val = str(row_values[4]).strip()
                    if email_val and email_val.lower() != 'nan':
                        email = email_val
                        print(f"    [EMAIL DEBUG] Email trouvé: {email} pour {nom}")
                    else:
                        email = ""
                        print(f"    [EMAIL DEBUG] Email vide ou 'nan' string pour {nom}")
            
            # Filtrer les lignes vides ou les en-têtes
            if not nom or nom in ['NOM', 'Pass.', 'nan']:
                return None
            if not prenom or prenom in ['Prénom', 'nan']:
                return None
            
            # Debug pour vérifier la lecture des données
            print(f"  - Colonne B (nom): {nom}")
            print(f"  - Colonne C (prénom): {prenom}")
            print(f"  - Colonne D (date naissance): {birth_date}")
            print(f"  - Colonne E (email): {email}")
            
            # Parser l'heure individuelle (format "14h00" -> "14:00")
            individual_time = None
            if individual_time_str and 'h' in individual_time_str:
                try:
                    time_parts = individual_time_str.replace('h', ':')
                    individual_time = datetime.strptime(time_parts, '%H:%M').time()
                except:
                    pass
            
            # Pour TCF TP OBLIGATOIRE et TCF TP EE: l'heure en colonne A est l'heure collective
            collective_start_time = jury_data.get('collective_start')
            collective_end_time = jury_data.get('collective_end')
            
            if sheet_name in ['TCF TP OBLIGATOIRE', 'TCF TP EE'] and individual_time:
                collective_start_time = individual_time
                individual_time = None  # Ces types n'ont pas d'épreuve individuelle
                
                # Calculer l'heure de fin à partir de ADMIN B8 (durée)
                duree_str = jury_data.get('duree_collective', '01:00:00')
                if isinstance(duree_str, str) and ':' in duree_str:
                    # Format "01:00:00"
                    parts = duree_str.split(':')
                    hours = int(parts[0])
                    minutes = int(parts[1])
                    start_datetime = datetime.combine(datetime.today(), collective_start_time)
                    end_datetime = start_datetime + timedelta(hours=hours, minutes=minutes)
                    collective_end_time = end_datetime.time()
            
            # Pour TCF TP EO: calculer l'heure de fin de l'épreuve individuelle
            individual_end_time = None
            if sheet_name == 'TCF TP EO' and individual_time:
                # Durée depuis ADMIN B15 (format "12 minutes")
                duree_str = jury_data.get('duree_individuelle', '12 minutes')
                if 'minutes' in duree_str:
                    minutes = int(duree_str.replace(' minutes', '').strip())
                    start_datetime = datetime.combine(datetime.today(), individual_time)
                    end_datetime = start_datetime + timedelta(minutes=minutes)
                    individual_end_time = end_datetime.time()
            
            # Générer un numéro de candidat unique
            numero_candidat = f"TCF{datetime.now().year}{len(self.candidates)+1:06d}"
            
            candidate = {
                'nom': nom,
                'prenom': prenom,
                'numero_candidat': numero_candidat,
                'email': email,
                'date_naissance': birth_date,
                
                # Informations TCF spécifiques
                'tcf_type': sheet_name,
                'jury_name': jury_data['jury_name'],
                
                # Dates et heures
                'date_examen': jury_data['exam_date'],
                'date_ep_coll': jury_data['exam_date'],
                'date_ep_ind': jury_data['exam_date'],  # Même jour
                
                # Heures épreuve collective
                'debut_ep_coll': collective_start_time,
                'fin_ep_coll': collective_end_time,
                
                # Heure épreuve individuelle
                'heure_preparation': individual_time if jury_data['duration_info'].get('has_individual') else None,
                'heure_individuelle': individual_time if jury_data['duration_info'].get('has_individual') else None,
                'fin_individuelle': individual_end_time,  # Heure de fin calculée
                
                # Durées depuis ADMIN (B8 pour EE, B15 pour EO)
                'duree_collective': jury_data.get('duree_collective', '2h30'),
                'duree_individuelle': jury_data.get('duree_individuelle', '12 minutes'),
                
                # Informations complémentaires
                'has_individual_exam': jury_data['duration_info'].get('has_individual', False),
                'salle_collective': self._format_room_display(getattr(self, 'salle_collective', "1")),  # Utilise la valeur configurée
                'salle_individuelle': self._format_room_display(getattr(self, 'salle_individuelle', "1")),  # Utilise la valeur configurée
                
                # Informations institution (valeurs par défaut)
                'institution_name': 'Alliance Française de Bruxelles-Europe',
                'institution_address': 'Avenue des Arts 46',
                'institution_postal': '1000',
                'institution_city': 'Bruxelles',
            }
            
            # Formater les durées depuis ADMIN
            # TCF TP EE: B8 format "01:00:00" → "01h00"
            if sheet_name == 'TCF TP EE':
                duree_str = candidate['duree_collective']
                if isinstance(duree_str, str) and ':' in duree_str:
                    parts = duree_str.split(':')
                    candidate['duree_collective'] = f"{parts[0]}h{parts[1]}"
            
            # TCF TP EO: B15 format "12" → "12 minutes" (déjà formaté)
            # Pas de transformation nécessaire, duree_individuelle est déjà "12 minutes"
            
            return candidate
            
        except Exception as e:
            self.logger.error(f"Erreur lors du parsing du candidat: {e}")
            return None
    
    def get_all_candidates(self):
        """
        Retourne tous les candidats chargés (déjà fusionnés)
        
        Returns:
            list: Liste des candidats
        """
        return self.candidates
    
    def _merge_multi_exam_candidates_OLD(self, candidates):
        """
        ANCIENNE VERSION - NE PAS UTILISER
        Fusionne les candidats présents dans plusieurs feuilles TCF TP
        (TCF TP OBLIGATOIRE + TCF TP EE/EO, ou TCF TP EE + TCF TP EO)
        
        Args:
            candidates (list): Liste brute des candidats
            
        Returns:
            list: Liste avec candidats fusionnés
        """
        # Grouper par identifiant unique (nom+prenom+email)
        candidates_by_id = {}
        
        for candidate in candidates:
            nom = candidate.get('nom', '').strip().upper()
            prenom = candidate.get('prenom', '').strip().title()
            email = candidate.get('email', '').strip().lower()
            
            # Clé unique pour identifier le même candidat
            candidate_id = f"{nom}||{prenom}||{email}"
            
            if candidate_id not in candidates_by_id:
                candidates_by_id[candidate_id] = []
            
            candidates_by_id[candidate_id].append(candidate)
        
        # Fusionner les candidats avec plusieurs épreuves
        merged = []
        
        for candidate_id, exams in candidates_by_id.items():
            if len(exams) == 1:
                # Un seul examen, pas de fusion nécessaire
                merged.append(exams[0])
            else:
                # Plusieurs épreuves pour le même candidat - fusionner
                print(f"🔀 FUSION: {exams[0]['nom']} {exams[0]['prenom']} - {len(exams)} épreuves détectées")
                
                # Trier les épreuves par ordre chronologique
                sorted_exams = self._sort_exams_chronologically(exams)
                
                # Créer un candidat fusionné
                merged_candidate = self._create_merged_candidate(sorted_exams)
                merged.append(merged_candidate)
                
                print(f"   ✓ Fusion terminée: {merged_candidate.get('exam_types_combined', 'N/A')}")
        
        return merged
    
    def _sort_exams_chronologically(self, exams):
        """
        Trie les épreuves par ordre chronologique (date puis heure)
        
        Args:
            exams (list): Liste d'épreuves du même candidat
            
        Returns:
            list: Épreuves triées
        """
        def get_exam_datetime(exam):
            # Déterminer la date et l'heure de l'épreuve
            tcf_type = exam.get('tcf_type', '')
            
            if tcf_type == 'TCF TP EO':
                # Épreuve individuelle uniquement
                date = exam.get('date_ep_ind')
                time = exam.get('heure_preparation')
            elif tcf_type in ['TCF TP OBLIGATOIRE', 'TCF TP EE']:
                # Épreuve collective uniquement
                date = exam.get('date_ep_coll')
                time = exam.get('debut_ep_coll')
            else:
                # Par défaut, utiliser la date collective
                date = exam.get('date_ep_coll') or exam.get('date_ep_ind')
                time = exam.get('debut_ep_coll') or exam.get('heure_preparation')
            
            # Combiner date et heure pour le tri
            if date and time:
                try:
                    from datetime import datetime, time as time_type
                    if isinstance(time, time_type):
                        return datetime.combine(date, time)
                    elif isinstance(time, str) and ':' in time:
                        hour, minute = time.split(':')[:2]
                        return datetime.combine(date, time_type(int(hour), int(minute)))
                except:
                    pass
            
            # Si pas de date/heure valide, retourner une date minimale
            return datetime.min
        
        return sorted(exams, key=get_exam_datetime)
    
    def _create_merged_candidate(self, sorted_exams):
        """
        Crée un candidat fusionné avec toutes ses épreuves
        
        Args:
            sorted_exams (list): Épreuves triées chronologiquement
            
        Returns:
            dict: Candidat fusionné
        """
        # Partir du premier examen comme base
        merged = dict(sorted_exams[0])
        
        # Identifier les types d'épreuves combinés
        exam_types = [exam.get('tcf_type') for exam in sorted_exams]
        merged['exam_types_combined'] = ' + '.join(exam_types)
        merged['is_multi_exam'] = True
        merged['exams'] = sorted_exams  # Garder toutes les épreuves pour le template
        
        # Pour le template, on garde le premier type comme référence
        # mais on ajoutera une logique spéciale pour afficher les deux
        merged['tcf_type'] = 'TCF TP MULTI'  # Nouveau type pour identifier les multi-épreuves
        merged['primary_exam_type'] = exam_types[0]
        merged['secondary_exam_type'] = exam_types[1] if len(exam_types) > 1 else None
        
        # Stocker les dates/heures des deux épreuves
        first_exam = sorted_exams[0]
        second_exam = sorted_exams[1] if len(sorted_exams) > 1 else None
        
        # Premier examen (peut être collectif ou individuel)
        if first_exam.get('tcf_type') == 'TCF TP EO':
            merged['first_exam_is_individual'] = True
            merged['first_exam_date'] = first_exam.get('date_ep_ind')
            merged['first_exam_time'] = first_exam.get('heure_preparation')
            merged['first_exam_duration'] = first_exam.get('duree_individuelle')
            merged['first_exam_salle'] = first_exam.get('salle_individuelle', first_exam.get('salle'))
        else:
            merged['first_exam_is_individual'] = False
            merged['first_exam_date'] = first_exam.get('date_ep_coll')
            merged['first_exam_time'] = first_exam.get('debut_ep_coll')
            merged['first_exam_duration'] = first_exam.get('duree_collective')
            merged['first_exam_salle'] = first_exam.get('salle_collective', first_exam.get('salle'))
        
        # Deuxième examen (si existe)
        if second_exam:
            if second_exam.get('tcf_type') == 'TCF TP EO':
                merged['second_exam_is_individual'] = True
                merged['second_exam_date'] = second_exam.get('date_ep_ind')
                merged['second_exam_time'] = second_exam.get('heure_preparation')
                merged['second_exam_duration'] = second_exam.get('duree_individuelle')
                merged['second_exam_salle'] = second_exam.get('salle_individuelle', second_exam.get('salle'))
            else:
                merged['second_exam_is_individual'] = False
                merged['second_exam_date'] = second_exam.get('date_ep_coll')
                merged['second_exam_time'] = second_exam.get('debut_ep_coll')
                merged['second_exam_duration'] = second_exam.get('duree_collective')
                merged['second_exam_salle'] = second_exam.get('salle_collective', second_exam.get('salle'))
        
        print(f"   📅 1ère épreuve: {merged['primary_exam_type']} - {merged['first_exam_date']} à {merged['first_exam_time']}")
        if second_exam:
            print(f"   📅 2ème épreuve: {merged['secondary_exam_type']} - {merged['second_exam_date']} à {merged['second_exam_time']}")
        
        return merged
    
    def get_candidates_by_tcf_type(self, tcf_type):
        """
        Retourne les candidats d'une déclinaison TCF spécifique
        
        Args:
            tcf_type (str): Type de TCF
            
        Returns:
            list: Candidats filtrés
        """
        return [c for c in self.candidates if c.get('tcf_type') == tcf_type]
    
    def get_jurys_info(self):
        """
        Retourne les informations des jurys
        
        Returns:
            dict: Informations des jurys
        """
        return self.jurys_data
    
    def print_summary(self):
        """
        Affiche un résumé des données chargées
        """
        print(f"\n=== RÉSUMÉ DES DONNÉES TCF ===")
        print(f"Fichier: {self.excel_path}")
        print(f"Total candidats: {len(self.candidates)}")
        
        # Statistiques par déclinaison
        for tcf_type in self.TCF_DURATIONS.keys():
            candidates_count = len(self.get_candidates_by_tcf_type(tcf_type))
            print(f"  {tcf_type}: {candidates_count} candidats")
        
        # Informations des jurys
        print(f"\nJurys détectés: {len(self.jurys_data)}")
        for jury_name, jury_info in self.jurys_data.items():
            print(f"  {jury_name} ({jury_info['tcf_type']}): {jury_info['exam_date']} - {jury_info['collective_start']}-{jury_info['collective_end']}")

# Test du processeur
if __name__ == "__main__":
    processor = TCFExcelProcessor("JURYS FINAL TCF.xlsx")
    
    if processor.load_tcf_data():
        processor.print_summary()
        
        # Afficher quelques exemples de candidats
        candidates = processor.get_all_candidates()
        if candidates:
            print(f"\n=== EXEMPLES DE CANDIDATS ===")
            for i, candidate in enumerate(candidates[:3]):
                print(f"\nCandidat {i+1}:")
                for key, value in candidate.items():
                    print(f"  {key}: {value}")
    else:
        print("Erreur lors du chargement des données TCF")