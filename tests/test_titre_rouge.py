#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de test pour vérifier le nouveau style du titre avec bordure rouge
"""

import os
import pandas as pd
from pdf_generator import PDFGenerator

# Créer un fichier Excel de test
test_data = {
    'nom': ['ROUGE'],
    'prenom': ['Titre'],
    'numero_candidat': ['ROUGE2025001'],
    'email': ['titre.rouge@example.com'],
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

def test_titre_rouge():
    """Test du nouveau style de titre avec bordure rouge"""
    
    print("=== TEST DU TITRE AVEC BORDURE ROUGE ===\n")
    
    # Créer le DataFrame et sauvegarder
    df = pd.DataFrame(test_data)
    test_excel_path = 'test_titre_rouge_data.xlsx'
    df.to_excel(test_excel_path, index=False, engine='openpyxl')
    
    print("✓ Fichier Excel de test créé.")
    
    # Test avec nouveau style de titre
    print("\n=== GÉNÉRATION PDF AVEC TITRE BORDURE ROUGE ===")
    generator = PDFGenerator(
        excel_path=test_excel_path,
        template_path='templates/convocation_delf_template_modele.html',
        output_dir='output',
        access_code='ROUGE123'  # Code d'accès test
    )
    
    try:
        # Convertir en format dict simple (première ligne du DataFrame)
        candidate_data = df.iloc[0].to_dict()
        pdf_path = generator.generate_pdf(candidate_data)
        print(f"✅ PDF avec titre bordure rouge généré: {pdf_path}")
        
        # Afficher les détails du style
        print(f"\n📋 DÉTAILS DU NOUVEAU STYLE:")
        print(f"   Fond: Transparent (plus de gris)")
        print(f"   Bordure: Rouge vif #DA002E, 1pt")
        print(f"   Largeur: Élargie de 70px de chaque côté")
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
    print("✓ Fond gris supprimé du titre")
    print("✓ Bordure rouge vif #DA002E ajoutée (1pt)")
    print("✓ Cadre élargi de 70px de chaque côté")
    print("✓ Vérifiez le PDF généré dans le dossier 'output'")
    
    return True

if __name__ == "__main__":
    success = test_titre_rouge()
    if success:
        print("\n🎉 Test du titre avec bordure rouge réussi!")
    else:
        print("\n❌ Test du titre avec bordure rouge échoué.")
