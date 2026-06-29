#!/usr/bin/env python3
"""
Test d'extraction des emails sans dépendances cryptography
"""

import pandas as pd
import logging

def is_jury_file(excel_path):
    """Vérifie si le fichier Excel est un fichier de jurys DELF/DALF"""
    try:
        xl = pd.ExcelFile(excel_path)
        sheet_names = [sheet.strip().upper() for sheet in xl.sheet_names]
        
        # Vérifier si c'est un fichier DELF/DALF (niveaux A1, A2, B1, B2, C1, C2)
        delf_levels = ['A1', 'A2', 'B1', 'B2', 'C1', 'C2']
        has_delf_levels = any(level in name for name in sheet_names for level in delf_levels)
        
        return has_delf_levels
    except Exception as e:
        print(f"Erreur lors de la vérification: {e}")
        return False

def convert_jury_file_to_candidates(excel_path):
    """Convertit un fichier de jurys en format candidats avec emails"""
    try:
        xl = pd.ExcelFile(excel_path)
        all_candidates = []
        
        for sheet_name in xl.sheet_names:
            if sheet_name.upper() == 'ADMIN':
                continue
                
            print(f"Traitement de l'onglet: {sheet_name}")
            
            try:
                # Lire l'onglet
                df = pd.read_excel(excel_path, sheet_name=sheet_name, engine='openpyxl')
                
                # Analyser les 5 premières lignes pour comprendre la structure
                print(f"  Colonnes: {list(df.columns)}")
                print(f"  Première ligne: {df.iloc[0].tolist() if len(df) > 0 else 'Vide'}")
                
                # Chercher la ligne d'en-tête (qui contient "Email")
                header_row = None
                for idx, row in df.iterrows():
                    row_values = row.tolist()
                    if any('Email' in str(cell) for cell in row_values):
                        header_row = idx
                        print(f"  En-tête trouvé à la ligne {idx}: {row_values}")
                        break
                
                if header_row is not None:
                    # Lire à partir de la ligne d'en-tête
                    df_data = pd.read_excel(excel_path, sheet_name=sheet_name, 
                                          header=header_row, engine='openpyxl')
                    
                    print(f"  Colonnes après en-tête: {list(df_data.columns)}")
                    
                    # Les emails sont dans la colonne 5 (index 5) selon la structure observée
                    # Structure: ['Prép.', 'Pass.', 'Numéro de candidat', 'NOM et Prénom', 'Date de naissance', 'Email', 'Besoins spéciaux']
                    email_col_idx = 5  # Index de la colonne Email
                    nom_prenom_idx = 3  # Index de la colonne "NOM et Prénom"
                    
                    if len(df_data.columns) > email_col_idx:
                        print(f"  Utilisation de la colonne {email_col_idx} pour les emails")
                        
                        # Traiter chaque ligne de données
                        for idx, row in df_data.iterrows():
                            row_values = row.tolist()
                            
                            # Extraire les données
                            if len(row_values) > email_col_idx:
                                email = str(row_values[email_col_idx]) if pd.notna(row_values[email_col_idx]) else ''
                                nom_prenom = str(row_values[nom_prenom_idx]) if len(row_values) > nom_prenom_idx and pd.notna(row_values[nom_prenom_idx]) else ''
                                
                                # Séparer nom et prénom si possible
                                if nom_prenom and ' ' in nom_prenom:
                                    parts = nom_prenom.split(' ', 1)
                                    nom = parts[0]
                                    prenom = parts[1] if len(parts) > 1 else ''
                                else:
                                    nom = nom_prenom
                                    prenom = ''
                                
                                # Vérifier que l'email est valide
                                if email and email.strip() and '@' in email and email.strip() != 'nan':
                                    candidate_data = {
                                        'nom': nom,
                                        'prenom': prenom,
                                        'email': email.strip(),
                                        'niveau': sheet_name,
                                        'type_examen': 'DELF'
                                    }
                                    
                                    all_candidates.append(candidate_data)
                                    print(f"    ✅ Candidat ajouté: {nom} {prenom} - {email}")
                                else:
                                    if nom_prenom:  # Seulement afficher si il y a un nom
                                        print(f"    ⚠️ Email manquant pour: {nom_prenom} (email='{email}')")
                    else:
                        print(f"  ❌ Pas assez de colonnes ({len(df_data.columns)} < {email_col_idx+1})")
                else:
                    print(f"  ❌ En-tête avec 'Email' non trouvé")
                        
            except Exception as e:
                print(f"  ❌ Erreur lors du traitement de l'onglet {sheet_name}: {e}")
        
        print(f"\n✅ Total: {len(all_candidates)} candidats avec emails valides")
        return all_candidates
        
    except Exception as e:
        print(f"❌ Erreur générale: {e}")
        return []

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    excel_file = 'juries_20250919_162205.xlsx'
    
    print(f"Test avec: {excel_file}")
    print(f"Est fichier de jurys: {is_jury_file(excel_file)}")
    
    candidates = convert_jury_file_to_candidates(excel_file)
    
    if candidates:
        print(f"\nPremiers candidats:")
        for i, candidate in enumerate(candidates[:5]):
            print(f"{i+1}. {candidate['nom']} {candidate['prenom']} - {candidate['email']} ({candidate['niveau']})")