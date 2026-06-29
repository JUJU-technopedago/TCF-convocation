#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Programme pour extraire les emails des candidats ventilés dans les jurys DELF
Identifie tous les candidats qui ont été assignés à des jurys avec leurs emails
"""

import pandas as pd
import os
from datetime import datetime
import json

class JuryEmailExtractor:
    def __init__(self, excel_path):
        """
        Initialise l'extracteur d'emails des jurys
        
        Args:
            excel_path (str): Chemin vers le fichier Excel des jurys
        """
        self.excel_path = excel_path
        self.jury_candidates = []
        self.emails_by_jury = {}
        self.all_emails = set()
        
    def extract_jury_emails(self):
        """
        Extrait tous les emails des candidats ventilés dans les jurys
        
        Returns:
            dict: Dictionnaire avec les emails organisés par jury et niveau
        """
        try:
            print(f"📁 Lecture du fichier: {self.excel_path}")
            
            # Charger toutes les feuilles du fichier Excel
            all_sheets = pd.read_excel(
                self.excel_path, 
                sheet_name=None, 
                engine='openpyxl',
                header=None
            )
            
            results = {
                'summary': {
                    'total_candidates': 0,
                    'total_emails': 0,
                    'levels_processed': [],
                    'juries_processed': [],
                    'extraction_date': datetime.now().strftime('%d/%m/%Y %H:%M:%S')
                },
                'by_level': {},
                'by_jury': {},
                'all_emails': [],
                'candidates_details': []
            }
            
            # Traiter chaque niveau (ignorer la feuille ADMIN)
            for sheet_name, df in all_sheets.items():
                if sheet_name.startswith('Niveau '):
                    niveau = sheet_name.replace('Niveau ', '')
                    print(f"\n=== Traitement du niveau {niveau} ===")
                    
                    level_data = self._process_level_sheet(df, niveau)
                    results['by_level'][niveau] = level_data
                    
                    # Ajouter au résumé
                    results['summary']['levels_processed'].append(niveau)
                    results['summary']['total_candidates'] += level_data['total_candidates']
                    
                    # Ajouter les jurys traités
                    for jury_info in level_data['juries']:
                        jury_key = f"{niveau} - {jury_info['jury_name']}"
                        results['by_jury'][jury_key] = jury_info
                        results['summary']['juries_processed'].append(jury_key)
                        
                        print(f"  📋 {jury_info['jury_name']}: {len(jury_info['candidates'])} candidats")
                        
                        # Ajouter les emails à la liste globale
                        for candidate in jury_info['candidates']:
                            if candidate['email'] and candidate['email'] not in self.all_emails:
                                self.all_emails.add(candidate['email'])
                                results['candidates_details'].append({
                                    'niveau': niveau,
                                    'jury': jury_info['jury_name'],
                                    'date_jury': jury_info['date'],
                                    'nom': candidate['nom'],
                                    'prenom': candidate['prenom'],
                                    'email': candidate['email'],
                                    'numero_candidat': candidate['numero_candidat'],
                                    'date_naissance': candidate['date_naissance'],
                                    'heure_preparation': candidate['heure_preparation'],
                                    'heure_passage': candidate['heure_passage'],
                                    'besoins_speciaux': candidate.get('besoins_speciaux', 'Non')
                                })
            
            # Finaliser le résumé
            results['all_emails'] = sorted(list(self.all_emails))
            results['summary']['total_emails'] = len(self.all_emails)
            
            print(f"\n✅ Extraction terminée:")
            print(f"   📊 {results['summary']['total_candidates']} candidats trouvés")
            print(f"   📧 {results['summary']['total_emails']} emails uniques extraits")
            print(f"   📚 {len(results['summary']['levels_processed'])} niveaux traités")
            print(f"   ⚖️ {len(results['summary']['juries_processed'])} jurys traités")
            
            return results
            
        except Exception as e:
            raise Exception(f"Erreur lors de l'extraction des emails: {e}")
    
    def _process_level_sheet(self, df, niveau):
        """
        Traite une feuille de niveau spécifique
        
        Args:
            df (DataFrame): Données de la feuille
            niveau (str): Niveau DELF (A1, A2, B1, B2, C1, C2)
            
        Returns:
            dict: Données structurées du niveau
        """
        level_data = {
            'niveau': niveau,
            'total_candidates': 0,
            'juries': [],
            'epreuve_collective': {}
        }
        
        current_jury = None
        
        # Traiter ligne par ligne
        for index, row in df.iterrows():
            row_values = [str(val) if pd.notna(val) else '' for val in row.values]
            
            # Détecter les informations d'épreuve collective (première ligne)
            if index == 0:
                if len(row_values) > 3 and row_values[3]:  # Date en colonne D
                    level_data['epreuve_collective']['date'] = row_values[3]
                if len(row_values) > 5 and row_values[5]:  # Heure début en colonne F
                    level_data['epreuve_collective']['debut'] = row_values[5]
                if len(row_values) > 7 and row_values[7]:  # Heure fin en colonne H
                    level_data['epreuve_collective']['fin'] = row_values[7]
            
            # Détecter un nouveau jury
            elif len(row_values) > 0 and row_values[0].startswith('Jury '):
                # Sauvegarder le jury précédent
                if current_jury is not None:
                    level_data['juries'].append(current_jury)
                    level_data['total_candidates'] += len(current_jury['candidates'])
                
                # Créer un nouveau jury
                jury_name = row_values[0]
                jury_date = row_values[1] if len(row_values) > 1 and row_values[1] else ''
                
                current_jury = {
                    'jury_name': jury_name,
                    'date': jury_date,
                    'candidates': []
                }
            
            # Détecter les candidats (lignes avec numéro de candidat)
            elif len(row_values) >= 6 and self._is_candidate_row(row_values):
                if current_jury is None:
                    # Créer un jury par défaut si pas encore défini
                    current_jury = {
                        'jury_name': 'Jury 1',
                        'date': '',
                        'candidates': []
                    }
                
                candidat = self._parse_candidate_row(row_values, niveau, current_jury['date'])
                if candidat:
                    current_jury['candidates'].append(candidat)
        
        # Ajouter le dernier jury
        if current_jury is not None:
            level_data['juries'].append(current_jury)
            level_data['total_candidates'] += len(current_jury['candidates'])
        
        return level_data
    
    def _is_candidate_row(self, row_values):
        """
        Vérifie si une ligne contient des données de candidat
        Structure attendue: Prép. | Pass. | Numéro candidat | NOM Prénom | Date naissance | Email | Besoins spéciaux
        """
        # Vérifier s'il y a un numéro de candidat en colonne 2 (index 2)
        if len(row_values) > 2:
            numero_candidat = str(row_values[2]).strip()
            # Un numéro de candidat est un nombre long (au moins 8 chiffres)
            if numero_candidat and (numero_candidat.replace('.', '').replace('E+', '').replace(',', '').isdigit() or 'E+' in numero_candidat):
                return len(numero_candidat.replace('.', '').replace('E+', '').replace(',', '')) >= 8
        return False
    
    def _parse_candidate_row(self, row_values, niveau, jury_date):
        """
        Parse une ligne de candidat
        Structure: Prép. | Pass. | Numéro candidat | NOM Prénom | Date naissance | Email | Besoins spéciaux
        """
        try:
            if len(row_values) < 6:
                return None
            
            # Extraire les données selon la structure connue
            heure_preparation = str(row_values[0]).strip() if row_values[0] else ''
            heure_passage = str(row_values[1]).strip() if row_values[1] else ''
            numero_candidat = str(row_values[2]).strip() if row_values[2] else ''
            nom_prenom = str(row_values[3]).strip() if row_values[3] else ''
            date_naissance = str(row_values[4]).strip() if row_values[4] else ''
            email = str(row_values[5]).strip() if row_values[5] else ''
            besoins_speciaux = str(row_values[6]).strip() if len(row_values) > 6 and row_values[6] else 'Non'
            
            # Vérifier que nous avons au minimum un numéro de candidat et un email
            if not numero_candidat or not email or email.lower() == 'nan':
                return None
            
            # Parser le nom et prénom
            nom, prenom = self._parse_nom_prenom(nom_prenom)
            
            candidat = {
                'numero_candidat': numero_candidat,
                'nom': nom,
                'prenom': prenom,
                'email': email,
                'date_naissance': date_naissance,
                'niveau': niveau,
                'date_jury': jury_date,
                'heure_preparation': heure_preparation,
                'heure_passage': heure_passage,
                'besoins_speciaux': besoins_speciaux
            }
            
            return candidat
            
        except Exception as e:
            print(f"⚠️  Erreur lors du parsing du candidat: {e}")
            return None
    
    def _parse_nom_prenom(self, nom_prenom):
        """Parse le nom et prénom depuis une chaîne 'NOM Prénom'"""
        if not nom_prenom:
            return '', ''
        
        parts = nom_prenom.strip().split(' ')
        if len(parts) >= 2:
            nom = parts[0]
            prenom = ' '.join(parts[1:])
        else:
            nom = nom_prenom
            prenom = ''
        
        return nom, prenom
    
    def save_results_to_files(self, results, output_dir="output_emails"):
        """
        Sauvegarde les résultats dans différents formats
        
        Args:
            results (dict): Résultats de l'extraction
            output_dir (str): Répertoire de sortie
        """
        # Créer le répertoire de sortie
        os.makedirs(output_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # 1. Sauvegarder le rapport complet en JSON
        json_file = os.path.join(output_dir, f'jury_emails_complete_{timestamp}.json')
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"📄 Rapport complet sauvegardé: {json_file}")
        
        # 2. Sauvegarder la liste simple des emails
        emails_file = os.path.join(output_dir, f'emails_list_{timestamp}.txt')
        with open(emails_file, 'w', encoding='utf-8') as f:
            f.write("# Liste des emails des candidats ventilés dans les jurys DELF\n")
            f.write(f"# Extraction du {results['summary']['extraction_date']}\n")
            f.write(f"# Total: {results['summary']['total_emails']} emails\n\n")
            for email in results['all_emails']:
                f.write(f"{email}\n")
        print(f"📧 Liste des emails sauvegardée: {emails_file}")
        
        # 3. Sauvegarder les détails des candidats en CSV
        if results['candidates_details']:
            csv_file = os.path.join(output_dir, f'candidats_details_{timestamp}.csv')
            df_candidates = pd.DataFrame(results['candidates_details'])
            df_candidates.to_csv(csv_file, index=False, encoding='utf-8-sig')
            print(f"📊 Détails des candidats sauvegardés: {csv_file}")
        
        # 4. Sauvegarder un résumé par jury
        summary_file = os.path.join(output_dir, f'resume_par_jury_{timestamp}.txt')
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write("# Résumé des candidats par jury\n")
            f.write(f"# Extraction du {results['summary']['extraction_date']}\n\n")
            
            for niveau in results['summary']['levels_processed']:
                f.write(f"\n=== NIVEAU {niveau} ===\n")
                level_data = results['by_level'][niveau]
                
                for jury in level_data['juries']:
                    f.write(f"\n{jury['jury_name']} ({jury['date']})\n")
                    f.write(f"Candidats: {len(jury['candidates'])}\n")
                    
                    for candidate in jury['candidates']:
                        f.write(f"  - {candidate['nom']} {candidate['prenom']} ({candidate['email']})\n")
        
        print(f"📋 Résumé par jury sauvegardé: {summary_file}")
        
        return {
            'json_file': json_file,
            'emails_file': emails_file,
            'csv_file': csv_file if results['candidates_details'] else None,
            'summary_file': summary_file
        }
    
    def print_summary(self, results):
        """Affiche un résumé des résultats"""
        print(f"\n" + "="*60)
        print(f"📊 RÉSUMÉ DE L'EXTRACTION DES EMAILS")
        print(f"="*60)
        print(f"📁 Fichier traité: {os.path.basename(self.excel_path)}")
        print(f"📅 Date d'extraction: {results['summary']['extraction_date']}")
        print(f"📚 Niveaux traités: {', '.join(results['summary']['levels_processed'])}")
        print(f"⚖️ Nombre de jurys: {len(results['summary']['juries_processed'])}")
        print(f"👥 Total candidats: {results['summary']['total_candidates']}")
        print(f"📧 Emails uniques: {results['summary']['total_emails']}")
        
        print(f"\n📋 Détail par niveau:")
        for niveau in results['summary']['levels_processed']:
            level_data = results['by_level'][niveau]
            print(f"  • {niveau}: {level_data['total_candidates']} candidats, {len(level_data['juries'])} jury(s)")
        
        print(f"\n📧 Premiers emails extraits:")
        for i, email in enumerate(results['all_emails'][:10]):
            print(f"  {i+1:2d}. {email}")
        
        if len(results['all_emails']) > 10:
            print(f"  ... et {len(results['all_emails']) - 10} autres emails")
        
        print(f"="*60)

def main():
    """Fonction principale"""
    # Fichier à traiter
    excel_file = "juries_20250825_181821.xlsx"
    
    if not os.path.exists(excel_file):
        print(f"❌ Erreur: Le fichier {excel_file} n'existe pas.")
        return
    
    try:
        # Créer l'extracteur
        extractor = JuryEmailExtractor(excel_file)
        
        # Extraire les emails
        results = extractor.extract_jury_emails()
        
        # Afficher le résumé
        extractor.print_summary(results)
        
        # Sauvegarder les résultats
        files_created = extractor.save_results_to_files(results)
        
        print(f"\n✅ Extraction terminée avec succès!")
        print(f"📁 Fichiers créés dans le dossier 'output_emails/'")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    main()
