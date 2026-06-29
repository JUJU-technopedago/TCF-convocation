#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Analyse détaillée du fichier Excel TCF pour comprendre la structure
"""
import pandas as pd

def analyze_tcf_detailed():
    file_path = 'JURYS FINAL TCF.xlsx'
    
    print("ANALYSE DÉTAILLÉE DU FICHIER TCF")
    print("=" * 50)
    
    # Analyser la feuille TCF CANADA en détail
    sheet_name = 'TCF CANADA'
    print(f"\nAnalyse détaillée de la feuille: {sheet_name}")
    
    # Lire sans header pour voir la structure brute
    df_raw = pd.read_excel(file_path, sheet_name=sheet_name, header=None, engine='openpyxl')
    
    print("\nPremières lignes brutes (sans interprétation):")
    print(df_raw.head(10).to_string())
    
    print(f"\nNombre total de lignes: {len(df_raw)}")
    print(f"Nombre de colonnes: {len(df_raw.columns)}")
    
    # Essayer de détecter où commencent les vraies données
    print("\nRecherche du début des données candidats...")
    for i, row in df_raw.iterrows():
        row_str = str(row.tolist())
        if any(keyword in row_str.lower() for keyword in ['nom', 'prenom', 'email', 'date']):
            print(f"Ligne {i}: {row.tolist()}")
        if i > 15:  # Limiter l'affichage
            break
    
    # Analyser aussi une feuille plus simple
    print(f"\n" + "="*50)
    print("Analyse de la feuille TCF TP OBLIGATOIRE:")
    df_obligatoire = pd.read_excel(file_path, sheet_name='TCF TP OBLIGATOIRE', header=None, engine='openpyxl')
    print(df_obligatoire.head(5).to_string())

if __name__ == "__main__":
    analyze_tcf_detailed()