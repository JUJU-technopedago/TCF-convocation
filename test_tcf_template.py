#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test du template TCF avec le processeur TCF
"""

import os
import sys
from datetime import datetime
from tcf_excel_processor import TCFExcelProcessor
from pdf_generator import PDFGenerator

def test_tcf_template():
    """Test de génération d'un PDF TCF avec le nouveau template"""
    
    print("=== TEST DU TEMPLATE TCF ===")
    print("=" * 40)
    
    # 1. Charger les données TCF
    print("1. Chargement des données TCF...")
    processor = TCFExcelProcessor("JURYS FINAL TCF.xlsx")
    
    if not processor.load_tcf_data():
        print("❌ Erreur lors du chargement des données TCF")
        return False
        
    processor.print_summary()
    
    # 2. Récupérer quelques candidats de test
    candidates = processor.get_all_candidates()
    if not candidates:
        print("❌ Aucun candidat trouvé")
        return False
    
    print(f"\n2. Test avec les premiers candidats...")
    
    # Prendre un candidat de chaque type TCF si possible
    test_candidates = []
    tcf_types_tested = set()
    
    for candidate in candidates:
        tcf_type = candidate.get('tcf_type')
        if tcf_type not in tcf_types_tested:
            test_candidates.append(candidate)
            tcf_types_tested.add(tcf_type)
            if len(test_candidates) >= 3:  # Limiter à 3 tests
                break
    
    # 3. Créer le répertoire de sortie
    output_dir = f"output_test_tcf_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    os.makedirs(output_dir, exist_ok=True)
    print(f"Répertoire de sortie: {output_dir}")
    
    # 4. Configurer le générateur PDF avec le template TCF
    try:
        generator = PDFGenerator(
            excel_path="JURYS FINAL TCF.xlsx",
            template_path="templates/convocation_tcf_template_modele.html",
            logo_af_path="assets/logoAF.png",  # Logo AF existant
            logo_delf_path="assets/logoDELF.png",  # Temporaire, sera remplacé par logo TCF
            output_dir=output_dir,
            access_code="AF2025"
        )
        
        print(f"✅ Générateur PDF configuré avec template TCF")
        
        # 5. Générer les PDF de test
        success_count = 0
        
        for i, candidate in enumerate(test_candidates, 1):
            try:
                print(f"\n--- Test {i}: {candidate['prenom']} {candidate['nom']} ---")
                print(f"Type TCF: {candidate['tcf_type']}")
                print(f"Jury: {candidate['jury_name']}")
                print(f"Date: {candidate['date_examen']}")
                print(f"Épreuve collective: {candidate['debut_ep_coll']}-{candidate['fin_ep_coll']}")
                if candidate.get('has_individual_exam'):
                    print(f"Épreuve individuelle: {candidate['heure_preparation']}")
                else:
                    print("Pas d'épreuve individuelle")
                
                # Générer le PDF
                output_filename = f"test_tcf_{candidate['tcf_type'].replace(' ', '_')}_{candidate['nom']}_{candidate['prenom']}.pdf"
                pdf_path = generator.generate_pdf(candidate, output_filename)
                
                if os.path.exists(pdf_path):
                    file_size = os.path.getsize(pdf_path)
                    print(f"✅ PDF généré: {os.path.basename(pdf_path)} ({file_size} bytes)")
                    success_count += 1
                else:
                    print(f"❌ PDF non trouvé: {pdf_path}")
                    
            except Exception as e:
                print(f"❌ Erreur pour {candidate['prenom']} {candidate['nom']}: {e}")
        
        # 6. Résumé
        print(f"\n=== RÉSUMÉ DU TEST ===")
        print(f"PDF générés avec succès: {success_count}/{len(test_candidates)}")
        print(f"Répertoire: {output_dir}")
        
        if success_count > 0:
            print(f"\n🎉 Test réussi ! Vous pouvez vérifier les PDF dans le dossier {output_dir}")
            return True
        else:
            print(f"\n❌ Aucun PDF généré correctement")
            return False
            
    except Exception as e:
        print(f"❌ Erreur lors de la configuration du générateur: {e}")
        return False

def test_template_data_preparation():
    """Test spécifique de la préparation des données pour le template"""
    
    print("\n=== TEST PRÉPARATION DONNÉES TEMPLATE ===")
    
    # Charger un candidat
    processor = TCFExcelProcessor("JURYS FINAL TCF.xlsx")
    processor.load_tcf_data()
    candidates = processor.get_all_candidates()
    
    if candidates:
        candidate = candidates[0]
        print(f"Test avec: {candidate['prenom']} {candidate['nom']}")
        
        # Simuler la préparation des données template
        from pdf_generator import PDFGenerator
        
        generator = PDFGenerator(
            excel_path="JURYS FINAL TCF.xlsx",
            template_path="templates/convocation_tcf_template_modele.html",
            logo_af_path="assets/logoAF.png",
            logo_delf_path="assets/logoDELF.png",
            output_dir="test_output"
        )
        
        template_data = generator._prepare_template_data(candidate)
        
        print("\nDonnées préparées pour le template:")
        for key, value in template_data.items():
            print(f"  {key}: {value}")
            
        return True
    
    return False

if __name__ == "__main__":
    print("🚀 LANCEMENT DES TESTS TCF")
    
    # Test 1: Préparation des données
    if test_template_data_preparation():
        print("\n" + "="*50)
        # Test 2: Génération complète
        test_tcf_template()
    else:
        print("❌ Échec du test de préparation des données")