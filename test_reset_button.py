#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test du bouton Reset - Vérification des fonctionnalités de remise à zéro
"""

import os
import json
import tempfile
import shutil
from pathlib import Path

def create_test_files():
    """Crée des fichiers de test pour simuler une application utilisée"""
    
    print("🎯 CRÉATION DE FICHIERS DE TEST...")
    
    # Créer dossier output avec contenu
    os.makedirs("output", exist_ok=True)
    
    # Créer quelques PDFs de test
    test_pdfs = [
        "output/convocation_TCF_DUPONT_Jean_a1b2c3.pdf",
        "output/convocation_TCF_MARTIN_Marie_d4e5f6.pdf"
    ]
    
    for pdf_path in test_pdfs:
        with open(pdf_path, 'w') as f:
            f.write("PDF de test")
        print(f"   📄 Créé: {pdf_path}")
    
    # Créer registre de candidats
    registry = {
        "a1b2c3": {
            "nom": "DUPONT",
            "prenom": "Jean", 
            "email": "jean.dupont@test.com",
            "pdf_filename": "convocation_TCF_DUPONT_Jean_a1b2c3.pdf"
        },
        "d4e5f6": {
            "nom": "MARTIN",
            "prenom": "Marie",
            "email": "marie.martin@test.com", 
            "pdf_filename": "convocation_TCF_MARTIN_Marie_d4e5f6.pdf"
        }
    }
    
    with open("output/candidate_pdf_registry.json", 'w', encoding='utf-8') as f:
        json.dump(registry, f, indent=2, ensure_ascii=False)
    print("   📊 Créé: output/candidate_pdf_registry.json")
    
    # Créer configurations email de test
    configs = {
        "mailjet_config.json": {"api_key": "test_key", "configured": True},
        "oauth_credentials.json": {"client_id": "test_oauth", "configured": True},
        "graphics_config.json": {"logo_af": "test_logo.png", "configured": True}
    }
    
    for config_name, config_data in configs.items():
        with open(config_name, 'w', encoding='utf-8') as f:
            json.dump(config_data, f, indent=2)
        print(f"   ⚙️ Créé: {config_name}")
    
    # Créer logs de test
    logs = [
        "convocation_generator.log",
        "auto_decrepit_fix.log",
        "registry_report.txt"
    ]
    
    for log_file in logs:
        with open(log_file, 'w', encoding='utf-8') as f:
            f.write("Log de test\nContenu test\n")
        print(f"   📝 Créé: {log_file}")
    
    print(f"✅ FICHIERS DE TEST CRÉÉS")
    print(f"   📂 Dossier output: {len(os.listdir('output')) if os.path.exists('output') else 0} fichiers")
    print(f"   ⚙️ Configs: {len([f for f in configs.keys() if os.path.exists(f)])} fichiers")
    print(f"   📝 Logs: {len([f for f in logs if os.path.exists(f)])} fichiers")

def check_reset_effectiveness():
    """Vérifie si le reset a bien tout supprimé"""
    
    print("\n🔍 VÉRIFICATION POST-RESET...")
    
    # Fichiers qui doivent être supprimés
    files_to_check = [
        "mailjet_config.json",
        "oauth_credentials.json", 
        "graphics_config.json",
        "convocation_generator.log",
        "auto_decrepit_fix.log",
        "registry_report.txt",
        "candidate_pdf_registry.json"
    ]
    
    remaining_files = []
    for file_path in files_to_check:
        if os.path.exists(file_path):
            remaining_files.append(file_path)
    
    # Vérifier dossier output
    output_empty = True
    if os.path.exists("output"):
        output_contents = os.listdir("output")
        if output_contents:
            output_empty = False
            remaining_files.extend([f"output/{f}" for f in output_contents])
    
    if remaining_files:
        print("❌ RESET INCOMPLET - Fichiers restants:")
        for file_path in remaining_files:
            print(f"   🚫 {file_path}")
        return False
    else:
        print("✅ RESET COMPLET RÉUSSI")
        print("   🧹 Tous les fichiers ont été supprimés")
        print("   📂 Dossier output est vide")
        return True

def simulate_reset_scenario():
    """Simule un scénario complet de test du reset"""
    
    print("=" * 60)
    print("🧪 TEST DU BOUTON RESET - SIMULATION COMPLÈTE")
    print("=" * 60)
    
    # 1. Créer environnement de test
    create_test_files()
    
    print(f"\n📋 ÉTAT AVANT RESET:")
    print(f"   📂 Dossier output existe: {os.path.exists('output')}")
    print(f"   📊 Registre existe: {os.path.exists('output/candidate_pdf_registry.json') if os.path.exists('output') else False}")
    print(f"   ⚙️ Config Mailjet existe: {os.path.exists('mailjet_config.json')}")
    print(f"   🎨 Config graphique existe: {os.path.exists('graphics_config.json')}")
    
    # 2. Message pour utilisateur  
    print(f"\n🎯 PRÊT POUR LE TEST!")
    print(f"   1. Lancez l'application: python main.py")
    print(f"   2. Cliquez sur le bouton '🔄 RESET COMPLET'")
    print(f"   3. Confirmez les 2 boîtes de dialogue")
    print(f"   4. Revenez ici et tapez 'Entrée' pour vérifier")
    
    # Attendre que l'utilisateur teste
    input("\n⏳ Appuyez sur Entrée après avoir testé le reset...")
    
    # 3. Vérifier résultats
    success = check_reset_effectiveness()
    
    print(f"\n📊 RÉSULTAT DU TEST:")
    if success:
        print(f"🎉 SUCCÈS TOTAL! Le bouton reset fonctionne parfaitement!")
        print(f"   ✅ Toutes les données ont été supprimées")
        print(f"   ✅ L'application est revenue à l'état initial")
        print(f"   ✅ Fonctionnalité opérationnelle à 100%")
    else:
        print(f"⚠️ PROBLÈME DÉTECTÉ! Certains fichiers n'ont pas été supprimés")
        print(f"   🔧 Vérifiez les permissions de fichiers")
        print(f"   🔧 Certains fichiers étaient peut-être en cours d'utilisation")
    
    print(f"\n💡 CONSEILS D'UTILISATION:")
    print(f"   • Le reset supprime DÉFINITIVEMENT toutes les données")
    print(f"   • Utilisez-le pour repartir de zéro proprement")
    print(f"   • Idéal avant une nouvelle configuration")
    print(f"   • Parfait pour résoudre les problèmes de configuration")

if __name__ == "__main__":
    try:
        simulate_reset_scenario()
    except KeyboardInterrupt:
        print(f"\n⏹️ Test interrompu par l'utilisateur")
    except Exception as e:
        print(f"\n❌ Erreur pendant le test: {e}")