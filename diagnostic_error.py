#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de diagnostic pour trouver la source de l'erreur de type
"""

import os
import sys
import traceback
from pdf_generator import PDFGenerator

def trace_error():
    """
    Fonction pour tracer la source exacte de l'erreur de type
    """
    # Chemin absolu vers le template HTML
    template_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                               "templates", "convocation_delf_template_modele.html")
    
    excel_path = "juries_20250820_192410.xlsx"
    output_dir = "output_debug"
    
    print(f"=== DIAGNOSTIC D'ERREUR ===")
    print(f"Fichier Excel: {excel_path}")
    print(f"Template HTML: {template_path}")
    print(f"Répertoire de sortie: {output_dir}")
    print(f"============================")
    
    # Créer le répertoire de sortie
    os.makedirs(output_dir, exist_ok=True)
    
    # Activer le mode débug pour Python
    import sys
    sys.tracebacklimit = 1000
    
    # Créer le générateur
    generator = PDFGenerator(
        excel_path=excel_path,
        template_path=template_path,
        logo_af_path="assets/logoAF.png",
        logo_delf_path="assets/logoDELF.png",
        output_dir=output_dir
    )
    
    try:
        # Récupérer le premier candidat
        candidates = generator.get_candidate_list()
        if not candidates:
            print("Aucun candidat trouvé dans le fichier Excel")
            return
            
        candidate = candidates[0]
        print(f"\nTest avec candidat: {candidate.get('nom', '')} {candidate.get('prenom', '')}")
        
        # Préparer les données pour le template
        template_data = generator._prepare_template_data(candidate)
        
        # Afficher les données du candidat avec leur type
        print("\nDonnées du candidat (avec types):")
        for key, value in template_data.items():
            print(f"  {key}: {value} ({type(value).__name__})")
        
        # Générer le HTML
        print("\nGénération du HTML...")
        html_content = generator.template.render(**template_data)
        
        # Vérifier que le HTML est valide
        print(f"HTML généré: {len(html_content)} caractères")
        
        # Essayer de générer le PDF
        print("\nGénération du PDF...")
        
        # Créer un chemin absolu pour les ressources du template
        base_path = os.path.dirname(os.path.abspath(generator.template_path))
        
        # Chemin du fichier de sortie
        output_path = os.path.join(output_dir, f"debug_{candidate.get('nom', '')}.pdf")
        
        # Ouvrir le fichier en mode binaire
        with open(output_path, "w+b") as result_file:
            # Activer le mode débug pour xhtml2pdf
            import logging
            pisa_logger = logging.getLogger("xhtml2pdf")
            pisa_logger.setLevel(logging.DEBUG)
            
            # Configurer un handler de console
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.DEBUG)
            pisa_logger.addHandler(console_handler)
            
            # Essayer de générer le PDF
            from xhtml2pdf import pisa
            pisa_status = pisa.CreatePDF(
                src=html_content,         # Contenu HTML source
                dest=result_file,         # Fichier de destination
                encoding='utf-8',         # Encodage UTF-8
                path=base_path,           # Chemin pour les ressources
                debug=1                   # Activer le mode débug
            )
            
        # Vérifier le statut
        if pisa_status.err:
            print(f"\nERREUR: {pisa_status.err}")
        else:
            print(f"\nSUCCÈS: PDF généré à {output_path}")
            
    except Exception as e:
        print(f"\nERREUR: {str(e)}")
        print("\nTraceback complet:")
        traceback.print_exc()

if __name__ == "__main__":
    trace_error()