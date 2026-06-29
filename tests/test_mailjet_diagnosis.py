#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Diagnostic complet du système Mailjet
Teste la connexion, les credentials et l'envoi d'emails
"""

import os
import sys
import getpass
from datetime import datetime
import pandas as pd

# Importer le bridge Mailjet
try:
    from mailjet_bridge import MailjetBridge
    print("✅ Module mailjet_bridge importé avec succès")
except ImportError as e:
    print(f"❌ Erreur d'import mailjet_bridge: {e}")
    sys.exit(1)

class MailjetDiagnostic:
    def __init__(self):
        self.bridge = None
        self.test_results = {
            'import_mailjet': False,
            'credentials_exist': False,
            'authentication': False,
            'connection_test': False,
            'account_info': False,
            'excel_loading': False,
            'pdf_files': False,
            'test_email': False
        }
    
    def test_credentials_files(self):
        """Teste l'existence des fichiers de credentials"""
        print("\n🔐 Test des fichiers de credentials...")
        
        config_file = "mailjet_config.json"
        key_file = "mailjet.key"
        
        if os.path.exists(config_file):
            print(f"✅ Fichier de configuration trouvé: {config_file}")
            self.test_results['credentials_exist'] = True
        else:
            print(f"❌ Fichier de configuration manquant: {config_file}")
            print("💡 Vous devez d'abord configurer vos credentials Mailjet")
            return False
        
        if os.path.exists(key_file):
            print(f"✅ Fichier de clé trouvé: {key_file}")
        else:
            print(f"❌ Fichier de clé manquant: {key_file}")
            return False
        
        return True
    
    def test_excel_file(self, excel_path):
        """Teste le chargement du fichier Excel"""
        print(f"\n📊 Test du fichier Excel: {excel_path}")
        
        if not os.path.exists(excel_path):
            print(f"❌ Fichier Excel non trouvé: {excel_path}")
            return False
        
        try:
            df = pd.read_excel(excel_path, engine='openpyxl')
            print(f"✅ Fichier Excel chargé: {len(df)} candidats")
            
            # Vérifier les colonnes requises
            required_columns = ['nom', 'prenom', 'email', 'numero_candidat']
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            if missing_columns:
                print(f"❌ Colonnes manquantes: {missing_columns}")
                return False
            
            print("✅ Toutes les colonnes requises sont présentes")
            
            # Vérifier quelques emails
            emails_sample = df['email'].head(3).tolist()
            print(f"📧 Échantillon d'emails: {emails_sample}")
            
            self.test_results['excel_loading'] = True
            return True
            
        except Exception as e:
            print(f"❌ Erreur lors du chargement Excel: {e}")
            return False
    
    def test_pdf_directory(self, pdf_dir):
        """Teste l'existence du répertoire PDF"""
        print(f"\n📄 Test du répertoire PDF: {pdf_dir}")
        
        if not os.path.exists(pdf_dir):
            print(f"❌ Répertoire PDF non trouvé: {pdf_dir}")
            return False
        
        pdf_files = [f for f in os.listdir(pdf_dir) if f.endswith('.pdf')]
        print(f"✅ Répertoire PDF trouvé avec {len(pdf_files)} fichiers PDF")
        
        if len(pdf_files) > 0:
            print(f"📄 Exemples de PDF: {pdf_files[:3]}")
            self.test_results['pdf_files'] = True
        else:
            print("⚠️  Aucun fichier PDF trouvé")
        
        return len(pdf_files) > 0
    
    def test_mailjet_connection(self, password):
        """Teste la connexion Mailjet"""
        print(f"\n🌐 Test de la connexion Mailjet...")
        
        try:
            # Créer le bridge
            self.bridge = MailjetBridge(
                excel_path="candidats_emails_valides.xlsx",
                pdf_dir="output",
                sender_email="test@example.com",  # Email temporaire pour test
                sender_name="Test Service"
            )
            
            # Authentification
            print("🔑 Authentification...")
            self.bridge._authenticate(password)
            print("✅ Authentification réussie")
            self.test_results['authentication'] = True
            
            # Test de connexion
            print("🔗 Test de connexion API...")
            if self.bridge.test_connection():
                print("✅ Connexion Mailjet réussie")
                self.test_results['connection_test'] = True
            else:
                print("❌ Échec de la connexion Mailjet")
                return False
            
            # Informations du compte
            print("ℹ️  Récupération des informations du compte...")
            try:
                account_info = self.bridge.get_account_info()
                print("✅ Informations du compte récupérées")
                print(f"📊 Compte: {account_info}")
                self.test_results['account_info'] = True
            except Exception as e:
                print(f"⚠️  Impossible de récupérer les infos du compte: {e}")
            
            return True
            
        except Exception as e:
            print(f"❌ Erreur de connexion Mailjet: {e}")
            return False
    
    def test_single_email(self):
        """Teste l'envoi d'un email unique"""
        print(f"\n📧 Test d'envoi d'un email unique...")
        
        if not self.bridge:
            print("❌ Bridge Mailjet non initialisé")
            return False
        
        # Charger un candidat de test
        try:
            df = pd.read_excel("candidats_emails_valides.xlsx", engine='openpyxl')
            if len(df) == 0:
                print("❌ Aucun candidat dans le fichier")
                return False
            
            # Prendre le premier candidat
            test_candidate = df.iloc[0].to_dict()
            
            print(f"👤 Candidat de test: {test_candidate['nom']} {test_candidate['prenom']}")
            print(f"📧 Email: {test_candidate['email']}")
            
            # Demander confirmation
            confirm = input("Voulez-vous envoyer un email de test à ce candidat? (o/N): ").lower()
            if confirm != 'o':
                print("⏭️  Test d'email ignoré")
                return True
            
            # Envoyer l'email
            def progress_callback(message):
                print(f"  {message}")
            
            success = self.bridge.send_email(test_candidate, progress_callback)
            
            if success:
                print("✅ Email de test envoyé avec succès")
                self.test_results['test_email'] = True
                return True
            else:
                print("❌ Échec de l'envoi de l'email de test")
                return False
                
        except Exception as e:
            print(f"❌ Erreur lors du test d'email: {e}")
            return False
    
    def run_full_diagnosis(self):
        """Exécute un diagnostic complet"""
        print("🔍 DIAGNOSTIC COMPLET DU SYSTÈME MAILJET")
        print("=" * 60)
        
        # 1. Test des credentials
        if not self.test_credentials_files():
            print("\n❌ Diagnostic arrêté: credentials manquants")
            return False
        
        # 2. Test du fichier Excel
        excel_files = ["candidats_emails_valides.xlsx", "candidats_pour_mailjet.xlsx"]
        excel_found = False
        for excel_file in excel_files:
            if os.path.exists(excel_file):
                if self.test_excel_file(excel_file):
                    excel_found = True
                    break
        
        if not excel_found:
            print("\n❌ Diagnostic arrêté: aucun fichier Excel valide trouvé")
            return False
        
        # 3. Test du répertoire PDF
        self.test_pdf_directory("output")
        
        # 4. Test de connexion Mailjet
        password = getpass.getpass("\n🔑 Mot de passe Mailjet: ")
        if not self.test_mailjet_connection(password):
            print("\n❌ Diagnostic arrêté: connexion Mailjet échouée")
            return False
        
        # 5. Test d'envoi d'email (optionnel)
        self.test_single_email()
        
        # Résumé
        self.print_diagnosis_summary()
        
        return True
    
    def print_diagnosis_summary(self):
        """Affiche un résumé du diagnostic"""
        print("\n" + "=" * 60)
        print("📊 RÉSUMÉ DU DIAGNOSTIC")
        print("=" * 60)
        
        tests = [
            ("Fichiers credentials", self.test_results['credentials_exist']),
            ("Authentification", self.test_results['authentication']),
            ("Connexion API", self.test_results['connection_test']),
            ("Informations compte", self.test_results['account_info']),
            ("Chargement Excel", self.test_results['excel_loading']),
            ("Fichiers PDF", self.test_results['pdf_files']),
            ("Test email", self.test_results['test_email'])
        ]
        
        passed = 0
        for test_name, result in tests:
            status = "✅" if result else "❌"
            print(f"{status} {test_name}")
            if result:
                passed += 1
        
        print(f"\n📈 Score: {passed}/{len(tests)} tests réussis")
        
        if passed == len(tests):
            print("🎉 Système Mailjet entièrement fonctionnel !")
        elif passed >= len(tests) - 2:
            print("⚠️  Système Mailjet presque prêt, quelques ajustements nécessaires")
        else:
            print("❌ Problèmes majeurs détectés avec le système Mailjet")
        
        # Recommandations
        print("\n💡 RECOMMANDATIONS:")
        
        if not self.test_results['credentials_exist']:
            print("   1. Configurez vos credentials Mailjet avec setup_credentials()")
        
        if not self.test_results['pdf_files']:
            print("   2. Générez les PDF de convocation avant l'envoi")
        
        if self.test_results['connection_test'] and not self.test_results['test_email']:
            print("   3. Testez l'envoi d'un email pour valider le système complet")
        
        print("   4. Utilisez le fichier 'candidats_emails_valides.xlsx' pour l'envoi")

def main():
    """Fonction principale"""
    diagnostic = MailjetDiagnostic()
    
    try:
        diagnostic.run_full_diagnosis()
    except KeyboardInterrupt:
        print("\n⏹️  Diagnostic interrompu par l'utilisateur")
    except Exception as e:
        print(f"\n❌ Erreur inattendue: {e}")

if __name__ == "__main__":
    main()
