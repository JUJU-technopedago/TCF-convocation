#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script pour vérifier la détection des candidats en double inscription
et la génération des noms de fichier avec suffixe de niveau
"""

import pandas as pd
import os
from pdf_generator import PDFGenerator

def create_test_excel_with_duplicates():
    """Crée un fichier Excel de test avec des candidats en double inscription"""
    
    # Données de test avec des candidats dupliqués
    test_data = [
        # Candidat unique
        {
            'nom': 'MARTIN',
            'prenom': 'Jean',
            'numero_candidat': '032002111111',
            'email': 'jean.martin@email.com',
            'date_naissance': '15/03/1995',
            'telephone': '06.12.34.56.78',
            'niveau': 'A1',
            'matiere': 'DELF A1',
            'date_examen': '25/01/2025',
            'heure_debut': '09:00',
            'heure_fin': '10:30',
            'duree': '1h30',
            'salle': 'A101',
            'institution_name': 'Alliance Française Bruxelles Europe',
            'institution_address': 'Avenue des Arts 46',
            'institution_city': 'Bruxelles',
            'institution_postal': '1000',
            'institution_phone': '+32 2 788 21 60'
        },
        # Candidat en double inscription - niveau B1
        {
            'nom': 'DUPONT',
            'prenom': 'Valerie',
            'numero_candidat': '032002111111',  # Même numéro que l'exemple
            'email': 'valerie.dupont@email.com',
            'date_naissance': '22/07/1996',
            'telephone': '06.98.76.54.32',
            'niveau': 'B1',
            'matiere': 'DELF B1',
            'date_examen': '25/01/2025',
            'heure_debut': '09:00',
            'heure_fin': '11:00',
            'duree': '2h',
            'salle': 'B205',
            'institution_name': 'Alliance Française Bruxelles Europe',
            'institution_address': 'Avenue des Arts 46',
            'institution_city': 'Bruxelles',
            'institution_postal': '1000',
            'institution_phone': '+32 2 788 21 60'
        },
        # Candidat en double inscription - niveau B2
        {
            'nom': 'DUPONT',
            'prenom': 'Valerie',
            'numero_candidat': '032002111111',  # Même candidat, autre niveau
            'email': 'valerie.dupont@email.com',
            'date_naissance': '22/07/1996',
            'telephone': '06.98.76.54.32',
            'niveau': 'B2',
            'matiere': 'DELF B2',
            'date_examen': '26/01/2025',
            'heure_debut': '14:00',
            'heure_fin': '16:30',
            'duree': '2h30',
            'salle': 'C301',
            'institution_name': 'Alliance Française Bruxelles Europe',
            'institution_address': 'Avenue des Arts 46',
            'institution_city': 'Bruxelles',
            'institution_postal': '1000',
            'institution_phone': '+32 2 788 21 60'
        },
        # Autre candidat unique
        {
            'nom': 'BERNARD',
            'prenom': 'Pierre',
            'numero_candidat': '032002222222',
            'email': 'pierre.bernard@email.com',
            'date_naissance': '10/11/1994',
            'telephone': '06.11.22.33.44',
            'niveau': 'C1',
            'matiere': 'DALF C1',
            'date_examen': '27/01/2025',
            'heure_debut': '10:00',
            'heure_fin': '14:00',
            'duree': '4h',
            'salle': 'D102',
            'institution_name': 'Alliance Française Bruxelles Europe',
            'institution_address': 'Avenue des Arts 46',
            'institution_city': 'Bruxelles',
            'institution_postal': '1000',
            'institution_phone': '+32 2 788 21 60'
        },
        # Candidat triple inscription (cas extrême)
        {
            'nom': 'MOREAU',
            'prenom': 'Sophie',
            'numero_candidat': '032002333333',
            'email': 'sophie.moreau@email.com',
            'date_naissance': '05/09/1997',
            'telephone': '06.55.44.33.22',
            'niveau': 'A2',
            'matiere': 'DELF A2',
            'date_examen': '28/01/2025',
            'heure_debut': '09:00',
            'heure_fin': '11:00',
            'duree': '2h',
            'salle': 'A203',
            'institution_name': 'Alliance Française Bruxelles Europe',
            'institution_address': 'Avenue des Arts 46',
            'institution_city': 'Bruxelles',
            'institution_postal': '1000',
            'institution_phone': '+32 2 788 21 60'
        },
        {
            'nom': 'MOREAU',
            'prenom': 'Sophie',
            'numero_candidat': '032002333333',  # Même candidat
            'email': 'sophie.moreau@email.com',
            'date_naissance': '05/09/1997',
            'telephone': '06.55.44.33.22',
            'niveau': 'B1',
            'matiere': 'DELF B1',
            'date_examen': '28/01/2025',
            'heure_debut': '14:00',
            'heure_fin': '16:00',
            'duree': '2h',
            'salle': 'B101',
            'institution_name': 'Alliance Française Bruxelles Europe',
            'institution_address': 'Avenue des Arts 46',
            'institution_city': 'Bruxelles',
            'institution_postal': '1000',
            'institution_phone': '+32 2 788 21 60'
        },
        {
            'nom': 'MOREAU',
            'prenom': 'Sophie',
            'numero_candidat': '032002333333',  # Même candidat
            'email': 'sophie.moreau@email.com',
            'date_naissance': '05/09/1997',
            'telephone': '06.55.44.33.22',
            'niveau': 'B2',
            'matiere': 'DELF B2',
            'date_examen': '29/01/2025',
            'heure_debut': '09:00',
            'heure_fin': '11:30',
            'duree': '2h30',
            'salle': 'C205',
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
    test_file = 'candidats_test_duplicates.xlsx'
    df.to_excel(test_file, index=False, engine='openpyxl')
    
    print(f"✅ Fichier de test créé: {test_file}")
    print(f"📊 Contient {len(test_data)} lignes de candidats")
    print(f"👥 Candidats uniques: MARTIN Jean, BERNARD Pierre")
    print(f"👥 Candidats dupliqués: DUPONT Valerie (B1, B2), MOREAU Sophie (A2, B1, B2)")
    
    return test_file

def test_duplicate_detection():
    """Test la détection des candidats en double inscription"""
    
    print("=== TEST DE DÉTECTION DES CANDIDATS EN DOUBLE INSCRIPTION ===\n")
    
    # Créer le fichier de test
    test_file = create_test_excel_with_duplicates()
    
    try:
        # Créer le générateur de PDF
        generator = PDFGenerator(
            excel_path=test_file,
            template_path='templates/convocation_delf_template_modele.html',
            logo_af_path='assets/logoAF.png',
            logo_delf_path='assets/logoDELF.png',
            output_dir='output_test',
            access_code='1234'
        )
        
        # Messages de progression
        messages = []
        def capture_progress(message):
            messages.append(message)
            print(message)
        
        # Générer les PDF
        print("\n=== GÉNÉRATION DES PDF ===")
        success_count = generator.generate_all_pdfs(capture_progress)
        
        print(f"\n=== RÉSULTATS ===")
        print(f"PDF générés avec succès: {success_count}")
        
        # Vérifier les fichiers générés
        output_dir = 'output_test'
        if os.path.exists(output_dir):
            generated_files = [f for f in os.listdir(output_dir) if f.endswith('.pdf')]
            generated_files.sort()
            
            print(f"\n=== FICHIERS GÉNÉRÉS ({len(generated_files)}) ===")
            for file in generated_files:
                print(f"  📄 {file}")
            
            # Vérifier les noms de fichier attendus
            # Note: les zéros initiaux peuvent être supprimés lors du traitement Excel
            expected_patterns = [
                'convocation_MARTIN_Jean_32002111111.pdf',  # Candidat unique
                'convocation_DUPONT_Valerie_32002111111_B1.pdf',  # Double inscription B1
                'convocation_DUPONT_Valerie_32002111111_B2.pdf',  # Double inscription B2
                'convocation_BERNARD_Pierre_32002222222.pdf',  # Candidat unique
                'convocation_MOREAU_Sophie_32002333333_A2.pdf',  # Triple inscription A2
                'convocation_MOREAU_Sophie_32002333333_B1.pdf',  # Triple inscription B1
                'convocation_MOREAU_Sophie_32002333333_B2.pdf'   # Triple inscription B2
            ]
            
            print(f"\n=== VÉRIFICATION DES NOMS DE FICHIER ===")
            all_correct = True
            for expected in expected_patterns:
                if expected in generated_files:
                    print(f"  ✅ {expected}")
                else:
                    print(f"  ❌ MANQUANT: {expected}")
                    all_correct = False
            
            # Vérifier qu'il n'y a pas de fichiers inattendus
            unexpected_files = [f for f in generated_files if f not in expected_patterns]
            if unexpected_files:
                print(f"\n  ⚠️  FICHIERS INATTENDUS:")
                for f in unexpected_files:
                    print(f"    - {f}")
                all_correct = False
            
            if all_correct:
                print(f"\n🎉 TEST RÉUSSI! Tous les noms de fichier sont corrects.")
                print(f"✅ Les candidats en double inscription ont bien le suffixe _{'{NIVEAU}'}.pdf")
                print(f"✅ Les candidats uniques ont le format standard")
            else:
                print(f"\n❌ TEST ÉCHOUÉ! Certains fichiers ne correspondent pas aux attentes.")
        
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
    test_duplicate_detection()
