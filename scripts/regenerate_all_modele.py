#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Régénération de tous les PDF avec le template modèle (encadrés gris)
"""

from pdf_generator import PDFGenerator
import os

def regenerate_all_with_modele():
    """Régénère tous les PDF avec le template modèle"""
    
    print("=== Régénération de tous les PDF avec template MODÈLE ===")
    
    # Configuration avec le template modèle
    excel_path = "juries_20250820_192410.xlsx"
    template_path = "templates/convocation_delf_template_modele.html"
    logo_af_path = "assets/logoAF.png"
    logo_delf_path = "assets/logoDELF.png"
    output_dir = "output"
    
    try:
        # Créer le générateur avec le template modèle
        generator = PDFGenerator(
            excel_path=excel_path,
            template_path=template_path,
            logo_af_path=logo_af_path,
            logo_delf_path=logo_delf_path,
            output_dir=output_dir
        )
        
        print("✅ Générateur PDF initialisé avec le template MODÈLE")
        print("🎨 Template utilisé: encadrés gris comme dans votre modèle")
        
        def progress_callback(message):
            print(message)
        
        # Générer tous les PDF
        success_count = generator.generate_all_pdfs(progress_callback)
        
        print(f"\n🎉 Régénération terminée avec le template MODÈLE!")
        print(f"📊 {success_count} PDF générés avec succès")
        print("✨ Tous les PDF ont maintenant l'apparence avec encadrés gris")
        
        # Lister les fichiers générés
        if os.path.exists(output_dir):
            pdf_files = [f for f in os.listdir(output_dir) if f.endswith('.pdf') and not f.startswith('test_')]
            print(f"\n📁 Fichiers PDF de convocation dans {output_dir}:")
            for pdf_file in sorted(pdf_files):
                file_path = os.path.join(output_dir, pdf_file)
                file_size = os.path.getsize(file_path)
                print(f"  📄 {pdf_file} ({file_size} bytes)")
        
        print(f"\n✅ Tous les PDF ont été régénérés avec le nouveau design!")
        print(f"🎨 Caractéristiques du nouveau template:")
        print(f"   - Encadrés gris pour les titres")
        print(f"   - Logos bien positionnés")
        print(f"   - Mise en page structurée")
        print(f"   - Apparence identique au modèle demandé")
        
    except Exception as e:
        print(f"❌ Erreur lors de la génération: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    regenerate_all_with_modele()
