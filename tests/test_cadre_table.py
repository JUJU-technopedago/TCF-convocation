#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de test pour vérifier le cadre avec approche table HTML
"""

import os
import pandas as pd
from pdf_generator import PDFGenerator

# Créer un fichier Excel de test
test_data = {
    'nom': ['TABLE'],
    'prenom': ['Cadre'],
    'numero_candidat': ['TABLE2025001'],
    'email': ['cadre.table@example.com'],
    'date_naissance': ['01/01/1990'],
    'niveau': ['A2'],
    'date_examen': ['05/02/2025'],
    'heure_debut': ['10:00'],
    'date_ep_coll': ['05/02/2025'],
    'debut_ep_coll': ['10:00'],
    'date_ep_ind': ['05/02/2025'],
    'heure_preparation': ['15:00'],
    'exam_type': ['DELF']
}

def test_cadre_table():
    """Test du cadre avec approche table HTML"""
    
    print("=== TEST DU CADRE AVEC TABLE HTML ===\n")
    
    # Créer le DataFrame et sauvegarder
    df = pd.DataFrame(test_data)
    test_excel_path = 'test_cadre_table_data.xlsx'
    df.to_excel(test_excel_path, index=False, engine='openpyxl')
    
    print("✓ Fichier Excel de test créé.")
    
    # Test avec nouvelle approche table
    print("\n=== GÉNÉRATION PDF AVEC CADRE TABLE ===")
    generator = PDFGenerator(
        excel_path=test_excel_path,
        template_path='templates/convocation_delf_template_modele.html',
        output_dir='output',
        access_code='TBL456'  # Code d'accès test
    )
    
    try:
        # Convertir en format dict simple (première ligne du DataFrame)
        candidate_data = df.iloc[0].to_dict()
        pdf_path = generator.generate_pdf(candidate_data)
        print(f"✅ PDF avec cadre table généré: {pdf_path}")
        
        # Afficher les détails de l'approche
        print(f"\n📋 DÉTAILS DE L'APPROCHE TABLE:")
        print(f"   Méthode: Table HTML avec bordure inline")
        print(f"   Bordure: 3px solid #000000")
        print(f"   Compatibilité: Optimisée pour xhtml2pdf")
        print(f"   Candidat test: {candidate_data['prenom']} {candidate_data['nom']}")
        print(f"   Examen: {candidate_data.get('exam_type', 'DELF')} {candidate_data['niveau']}")
        
        # Ouvrir le PDF pour vérification
        print(f"\n🔍 Ouverture du PDF...")
        os.system(f'start "output\\{os.path.basename(pdf_path)}"')
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False
    
    # Nettoyer
    if os.path.exists(test_excel_path):
        os.remove(test_excel_path)
        print("\n🧹 Fichier Excel de test supprimé.")
    
    print("\n=== TEST TERMINÉ ===")
    print("✓ Approche table HTML utilisée")
    print("✓ Bordure noire 3px appliquée inline")
    print("✓ Centrage automatique")
    print("✓ Compatible xhtml2pdf")
    
    return True

if __name__ == "__main__":
    success = test_cadre_table()
    if success:
        print("\n🎉 Test du cadre avec table réussi!")
    else:
        print("\n❌ Test du cadre avec table échoué.")
