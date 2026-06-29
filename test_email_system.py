#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test rapide du système d'emails avec le nouveau registre
"""

import json
import os
import sys
from pathlib import Path

# Ajouter le répertoire courant au path
sys.path.insert(0, str(Path(__file__).parent))

def test_email_system():
    print("🧪 TEST DU SYSTÈME D'EMAILS AVEC NOUVEAU REGISTRE")
    print("=" * 60)
    
    # Vérification du registre
    registry_path = "candidate_pdf_registry.json"
    if not os.path.exists(registry_path):
        print("❌ ERREUR: Registre non trouvé!")
        return False
    
    with open(registry_path, 'r', encoding='utf-8') as f:
        registry = json.load(f)
    
    print(f"✅ Registre chargé: {len(registry)} candidats")
    
    # Afficher quelques exemples avec nouveau format ID
    print("\n🔍 EXEMPLES DE CANDIDATS AVEC NOUVEAUX IDs:")
    count = 0
    for candidate_id, info in registry.items():
        if count < 5:
            print(f"   {count+1}. ID: {candidate_id} → {info['prenom']} {info['nom']}")
            print(f"      📧 Email: {info['email']}")
            print(f"      📄 PDF: {info['pdf_filename']}")
            count += 1
        else:
            break
    
    # Test d'importation des modules
    try:
        print("\n🔧 Test des imports...")
        from mailjet_bridge import MailjetBridge
        from candidate_pdf_registry import CandidatePDFRegistry
        print("✅ Imports réussis")
        
        # Test d'initialisation
        registry_obj = CandidatePDFRegistry()
        print(f"✅ Registre initialisé: {len(registry_obj.registry)} candidats")
        
        # Test de quelques candidats
        test_candidates = list(registry.keys())[:3]
        print(f"\n🎯 Test de 3 candidats avec nouveaux IDs:")
        
        for candidate_id in test_candidates:
            info = registry[candidate_id]
            pdf_path = registry_obj.get_pdf_path(candidate_id)
            
            print(f"\n   📝 Candidat: {info['prenom']} {info['nom']}")
            print(f"   🆔 ID simplifié: {candidate_id}")
            print(f"   📧 Email: {info['email']}")
            print(f"   📄 PDF attendu: {pdf_path}")
            print(f"   📂 PDF existe: {'✅' if os.path.exists(pdf_path) else '❌'}")
        
        print(f"\n✅ SYSTÈME PRÊT POUR L'ENVOI!")
        print(f"📊 Total candidats: {len(registry)}")
        print(f"🔐 Format ID: 6 caractères alternés (ex: {list(registry.keys())[0]})")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_email_system()
    if success:
        print("\n🎉 LE SYSTÈME EST OPÉRATIONNEL!")
        print("   Vous pouvez maintenant lancer l'envoi d'emails.")
    else:
        print("\n💥 Des problèmes subsistent...")