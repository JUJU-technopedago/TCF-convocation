#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de génération des convocations pour TCF TP OBLIGATOIRE, EE et EO
"""

from tcf_excel_processor import TCFExcelProcessor
from pdf_generator import PDFGenerator
import os

# Configuration
excel_path = 'JURYS FINAL TCF.xlsx'
template_path = 'templates/convocation_tcf_template_modele.html'
output_dir = 'output'
logo_af_path = 'logos/logo_af.png'
logo_tcf_path = 'logos/logo_tcf.png'

# Créer le dossier output
os.makedirs(output_dir, exist_ok=True)

# Charger les candidats
print("Chargement des candidats TCF TP...\n")
processor = TCFExcelProcessor(excel_path)
processor.load_tcf_data()

# Filtrer uniquement les 3 onglets TCF TP
tcf_tp_types = ['TCF TP OBLIGATOIRE', 'TCF TP EE', 'TCF TP EO']
all_candidates = processor.get_all_candidates()
candidates = [c for c in all_candidates if c.get('tcf_type') in tcf_tp_types]

print(f"{len(candidates)} candidats trouves pour generation:\n")
for tcf_type in tcf_tp_types:
    count = len([c for c in candidates if c.get('tcf_type') == tcf_type])
    print(f"  - {tcf_type}: {count} candidat(s)")

# Créer le générateur PDF
generator = PDFGenerator(
    excel_path=excel_path,
    template_path=template_path,
    logo_af_path=logo_af_path,
    logo_delf_path=logo_tcf_path,
    output_dir=output_dir,
    access_code='',
    qrcode_path='',
    image_a1_path='',
    image_a2_path='',
    image_b1_path='',
    image_b2_path='',
    image_c1_path='',
    image_c2_path=''
)

# Générer les PDFs
print(f"\nGeneration des {len(candidates)} convocations...\n")
success_count = 0
errors = []

for i, candidate in enumerate(candidates, 1):
    try:
        nom = candidate.get('nom', 'INCONNU')
        prenom = candidate.get('prenom', '')
        tcf_type = candidate.get('tcf_type', '')
        
        # Nom du fichier
        filename = f"convocation_{nom}_{prenom}_{tcf_type.replace(' ', '_')}.pdf"
        
        print(f"[{i}/{len(candidates)}] Generation: {prenom} {nom} ({tcf_type})")
        
        # Ajouter les données formatées
        if 'date_ep_coll' in candidate and candidate['date_ep_coll']:
            candidate['date_collective_format'] = candidate['date_ep_coll'].strftime("%d/%m/%Y")
        else:
            candidate['date_collective_format'] = ""
            
        if 'date_ep_ind' in candidate and candidate['date_ep_ind']:
            candidate['date_individual_format'] = candidate['date_ep_ind'].strftime("%d/%m/%Y")
        else:
            candidate['date_individual_format'] = ""
        
        candidate['heure_collective'] = candidate.get('debut_ep_coll', '')
        candidate['heure_individual'] = candidate.get('heure_preparation', '')
        candidate['salle'] = '1'
        candidate['has_individual_exam'] = tcf_type == 'TCF TP EO'
        
        # Générer le PDF
        pdf_path = generator.generate_pdf(candidate, filename)
        
        if pdf_path and os.path.exists(pdf_path):
            print(f"  [OK] PDF genere: {filename}")
            success_count += 1
        else:
            print(f"  [ERREUR] Echec generation")
            errors.append(f"{prenom} {nom} ({tcf_type})")
            
    except Exception as e:
        print(f"  [ERREUR] {e}")
        errors.append(f"{candidate.get('prenom', '')} {candidate.get('nom', 'INCONNU')} - {e}")

# Rapport final
print(f"\n{'='*60}")
print(f"RAPPORT DE GENERATION")
print(f"{'='*60}")
print(f"Reussis: {success_count}/{len(candidates)}")
print(f"Echecs: {len(errors)}/{len(candidates)}")

if errors:
    print(f"\nDetails des echecs:")
    for error in errors:
        print(f"  - {error}")

print(f"\nPDFs disponibles dans: {output_dir}/")
