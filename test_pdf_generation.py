#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script to verify PDF generation for candidates that were previously failing
"""

import sys
import os
import logging
from jury_excel_processor import JuryExcelProcessor
from pdf_generator import PDFGenerator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger()

def test_pdf_generation():
    # Specify the Excel file containing jury data
    excel_file = "juries_20250825_181821.xlsx"
    if not os.path.exists(excel_file):
        logger.error(f"Excel file not found: {excel_file}")
        return
    
    # Load candidate data
    logger.info(f"Loading candidate data from {excel_file}...")
    processor = JuryExcelProcessor(excel_file)
    try:
        processor.load_jury_data()
        candidates = processor.get_all_candidates()
        logger.info(f"Found {len(candidates)} candidates total")
    except Exception as e:
        logger.error(f"Error loading candidates: {e}")
        return
    
    # Initialize PDF generator
    template_path = os.path.join("templates", "convocation_delf_template_modele.html")
    logo_af_path = os.path.join("assets", "logoAF.svg")
    logo_delf_path = os.path.join("assets", "logoDELF.svg")
    output_dir = "output_test"
    os.makedirs(output_dir, exist_ok=True)
    
    # Create PDF generator with the excel file path
    pdf_generator = PDFGenerator(
        excel_path=excel_file,
        template_path=template_path,
        logo_af_path=logo_af_path,
        logo_delf_path=logo_delf_path,
        output_dir=output_dir
    )
    
    # Test generating PDFs for specific candidates that were failing
    test_candidates = [
        "CIUPITU", "FILINIS", "BITSIOS", "BOLANI", "FUKUNAGA",
        "INOUE", "MAKRIDIS", "MASTELLOU", "XIRADAKI",
        "ANGELOPOULOS", "CHATZI", "GARCIA", "KAMRA", "SZYNDLAUER", "TODERAS"
    ]
    
    success_count = 0
    error_count = 0
    
    for candidate in candidates:
        candidate_nom = candidate.get('nom', '')
        if candidate_nom in test_candidates:
            try:
                logger.info(f"Generating PDF for {candidate_nom} {candidate.get('prenom', '')}...")
                # Include candidate data debug
                logger.info(f"  - Preparation time: {candidate.get('heure_preparation', '')}")
                logger.info(f"  - End time: {candidate.get('heure_fin', '')}")
                
                # Generate PDF
                pdf_path = pdf_generator.generate_pdf(candidate)
                if pdf_path:
                    logger.info(f"  - PDF generated: {pdf_path}")
                    success_count += 1
                else:
                    logger.error(f"  - Failed to generate PDF for {candidate_nom}")
                    error_count += 1
            except Exception as e:
                logger.error(f"  - Error for {candidate_nom}: {e}")
                error_count += 1
    
    logger.info(f"Test completed: {success_count} PDFs generated successfully, {error_count} errors")

if __name__ == "__main__":
    test_pdf_generation()