"""
Test de débogage Gmail OAuth2
Diagnostic complet du problème d'authentification
"""

import json
import os
from gmail_oauth import GmailOAuthAuthenticator
from gmail_email_sender import GmailEmailSender

def test_gmail_complete():
    """Test complet Gmail OAuth2 avec débogage"""
    print("🔍 DIAGNOSTIC GMAIL OAUTH2")
    print("=" * 60)
    
    # Vérifier la configuration
    print("1. Vérification de la configuration...")
    if os.path.exists('gmail_config.json'):
        with open('gmail_config.json', 'r') as f:
            config = json.load(f)
            print(f"   ✅ Client ID: {config['client_id'][:20]}...{config['client_id'][-10:]}")
            print(f"   ✅ Client Secret: {config['client_secret'][:10]}...")
    else:
        print("   ❌ Fichier gmail_config.json manquant")
        return
    
    # Test d'authentification
    print("\n2. Test d'authentification...")
    try:
        auth = GmailOAuthAuthenticator()
        print("   ✅ Authenticator créé")
        
        # Forcer une nouvelle authentification
        result = auth.authenticate_with_gmail()
        
        if result['success']:
            print(f"   ✅ Authentification réussie!")
            print(f"   📧 Email: {result['email']}")
            print(f"   🔑 Token: {result['access_token'][:20]}...")
            
            # Test de l'API Gmail
            print("\n3. Test de l'API Gmail...")
            sender = GmailEmailSender()
            
            # Test de connexion
            test_result = sender.test_connection(result['access_token'])
            
            if test_result['success']:
                print(f"   ✅ Connexion Gmail API réussie!")
                print(f"   📧 Email confirmé: {test_result['email']}")
                print(f"   📊 Messages totaux: {test_result['messages_total']}")
                
                # Test d'envoi d'email simple
                print("\n4. Test d'envoi d'email...")
                email_result = sender.send_email_with_attachment(
                    access_token=result['access_token'],
                    to_email=result['email'],  # S'envoyer à soi-même
                    subject="Test Gmail OAuth2 - Générateur Convocations",
                    body="<html><body><h2>Test réussi!</h2><p>Votre configuration Gmail OAuth2 fonctionne parfaitement.</p></body></html>"
                )
                
                if email_result['success']:
                    print(f"   ✅ Email de test envoyé avec succès!")
                    print(f"   📧 ID du message: {email_result['message_id']}")
                    print(f"\n🎉 TOUT FONCTIONNE PARFAITEMENT!")
                    return True
                else:
                    print(f"   ❌ Erreur envoi email: {email_result['error']}")
                    
            else:
                print(f"   ❌ Erreur connexion Gmail API: {test_result['error']}")
                
        else:
            print(f"   ❌ Erreur authentification: {result['error']}")
            
    except Exception as e:
        print(f"   ❌ Exception: {str(e)}")
        import traceback
        traceback.print_exc()
    
    return False

def test_main_app_integration():
    """Test de l'intégration avec l'application principale"""
    print("\n" + "=" * 60)
    print("🔍 TEST INTÉGRATION APPLICATION PRINCIPALE")
    print("=" * 60)
    
    try:
        # Simuler l'authentification depuis main.py
        from gmail_oauth import GmailOAuthAuthenticator
        from gmail_email_sender import GmailEmailSender
        
        print("1. Création des objets...")
        gmail_auth = GmailOAuthAuthenticator()
        gmail_sender = GmailEmailSender()
        print("   ✅ Objets créés")
        
        print("2. Test d'authentification...")
        result = gmail_auth.authenticate_with_gmail()
        
        if result and result['success']:
            print(f"   ✅ Authentification OK: {result['email']}")
            
            # Simuler ce que fait main.py
            oauth_auth_result = result
            oauth_email_sender = gmail_sender
            
            print("3. Test variables d'état...")
            print(f"   ✅ oauth_auth_result: {bool(oauth_auth_result)}")
            print(f"   ✅ oauth_email_sender: {bool(oauth_email_sender)}")
            print(f"   ✅ access_token: {oauth_auth_result['access_token'][:20]}...")
            
            print("\n🎉 INTÉGRATION MAIN.PY OK!")
            return True
            
        else:
            print(f"   ❌ Échec authentification: {result.get('error', 'Erreur inconnue')}")
            
    except Exception as e:
        print(f"   ❌ Erreur intégration: {str(e)}")
        import traceback
        traceback.print_exc()
    
    return False

if __name__ == "__main__":
    print("🚀 DÉMARRAGE DU DIAGNOSTIC GMAIL OAUTH2")
    print("=" * 70)
    
    # Test complet
    success1 = test_gmail_complete()
    
    # Test intégration
    success2 = test_main_app_integration()
    
    print("\n" + "=" * 70)
    print("📋 RÉSUMÉ DU DIAGNOSTIC")
    print("=" * 70)
    print(f"Gmail OAuth2 complet: {'✅ OK' if success1 else '❌ ÉCHEC'}")
    print(f"Intégration main.py: {'✅ OK' if success2 else '❌ ÉCHEC'}")
    
    if success1 and success2:
        print("\n🎉 TOUT FONCTIONNE! Le problème est ailleurs.")
    else:
        print("\n🔧 PROBLÈME IDENTIFIÉ! Voir les détails ci-dessus.")
    
    print("\n🏁 Diagnostic terminé.")
