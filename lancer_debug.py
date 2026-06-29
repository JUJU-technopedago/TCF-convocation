import sys
import main

print("=== LANCEMENT AVEC DEBUG ===")

print("1. Création de l'application...")
app = main.ConvocationGenerator()
print("✅ Application créée")

print("2. Vérification de l'interface...")
if hasattr(app, 'root'):
    print(f"✅ Fenêtre root: {app.root}")
    print(f"✅ Titre: {app.root.title()}")
    
    # Force la fenêtre au premier plan
    app.root.lift()
    app.root.attributes('-topmost', True)
    app.root.after(100, lambda: app.root.attributes('-topmost', False))
    
    # Centre la fenêtre sur l'écran
    app.root.update_idletasks()
    width = app.root.winfo_width()
    height = app.root.winfo_height()
    x = (app.root.winfo_screenwidth() // 2) - (width // 2)
    y = (app.root.winfo_screenheight() // 2) - (height // 2)
    app.root.geometry(f'{width}x{height}+{x}+{y}')
    
    print(f"✅ Fenêtre positionnée: {app.root.geometry()}")
else:
    print("❌ Pas de fenêtre root trouvée")

print("3. Démarrage de l'application...")
print("   (La fenêtre devrait maintenant être visible)")

try:
    app.run()
    print("✅ Application fermée normalement")
except Exception as e:
    print(f"❌ Erreur: {e}")
    import traceback
    traceback.print_exc()