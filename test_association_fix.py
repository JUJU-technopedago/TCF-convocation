#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test spécifique pour valider la correction du problème d'association PDF
"""

import os
import sys
import shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from candidate_pdf_registry import CandidatePDFRegistry


def test_pdf_email_fix():
    """Test la correction du problème d'association PDF-email"""
    print("🧪 TEST CORRECTION ASSOCIATION PDF-EMAIL")
    print("=" * 60)
    
    test_dir = "./test_fix"
    os.makedirs(test_dir, exist_ok=True)
    
    try:
        # Candidats de test
        candidates = [
            {'nom': 'DUPONT', 'prenom': 'Jean', 'email': 'jean@test.com', 'tcf_type': 'TCF CANADA'},
            {'nom': 'MARTIN', 'prenom': 'Marie', 'email': 'marie@test.com', 'tcf_type': 'TCF TP COMPLET'},
            {'nom': 'BERNARD', 'prenom': 'Pierre', 'email': 'pierre@test.com', 'tcf_type': 'TCF IRN'}
        ]
        
        # ÉTAPE 1: Génération PDF avec registre
        print("📋 ÉTAPE 1: GÉNÉRATION PDF")
        registry1 = CandidatePDFRegistry(test_dir)
        
        for i, candidate in enumerate(candidates, 1):
            filename = registry1.generate_secure_filename(candidate, "TCF")
            pdf_path = os.path.join(test_dir, filename)
            
            # PDF unique pour chaque candidat
            with open(pdf_path, 'wb') as f:
                content = f"PDF pour {candidate['prenom']} {candidate['nom']} - {candidate['email']}"
                f.write(b'%PDF-1.4\n' + content.encode('utf-8') + b'\n%%EOF')
            
            registry1.register_candidate_pdf(candidate, filename, pdf_path)
            print(f"  {i}. ✅ {candidate['prenom']} {candidate['nom']} -> {filename}")
        
        # ÉTAPE 2: Envoi email avec nouveau registre (simulation problème)
        print("\n📧 ÉTAPE 2: ENVOI EMAILS SÉPARÉ")
        registry2 = CandidatePDFRegistry(test_dir)  # Nouveau registre
        
        results = []
        for i, candidate in enumerate(candidates, 1):
            pdf_path, filename = registry2.find_pdf_for_candidate(candidate)
            
            if pdf_path and filename:
                # Vérifier contenu
                with open(pdf_path, 'rb') as f:
                    content = f.read().decode('utf-8', errors='ignore')
                
                correct = (candidate['email'] in content and candidate['nom'] in content)
                results.append(correct)
                
                status = "✅ CORRECT" if correct else "❌ INCORRECT"
                print(f"  {i}. {status}: {candidate['prenom']} {candidate['nom']}")
                print(f"     PDF: {filename}")
            else:
                print(f"  {i}. ❌ AUCUN PDF: {candidate['prenom']} {candidate['nom']}")
                results.append(False)
        
        success = all(results)
        print(f"\n🎯 RÉSULTAT: {sum(results)}/{len(results)} associations correctes")
        
        return success
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False
        
    finally:
        if os.path.exists(test_dir):
            shutil.rmtree(test_dir)


if __name__ == "__main__":
    try:
        success = test_pdf_email_fix()
        
        print("\n" + "=" * 60)
        if success:
            print("🎉 ✅ CORRECTION VALIDÉE")
            print("🔒 Association PDF-email maintenant fiable")
        else:
            print("❌ PROBLÈME PERSISTANT")
            
    except Exception as e:
        print(f"💥 Erreur: {e}")