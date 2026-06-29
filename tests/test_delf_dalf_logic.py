#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script pour vérifier la logique DELF/DALF selon les niveaux
"""

import pandas as pd
import os
from pdf_generator import PDFGenerator

def create_test_data():
    """Crée des données de test avec différents niveaux"""
    test_data = [
        {
            'nom': 'MARTIN',
            'prenom': 'Sophie',
            'numero_candidat': '032002032001',
            'email': 'sophie.martin@example.com',
            'date_naissance': '15/03/1995',
            'niveau': 'A1',
            'date_examen': '25/08/2025',
            'heure_debut': '09:00',
            'date_ep_coll': '25/08/2025',
            'debut_ep_coll': '09:00',
            'date_ep_ind': '25/08/2025',
            'heure_preparation': '14:00'
        },
        {
            'nom': 'DUBOIS',
            'prenom': 'Pierre',
            'numero_candidat': '032002032002',
            'email': 'pierre.dubois@example.com',
            'date_naissance': '22/07/1988',
            'niveau': 'A2',
            'date_examen': '25/08/2025',
            'heure_debut': '09:00',
            'date_ep_coll': '25/08/2025',
            'debut_ep_coll': '09:00',
            'date_ep_ind': '25/08/2025',
            'heure_preparation': '14:30'
        },
        {
            'nom': 'GARCIA',
            'prenom': 'Maria',
            'numero_candidat': '032002032003',
            'email': 'maria.garcia@example.com',
            'date_naissance': '10/12/1992',
            'niveau': 'B1',
            'date_examen': '25/08/2025',
            'heure_debut': '09:00',
            'date_ep_coll': '25/08/2025',
            'debut_ep_coll': '09:00',
            'date_ep_ind': '25/08/2025',
            'heure_preparation': '15:00'
        },
        {
            'nom': 'JOHNSON',
            'prenom': 'Michael',
            'numero_candidat': '032002032004',
            'email': 'michael.johnson@example.com',
            'date_naissance': '05/09/1985',
            'niveau': 'B2',
            'date_examen': '25/08/2025',
            'heure_debut': '09:00',
            'date_ep_coll': '25/08/2025',
            'debut_ep_coll': '09:00',
            'date_ep_ind': '25/08/2025',
            'heure_preparation': '15:30'
        },
        {
            'nom': 'SCHMIDT',
            'prenom': 'Anna',
            'numero_candidat': '032002032005',
            'email': 'anna.schmidt@example.com',
            'date_naissance': '18/04/1990',
            'niveau': 'C1',
            'date_examen': '25/08/2025',
            'heure_debut': '09:00',
            'date_ep_coll': '25/08/2025',
            'debut_ep_coll': '09:00',
            'date_ep_ind': '25/08/2025',
            'heure_preparation': '16:00'
        },
        {
            'nom': 'TANAKA',
            'prenom': 'Hiroshi',
            'numero_candidat': '032002032006',
            'email': 'hiroshi.tanaka@example.com',
            'date_naissance': '30/11/1987',
            'niveau': 'C2',
            'date_examen': '25/08/2025',
            'heure_debut': '09:00',
            'date_ep_coll': '25/08/2025',
            'debut_ep_coll': '09:00',
            'date_ep_ind': '25/08/2025',
            'heure_preparation': '16:30'
        }
    ]
    
    return pd.DataFrame(test_data)

def test_exam_type_logic():
    """Test la logique de détermination du type d'examen"""
    print("=== TEST DE LA LOGIQUE DELF/DALF ===\n")
    
    # Créer les données de test
    df = create_test_data()
    
    # Sauvegarder dans un fichier Excel temporaire
    test_excel_path = "test_delf_dalf.xlsx"
    df.to_excel(test_excel_path, index=False)
    
    try:
        # Créer le générateur PDF
        generator = PDFGenerator(
            excel_path=test_excel_path,
            template_path="templates/convocation_delf_template_modele.html",
            logo_af_path="assets/logoAF.png",
            logo_delf_path="assets/logoDELF.png",
            output_dir="output"
        )
        
        # Tester la logique pour chaque candidat
        for index, row in df.iterrows():
            template_data = generator._prepare_template_data(row)
            niveau = template_data['niveau']
            exam_type = template_data['exam_type']
            
            print(f"Candidat: {template_data['prenom']} {template_data['nom']}")
            print(f"  Niveau: {niveau}")
            print(f"  Type d'examen: {exam_type}")
            
            # Vérifier la logique
            if niveau in ['C1', 'C2']:
                expected = 'DALF'
            else:
                expected = 'DELF'
            
            if exam_type == expected:
                print(f"  ✅ Correct: {niveau} → {exam_type}")
            else:
                print(f"  ❌ Erreur: {niveau} → {exam_type} (attendu: {expected})")
            
            print()
        
        print("=== GÉNÉRATION DES PDF DE TEST ===\n")
        
        # Générer les PDF pour vérifier visuellement
        def progress_callback(message):
            print(message)
        
        success_count = generator.generate_all_pdfs(progress_callback)
        print(f"\n✅ {success_count} PDF générés avec succès!")
        print("\nVérifiez les PDF dans le dossier 'output' pour confirmer que:")
        print("- A1, A2, B1, B2 affichent 'Examen DELF'")
        print("- C1, C2 affichent 'Examen DALF'")
        
    finally:
        # Nettoyer le fichier temporaire
        if os.path.exists(test_excel_path):
            os.remove(test_excel_path)
            print(f"\n🧹 Fichier temporaire {test_excel_path} supprimé")

if __name__ == "__main__":
    test_exam_type_logic()
