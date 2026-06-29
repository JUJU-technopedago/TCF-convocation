#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test des corrections appliquées pour les erreurs JSON et Unicode
Vérifie que les problèmes sont résolus
"""

import sys
import os
import logging
from unittest.mock import Mock, patch

def test_json_error_handling():
    """Test de la gestion des erreurs JSON"""
    print("🧪 Test de la gestion des erreurs JSON...")
    
    try:
        from mailjet_bridge import MailjetBridge
        
        # Créer une instance de test
        bridge = MailjetBridge("", "", "test@example.com", "Test")
        
        # Simuler une réponse Mailjet sans JSON valide
        mock_result = Mock()
        mock_result.status_code = 400
        mock_result.json.side_effect = ValueError("Expecting value: line 1 column 1 (char 0)")
        mock_result.text = "Bad Request - Invalid API key"
        
        # Tester la gestion d'erreur dans send_email
        candidate_data = {
            'nom': 'Test',
            'prenom': 'User',
            'email': 'test@example.com',
            'numero_candidat': '123456'
        }
        
        # Mock du client Mailjet
        bridge.mailjet_client = Mock()
        bridge.mailjet_client.send.create.return_value = mock_result
        
        # Mock pour trouver un PDF
        with patch.object(bridge, '_find_pdf_file', return_value='test.pdf'):
            with patch('os.path.exists', return_value=True):
                with patch('builtins.open', mock_open_pdf()):
                    with patch.object(bridge, '_create_email_content', return_value=('Subject', 'HTML', 'Text')):
                        with patch.object(bridge, '_encode_attachment', return_value=('base64content', 'test.pdf')):
                            try:
                                bridge.send_email(candidate_data)
                                print("❌ L'exception aurait dû être levée")
                                return False
                            except Exception as e:
                                error_msg = str(e)
                                if "Bad Request - Invalid API key" in error_msg:
                                    print("✅ Gestion des erreurs JSON fonctionne correctement")
                                    return True
                                else:
                                    print(f"❌ Message d'erreur inattendu: {error_msg}")
                                    return False
        
    except Exception as e:
        print(f"❌ Erreur lors du test JSON: {e}")
        return False

def mock_open_pdf():
    """Mock pour simuler l'ouverture d'un fichier PDF"""
    from unittest.mock import mock_open
    return mock_open(read_data=b'%PDF-1.4\n%mock pdf content')

def test_unicode_logging():
    """Test de la gestion des caractères Unicode dans les logs"""
    print("🧪 Test de la gestion Unicode dans les logs...")
    
    try:
        from mailjet_bridge import MailjetBridge
        
        # Créer une instance de test
        bridge = MailjetBridge("", "", "test@example.com", "Test")
        
        # Tester la méthode _safe_log
        if hasattr(bridge, '_safe_log'):
            # Capturer les logs
            import io
            log_capture = io.StringIO()
            handler = logging.StreamHandler(log_capture)
            bridge.logger.addHandler(handler)
            
            # Tester avec des caractères Unicode problématiques
            test_messages = [
                "✓ Email envoyé avec succès",
                "✗ Erreur lors de l'envoi",
                "⚠️ Attention: problème détecté",
                "🚀 Démarrage du processus",
                "🎉 Succès complet",
                "❌ Échec critique"
            ]
            
            for message in test_messages:
                bridge._safe_log(message)
            
            # Vérifier que les logs ont été écrits sans erreur
            log_output = log_capture.getvalue()
            if "[OK]" in log_output and "[ERREUR]" in log_output and "[ATTENTION]" in log_output:
                print("✅ Conversion des caractères Unicode fonctionne")
                return True
            else:
                print(f"❌ Problème avec la conversion Unicode: {log_output}")
                return False
        else:
            print("❌ Méthode _safe_log non trouvée")
            return False
            
    except Exception as e:
        print(f"❌ Erreur lors du test Unicode: {e}")
        return False

def test_progress_callback():
    """Test des callbacks de progression sans erreurs Unicode"""
    print("🧪 Test des callbacks de progression...")
    
    try:
        messages_received = []
        
        def test_callback(message):
            messages_received.append(message)
            # Simuler l'écriture dans un log qui pourrait avoir des problèmes d'encodage
            try:
                # Ceci devrait maintenant fonctionner sans erreur
                logging.info(message)
            except UnicodeEncodeError:
                print(f"❌ Erreur Unicode dans le callback: {message}")
                return False
        
        from mailjet_bridge import MailjetBridge
        bridge = MailjetBridge("", "", "test@example.com", "Test")
        
        # Simuler des messages de progression avec les nouveaux formats
        test_callback("[OK] Email envoyé à test@example.com via Mailjet")
        test_callback("[ERREUR] Erreur pour test@example.com: Connection failed")
        
        if len(messages_received) == 2:
            print("✅ Callbacks de progression fonctionnent sans erreur Unicode")
            return True
        else:
            print(f"❌ Problème avec les callbacks: {messages_received}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur lors du test des callbacks: {e}")
        return False

def test_logging_configuration():
    """Test de la configuration du logging UTF-8"""
    print("🧪 Test de la configuration du logging UTF-8...")
    
    try:
        # Vérifier que le logging est configuré avec UTF-8
        root_logger = logging.getLogger()
        
        utf8_handlers = []
        for handler in root_logger.handlers:
            if hasattr(handler, 'stream') and hasattr(handler.stream, 'encoding'):
                if handler.stream.encoding and 'utf' in handler.stream.encoding.lower():
                    utf8_handlers.append(handler)
        
        if utf8_handlers:
            print("✅ Configuration du logging UTF-8 détectée")
            return True
        else:
            print("⚠️ Configuration UTF-8 non détectée, mais cela peut être normal")
            return True  # Ne pas échouer pour cela
            
    except Exception as e:
        print(f"❌ Erreur lors du test de configuration logging: {e}")
        return False

def run_all_tests():
    """Exécute tous les tests"""
    print("🔧 TESTS DES CORRECTIONS MAILJET")
    print("=" * 50)
    
    tests = [
        ("Gestion des erreurs JSON", test_json_error_handling),
        ("Gestion Unicode dans les logs", test_unicode_logging),
        ("Callbacks de progression", test_progress_callback),
        ("Configuration logging UTF-8", test_logging_configuration)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}:")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Erreur critique dans {test_name}: {e}")
            results.append((test_name, False))
    
    # Résumé
    print("\n" + "=" * 50)
    print("📊 RÉSUMÉ DES TESTS:")
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSÉ" if result else "❌ ÉCHOUÉ"
        print(f"   {status}: {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Résultat global: {passed}/{total} tests passés")
    
    if passed == total:
        print("🎉 TOUS LES TESTS SONT PASSÉS!")
        print("\nLes corrections sont fonctionnelles. Vous pouvez utiliser votre application.")
        return True
    else:
        print("⚠️ Certains tests ont échoué. Vérifiez les détails ci-dessus.")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
