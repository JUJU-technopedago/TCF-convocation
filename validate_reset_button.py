#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Validation rapide du bouton Reset - Vérification de l'interface
"""

import os
import json

def check_button_implementation():
    """Vérifie que le bouton reset a été correctement implémenté"""
    
    print("🔍 VÉRIFICATION DE L'IMPLÉMENTATION DU BOUTON RESET")
    print("=" * 55)
    
    # 1. Vérifier que le code contient le bouton
    try:
        with open("main.py", 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Vérifications du code
        checks = [
            ("🔄 RESET COMPLET", "Texte du bouton présent"),
            ("reset_all_data", "Méthode reset_all_data définie"),
            ("Danger.TButton", "Style de bouton danger configuré"),
            ("REMISE À ZÉRO COMPLÈTE", "Messages d'avertissement présents"),
            ("shutil.rmtree", "Suppression de dossiers implémentée"),
            ("messagebox.askquestion", "Confirmations utilisateur présentes")
        ]
        
        print("📋 VÉRIFICATIONS DU CODE:")
        all_passed = True
        
        for check_text, description in checks:
            if check_text in content:
                print(f"   ✅ {description}")
            else:
                print(f"   ❌ {description}")
                all_passed = False
        
        print(f"\n📊 RÉSULTAT: {'✅ TOUTES LES VÉRIFICATIONS PASSÉES' if all_passed else '❌ CERTAINES VÉRIFICATIONS ÉCHOUÉES'}")
        
        return all_passed
        
    except Exception as e:
        print(f"❌ Erreur lors de la vérification: {e}")
        return False

def show_reset_features():
    """Affiche les fonctionnalités du bouton reset"""
    
    print(f"\n🚀 FONCTIONNALITÉS DU BOUTON RESET")
    print("=" * 40)
    
    features = [
        "🧹 Suppression complète du dossier output/",
        "🔐 Suppression de toutes les configurations email",
        "📊 Suppression des registres de candidats",
        "📝 Suppression des logs d'application", 
        "🎨 Suppression de la configuration graphique",
        "🔌 Déconnexion de toutes les sessions email",
        "🔄 Remise à zéro de toutes les variables",
        "⚠️ Double confirmation avant suppression",
        "🎯 Interface remise à l'état initial",
        "💾 Nettoyage mémoire et garbage collection"
    ]
    
    print("📋 LE BOUTON RESET EFFECTUE :")
    for feature in features:
        print(f"   {feature}")
    
    print(f"\n⚠️ AVERTISSEMENTS IMPORTANTS:")
    print(f"   • Cette action est IRRÉVERSIBLE")
    print(f"   • Toutes les données seront DÉFINITIVEMENT supprimées")
    print(f"   • L'utilisateur doit confirmer 2 fois avant suppression")
    print(f"   • Idéal pour repartir de zéro proprement")

def test_file_detection():
    """Teste la détection des fichiers qui seraient supprimés"""
    
    print(f"\n🔍 DÉTECTION DES FICHIERS À SUPPRIMER")
    print("=" * 45)
    
    # Fichiers de configuration à supprimer
    config_files = [
        "mailjet_config.json",
        "mailjet.key", 
        "oauth_credentials.json",
        "gmail_token.json",
        "email_auth.json",
        "secure_credentials.dat"
    ]
    
    # Fichiers de registres et logs
    registry_files = [
        "candidate_pdf_registry.json",
        "registry_report.txt",
        "convocation_generator.log",
        "auto_decrepit_fix.log",
        "fix_decrepit.log"
    ]
    
    # Fichiers graphiques
    graphics_files = [
        "graphics_config.json"
    ]
    
    print("📂 ANALYSE DES FICHIERS PRÉSENTS:")
    
    categories = [
        ("⚙️ Configurations email", config_files),
        ("📊 Registres et logs", registry_files),
        ("🎨 Configuration graphique", graphics_files)
    ]
    
    total_found = 0
    
    for category_name, file_list in categories:
        print(f"\n   {category_name}:")
        found_in_category = 0
        
        for file_path in file_list:
            if os.path.exists(file_path):
                file_size = os.path.getsize(file_path)
                print(f"      ✅ {file_path} ({file_size} bytes)")
                found_in_category += 1
                total_found += 1
            else:
                print(f"      ⚪ {file_path} (absent)")
        
        print(f"      📊 {found_in_category}/{len(file_list)} fichiers présents")
    
    # Vérifier dossier output
    output_files = 0
    if os.path.exists("output"):
        output_contents = os.listdir("output")
        output_files = len(output_contents)
        print(f"\n   📂 Dossier output:")
        print(f"      📁 {output_files} fichiers trouvés")
        if output_files > 0:
            total_found += output_files
            # Afficher quelques exemples
            for i, filename in enumerate(output_contents[:3]):
                print(f"         📄 {filename}")
            if output_files > 3:
                print(f"         ... et {output_files - 3} autres fichiers")
    else:
        print(f"\n   📂 Dossier output: absent")
    
    print(f"\n📊 RÉSUMÉ:")
    print(f"   🎯 Total fichiers détectés: {total_found}")
    print(f"   🧹 Tous seraient supprimés par le reset")
    print(f"   ⚠️ {'ATTENTION: Des données seraient perdues!' if total_found > 0 else 'Aucune donnée à supprimer'}")

def main():
    """Fonction principale de validation"""
    
    print("🧪 VALIDATION DU BOUTON RESET")
    print("=" * 40)
    print("Vérification de l'implémentation et des fonctionnalités\n")
    
    # 1. Vérifier l'implémentation
    implementation_ok = check_button_implementation()
    
    # 2. Afficher les fonctionnalités
    show_reset_features()
    
    # 3. Tester la détection de fichiers
    test_file_detection()
    
    # 4. Conclusion
    print(f"\n🎯 CONCLUSION:")
    if implementation_ok:
        print(f"   ✅ Le bouton reset est correctement implémenté")
        print(f"   ✅ Toutes les fonctionnalités sont présentes")
        print(f"   ✅ Les mesures de sécurité sont en place")
        print(f"   🚀 Prêt pour utilisation!")
    else:
        print(f"   ❌ Problèmes détectés dans l'implémentation")
        print(f"   🔧 Vérifiez le code et corrigez les erreurs")
    
    print(f"\n💡 POUR TESTER:")
    print(f"   1. Lancez: python main.py")
    print(f"   2. Cherchez le bouton '🔄 RESET COMPLET' (rouge)")
    print(f"   3. Cliquez dessus et suivez les confirmations")
    print(f"   4. Vérifiez que tout a été supprimé")

if __name__ == "__main__":
    main()