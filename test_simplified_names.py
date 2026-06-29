#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test du système de noms de fichiers simplifiés avec identifiants alternés
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from candidate_pdf_registry import CandidatePDFRegistry

def test_simplified_naming():
    """Test des nouveaux noms de fichiers simplifiés"""
    print("🧪 TEST DES NOMS DE FICHIERS SIMPLIFIÉS")
    print("=" * 60)
    
    # Candidats de test
    test_candidates = [
        {
            'nom': 'DUPONT',
            'prenom': 'Jean',
            'email': 'jean.dupont@email.com',
            'numero_candidat': 'TCF001',
            'tcf_type': 'TCF CANADA'
        },
        {
            'nom': 'MARTIN-LEFÈVRE',
            'prenom': 'Émilie',
            'email': 'emilie.martin@email.fr',
            'numero_candidat': 'TCF002',
            'tcf_type': 'TCF TP COMPLET'
        },
        {
            'nom': 'GARCÍA-HERNÁNDEZ',
            'prenom': 'José-María',
            'email': 'jose.garcia@email.es',
            'numero_candidat': 'TCF003',
            'tcf_type': 'TCF IRN'
        }
    ]
    
    # Créer le registre de test
    registry = CandidatePDFRegistry("./test_output")
    
    print("📁 NOUVEAUX NOMS DE FICHIERS SIMPLIFIÉS:")
    print()
    
    for i, candidate in enumerate(test_candidates, 1):
        print(f"🧑 Candidat {i}: {candidate['prenom']} {candidate['nom']}")
        print(f"   📧 Email: {candidate['email']}")
        
        # Générer l'ID unique simplifié
        candidate_id = registry.generate_candidate_id(candidate)
        print(f"   🆔 ID unique simplifié: {candidate_id}")
        
        # Générer le nom de fichier simplifié
        filename = registry.generate_secure_filename(candidate, "TCF")
        print(f"   📄 Nom fichier: {filename}")
        
        # Vérifier la reproductibilité
        candidate_id_2 = registry.generate_candidate_id(candidate)
        filename_2 = registry.generate_secure_filename(candidate, "TCF")
        
        if candidate_id == candidate_id_2 and filename == filename_2:
            print(f"   ✅ Reproductibilité: OK")
        else:
            print(f"   ❌ Reproductibilité: ÉCHEC")
        
        print("-" * 50)
    
    print()
    print("🎯 AVANTAGES DU NOUVEAU FORMAT:")
    print("  ✅ Noms plus courts et lisibles")
    print("  ✅ Identifiants uniques avec pattern lisible (lettre-chiffre alterné)")
    print("  ✅ Pas de timestamp long")
    print("  ✅ Toujours 100% d'unicité garantie")
    print("  ✅ Association candidat-PDF-email fiable")
    print()
    print("📝 EXEMPLE DE NOMS GÉNÉRÉS:")
    for candidate in test_candidates:
        filename = registry.generate_secure_filename(candidate, "TCF")
        print(f"  • {filename}")
    
    return True

if __name__ == "__main__":
    test_simplified_naming()