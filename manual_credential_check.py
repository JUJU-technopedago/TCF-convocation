#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Direct credential check - bypass mailjet_bridge import
"""

import json
import base64
import hashlib

print("🔍 MANUAL CREDENTIAL CHECK\n")

# Try to manually decrypt
config_file = "mailjet_config.json"
key_file = "mailjet.key"

# Read key file
with open(key_file, 'r') as f:
    key_data = json.load(f)
    password_hash = key_data["password_hash"]
    print(f"✅ Password hash from key file: {password_hash[:20]}...")

# Try common passwords
passwords_to_try = ["alliance2024", "alliancefr", "tcf2024", "", "mailjet"]

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

def generate_key(password: str) -> bytes:
    """Génère une clé de chiffrement à partir d'un mot de passe"""
    password_bytes = password.encode()
    salt = b'mailjet_secure_salt_2024'
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password_bytes))
    return key

print("\n🔐 Trying to find correct password...")
for password in passwords_to_try:
    test_hash = hashlib.sha256(password.encode()).hexdigest()
    if test_hash == password_hash:
        print(f"\n✅ FOUND PASSWORD: '{password}'")
        
        # Decrypt
        key = generate_key(password)
        f = Fernet(key)
        
        with open(config_file, 'rb') as file:
            encrypted_data = file.read()
        
        decrypted_data = f.decrypt(encrypted_data)
        credentials = json.loads(decrypted_data.decode())
        
        api_key = credentials["api_key"]
        secret_key = credentials["secret_key"]
        
        print(f"\n📌 API Key: {api_key}")
        print(f"📌 Secret Key: {secret_key}")
        
        # Now test with Mailjet
        print(f"\n📡 Testing Mailjet connection...")
        
        # Import without going through mailjet_bridge
        import sys
        import os
        mailjet_path = os.path.join(os.path.dirname(__file__), 'mailjet')
        if mailjet_path not in sys.path:
            sys.path.insert(0, mailjet_path)
        
        from mailjet_rest import Client
        
        # Test sender verification
        test_client = Client(auth=(api_key, secret_key), version='v3')
        result = test_client.sender.get()
        
        print(f"Status: {result.status_code}")
        
        if result.status_code == 200:
            data = result.json()
            print(f"\n✅ Mailjet connected!")
            print(f"Response: {data}")
            
            sender_email = "no-reply@alliancefr.be"
            
            if 'Data' in data:
                print(f"\n📧 Verified senders:")
                for sender in data['Data']:
                    email = sender.get('Email')
                    status = sender.get('Status')
                    is_default = sender.get('IsDefaultSender', False)
                    print(f"   • {email}: {status} (Default: {is_default})")
                    
                    if email == sender_email:
                        if status != 'Active':
                            print(f"\n   ⚠️  PROBLEM: {sender_email} status is '{status}', NOT 'Active'!")
                            print(f"   ⚠️  This could prevent email delivery!")
                        else:
                            print(f"\n   ✅ {sender_email} is ACTIVE - should work!")
        
        break
else:
    print(f"\n❌ Could not find matching password")
    print(f"Expected hash: {password_hash}")
    print(f"\nHashes tried:")
    for pwd in passwords_to_try:
        print(f"  '{pwd}': {hashlib.sha256(pwd.encode()).hexdigest()[:20]}...")
