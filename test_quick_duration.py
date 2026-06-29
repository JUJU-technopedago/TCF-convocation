from tcf_excel_processor import TCFExcelProcessor

p = TCFExcelProcessor('JURYS FINAL TCF.xlsx')
p.load_tcf_data()

# Test TCF TP OBLIGATOIRE
obligatoire = p.get_candidates_by_tcf_type('TCF TP OBLIGATOIRE')
if obligatoire:
    c = obligatoire[0]
    print(f"\nTCF TP OBLIGATOIRE - {c['nom']} {c['prenom']}:")
    print(f"  Debut: {c.get('debut_ep_coll')}")
    print(f"  Fin: {c.get('fin_ep_coll')}")

# Test TCF TP EE
ee = p.get_candidates_by_tcf_type('TCF TP EE')
if ee:
    c = ee[0]
    print(f"\nTCF TP EE - {c['nom']} {c['prenom']}:")
    print(f"  Debut: {c.get('debut_ep_coll')}")
    print(f"  Fin: {c.get('fin_ep_coll')}")

# Test TCF TP EO
eo = p.get_candidates_by_tcf_type('TCF TP EO')
if eo:
    c = eo[0]
    print(f"\nTCF TP EO - {c['nom']} {c['prenom']}:")
    print(f"  Debut: {c.get('heure_individuelle')}")
    print(f"  Fin: {c.get('fin_individuelle')}")
