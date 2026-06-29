#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for the time calculation fix
"""

from jury_excel_processor import JuryExcelProcessor

def test_time_calculation():
    processor = JuryExcelProcessor("juries_20250825_181821.xlsx")
    
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
    
    print("Testing time calculation with various formats:")
    for start_time, duration in test_cases:
        result = processor._calculate_end_time(start_time, duration)
        print(f"  Start: {start_time}, Duration: {duration} => End: {result}")
    
    print("\nAll tests completed.")

if __name__ == "__main__":
    test_time_calculation()