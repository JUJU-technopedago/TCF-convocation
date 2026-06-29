from tcf_excel_processor import TCFExcelProcessor

p = TCFExcelProcessor('JURYS FINAL TCF.xlsx')
p.load_tcf_data()

# Test TCF TP EE
ee = p.get_candidates_by_tcf_type('TCF TP EE')
if ee:
    print("TCF TP EE:")
    for c in ee:
        print(f"  {c['nom']} {c['prenom']}:")
        print(f"    Durée collective: {c.get('duree_collective')}")
        print(f"    Début: {c.get('debut_ep_coll')}")
        print(f"    Fin: {c.get('fin_ep_coll')}")

# Test TCF TP EO
eo = p.get_candidates_by_tcf_type('TCF TP EO')
if eo:
    print("\nTCF TP EO:")
    for c in eo:
        print(f"  {c['nom']} {c['prenom']}:")
        print(f"    Durée individuelle: {c.get('duree_individuelle')}")
        print(f"    Début: {c.get('heure_individuelle')}")
        print(f"    Fin: {c.get('fin_individuelle')}")
