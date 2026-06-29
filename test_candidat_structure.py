#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test pour voir la structure d'un candidat"""

from tcf_excel_processor import TCFExcelProcessor

processor = TCFExcelProcessor('JURYS FINAL TCF.xlsx')
processor.load_tcf_data()

# Trouver CAMACHO avant fusion (dans les candidats bruts)
print("=== STRUCTURE D'UN CANDIDAT ===")
if len(processor.candidates) > 0:
    candidat = processor.candidates[0]
    print(f"Candidat: {candidat.get('nom')} {candidat.get('prenom')}")
    print(f"\nTous les champs:")
    for key, value in sorted(candidat.items()):
        print(f"  {key}: {value}")
