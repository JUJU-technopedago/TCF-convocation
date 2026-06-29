import json
import os

registry_path = "output/candidate_pdf_registry.json"

if not os.path.exists(registry_path):
    print("❌ Registry file not found! PDFs need to be regenerated.")
    exit(1)

with open(registry_path, encoding='utf-8') as f:
    registry = json.load(f)

print(f"Total candidates in registry: {len(registry)}")

with_email = {k: v for k, v in registry.items() if v.get('candidate_info', {}).get('email', '').strip()}
print(f"Candidates WITH valid email: {len(with_email)}")

without_email = len(registry) - len(with_email)
print(f"Candidates WITHOUT email: {without_email}")

if len(with_email) > 0:
    print("\n✅ Sample emails found:")
    for k in list(with_email.keys())[:5]:
        info = registry[k]['candidate_info']
        print(f"  - {info.get('prenom', '')} {info.get('nom', '')}: {info.get('email', '')}")
else:
    print("\n❌ NO EMAILS found in registry!")
    print("The registry was created with the OLD buggy code.")
    print("You need to regenerate PDFs with the fixed code!")
