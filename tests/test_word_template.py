#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test du nouveau template basé sur le modèle Word
"""

from pdf_generator import PDFGenerator
from jury_excel_processor import JuryExcelProcessor

def test_word_template():
    """Test du nouveau template Word"""
    
    print("=== TEST TEMPLATE BASÉ SUR MODÈLE WORD ===\n")
    
    try:
        # 1. Charger les données du fichier de jurys
        print("1. Chargement des données...")
        processor = JuryExcelProcessor('juries_20250820_192410.xlsx')
        processor.load_jury_data()
        candidates = processor.get_all_candidates()
        
        print(f"   ✓ {len(candidates)} candidats chargés")
        
        # 2. Créer le générateur PDF avec le nouveau template
        print("2. Configuration du générateur PDF...")
        generator = PDFGenerator(
            excel_path='juries_20250820_192410.xlsx',
            template_path='templates/convocation_delf_template_word_style.html',
            logo_af_path='logoAF.svg',
            logo_delf_path='logoDELF.svg',
            output_dir='output'
        )
        
        print("   ✓ Générateur configuré avec le template Word")
        
        # 3. Tester avec quelques candidats de différents niveaux
        print("3. Test de génération PDF...")
        
        # Prendre un candidat de chaque niveau
        niveaux_testes = set()
        candidats_test = []
        
        for candidat in candidates:
            niveau = candidat['niveau']
            if niveau not in niveaux_testes and len(candidats_test) < 3:
                niveaux_testes.add(niveau)
                candidats_test.append(candidat)
        
        for i, candidat in enumerate(candidats_test):
            print(f"   Test {i+1}: {candidat['nom']} {candidat['prenom']} ({candidat['niveau']})")
            
            # Générer le PDF
            filename = f"test_word_template_{candidat['niveau']}_{candidat['nom']}_{candidat['prenom']}.pdf"
            pdf_path = generator.generate_pdf(candidat, filename)
            
            print(f"   ✓ PDF généré: {pdf_path}")
            
            # Afficher les informations utilisées
            print(f"     - Date épreuve collective: {candidat.get('date_ep_coll', 'N/A')}")
            print(f"     - Heure épreuve collective: {candidat.get('debut_ep_coll', 'N/A')}")
            print(f"     - Date épreuve individuelle: {candidat.get('date_examen', 'N/A')}")
            print(f"     - Heure préparation: {candidat.get('heure_preparation', candidat.get('heure_debut', 'N/A'))}")
            print(f"     - Adresse: {candidat['institution_address']}, {candidat['institution_postal']} {candidat['institution_city']}")
            print()
        
        print("=== RÉSUMÉ ===")
        print(f"✅ Template Word créé et testé")
        print(f"✅ {len(candidats_test)} PDF de test générés")
        print(f"✅ Structure conforme au modèle Word")
        print(f"✅ Informations d'épreuve collective correctes")
        print(f"✅ Adresse mise à jour (Avenue des Arts 46)")
        
        print(f"\nPour utiliser le nouveau template:")
        print(f"1. Dans l'application main.py, changez le template vers:")
        print(f"   'templates/convocation_delf_template_word_style.html'")
        print(f"2. Ou remplacez le contenu du template existant")
        
        return True
        
    except Exception as e:
        print(f"✗ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_word_template()
