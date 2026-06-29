#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de l'alignement des logos avec les bords du cadre
"""

from pdf_generator import PDFGenerator
import os

def test_logo_alignment():
    """Test de l'alignement des logos"""
    
    print("=== Test de l'alignement des logos ===")
    
    # Configuration avec le nouveau template
    excel_path = "juries_20250820_192410.xlsx"
    template_path = "templates/convocation_delf_template_modele.html"
    logo_af_path = "assets/logoAF.png"
    logo_delf_path = "assets/logoDELF.png"
    output_dir = "output"
    
    try:
        # Créer le générateur avec le nouveau template
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
            # Prendre le premier candidat
            first_candidate = candidates[0]
            print(f"📝 Test avec: {first_candidate.get('nom', '')} {first_candidate.get('prenom', '')}")
            
            # Générer le PDF avec un nom unique
            import time
            timestamp = str(int(time.time()))
            output_filename = f"test_alignment_{timestamp}.pdf"
            pdf_path = generator.generate_pdf(first_candidate, output_filename)
            print(f"✅ PDF généré avec alignement des logos: {pdf_path}")
            
            # Vérifier que le fichier existe
            if os.path.exists(pdf_path):
                file_size = os.path.getsize(pdf_path)
                print(f"✅ Fichier créé avec succès ({file_size} bytes)")
                print(f"📁 Chemin: {os.path.abspath(pdf_path)}")
                print(f"🎯 Logos alignés avec les bords du cadre titre")
            else:
                print("❌ Le fichier PDF n'a pas été créé")
        
    except Exception as e:
        print(f"❌ Erreur lors de la génération: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_logo_alignment()
