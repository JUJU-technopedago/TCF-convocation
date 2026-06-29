#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def test_email_personalization():
    """Test pour vérifier que chaque candidat reçoit un email personnalisé"""
    
    print("=== TEST DE PERSONNALISATION DES EMAILS ===")
    print("=" * 50)
    
    try:
        import sys
        import os
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        
        from tcf_excel_processor import TCFExcelProcessor
        from mailjet_bridge import MailjetEmailSender
        
        # 1. Charger les données TCF
        print("1. Chargement des données TCF...")
        processor = TCFExcelProcessor("JURYS FINAL TCF.xlsx")
        
        if not processor.load_tcf_data():
            print("❌ Erreur lors du chargement des données TCF")
            return False
        
        candidates = processor.get_all_candidates()
        print(f"✅ {len(candidates)} candidats chargés")
        
        # 2. Créer le générateur d'email
        print("\n2. Création du générateur d'email...")
        email_generator = MailjetEmailSender(api_key="dummy", secret_key="dummy")
        
        # 3. Tester avec 5 candidats différents
        test_candidates = candidates[:5]  # Prendre les 5 premiers
        
        print(f"\n3. Test de personnalisation pour {len(test_candidates)} candidats...")
        print("-" * 60)
        
        emails_generated = []
        
        for i, candidate in enumerate(test_candidates, 1):
            print(f"\n--- CANDIDAT {i}: {candidate['prenom']} {candidate['nom']} ---")
            print(f"Type TCF: {candidate['tcf_type']}")
            print(f"Email: {candidate['email']}")
            print(f"Date examen: {candidate.get('date_examen', 'N/A')}")
            
            # Générer le contenu email personnalisé
            try:
                email_content = email_generator._create_email_content(candidate)
                
                print(f"📧 Sujet: {email_content['subject']}")
                print(f"📝 Contenu (extrait): {email_content['html_content'][:200]}...")
                
                # Vérifier que l'email contient les bonnes informations personnalisées
                html_content = email_content['html_content']
                text_content = email_content['text_content']
                
                personalization_checks = {
                    'nom_in_html': candidate['nom'] in html_content,
                    'prenom_in_html': candidate['prenom'] in html_content,
                    'nom_in_text': candidate['nom'] in text_content,
                    'prenom_in_text': candidate['prenom'] in text_content,
                    'tcf_in_subject': 'TCF' in email_content['subject'],
                    'mailto_link': 'mailto:examens@alliancefr.be' in html_content,
                    'contact_email': 'examens@alliancefr.be' in text_content
                }
                
                print(f"✅ Vérifications personnalisation:")
                for check, result in personalization_checks.items():
                    status = "✅" if result else "❌"
                    print(f"   {status} {check}: {result}")
                
                # Stocker pour comparaison d'unicité
                emails_generated.append({
                    'candidate': f"{candidate['prenom']} {candidate['nom']}",
                    'subject': email_content['subject'],
                    'html_hash': hash(email_content['html_content']),
                    'text_hash': hash(email_content['text_content']),
                    'personalized': all(personalization_checks.values())
                })
                
                if all(personalization_checks.values()):
                    print("🎯 PERSONNALISATION RÉUSSIE!")
                else:
                    print("⚠️ PROBLÈME DE PERSONNALISATION")
                
            except Exception as e:
                print(f"❌ Erreur génération email: {e}")
                emails_generated.append({
                    'candidate': f"{candidate['prenom']} {candidate['nom']}",
                    'subject': 'ERREUR',
                    'html_hash': 0,
                    'text_hash': 0,
                    'personalized': False
                })
        
        # 4. Vérifier l'unicité des emails générés
        print(f"\n" + "=" * 60)
        print("4. VÉRIFICATION DE L'UNICITÉ DES EMAILS")
        print("=" * 60)
        
        unique_subjects = set(email['subject'] for email in emails_generated)
        unique_html = set(email['html_hash'] for email in emails_generated)
        unique_text = set(email['text_hash'] for email in emails_generated)
        
        print(f"📊 Statistiques:")
        print(f"   • Emails générés: {len(emails_generated)}")
        print(f"   • Sujets uniques: {len(unique_subjects)}")
        print(f"   • Contenus HTML uniques: {len(unique_html)}")
        print(f"   • Contenus TEXTE uniques: {len(unique_text)}")
        
        all_personalized = all(email['personalized'] for email in emails_generated)
        all_unique = len(unique_html) == len(emails_generated) and len(unique_text) == len(emails_generated)
        
        print(f"\n📋 Résumé des emails générés:")
        for email in emails_generated:
            status = "✅" if email['personalized'] else "❌"
            print(f"   {status} {email['candidate']}: {email['subject']}")
        
        # 5. Conclusion
        print(f"\n" + "=" * 60)
        print("🏁 CONCLUSION")
        print("=" * 60)
        
        if all_personalized and all_unique:
            print("🎉 SUCCÈS COMPLET!")
            print("✅ Tous les emails sont correctement personnalisés")
            print("✅ Chaque candidat recevra un email unique")
            print("✅ Le problème d'emails identiques est RÉSOLU!")
            return True
        else:
            print("⚠️ PROBLÈMES DÉTECTÉS:")
            if not all_personalized:
                print("❌ Certains emails ne sont pas correctement personnalisés")
            if not all_unique:
                print("❌ Certains emails ont le même contenu (problème persiste)")
            return False
        
    except ImportError as e:
        print(f"❌ Erreur d'import: {e}")
        print("Vérifiez que tous les modules nécessaires sont disponibles")
        return False
    except Exception as e:
        print(f"❌ Erreur inattendue: {e}")
        return False

if __name__ == "__main__":
    print("🚀 LANCEMENT DU TEST DE PERSONNALISATION DES EMAILS")
    test_email_personalization()