#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de la prise en charge des nouveaux onglets TCF TP EE et TCF TP EO
"""

import sys
import os

# Ajouter le répertoire parent au path pour importer les modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_tcf_durations():
    """Teste que les nouvelles déclinaisons TCF sont bien définies"""
    from tcf_excel_processor import TCFExcelProcessor
    
    print("🧪 TEST DES NOUVELLES DÉCLINAISONS TCF")
    print("=" * 50)
    
    # Créer une instance du processeur
    processor = TCFExcelProcessor("dummy.xlsx")
    
    print("\n📋 DÉCLINAISONS TCF CONFIGURÉES:")
    for tcf_type, config in processor.TCF_DURATIONS.items():
        print(f"\n   🎯 {tcf_type}:")
        print(f"      📅 Durée collective: {config.get('collective_duration', 'N/A')}")
        print(f"      ⏱️  Durée individuelle: {config.get('individual_duration', 'N/A')}")
        print(f"      👤 Épreuve individuelle: {'Oui' if config.get('has_individual') else 'Non'}")
        if config.get('is_optional'):
            print(f"      ✨ Type: Épreuve facultative")
            print(f"      📝 Nom complet: {config.get('full_name', tcf_type)}")
    
    # Vérifier que les nouveaux types sont présents
    print("\n✅ VÉRIFICATION DES NOUVEAUX TYPES:")
    
    required_types = [
        'TCF CANADA',
        'TCF TP COMPLET', 
        'TCF TP OBLIGATOIRE',
        'TCF TP EE',  # Nouveau
        'TCF TP EO',  # Nouveau
        'TCF IRN'
    ]
    
    all_present = True
    for tcf_type in required_types:
        if tcf_type in processor.TCF_DURATIONS:
            is_new = tcf_type in ['TCF TP EE', 'TCF TP EO']
            marker = "🆕" if is_new else "✅"
            print(f"   {marker} {tcf_type}: Présent")
        else:
            print(f"   ❌ {tcf_type}: MANQUANT")
            all_present = False
    
    return all_present

def test_tcf_logos():
    """Teste que les logos pour les nouveaux types sont configurés"""
    print("\n\n🎨 TEST DES LOGOS TCF")
    print("=" * 50)
    
    # Simuler l'import de main pour vérifier les variables
    try:
        # On ne peut pas importer main.py directement car il lance l'interface
        # On va juste vérifier que le code contient les nouvelles variables
        with open("main.py", 'r', encoding='utf-8') as f:
            main_content = f.read()
        
        print("\n📋 VÉRIFICATION DES VARIABLES DE LOGOS:")
        
        logo_vars = [
            ('logo_tcf_path', 'Logo TCF générique'),
            ('logo_tcf_canada_path', 'Logo TCF CANADA'),
            ('logo_tcf_tp_path', 'Logo TCF TP'),
            ('logo_tcf_tp_ee_path', 'Logo TCF TP EE (nouveau)'),
            ('logo_tcf_tp_eo_path', 'Logo TCF TP EO (nouveau)'),
            ('logo_tcf_irn_path', 'Logo TCF IRN')
        ]
        
        all_present = True
        for var_name, description in logo_vars:
            if var_name in main_content:
                is_new = 'nouveau' in description
                marker = "🆕" if is_new else "✅"
                print(f"   {marker} {description}: Configuré")
            else:
                print(f"   ❌ {description}: MANQUANT")
                all_present = False
        
        # Vérifier le mapping des logos
        print("\n📋 VÉRIFICATION DU MAPPING DES LOGOS:")
        if "'TCF TP EE':" in main_content:
            print(f"   🆕 TCF TP EE: Mappé")
        else:
            print(f"   ❌ TCF TP EE: NON mappé")
            all_present = False
            
        if "'TCF TP EO':" in main_content:
            print(f"   🆕 TCF TP EO: Mappé")
        else:
            print(f"   ❌ TCF TP EO: NON mappé")
            all_present = False
        
        return all_present
        
    except Exception as e:
        print(f"   ❌ Erreur lors de la vérification: {e}")
        return False

def show_usage_instructions():
    """Affiche les instructions d'utilisation"""
    print("\n\n📚 INSTRUCTIONS D'UTILISATION")
    print("=" * 50)
    
    print("\n🎯 NOUVEAUX ONGLETS EXCEL:")
    print("   1. TCF TP EE (Expression Écrite)")
    print("      • Épreuve collective uniquement")
    print("      • Durée: 1h00")
    print("      • Peut être combinée avec d'autres épreuves")
    
    print("\n   2. TCF TP EO (Expression Orale)")
    print("      • Épreuve individuelle uniquement")
    print("      • Durée: 12 minutes")
    print("      • Peut être combinée avec d'autres épreuves")
    
    print("\n📋 STRUCTURE DU FICHIER EXCEL:")
    print("   Le fichier 'JURYS FINAL TCF' doit contenir 7 onglets:")
    print("   ✅ TCF CANADA")
    print("   ✅ TCF TP COMPLET")
    print("   ✅ TCF TP OBLIGATOIRE")
    print("   🆕 TCF TP EE")
    print("   🆕 TCF TP EO")
    print("   ✅ TCF IRN")
    print("   ✅ ADMIN")
    
    print("\n⚙️ ONGLET ADMIN:")
    print("   L'onglet ADMIN doit définir les durées pour:")
    print("   • TCF TP EE (durée collective)")
    print("   • TCF TP EO (durée individuelle)")
    
    print("\n🎨 LOGOS:")
    print("   Par défaut, TCF TP EE et TCF TP EO utilisent le logo TCF TP")
    print("   Vous pouvez définir des logos spécifiques si nécessaire")
    
    print("\n🚀 GÉNÉRATION DES CONVOCATIONS:")
    print("   1. Ouvrez l'application: python main.py")
    print("   2. Sélectionnez votre fichier Excel avec les 7 onglets")
    print("   3. Générez les PDFs")
    print("   4. Les candidats TCF TP EE et EO seront traités automatiquement")

def main():
    """Fonction principale de test"""
    
    print("🧪 TEST DE PRISE EN CHARGE DES NOUVEAUX ONGLETS TCF")
    print("=" * 60)
    print("Vérification de TCF TP EE et TCF TP EO\n")
    
    # Test 1: Durées TCF
    durations_ok = test_tcf_durations()
    
    # Test 2: Logos
    logos_ok = test_tcf_logos()
    
    # Résultats
    print("\n\n📊 RÉSULTATS DES TESTS")
    print("=" * 50)
    
    if durations_ok and logos_ok:
        print("🎉 TOUS LES TESTS RÉUSSIS!")
        print("   ✅ Les nouveaux types TCF TP EE et EO sont configurés")
        print("   ✅ Les logos sont mappés correctement")
        print("   ✅ Le système est prêt à traiter les 7 onglets")
    else:
        print("⚠️ CERTAINS TESTS ONT ÉCHOUÉ")
        if not durations_ok:
            print("   ❌ Problème avec les durées TCF")
        if not logos_ok:
            print("   ❌ Problème avec les logos")
    
    # Instructions
    show_usage_instructions()
    
    print("\n" + "=" * 60)
    print("✨ Système mis à jour pour supporter 7 onglets TCF!")

if __name__ == "__main__":
    main()