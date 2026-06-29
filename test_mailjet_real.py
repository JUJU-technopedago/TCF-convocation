#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test direct Mailjet sending to verify configuration
"""

import os
from mailjet_rest import Client

# Load credentials
api_key = os.getenv('MAILJET_API_KEY')
api_secret = os.getenv('MAILJET_API_SECRET')

if not api_key or not api_secret:
    print("❌ MAILJET_API_KEY or MAILJET_API_SECRET not set in environment")
    exit(1)

print(f"✅ API Key found: {api_key[:10]}...")
print(f"✅ API Secret found: {api_secret[:10]}...")

# Initialize client
mailjet = Client(auth=(api_key, api_secret), version='v3.1')

# Test 1: Check account info
print("\n=== TEST 1: Account Info ===")
try:
    result = mailjet.sender.get()
    print(f"Status: {result.status_code}")
    if result.status_code == 200:
        data = result.json()
        print(f"Response: {data}")
        if 'Data' in data and len(data['Data']) > 0:
            for sender in data['Data']:
                print(f"  Sender: {sender.get('Email')} - Status: {sender.get('Status')}")
    else:
        print(f"Error: {result.text}")
except Exception as e:
    print(f"Error: {e}")

# Test 2: Send a simple test email
print("\n=== TEST 2: Sending Test Email ===")
test_email = "zermitt@gmail.com"  # One of the test addresses from logs
print(f"Sending to: {test_email}")

data = {
    'Messages': [
        {
            "From": {
                "Email": "no-reply@alliancefr.be",
                "Name": "Alliance Française Test"
            },
            "To": [
                {
                    "Email": test_email,
                    "Name": "Test User"
                }
            ],
            "Subject": "TEST - Email System Verification",
            "TextPart": "This is a test email to verify Mailjet configuration. If you receive this, the system is working.",
            "HTMLPart": "<h3>Test Email</h3><p>This is a test email to verify Mailjet configuration.</p><p>If you receive this, the system is working correctly.</p>"
        }
    ]
}

try:
    result = mailjet.send.create(data=data)
    print(f"Status Code: {result.status_code}")
    print(f"Response: {result.json()}")
    
    if result.status_code == 200:
        response_data = result.json()
        if 'Messages' in response_data:
            for msg in response_data['Messages']:
                print(f"\n✅ Message Status: {msg.get('Status')}")
                print(f"   To: {msg.get('To', [{}])[0].get('Email')}")
                print(f"   MessageUUID: {msg.get('To', [{}])[0].get('MessageUUID')}")
                print(f"   MessageID: {msg.get('To', [{}])[0].get('MessageID')}")
                print(f"   MessageHref: {msg.get('To', [{}])[0].get('MessageHref')}")
    else:
        print(f"❌ Error: {result.text}")
        
except Exception as e:
    print(f"❌ Exception: {e}")
    import traceback
    traceback.print_exc()

print("\n=== DIAGNOSTIC COMPLETE ===")
print("\nIf Status = 200 and you still don't receive emails, check:")
print("1. Spam/Junk folders")
print("2. Mailjet account status (sandbox mode?)")
print("3. Sender domain verification status")
print("4. Mailjet dashboard for delivery stats")
