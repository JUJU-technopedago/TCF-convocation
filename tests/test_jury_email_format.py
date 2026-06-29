#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test du système d'emails avec le fichier de jurys converti
"""

import sys
import os
from datetime import datetime

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from mailjet_bridge import MailjetBridge
import pandas as pd

def test_jury_email_system():
    """Test le système d'emails avec les candidats du fichier de jurys"""
    
    print("=" * 70)
    print("TEST DU SYSTÈME D'EMAILS AVEC FICHIER DE JURYS")
    print("=" * 70)
    
    # Vérifier que le fichier converti existe
    jury_file = "candidats_from_jury.xlsx"
    if not os.path.exists(jury_file):
        print(f"❌ Fichier {jury_file} non trouvé. Exécutez d'abord jury_file_processor.py")
        return
    
    # Lire quelques candidats pour test
    try:
        df = pd.read_excel(jury_file)
        print(f"✅ Fichier chargé: {len(df)} candidats trouvés")
        
        # Afficher la structure
        print(f"\n📋 Colonnes disponibles: {list(df.columns)}")
        
        # Prendre quelques candidats de différents niveaux pour test
        test_candidates = []
        
        # Un candidat de chaque niveau si possible
        for level in ['A1', 'A2', 'B1', 'B2', 'C1', 'C2']:
            level_candidates = df[df['niveau'] == level]
            if not level_candidates.empty:
                candidate = level_candidates.iloc[0].to_dict()
                test_candidates.append(candidate)
                print(f"   - {level}: {candidate['prenom']} {candidate['nom']} ({candidate['email']})")
        
        if not test_candidates:
            print("❌ Aucun candidat de test trouvé")
            return
        
        # Créer une instance du bridge
        bridge = MailjetBridge(
            excel_path=jury_file,
            pdf_dir="output",
            sender_email="test@example.com",
            sender_name="Alliance Française Bruxelles Europe"
        )
        
        print(f"\n🧪 Test du format d'email pour {len(test_candidates)} candidats:")
        print("-" * 50)
        
        for i, candidate in enumerate(test_candidates, 1):
            print(f"\n{i}. TEST {candidate['matiere']} - {candidate['prenom']} {candidate['nom']}")
            print("   " + "-" * 45)
            
            try:
                subject, body_html, body_text = bridge._create_email_content(candidate)
                
                # Vérifications du format
                checks = {
                    'Sujet décodé': 'd\'examen' in subject,
                    'Nom en majuscules': candidate['nom'].upper() in body_html,
                    'Type DELF/DALF': candidate['matiere'] in body_html,
                    'Date française': any(month in body_html for month in ['janvier', 'février', 'mars', 'avril', 'mai', 'juin', 'juillet', 'août', 'septembre', 'octobre', 'novembre', 'décembre']),
                    '30 minutes avant': '30 minutes avant' in body_html,
                    'Couleur rouge': '#da002e' in body_html,
                    'Sections séparées': 'ÉPREUVES COLLECTIVES' in body_html and 'ÉPREUVE INDIVIDUELLE' in body_html
                }
                
                for check, result in checks.items():
                    status = "✅" if result else "❌"
                    print(f"   {status} {check}")
                
                # Afficher un extrait du contenu
                print(f"\n   📧 Sujet: {subject}")
                
                # Chercher les lignes importantes dans le HTML
                lines = body_html.split('\n')
                important_lines = []
                for line in lines:
                    line_clean = line.strip()
                    if any(keyword in line_clean for keyword in ['Bonjour', candidate['matiere'], 'ÉPREUVES COLLECTIVES', 'ÉPREUVE INDIVIDUELLE', '[IMPORTANT]']):
                        important_lines.append(line_clean)
                
                if important_lines:
                    print("   📄 Extrait du contenu:")
                    for line in important_lines[:5]:  # Limiter à 5 lignes
                        if line:
                            print(f"      {line}")
                
            except Exception as e:
                print(f"   ❌ Erreur: {e}")
        
        print(f"\n" + "=" * 70)
        print("✅ TEST TERMINÉ")
        print("   Le système est maintenant compatible avec les fichiers de jurys!")
        print("   Utilisez jury_file_processor.py pour convertir vos fichiers de jurys,")
        print("   puis utilisez le fichier converti avec le système d'emails.")
        print("=" * 70)
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")

if __name__ == "__main__":
    test_jury_email_system()
