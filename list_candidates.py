#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
List all candidates in the jury file
"""

import sys
import os
from jury_excel_processor import JuryExcelProcessor

def list_candidates():
    # Try both possible Excel files
    excel_files = ["juries_20250825_181821.xlsx", "juries_20250820_192410.xlsx"]
    
    for excel_file in excel_files:
        if not os.path.exists(excel_file):
            print(f"Excel file not found: {excel_file}")
            continue
        
        print(f"\nListing candidates from {excel_file}...")
        processor = JuryExcelProcessor(excel_file)
        
        try:
            processor.load_jury_data()
            candidates = processor.get_all_candidates()
            print(f"Found {len(candidates)} candidates total")
            
            # Display all candidates
            print("\nAll candidates:")
            for i, candidate in enumerate(candidates):
                print(f"{i+1}. {candidate.get('nom', '')} {candidate.get('prenom', '')}")
                
        except Exception as e:
            print(f"Error loading candidates from {excel_file}: {e}")

if __name__ == "__main__":
    list_candidates()