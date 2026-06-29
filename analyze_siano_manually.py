import pandas as pd
import os

def analyze_siano_manually():
    """Analyse le fichier Excel manuellement pour vérifier les données de SIANO Marco"""
    
    excel_path = "JURYS.xlsx"
    print(f"Analyse du fichier: {excel_path}")
    
    # Vérifier si le fichier existe
    if not os.path.exists(excel_path):
        print(f"Le fichier {excel_path} n'existe pas!")
        return
    
    # Lire l'onglet Niveau B2 (où se trouve SIANO)
    try:
        print("Lecture de l'onglet Niveau B2...")
        df = pd.read_excel(excel_path, sheet_name="Niveau B2", header=None, engine='openpyxl')
        
        # Afficher les dimensions
        print(f"Dimensions: {df.shape[0]} lignes x {df.shape[1]} colonnes")
        
        # Chercher SIANO dans toutes les cellules
        print("\nRecherche de 'SIANO' dans les données...")
        found = False
        
        for i, row in df.iterrows():
            for j, cell in enumerate(row):
                if isinstance(cell, str) and 'SIANO' in cell:
                    found = True
                    print(f"Trouvé à la ligne {i+1}, colonne {j+1} (index {i},{j})")
                    print(f"Contenu: {cell}")
                    
                    # Afficher les données de la ligne
                    print(f"Ligne complète (ligne {i+1}):")
                    for k, value in enumerate(row):
                        col_letter = chr(65 + k)  # Convertir l'indice en lettre (A, B, C...)
                        print(f"  Colonne {col_letter} (index {k}): {value}")
                    
                    # Vérifier la colonne G (index 6)
                    if len(row) > 6:
                        g_value = row[6]
                        print(f"\nValeur en colonne G: '{g_value}' (type: {type(g_value)})")
                        
                        if isinstance(g_value, str):
                            print(f"  Valeur en minuscules: '{g_value.lower()}'")
                            print(f"  Contient 'oui': {('oui' in g_value.lower())}")
        
        if not found:
            print("SIANO non trouvé dans l'onglet Niveau B2")
        
        # Lire la première ligne (informations d'en-tête)
        print("\nPremière ligne (ligne 1):")
        if len(df) > 0:
            for j, cell in enumerate(df.iloc[0]):
                col_letter = chr(65 + j)
                print(f"  Colonne {col_letter} (index {j}): {cell}")
    
    except Exception as e:
        print(f"Erreur: {e}")

if __name__ == "__main__":
    analyze_siano_manually()