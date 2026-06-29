import pandas as pd

excel_file = "JURYS FINAL TCF 11-18.xlsx"
df = pd.read_excel(excel_file, sheet_name=1, engine='openpyxl', header=None)

print("Testing email extraction for first 10 rows:")
print()

for idx in range(2, 12):  # Start from row 2 (skip headers)
    row_values = df.iloc[idx].values
    
    nom = str(row_values[1]).strip() if len(row_values) > 1 else ""
    prenom = str(row_values[2]).strip() if len(row_values) > 2 else ""
    
    # Method currently in code
    email = ""
    if len(row_values) > 4 and row_values[4] is not None:
        email_val = str(row_values[4]).strip()
        if email_val and email_val.lower() != 'nan':
            email = email_val
    
    # Direct access
    email_direct = row_values[4] if len(row_values) > 4 else None
    
    print(f"Row {idx}: {prenom} {nom}")
    print(f"  Email column value: {repr(email_direct)}")
    print(f"  Type: {type(email_direct)}")
    print(f"  Extracted email: '{email}'")
    print()
