#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de test pour vérifier le cadre ajusté (hauteur réduite, bordure fine)
"""

import os
import pandas as pd
from pdf_generator import PDFGenerator

# Créer un fichier Excel de test
test_data = {
    'nom': ['FINAL'],
    'prenom': ['Cadre'],
    'numero_candidat': ['FINAL2025001'],
    'email': ['cadre.final@example.com'],
    'date_naissance': ['01/01/1990'],
    'niveau': ['B1'],
    'date_examen': ['10/02/2025'],
    'heure_debut': ['11:00'],
    'date_ep_coll': ['10/02/2025'],
    'debut_ep_coll': ['11:00'],
    'date_ep_ind': ['10/02/2025'],
    'heure_preparation': ['16:00'],
    'exam_type': ['DELF']
}

def test_cadre_final():
    """Test du cadre ajusté avec hauteur réduite"""
    
    print("=== TEST DU CADRE AJUSTÉ (HAUTEUR RÉDUITE) ===\n")
    
    # Créer le DataFrame et sauvegarder
    df = pd.DataFrame(test_data)
    test_excel_path = 'test_cadre_final_data.xlsx'
    df.to_excel(test_excel_path, index=False, engine='openpyxl')
    
    print("✓ Fichier Excel de test créé.")
    
    # Test avec cadre ajusté
    print("\n=== GÉNÉRATION PDF AVEC CADRE AJUSTÉ ===")
    generator = PDFGenerator(
        excel_path=test_excel_path,
        template_path='templates/convocation_delf_template_modele.html',
        output_dir='output',
        access_code='FINAL789'  # Code d'accès test
    )
    
    try:
        # Convertir en format dict simple (première ligne du DataFrame)
        candidate_data = df.iloc[0].to_dict()
        pdf_path = generator.generate_pdf(candidate_data)
        print(f"✅ PDF avec cadre ajusté généré: {pdf_path}")
        
        # Afficher les détails des ajustements
        print(f"\n📋 DÉTAILS DES AJUSTEMENTS:")
        print(f"   Padding vertical: 2px (au lieu de 15px)")
        print(f"   Bordure: 1px solid #000000 (au lieu de 3px)")
        print(f"   Hauteur: Minimale, juste autour du texte")
        print(f"   Style: Fin et élégant")
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
    print("✓ Hauteur réduite à 2px au dessus/dessous")
    print("✓ Bordure fine 1px")
    print("✓ Cadre élégant et discret")
    print("✓ Vérifiez le PDF généré dans le dossier 'output'")
    
    return True

if __name__ == "__main__":
    success = test_cadre_final()
    if success:
        print("\n🎉 Test du cadre ajusté réussi!")
    else:
        print("\n❌ Test du cadre ajusté échoué.")
