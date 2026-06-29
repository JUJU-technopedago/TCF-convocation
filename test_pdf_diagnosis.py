#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test pour diagnostiquer le problème de génération PDF identique
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tcf_excel_processor import TCFExcelProcessor
from pdf_generator import PDFGenerator

def test_pdf_generation_diagnosis():
    """Diagnostic approfondi de la génération PDF"""
    
    print("🔍 DIAGNOSTIC GÉNÉRATION PDF - Recherche du problème de contenu identique")
    print("=" * 80)
    
    try:
        # Charger les candidats TCF
        processor = TCFExcelProcessor("JURYS FINAL TCF.xlsx")
        processor.load_tcf_data()
        candidates = processor.get_all_candidates()
        
        print(f"📊 Total candidats chargés: {len(candidates)}")
        
        # Prendre les 3 premiers candidats pour diagnostic
        test_candidates = candidates[:3]
        
        print("\n🔍 ÉTAPE 1: Vérification des données candidats AVANT génération PDF")
        print("-" * 60)
        
        for i, candidate in enumerate(test_candidates, 1):
            print(f"\n{i}. Candidat dans la liste:")
            print(f"   Nom: {candidate.get('nom', 'N/A')}")
            print(f"   Prénom: {candidate.get('prenom', 'N/A')}")
            print(f"   Email: {candidate.get('email', 'N/A')}")
            print(f"   TCF Type: {candidate.get('tcf_type', 'N/A')}")
            print(f"   Numéro: {candidate.get('numero_candidat', 'N/A')}")
            print(f"   Toutes les clés: {list(candidate.keys())[:10]}...")  # Première 10 clés
        
        print(f"\n🔍 ÉTAPE 2: Test avec PDFGenerator - Vérification de _prepare_template_data")
        print("-" * 60)
        
        # Créer un générateur PDF pour test
        generator = PDFGenerator(
            excel_path="JURYS FINAL TCF.xlsx",
            template_path="templates/template_tcf_simple.html",
            logo_af_path="assets/logoAF.png",
            logo_delf_path="assets/logoTCF.png",
            output_dir="test_output",
            access_code="",
            qrcode_path=""
        )
        
        # Créer répertoire de test
        os.makedirs("test_output", exist_ok=True)
        
        # Tester la préparation des données pour chaque candidat
        for i, candidate in enumerate(test_candidates, 1):
            print(f"\n{i}. Test _prepare_template_data pour:")
            print(f"   Candidat source: {candidate.get('nom', 'N/A')} {candidate.get('prenom', 'N/A')}")
            
            # Appeler directement _prepare_template_data pour voir ce qui est préparé
            template_data = generator._prepare_template_data(candidate)
            
            print(f"   Données template préparées:")
            print(f"     nom: {template_data.get('nom', 'N/A')}")
            print(f"     prenom: {template_data.get('prenom', 'N/A')}")
            print(f"     email: {template_data.get('email', 'N/A')}")
            print(f"     tcf_type: {template_data.get('tcf_type', 'N/A')}")
            print(f"     type_tcf: {template_data.get('type_tcf', 'N/A')}")
            print(f"     numero_candidat: {template_data.get('numero_candidat', 'N/A')}")
            
            # Vérifier si les données sont bien distinctes
            if i == 1:
                first_candidate_data = template_data
            else:
                # Comparer avec le premier candidat
                differences = []
                for key in ['nom', 'prenom', 'email', 'tcf_type', 'numero_candidat']:
                    if template_data.get(key) != first_candidate_data.get(key):
                        differences.append(f"{key}: {first_candidate_data.get(key)} → {template_data.get(key)}")
                
                if differences:
                    print(f"   ✅ Différences détectées: {'; '.join(differences)}")
                else:
                    print(f"   ❌ PROBLÈME: Données identiques au premier candidat !")
        
        print(f"\n🔍 ÉTAPE 3: Test génération PDF réelle")
        print("-" * 60)
        
        # Générer un PDF pour chaque candidat et vérifier le contenu
        generated_files = []
        
        for i, candidate in enumerate(test_candidates, 1):
            nom = candidate.get('nom', 'INCONNU')
            prenom = candidate.get('prenom', '')
            pdf_filename = f"test_convocation_tcf_{nom}_{prenom}.pdf".replace(" ", "_")
            
            print(f"\n{i}. Génération PDF pour {prenom} {nom}")
            print(f"   Fichier: {pdf_filename}")
            
            try:
                pdf_path = generator.generate_pdf(candidate, pdf_filename)
                
                if pdf_path and os.path.exists(pdf_path):
                    file_size = os.path.getsize(pdf_path)
                    print(f"   ✅ PDF généré: {file_size} bytes")
                    generated_files.append((pdf_filename, file_size, nom, prenom))
                else:
                    print(f"   ❌ Échec génération PDF")
            except Exception as e:
                print(f"   ❌ Erreur: {e}")
        
        print(f"\n🔍 ÉTAPE 4: Analyse des PDF générés")
        print("-" * 60)
        
        if len(generated_files) >= 2:
            # Comparer les tailles de fichier
            sizes = [f[1] for f in generated_files]
            unique_sizes = set(sizes)
            
            print(f"📊 Fichiers générés: {len(generated_files)}")
            print(f"📊 Tailles uniques: {len(unique_sizes)}")
            
            for filename, size, nom, prenom in generated_files:
                print(f"   - {filename}: {size} bytes ({prenom} {nom})")
            
            if len(unique_sizes) == 1:
                print(f"\n❌ PROBLÈME CONFIRMÉ: Tous les PDF ont la même taille ({sizes[0]} bytes)")
                print("   Cela suggère fortement qu'ils contiennent le même contenu")
            elif len(unique_sizes) == len(generated_files):
                print(f"\n✅ BONNE NOUVELLE: Chaque PDF a une taille différente")
                print("   Cela suggère que les PDF contiennent des données distinctes")
            else:
                print(f"\n⚠️ RÉSULTAT MIXTE: {len(unique_sizes)} tailles différentes pour {len(generated_files)} fichiers")
        
        print(f"\n📋 CONCLUSION:")
        print("Si tous les PDF ont la même taille, le problème est dans la génération du contenu.")
        print("Si les PDF ont des tailles différentes, le problème pourrait être ailleurs.")
        
    except Exception as e:
        print(f"❌ Erreur durant le diagnostic: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_pdf_generation_diagnosis()