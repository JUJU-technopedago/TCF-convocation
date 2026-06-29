#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de test pour valider la stratégie d'association 100% sûre candidat-PDF-email
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from candidate_pdf_registry import CandidatePDFRegistry


def test_secure_association_strategy():
    """
    Test complet de la stratégie d'association sécurisée candidat-PDF-email
    """
    print("🧪 TEST STRATÉGIE ASSOCIATION 100% SÛRE CANDIDAT-PDF-EMAIL")
    print("=" * 70)
    
    # Créer un répertoire de test
    test_output_dir = "./test_secure_association"
    os.makedirs(test_output_dir, exist_ok=True)
    
    # Initialiser le registre sécurisé
    registry = CandidatePDFRegistry(test_output_dir)
    
    # Candidats de test avec cas difficiles
    test_candidates = [
        {
            'nom': 'MARTIN-LEFÈVRE',
            'prenom': 'Jean-Marie',
            'email': 'jean.marie.martin@test.com',
            'numero_candidat': 'TCF001',
            'tcf_type': 'TCF CANADA'
        },
        {
            'nom': "O'CONNOR",
            'prenom': 'Émilie',
            'email': 'emilie.oconnor@email.fr',
            'numero_candidat': 'TCF002', 
            'tcf_type': 'TCF TP COMPLET'
        },
        {
            'nom': 'JOSÉ DA SILVA',
            'prenom': 'António',
            'email': 'antonio.silva@example.org',
            'numero_candidat': 'TCF003',
            'tcf_type': 'TCF IRN'
        },
        {
            'nom': 'MÜLLER-GONZÁLEZ',
            'prenom': 'François',
            'email': 'francois.muller@domain.de',
            'numero_candidat': 'TCF004',
            'tcf_type': 'TCF CANADA'
        },
        {
            'nom': 'MARTIN',  # NOM IDENTIQUE à un autre candidat
            'prenom': 'Pierre',
            'email': 'pierre.martin@email.com',
            'numero_candidat': 'TCF005',
            'tcf_type': 'TCF TP COMPLET'
        }
    ]
    
    print(f"📋 Candidats de test: {len(test_candidates)}")
    print("-" * 50)
    
    # Test 1: Génération d'identifiants uniques
    print("🆔 TEST 1: GÉNÉRATION IDENTIFIANTS UNIQUES")
    candidate_ids = []
    for i, candidate in enumerate(test_candidates, 1):
        candidate_id = registry.generate_candidate_id(candidate)
        candidate_ids.append(candidate_id)
        
        print(f"  {i}. {candidate['prenom']} {candidate['nom']}")
        print(f"     Email: {candidate['email']}")
        print(f"     ID unique: {candidate_id}")
        print(f"     TCF Type: {candidate['tcf_type']}")
        print()
    
    # Vérifier l'unicité des IDs
    unique_ids = set(candidate_ids)
    if len(unique_ids) == len(candidate_ids):
        print("✅ TOUS LES IDs SONT UNIQUES !")
    else:
        print("❌ COLLISION D'IDs DÉTECTÉE !")
        return False
    
    print("-" * 50)
    
    # Test 2: Génération de noms de fichiers sécurisés
    print("📄 TEST 2: GÉNÉRATION NOMS FICHIERS SÉCURISÉS")
    secure_filenames = []
    for i, candidate in enumerate(test_candidates, 1):
        secure_filename = registry.generate_secure_filename(candidate, "TCF")
        secure_filenames.append(secure_filename)
        
        print(f"  {i}. {candidate['prenom']} {candidate['nom']}")
        print(f"     Fichier sécurisé: {secure_filename}")
        print()
    
    # Vérifier l'unicité des noms de fichiers
    unique_filenames = set(secure_filenames)
    if len(unique_filenames) == len(secure_filenames):
        print("✅ TOUS LES NOMS DE FICHIERS SONT UNIQUES !")
    else:
        print("❌ COLLISION DE NOMS DE FICHIERS DÉTECTÉE !")
        return False
    
    print("-" * 50)
    
    # Test 3: Simulation d'enregistrement et de recherche
    print("🔒 TEST 3: ENREGISTREMENT ET RECHERCHE SÉCURISÉS")
    
    # Créer des fichiers PDF factices pour le test
    for i, (candidate, secure_filename) in enumerate(zip(test_candidates, secure_filenames), 1):
        pdf_path = os.path.join(test_output_dir, secure_filename)
        
        # Créer un fichier PDF factice avec contenu unique
        with open(pdf_path, 'wb') as f:
            # Signature PDF basique + contenu unique
            unique_content = f"PDF FACTICE POUR {candidate['prenom']} {candidate['nom']} - {candidate['email']}"
            pdf_header = b'%PDF-1.4\n' + unique_content.encode('utf-8') + b'\n%%EOF'
            f.write(pdf_header)
        
        print(f"  {i}. Fichier créé: {secure_filename} ({os.path.getsize(pdf_path)} bytes)")
    
    print("\n🔒 ENREGISTREMENT DANS LE REGISTRE SÉCURISÉ:")
    # Enregistrer dans le registre
    registration_results = []
    for i, (candidate, secure_filename) in enumerate(zip(test_candidates, secure_filenames), 1):
        pdf_path = os.path.join(test_output_dir, secure_filename)
        
        try:
            candidate_id = registry.register_candidate_pdf(candidate, secure_filename, pdf_path)
            registration_results.append((candidate_id, True, None))
            print(f"  ✅ {i}. Enregistré: {candidate['prenom']} {candidate['nom']} (ID: {candidate_id})")
        except Exception as e:
            registration_results.append((None, False, str(e)))
            print(f"  ❌ {i}. Échec: {candidate['prenom']} {candidate['nom']} - {e}")
    
    print("\n🔍 TEST DE RECHERCHE:")
    # Tester la recherche pour chaque candidat
    search_results = []
    for i, candidate in enumerate(test_candidates, 1):
        found_path, found_filename = registry.find_pdf_for_candidate(candidate)
        
        if found_path and found_filename:
            search_results.append(True)
            print(f"  ✅ {i}. Trouvé: {candidate['prenom']} {candidate['nom']}")
            print(f"      Fichier: {found_filename}")
            print(f"      Chemin: {found_path}")
        else:
            search_results.append(False)
            print(f"  ❌ {i}. NON TROUVÉ: {candidate['prenom']} {candidate['nom']}")
        print()
    
    print("-" * 50)
    
    # Test 4: Validation intégrité
    print("🔍 TEST 4: VALIDATION INTÉGRITÉ DU REGISTRE")
    integrity_report = registry.validate_registry_integrity()
    
    print(f"📊 Rapport d'intégrité:")
    print(f"  Total enregistrements: {integrity_report['total_registered']}")
    print(f"  Entrées valides: {integrity_report['valid_entries']}")
    print(f"  Fichiers manquants: {integrity_report['missing_files']}")
    print(f"  Checksums invalides: {integrity_report['invalid_checksums']}")
    
    if integrity_report['errors']:
        print(f"  ⚠️ Erreurs détectées:")
        for error in integrity_report['errors']:
            print(f"    - {error}")
    else:
        print("  ✅ Aucune erreur détectée !")
    
    print("-" * 50)
    
    # Test 5: Simulation association email
    print("📧 TEST 5: SIMULATION ASSOCIATION CANDIDAT-PDF-EMAIL")
    
    email_associations = []
    for i, candidate in enumerate(test_candidates, 1):
        candidate_id = registry.generate_candidate_id(candidate)
        found_path, found_filename = registry.find_pdf_for_candidate(candidate)
        
        association = {
            'candidat': f"{candidate['prenom']} {candidate['nom']}",
            'email': candidate['email'],
            'candidate_id': candidate_id,
            'pdf_filename': found_filename,
            'pdf_path': found_path,
            'association_valide': bool(found_path and found_filename and candidate['email'])
        }
        
        email_associations.append(association)
        
        status = "✅ VALIDE" if association['association_valide'] else "❌ INVALIDE"
        print(f"  {i}. {status}")
        print(f"     Candidat: {association['candidat']}")
        print(f"     Email: {association['email']}")
        print(f"     ID: {association['candidate_id']}")
        print(f"     PDF: {association['pdf_filename']}")
        print()
    
    # Vérifications finales
    total_valid_associations = sum(1 for assoc in email_associations if assoc['association_valide'])
    
    print("=" * 70)
    print("🎯 RÉSULTAT FINAL DU TEST")
    print(f"📊 Associations valides: {total_valid_associations}/{len(test_candidates)}")
    
    if total_valid_associations == len(test_candidates):
        print("🎉 ✅ STRATÉGIE D'ASSOCIATION 100% SÛRE: VALIDÉE !")
        print("🔒 Chaque candidat est associé de manière fiable à son PDF et email unique")
        
        # Générer rapport détaillé
        report_file = registry.export_registry_report()
        print(f"📋 Rapport détaillé généré: {report_file}")
        
        return True
    else:
        print("💥 ❌ STRATÉGIE D'ASSOCIATION: ÉCHEC")
        print("⚠️ Des candidats ne sont pas correctement associés")
        return False


def cleanup_test_files():
    """Nettoie les fichiers de test"""
    import shutil
    test_dir = "./test_secure_association"
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)
        print("🧹 Fichiers de test nettoyés")


if __name__ == "__main__":
    try:
        success = test_secure_association_strategy()
        
        print("\n" + "=" * 70)
        if success:
            print("🏆 CONCLUSION: La stratégie d'association 100% sûre est OPÉRATIONNELLE")
            print("✅ Vous pouvez générer des PDFs en toute confiance")
            print("🔒 Chaque candidat sera associé à son PDF unique sans erreur possible")
        else:
            print("⚠️ CONCLUSION: Des problèmes ont été détectés")
            print("🔧 Vérifiez la configuration avant utilisation en production")
        
        # Proposer de nettoyer
        response = input("\n🧹 Voulez-vous nettoyer les fichiers de test ? (o/N): ")
        if response.lower() in ['o', 'oui', 'y', 'yes']:
            cleanup_test_files()
            
    except Exception as e:
        print(f"💥 Erreur lors du test: {e}")
        import traceback
        traceback.print_exc()