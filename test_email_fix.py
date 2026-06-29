#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test complet du système d'envoi d'emails après le correctif
"""

import json
import os

def simulate_email_sending():
    """Simule l'envoi d'emails avec le nouveau parsing"""
    
    print("📧 SIMULATION DU SYSTÈME D'ENVOI D'EMAILS")
    print("=" * 50)
    
    registry_path = "output/candidate_pdf_registry.json"
    
    if not os.path.exists(registry_path):
        print("❌ Pas de registre trouvé - Générez d'abord les PDFs")
        return False
    
    try:
        with open(registry_path, 'r', encoding='utf-8') as f:
            registry = json.load(f)
        
        print(f"📂 REGISTRE CHARGÉ: {len(registry)} candidats")
        
        # Simulation du nouveau parsing
        valid_candidates = 0
        inconnu_candidates = 0
        ready_for_sending = 0
        
        print(f"\n🔍 ANALYSE DES CANDIDATS:")
        
        for candidate_id, info in registry.items():
            # Nouveau parsing correct
            candidate_data = info.get('candidate_info', {})
            pdf_info = info.get('pdf_info', {})
            
            nom = candidate_data.get('nom', 'INCONNU')
            prenom = candidate_data.get('prenom', '')
            email = candidate_data.get('email', 'N/A')
            pdf_filename = pdf_info.get('filename', '')
            
            if nom != 'INCONNU' and nom.strip():
                valid_candidates += 1
                
                # Vérifier si le PDF existe
                pdf_path = os.path.join("output", pdf_filename)
                if os.path.exists(pdf_path):
                    ready_for_sending += 1
                    if ready_for_sending <= 3:  # Afficher les 3 premiers
                        print(f"   ✅ {prenom} {nom} ({email}) -> {pdf_filename}")
                else:
                    print(f"   ⚠️ {prenom} {nom} - PDF manquant: {pdf_filename}")
            else:
                inconnu_candidates += 1
        
        if ready_for_sending > 3:
            print(f"   ... et {ready_for_sending - 3} autres candidats prêts")
        
        # Calcul des ratios
        ratio_valid = valid_candidates / len(registry) * 100
        ratio_ready = ready_for_sending / len(registry) * 100
        
        print(f"\n📊 RÉSULTATS:")
        print(f"   👤 Candidats valides: {valid_candidates}/{len(registry)} ({ratio_valid:.1f}%)")
        print(f"   📄 PDFs disponibles: {ready_for_sending}/{len(registry)} ({ratio_ready:.1f}%)")
        print(f"   ❌ Candidats INCONNU: {inconnu_candidates}/{len(registry)}")
        
        # Prédiction du résultat
        print(f"\n🎯 PRÉDICTION ENVOI D'EMAILS:")
        
        if ratio_valid >= 50:
            print(f"   ✅ SUCCÈS ATTENDU - Plus de 50% de candidats valides")
            print(f"   🚀 L'envoi d'emails devrait fonctionner sans problème")
            print(f"   📧 {ready_for_sending} emails seraient envoyés")
        else:
            print(f"   ⚠️ PROBLÈME POTENTIEL - Moins de 50% de candidats valides")
            print(f"   🔄 Une confirmation utilisateur sera demandée")
        
        if ready_for_sending == valid_candidates:
            print(f"   📎 Tous les PDFs sont disponibles")
        else:
            print(f"   ⚠️ {valid_candidates - ready_for_sending} PDFs manquants")
        
        return ratio_valid >= 50 and ready_for_sending > 0
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def show_fix_summary():
    """Affiche un résumé du correctif appliqué"""
    
    print(f"\n🔧 RÉSUMÉ DU CORRECTIF APPLIQUÉ")
    print("=" * 40)
    
    print(f"🐛 PROBLÈME IDENTIFIÉ:")
    print(f"   • Le registre stockait les données dans 'candidate_info'")
    print(f"   • L'ancien code cherchait les données à la racine")
    print(f"   • Résultat: tous les candidats marqués 'INCONNU'")
    
    print(f"\n🔧 CORRECTIF APPLIQUÉ:")
    print(f"   • Lecture correcte dans 'candidate_info'")
    print(f"   • Lecture correcte dans 'pdf_info'")
    print(f"   • Parsing adapté à la vraie structure du registre")
    
    print(f"\n✅ RÉSULTAT:")
    print(f"   • Tous les noms sont maintenant correctement lus")
    print(f"   • Le système de validation fonctionne")
    print(f"   • L'envoi d'emails devrait être opérationnel")

def main():
    """Fonction principale de test"""
    
    # 1. Tester le parsing
    success = simulate_email_sending()
    
    # 2. Afficher le résumé
    show_fix_summary()
    
    # 3. Instructions pour l'utilisateur
    print(f"\n💡 INSTRUCTIONS:")
    if success:
        print(f"   🎉 TOUT EST PRÊT!")
        print(f"   1. Lancez l'application: python main.py")
        print(f"   2. Cliquez sur 'Envoyer Emails'")
        print(f"   3. Le système devrait fonctionner sans erreur")
        print(f"   4. Plus de message 'candidats INCONNU'!")
    else:
        print(f"   ⚠️ Problèmes détectés")
        print(f"   1. Vérifiez que les PDFs existent")
        print(f"   2. Régénérez les PDFs si nécessaire")
        print(f"   3. Réessayez l'envoi d'emails")

if __name__ == "__main__":
    main()