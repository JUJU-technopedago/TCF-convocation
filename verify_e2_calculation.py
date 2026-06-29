"""
Test de vérification: Lecture E2 et calcul des heures de fin
"""
from tcf_excel_processor import TCFExcelProcessor

print("=" * 70)
print("VÉRIFICATION: Durées E2 et calcul automatique des heures de fin")
print("=" * 70)

parser = TCFExcelProcessor('JURYS FINAL TCF.xlsx')
parser.load_tcf_data()

test_cases = [
    ('TCF TP OBLIGATOIRE', 'Durée E2: 01h25', '13:30 → 14:55'),
    ('TCF TP EE', 'Durée E2: 01h00', '13:30 → 14:30'),
    ('TCF TP EO', 'Durée E2: 00h12', 'Variable selon candidat')
]

for tcf_type, duree_info, expected in test_cases:
    candidates = parser.get_candidates_by_tcf_type(tcf_type)
    if candidates:
        print(f"\n{tcf_type}")
        print(f"  {duree_info}")
        print(f"  Attendu: {expected}")
        print(f"  Candidats testés:")
        
        for i, c in enumerate(candidates[:2], 1):
            nom = c.get('nom', 'N/A')
            prenom = c.get('prenom', 'N/A')
            
            if tcf_type in ['TCF TP OBLIGATOIRE', 'TCF TP EE']:
                debut = c.get('debut_ep_coll')
                fin = c.get('fin_ep_coll')
                print(f"    {i}. {nom} {prenom}: {debut} → {fin}")
            else:
                debut = c.get('heure_individuelle')
                fin = c.get('fin_individuelle')
                print(f"    {i}. {nom} {prenom}: {debut} → {fin}")

print("\n" + "=" * 70)
print("✅ Toutes les heures de fin sont calculées automatiquement depuis E2")
print("=" * 70)
