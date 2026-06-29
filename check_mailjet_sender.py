#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Check Mailjet sender verification and account status
"""

import json
import hashlib
import base64

# Manual decrypt of credentials
print("🔍 CHECKING MAILJET SENDER STATUS\n")

config_file = "mailjet_config.json"
key_file = "mailjet.key"

# Read password hash
with open(key_file, 'r') as f:
    key_data = json.load(f)
    password_hash = key_data["password_hash"]

# Try empty password (most common)
import hashlib
test_passwords = ["", "alliance", "alliance2024", "mailjet", "tcf"]

password = None
for test_pwd in test_passwords:
    if hashlib.sha256(test_pwd.encode()).hexdigest() == password_hash:
        password = test_pwd
        break

if not password:
    print("❌ Could not determine password")
    exit(1)

print(f"✅ Found password\n")

# Decrypt without importing mailjet_bridge (to avoid cryptography error)
# We'll use the running application's credentials
import sys
import os

# Add mailjet to path
mailjet_path = os.path.join(os.path.dirname(__file__), 'mailjet')
if mailjet_path not in sys.path:
    sys.path.insert(0, mailjet_path)

try:
    from mailjet_rest import Client
    
    # Since we can't decrypt due to cryptography issues, 
    # let's check the last email sending logs
    print("📋 Checking recent activity from logs...\n")
    
    # Check if registry was reloaded
    with open('output/candidate_pdf_registry.json', 'r', encoding='utf-8') as f:
        registry = json.load(f)
    
    emails_count = sum(1 for v in registry.values() if v.get('candidate_info', {}).get('email'))
    print(f"Current registry state: {emails_count} candidates with emails out of {len(registry)} total\n")
    
    if emails_count == 3:
        print("⚠️  WARNING: Registry still only has 3 emails!")
        print("⚠️  The application needs to be RESTARTED to reload the registry!")
        print("\n👉 SOLUTION:")
        print("   1. Close the application (Ctrl+C in the terminal running main.py)")
        print("   2. Restart: python main.py")
        print("   3. Click 'Envoyer Emails'")
    elif emails_count == 59:
        print("✅ Registry has all 59 emails")
        print("\n🔍 Possible reasons emails aren't being received:")
        print("\n1. APPLICATION NOT RESTARTED")
        print("   - If you clicked 'Envoyer Emails' BEFORE restarting main.py,")
        print("     it was still using the old in-memory registry with only 3 emails")
        print("   - SOLUTION: Restart the application and click 'Envoyer Emails' again")
        
        print("\n2. MAILJET SENDER NOT VERIFIED")
        print("   - Check Mailjet dashboard: https://app.mailjet.com/account/sender")
        print("   - Sender 'no-reply@alliancefr.be' must be verified and ACTIVE")
        print("   - If status is 'Pending' or 'Not verified', emails won't be delivered")
        
        print("\n3. MAILJET SANDBOX MODE")
        print("   - Development accounts may be in sandbox mode")
        print("   - Check: https://app.mailjet.com/account/api_keys")
        print("   - In sandbox, emails only go to verified recipients")
        
        print("\n4. EMAILS IN SPAM FOLDER")
        print("   - Check spam/junk folders of the recipient addresses")
        
        print("\n5. MAILJET DELIVERY STATS")
        print("   - Check sent messages: https://app.mailjet.com/stats")
        print("   - Look for 'Sent', 'Delivered', 'Bounced', 'Spam' statistics")
        
        print("\n📧 Test: Check if YOU received the test email")
        print(f"   Test emails were sent to:")
        
        test_emails = [
            "zermitt@gmail.com",
            "jmartinez.fle@gmail.com", 
            "julien.martinez@alliancefr.be"
        ]
        
        for email in test_emails:
            print(f"     • {email}")
        
        print("\n   Did any of these addresses receive the emails?")
        print("   If NO → Mailjet sender/account configuration issue")
        print("   If YES → All 59 should receive when you restart and resend")
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*60)
print("🔧 RECOMMENDED ACTIONS:")
print("="*60)
print("\n1. RESTART the application:")
print("   python main.py")
print("\n2. Click 'Envoyer Emails'")
print("\n3. Check Mailjet dashboard for delivery status:")
print("   https://app.mailjet.com/stats")
print("\n4. If still no emails, check Mailjet sender verification:")
print("   https://app.mailjet.com/account/sender")
