"""
Test script for OAuth authentication system
Tests the complete OAuth flow including authentication and email sending
"""

import sys
import os

def test_oauth_authentication():
    """Test OAuth authentication dialog"""
    print("🧪 Test 1: OAuth Authentication Dialog")
    print("=" * 50)
    
    try:
        from oauth_login_dialog import OAuthLoginDialog
        
        print("Ouverture de la fenêtre d'authentification OAuth...")
        dialog = OAuthLoginDialog()
        result = dialog.show()
        
        if result and result['success']:
            print(f"✅ Authentification réussie!")
            print(f"   Email: {result['email']}")
            print(f"   Provider: {result['provider']}")
            print(f"   Token disponible: {'access_token' in result}")
            return result
        else:
            print("❌ Authentification annulée ou échouée")
            return None
            
    except Exception as e:
        print(f"❌ Erreur lors du test d'authentification: {e}")
        return None

def test_oauth_email_connection(auth_result):
    """Test OAuth email connection"""
    print("\n🧪 Test 2: Test de Connexion Email OAuth")
    print("=" * 50)
    
    try:
        from oauth_email_sender import OAuthEmailSender
        
        sender = OAuthEmailSender()
        
        print("Test de la connexion...")
        result = sender.test_connection(auth_result['access_token'])
        
        if result['success']:
            print(f"✅ Connexion réussie!")
            print(f"   Utilisateur: {result['display_name']}")
            print(f"   Email: {result['user_email']}")
            return True
        else:
            print(f"❌ Erreur de connexion: {result['error']}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur lors du test de connexion: {e}")
        return False

def test_oauth_email_sending(auth_result):
    """Test OAuth email sending"""
    print("\n🧪 Test 3: Envoi d'Email de Test OAuth")
    print("=" * 50)
    
    try:
        from oauth_email_sender import OAuthEmailSender
        
        sender = OAuthEmailSender()
        
        # Email de test
        test_email = {
            'to_email': auth_result['email'],  # Envoyer à soi-même
            'subject': 'Test OAuth - Générateur de Convocations DELF',
            'body': '''
            <html>
            <body>
                <h2>🎉 Test OAuth Réussi!</h2>
                <p>Félicitations! L'authentification OAuth fonctionne correctement.</p>
                
                <h3>Détails du test:</h3>
                <ul>
                    <li><strong>Méthode:</strong> Microsoft Graph API avec OAuth2</li>
                    <li><strong>Application:</strong> Générateur de Convocations DELF</li>
                    <li><strong>Statut:</strong> ✅ Opérationnel</li>
                </ul>
                
                <p>Vous pouvez maintenant utiliser l'authentification OAuth pour envoyer des convocations d'examens de manière sécurisée.</p>
                
                <hr>
                <p><em>Alliance Française Bruxelles Europe</em><br>
                <small>Générateur de Convocations - Version OAuth</small></p>
            </body>
            </html>
            '''
        }
        
        print(f"Envoi d'un email de test à {test_email['to_email']}...")
        
        result = sender.send_email_with_attachment(
            access_token=auth_result['access_token'],
            **test_email
        )
        
        if result['success']:
            print(f"✅ {result['message']}")
            print("   Vérifiez votre boîte de réception!")
            return True
        else:
            print(f"❌ Erreur d'envoi: {result['error']}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur lors du test d'envoi: {e}")
        return False

def test_main_application():
    """Test de l'application principale avec OAuth"""
    print("\n🧪 Test 4: Application Principale avec OAuth")
    print("=" * 50)
    
    try:
        print("Lancement de l'application principale...")
        print("Vous pouvez maintenant tester le bouton '🌐 Authentification OAuth'")
        
        from main import ConvocationGenerator
        
        app = ConvocationGenerator()
        app.run()
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du lancement de l'application: {e}")
        return False

def main():
    """Fonction principale de test"""
    print("🚀 Test Complet du Système OAuth")
    print("=" * 60)
    print("Ce script teste l'ensemble du système d'authentification OAuth")
    print("pour le générateur de convocations DELF.\n")
    
    # Test 1: Authentification OAuth
    auth_result = test_oauth_authentication()
    if not auth_result:
        print("\n❌ Échec du test d'authentification. Arrêt des tests.")
        return
    
    # Test 2: Test de connexion
    connection_ok = test_oauth_email_connection(auth_result)
    if not connection_ok:
        print("\n❌ Échec du test de connexion. Arrêt des tests.")
        return
    
    # Test 3: Envoi d'email de test
    email_ok = test_oauth_email_sending(auth_result)
    if not email_ok:
        print("\n⚠️ Échec du test d'envoi d'email, mais on continue...")
    
    # Test 4: Application principale
    print("\n" + "=" * 60)
    print("🎯 Tous les tests de base sont terminés!")
    print("=" * 60)
    
    if email_ok:
        print("✅ Système OAuth entièrement fonctionnel")
    else:
        print("⚠️ Système OAuth partiellement fonctionnel (authentification OK, envoi à vérifier)")
    
    print("\nVoulez-vous tester l'application principale? (o/n): ", end="")
    choice = input().lower().strip()
    
    if choice in ['o', 'oui', 'y', 'yes']:
        test_main_application()
    else:
        print("\n🏁 Tests terminés. Merci!")

if __name__ == "__main__":
    main()
