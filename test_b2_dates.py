#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de lecture de la date en B2 pour les onglets TCF TP
"""

from tcf_excel_processor import TCFExcelProcessor

# Charger le fichier Excel
processor = TCFExcelProcessor('JURYS FINAL TCF.xlsx')

# Charger les données TCF
print("🔄 Chargement des données TCF...\n")
processor.load_tcf_data()

# Afficher les candidats avec leurs dates
print("\n📊 RÉSULTAT - Candidats avec dates d'épreuve:\n")

tcf_tp_sheets = ['TCF TP OBLIGATOIRE', 'TCF TP EE', 'TCF TP EO']
candidates = processor.get_all_candidates()

for sheet_name in tcf_tp_sheets:
    sheet_candidates = [c for c in candidates if c.get('tcf_type') == sheet_name]
    if sheet_candidates:
        print(f"\n{'='*60}")
        print(f"📋 {sheet_name} ({len(sheet_candidates)} candidats)")
        print(f"{'='*60}")
        
        for i, candidate in enumerate(sheet_candidates, 1):
            nom = candidate.get('nom', 'INCONNU')
            prenom = candidate.get('prenom', '')
            date_coll = candidate.get('date_ep_coll')
            date_ind = candidate.get('date_ep_ind')
            
            print(f"\n  {i}. {prenom} {nom}")
            print(f"     📅 Date épreuve collective: {date_coll}")
            print(f"     📅 Date épreuve individuelle: {date_ind}")
            print(f"     🕐 Heure collective: {candidate.get('debut_ep_coll', 'N/A')}")
            print(f"     🕐 Heure individuelle: {candidate.get('heure_preparation', 'N/A')}")

print("\n" + "="*60)
print(f"✅ Total candidats TCF TP: {len([c for c in candidates if c.get('tcf_type') in tcf_tp_sheets])}")
