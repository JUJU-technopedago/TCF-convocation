#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test PDF pour CAMACHO TCF TP EO uniquement
"""

from tcf_excel_processor import TCFExcelProcessor
from pdf_generator import PDFGenerator
import os

# Charger les données
processor = TCFExcelProcessor('JURYS FINAL TCF.xlsx')
processor.load_tcf_data()

# Trouver CAMACHO TCF TP EO
camacho_eo = None
for c in processor.candidates:
    if 'CAMACHO' in c['nom'] and c['tcf_type'] == 'TCF TP EO':
        camacho_eo = c
        break

if camacho_eo:
    print(f"✅ Candidat trouvé: {camacho_eo['prenom']} {camacho_eo['nom']}")
    print(f"   Type: {camacho_eo['tcf_type']}")
    print(f"   Date examen: {camacho_eo.get('date_examen')}")
    print(f"   Heure individuelle: {camacho_eo.get('heure_individuelle')}")
    print(f"   Durée individuelle: {camacho_eo.get('duree_individuelle')}")
    print(f"   Heure collective: {camacho_eo.get('debut_ep_coll')}")
    print(f"   Date collective: {camacho_eo.get('date_ep_coll')}")
    
    # Générer le PDF
    generator = PDFGenerator(
        template_path='templates/convocation_tcf_template_modele.html',
        output_dir='output'
    )
    
    pdf_path = generator.generate_pdf(camacho_eo, output_filename='test_camacho_eo_only.pdf')
    print(f"\n✅ PDF généré: {pdf_path}")
else:
    print("❌ CAMACHO TCF TP EO non trouvé")
