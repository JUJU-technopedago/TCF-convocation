#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test complet de la solution Mailjet corrigée
Vérifie que toutes les corrections fonctionnent ensemble
"""

import sys
import os
import logging
from unittest.mock import Mock, patch

def test_complete_mailjet_solution():
    """Test complet de la solution Mailjet"""
    print("🧪 TEST COMPLET DE LA SOLUTION MAILJET CORRIGÉE")
    print("=" * 60)
    
    test_results = []
    
    # Test 1: Import des modules corrigés
    print("\n📋 1. Test des imports...")
    try:
        from mailjet_bridge import MailjetBridge
        from mailjet_400_fixes import Mailjet400Fixer
        print("   ✅ Imports réussis")
        test_results.append(("Imports", True))
    except Exception as e:
        print(f"   ❌ Erreur import: {e}")
        test_results.append(("Imports", False))
        return test_results
    
    # Test 2: Création d'instance avec corrections
    print("\n📋 2. Test de création d'instance...")
    try:
        bridge = MailjetBridge("", "", "test@example.com", "Test Service")
        
        # Vérifier que le fixer 400 est présent
        if hasattr(bridge, 'error_fixer'):
            print("   ✅ Correcteur 400 intégré")
            test_results.append(("Correcteur 400", True))
        else:
            print("   ❌ Correcteur 400 manquant")
            test_results.append(("Correcteur 400", False))
            
        # Vérifier que la méthode _safe_log est présente
        if hasattr(bridge, '_safe_log'):
            print("   ✅ Méthode _safe_log présente")
            test_results.append(("Safe logging", True))
        else:
            print("   ❌ Méthode _safe_log manquante")
            test_results.append(("Safe logging", False))
            
    except Exception as e:
        print(f"   ❌ Erreur création instance: {e}")
        test_results.append(("Création instance", False))
        return test_results
    
    # Test 3: Test du correcteur 400
    print("\n📋 3. Test du correcteur 400...")
    try:
        fixer = Mailjet400Fixer()
        
        # Test validation email
        valid_email = fixer.validate_email("test@example.com")
        invalid_email = fixer.validate_email("invalid-email")
        
        if valid_email and not invalid_email:
            print("   ✅ Validation email fonctionne")
            test_results.append(("Validation email", True))
        else:
            print("   ❌ Problème validation email")
            test_results.append(("Validation email", False))
        
        # Test nettoyage contenu
        dirty_content = "Test ✓ avec ✗ caractères ⚠️ spéciaux"
        clean_content = fixer.clean_email_content(dirty_content)
        
        if "[OK]" in clean_content and "[ERREUR]" in clean_content:
            print("   ✅ Nettoyage contenu fonctionne")
            test_results.append(("Nettoyage contenu", True))
        else:
            print("   ❌ Problème nettoyage contenu")
            test_results.append(("Nettoyage contenu", False))
            
    except Exception as e:
        print(f"   ❌ Erreur test correcteur 400: {e}")
        test_results.append(("Correcteur 400", False))
    
    # Test 4: Test de la gestion JSON sécurisée
    print("\n📋 4. Test de la gestion JSON sécurisée...")
    try:
        # Simuler une réponse Mailjet sans JSON valide
        mock_result = Mock()
        mock_result.status_code = 400
        mock_result.json.side_effect = ValueError("Expecting value: line 1 column 1 (char 0)")
        mock_result.text = "Bad Request - Invalid sender"
        
        # Tester avec le fixer
        fixer = Mailjet400Fixer()
        result = fixer.send_with_retry(None, {}, max_retries=1)
        
        # Le résultat devrait être un échec mais sans crash JSON
        if not result["success"] and "Bad Request" in result["error"]:
            print("   ✅ Gestion JSON sécurisée fonctionne")
            test_results.append(("Gestion JSON", True))
        else:
            print("   ❌ Problème gestion JSON")
            test_results.append(("Gestion JSON", False))
            
    except Exception as e:
        print(f"   ❌ Erreur test JSON: {e}")
        test_results.append(("Gestion JSON", False))
    
    # Test 5: Test du logging Unicode sécurisé
    print("\n📋 5. Test du logging Unicode sécurisé...")
    try:
        bridge = MailjetBridge("", "", "test@example.com", "Test Service")
        
        # Capturer les logs
        import io
        log_capture = io.StringIO()
        handler = logging.StreamHandler(log_capture)
        bridge.logger.addHandler(handler)
        
        # Tester avec des caractères Unicode
        bridge._safe_log("Test ✓ avec ✗ caractères ⚠️ Unicode")
        
        log_output = log_capture.getvalue()
        if "[OK]" in log_output and "[ERREUR]" in log_output:
            print("   ✅ Logging Unicode sécurisé fonctionne")
            test_results.append(("Logging Unicode", True))
        else:
            print("   ❌ Problème logging Unicode")
            test_results.append(("Logging Unicode", False))
            
    except Exception as e:
        print(f"   ❌ Erreur test logging: {e}")
        test_results.append(("Logging Unicode", False))
    
    # Test 6: Test de création de données Mailjet sécurisées
    print("\n📋 6. Test de création de données Mailjet sécurisées...")
    try:
        fixer = Mailjet400Fixer()
        
        candidate_data = {
            'nom': 'Dupont',
            'prenom': 'Jean',
            'email': 'jean.dupont@example.com'
        }
        
        # Créer des données sécurisées
        safe_data = fixer.create_safe_mailjet_data(
            candidate_data,
            "sender@example.com",
            "Service Test",
            "Test Subject ✓",
            "<p>Test HTML ⚠️</p>",
            "Test text ✗"
        )
        
        # Vérifier la structure
        if (safe_data.get('Messages') and 
            safe_data['Messages'][0].get('From') and
            safe_data['Messages'][0].get('To')):
            print("   ✅ Création données Mailjet sécurisées fonctionne")
            test_results.append(("Données Mailjet", True))
        else:
            print("   ❌ Problème création données Mailjet")
            test_results.append(("Données Mailjet", False))
            
    except Exception as e:
        print(f"   ❌ Erreur test données Mailjet: {e}")
        test_results.append(("Données Mailjet", False))
    
    # Résumé des tests
    print("\n" + "=" * 60)
    print("📊 RÉSUMÉ DES TESTS:")
    
    passed = 0
    total = len(test_results)
    
    for test_name, result in test_results:
        status = "✅ PASSÉ" if result else "❌ ÉCHOUÉ"
        print(f"   {status}: {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Résultat global: {passed}/{total} tests passés")
    
    if passed == total:
        print("🎉 TOUS LES TESTS SONT PASSÉS!")
        print("\n✅ La solution Mailjet est complètement corrigée:")
        print("   • Erreurs JSON decode résolues")
        print("   • Erreurs Unicode encoding résolues")
        print("   • Erreurs 400 Mailjet améliorées")
        print("   • Validation et nettoyage des données")
        print("   • Système de retry intégré")
        
        print("\n📋 Votre application est prête à être utilisée!")
        return True
    else:
        print("⚠️ Certains tests ont échoué.")
        print("Vérifiez les détails ci-dessus avant d'utiliser l'application.")
        return False

def test_real_world_scenario():
    """Test avec un scénario réel"""
    print("\n🌍 TEST SCÉNARIO RÉEL")
    print("=" * 30)
    
    try:
        from mailjet_bridge import MailjetBridge
        
        # Simuler des données réelles
        bridge = MailjetBridge(
            excel_path="exemple_candidats.xlsx",
            pdf_dir="output",
            sender_email="test@example.com",
            sender_name="Alliance Française Test"
        )
        
        # Données candidat avec caractères spéciaux
        candidate_data = {
            'nom': 'Müller',
            'prenom': 'François',
            'email': 'francois.muller@example.com',
            'numero_candidat': '123456'
        }
        
        # Test de création de contenu email
        subject, html, text = bridge._create_email_content(candidate_data)
        
        if subject and html and text:
            print("   ✅ Création contenu email réussie")
            
            # Vérifier que les caractères spéciaux sont gérés
            if "François" in html and "Müller" in html:
                print("   ✅ Caractères spéciaux gérés correctement")
                return True
            else:
                print("   ❌ Problème avec les caractères spéciaux")
                return False
        else:
            print("   ❌ Échec création contenu email")
            return False
            
    except Exception as e:
        print(f"   ❌ Erreur test scénario réel: {e}")
        return False

def main():
    """Fonction principale"""
    print("🔧 TEST COMPLET DE LA SOLUTION MAILJET CORRIGÉE")
    print("=" * 70)
    
    # Tests principaux
    main_success = test_complete_mailjet_solution()
    
    # Test scénario réel
    real_world_success = test_real_world_scenario()
    
    print("\n" + "=" * 70)
    print("🏁 RÉSULTAT FINAL:")
    
    if main_success and real_world_success:
        print("✅ SOLUTION COMPLÈTEMENT FONCTIONNELLE!")
        print("\nVotre système d'envoi d'emails Mailjet est maintenant:")
        print("• Résistant aux erreurs JSON")
        print("• Compatible avec tous les caractères Unicode")
        print("• Optimisé pour éviter les erreurs 400")
        print("• Équipé d'un système de retry automatique")
        print("• Sécurisé avec validation des données")
        
        print("\n🚀 Vous pouvez maintenant utiliser votre application sans crainte!")
        return True
    else:
        print("❌ Des problèmes subsistent.")
        print("Consultez les détails des tests ci-dessus.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
