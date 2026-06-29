import json

with open('output/candidate_pdf_registry.json', encoding='utf-8') as f:
    registry = json.load(f)

print(f"Total candidates: {len(registry)}")

with_email = {k: v for k, v in registry.items() if v.get('candidate_info', {}).get('email', '').strip() != ''}
print(f"With emails: {len(with_email)}")

print("\nFirst 10 emails:")
for k in list(with_email.keys())[:10]:
    email = registry[k]['candidate_info']['email']
    nom = registry[k]['candidate_info'].get('nom', '')
    prenom = registry[k]['candidate_info'].get('prenom', '')
    print(f"  {prenom} {nom}: {email}")
