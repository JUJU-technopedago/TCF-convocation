#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test final pour CAMACHO GONZALEZ Amys - Vérification durées ADMIN et ordre chronologique
"""

from tcf_excel_processor import TCFExcelProcessor

# Charger les données
processor = TCFExcelProcessor('JURYS FINAL TCF.xlsx')
processor.load_tcf_data()

# Trouver tous les candidats CAMACHO
camacho_candidates = [c for c in processor.candidates if 'CAMACHO' in c['nom']]

print(f"\n✅ Trouvé {len(camacho_candidates)} entrées pour CAMACHO GONZALEZ Amys\n")

for i, candidate in enumerate(camacho_candidates, 1):
    print(f"{'='*60}")
    print(f"Entrée {i}: {candidate['tcf_type']}")
    print(f"{'='*60}")
    print(f"  📅 Date: {candidate['date_examen']}")
    
    if candidate['tcf_type'] == 'TCF TP EE':
        print(f"  🏛️  ÉPREUVE COLLECTIVE (TCF TP EE)")
        print(f"     - Heure début: {candidate.get('debut_ep_coll')}")
        print(f"     - Heure fin: {candidate.get('fin_ep_coll')}")
        print(f"     - Durée: {candidate.get('duree_collective')}")
        print(f"     - Salle: {candidate.get('salle_collective')}")
    
    elif candidate['tcf_type'] == 'TCF TP EO':
        print(f"  🎤 ÉPREUVE INDIVIDUELLE (TCF TP EO)")
        print(f"     - Heure passage: {candidate.get('heure_individuelle')}")
        print(f"     - Heure fin: {candidate.get('fin_individuelle')}")
        print(f"     - Durée: {candidate.get('duree_individuelle')}")
        print(f"     - Salle: {candidate.get('salle_individuelle')}")
    
    print()

# Vérifier l'ordre chronologique pour la convocation
print("\n" + "="*60)
print("ORDRE CHRONOLOGIQUE POUR LA CONVOCATION")
print("="*60)

# Trier par heure de passage (EO) ou heure collective (EE)
sorted_candidates = sorted(camacho_candidates, key=lambda c: 
    c.get('heure_individuelle') if c['tcf_type'] == 'TCF TP EO' 
    else c.get('debut_ep_coll'))

for i, candidate in enumerate(sorted_candidates, 1):
    tcf_type = candidate['tcf_type']
    if tcf_type == 'TCF TP EO':
        heure = candidate.get('heure_individuelle')
        titre = "Épreuve Orale (EO)"
    else:
        heure = candidate.get('debut_ep_coll')
        titre = "Épreuve Écrite (EE)"
    
    print(f"{i}. {titre} - {heure}")

print("\n✅ L'ordre est correct si EO (13:00) apparaît AVANT EE (13:30)")
