from tcf_excel_processor import TCFExcelProcessor
p = TCFExcelProcessor("Inscriptions TCF Session Decembre 2025.xlsx")
candidates = p.get_all_candidates()
for c in candidates:
    if "douanfack" in c.get("nom", "").lower() or "douanfack" in c.get("prenom", "").lower():
        print(f"Nom: '{c['nom']}', Prénom: '{c['prenom']}'")
