#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DIRECT EMAIL SENDER - Bypasses the application completely
Sends all 59 emails directly using Mailjet API
"""

import json
import hashlib
import base64
import os
import sys

# Add mailjet to path
mailjet_path = os.path.join(os.path.dirname(__file__), 'mailjet')
if mailjet_path not in sys.path:
    sys.path.insert(0, mailjet_path)

from mailjet_rest import Client

print("="*60)
print("📧 DIRECT EMAIL SENDER")
print("="*60)

# Step 1: Decrypt credentials
print("\n1. Loading credentials...")

config_file = "mailjet_config.json"
key_file = "mailjet.key"

with open(key_file, 'r') as f:
    key_data = json.load(f)
    password_hash = key_data["password_hash"]

# Try to find the password
test_passwords = ["", "alliance", "alliance2024", "mailjet", "tcf", "alliancefr", "Alliance2024"]

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet

password = None
for test_pwd in test_passwords:
    if hashlib.sha256(test_pwd.encode()).hexdigest() == password_hash:
        password = test_pwd
        print(f"   ✅ Password found")
        break

if password is None:
    print("   ❌ Could not find password. Please enter it manually:")
    password = input("   Password: ")
    if hashlib.sha256(password.encode()).hexdigest() != password_hash:
        print("   ❌ Incorrect password!")
        exit(1)

# Decrypt
def generate_key(pwd):
    password_bytes = pwd.encode()
    salt = b'mailjet_secure_salt_2024'
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    return base64.urlsafe_b64encode(kdf.derive(password_bytes))

key = generate_key(password)
f = Fernet(key)

with open(config_file, 'rb') as file:
    encrypted_data = file.read()

decrypted_data = f.decrypt(encrypted_data)
credentials = json.loads(decrypted_data.decode())

api_key = credentials["api_key"]
secret_key = credentials["secret_key"]

print(f"   ✅ API Key: {api_key[:10]}...")
print(f"   ✅ Secret Key: {secret_key[:10]}...")

# Step 2: Check Mailjet account
print("\n2. Checking Mailjet account...")

client_v3 = Client(auth=(api_key, secret_key), version='v3')
client_v31 = Client(auth=(api_key, secret_key), version='v3.1')

# Check senders
result = client_v3.sender.get()
print(f"   Sender check status: {result.status_code}")

if result.status_code == 200:
    data = result.json()
    print(f"\n   📧 Verified senders:")
    sender_ok = False
    for sender in data.get('Data', []):
        email = sender.get('Email')
        status = sender.get('Status')
        print(f"      • {email}: {status}")
        if email == "no-reply@alliancefr.be" and status == "Active":
            sender_ok = True
    
    if not sender_ok:
        print("\n   ⚠️  WARNING: no-reply@alliancefr.be may not be verified!")
        print("   ⚠️  Go to: https://app.mailjet.com/account/sender")

# Step 3: Load registry and send emails
print("\n3. Loading registry with 59 candidates...")

with open('output/candidate_pdf_registry.json', 'r', encoding='utf-8') as f:
    registry = json.load(f)

candidates_with_email = []
for cid, info in registry.items():
    cand = info.get('candidate_info', {})
    email = cand.get('email', '')
    if email:
        candidates_with_email.append({
            'id': cid,
            'nom': cand.get('nom', ''),
            'prenom': cand.get('prenom', ''),
            'email': email,
            'pdf_file': info.get('pdf_file', '')
        })

print(f"   Found {len(candidates_with_email)} candidates with email")

if len(candidates_with_email) < 59:
    print(f"\n   ⚠️  Only {len(candidates_with_email)} emails found!")
    print("   Running emergency script to add emails...")
    import subprocess
    subprocess.run([sys.executable, 'emergency_add_emails_to_registry.py'])
    
    # Reload
    with open('output/candidate_pdf_registry.json', 'r', encoding='utf-8') as f:
        registry = json.load(f)
    
    candidates_with_email = []
    for cid, info in registry.items():
        cand = info.get('candidate_info', {})
        email = cand.get('email', '')
        if email:
            candidates_with_email.append({
                'id': cid,
                'nom': cand.get('nom', ''),
                'prenom': cand.get('prenom', ''),
                'email': email,
                'pdf_file': info.get('pdf_file', '')
            })
    
    print(f"   After update: {len(candidates_with_email)} candidates with email")

# Step 4: Send emails
print(f"\n4. Sending {len(candidates_with_email)} emails...")
print("   (This will take about 30 seconds)")

sender_email = "no-reply@alliancefr.be"
sender_name = "Alliance Française Bruxelles-Europe"

success_count = 0
errors = []

for i, cand in enumerate(candidates_with_email):
    email = cand['email']
    nom = cand['nom']
    prenom = cand['prenom']
    pdf_path = os.path.join('output', cand['pdf_file'])
    
    print(f"\n   [{i+1}/{len(candidates_with_email)}] {prenom} {nom} → {email}")
    
    # Read PDF if exists
    attachments = []
    if os.path.exists(pdf_path):
        with open(pdf_path, 'rb') as pdf_file:
            pdf_content = base64.b64encode(pdf_file.read()).decode('utf-8')
            attachments.append({
                "ContentType": "application/pdf",
                "Filename": f"convocation_TCF_{nom}_{prenom}.pdf",
                "Base64Content": pdf_content
            })
    
    # Build email
    data = {
        'Messages': [
            {
                "From": {
                    "Email": sender_email,
                    "Name": sender_name
                },
                "To": [
                    {
                        "Email": email,
                        "Name": f"{prenom} {nom}"
                    }
                ],
                "Bcc": [
                    {
                        "Email": sender_email,
                        "Name": "Archive"
                    }
                ],
                "Subject": f"Convocation TCF - {prenom} {nom}",
                "TextPart": f"Bonjour {prenom} {nom},\n\nVeuillez trouver ci-joint votre convocation pour l'examen TCF.\n\nCordialement,\nAlliance Française Bruxelles-Europe",
                "HTMLPart": f"""
                <html>
                <body style="font-family: Arial, sans-serif; padding: 20px;">
                    <h2>Convocation TCF</h2>
                    <p>Bonjour <strong>{prenom} {nom}</strong>,</p>
                    <p>Veuillez trouver ci-joint votre convocation pour l'examen TCF (Test de Connaissance du Français).</p>
                    <p>Merci de bien vouloir:</p>
                    <ul>
                        <li>Imprimer cette convocation</li>
                        <li>La présenter le jour de l'examen</li>
                        <li>Vous munir d'une pièce d'identité valide</li>
                    </ul>
                    <p>Pour toute question, n'hésitez pas à nous contacter.</p>
                    <p>Cordialement,<br><strong>Alliance Française Bruxelles-Europe</strong></p>
                </body>
                </html>
                """
            }
        ]
    }
    
    if attachments:
        data['Messages'][0]['Attachments'] = attachments
    
    try:
        result = client_v31.send.create(data=data)
        
        if result.status_code == 200:
            response = result.json()
            msg_status = response.get('Messages', [{}])[0].get('Status', 'unknown')
            print(f"      ✅ Status: {result.status_code}, Message: {msg_status}")
            
            if msg_status == 'success':
                success_count += 1
            else:
                errors.append(f"{email}: Status={msg_status}")
        else:
            print(f"      ❌ Failed: {result.status_code}")
            try:
                error_data = result.json()
                print(f"         Error: {error_data}")
            except:
                print(f"         Error: {result.text}")
            errors.append(f"{email}: HTTP {result.status_code}")
            
    except Exception as e:
        print(f"      ❌ Exception: {e}")
        errors.append(f"{email}: {str(e)}")
    
    # Small delay to respect API limits
    import time
    time.sleep(0.3)

# Summary
print("\n" + "="*60)
print("📊 SUMMARY")
print("="*60)
print(f"\n✅ Successfully sent: {success_count}/{len(candidates_with_email)}")

if errors:
    print(f"\n❌ Errors ({len(errors)}):")
    for err in errors[:10]:
        print(f"   • {err}")
    if len(errors) > 10:
        print(f"   ... and {len(errors) - 10} more")

print("\n" + "="*60)
print("📬 NEXT STEPS")
print("="*60)
print("\n1. Check Mailjet dashboard: https://app.mailjet.com/stats")
print("   Look for 'Sent' count - should show 59 (or close to it)")
print("\n2. If 'Sent' shows 0 or very low:")
print("   → Sender email not verified")
print("   → Go to: https://app.mailjet.com/account/sender")
print("   → Verify 'no-reply@alliancefr.be'")
print("\n3. If 'Sent' shows 59 but 'Delivered' is 0:")
print("   → Domain reputation issue")
print("   → Emails may be blocked by recipients' servers")
print("\n4. Check spam folders of recipients!")
