#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Corrections spécifiques pour les erreurs Mailjet 400
"""

import re
import time
import os
from typing import Dict, List

class Mailjet400Fixer:
    """Correcteur pour les erreurs Mailjet 400"""
    
    def __init__(self):
        self.max_attachment_size = 25 * 1024 * 1024  # 25MB
        self.rate_limit_delay = 1.0  # 1 seconde entre les emails
        
    def validate_email(self, email: str) -> bool:
        """Valide une adresse email"""
        if not email or not isinstance(email, str):
            return False
            
        # Pattern email plus strict
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email.strip()) is not None
    
    def clean_email_content(self, content: str) -> str:
        """Nettoie le contenu email des caractères problématiques"""
        if not content:
            return ""
            
        # Remplacer les caractères problématiques
        replacements = {
            # Ne pas remplacer les apostrophes et guillemets pour l'objet du mail
            # '"': '&quot;',
            # "'": '&#39;',
            # Caractères Unicode problématiques
            '⚠️': '[ATTENTION]',
            '✓': '[OK]',
            '✗': '[ERREUR]',
            '🚀': '[DEMARRAGE]',
            '🎉': '[SUCCES]',
            '❌': '[ECHEC]'
        }
        
        cleaned = content
        for old, new in replacements.items():
            cleaned = cleaned.replace(old, new)
            
        return cleaned
    
    def validate_attachment_size(self, file_path: str) -> bool:
        """Vérifie la taille de la pièce jointe"""
        try:
            if not os.path.exists(file_path):
                return False
                
            size = os.path.getsize(file_path)
            return size <= self.max_attachment_size
        except:
            return False
    
    def create_safe_mailjet_data(self, candidate_data: Dict, sender_email: str, 
                                sender_name: str, subject: str, html_content: str, 
                                text_content: str, attachment_path: str = None) -> Dict:
        """Crée des données Mailjet sécurisées"""
        
        # Valider l'email destinataire
        recipient_email = str(candidate_data.get('email', '')).strip()
        if not self.validate_email(recipient_email):
            raise ValueError(f"Email destinataire invalide: {recipient_email}")
        
        # Valider l'email expéditeur
        if not self.validate_email(sender_email):
            raise ValueError(f"Email expéditeur invalide: {sender_email}")
        
        # Nettoyer le contenu
        # L'objet du mail ne devrait pas avoir d'entités HTML
        safe_subject = subject[:255]  # Limiter la longueur sans encoder les caractères spéciaux
        # Pour le contenu HTML et texte, on peut toujours nettoyer les caractères problématiques
        safe_html = self.clean_email_content(html_content)
        safe_text = self.clean_email_content(text_content)
        safe_sender_name = sender_name[:50]  # Ne pas encoder le nom de l'expéditeur
        
        # Nom du destinataire sécurisé
        recipient_name = f"{candidate_data.get('prenom', '')} {candidate_data.get('nom', '')}"
        safe_recipient_name = self.clean_email_content(recipient_name)[:100]
        
        # Structure de base
        data = {
            'Messages': [
                {
                    "From": {
                        "Email": sender_email,
                        "Name": safe_sender_name
                    },
                    "To": [
                        {
                            "Email": recipient_email,
                            "Name": safe_recipient_name
                        }
                    ],
                    "Bcc": [
                        {
                            "Email": "no-reply@alliancefr.be",
                            "Name": "Archive TCF"
                        }
                    ],
                    "Subject": safe_subject,
                    "TextPart": safe_text,
                    "HTMLPart": safe_html
                }
            ]
        }
        
        # Ajouter la pièce jointe si fournie
        if attachment_path:
            if not self.validate_attachment_size(attachment_path):
                raise ValueError(f"Pièce jointe trop volumineuse: {attachment_path}")
            
            import base64
            
            try:
                with open(attachment_path, 'rb') as f:
                    content = f.read()
                
                content_base64 = base64.b64encode(content).decode('utf-8')
                filename = os.path.basename(attachment_path)
                
                data['Messages'][0]['Attachments'] = [
                    {
                        "ContentType": "application/pdf",
                        "Filename": filename,
                        "Base64Content": content_base64
                    }
                ]
            except Exception as e:
                raise ValueError(f"Erreur encodage pièce jointe: {e}")
        
        return data
    
    def send_with_retry(self, mailjet_client, data: Dict, max_retries: int = 3) -> Dict:
        """Envoie avec retry en cas d'erreur temporaire"""
        
        for attempt in range(max_retries):
            try:
                result = mailjet_client.send.create(data=data)
                
                if result.status_code == 200:
                    return {"success": True, "result": result}
                elif result.status_code == 429:  # Rate limit
                    if attempt < max_retries - 1:
                        time.sleep(self.rate_limit_delay * (attempt + 1))
                        continue
                    else:
                        return {"success": False, "error": "Rate limit dépassé"}
                else:
                    # Erreur 400 ou autre
                    try:
                        error_data = result.json()
                        error_msg = f"Erreur Mailjet {result.status_code}: {error_data}"
                    except:
                        error_msg = f"Erreur Mailjet {result.status_code}: {result.text[:200] if hasattr(result, 'text') else 'Erreur inconnue'}"
                    
                    return {"success": False, "error": error_msg}
                    
            except Exception as e:
                if attempt < max_retries - 1:
                    time.sleep(1)
                    continue
                else:
                    return {"success": False, "error": f"Exception: {e}"}
        
        return {"success": False, "error": "Échec après tous les tentatives"}

def patch_mailjet_bridge_with_400_fixes():
    """Applique les corrections 400 au bridge Mailjet"""
    
    mailjet_file = "mailjet_bridge.py"
    if not os.path.exists(mailjet_file):
        print(f"❌ Fichier {mailjet_file} non trouvé")
        return False
    
    with open(mailjet_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Vérifier si les corrections sont déjà appliquées
    if "from mailjet_400_fixes import Mailjet400Fixer" in content:
        print("✅ Corrections 400 déjà appliquées")
        return True
    
    # Ajouter l'import du fixer
    import_addition = "\n# Import pour les corrections 400\nfrom mailjet_400_fixes import Mailjet400Fixer\n"
    
    # Ajouter dans __init__
    init_addition = "\n        # Correcteur pour erreurs 400\n        self.error_fixer = Mailjet400Fixer()\n"
    
    # Modifier la méthode send_email pour utiliser le fixer
    old_send_method = "            # Envoyer l'email via Mailjet\n            result = self.mailjet_client.send.create(data=data)"
    
    new_send_method = """            # Créer des données sécurisées avec le fixer
            safe_data = self.error_fixer.create_safe_mailjet_data(
                candidate_data, self.sender_email, self.sender_name,
                subject, body_html, body_text, pdf_path
            )
            
            # Envoyer avec retry
            send_result = self.error_fixer.send_with_retry(self.mailjet_client, safe_data)
            
            if send_result["success"]:
                result = send_result["result"]
            else:
                raise Exception(send_result["error"])"""
    
    # Appliquer les modifications
    # Trouver la ligne d'import appropriée
    import_pos = content.find("from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC")
    if import_pos != -1:
        insert_pos = content.find("\n", import_pos) + 1
        content = content[:insert_pos] + import_addition + content[insert_pos:]
    
    # Ajouter dans __init__
    init_pos = content.find("if config_password:")
    if init_pos != -1:
        content = content[:init_pos] + init_addition + "\n        " + content[init_pos:]
    
    # Remplacer la méthode d'envoi
    if old_send_method in content:
        content = content.replace(old_send_method, new_send_method)
    
    # Sauvegarder
    with open(mailjet_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Corrections 400 appliquées au bridge Mailjet")
    return True

def main():
    """Fonction principale pour appliquer les corrections"""
    print("🔧 APPLICATION DES CORRECTIONS MAILJET 400")
    print("=" * 50)
    
    # Appliquer les corrections au bridge
    success = patch_mailjet_bridge_with_400_fixes()
    
    if success:
        print("\n✅ CORRECTIONS APPLIQUÉES AVEC SUCCÈS!")
        print("\nLes améliorations suivantes ont été ajoutées:")
        print("1. Validation stricte des emails")
        print("2. Nettoyage du contenu HTML/texte")
        print("3. Vérification de la taille des pièces jointes")
        print("4. Système de retry pour les erreurs temporaires")
        print("5. Gestion améliorée des erreurs 400")
        
        print("\n📋 Prochaines étapes:")
        print("1. Vérifiez que votre email expéditeur est vérifié dans Mailjet")
        print("2. Testez l'envoi avec un petit nombre d'emails")
        print("3. Surveillez les logs pour d'éventuelles erreurs")
    else:
        print("\n❌ Échec de l'application des corrections")

if __name__ == "__main__":
    main()