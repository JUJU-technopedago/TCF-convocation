import pandas as pd
import unicodedata

def analyze_cell_content():
    """Analyse en détail le contenu de la cellule G pour SIANO Marco"""
    try:
        # Charger l'onglet B2
        df = pd.read_excel("JURYS.xlsx", sheet_name="Niveau B2", header=None)
        
        # Chercher SIANO Marco
        siano_row = None
        for i in range(df.shape[0]):
            if not pd.isna(df.iloc[i, 3]) and "SIANO" in str(df.iloc[i, 3]):
                siano_row = i
                break
        
        if siano_row is None:
            print("SIANO Marco non trouvé")
            return
            
        # Extraire et analyser la valeur de la cellule G
        cell_value = df.iloc[siano_row, 6]
        print(f"Valeur brute: '{cell_value}'")
        
        # Analyser chaque caractère
        if isinstance(cell_value, str):
            print("\nAnalyse caractère par caractère:")
            for i, char in enumerate(cell_value):
                code_point = ord(char)
                name = unicodedata.name(char, "Inconnu")
                category = unicodedata.category(char)
                print(f"  Position {i}: '{char}' (U+{code_point:04X}, {name}, {category})")
            
            # Convertir en minuscules pour tester
            lowered = cell_value.lower()
            print(f"\nEn minuscules: '{lowered}'")
            print(f"'oui' in lowered: {('oui' in lowered)}")
            
            # Nettoyage et comparaison
            cleaned = "".join(c for c in lowered if c.isalpha())
            print(f"Après nettoyage: '{cleaned}'")
            print(f"cleaned == 'oui': {cleaned == 'oui'}")
        else:
            print(f"Type de valeur non textuel: {type(cell_value)}")
            
        # Vérifier si la condition serait vraie avec notre test actuel
        if isinstance(cell_value, str):
            test_value = str(cell_value).strip().lower()
            valid_values = ["oui", "o", "yes", "y", "1", "true", "vrai", "x"]
            would_detect = False
            
            for valid_value in valid_values:
                if valid_value in test_value:
                    would_detect = True
                    matching_value = valid_value
                    break
            
            print(f"\nDétection avec l'algorithme actuel: {would_detect}")
            if would_detect:
                print(f"Valeur correspondante: '{matching_value}'")
            
    except Exception as e:
        print(f"Erreur: {e}")

# Exécuter l'analyse
analyze_cell_content()