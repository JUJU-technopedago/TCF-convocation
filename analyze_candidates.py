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

# Chercher spécifiquement SIANO Marco et analyser tous les candidats
siano_found = False
all_candidates = []

for sheet_name in xls.sheet_names:
    print(f"\n{'='*50}")
    print(f"ONGLET: {sheet_name}")
    print(f"{'='*50}")
    
    # Lire l'onglet sans en-têtes pour voir les données brutes
    df = pd.read_excel(latest_file, sheet_name=sheet_name, header=None)
    
    # Rechercher "SIANO" dans tout l'onglet
    siano_rows = df.apply(lambda row: row.astype(str).str.contains('SIANO', case=False).any(), axis=1)
    
    if siano_rows.any():
        print(f"\n*** SIANO trouvé dans l'onglet {sheet_name} ***")
        siano_indices = df[siano_rows].index.tolist()
        print(f"Trouvé aux lignes: {siano_indices}")
        
        for idx in siano_indices:
            print(f"\nDétails de la ligne {idx}:")
            row_data = df.iloc[idx].tolist()
            for col_idx, value in enumerate(row_data):
                if pd.notna(value):
                    col_letter = chr(65 + col_idx)  # Convertir l'index en lettre de colonne (A, B, C...)
                    print(f"Colonne {col_letter} (index {col_idx}): {value}")
        
        siano_found = True
    
    # Collecter les informations des candidats pour l'onglet
    # Chercher les en-têtes "NOM et Prénom" pour identifier la ligne d'en-tête
    header_rows = df.apply(lambda row: row.astype(str).str.contains('NOM et Prénom', case=False).any(), axis=1)
    
    if header_rows.any():
        header_idx = header_rows.idxmax()
        
        # Les données des candidats commencent à la ligne suivante
        candidates_df = df.iloc[header_idx+1:].copy()
        
        # Identifier les colonnes importantes
        col_mapping = {}
        for col_idx, value in enumerate(df.iloc[header_idx].tolist()):
            if pd.notna(value):
                if "Numéro de candidat" in str(value):
                    col_mapping['num_candidat'] = col_idx
                elif "NOM et Prénom" in str(value):
                    col_mapping['nom_prenom'] = col_idx
                elif "Date de naissance" in str(value):
                    col_mapping['date_naissance'] = col_idx
                elif "Email" in str(value):
                    col_mapping['email'] = col_idx
                elif "Besoins spéciaux" in str(value):
                    col_mapping['besoins_speciaux'] = col_idx
        
        # Collecter les candidats
        for idx, row in candidates_df.iterrows():
            candidate = {'niveau': sheet_name.replace('Niveau ', '')}
            
            for key, col_idx in col_mapping.items():
                if col_idx < len(row):
                    candidate[key] = row[col_idx]
            
            # Vérifier si c'est un candidat valide (a un nom et prénom)
            if 'nom_prenom' in candidate and pd.notna(candidate['nom_prenom']):
                all_candidates.append(candidate)
                
                # Vérifier si c'est SIANO Marco
                if 'SIANO' in str(candidate.get('nom_prenom', '')):
                    print(f"\n*** Candidat SIANO trouvé ***")
                    print(f"Détails: {candidate}")

# Résumé des candidats
print(f"\n{'='*50}")
print(f"RÉSUMÉ DES CANDIDATS")
print(f"{'='*50}")
print(f"Nombre total de candidats trouvés: {len(all_candidates)}")

# Compter les candidats par niveau
niveau_counts = {}
for candidate in all_candidates:
    niveau = candidate.get('niveau', 'Inconnu')
    niveau_counts[niveau] = niveau_counts.get(niveau, 0) + 1

print("\nCandidats par niveau:")
for niveau, count in niveau_counts.items():
    print(f"{niveau}: {count}")

# Compter les candidats avec besoins spéciaux
special_needs_count = sum(1 for c in all_candidates if str(c.get('besoins_speciaux', '')).upper() == 'OUI')
print(f"\nCandidats avec besoins spéciaux: {special_needs_count}")

if not siano_found:
    print("\nAucune mention de SIANO n'a été trouvée dans le fichier Excel.")