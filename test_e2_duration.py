"""
Test de lecture de la durée E2 et calcul des heures de fin
"""
import sys
from tcf_excel_processor import TCFExcelProcessor

print("=" * 70)
print("TEST: Lecture durée E2 et calcul heures de fin")
print("=" * 70)

# Créer le parser
parser = TCFExcelProcessor('JURYS FINAL TCF.xlsx')

# Charger les candidats
parser.load_tcf_data()

# Afficher les candidats TCF TP avec leurs heures
tcf_tp_types = ['TCF TP OBLIGATOIRE', 'TCF TP EE', 'TCF TP EO']

for tcf_type in tcf_tp_types:
    candidates = parser.get_candidates_by_tcf_type(tcf_type)
    if candidates:
        print(f"\n{'=' * 70}")
        print(f"{tcf_type}: {len(candidates)} candidats")
        print(f"{'=' * 70}")
        
        for candidate in candidates[:3]:  # Afficher les 3 premiers
            nom = candidate.get('nom', 'N/A')
            prenom = candidate.get('prenom', 'N/A')
            
            print(f"\n{nom} {prenom}:")
            print(f"  DEBUG - Toutes les clés: {list(candidate.keys())}")
            
            if tcf_type in ['TCF TP OBLIGATOIRE', 'TCF TP EE']:
                # Épreuves collectives
                debut = candidate.get('debut_ep_coll')
                fin = candidate.get('fin_ep_coll')
                print(f"  Épreuve collective: {debut} → {fin}")
            else:
                # TCF TP EO: épreuve individuelle
                debut = candidate.get('heure_individuelle')
                fin = candidate.get('fin_individuelle')
                print(f"  Épreuve individuelle: {debut} → {fin}")

print("\n" + "=" * 70)
print("Test terminé")
print("=" * 70)
