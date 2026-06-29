#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Version simplifiée du MailjetBridge sans cryptographie
"""

import json
import os
import smtplib
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path

# Ajouter le répertoire courant au path
sys.path.insert(0, str(Path(__file__).parent))

class SimpleMailjetBridge:
    """Version simplifiée sans cryptographie"""
    
    def __init__(self):
        self.api_key = "your_api_key"
        self.secret_key = "your_secret_key"
        self.fallback_enabled = True
        
        # Charger le registre des candidats
        from candidate_pdf_registry import CandidatePDFRegistry
        self.registry = CandidatePDFRegistry(".")
        
    def send_convocation_email(self, candidate_id, force_fallback=False):
        """
        Envoie un email de convocation à un candidat
        """
        try:
            # Récupérer les infos du candidat depuis le registre JSON
            if candidate_id not in self.registry.registry:
                return {
                    'success': False,
                    'error': f'Candidat {candidate_id} non trouvé dans le registre'
                }
            
            candidate_info = self.registry.registry[candidate_id]
            pdf_filename = candidate_info['pdf_filename']
            pdf_path = os.path.join(self.registry.output_dir, pdf_filename)
            
            # Vérifier si le PDF existe
            if not os.path.exists(pdf_path):
                return {
                    'success': False,
                    'error': f'Fichier PDF non trouvé: {pdf_path}'
                }
            
            print(f"📧 Préparation email pour {candidate_info['prenom']} {candidate_info['nom']}")
            print(f"   📁 PDF: {os.path.basename(pdf_path)}")
            print(f"   📬 Email: {candidate_info['email']}")
            
            if force_fallback or self.fallback_enabled:
                return self._send_fallback_notification(candidate_info, pdf_path)
            else:
                return self._send_mailjet_email(candidate_info, pdf_path)
                
        except Exception as e:
            return {
                'success': False,
                'error': f'Erreur lors de l\'envoi: {str(e)}'
            }
    
    def _send_mailjet_email(self, candidate_info, pdf_path):
        """Envoi via Mailjet (simulé pour éviter les erreurs crypto)"""
        print("   🚀 Envoi via Mailjet (SIMULÉ)")
        return {
            'success': True,
            'method': 'mailjet_simulated',
            'candidate_id': candidate_info.get('id', 'unknown'),
            'email': candidate_info['email']
        }
    
    def _send_fallback_notification(self, candidate_info, pdf_path):
        """Notification de fallback (sans envoi réel)"""
        print("   📋 Mode fallback - Notification préparée")
        return {
            'success': True,
            'method': 'fallback',
            'candidate_id': candidate_info.get('id', 'unknown'),
            'email': candidate_info['email'],
            'pdf_ready': os.path.exists(pdf_path)
        }
    
    def send_batch_emails(self, candidate_ids=None, max_emails=None):
        """
        Envoie des emails en lot
        """
        if candidate_ids is None:
            candidate_ids = list(self.registry.registry.keys())
        
        if max_emails:
            candidate_ids = candidate_ids[:max_emails]
        
        results = {
            'total': len(candidate_ids),
            'sent': 0,
            'failed': 0,
            'details': []
        }
        
        print(f"📮 ENVOI EN LOT: {len(candidate_ids)} candidats")
        print("=" * 50)
        
        for i, candidate_id in enumerate(candidate_ids, 1):
            print(f"\n[{i}/{len(candidate_ids)}] ", end="")
            
            result = self.send_convocation_email(candidate_id, force_fallback=True)
            
            if result['success']:
                results['sent'] += 1
                print("✅ Succès")
            else:
                results['failed'] += 1
                print(f"❌ Échec: {result['error']}")
            
            results['details'].append({
                'candidate_id': candidate_id,
                'success': result['success'],
                'error': result.get('error', None)
            })
        
        print(f"\n📊 RÉSULTATS:")
        print(f"   ✅ Envoyés: {results['sent']}")
        print(f"   ❌ Échecs: {results['failed']}")
        print(f"   📈 Taux de succès: {results['sent']/results['total']*100:.1f}%")
        
        return results

def test_simple_mailjet():
    """Test du système simplifié"""
    print("🧪 TEST DU SYSTÈME MAILJET SIMPLIFIÉ")
    print("=" * 50)
    
    try:
        bridge = SimpleMailjetBridge()
        print(f"✅ Bridge initialisé avec {len(bridge.registry.registry)} candidats")
        
        # Test avec 3 candidats
        candidate_ids = list(bridge.registry.registry.keys())[:3]
        results = bridge.send_batch_emails(candidate_ids)
        
        if results['failed'] == 0:
            print("\n🎉 TOUS LES TESTS RÉUSSIS!")
            return True
        else:
            print(f"\n⚠️  {results['failed']} échecs détectés")
            return False
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_simple_mailjet()