import tkinter as tk
import main

print("=== TEST FENÊTRE SIMPLE ===")

# Test 1: Fenêtre Tkinter basique
print("1. Test fenêtre Tkinter simple...")
root = tk.Tk()
root.title("Test Simple")
root.geometry("400x300+100+100")
root.configure(bg='yellow')

label = tk.Label(root, text="TEST - Cette fenêtre devrait être visible", 
                 font=("Arial", 16), bg='yellow', fg='red')
label.pack(expand=True)

button = tk.Button(root, text="FERMER", command=root.destroy,
                   font=("Arial", 12), bg='red', fg='white')
button.pack(pady=20)

print("✅ Fenêtre test créée - REGARDEZ VOTRE ÉCRAN")
print("   Une fenêtre JAUNE devrait apparaître")
print("   Cliquez sur FERMER ou fermez-la pour continuer")

root.mainloop()
print("✅ Fenêtre test fermée")

print()
print("2. Test de l'application ConvocationGenerator...")

try:
    app = main.ConvocationGenerator()
    
    # Force l'affichage
    app.root.configure(bg='lightblue')
    app.root.geometry("600x400+200+200")
    app.root.lift()
    app.root.focus_force()
    
    print("✅ Application ConvocationGenerator créée")
    print("   Une fenêtre BLEUE devrait maintenant apparaître")
    
    # Ajouter un label de test
    test_label = tk.Label(app.root, text="APPLICATION CONVOCATION - VISIBLE ?", 
                         font=("Arial", 20), bg='lightblue', fg='darkblue')
    test_label.pack(pady=50)
    
    app.run()
    
except Exception as e:
    print(f"❌ Erreur: {e}")
    import traceback
    traceback.print_exc()