#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TEST INTERFACE - Simule l'envoi d'emails pour vérifier que l'interface utilise le bon registre
"""

import json
import os

def simulate_interface_email_function():
    """Simule la fonction send_emails_simple_mailjet() de l'interface"""
    
    print("SIMULATION DE L'INTERFACE - Test envoi emails")
    print("=" * 50)
    
    # Simuler le dossier output configuré dans l'interface
    output_dir = r"C:\Users\JMM\Desktop\convoc generator TCF\output"
    
    # Vérifier que le registre existe dans output (comme le fait l'interface)
    registry_path = os.path.join(output_dir, "candidate_pdf_registry.json")
    
    print(f"Recherche registre dans: {registry_path}")
    
    if not os.path.exists(registry_path):
        print("ERREUR: Registre des candidats non trouvé dans output!")
        return 0
    
    # Charger le registre depuis le dossier OUTPUT (comme le fait l'interface)
    with open(registry_path, 'r', encoding='utf-8') as f:
        registry = json.load(f)
    
    print(f"REGISTRE OUTPUT: {len(registry)} candidats chargés")
    
    # Simuler l'envoi d'emails (compter les candidats valides)
    valid_candidates = 0
    inconnu_candidates = 0
    
    print("\nSIMULATION ENVOI:")
    for i, (candidate_id, candidate_info) in enumerate(list(registry.items())[:10], 1):  # Teste les 10 premiers
        nom = candidate_info.get('nom', 'INCONNU')
        prenom = candidate_info.get('prenom', '')
        email = candidate_info.get('email', 'N/A')
        
        print(f"[{i}/10] Candidat {candidate_id}: {prenom} {nom} ({email})")
        
        if nom != 'INCONNU' and email != 'N/A':
            valid_candidates += 1
            print(f"   ✅ Candidat valide - Email serait envoyé")
        else:
            inconnu_candidates += 1
            print(f"   ❌ Candidat invalide (INCONNU) - Email échouerait")
    
    print(f"\nRÉSULTATS SIMULATION:")
    print(f"   Total testé: 10 candidats")
    print(f"   Candidats valides: {valid_candidates}")
    print(f"   Candidats INCONNU: {inconnu_candidates}")
    
    # Test avec tous les candidats
    all_valid = 0
    all_inconnu = 0
    for candidate_id, candidate_info in registry.items():
        nom = candidate_info.get('nom', 'INCONNU')
        email = candidate_info.get('email', 'N/A')
        
        if nom != 'INCONNU' and email != 'N/A':
            all_valid += 1
        else:
            all_inconnu += 1
    
    print(f"\nSTATUT COMPLET ({len(registry)} candidats):")
    print(f"   Candidats valides: {all_valid}")
    print(f"   Candidats INCONNU: {all_inconnu}")
    
    if all_inconnu == 0:
        print("\n🎉 SUCCÈS: Tous les candidats ont des noms valides!")
        print("   L'interface devrait maintenant fonctionner correctement.")
    else:
        print(f"\n⚠️ PROBLÈME: {all_inconnu} candidats sont encore INCONNU")
    
    return all_valid

if __name__ == "__main__":
    simulate_interface_email_function()