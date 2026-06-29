#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def test_tcf_email_content_precise():
    """Test précis du contenu TCF en lisant directement le fichier"""
    
    # Lire le contenu du fichier mailjet_bridge.py
    with open(r'c:\Users\JMM\Desktop\convoc generator TCF\mailjet_bridge.py', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    print("=== Vérification des liens mailto dans le code TCF ===")
    
    # Chercher la ligne "if is_tcf:"
    tcf_start = -1
    tcf_end = -1
    
    for i, line in enumerate(lines):
        if 'if is_tcf:' in line:
            tcf_start = i
            print(f"Section 'if is_tcf:' trouvée à la ligne {i+1}")
            break
    
    if tcf_start == -1:
        print("❌ Section 'if is_tcf:' non trouvée")
        return False
    
    # Chercher la fin de la section (le "else:")
    for i in range(tcf_start + 1, len(lines)):
        if lines[i].strip().startswith('else:'):
            tcf_end = i
            print(f"Fin de section TCF à la ligne {i+1}")
            break
    
    if tcf_end == -1:
        tcf_end = len(lines)
        print(f"Fin de section TCF à la fin du fichier (ligne {len(lines)})")
    
    # Extraire la section TCF
    tcf_section = ''.join(lines[tcf_start:tcf_end])
    
    print(f"Section TCF analysée: lignes {tcf_start+1} à {tcf_end}")
    
    # Vérifier la présence des liens mailto dans la section TCF
    html_mailto = 'href="mailto:examens@alliancefr.be"' in tcf_section
    text_contact = 'nous contacter (examens@alliancefr.be)' in tcf_section
    
    print(f"HTML contient 'href=\"mailto:examens@alliancefr.be\"': {html_mailto}")
    print(f"TEXTE contient 'nous contacter (examens@alliancefr.be)': {text_contact}")
    
    if html_mailto and text_contact:
        print("✅ SUCCESS: Les liens mailto sont présents dans la section TCF!")
        
        # Montrer les lignes exactes
        for i, line in enumerate(lines[tcf_start:tcf_end], tcf_start+1):
            if 'mailto:examens@alliancefr.be' in line:
                print(f"\nLigne {i}: {line.strip()}")
            if 'nous contacter (examens@alliancefr.be)' in line:
                print(f"Ligne {i}: {line.strip()}")
        
        return True
    else:
        print("❌ FAIL: Les liens mailto sont manquants dans la section TCF")
        
        # Chercher ce qui existe
        print("\n=== Recherche dans la section TCF ===")
        for i, line in enumerate(lines[tcf_start:tcf_end], tcf_start+1):
            if 'mailto' in line.lower() or 'examens@' in line.lower():
                print(f"Ligne {i}: {line.strip()}")
        
        return False

if __name__ == "__main__":
    test_tcf_email_content_precise()