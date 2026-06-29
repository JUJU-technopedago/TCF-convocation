#!/usr/bin/env python3
"""
Script de diagnostic pour ConvocationGenerator
"""
import sys
import traceback

print("=== DIAGNOSTIC CONVOCATION GENERATOR ===")
print(f"Python version: {sys.version}")
print(f"Python executable: {sys.executable}")
print()

try:
    print("1. Test des imports de base...")
    import tkinter as tk
    print("✅ tkinter: OK")
    
    import pandas
    print(f"✅ pandas: {pandas.__version__}")
    
    import jinja2
    print("✅ jinja2: OK")
    
    import cryptography
    print(f"✅ cryptography: {cryptography.__version__}")
    
    print()
    print("2. Test de création d'une fenêtre Tkinter simple...")
    
    # Test fenêtre simple
    root = tk.Tk()
    root.title("Test Tkinter")
    root.geometry("300x200")
    
    label = tk.Label(root, text="Test réussi !")
    label.pack(pady=50)
    
    # Fermer automatiquement après 2 secondes
    root.after(2000, root.destroy)
    
    print("✅ Fenêtre créée, affichage pendant 2 secondes...")
    root.mainloop()
    print("✅ Fenêtre fermée normalement")
    
    print()
    print("3. Test d'import du module main...")
    import main
    print("✅ Module main importé")
    
    print()
    print("4. Test de création de l'application...")
    app = main.ConvocationGenerator()
    print("✅ Application créée")
    
    print()
    print("5. Test des composants de l'application...")
    if hasattr(app, 'root'):
        print("✅ Interface root créée")
    else:
        print("❌ Interface root manquante")
        
    if hasattr(app, 'setup_ui'):
        print("✅ Méthode setup_ui trouvée")
    else:
        print("❌ Méthode setup_ui manquante")
    
    print()
    print("=== DIAGNOSTIC TERMINE ===")
    print("Si tout est ✅, l'application devrait fonctionner")
    
except Exception as e:
    print(f"❌ ERREUR: {e}")
    print()
    print("=== TRACEBACK COMPLET ===")
    traceback.print_exc()
    print()
    print("=== DIAGNOSTIC ECHOUE ===")
    sys.exit(1)