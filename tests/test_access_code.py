#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de test pour vérifier l'intégration du code d'accès aux locaux
"""

import os
import pandas as pd
from pdf_generator import PDFGenerator

# Créer un fichier Excel de test
test_data = {
    'nom': ['MARTIN'],
    'prenom': ['Sophie'],
    'numero_candidat': ['TEST2025001'],
    'email': ['sophie.martin@example.com'],
    'date_naissance': ['15/03/1995'],
    'niveau': ['B2'],
    'date_examen': ['25/01/2025'],
    'heure_debut': ['09:00'],
    'date_ep_coll': ['25/01/2025'],
    'debut_ep_coll': ['09:00'],
    'date_ep_ind': ['25/01/2025'],
    'heure_preparation': ['14:00']
}

# Créer le DataFrame et sauvegarder
df = pd.DataFrame(test_data)
test_excel_path = 'test_access_code_data.xlsx'
df.to_excel(test_excel_path, index=False, engine='openpyxl')

print("Fichier Excel de test créé.")

# Test 1: Générer un PDF SANS code d'accès
print("\n=== TEST 1: PDF sans code d'accès ===")
generator1 = PDFGenerator(
    excel_path=test_excel_path,
    template_path='templates/convocation_delf_template_modele.html',
    output_dir='output',
    access_code=''  # Pas de code
)

try:
    # Convertir en format dict simple (première ligne du DataFrame)
    candidate_data = df.iloc[0].to_dict()
    pdf_path1 = generator1.generate_pdf(candidate_data)
    print(f"✓ PDF généré sans code: {pdf_path1}")
except Exception as e:
    print(f"✗ Erreur: {e}")

# Test 2: Générer un PDF AVEC code d'accès
print("\n=== TEST 2: PDF avec code d'accès ===")
generator2 = PDFGenerator(
    excel_path=test_excel_path,
    template_path='templates/convocation_delf_template_modele.html',
    output_dir='output',
    access_code='1234AB'  # Code d'accès test
)

try:
    # Modifier le numéro de candidat pour distinguer les tests
    df_copy = df.copy()
    df_copy.loc[0, 'numero_candidat'] = 'TEST2025002'
    candidate_data2 = df_copy.iloc[0].to_dict()
    pdf_path2 = generator2.generate_pdf(candidate_data2)
    print(f"✓ PDF généré avec code '1234AB': {pdf_path2}")
except Exception as e:
    print(f"✗ Erreur: {e}")

# Nettoyer
if os.path.exists(test_excel_path):
    os.remove(test_excel_path)
    print("\nFichier Excel de test supprimé.")

print("\n=== TEST TERMINÉ ===")
print("Vérifiez les PDF générés dans le dossier 'output' pour voir :")
print("1. convocation_MARTIN_Sophie_TEST2025001.pdf - SANS code d'accès")
print("2. convocation_MARTIN_Sophie_TEST2025002.pdf - AVEC code d'accès '1234AB'")
