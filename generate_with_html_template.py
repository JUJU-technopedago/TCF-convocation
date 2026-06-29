#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour générer des convocations avec le template HTML spécifique
"""

import os
import sys
from pdf_generator import PDFGenerator

def print_progress(message):
    print(message)

def generate_convocations(excel_path, output_dir="output_html_template"):
    """
    Génère les convocations avec le template HTML spécifique
    """
    # Chemin absolu vers le template HTML
    template_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                                "templates", "convocation_delf_template_modele.html")
    
    # Vérifier que le template existe
    if not os.path.exists(template_path):
        print(f"ERREUR: Le template HTML '{template_path}' n'existe pas!")
        return 0
        
    print(f"=== GÉNÉRATEUR DE CONVOCATIONS AVEC TEMPLATE HTML ===")
    print(f"Fichier Excel: {excel_path}")
    print(f"Template HTML: {template_path}")
    print(f"Répertoire de sortie: {output_dir}")
    print(f"=========================================================")
    
    # Créer le répertoire de sortie s'il n'existe pas
    os.makedirs(output_dir, exist_ok=True)
    
    # Créer le générateur de PDF avec le template HTML
    generator = PDFGenerator(
        excel_path=excel_path,
        template_path=template_path,
        logo_af_path="assets/logoAF.png",
        logo_delf_path="assets/logoDELF.png",
        output_dir=output_dir,
        access_code="1234"  # Remplacez par le code d'accès réel si nécessaire
    )
    
    # Générer les PDF
    print("\nDémarrage de la génération des PDF...")
    count = generator.generate_all_pdfs(print_progress)
    
    print(f"\n=== GÉNÉRATION TERMINÉE ===")
    print(f"{count} PDF générés avec succès dans {output_dir}")
    
    return count

if __name__ == "__main__":
    # Vérifier les arguments
    if len(sys.argv) < 2:
        print("Usage: python generate_with_html_template.py <fichier_excel> [output_dir]")
        sys.exit(1)
    
    # Récupérer les arguments
    excel_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "output_html_template"
    
    # Vérifier que le fichier Excel existe
    if not os.path.exists(excel_path):
        print(f"ERREUR: Le fichier Excel '{excel_path}' n'existe pas.")
        sys.exit(1)
    
    # Générer les convocations
    try:
        generate_convocations(excel_path, output_dir)
    except Exception as e:
        print(f"ERREUR lors de la génération des convocations: {e}")
        sys.exit(1)