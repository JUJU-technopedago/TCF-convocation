#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour vérifier la structure du registre et tester le correctif
"""

import json
import os

def check_registry_structure():
    """Vérifier la structure du registre actuel"""
    
    print("🔍 VÉRIFICATION DE LA STRUCTURE DU REGISTRE")
    print("=" * 50)
    
    registry_path = "output/candidate_pdf_registry.json"
    
    if not os.path.exists(registry_path):
        print("❌ Pas de registre trouvé")
        return False
    
    try:
        with open(registry_path, 'r', encoding='utf-8') as f:
            registry = json.load(f)
        
        print(f"📊 REGISTRE TROUVÉ: {len(registry)} entrées")
        
        if registry:
            first_key = list(registry.keys())[0]
            first_entry = registry[first_key]
            
            print(f"🔑 Clé exemple: {first_key}")
            print(f"📋 Structure racine: {list(first_entry.keys())}")
            
            if 'candidate_info' in first_entry:
                print(f"👤 candidate_info: {list(first_entry['candidate_info'].keys())}")
            if 'pdf_info' in first_entry:
                print(f"📄 pdf_info: {list(first_entry['pdf_info'].keys())}")
            
            # Test de l'ancien parsing
            print(f"\n🔍 TEST ANCIEN PARSING:")
            valid_old = 0
            for cid, info in registry.items():
                nom = info.get('nom', 'INCONNU')
                if nom != 'INCONNU' and nom.strip():
                    valid_old += 1
            print(f"   ❌ Candidats valides (ancien): {valid_old}/{len(registry)}")
            
            # Test du nouveau parsing
            print(f"\n🔍 TEST NOUVEAU PARSING:")
            valid_new = 0
            for cid, info in registry.items():
                candidate_data = info.get('candidate_info', {})
                nom = candidate_data.get('nom', 'INCONNU')
                if nom != 'INCONNU' and nom.strip():
                    valid_new += 1
            print(f"   ✅ Candidats valides (nouveau): {valid_new}/{len(registry)}")
            
            # Afficher quelques exemples
            print(f"\n📋 EXEMPLES:")
            for i, (cid, info) in enumerate(list(registry.items())[:3]):
                candidate_data = info.get('candidate_info', {})
                nom = candidate_data.get('nom', 'INCONNU')
                prenom = candidate_data.get('prenom', '')
                email = candidate_data.get('email', 'N/A')
                print(f"   {i+1}. {cid}: {prenom} {nom} ({email})")
            
            return valid_new > 0
        else:
            print("❌ Registre vide")
            return False
            
    except Exception as e:
        print(f"❌ Erreur lecture registre: {e}")
        return False

if __name__ == "__main__":
    success = check_registry_structure()
    
    if success:
        print(f"\n🎉 CORRECTIF VALIDÉ!")
        print(f"   ✅ Le nouveau parsing fonctionne")
        print(f"   ✅ Les noms sont maintenant correctement lus")
        print(f"   🚀 L'envoi d'emails devrait fonctionner!")
    else:
        print(f"\n⚠️ PROBLÈME PERSISTANT")
        print(f"   🔄 Régénérez les PDFs pour créer un nouveau registre")
        print(f"   🔧 Ou vérifiez la structure des données")