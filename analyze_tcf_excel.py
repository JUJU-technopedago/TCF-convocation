#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script d'analyse du fichier Excel TCF
"""
import pandas as pd
import os

def analyze_tcf_excel():
    file_path = 'JURYS FINAL TCF.xlsx'
    
    print(f"Analyse du fichier: {file_path}")
    print(f"Fichier existe: {os.path.exists(file_path)}")
    print("=" * 60)
    
    try:
        excel_file = pd.ExcelFile(file_path, engine='openpyxl')
        print(f"Feuilles disponibles: {excel_file.sheet_names}")
        print("=" * 60)
        
        for sheet in ['TCF CANADA', 'TCF TP COMPLET', 'TCF TP OBLIGATOIRE', 'TCF IRN']:
            try:
                df = pd.read_excel(file_path, sheet_name=sheet, engine='openpyxl')
                print(f"\n=== FEUILLE: {sheet} ===")
                print(f"Nombre de lignes: {len(df)}")
                print(f"Nombre de candidats: {len(df) if len(df) > 0 else 0}")
                
                if len(df) > 0:
                    print(f"Colonnes ({len(df.columns)}):")
                    for i, col in enumerate(df.columns, 1):
                        print(f"  {i:2d}. {col}")
                    
                    print("\nAperçu des premières lignes:")
                    print(df.head(3).to_string())
                    
                    # Vérifier s'il y a des données de dates/heures
                    date_cols = [col for col in df.columns if 'date' in col.lower()]
                    heure_cols = [col for col in df.columns if 'heure' in col.lower() or 'time' in col.lower()]
                    
                    if date_cols:
                        print(f"\nColonnes de dates trouvées: {date_cols}")
                    if heure_cols:
                        print(f"Colonnes d'heures trouvées: {heure_cols}")
                        
                else:
                    print("Aucune donnée dans cette feuille")
                    
            except Exception as e:
                print(f"Erreur lors de la lecture de la feuille {sheet}: {e}")
                
    except Exception as e:
        print(f"Erreur lors de l'ouverture du fichier: {e}")

if __name__ == "__main__":
    analyze_tcf_excel()