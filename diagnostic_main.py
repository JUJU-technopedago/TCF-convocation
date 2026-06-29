import sys
import traceback

try:
    print("🧪 DIAGNOSTIC MAIN.PY")
    print("=" * 40)
    
    print("📦 Test des imports...")
    import tkinter as tk
    print("✅ tkinter OK")
    
    import main
    print("✅ main.py importé")
    
    print("\n🚀 Tentative de création de l'application...")
    app = main.ConvocationGenerator()
    print("✅ Application créée")
    
    print("🔍 Vérification de la fenêtre...")
    if hasattr(app, 'root') and app.root:
        print(f"✅ Root trouvé: {app.root}")
        print(f"✅ Géométrie: {app.root.geometry()}")
        
        # Force l'affichage
        app.root.deiconify()
        app.root.lift()
        app.root.focus_force()
        app.root.update()
        
        print("✅ Application prête - test de 3 secondes...")
        app.root.after(3000, lambda: app.root.quit())
        app.root.mainloop()
        print("✅ Test terminé")
    else:
        print("❌ Pas de fenêtre root trouvée")
        
except Exception as e:
    print(f"❌ ERREUR: {e}")
    print("\n🔍 TRACEBACK COMPLET:")
    traceback.print_exc()
    
print("\n🎯 Diagnostic terminé")
input("Appuyez sur Entrée pour fermer...")