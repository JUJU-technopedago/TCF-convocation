#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de génération PDF avec les corrections appliquées
"""

from pdf_generator import PDFGenerator
import os

def test_pdf_generation():
    """Test de génération d'un PDF avec le template corrigé"""
    
    print("=== Test de génération PDF corrigé ===")
    
    # Configuration
    excel_path = "juries_20250820_192410.xlsx"
    template_path = "templates/convocation_delf_template_word_style.html"
    logo_af_path = "assets/logoAF.png"
    logo_delf_path = "assets/logoDELF.png"
    output_dir = "output"
    
    # Vérifier que les fichiers existent
    if not os.path.exists(excel_path):
        print(f"❌ Fichier Excel non trouvé: {excel_path}")
        return
    
    if not os.path.exists(template_path):
        print(f"❌ Template non trouvé: {template_path}")
        return
        
    if not os.path.exists(logo_af_path):
        print(f"❌ Logo AF non trouvé: {logo_af_path}")
        return
        
    if not os.path.exists(logo_delf_path):
        print(f"❌ Logo DELF non trouvé: {logo_delf_path}")
        return
    
    print("✅ Tous les fichiers requis sont présents")
    
    try:
        # Créer le générateur
        generator = PDFGenerator(
            excel_path=excel_path,
            template_path=template_path,
            logo_af_path=logo_af_path,
            logo_delf_path=logo_delf_path,
            output_dir=output_dir
        )
        
        print("✅ Générateur PDF initialisé")
        
        # Obtenir la liste des candidats
        candidates = generator.get_candidate_list()
        print(f"✅ Trouvé {len(candidates)} candidats")
        
        if candidates:
            # Prendre le premier candidat pour le test
            first_candidate = candidates[0]
            print(f"📝 Test avec: {first_candidate.get('nom', '')} {first_candidate.get('prenom', '')}")
            
            # Générer le PDF
            pdf_path = generator.generate_pdf(first_candidate)
            print(f"✅ PDF généré: {pdf_path}")
            
            # Vérifier que le fichier existe
            if os.path.exists(pdf_path):
                file_size = os.path.getsize(pdf_path)
                print(f"✅ Fichier créé avec succès ({file_size} bytes)")
                print(f"📁 Chemin: {os.path.abspath(pdf_path)}")
            else:
                print("❌ Le fichier PDF n'a pas été créé")
        
    except Exception as e:
        print(f"❌ Erreur lors de la génération: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_pdf_generation()
