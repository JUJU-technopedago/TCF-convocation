#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Régénération de tous les PDF avec le template corrigé
"""

from pdf_generator import PDFGenerator
import os

def regenerate_all_pdfs():
    """Régénère tous les PDF avec le template corrigé"""
    
    print("=== Régénération de tous les PDF avec template corrigé ===")
    
    # Configuration
    excel_path = "juries_20250820_192410.xlsx"
    template_path = "templates/convocation_delf_template_word_style.html"
    logo_af_path = "assets/logoAF.png"
    logo_delf_path = "assets/logoDELF.png"
    output_dir = "output"
    
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
        
        def progress_callback(message):
            print(message)
        
        # Générer tous les PDF
        success_count = generator.generate_all_pdfs(progress_callback)
        
        print(f"\n🎉 Régénération terminée!")
        print(f"📊 {success_count} PDF générés avec succès")
        
        # Lister les fichiers générés
        if os.path.exists(output_dir):
            pdf_files = [f for f in os.listdir(output_dir) if f.endswith('.pdf')]
            print(f"\n📁 Fichiers PDF dans {output_dir}:")
            for pdf_file in sorted(pdf_files):
                file_path = os.path.join(output_dir, pdf_file)
                file_size = os.path.getsize(file_path)
                print(f"  📄 {pdf_file} ({file_size} bytes)")
        
    except Exception as e:
        print(f"❌ Erreur lors de la génération: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    regenerate_all_pdfs()
