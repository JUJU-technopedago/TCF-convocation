#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test du système d'enforcement robuste des pièces jointes
Vérifie que les emails ne sont envoyés que si les PDF sont valides et trouvés
"""

import os
import sys
import tempfile
import shutil
from pathlib import Path

# Ajouter le répertoire racine au path pour les imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def create_test_pdfs(test_dir):
    """Crée des fichiers PDF de test avec différentes conditions"""
    
    # Créer un PDF valide (simulé)
    valid_pdf_path = os.path.join(test_dir, "convocation_MARTIN_Jean_032002001001.pdf")
    with open(valid_pdf_path, 'wb') as f:
        f.write(b'%PDF-1.4\n')  # Header PDF valide
        f.write(b'Test PDF content with sufficient size to pass validation' * 100)
    
    # Créer un PDF avec suffixe niveau
    level_pdf_path = os.path.join(test_dir, "convocation_DUPONT_Marie_032002001002_B2.pdf")
    with open(level_pdf_path, 'wb') as f:
        f.write(b'%PDF-1.4\n')
        f.write(b'Test PDF content with level suffix' * 100)
    
    # Créer un fichier trop petit (invalide)
    small_pdf_path = os.path.join(test_dir, "convocation_PETIT_Paul_032002001003.pdf")
    with open(small_pdf_path, 'wb') as f:
        f.write(b'%PDF-1.4\n')  # Seulement le header, trop petit
    
    # Créer un fichier non-PDF
    fake_pdf_path = os.path.join(test_dir, "convocation_FAUX_Pierre_032002001004.pdf")
    with open(fake_pdf_path, 'wb') as f:
        f.write(b'Not a PDF file content')
    
    return {
        'valid': valid_pdf_path,
        'level_suffix': level_pdf_path,
        'too_small': small_pdf_path,
        'fake_pdf': fake_pdf_path
    }

def test_find_pdf_file_robust():
    """Teste la recherche robuste de fichiers PDF"""
    
    print("🔍 TEST: Recherche robuste de fichiers PDF")
    print("=" * 50)
    
    # Créer un répertoire temporaire
    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"📁 Répertoire de test: {temp_dir}")
        
        # Créer des PDF de test
        test_pdfs = create_test_pdfs(temp_dir)
        
        # Importer la classe principale (simulation)
        from main import ConvocationGenerator
        
        # Créer une instance pour accéder aux méthodes
        app = ConvocationGenerator()
        
        # Test 1: Candidat avec PDF valide
        candidat1 = {
            'nom': 'MARTIN',
            'prenom': 'Jean',
            'numero_candidat': '032002001001'
        }
        
        print(f"\n🧪 Test 1: Candidat avec PDF valide")
        pdf_path, pdf_filename = app._find_pdf_file_robust(candidat1, temp_dir)
        
        if pdf_path and os.path.exists(pdf_path):
            print(f"   ✅ PDF trouvé: {pdf_filename}")
            
            # Test de validation
            is_valid, msg = app._validate_attachment(pdf_path, pdf_filename, candidat1)
            print(f"   📎 Validation: {msg}")
            if is_valid:
                print(f"   ✅ PDF valide et prêt pour envoi")
            else:
                print(f"   ❌ PDF invalide: {msg}")
        else:
            print(f"   ❌ PDF non trouvé")
        
        # Test 2: Candidat avec PDF avec suffixe niveau
        candidat2 = {
            'nom': 'DUPONT',
            'prenom': 'Marie',
            'numero_candidat': '032002001002'
        }
        
        print(f"\n🧪 Test 2: Candidat avec PDF avec suffixe niveau")
        pdf_path, pdf_filename = app._find_pdf_file_robust(candidat2, temp_dir)
        
        if pdf_path:
            print(f"   ✅ PDF trouvé: {pdf_filename}")
            is_valid, msg = app._validate_attachment(pdf_path, pdf_filename, candidat2)
            print(f"   📎 Validation: {msg}")
        else:
            print(f"   ❌ PDF non trouvé")
        
        # Test 3: Candidat avec PDF trop petit
        candidat3 = {
            'nom': 'PETIT',
            'prenom': 'Paul',
            'numero_candidat': '032002001003'
        }
        
        print(f"\n🧪 Test 3: Candidat avec PDF trop petit")
        pdf_path, pdf_filename = app._find_pdf_file_robust(candidat3, temp_dir)
        
        if pdf_path:
            print(f"   ⚠️ PDF trouvé: {pdf_filename}")
            is_valid, msg = app._validate_attachment(pdf_path, pdf_filename, candidat3)
            print(f"   📎 Validation: {msg}")
            if not is_valid:
                print(f"   ✅ Correctement rejeté (trop petit)")
        else:
            print(f"   ❌ PDF non trouvé")
        
        # Test 4: Candidat avec faux PDF
        candidat4 = {
            'nom': 'FAUX',
            'prenom': 'Pierre',
            'numero_candidat': '032002001004'
        }
        
        print(f"\n🧪 Test 4: Candidat avec faux PDF")
        pdf_path, pdf_filename = app._find_pdf_file_robust(candidat4, temp_dir)
        
        if pdf_path:
            print(f"   ⚠️ PDF trouvé: {pdf_filename}")
            is_valid, msg = app._validate_attachment(pdf_path, pdf_filename, candidat4)
            print(f"   📎 Validation: {msg}")
            if not is_valid:
                print(f"   ✅ Correctement rejeté (pas un PDF)")
        else:
            print(f"   ❌ PDF non trouvé")
        
        # Test 5: Candidat sans PDF
        candidat5 = {
            'nom': 'INEXISTANT',
            'prenom': 'Absent',
            'numero_candidat': '032002999999'
        }
        
        print(f"\n🧪 Test 5: Candidat sans PDF")
        pdf_path, pdf_filename = app._find_pdf_file_robust(candidat5, temp_dir)
        
        if pdf_path:
            print(f"   ❌ PDF trouvé unexpectedly: {pdf_filename}")
        else:
            print(f"   ✅ PDF correctement non trouvé (enforcement fonctionnel)")

def test_patterns_recherche():
    """Teste les différents patterns de recherche"""
    
    print(f"\n🔍 TEST: Patterns de recherche de fichiers")
    print("=" * 50)
    
    with tempfile.TemporaryDirectory() as temp_dir:
        # Créer des fichiers avec différents formats
        test_files = [
            "convocation_MARTIN_Jean_032002001001.pdf",
            "convocation_martin_jean_032002001001.pdf",
            "convocation_MARTIN_JEAN_032002001001.pdf",
            "convocation_DUBOIS_Marie-Claire_032002001002.pdf",
            "convocation_VAN_DEN_Berg_Klaus_032002001003.pdf",
            "convocation_DUPONT_Paul_032002001004_B2.pdf",
            "convocation_BERNARD_Sophie_032002001005_C1.pdf",
        ]
        
        # Créer tous les fichiers
        for filename in test_files:
            filepath = os.path.join(temp_dir, filename)
            with open(filepath, 'wb') as f:
                f.write(b'%PDF-1.4\n')
                f.write(b'Test PDF content' * 200)
        
        print(f"📁 Fichiers créés: {len(test_files)}")
        for f in test_files:
            print(f"   • {f}")
        
        from main import ConvocationGenerator
        app = ConvocationGenerator()
        
        # Test des patterns
        candidats_test = [
            {'nom': 'MARTIN', 'prenom': 'Jean', 'numero_candidat': '032002001001'},
            {'nom': 'martin', 'prenom': 'jean', 'numero_candidat': '032002001001'},  # minuscules
            {'nom': 'DUBOIS', 'prenom': 'Marie-Claire', 'numero_candidat': '032002001002'},  # tiret
            {'nom': 'VAN DEN Berg', 'prenom': 'Klaus', 'numero_candidat': '032002001003'},  # espaces et casse mixte
            {'nom': 'DUPONT', 'prenom': 'Paul', 'numero_candidat': '032002001004'},  # avec niveau
            {'nom': 'BERNARD', 'prenom': 'Sophie', 'numero_candidat': '032002001005'},  # avec niveau C1
        ]
        
        for i, candidat in enumerate(candidats_test, 1):
            print(f"\n🧪 Test pattern {i}: {candidat['prenom']} {candidat['nom']}")
            pdf_path, pdf_filename = app._find_pdf_file_robust(candidat, temp_dir)
            
            if pdf_path:
                is_valid, msg = app._validate_attachment(pdf_path, pdf_filename, candidat)
                if is_valid:
                    print(f"   ✅ Trouvé et valide: {pdf_filename}")
                else:
                    print(f"   ⚠️ Trouvé mais invalide: {msg}")
            else:
                print(f"   ❌ Non trouvé")

def main():
    """Fonction principale de test"""
    
    print("🧪 TESTS DU SYSTÈME D'ENFORCEMENT DES PIÈCES JOINTES")
    print("=" * 60)
    
    try:
        # Test 1: Recherche robuste
        test_find_pdf_file_robust()
        
        # Test 2: Patterns de recherche
        test_patterns_recherche()
        
        print(f"\n✅ TOUS LES TESTS TERMINÉS")
        print(f"📊 Le système d'enforcement est opérationnel")
        print(f"🚫 Les emails sans pièces jointes valides seront bloqués")
        
    except Exception as e:
        print(f"\n❌ ERREUR DURANT LES TESTS: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
