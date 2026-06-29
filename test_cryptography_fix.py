#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test complet de la correction de l'erreur cryptography CAST5
"""

import sys
import traceback

def test_cryptography_fix():
    """Test de la correction complète des modules cryptography"""
    print("🔧 TEST DE LA CORRECTION CRYPTOGRAPHY")
    print("=" * 50)
    
    # 1. Test du module de correction
    print("1. Test du module auto_decrepit_fix...")
    try:
        import auto_decrepit_fix
        fixer = auto_decrepit_fix.DefecratedImportFixer()
        print(f"   ✅ Module auto_decrepit_fix importé")
        
        # Obtenir la version de cryptography
        version = fixer.get_cryptography_version()
        print(f"   ✅ Version cryptography: {version}")
        
        # Appliquer la correction
        success = fixer.fix_decrepit_imports()
        print(f"   ✅ Correction appliquée: {success}")
        
    except Exception as e:
        print(f"   ❌ Erreur module auto_decrepit_fix: {e}")
        return False
    
    # 2. Test des importations individuelles
    print("\\n2. Test des importations individuelles...")
    
    algorithms_to_test = ['ARC4', 'TripleDES', 'RC2', 'CAST5']
    
    for algorithm in algorithms_to_test:
        try:
            exec(f"from cryptography.hazmat.decrepit.ciphers.algorithms import {algorithm}")
            print(f"   ✅ {algorithm}: importation réussie")
        except ImportError as e:
            print(f"   ❌ {algorithm}: échec importation - {e}")
            return False
        except Exception as e:
            print(f"   ⚠️  {algorithm}: autre erreur - {e}")
    
    # 3. Test de l'importation groupée
    print("\\n3. Test de l'importation groupée...")
    try:
        from cryptography.hazmat.decrepit.ciphers.algorithms import ARC4, TripleDES, RC2, CAST5
        print("   ✅ Importation groupée réussie")
    except ImportError as e:
        print(f"   ❌ Échec importation groupée: {e}")
        return False
    
    # 4. Test de création d'instances
    print("\\n4. Test de création d'instances...")
    try:
        # Test CAST5 spécifiquement (celui qui causait l'erreur)
        test_key = b"test_key_123456"
        cast5_instance = CAST5(test_key)
        print(f"   ✅ CAST5 instance créée avec clé de {cast5_instance.key_size} bits")
        
        # Test des autres
        arc4_instance = ARC4(test_key)
        print(f"   ✅ ARC4 instance créée avec clé de {arc4_instance.key_size} bits")
        
        rc2_instance = RC2(test_key)
        print(f"   ✅ RC2 instance créée avec clé de {rc2_instance.key_size} bits")
        
        tripledes_instance = TripleDES(test_key)
        print(f"   ✅ TripleDES instance créée avec clé de {tripledes_instance.key_size} bits")
        
    except Exception as e:
        print(f"   ❌ Erreur création instances: {e}")
        return False
    
    # 5. Test de l'application principale
    print("\\n5. Test de l'application principale...")
    try:
        # Tester l'import de main.py sans l'exécuter
        import main
        print("   ✅ Module main.py importé sans erreur")
    except Exception as e:
        print(f"   ❌ Erreur import main.py: {e}")
        return False
    
    return True

def test_application_launch():
    """Test du lancement de l'application"""
    print("\\n6. Test du lancement de l'application...")
    try:
        # Importer ConvocationGenerator
        from main import ConvocationGenerator
        
        # Créer une instance (sans afficher l'interface)
        app = ConvocationGenerator()
        print("   ✅ Application créée sans erreur cryptography")
        
        # Vérifier que l'application peut accéder à ses méthodes principales
        hasattr_checks = [
            'browse_excel_file',
            'browse_logo_af_file', 
            'browse_tcf_logo',
            '_generate_tcf_pdfs'
        ]
        
        for method_name in hasattr_checks:
            if hasattr(app, method_name):
                print(f"   ✅ Méthode {method_name} disponible")
            else:
                print(f"   ❌ Méthode {method_name} manquante")
                return False
        
        return True
        
    except Exception as e:
        print(f"   ❌ Erreur lancement application: {e}")
        traceback.print_exc()
        return False

def main():
    """Fonction principale de test"""
    try:
        success1 = test_cryptography_fix()
        success2 = test_application_launch()
        
        print("\\n" + "=" * 60)
        if success1 and success2:
            print("🎉 TOUS LES TESTS RÉUSSIS!")
            print("✅ L'erreur cryptography CAST5 est complètement corrigée")
            print("✅ L'application peut démarrer sans erreur")
            print("✅ Tous les algorithmes decrepit sont disponibles")
            print("\\n📋 Modules cryptography supportés:")
            print("   • ARC4")
            print("   • TripleDES") 
            print("   • RC2")
            print("   • CAST5 ⭐ (corrigé)")
            print("\\n🚀 L'application est prête à être utilisée!")
            return True
        else:
            print("❌ CERTAINS TESTS ONT ÉCHOUÉ")
            print("⚠️  L'erreur cryptography pourrait persister")
            return False
            
    except Exception as e:
        print(f"\\n💥 ERREUR CRITIQUE: {e}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)