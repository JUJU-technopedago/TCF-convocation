import pandas as pd

def analyze_jurys_file(file_path):
    """
    Analyse le fichier JURYS.xlsx pour vérifier sa structure
    """
    print(f"Analyse du fichier: {file_path}")
    
    try:
        # Lire tous les onglets
        excel_file = pd.ExcelFile(file_path, engine='openpyxl')
        sheet_names = excel_file.sheet_names
        
        print(f"\nOnglets trouvés ({len(sheet_names)}):")
        for sheet_name in sheet_names:
            print(f"  - {sheet_name}")
        
        # Vérifier si Marco SIANO est présent dans les données
        found_siano = False
        siano_details = []
        
        for sheet_name in sheet_names:
            # Lire la feuille sans en-tête
            df = pd.read_excel(file_path, sheet_name=sheet_name, header=None)
            
            # Rechercher SIANO
            for row_idx, row in df.iterrows():
                row_str = ' '.join([str(val) for val in row.values if pd.notna(val)])
                if 'SIANO' in row_str or 'siano' in row_str.lower():
                    found_siano = True
                    
                    # Trouver l'indice de colonne où se trouve SIANO
                    siano_col = None
                    for col_idx, val in enumerate(row.values):
                        if pd.notna(val) and ('SIANO' in str(val) or 'siano' in str(val).lower()):
                            siano_col = col_idx
                            break
                    
                    # Récupérer les données de la ligne
                    siano_info = {
                        'onglet': sheet_name,
                        'ligne': row_idx + 1,  # +1 car pandas est 0-indexé
                        'données': {f'colonne {chr(65+i)}': val for i, val in enumerate(row.values) if pd.notna(val)}
                    }
                    
                    # Vérifier spécifiquement la colonne G (index 6)
                    if len(row.values) > 6:
                        siano_info['colonne_G'] = row.values[6] if pd.notna(row.values[6]) else 'Vide'
                    
                    siano_details.append(siano_info)
        
        if found_siano:
            print("\nMarco SIANO trouvé dans le fichier:")
            for idx, info in enumerate(siano_details):
                print(f"\nOccurrence {idx+1}:")
                print(f"  - Onglet: {info['onglet']}")
                print(f"  - Ligne: {info['ligne']}")
                
                if 'colonne_G' in info:
                    print(f"  - Valeur colonne G: '{info['colonne_G']}'")
                
                print("  - Données:")
                for col, val in info['données'].items():
                    print(f"    • {col}: {val}")
        else:
            print("\nMarco SIANO n'a pas été trouvé dans le fichier.")
        
        # Vérifier les colonnes spéciales J1 et H1 dans chaque onglet
        print("\nVérification des heures de fin d'épreuve:")
        for sheet_name in sheet_names:
            df = pd.read_excel(file_path, sheet_name=sheet_name, header=None)
            
            if len(df) > 0:
                first_row = df.iloc[0]
                
                # Vérifier H1 (colonne 7, index 0-based) - Fin standard
                fin_standard = first_row[7] if len(first_row) > 7 and pd.notna(first_row[7]) else 'Non définie'
                
                # Vérifier J1 (colonne 9, index 0-based) - Fin besoins spéciaux
                fin_bs = first_row[9] if len(first_row) > 9 and pd.notna(first_row[9]) else 'Non définie'
                
                print(f"  - Onglet {sheet_name}:")
                print(f"    • Fin standard (H1): {fin_standard}")
                print(f"    • Fin besoins spéciaux (J1): {fin_bs}")
    
    except Exception as e:
        print(f"Erreur lors de l'analyse: {e}")

if __name__ == "__main__":
    analyze_jurys_file("JURYS.xlsx")