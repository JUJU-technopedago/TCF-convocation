#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test du processeur de jurys
"""

from jury_excel_processor import JuryExcelProcessor

def test_processor():
    processor = JuryExcelProcessor('test_juries.xlsx')
    
    try:
        processor.load_jury_data()
        candidates = processor.get_all_candidates()
        
        print(f"Trouvé {len(candidates)} candidats")
        
        for i, c in enumerate(candidates[:5]):
            print(f"- {c['nom']} {c['prenom']} ({c['niveau']}) - {c['email']}")
        
        # Test d'export
        count = processor.export_to_standard_excel('candidats_test.xlsx')
        print(f"\n{count} candidats exportés vers candidats_test.xlsx")
        
        return True
        
    except Exception as e:
        print(f"Erreur: {e}")
        return False

if __name__ == "__main__":
    test_processor()
