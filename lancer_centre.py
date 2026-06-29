import tkinter as tk
import main

def launch_centered():
    """Lance l'application centrée sur l'écran principal"""
    print("=== LANCEMENT CENTRÉ FORCÉ ===")
    
    # Créer l'application
    app = main.ConvocationGenerator()
    root = app.root
    
    # Force la géométrie au centre de l'écran
    root.update_idletasks()  # Assure que les dimensions sont calculées
    
    # Récupère les dimensions de l'écran
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    # Dimensions de la fenêtre
    window_width = 900
    window_height = 700
    
    # Centre la fenêtre
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    
    # Force la position
    geometry = f"{window_width}x{window_height}+{x}+{y}"
    root.geometry(geometry)
    
    print(f"Écran: {screen_width}x{screen_height}")
    print(f"Fenêtre: {geometry}")
    
    # Maximise les chances d'affichage
    root.deiconify()  # Assure que la fenêtre n'est pas minimisée
    root.lift()       # Met au premier plan
    root.focus_force() # Force le focus
    root.attributes('-topmost', True)  # Temporairement au-dessus
    
    # Retire le topmost après 500ms
    root.after(500, lambda: root.attributes('-topmost', False))
    
    # Couleur temporaire pour debug
    root.configure(bg='lightgreen')
    
    print("✅ FENÊTRE VERTE DEVRAIT ÊTRE VISIBLE AU CENTRE DE L'ÉCRAN")
    print("✅ Si vous ne la voyez pas, vérifiez:")
    print("   - Alt+Tab pour voir les fenêtres ouvertes")
    print("   - Barre des tâches")
    print("   - Écrans multiples")
    
    try:
        app.run()
    except KeyboardInterrupt:
        print("Fermé par Ctrl+C")
        root.destroy()

if __name__ == "__main__":
    launch_centered()