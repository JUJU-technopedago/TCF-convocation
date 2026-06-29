#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Direct test for the time calculation function
"""

from jury_excel_processor import JuryExcelProcessor

def test_time_calculation():
    processor = JuryExcelProcessor("juries_20250825_181821.xlsx")
    
    # Test various time formats that previously caused errors
    test_cases = [
        # Format: (start_time, duration, expected_result)
        ("9:30", "1h20 (collective) + 5-7min (individuelle)", "11:00"),
        ("9h30", "1h40 (collective) + 6-8min (individuelle)", "11:18"),
        ("10:00", "1h45 (collective) + 15min (individuelle)", "12:00"),
        ("10h00", "2h30 (collective) + 20min (individuelle)", "12:50"),
        ("10", "4h (collective) + 30min (individuelle)", "14:30"),
        ("11", "3h30 (collective) + 30min (individuelle)", "15:00"),
        (930, "1h20 (collective) + 5-7min (individuelle)", "11:00"),
        (1030, "1h40 (collective) + 6-8min (individuelle)", "12:18"),
        ("10.30", "1h45 (collective) + 15min (individuelle)", "12:30"),
        # Add some problematic cases that may have caused the errors
        ("9.30", "1h20 (collective) + 5-7min (individuelle)", None),
        ("10,30", "1h40 (collective) + 6-8min (individuelle)", None),
        ("10h30", "1h45 (collective) + 15min (individuelle)", None),
        ("10:3", "2h30 (collective) + 20min (individuelle)", None),
        ("9 h 30", "1h20 (collective) + 5-7min (individuelle)", None),
    ]
    
    print("\nTesting time calculation with various formats:\n")
    print(f"{'Start Time':<15} {'Duration':<40} {'Expected End':<15} {'Actual End':<15} {'Result':<10}")
    print(f"{'-'*15} {'-'*40} {'-'*15} {'-'*15} {'-'*10}")
    
    for start_time, duration, expected_result in test_cases:
        result = processor._calculate_end_time(start_time, duration)
        success = "✅" if result == expected_result or (expected_result is None and result == '') else "❌"
        
        print(f"{str(start_time):<15} {duration:<40} {str(expected_result):<15} {str(result):<15} {success}")
    
    print("\nTest cases completed.")

if __name__ == "__main__":
    test_time_calculation()