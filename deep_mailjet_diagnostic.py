#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Deep diagnostic tool for Mailjet configuration - check EVERYTHING
"""

import json
import os
import sys
from pathlib import Path

print("="*60)
print("🔍 MAILJET DEEP DIAGNOSTIC")
print("="*60)

# 1. Check config files
print("\n1. Checking config files...")
config_file = "mailjet_config.json"
key_file = "mailjet.key"

if os.path.exists(config_file):
    print(f"   ✅ {config_file} exists")
    # Read encrypted config
    with open(config_file, 'rb') as f:
        data = f.read()
        print(f"   📦 Config size: {len(data)} bytes")
else:
    print(f"   ❌ {config_file} NOT FOUND")

if os.path.exists(key_file):
    print(f"   ✅ {key_file} exists")
else:
    print(f"   ❌ {key_file} NOT FOUND")

# 2. Try to decrypt and get credentials
print("\n2. Attempting to decrypt credentials...")
try:
    from mailjet_bridge import MailjetSecurityManager
    security = MailjetSecurityManager()
    
    # Try to decrypt with common password
    # Based on logs, seems like there's a password
    password = "alliance2024"  # Common password pattern
    
    try:
        credentials = security.decrypt_credentials(password)
        api_key = credentials.get("api_key", "")
        secret_key = credentials.get("secret_key", "")
        
        print(f"   ✅ Credentials decrypted!")
        print(f"   📌 API Key: {api_key[:15]}...{api_key[-5:] if len(api_key) > 20 else ''}")
        print(f"   📌 Secret Key: {secret_key[:15]}...{secret_key[-5:] if len(secret_key) > 20 else ''}")
        
        # 3. Test authentication
        print("\n3. Testing Mailjet authentication...")
        from mailjet_rest import Client
        
        # Test with v3 endpoint (for account info)
        test_client = Client(auth=(api_key, secret_key), version='v3')
        result = test_client.sender.get()
        
        print(f"   📡 Response Status: {result.status_code}")
        
        if result.status_code == 200:
            print(f"   ✅ Authentication SUCCESSFUL!")
            data = result.json()
            print(f"   📊 Response: {data}")
            
            # Check senders
            if 'Data' in data and len(data['Data']) > 0:
                print(f"\n   📧 Verified Senders:")
                for sender in data['Data']:
                    email = sender.get('Email', 'N/A')
                    status = sender.get('Status', 'N/A')
                    print(f"      • {email} - Status: {status}")
                    
            # 4. Check if sender email is verified
            print("\n4. Checking sender email status...")
            sender_email = "no-reply@alliancefr.be"
            found_sender = False
            
            if 'Data' in data:
                for sender in data['Data']:
                    if sender.get('Email') == sender_email:
                        found_sender = True
                        sender_status = sender.get('Status')
                        print(f"   📧 Sender: {sender_email}")
                        print(f"   📌 Status: {sender_status}")
                        
                        if sender_status != 'Active':
                            print(f"\n   ⚠️  WARNING: Sender is NOT ACTIVE!")
                            print(f"   ⚠️  Emails may not be delivered!")
                        else:
                            print(f"   ✅ Sender is ACTIVE")
                            
            if not found_sender:
                print(f"   ❌ Sender {sender_email} NOT FOUND in verified senders!")
                print(f"   ⚠️  This is likely why emails are not being received!")
                
            # 5. Check account status
            print("\n5. Checking account status...")
            account_result = test_client.user.get()
            if account_result.status_code == 200:
                account_data = account_result.json()
                print(f"   📊 Account Data: {account_data}")
                
                if 'Data' in account_data and len(account_data['Data']) > 0:
                    user = account_data['Data'][0]
                    max_emails = user.get('MaxAllowedAPIKeys', 'N/A')
                    print(f"   📊 Max Allowed API Keys: {max_emails}")
                    
            # 6. Try sending a test email
            print("\n6. Attempting to send test email...")
            test_recipient = "zermitt@gmail.com"  # One of the test addresses
            
            send_client = Client(auth=(api_key, secret_key), version='v3.1')
            
            email_data = {
                'Messages': [
                    {
                        "From": {
                            "Email": sender_email,
                            "Name": "Alliance Française - TEST"
                        },
                        "To": [
                            {
                                "Email": test_recipient,
                                "Name": "Test User"
                            }
                        ],
                        "Subject": "TEST DIAGNOSTIC - Mailjet Configuration",
                        "TextPart": "This is a diagnostic test email. If you receive this, Mailjet is configured correctly.",
                        "HTMLPart": "<h3>Mailjet Diagnostic Test</h3><p>This is a diagnostic test email.</p><p><strong>If you receive this, Mailjet is configured correctly.</strong></p><p>Time: " + str(datetime.now()) + "</p>"
                    }
                ]
            }
            
            from datetime import datetime
            email_data['Messages'][0]['HTMLPart'] = email_data['Messages'][0]['HTMLPart'].replace(str(datetime.now()), datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            
            send_result = send_client.send.create(data=email_data)
            print(f"   📡 Send Status: {send_result.status_code}")
            print(f"   📊 Response: {send_result.json()}")
            
            if send_result.status_code == 200:
                print(f"\n   ✅ Email sent successfully!")
                response_data = send_result.json()
                
                if 'Messages' in response_data and len(response_data['Messages']) > 0:
                    msg = response_data['Messages'][0]
                    msg_status = msg.get('Status')
                    print(f"   📌 Message Status: {msg_status}")
                    
                    if msg_status == 'success':
                        print(f"\n   🎉 SUCCESS! Email should be delivered!")
                        print(f"\n   👉 Check spam folder if not in inbox!")
                        print(f"   👉 Check Mailjet dashboard: https://app.mailjet.com/stats")
                    else:
                        print(f"\n   ⚠️  Message status is '{msg_status}' - may not be delivered!")
            else:
                print(f"\n   ❌ Send failed!")
                try:
                    error_data = send_result.json()
                    print(f"   📊 Error: {error_data}")
                except:
                    print(f"   📊 Error: {send_result.text}")
                    
        else:
            print(f"   ❌ Authentication FAILED!")
            print(f"   📊 Response: {result.json()}")
            
    except ValueError as e:
        print(f"   ❌ Wrong password or corrupted config: {e}")
        print(f"\n   💡 TIP: Check the password used in main.py")
        
except Exception as e:
    print(f"   ❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*60)
print("🏁 DIAGNOSTIC COMPLETE")
print("="*60)
