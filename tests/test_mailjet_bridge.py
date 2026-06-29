#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de test pour le bridge Mailjet sécurisé
Teste toutes les fonctionnalités du bridge sans envoyer d'emails réels
"""

import os
import sys
import json
import tempfile
import pandas as pd
from datetime import datetime
import getpass

# Importer notre bridge
try:
    from mailjet_bridge import MailjetBridge, MailjetSecurityManager
except ImportError as e:
    print(f"Erreur d'importation: {e}")
    print("Assurez-vous d'avoir installé les dépendances: pip install -r requirements.txt")
    sys.exit(1)

def create_test_data():
    """Crée des données de test pour les candidats"""
    test_data = {
        'nom': ['DUPONT', 'MARTIN', 'BERNARD'],
        'prenom': ['Jean', 'Marie', 'Pierre'],
        'email': ['jean.dupont@test.com', 'marie.martin@test.com', 'pierre.bernard@test.com'],
        'numero_candidat': ['TEST001', 'TEST002', 'TEST003'],
        'matiere': ['DELF B2', 'DALF C1', 'DELF B1'],
        'date_examen': ['2024-03-15', '2024-03-16', '2024-03-17'],
        'heure_debut': ['09:00', '14:00', '10:00'],
        'salle': ['Salle A1', 'Salle B2', 'Salle C3']
    }
    
    df = pd.DataFrame(test_data)
    return df

def create_test_pdf():
    """Crée un fichier PDF de test"""
    test_content = b"%PDF-1.4\n1 0 obj\n<<\n/Type /Catalog\n/Pages 2 0 R\n>>\nendobj\n2 0 obj\n<<\n/Type /Pages\n/Kids [3 0 R]\n/Count 1\n>>\nendobj\n3 0 obj\n<<\n/Type /Page\n/Parent 2 0 R\n/MediaBox [0 0 612 792]\n/Contents 4 0 R\n>>\nendobj\n4 0 obj\n<<\n/Length 44\n>>\nstream\nBT\n/F1 12 Tf\n100 700 Td\n(Test PDF) Tj\nET\nendstream\nendobj\nxref\n0 5\n0000000000 65535 f \n0000000010 00000 n \n0000000079 00000 n \n0000000173 00000 n \n0000000301 00000 n \n0000000380 00000 n \ntrailer\n<<\n/Size 5\n/Root 1 0 R\n>>\nstartxref\n492\n%%EOF"
    
    # Créer un répertoire de test temporaire
    os.makedirs('test_output', exist_ok=True)
    
    # Créer des fichiers PDF de test
    test_files = [
        'convocation_DUPONT_Jean_TEST001.pdf',
        'convocation_MARTIN_Marie_TEST002.pdf', 
        'convocation_BERNARD_Pierre_TEST003.pdf'
    ]
    
    for filename in test_files:
        filepath = os.path.join('test_output', filename)
        with open(filepath, 'wb') as f:
            f.write(test_content)
            
    return 'test_output'

def test_security_manager():
    """Teste le gestionnaire de sécurité"""
    print("=== Test du gestionnaire de sécurité ===")
    
    try:
        # Créer un gestionnaire de sécurité pour les tests
        security_manager = MailjetSecurityManager("test_mailjet_config.json")
        
        # Tester le chiffrement et déchiffrement
        test_api_key = "test_api_key_12345"
        test_secret_key = "test_secret_key_67890"
        test_password = "test_password_secure"
        
        print("Test du chiffrement des credentials...")
        security_manager.encrypt_credentials(test_api_key, test_secret_key, test_password)
        print("✓ Chiffrement réussi")
        
        print("Test du déchiffrement des credentials...")
        credentials = security_manager.decrypt_credentials(test_password)
        
        if credentials['api_key'] == test_api_key and credentials['secret_key'] == test_secret_key:
            print("✓ Déchiffrement réussi")
            print("✓ Gestionnaire de sécurité fonctionnel")
        else:
            print("✗ Erreur dans le déchiffrement")
            
        # Test mot de passe incorrect
        try:
            security_manager.decrypt_credentials("wrong_password")
            print("✗ Erreur: mot de passe incorrect accepté")
        except ValueError:
            print("✓ Mot de passe incorrect correctement rejeté")
            
    except Exception as e:
        print(f"✗ Erreur dans le gestionnaire de sécurité: {e}")
        return False
    
    finally:
        # Nettoyer les fichiers de test
        for file in ["test_mailjet_config.json", "mailjet.key"]:
            if os.path.exists(file):
                os.remove(file)
                
    return True

def test_data_loading():
    """Teste le chargement des données Excel"""
    print("\n=== Test du chargement des données ===")
    
    try:
        # Créer un fichier Excel de test
        df_test = create_test_data()
        test_excel_path = "test_candidats.xlsx"
        df_test.to_excel(test_excel_path, index=False)
        
        # Tester avec un bridge sans authentification pour les tests de données
        class MockBridge(MailjetBridge):
            def __init__(self, excel_path, pdf_dir):
                self.excel_path = excel_path
                self.pdf_dir = pdf_dir
                
        bridge = MockBridge(test_excel_path, "test_output")
        
        # Tester le chargement Excel
        print("Test du chargement des données Excel...")
        df = bridge._load_excel_data()
        
        if len(df) == 3:
            print(f"✓ Chargement réussi: {len(df)} candidats trouvés")
        else:
            print(f"✗ Erreur: nombre de candidats incorrect ({len(df)})")
            return False
            
        # Tester la recherche de fichiers PDF
        print("Test de la recherche des fichiers PDF...")
        pdf_dir = create_test_pdf()
        
        for index, row in df.iterrows():
            pdf_path = bridge._find_pdf_file(row)
            if pdf_path and os.path.exists(pdf_path):
                print(f"✓ PDF trouvé pour {row['nom']} {row['prenom']}: {pdf_path}")
            else:
                print(f"✗ PDF non trouvé pour {row['nom']} {row['prenom']}")
                return False
        
        # Tester la création du contenu email
        print("Test de la création du contenu email...")
        test_candidate = df.iloc[0]
        bridge.sender_name = "Service Test"
        subject, body_html, body_text = bridge._create_email_content(test_candidate)
        
        if subject and body_html and body_text:
            print("✓ Contenu email créé avec succès")
            print(f"  Sujet: {subject}")
        else:
            print("✗ Erreur dans la création du contenu email")
            return False
            
    except Exception as e:
        print(f"✗ Erreur dans le test de données: {e}")
        return False
    
    finally:
        # Nettoyer les fichiers de test
        for file in ["test_candidats.xlsx"]:
            if os.path.exists(file):
                os.remove(file)
        
        # Nettoyer le répertoire de test
        import shutil
        if os.path.exists("test_output"):
            shutil.rmtree("test_output")
            
    return True

def test_email_formatting():
    """Teste le formatage des emails"""
    print("\n=== Test du formatage des emails ===")
    
    try:
        class MockBridge(MailjetBridge):
            def __init__(self):
                self.sender_name = "Service Test"
                
        bridge = MockBridge()
        
        # Tester le formatage des dates
        test_dates = [
            "2024-03-15",
            "15/03/2024", 
            "15-03-2024",
            datetime(2024, 3, 15),
            "",
            None
        ]
        
        print("Test du formatage des dates...")
        for date_test in test_dates:
            formatted = bridge._format_date(date_test)
            print(f"  {date_test} -> {formatted}")
        
        # Tester la création complète d'email
        test_candidate = {
            'nom': 'DUPONT',
            'prenom': 'Jean',
            'matiere': 'DELF B2',
            'date_examen': '2024-03-15',
            'heure_debut': '09:00',
            'salle': 'Salle A1'
        }
        
        subject, body_html, body_text = bridge._create_email_content(test_candidate)
        
        print("\nTest de création d'email complet:")
        print(f"✓ Sujet: {subject}")
        print(f"✓ HTML généré: {len(body_html)} caractères")
        print(f"✓ Texte généré: {len(body_text)} caractères")
        
        # Vérifier que les données sont bien intégrées
        if "DUPONT" in body_html and "Jean" in body_html and "DELF B2" in body_html:
            print("✓ Données candidat correctement intégrées")
        else:
            print("✗ Erreur dans l'intégration des données")
            return False
            
    except Exception as e:
        print(f"✗ Erreur dans le test de formatage: {e}")
        return False
        
    return True

def test_attachment_encoding():
    """Teste l'encodage des pièces jointes"""
    print("\n=== Test de l'encodage des pièces jointes ===")
    
    try:
        class MockBridge(MailjetBridge):
            def __init__(self):
                pass
                
        bridge = MockBridge()
        
        # Créer un fichier de test temporaire
        test_content = b"Test PDF content for attachment"
        test_file = "test_attachment.pdf"
        
        with open(test_file, 'wb') as f:
            f.write(test_content)
        
        # Tester l'encodage
        print("Test de l'encodage base64...")
        content_base64, filename = bridge._encode_attachment(test_file)
        
        if content_base64 and filename == "test_attachment.pdf":
            print(f"✓ Encodage réussi: {len(content_base64)} caractères base64")
            print(f"✓ Nom de fichier: {filename}")
            
            # Vérifier que le décodage fonctionne
            import base64
            decoded_content = base64.b64decode(content_base64)
            if decoded_content == test_content:
                print("✓ Encodage/décodage validé")
            else:
                print("✗ Erreur dans l'encodage/décodage")
                return False
        else:
            print("✗ Erreur dans l'encodage")
            return False
            
    except Exception as e:
        print(f"✗ Erreur dans le test d'encodage: {e}")
        return False
    
    finally:
        # Nettoyer
        if os.path.exists(test_file):
            os.remove(test_file)
            
    return True

def interactive_credentials_test():
    """Test interactif des credentials (optionnel)"""
    print("\n=== Test interactif des credentials (optionnel) ===")
    
    test_real_credentials = input("Tester avec de vrais credentials Mailjet? (o/N): ").lower() == 'o'
    
    if not test_real_credentials:
        print("Test des credentials ignoré (test en mode simulation)")
        return True
    
    try:
        # Demander les credentials
        print("\nEntrez vos credentials Mailjet pour le test:")
        api_key = input("Clé API Mailjet: ").strip()
        secret_key = getpass.getpass("Clé secrète Mailjet: ").strip()
        
        if not api_key or not secret_key:
            print("Credentials non fournis, test ignoré")
            return True
        
        # Tester la connexion
        try:
            from mailjet_rest import Client
            test_client = Client(auth=(api_key, secret_key), version='v3.1')
            result = test_client.contact.get()
            
            if result.status_code == 200:
                print("✓ Connexion Mailjet réussie")
                
                # Test des infos du compte
                user_result = test_client.user.get()
                if user_result.status_code == 200:
                    user_info = user_result.json()
                    print(f"✓ Compte validé: {user_info}")
                else:
                    print("⚠ Impossible de récupérer les infos du compte")
                    
                return True
            else:
                print(f"✗ Échec de la connexion Mailjet: {result.status_code}")
                return False
                
        except Exception as e:
            print(f"✗ Erreur de connexion Mailjet: {e}")
            return False
            
    except Exception as e:
        print(f"✗ Erreur dans le test des credentials: {e}")
        return False

def main():
    """Fonction principale de test"""
    print("🚀 Démarrage des tests du bridge Mailjet sécurisé")
    print("=" * 60)
    
    tests_results = []
    
    # Exécuter tous les tests
    tests = [
        ("Gestionnaire de sécurité", test_security_manager),
        ("Chargement des données", test_data_loading),
        ("Formatage des emails", test_email_formatting),
        ("Encodage des pièces jointes", test_attachment_encoding),
        ("Test des credentials (optionnel)", interactive_credentials_test)
    ]
    
    for test_name, test_func in tests:
        print(f"\n🧪 Exécution: {test_name}")
        print("-" * 40)
        
        try:
            result = test_func()
            tests_results.append((test_name, result))
            
            if result:
                print(f"✅ {test_name}: RÉUSSI")
            else:
                print(f"❌ {test_name}: ÉCHEC")
                
        except Exception as e:
            print(f"❌ {test_name}: ERREUR - {e}")
            tests_results.append((test_name, False))
    
    # Résumé des résultats
    print("\n" + "=" * 60)
    print("📊 RÉSUMÉ DES TESTS")
    print("=" * 60)
    
    passed = sum(1 for _, result in tests_results if result)
    total = len(tests_results)
    
    for test_name, result in tests_results:
        status = "✅ RÉUSSI" if result else "❌ ÉCHEC"
        print(f"{test_name:.<40} {status}")
    
    print("-" * 60)
    print(f"Tests réussis: {passed}/{total}")
    
    if passed == total:
        print("🎉 TOUS LES TESTS ONT RÉUSSI!")
        print("Le bridge Mailjet est prêt à être utilisé.")
    else:
        print("⚠️  CERTAINS TESTS ONT ÉCHOUÉ")
        print("Vérifiez les erreurs ci-dessus avant d'utiliser le bridge.")
    
    print("\n📖 Consultez GUIDE_MAILJET.md pour les instructions d'utilisation.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
