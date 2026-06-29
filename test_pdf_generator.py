#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de test pour le générateur de PDF
"""

import os
import sys
from pdf_generator import PDFGenerator

def main():
    # Vérifier si un fichier Excel est spécifié en argument
    if len(sys.argv) > 1:
        excel_path = sys.argv[1]
    else:
        # Chercher un fichier Excel dans le répertoire courant
        excel_files = [f for f in os.listdir('.') if f.endswith('.xlsx') and 'juries_' in f]
        if excel_files:
            excel_path = excel_files[0]
            print(f"Utilisation du fichier Excel: {excel_path}")
        else:
            print("Erreur: Aucun fichier Excel trouvé!")
            print("Usage: python test_pdf_generator.py [chemin_fichier_excel]")
            return

    # Créer un répertoire de test pour les PDF
    output_dir = "output_test"
    os.makedirs(output_dir, exist_ok=True)

    # Chemin vers le template HTML
    template_path = "templates/convocation_template.html"
    if not os.path.exists(template_path):
        print(f"Attention: Le fichier de template HTML {template_path} n'existe pas!")
        # Essayer le template DOCX en fallback
        template_path = "modele_convocation.docx"
        if not os.path.exists(template_path):
            print(f"Erreur: Aucun template trouvé!")
            return

    # Chemins vers les logos
    logo_af_path = "logoAF.svg"
    logo_delf_path = "logoDELF.svg"

    # Initialiser le générateur de PDF
    generator = PDFGenerator(
        excel_path=excel_path,
        template_path=template_path,
        logo_af_path=logo_af_path,
        logo_delf_path=logo_delf_path,
        output_dir=output_dir,
        access_code="2023"
    )

    # Fonction de callback pour afficher la progression
    def print_progress(message):
        print(message)

    try:
        # Générer les PDF
        count = generator.generate_all_pdfs(print_progress)
        print(f"\nTerminé! {count} PDF générés dans le répertoire {output_dir}")
    except Exception as e:
        print(f"Erreur critique: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()