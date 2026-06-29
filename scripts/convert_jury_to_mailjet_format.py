#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Convertit les données des jurys vers le format Excel attendu par le système Mailjet
Crée un fichier Excel compatible avec mailjet_bridge.py
"""

import pandas as pd
import os
from datetime import datetime
from extract_jury_emails import JuryEmailExtractor

class JuryToMailjetConverter:
    def __init__(self, jury_excel_path):
        """
        Initialise le convertisseur
        
        Args:
            jury_excel_path (str): Chemin vers le fichier Excel des jurys
        """
        self.jury_excel_path = jury_excel_path
        self.extractor = JuryEmailExtractor(jury_excel_path)
        
    def convert_to_mailjet_format(self, output_path="candidats_pour_mailjet.xlsx"):
        """
        Convertit les données des jurys vers le format attendu par Mailjet
        
        Args:
            output_path (str): Chemin de sortie du fichier Excel
            
        Returns:
            str: Chemin du fichier créé
        """
        print(f"🔄 Conversion des données de jurys vers le format Mailjet...")
        
        # Extraire les données des jurys
        results = self.extractor.extract_jury_emails()
        
        # Convertir vers le format attendu par mailjet_bridge.py
        mailjet_data = []
        
        for candidate in results['candidates_details']:
            # Créer un enregistrement au format attendu par mailjet_bridge.py
            record = {
                'numero_candidat': candidate['numero_candidat'],
                'nom': candidate['nom'],
                'prenom': candidate['prenom'],
                'email': candidate['email'],
                'date_naissance': candidate['date_naissance'],
                'niveau': candidate['niveau'],
                'matiere': f"DELF {candidate['niveau']}",
                'date_examen': candidate['date_jury'],
                'heure_debut': candidate['heure_preparation'] if candidate['heure_preparation'] else '09:00',
                'heure_fin': self._calculate_end_time(candidate['heure_preparation'], candidate['niveau']),
                'duree': self._get_duree_by_niveau(candidate['niveau']),
                'salle': 'Salle d\'examen',
                'heure_preparation': candidate['heure_preparation'],
                'heure_passage': candidate['heure_passage'],
                'besoins_speciaux': candidate.get('besoins_speciaux', 'Non'),
                'institution_name': 'Alliance Française Bruxelles Europe',
                'institution_address': 'Avenue des Arts 46',
                'institution_city': 'Bruxelles',
                'institution_postal': '1000',
                'institution_phone': '+32 2 788 21 60',
                'contact_urgence': 'info@alliancefrancaise.be'
            }
            
            mailjet_data.append(record)
        
        # Créer le DataFrame
        df = pd.DataFrame(mailjet_data)
        
        # Sauvegarder en Excel
        df.to_excel(output_path, index=False, engine='openpyxl')
        
        print(f"✅ Fichier créé: {output_path}")
        print(f"📊 {len(mailjet_data)} candidats convertis")
        print(f"📧 Emails inclus pour l'envoi via Mailjet")
        
        # Afficher un aperçu
        print(f"\n📋 Aperçu des données converties:")
        print(f"{'Nom':<20} {'Prénom':<15} {'Email':<30} {'Niveau':<6}")
        print("-" * 75)
        
        for i, candidate in enumerate(mailjet_data[:10]):
            nom = candidate['nom'][:19]
            prenom = candidate['prenom'][:14]
            email = candidate['email'][:29]
            niveau = candidate['niveau']
            print(f"{nom:<20} {prenom:<15} {email:<30} {niveau:<6}")
        
        if len(mailjet_data) > 10:
            print(f"... et {len(mailjet_data) - 10} autres candidats")
        
        return output_path
    
    def _get_duree_by_niveau(self, niveau):
        """Retourne la durée d'examen selon le niveau"""
        durees = {
            'A1': '1h20 (collective) + 5-7min (individuelle)',
            'A2': '1h40 (collective) + 6-8min (individuelle)',
            'B1': '1h45 (collective) + 15min (individuelle)',
            'B2': '2h30 (collective) + 20min (individuelle)',
            'C1': '4h (collective) + 30min (individuelle)',
            'C2': '3h30 (collective) + 30min (individuelle)'
        }
        return durees.get(niveau, '2h')
    
    def _calculate_end_time(self, start_time, niveau):
        """Calcule l'heure de fin approximative"""
        if not start_time:
            return ''
        
        try:
            from datetime import datetime, timedelta
            
            # Parser l'heure de début
            start = datetime.strptime(start_time, '%H:%M')
            
            # Durée approximative en minutes selon le niveau
            durations = {
                'A1': 90,   # 1h20 + 10min
                'A2': 110,  # 1h40 + 10min
                'B1': 120,  # 1h45 + 15min
                'B2': 170,  # 2h30 + 20min
                'C1': 270,  # 4h + 30min
                'C2': 240   # 3h30 + 30min
            }
            
            duration_minutes = durations.get(niveau, 120)
            end = start + timedelta(minutes=duration_minutes)
            return end.strftime('%H:%M')
            
        except:
            return ''
    
    def create_test_email_list(self, output_path="test_emails.txt"):
        """
        Crée une liste simple des emails pour test
        
        Args:
            output_path (str): Chemin de sortie du fichier texte
        """
        results = self.extractor.extract_jury_emails()
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("# Liste des emails des candidats pour test Mailjet\n")
            f.write(f"# Générée le {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
            f.write(f"# Total: {len(results['all_emails'])} emails\n\n")
            
            for email in results['all_emails']:
                f.write(f"{email}\n")
        
        print(f"📧 Liste d'emails créée: {output_path}")
        return output_path

def main():
    """Fonction principale"""
    jury_file = "juries_20250825_181821.xlsx"
    
    if not os.path.exists(jury_file):
        print(f"❌ Erreur: Le fichier {jury_file} n'existe pas.")
        return
    
    try:
        # Créer le convertisseur
        converter = JuryToMailjetConverter(jury_file)
        
        # Convertir vers le format Mailjet
        mailjet_file = converter.convert_to_mailjet_format()
        
        # Créer aussi une liste simple des emails
        email_list_file = converter.create_test_email_list()
        
        print(f"\n✅ Conversion terminée!")
        print(f"📁 Fichier Excel pour Mailjet: {mailjet_file}")
        print(f"📧 Liste des emails: {email_list_file}")
        print(f"\n💡 Instructions:")
        print(f"   1. Utilisez le fichier '{mailjet_file}' avec votre système Mailjet")
        print(f"   2. Ce fichier contient tous les emails des candidats ventilés dans les jurys")
        print(f"   3. Le format est compatible avec mailjet_bridge.py")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    main()
