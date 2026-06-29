import pandas as pd

def check_special_needs_candidate(file_path, candidate_name):
    """Vérifie les informations d'un candidat à besoins spéciaux spécifique"""
    print(f"Recherche de {candidate_name} dans {file_path}")
    
    try:
        # Charger l'onglet Niveau B2
        df = pd.read_excel(file_path, sheet_name="Niveau B2", header=None)
        rows, cols = df.shape
        print(f"Dimensions de l'onglet B2: {rows} lignes × {cols} colonnes")
        
        # Chercher la ligne du candidat
        candidate_row = None
        candidate_data = {}
        
        for i in range(rows):
            row = df.iloc[i]
            name_col = 3  # Colonne D (index 3)
            
            if not pd.isna(row[name_col]) and candidate_name.lower() in str(row[name_col]).lower():
                candidate_row = i
                print(f"\nCandidat trouvé à la ligne {i+1}:")
                
                # Récupérer les infos du candidat
                for j in range(min(cols, 15)):  # Limiter à 15 colonnes pour la lisibilité
                    if not pd.isna(row[j]):
                        col_letter = chr(65 + j)  # A, B, C, etc.
                        candidate_data[col_letter] = row[j]
                        print(f"  Colonne {col_letter}: {row[j]}")
                break
        
        if candidate_row is None:
            print(f"Candidat {candidate_name} non trouvé dans l'onglet Niveau B2")
            return
        
        # Vérifier la colonne G (besoins spéciaux)
        special_needs = candidate_data.get('G', '')
        print(f"\nStatut besoins spéciaux (colonne G): '{special_needs}'")
        
        # Vérifier si "OUI" est bien détecté
        is_detected = str(special_needs).strip().lower() in ["oui", "o", "yes", "y", "1", "true", "vrai", "x"]
        print(f"Détection besoins spéciaux: {'OUI' if is_detected else 'NON'}")
        
        # Vérifier les cellules importantes pour l'heure de fin
        print("\nCellules importantes pour les heures de fin:")
        # Date épreuve collective (D1)
        if not pd.isna(df.iloc[0, 3]):
            print(f"  D1 (Date épreuve): {df.iloc[0, 3]}")
        
        # Heure début (F1)
        if not pd.isna(df.iloc[0, 5]):
            print(f"  F1 (Heure début): {df.iloc[0, 5]}")
        
        # Heure fin standard (H1)
        if not pd.isna(df.iloc[0, 7]):
            print(f"  H1 (Fin standard): {df.iloc[0, 7]}")
        
        # Heure fin besoins spéciaux (J1)
        if cols > 9 and not pd.isna(df.iloc[0, 9]):
            print(f"  J1 (Fin besoins spéciaux): {df.iloc[0, 9]}")
        else:
            print("  J1 (Fin besoins spéciaux): Non définie")
        
        print("\nDiagnostic des problèmes possibles:")
        
        if not is_detected:
            print("⚠️  La valeur dans la colonne G n'est pas reconnue comme 'OUI' pour les besoins spéciaux")
            print("    => Le script recherche: 'oui', 'o', 'yes', 'y', '1', 'true', 'vrai', 'x' (insensible à la casse)")
        
        if cols <= 9 or pd.isna(df.iloc[0, 9]):
            print("⚠️  La cellule J1 (heure de fin pour besoins spéciaux) est vide ou n'existe pas")
            print("    => Sans cette information, le script doit calculer automatiquement un tiers-temps")
        
    except Exception as e:
        print(f"Erreur lors de l'analyse: {e}")

if __name__ == "__main__":
    check_special_needs_candidate("JURYS.xlsx", "SIANO Marco")