#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de génération des convocations TCF
Version sans émojis pour éviter les erreurs d'encodage
"""

import os
import sys

# Configuration du chemin
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Import des modules
from tcf_excel_processor import TCFExcelProcessor
from pdf_generator import PDFGenerator

def main():
    # Fichier Excel
    excel_file = "JURYS FINAL TCF.xlsx"
    
    # Charger les données
    print("Chargement des donnees TCF...")
    processor = TCFExcelProcessor(excel_file)
    
    if not processor.load_tcf_data():
        print("Erreur lors du chargement des donnees")
        return
    
    # Récupérer tous les candidats (déjà fusionnés)
    candidates = processor.get_all_candidates()
    print(f"Total candidats: {len(candidates)}")
    
    # Générer les PDFs
    print("\nGeneration des PDFs...")
    pdf_gen = PDFGenerator(
        template_path="templates/convocation_tcf_template_modele.html",
        output_dir="output"
    )
    
    for i, candidate in enumerate(candidates, 1):
        try:
            nom = candidate.get('nom', 'INCONNU')
            prenom = candidate.get('prenom', '')
            is_multi = candidate.get('is_multi_exam', False)
            
            if is_multi:
                print(f"[{i}/{len(candidates)}] MULTI-EPREUVE: {nom} {prenom}")
            else:
                print(f"[{i}/{len(candidates)}] {nom} {prenom}")
            
            pdf_path = pdf_gen.generate_pdf(candidate)
            print(f"  -> PDF genere: {os.path.basename(pdf_path)}")
            
        except Exception as e:
            print(f"  -> ERREUR: {e}")
    
    print(f"\nTermine! {len(candidates)} PDFs generes dans output/")

if __name__ == "__main__":
    main()
