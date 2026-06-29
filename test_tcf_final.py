#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def test_tcf_email_final():
    """Test final du contenu TCF avec les bonnes limites"""
    
    # Lire le contenu du fichier mailjet_bridge.py
    with open(r'c:\Users\JMM\Desktop\convoc generator TCF\mailjet_bridge.py', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    print("=== Vérification FINALE des liens mailto dans le code TCF ===")
    
    # La section TCF va de la ligne 645 à 733 (basé sur notre lecture précédente)
    tcf_start = 644  # Index 0-based pour ligne 645
    tcf_end = 733    # Index 0-based pour ligne 734 (le else:)
    
    print(f"Analyse de la section TCF: lignes {tcf_start+1} à {tcf_end}")
    
    # Extraire la section TCF
    tcf_section = ''.join(lines[tcf_start:tcf_end])
    
    # Vérifier la présence des liens mailto dans la section TCF
    html_mailto = 'href="mailto:examens@alliancefr.be"' in tcf_section
    text_contact = 'nous contacter (examens@alliancefr.be)' in tcf_section
    
    print(f"HTML contient 'href=\"mailto:examens@alliancefr.be\"': {html_mailto}")
    print(f"TEXTE contient 'nous contacter (examens@alliancefr.be)': {text_contact}")
    
    if html_mailto and text_contact:
        print("✅ SUCCESS: Les liens mailto sont présents dans la section TCF!")
        
        # Montrer les lignes exactes
        print(f"\n=== Lignes contenant les liens mailto ===")
        for i in range(tcf_start, tcf_end):
            line = lines[i]
            if 'mailto:examens@alliancefr.be' in line:
                print(f"HTML - Ligne {i+1}: {line.strip()}")
            if 'nous contacter (examens@alliancefr.be)' in line:
                print(f"TEXTE - Ligne {i+1}: {line.strip()}")
        
        return True
    else:
        print("❌ FAIL: Les liens mailto sont manquants dans la section TCF")
        
        # Chercher ce qui existe
        print(f"\n=== Recherche dans la section TCF (lignes {tcf_start+1}-{tcf_end}) ===")
        for i in range(tcf_start, tcf_end):
            line = lines[i]
            if 'mailto' in line.lower() or 'examens@' in line.lower() or 'nous contacter' in line.lower():
                print(f"Ligne {i+1}: {line.strip()}")
        
        return False

if __name__ == "__main__":
    test_tcf_email_final()