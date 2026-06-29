#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test simple de la fusion"""
import sys
import io

# Force UTF-8 encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from tcf_excel_processor import TCFExcelProcessor
import logging

# Désactiver les logs debug
logging.basicConfig(level=logging.ERROR)

processor = TCFExcelProcessor('JURYS FINAL TCF.xlsx')
success = processor.load_tcf_data()

if success:
    multi = [c for c in processor.candidates if c.get('is_multi_exam')]
    print(f'\nTotal candidats: {len(processor.candidates)}')
    print(f'Multi-epreuves: {len(multi)}')
    
    for c in multi:
        print(f'\n{c["nom"]} {c["prenom"]}:')
        print(f'  Types: {c["tcf_type"]}')
        for exam in c.get('exams', []):
            print(f'    - {exam["tcf_type"]}: date={exam.get("exam_date")}, temps={exam.get("main_time")}')
else:
    print('ERREUR chargement')
