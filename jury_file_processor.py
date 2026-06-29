#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Processeur pour les fichiers de jurys DELF/DALF
Convertit la structure des jurys en format compatible avec le système d'emails
"""

import pandas as pd
import re
from datetime import datetime
import logging

class JuryFileProcessor:
    def __init__(self, jury_file_path):
        self.jury_file_path = jury_file_path
        self.candidates = []
        self.exam_config = {}
        
    def process_jury_file(self):
        """Traite le fichier de jurys et extrait tous les candidats"""
        try:
            # Lire toutes les feuilles du fichier Excel
            excel_file = pd.ExcelFile(self.jury_file_path)
            
            # Traiter d'abord la feuille ADMIN pour la configuration
            if 'ADMIN' in excel_file.sheet_names:
                self._process_admin_sheet(excel_file)
            
            # Traiter chaque niveau
            for sheet_name in excel_file.sheet_names:
                if sheet_name.startswith('Niveau '):
                    level = sheet_name.replace('Niveau ', '')
                    print(f"Traitement du niveau {level}...")
                    self._process_level_sheet(excel_file, sheet_name, level)
            
            print(f"✅ {len(self.candidates)} candidats extraits du fichier de jurys")
            return self.candidates
            
        except Exception as e:
            print(f"❌ Erreur lors du traitement du fichier de jurys: {e}")
            return []
    
    def _process_admin_sheet(self, excel_file):
        """Traite la feuille ADMIN pour extraire la configuration"""
        try:
            df = pd.read_excel(excel_file, sheet_name='ADMIN', header=None)
            # La configuration est dans cette feuille mais pour l'instant on l'ignore
            # On pourrait l'utiliser pour calculer les durées d'épreuves
            pass
        except Exception as e:
            print(f"⚠️ Impossible de lire la feuille ADMIN: {e}")
    
    def _process_level_sheet(self, excel_file, sheet_name, level):
        """Traite une feuille de niveau spécifique"""
        try:
            df = pd.read_excel(excel_file, sheet_name=sheet_name, header=None)
            
            # Chercher les informations d'épreuve collective (pour A1 principalement)
            collective_date = None
            collective_start = None
            collective_end = None
            
            # Scanner les premières lignes pour les infos collectives
            for i in range(min(10, len(df))):
                row = df.iloc[i]
                if pd.notna(row.iloc[1]) and 'Date épreuve collective' in str(row.iloc[0]):
                    collective_date = self._parse_date(str(row.iloc[1]))
                elif pd.notna(row.iloc[3]) and 'Début de l\'épreuve collective' in str(row.iloc[2]):
                    collective_start = str(row.iloc[3])
                elif pd.notna(row.iloc[5]) and 'Fin de l\'épreuve collective' in str(row.iloc[4]):
                    collective_end = str(row.iloc[5])
            
            # Chercher les candidats
            current_jury_date = None
            
            for i, row in df.iterrows():
                # Détecter une nouvelle section de jury
                if pd.notna(row.iloc[0]) and 'Jury' in str(row.iloc[0]):
                    if pd.notna(row.iloc[1]):
                        current_jury_date = self._parse_date(str(row.iloc[1]))
                    continue
                
                # Vérifier si c'est une ligne de candidat
                if self._is_candidate_row(row):
                    candidate = self._extract_candidate_info(row, level, collective_date, collective_start, current_jury_date)
                    if candidate:
                        self.candidates.append(candidate)
                        
        except Exception as e:
            print(f"❌ Erreur lors du traitement du niveau {level}: {e}")
    
    def _is_candidate_row(self, row):
        """Vérifie si une ligne contient des informations de candidat"""
        # Vérifier d'abord si c'est une ligne d'en-tête
        if len(row) > 2 and pd.notna(row.iloc[0]) and pd.notna(row.iloc[1]) and pd.notna(row.iloc[2]):
            # Vérifier différentes variations d'en-têtes possibles
            first_col = str(row.iloc[0]).strip().lower()
            second_col = str(row.iloc[1]).strip().lower()
            third_col = str(row.iloc[2]).strip().lower()
            
            # Méthode 1: Vérifier les en-têtes typiques
            if (first_col in ["prép.", "prep.", "prep", "preparation"] and 
                second_col in ["pass.", "pass", "passage"] and 
                ("numéro" in third_col or "numero" in third_col or "candidat" in third_col)):
                # C'est une ligne d'en-tête, pas un candidat
                print(f"Header detected and skipped: {row.iloc[0]} {row.iloc[1]} {row.iloc[2]}")
                return False
            
            # Méthode 2: Vérifier si les colonnes contiennent des en-têtes typiques
            if "préparation" in first_col or "preparation" in first_col:
                if "passage" in second_col:
                    if "candidat" in third_col or "numéro" in third_col or "numero" in third_col:
                        print(f"Header detected and skipped: {row.iloc[0]} {row.iloc[1]} {row.iloc[2]}")
                        return False
        
        # Chercher le numéro de candidat (colonne 2 généralement)
        if len(row) > 2 and pd.notna(row.iloc[2]):
            candidate_num = str(row.iloc[2])
            # Un numéro de candidat est généralement numérique ou contient des chiffres
            if re.match(r'^[\d,E+]+$', candidate_num.replace('.', '').replace(' ', '')):
                return True
        return False
    
    def _extract_candidate_info(self, row, level, collective_date, collective_start, jury_date):
        """Extrait les informations d'un candidat depuis une ligne"""
        try:
            # Structure attendue: Prép, Pass, Numéro candidat, NOM Prénom, Date naissance, Email, Besoins spéciaux
            prep_time = str(row.iloc[0]) if pd.notna(row.iloc[0]) else ""
            pass_time = str(row.iloc[1]) if pd.notna(row.iloc[1]) else ""
            candidate_num = str(row.iloc[2]) if pd.notna(row.iloc[2]) else ""
            name_full = str(row.iloc[3]) if pd.notna(row.iloc[3]) else ""
            birth_date = str(row.iloc[4]) if pd.notna(row.iloc[4]) else ""
            email = str(row.iloc[5]) if pd.notna(row.iloc[5]) else ""
            special_needs = str(row.iloc[6]) if pd.notna(row.iloc[6]) else "Non"
            
            # Parser le nom complet
            nom, prenom = self._parse_name(name_full)
            
            # Déterminer les dates d'examen
            exam_date = collective_date if collective_date else jury_date
            if not exam_date:
                exam_date = "2025-08-14"  # Date par défaut
            
            # Créer l'objet candidat
            candidate = {
                'numero_candidat': candidate_num,
                'nom': nom,
                'prenom': prenom,
                'email': email,
                'matiere': f"DELF {level}" if level in ['A1', 'A2', 'B1', 'B2'] else f"DALF {level}",
                'date_examen': exam_date,
                'heure_debut': collective_start if collective_start else "09:00",
                'date_collective': collective_date if collective_date else exam_date,
                'heure_collective': collective_start if collective_start else "09:00",
                'date_individuelle': jury_date if jury_date else exam_date,
                'heure_individuelle': pass_time if pass_time and pass_time != 'nan' else "14:30",
                'besoins_speciaux': special_needs,
                'niveau': level
            }
            
            return candidate
            
        except Exception as e:
            print(f"⚠️ Erreur lors de l'extraction du candidat: {e}")
            return None
    
    def _parse_name(self, name_full):
        """Parse le nom complet en nom et prénom"""
        if not name_full or name_full == 'nan':
            return "", ""
        
        # Format attendu: "NOM Prénom" ou "NOM Prénom1 Prénom2"
        parts = name_full.strip().split()
        if len(parts) >= 2:
            nom = parts[0]
            prenom = " ".join(parts[1:])
            return nom, prenom
        else:
            return name_full, ""
    
    def _parse_date(self, date_str):
        """Parse une date depuis différents formats"""
        if not date_str or date_str == 'nan':
            return None
        
        try:
            # Format DD/MM/YYYY
            if '/' in date_str:
                parts = date_str.split('/')
                if len(parts) == 3:
                    day, month, year = parts
                    return f"{year}-{month.zfill(2)}-{day.zfill(2)}"
            
            # Format DD-MM-YYYY
            if '-' in date_str and len(date_str.split('-')) == 3:
                parts = date_str.split('-')
                if len(parts[2]) == 4:  # Année à 4 chiffres
                    day, month, year = parts
                    return f"{year}-{month.zfill(2)}-{day.zfill(2)}"
            
            return date_str
            
        except Exception:
            return None
    
    def save_to_mailjet_format(self, output_path):
        """Sauvegarde les candidats au format compatible Mailjet"""
        if not self.candidates:
            print("❌ Aucun candidat à sauvegarder")
            return False
        
        try:
            # Créer un DataFrame avec les candidats
            df = pd.DataFrame(self.candidates)
            
            # Réorganiser les colonnes dans l'ordre attendu
            columns_order = [
                'numero_candidat', 'nom', 'prenom', 'email', 'matiere',
                'date_examen', 'heure_debut', 'date_collective', 'heure_collective',
                'date_individuelle', 'heure_individuelle', 'niveau', 'besoins_speciaux'
            ]
            
            # Garder seulement les colonnes qui existent
            existing_columns = [col for col in columns_order if col in df.columns]
            df = df[existing_columns]
            
            # Sauvegarder
            df.to_excel(output_path, index=False)
            print(f"✅ Candidats sauvegardés dans {output_path}")
            return True
            
        except Exception as e:
            print(f"❌ Erreur lors de la sauvegarde: {e}")
            return False

def main():
    """Fonction principale pour tester le processeur"""
    processor = JuryFileProcessor("juries_20250825_181821.xlsx")
    
    print("🔄 Traitement du fichier de jurys...")
    candidates = processor.process_jury_file()
    
    if candidates:
        print(f"\n📊 Résumé:")
        print(f"   - Total candidats: {len(candidates)}")
        
        # Compter par niveau
        levels = {}
        for candidate in candidates:
            level = candidate.get('niveau', 'Inconnu')
            levels[level] = levels.get(level, 0) + 1
        
        for level, count in sorted(levels.items()):
            print(f"   - {level}: {count} candidats")
        
        # Sauvegarder au format Mailjet
        output_file = "candidats_from_jury.xlsx"
        processor.save_to_mailjet_format(output_file)
        
        print(f"\n✅ Conversion terminée! Fichier de sortie: {output_file}")
        print("   Vous pouvez maintenant utiliser ce fichier avec le système d'emails.")
    
    else:
        print("❌ Aucun candidat trouvé dans le fichier de jurys")

if __name__ == "__main__":
    main()
