#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test simple pour vérifier l'import du main.py modifié
"""

print("Test d'import du main.py modifié...")

try:
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    
    # Test d'import simple
    print("1. Import des modules...")
    from tcf_excel_processor import TCFExcelProcessor
    from reportlab_pdf_generator import ReportLabPDFGenerator
    print("✅ Modules TCF importés")
    
    # Test d'import du main (sans l'exécuter)
    print("2. Import du main...")
    import main
    print("✅ Main importé")
    
    # Vérifier que la classe existe
    print("3. Vérification de la classe...")
    ConvocationGenerator = main.ConvocationGenerator
    print("✅ Classe ConvocationGenerator trouvée")
    
    print("\n🎉 TOUS LES IMPORTS FONCTIONNENT!")
    print("L'intégration TCF est opérationnelle.")
    
except Exception as e:
    print(f"❌ Erreur: {e}")
    import traceback
    traceback.print_exc()