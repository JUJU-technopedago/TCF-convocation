import openpyxl

# Charger le fichier Excel
wb = openpyxl.load_workbook('JURYS FINAL TCF.xlsx')

# Vérifier les dates en B2 pour les 3 onglets TCF TP
sheets_to_check = ['TCF TP OBLIGATOIRE', 'TCF TP EE', 'TCF TP EO']

print("📅 Dates en cellule B2 des onglets TCF TP:\n")
for sheet_name in sheets_to_check:
    if sheet_name in wb.sheetnames:
        sheet = wb[sheet_name]
        b2_value = sheet['B2'].value
        print(f"  • {sheet_name}: B2 = {b2_value} (type: {type(b2_value).__name__})")
    else:
        print(f"  ⚠️ Onglet '{sheet_name}' non trouvé")
