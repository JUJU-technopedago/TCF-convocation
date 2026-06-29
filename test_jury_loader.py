#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for loading jury data and time calculation
"""

from jury_excel_processor import JuryExcelProcessor
import sys

def test_jury_processor():
    excel_file = "juries_20250825_181821.xlsx"
    print(f"Testing with Excel file: {excel_file}")
    
    processor = JuryExcelProcessor(excel_file)
    
    # Test various time formats
    test_cases = [
        ("9:30", "1h20 (collective) + 5-7min (individuelle)"),
        ("9h30", "1h40 (collective) + 6-8min (individuelle)"),
        ("10:00", "1h45 (collective) + 15min (individuelle)"),
        ("10h00", "2h30 (collective) + 20min (individuelle)"),
        ("10", "4h (collective) + 30min (individuelle)"),
        ("11", "3h30 (collective) + 30min (individuelle)"),
        (930, "1h20 (collective) + 5-7min (individuelle)"),
        (1030, "1h40 (collective) + 6-8min (individuelle)"),
        ("10.30", "1h45 (collective) + 15min (individuelle)"),
    ]
    
    print("\nTesting time calculation with various formats:")
    for start_time, duration in test_cases:
        result = processor._calculate_end_time(start_time, duration)
        print(f"  Start: {start_time}, Duration: {duration} => End: {result}")
    
    try:
        print("\nLoading jury data...")
        processor.load_jury_data()
        candidates = processor.get_all_candidates()
        
        print(f"Found {len(candidates)} candidates total")
        
        # Display a few examples
        for i, candidate in enumerate(candidates[:5]):
            print(f"\nCandidate {i+1}:")
            print(f"  Name: {candidate['nom']} {candidate['prenom']}")
            print(f"  Level: {candidate['niveau']}")
            print(f"  Special needs: {candidate['besoins_speciaux']}")
            print(f"  Preparation time: {candidate.get('heure_preparation', '')}")
            print(f"  End time: {candidate.get('heure_fin', '')}")
        
        print("\nAll tests completed successfully.")
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_jury_processor()