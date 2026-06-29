#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def test_tcf_email_content():
    """Test simple du contenu TCF en lisant directement le fichier"""
    
    # Lire le contenu du fichier mailjet_bridge.py
    with open(r'c:\Users\JMM\Desktop\convoc generator TCF\mailjet_bridge.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("=== Vérification des liens mailto dans le code TCF ===")
    
    # Chercher la section TCF
    tcf_start = content.find('if is_tcf:')
    if tcf_start == -1:
        print("❌ Section 'if is_tcf:' non trouvée")
        return False
        
    tcf_end = content.find('else:', tcf_start)
    if tcf_end == -1:
        tcf_section = content[tcf_start:]
    else:
        tcf_section = content[tcf_start:tcf_end]
    
    print(f"Section TCF trouvée (lignes {tcf_start}-{tcf_end})")
    
    # Vérifier la présence des liens mailto dans la section TCF
    html_mailto = 'mailto:examens@alliancefr.be' in tcf_section
    text_contact = 'nous contacter (examens@alliancefr.be)' in tcf_section
    
    print(f"HTML contient 'mailto:examens@alliancefr.be': {html_mailto}")
    print(f"TEXTE contient 'nous contacter (examens@alliancefr.be)': {text_contact}")
    
    if html_mailto and text_contact:
        print("✅ SUCCESS: Les liens mailto sont présents dans la section TCF!")
        
        # Montrer les extraits
        print("\n=== Extrait HTML ===")
        html_start = tcf_section.find('mailto:examens@alliancefr.be')
        if html_start != -1:
            extract = tcf_section[html_start-50:html_start+100]
            print(f"...{extract}...")
            
        print("\n=== Extrait TEXTE ===")
        text_start = tcf_section.find('nous contacter (examens@alliancefr.be)')
        if text_start != -1:
            extract = tcf_section[text_start-50:text_start+100]
            print(f"...{extract}...")
        
        return True
    else:
        print("❌ FAIL: Les liens mailto sont manquants dans la section TCF")
        return False

if __name__ == "__main__":
    test_tcf_email_content()