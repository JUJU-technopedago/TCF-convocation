import json

with open('output/candidate_pdf_registry.json', 'r', encoding='utf-8') as f:
    reg = json.load(f)

emails = [v['candidate_info']['email'] for v in reg.values() if v['candidate_info'].get('email')]

print(f'Registry has {len(emails)} candidates with emails out of {len(reg)} total')
print(f'\nSample emails from registry:')

for i, (cid, info) in enumerate(list(reg.items())[:10]):
    cand = info['candidate_info']
    print(f"  {cand['prenom']} {cand['nom']}: '{cand.get('email', 'NO EMAIL')}'")
