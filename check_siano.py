import pandas as pd

# Charger l'onglet Niveau B2
df = pd.read_excel("JURYS.xlsx", sheet_name="Niveau B2", header=None)
print(f"Dimensions de l'onglet B2: {df.shape[0]} lignes × {df.shape[1]} colonnes")

# Afficher les cellules importantes
print("\nCellules importantes:")
print(f"D1 (Date épreuve): {df.iloc[0, 3]}")
print(f"F1 (Heure début): {df.iloc[0, 5]}")
print(f"H1 (Fin standard): {df.iloc[0, 7]}")
if df.shape[1] > 9:
    print(f"J1 (Fin besoins spéciaux): {df.iloc[0, 9]}")

# Chercher SIANO Marco
print("\nRecherche de SIANO Marco:")
for i in range(df.shape[0]):
    row = df.iloc[i]
    if not pd.isna(row[3]) and "SIANO" in str(row[3]):
        print(f"Trouvé à la ligne {i+1}:")
        print(f"A (heure préparation): {row[0]}")
        print(f"B (heure passage): {row[1]}")
        print(f"C (numéro): {row[2]}")
        print(f"D (nom): {row[3]}")
        print(f"E (date naissance): {row[4]}")
        print(f"F (email): {row[5]}")
        print(f"G (besoins spéciaux): {row[6]}")
        break