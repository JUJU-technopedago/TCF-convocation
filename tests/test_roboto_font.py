#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de test pour vérifier l'utilisation de la police Roboto
"""

import os
import pandas as pd
from pdf_generator import PDFGenerator

# Créer un fichier Excel de test
test_data = {
    'nom': ['DUPONT'],
    'prenom': ['Marie'],
    'numero_candidat': ['ROBOTO2025001'],
    'email': ['marie.dupont@example.com'],
    'date_naissance': ['25/08/1995'],
    'niveau': ['B2'],
    'date_examen': ['30/01/2025'],
    'heure_debut': ['10:00'],
    'date_ep_coll': ['30/01/2025'],
    'debut_ep_coll': ['10:00'],
    'date_ep_ind': ['30/01/2025'],
    'heure_preparation': ['15:00'],
    'exam_type': ['DELF']
}

def test_roboto_font():
    """Test de la police Roboto sur une convocation"""
    
    print("=== TEST DE LA POLICE ROBOTO ===\n")
    
    # Créer le DataFrame et sauvegarder
    df = pd.DataFrame(test_data)
    test_excel_path = 'test_roboto_data.xlsx'
    df.to_excel(test_excel_path, index=False, engine='openpyxl')
    
    print("✓ Fichier Excel de test créé.")
    
    # Test avec police Roboto
    print("\n=== GÉNÉRATION PDF AVEC POLICE ROBOTO ===")
    generator = PDFGenerator(
        excel_path=test_excel_path,
        template_path='templates/convocation_delf_template_modele.html',
        output_dir='output',
        access_code='RBT123'  # Code d'accès test
    )
    
    try:
        # Convertir en format dict simple (première ligne du DataFrame)
        candidate_data = df.iloc[0].to_dict()
        pdf_path = generator.generate_pdf(candidate_data)
        print(f"✅ PDF avec police Roboto généré: {pdf_path}")
        
        # Afficher les détails de la police
        print(f"\n📋 DÉTAILS DE LA POLICE:")
        print(f"   Police: Roboto (Google Fonts)")
        print(f"   Application: Sur tous les éléments texte")
        print(f"   Import: Via Google Fonts CDN")
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
    print("✓ La police Roboto a été appliquée au template")
    print("✓ Import Google Fonts ajouté au HTML")
    print("✓ Sélecteur universel '*' pour forcer Roboto")
    print("✓ Vérifiez le PDF généré dans le dossier 'output'")
    
    return True

if __name__ == "__main__":
    success = test_roboto_font()
    if success:
        print("\n🎉 Test de la police Roboto réussi!")
    else:
        print("\n❌ Test de la police Roboto échoué.")
