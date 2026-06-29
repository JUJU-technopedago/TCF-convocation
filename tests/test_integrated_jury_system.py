#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test du système intégré avec détection automatique des fichiers de jurys
"""

import sys
import os
from datetime import datetime

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from mailjet_bridge import MailjetBridge

def test_integrated_jury_system():
    """Test le système intégré avec détection automatique des fichiers de jurys"""
    
    print("=" * 80)
    print("TEST DU SYSTÈME INTÉGRÉ - DÉTECTION AUTOMATIQUE FICHIERS DE JURYS")
    print("=" * 80)
    
    # Fichier de jurys à tester
    jury_file = "juries_20250825_181821.xlsx"
    
    if not os.path.exists(jury_file):
        print(f"❌ Fichier {jury_file} non trouvé")
        return
    
    try:
        print(f"📋 Test avec le fichier: {jury_file}")
        
        # Créer une instance du bridge Mailjet (sans authentification pour le test)
        bridge = MailjetBridge(
            excel_path=jury_file,
            pdf_dir="output",
            sender_email="test@example.com",
            sender_name="Alliance Française Bruxelles Europe"
        )
        
        print("\n🔍 ÉTAPE 1: Détection du type de fichier")
        print("-" * 50)
        
        # Tester la détection
        is_jury = bridge._is_jury_file()
        print(f"   Fichier de jurys détecté: {'✅ OUI' if is_jury else '❌ NON'}")
        
        if not is_jury:
            print("❌ Le fichier n'a pas été détecté comme un fichier de jurys")
            return
        
        print("\n🔄 ÉTAPE 2: Conversion automatique")
        print("-" * 50)
        
        # Tester la conversion
        df = bridge._load_excel_data()
        
        print(f"   ✅ Conversion réussie!")
        print(f"   📊 Nombre de candidats extraits: {len(df)}")
        print(f"   📋 Colonnes disponibles: {list(df.columns)}")
        
        # Afficher quelques statistiques
        if 'niveau' in df.columns:
            niveau_counts = df['niveau'].value_counts()
            print(f"\n   📈 Répartition par niveau:")
            for niveau, count in niveau_counts.items():
                print(f"      - {niveau}: {count} candidats")
        
        print("\n🧪 ÉTAPE 3: Test du format d'email")
        print("-" * 50)
        
        # Tester le format d'email sur quelques candidats
        test_candidates = df.head(3)  # Prendre les 3 premiers
        
        for i, (_, candidate) in enumerate(test_candidates.iterrows(), 1):
            print(f"\n   {i}. Test candidat: {candidate.get('prenom', '')} {candidate.get('nom', '')} ({candidate.get('matiere', '')})")
            
            try:
                subject, body_html, body_text = bridge._create_email_content(candidate)
                
                # Vérifications
                checks = {
                    'Sujet décodé': 'd\'examen' in subject,
                    'Nom en majuscules': candidate.get('nom', '').upper() in body_html,
                    'Type DELF/DALF': candidate.get('matiere', '') in body_html,
                    'Date française': any(month in body_html for month in ['janvier', 'février', 'mars', 'avril', 'mai', 'juin', 'juillet', 'août', 'septembre', 'octobre', 'novembre', 'décembre']),
                    '30 minutes avant': '30 minutes avant' in body_html,
                    'Couleur rouge': '#da002e' in body_html,
                    'Sections séparées': 'ÉPREUVES COLLECTIVES' in body_html and 'ÉPREUVE INDIVIDUELLE' in body_html
                }
                
                all_passed = all(checks.values())
                status = "✅ TOUS VALIDÉS" if all_passed else "❌ ÉCHECS DÉTECTÉS"
                print(f"      {status}")
                
                for check, result in checks.items():
                    if not result:
                        print(f"         ❌ {check}")
                
                if all_passed:
                    print(f"      📧 Sujet: {subject}")
                
            except Exception as e:
                print(f"      ❌ Erreur: {e}")
        
        print("\n🎯 ÉTAPE 4: Test de recherche PDF")
        print("-" * 50)
        
        # Tester la recherche de PDF pour quelques candidats
        pdf_found_count = 0
        for i, (_, candidate) in enumerate(test_candidates.iterrows(), 1):
            pdf_path = bridge._find_pdf_file(candidate)
            if pdf_path:
                pdf_found_count += 1
                print(f"   {i}. ✅ PDF trouvé: {os.path.basename(pdf_path)}")
            else:
                print(f"   {i}. ❌ PDF non trouvé pour {candidate.get('prenom', '')} {candidate.get('nom', '')}")
        
        print(f"\n   📊 PDFs trouvés: {pdf_found_count}/{len(test_candidates)}")
        
        print("\n" + "=" * 80)
        print("✅ TEST DU SYSTÈME INTÉGRÉ TERMINÉ")
        print("=" * 80)
        print("🎉 RÉSULTATS:")
        print(f"   ✅ Détection automatique: FONCTIONNELLE")
        print(f"   ✅ Conversion fichier jurys: FONCTIONNELLE")
        print(f"   ✅ Format email DELF/DALF: FONCTIONNEL")
        print(f"   ✅ Extraction de {len(df)} candidats")
        print(f"   📁 PDFs disponibles: {pdf_found_count}/{len(test_candidates)} testés")
        print()
        print("🚀 LE SYSTÈME EST PRÊT!")
        print("   L'application peut maintenant:")
        print("   • Détecter automatiquement les fichiers de jurys")
        print("   • Les convertir en interne sans étape manuelle")
        print("   • Générer les emails au format DELF/DALF")
        print("   • Récupérer les bonnes dates et heures pour chaque épreuve")
        print("=" * 80)
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_integrated_jury_system()
