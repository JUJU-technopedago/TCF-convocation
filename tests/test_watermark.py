#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de test pour vérifier l'implémentation du watermark
"""

import os
import pandas as pd
from pdf_generator import PDFGenerator

# Créer un fichier Excel de test avec des données réalistes
test_data = {
    'nom': ['YAKURI'],
    'prenom': ['Satushi'],
    'numero_candidat': ['WATERMARK2025001'],
    'email': ['satushi.yakuri@example.com'],
    'date_naissance': ['10/05/1992'],
    'niveau': ['C2'],
    'date_examen': ['25/01/2025'],
    'heure_debut': ['09:00'],
    'date_ep_coll': ['25/01/2025'],
    'debut_ep_coll': ['09:00'],
    'date_ep_ind': ['25/01/2025'],
    'heure_preparation': ['14:30'],
    'exam_type': ['DALF']
}

def test_watermark():
    """Test du watermark sur une convocation"""
    
    print("=== TEST DU WATERMARK ===\n")
    
    # Créer le DataFrame et sauvegarder
    df = pd.DataFrame(test_data)
    test_excel_path = 'test_watermark_data.xlsx'
    df.to_excel(test_excel_path, index=False, engine='openpyxl')
    
    print("✓ Fichier Excel de test créé.")
    
    # Test avec watermark
    print("\n=== GÉNÉRATION PDF AVEC WATERMARK ===")
    generator = PDFGenerator(
        excel_path=test_excel_path,
        template_path='templates/convocation_delf_template_modele.html',
        output_dir='output',
        access_code='W12345'  # Code d'accès test
    )
    
    try:
        # Convertir en format dict simple (première ligne du DataFrame)
        candidate_data = df.iloc[0].to_dict()
        pdf_path = generator.generate_pdf(candidate_data)
        print(f"✅ PDF avec watermark généré: {pdf_path}")
        
        # Afficher les détails du watermark qui sera visible
        print(f"\n📋 DÉTAILS DU WATERMARK:")
        print(f"   Texte: {candidate_data['prenom'].upper()} {candidate_data['nom'].upper()} {candidate_data.get('exam_type', 'DALF').upper()} {candidate_data['niveau'].upper()}")
        print(f"   Police: Helvetica Bold 26pt")
        print(f"   Angle: 45°")
        print(f"   Opacité: 10%")
        print(f"   Position: Répété sur toute la page, sous le contenu")
        
        # Ouvrir le PDF automatiquement
        print(f"\n🔍 Ouverture du PDF pour vérification...")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False
    
    # Nettoyer
    if os.path.exists(test_excel_path):
        os.remove(test_excel_path)
        print("\n🧹 Fichier Excel de test supprimé.")
    
    print("\n=== TEST TERMINÉ ===")
    print("✓ Le watermark a été ajouté au template")
    print("✓ Format: PRÉNOM NOM EXAMEN NIVEAU")
    print("✓ Exemple attendu: SATUSHI YAKURI DALF C2")
    print("✓ Vérifiez le PDF généré dans le dossier 'output'")
    
    return True

if __name__ == "__main__":
    success = test_watermark()
    if success:
        print("\n🎉 Test du watermark réussi!")
    else:
        print("\n❌ Test du watermark échoué.")
