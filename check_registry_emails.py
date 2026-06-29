import json

# Load registry
with open('output/candidate_pdf_registry.json', 'r', encoding='utf-8') as f:
    registry = json.load(f)

print(f"Total entries in registry: {len(registry)}")

# Count nan emails
nan_count = 0
valid_count = 0

print("\n" + "="*80)
print("EMAIL STATUS IN REGISTRY:")
print("="*80)

for candidate_id, data in list(registry.items())[:10]:
    candidate_info = data.get('candidate_info', {})
    nom = candidate_info.get('nom', '?')
    prenom = candidate_info.get('prenom', '?')
    email = candidate_info.get('email', '?')
    
    if email == 'nan':
        status = "❌ NAN"
        nan_count += 1
    elif '@' in email:
        status = "✅ VALID"
        valid_count += 1
    else:
        status = "⚠️ OTHER"
    
    print(f"{prenom} {nom}: {status} ({email})")

# Count all
all_nan = sum(1 for v in registry.values() if v.get('candidate_info', {}).get('email') == 'nan')
all_valid = sum(1 for v in registry.values() if '@' in str(v.get('candidate_info', {}).get('email', '')))

print("\n" + "="*80)
print(f"TOTAL: {len(registry)} candidates")
print(f"Valid emails: {all_valid}")
print(f"NAN emails: {all_nan}")
print(f"Other: {len(registry) - all_valid - all_nan}")
print("="*80)
