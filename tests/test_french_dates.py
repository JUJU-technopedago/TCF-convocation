#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script pour vérifier le formatage des dates en français
Format attendu: "lundi 01 janvier 2000"
"""

import pandas as pd
import os
from pdf_generator import PDFGenerator
from datetime import datetime

def create_test_excel_with_dates():
    """Crée un fichier Excel de test avec des dates spécifiques"""
    
    # Données de test avec des dates variées
    test_data = [
        # Test avec une date de lundi
        {
            'nom': 'MARTIN',
            'prenom': 'Jean',
            'numero_candidat': '032002111111',
            'email': 'jean.martin@email.com',
            'date_naissance': '15/03/1995',
            'telephone': '06.12.34.56.78',
            'niveau': 'B1',
            'matiere': 'DELF B1',
            'date_examen': '27/01/2025',  # Lundi
            'date_ep_coll': '27/01/2025',
            'date_ep_ind': '28/01/2025',   # Mardi
            'heure_debut': '09:00',
            'debut_ep_coll': '09:00',
            'heure_preparation': '14:30',
            'heure_fin': '11:00',
            'duree': '2h',
            'salle': 'A101',
            'institution_name': 'Alliance Française Bruxelles Europe',
            'institution_address': 'Avenue des Arts 46',
            'institution_city': 'Bruxelles',
            'institution_postal': '1000',
            'institution_phone': '+32 2 788 21 60'
        },
        # Test avec une date de vendredi en décembre
        {
            'nom': 'DUPONT',
            'prenom': 'Marie',
            'numero_candidat': '032002222222',
            'email': 'marie.dupont@email.com',
            'date_naissance': '22/07/1996',
            'telephone': '06.98.76.54.32',
            'niveau': 'B2',
            'matiere': 'DELF B2',
            'date_examen': '20/12/2024',  # Vendredi
            'date_ep_coll': '20/12/2024',
            'date_ep_ind': '21/12/2024',   # Samedi
            'heure_debut': '08:30',
            'debut_ep_coll': '08:30',
            'heure_preparation': '15:15',
            'heure_fin': '11:00',
            'duree': '2h30',
            'salle': 'B205',
            'institution_name': 'Alliance Française Bruxelles Europe',
            'institution_address': 'Avenue des Arts 46',
            'institution_city': 'Bruxelles',
            'institution_postal': '1000',
            'institution_phone': '+32 2 788 21 60'
        }
    ]
    
    # Créer le DataFrame
    df = pd.DataFrame(test_data)
    
    # Sauvegarder dans un fichier Excel
    test_file = 'candidats_test_dates_francaises.xlsx'
    df.to_excel(test_file, index=False, engine='openpyxl')
    
    print(f"✅ Fichier de test créé: {test_file}")
    print(f"📊 Contient {len(test_data)} candidats avec dates de test")
    print(f"📅 Date 1: 27/01/2025 (lundi) et 28/01/2025 (mardi)")
    print(f"📅 Date 2: 20/12/2024 (vendredi) et 21/12/2024 (samedi)")
    
    return test_file

def test_french_date_formatting():
    """Test le formatage des dates en français"""
    
    print("=== TEST DE FORMATAGE DES DATES EN FRANÇAIS ===\n")
    
    # Test unitaire de la fonction de formatage
    generator = PDFGenerator(
        excel_path='dummy.xlsx',  # Pas utilisé pour ce test
        template_path='templates/convocation_delf_template_modele.html',
        logo_af_path='assets/logoAF.png',
        logo_delf_path='assets/logoDELF.png',
        output_dir='output_test_dates',
        access_code='1234'
    )
    
    print("=== TESTS UNITAIRES DES DATES ===")
    
    # Test de dates spécifiques
    test_dates = [
        ('27/01/2025', 'lundi 27 janvier 2025'),
        ('28/01/2025', 'mardi 28 janvier 2025'),
        ('20/12/2024', 'vendredi 20 décembre 2024'),
        ('21/12/2024', 'samedi 21 décembre 2024'),
        ('01/01/2000', 'samedi 01 janvier 2000'),
        ('15/08/2024', 'jeudi 15 août 2024'),
        ('29/02/2024', 'jeudi 29 février 2024'),  # Année bissextile
    ]
    
    all_tests_passed = True
    for input_date, expected in test_dates:
        result = generator._format_date_french(input_date)
        if result == expected:
            print(f"  ✅ {input_date} → {result}")
        else:
            print(f"  ❌ {input_date} → {result} (attendu: {expected})")
            all_tests_passed = False
    
    if all_tests_passed:
        print("\n🎉 Tous les tests unitaires sont réussis!\n")
    else:
        print("\n❌ Certains tests unitaires ont échoué!\n")
        return False
    
    # Créer le fichier de test pour génération PDF
    test_file = create_test_excel_with_dates()
    
    try:
        # Messages de progression
        messages = []
        def capture_progress(message):
            messages.append(message)
            print(message)
        
        # Générer les PDF
        print("\n=== GÉNÉRATION DES PDF AVEC DATES FRANÇAISES ===")
        success_count = generator.generate_all_pdfs(capture_progress)
        
        print(f"\n=== RÉSULTATS ===")
        print(f"PDF générés avec succès: {success_count}")
        
        # Vérifier les fichiers générés
        output_dir = 'output_test_dates'
        if os.path.exists(output_dir):
            generated_files = [f for f in os.listdir(output_dir) if f.endswith('.pdf')]
            generated_files.sort()
            
            print(f"\n=== FICHIERS GÉNÉRÉS ({len(generated_files)}) ===")
            for file in generated_files:
                print(f"  📄 {file}")
            
            if len(generated_files) >= 2:
                print(f"\n🎉 TEST RÉUSSI!")
                print(f"✅ {success_count} convocations générées avec formatage français des dates")
                print(f"✅ Les dates doivent apparaître comme 'lundi 27 janvier 2025' dans les PDF")
                print(f"📝 Vérifiez manuellement les PDF pour confirmer le bon formatage")
                
                # Afficher les dates attendues
                print(f"\n📅 Dates attendues dans les convocations:")
                print(f"  - MARTIN Jean: lundi 27 janvier 2025 (collectives), mardi 28 janvier 2025 (individuelle)")
                print(f"  - DUPONT Marie: vendredi 20 décembre 2024 (collectives), samedi 21 décembre 2024 (individuelle)")
            else:
                print(f"\n❌ TEST ÉCHOUÉ! Pas assez de PDF générés.")
                return False
        
    except Exception as e:
        print(f"❌ ERREUR lors du test: {e}")
        return False
    
    finally:
        # Nettoyer les fichiers de test
        try:
            if os.path.exists(test_file):
                os.remove(test_file)
                print(f"\n🧹 Fichier de test supprimé: {test_file}")
        except:
            pass
    
    return True

if __name__ == "__main__":
    test_french_date_formatting()
