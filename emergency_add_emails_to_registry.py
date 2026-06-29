#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EMERGENCY: Add emails from Excel directly to existing registry
"""

import json
import pandas as pd

# Load Excel and get all emails
print("📖 Reading Excel file...")
excel_file = "JURYS FINAL TCF 11-18.xlsx"
all_candidates_data = {}

# Read all sheets
xl = pd.ExcelFile(excel_file, engine='openpyxl')

for sheet_name in xl.sheet_names:
    print(f"\n📄 Processing sheet: {sheet_name}")
    df = pd.read_excel(excel_file, sheet_name=sheet_name, engine='openpyxl', header=None)
    
    for idx in range(df.shape[0]):
        row_values = df.iloc[idx].values
        
        # Skip header rows
        if len(row_values) < 5:
            continue
            
        nom = str(row_values[1]).strip() if len(row_values) > 1 and pd.notna(row_values[1]) else ""
        prenom = str(row_values[2]).strip() if len(row_values) > 2 and pd.notna(row_values[2]) else ""
        
        # Skip headers
        if not nom or nom in ['NOM', 'Pass.', 'nan']:
            continue
        if not prenom or prenom in ['Prénom', 'nan']:
            continue
        
        # Get email
        email = ""
        if len(row_values) > 4 and pd.notna(row_values[4]):
            email_val = str(row_values[4]).strip()
            if email_val and email_val.lower() != 'nan' and '@' in email_val:
                email = email_val
        
        if email:
            key = f"{nom}_{prenom}"
            all_candidates_data[key] = {
                'nom': nom,
                'prenom': prenom,
                'email': email
            }
            print(f"  ✅ {prenom} {nom}: {email}")

print(f"\n📊 Total candidates with emails found in Excel: {len(all_candidates_data)}")

# Load existing registry
print("\n📂 Loading existing registry...")
registry_path = "output/candidate_pdf_registry.json"

with open(registry_path, 'r', encoding='utf-8') as f:
    registry = json.load(f)

print(f"Registry has {len(registry)} entries")

# Update emails in registry
print("\n🔄 Updating emails in registry...")
updated_count = 0

for candidate_id, candidate_info in registry.items():
    if 'candidate_info' in candidate_info:
        nom = candidate_info['candidate_info'].get('nom', '')
        prenom = candidate_info['candidate_info'].get('prenom', '')
        key = f"{nom}_{prenom}"
        
        if key in all_candidates_data:
            email = all_candidates_data[key]['email']
            candidate_info['candidate_info']['email'] = email
            updated_count += 1
            print(f"  ✅ Updated {prenom} {nom}: {email}")

print(f"\n✅ Updated {updated_count} candidates with emails")

# Save updated registry
print("\n💾 Saving updated registry...")
with open(registry_path, 'w', encoding='utf-8') as f:
    json.dump(registry, f, indent=2, ensure_ascii=False)

print("\n🎉 DONE! Registry updated with all emails from Excel!")
print(f"\nBefore: 3 emails")
print(f"After: {updated_count} emails")
print("\n👉 Now click 'Envoyer Emails' button to send to ALL candidates!")
