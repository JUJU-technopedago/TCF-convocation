#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour tester la génération de PDF avec la nouvelle fonction _calculate_end_time
"""

import os
import sys
import logging
from jury_excel_processor import JuryExcelProcessor
from pdf_generator import PDFGenerator

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger()

def test_generation_pdf():
    # Fichier Excel avec les données des jurys
    excel_file = "juries_20250825_181821.xlsx"
    
    if not os.path.exists(excel_file):
        logger.error(f"Fichier Excel non trouvé: {excel_file}")
        excel_file = "juries_20250820_192410.xlsx"
        
        if not os.path.exists(excel_file):
            logger.error(f"Fichier Excel alternatif non trouvé: {excel_file}")
            excel_file = "JURYS.xlsx"
            
            if not os.path.exists(excel_file):
                logger.error(f"Aucun fichier de jurys trouvé")
                return
    
    logger.info(f"Utilisation du fichier Excel: {excel_file}")
    
    # Chargement des données
    processor = JuryExcelProcessor(excel_file)
    try:
        processor.load_jury_data()
        candidates = processor.get_all_candidates()
        logger.info(f"Trouvé {len(candidates)} candidats au total")
    except Exception as e:
        logger.error(f"Erreur lors du chargement des candidats: {e}")
        return
    
    # Initialisation du générateur de PDF
    template_path = os.path.join("templates", "convocation_delf_template_modele.html")
    logo_af_path = "logoAF.svg"
    logo_delf_path = "logoDELF.svg"
    output_dir = "output_test_generation"
    
    # Création du répertoire de sortie
    os.makedirs(output_dir, exist_ok=True)
    
    # Création du générateur de PDF
    pdf_generator = PDFGenerator(
        excel_path=excel_file,
        template_path=template_path,
        logo_af_path=logo_af_path,
        logo_delf_path=logo_delf_path,
        output_dir=output_dir
    )
    
    # Génération des PDF pour chaque candidat
    success_count = 0
    error_count = 0
    
    for i, candidate in enumerate(candidates):
        candidate_nom = candidate.get('nom', '')
        candidate_prenom = candidate.get('prenom', '')
        
        try:
            logger.info(f"Génération du PDF pour {candidate_nom} {candidate_prenom}...")
            
            # Affichage des données du candidat pour débogage
            logger.info(f"  - Niveau: {candidate.get('niveau', '')}")
            logger.info(f"  - Heure de préparation: {candidate.get('heure_preparation', '')}")
            logger.info(f"  - Heure de fin calculée: {candidate.get('heure_fin', '')}")
            
            # Génération du PDF
            pdf_path = pdf_generator.generate_pdf(candidate)
            
            if pdf_path:
                logger.info(f"  - PDF généré: {pdf_path}")
                success_count += 1
            else:
                logger.error(f"  - Échec de génération du PDF pour {candidate_nom}")
                error_count += 1
        except Exception as e:
            logger.error(f"  - Erreur pour {candidate_nom}: {e}")
            error_count += 1
    
    logger.info(f"Test terminé: {success_count} PDF générés avec succès, {error_count} erreurs")

if __name__ == "__main__":
    test_generation_pdf()