import pandas as pd
import os
from datetime import datetime

# Trouver le fichier Excel le plus récent dans le répertoire
excel_files = [f for f in os.listdir('.') if f.startswith('juries_') and f.endswith('.xlsx')]
if not excel_files:
    print("Aucun fichier Excel trouvé avec le format juries_*.xlsx")
    exit(1)

# Trier par date de modification (le plus récent en premier)
excel_files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
latest_file = excel_files[0]
print(f"Utilisation du fichier: {latest_file}")

# Charger le fichier Excel
xls = pd.ExcelFile(latest_file)
print(f"\nOnglets disponibles: {xls.sheet_names}")

# Pour chaque onglet, afficher le nombre de lignes et les en-têtes
total_candidates = 0
for sheet_name in xls.sheet_names:
    df = pd.read_excel(latest_file, sheet_name=sheet_name)
    rows = len(df)
    total_candidates += rows
    print(f"\nOnglet: {sheet_name}")
    print(f"Nombre de lignes: {rows}")
    print(f"Colonnes: {list(df.columns)}")
    
    # Vérifier les valeurs dans la colonne G (besoins spéciaux)
    if 'Unnamed: 6' in df.columns:  # Colonne G peut être nommée "Unnamed: 6"
        special_needs = df[df['Unnamed: 6'].str.upper() == 'OUI'].shape[0]
        print(f"Candidats avec besoins spéciaux (colonne G = 'OUI'): {special_needs}")
    
    # Afficher les premières lignes pour inspection
    print("\nPremières lignes:")
    print(df.head(3))

print(f"\nTotal des candidats: {total_candidates}")