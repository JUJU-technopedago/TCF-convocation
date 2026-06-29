#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test rapide multi-épreuves avec heures formatées"""
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from tcf_excel_processor import TCFExcelProcessor

processor = TCFExcelProcessor('JURYS FINAL TCF.xlsx')
processor.load_tcf_data()

multi = [c for c in processor.candidates if c.get('is_multi_exam')]
print(f'\nCandidats multi-epreuves: {len(multi)}\n')

for c in multi:
    print(f'{c["nom"]} {c["prenom"]}:')
    for i, exam in enumerate(c.get('exams', []), 1):
        time_str = exam.get('time_collective') or exam.get('time_individual')
        print(f'  {i}. {exam["tcf_type"]}: {time_str}')
    print()
