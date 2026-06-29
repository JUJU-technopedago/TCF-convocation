#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test de la fusion des candidats multi-épreuves"""

from tcf_excel_processor import TCFExcelProcessor

processor = TCFExcelProcessor('JURYS FINAL TCF.xlsx')
processor.load_tcf_data()

print('\n=== CANDIDATS MULTI-ÉPREUVES ===')
multi = [c for c in processor.candidates if c.get('is_multi_exam')]
print(f'Nombre de candidats multi-épreuves: {len(multi)}')

for i, c in enumerate(multi):
    print(f'\n{i+1}. {c["nom"]} {c["prenom"]}')
    print(f'   Type TCF: {c["tcf_type"]}')
    print(f'   Épreuves:')
    for exam in c.get('exams', []):
        print(f'      - {exam["tcf_type"]} le {exam.get("exam_date")} à {exam.get("time_collective") or exam.get("time_individual")}')

print(f'\n=== RÉSUMÉ ===')
print(f'Total candidats: {len(processor.candidates)}')
print(f'Multi-épreuves: {len(multi)}')
print(f'Mono-épreuve: {len(processor.candidates) - len(multi)}')
