#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Find where the import error is occurring
"""

import sys
import traceback

try:
    # Try importing modules that might use the decrepit module
    from mailjet_bridge import MailjetBridge
    print("MailjetBridge imported successfully")
    
    # If we got here, try creating an instance
    bridge = MailjetBridge("dummy.xlsx", "output", "test@example.com", "Test Sender")
    print("MailjetBridge instance created successfully")
    
except ImportError as e:
    print(f"ImportError: {e}")
    traceback.print_exc()
except Exception as e:
    print(f"Other error: {e}")
    traceback.print_exc()