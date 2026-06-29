import pandas as pd
import os

def analyze_excel_structure(file_path):
    """
    Analyse la structure d'un fichier Excel de jurys pour comprendre son organisation
    """
    print(f"Analyse du fichier: {file_path}")
    print("-" * 50)
    
    # Lire les noms des feuilles
    try:
        excel_file = pd.ExcelFile(file_path)
        sheet_names = excel_file.sheet_names
        print(f"Le fichier contient {len(sheet_names)} feuilles:")
        for i, sheet_name in enumerate(sheet_names):
            print(f"  {i+1}. {sheet_name}")
        
        print("\nAnalyse de chaque feuille:")
        print("-" * 50)
        
        # Pour chaque feuille, analyser sa structure
        for sheet_name in sheet_names:
            if sheet_name.startswith('Niveau'):
                print(f"\nFeuille: {sheet_name}")
                
                # Lire sans en-tête pour voir la structure brute
                df = pd.read_excel(file_path, sheet_name=sheet_name, header=None)
                
                # Afficher les dimensions
                rows, cols = df.shape
                print(f"  Dimensions: {rows} lignes × {cols} colonnes")
                
                # Vérifier les cellules spécifiques qui nous intéressent
                print("  Cellules importantes:")
                # Date épreuve collective (D1)
                if cols > 3 and not pd.isna(df.iloc[0, 3]):
                    print(f"    D1 (Date épreuve): {df.iloc[0, 3]}")
                
                # Heure début (F1)
                if cols > 5 and not pd.isna(df.iloc[0, 5]):
                    print(f"    F1 (Heure début): {df.iloc[0, 5]}")
                
                # Heure fin standard (H1)
                if cols > 7 and not pd.isna(df.iloc[0, 7]):
                    print(f"    H1 (Fin standard): {df.iloc[0, 7]}")
                
                # Heure fin besoins spéciaux (J1)
                if cols > 9 and not pd.isna(df.iloc[0, 9]):
                    print(f"    J1 (Fin besoins spéciaux): {df.iloc[0, 9]}")
                
                # Vérifier la présence de la colonne G pour les besoins spéciaux
                # Chercher dans les données des candidats
                if cols > 6:  # Vérifie si la colonne G existe
                    has_column_g = False
                    for i in range(5, min(20, rows)):  # Vérifier quelques lignes
                        if not pd.isna(df.iloc[i, 6]):  # Colonne G (index 6)
                            print(f"    Colonne G (besoins spéciaux) trouvée à la ligne {i+1}: {df.iloc[i, 6]}")
                            has_column_g = True
                            break
                    
                    if not has_column_g:
                        print("    Colonne G (besoins spéciaux): Non détectée dans les premières lignes")
                else:
                    print("    La colonne G n'existe pas dans cette feuille")
                    
                # Détection de la structure des candidats
                print("\n  Structure des candidats:")
                for i in range(5, min(15, rows)):
                    row = df.iloc[i]
                    if isinstance(row[0], str) and row[0].startswith('Jury'):
                        print(f"    Ligne {i+1}: {row[0]} - {row[1]}")
                    elif not pd.isna(row[1]) and not pd.isna(row[2]):
                        # Probablement un candidat
                        print(f"    Ligne {i+1}: Candidat - Préparation: {row[0]}, Passage: {row[1]}, Numéro: {row[2]}")
                        
                        # Afficher la ligne complète pour analyse
                        print("      Ligne complète:")
                        for j in range(min(15, cols)):
                            if not pd.isna(row[j]):
                                print(f"        Colonne {chr(65+j)}: {row[j]}")
                        break
        
        print("\nAnalyse terminée.")
    
    except Exception as e:
        print(f"Erreur lors de l'analyse du fichier: {e}")

if __name__ == "__main__":
    file_path = "JURYS.xlsx"
    if os.path.exists(file_path):
        analyze_excel_structure(file_path)
    else:
        print(f"Le fichier {file_path} n'existe pas dans le répertoire courant.")