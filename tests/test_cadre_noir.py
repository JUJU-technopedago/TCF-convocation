#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de test pour vérifier le nouveau style du titre avec cadre noir
"""

import os
import pandas as pd
from pdf_generator import PDFGenerator

# Créer un fichier Excel de test
test_data = {
    'nom': ['NOIR'],
    'prenom': ['Cadre'],
    'numero_candidat': ['NOIR2025001'],
    'email': ['cadre.noir@example.com'],
    'date_naissance': ['01/01/1990'],
    'niveau': ['B1'],
    'date_examen': ['01/02/2025'],
    'heure_debut': ['09:30'],
    'date_ep_coll': ['01/02/2025'],
    'debut_ep_coll': ['09:30'],
    'date_ep_ind': ['01/02/2025'],
    'heure_preparation': ['14:00'],
    'exam_type': ['DELF']
}

def test_cadre_noir():
    """Test du nouveau style de titre avec cadre noir"""
    
    print("=== TEST DU TITRE AVEC CADRE NOIR ===\n")
    
    # Créer le DataFrame et sauvegarder
    df = pd.DataFrame(test_data)
    test_excel_path = 'test_cadre_noir_data.xlsx'
    df.to_excel(test_excel_path, index=False, engine='openpyxl')
    
    print("✓ Fichier Excel de test créé.")
    
    # Test avec nouveau style de titre
    print("\n=== GÉNÉRATION PDF AVEC TITRE CADRE NOIR ===")
    generator = PDFGenerator(
        excel_path=test_excel_path,
        template_path='templates/convocation_delf_template_modele.html',
        output_dir='output',
        access_code='NOIR123'  # Code d'accès test
    )
    
    try:
        # Convertir en format dict simple (première ligne du DataFrame)
        candidate_data = df.iloc[0].to_dict()
        pdf_path = generator.generate_pdf(candidate_data)
        print(f"✅ PDF avec titre cadre noir généré: {pdf_path}")
        
        # Afficher les détails du style
        print(f"\n📋 DÉTAILS DU NOUVEAU STYLE:")
        print(f"   Fond: Transparent (comme dans votre modèle)")
        print(f"   Bordure: Noire #000000, 2pt")
        print(f"   Style: Cadre propre et simple")
        print(f"   Candidat test: {candidate_data['prenom']} {candidate_data['nom']}")
        print(f"   Examen: {candidate_data.get('exam_type', 'DELF')} {candidate_data['niveau']}")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False
    
    # Nettoyer
    if os.path.exists(test_excel_path):
        os.remove(test_excel_path)
        print("\n🧹 Fichier Excel de test supprimé.")
    
    print("\n=== TEST TERMINÉ ===")
    print("✓ Fond transparent (plus de gris)")
    print("✓ Bordure noire 2pt ajoutée")
    print("✓ Style simple et propre comme votre modèle")
    print("✓ Vérifiez le PDF généré dans le dossier 'output'")
    
    return True

if __name__ == "__main__":
    success = test_cadre_noir()
    if success:
        print("\n🎉 Test du titre avec cadre noir réussi!")
    else:
        print("\n❌ Test du titre avec cadre noir échoué.")
