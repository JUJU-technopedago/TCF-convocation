import openpyxl

wb = openpyxl.load_workbook('JURYS FINAL TCF.xlsx')

sheets_to_check = ['TCF TP OBLIGATOIRE', 'TCF TP EE', 'TCF TP EO']

print("🕐 Structure des premières lignes pour les onglets TCF TP:\n")

for sheet_name in sheets_to_check:
    if sheet_name in wb.sheetnames:
        sheet = wb[sheet_name]
        print(f"\n{'='*70}")
        print(f"📋 {sheet_name}")
        print(f"{'='*70}")
        
        # Afficher les 5 premières lignes avec toutes les colonnes jusqu'à F
        for row_num in range(1, 6):
            row_values = []
            for col in ['A', 'B', 'C', 'D', 'E', 'F']:
                cell_value = sheet[f'{col}{row_num}'].value
                row_values.append(f"{col}{row_num}={cell_value}")
            print(f"  Ligne {row_num}: {' | '.join(row_values)}")
