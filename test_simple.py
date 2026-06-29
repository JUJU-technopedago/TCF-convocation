import tkinter as tk
import time
import threading

def test_simple():
    """Test très simple d'affichage Tkinter"""
    print("=== TEST AFFICHAGE TKINTER ===")
    
    root = tk.Tk()
    root.title("TEST VISIBLE")
    root.geometry("300x200+100+100")
    root.configure(bg='red')
    
    # Label visible
    label = tk.Label(root, 
                    text="FENÊTRE TEST\nSi vous voyez ceci,\nTkinter fonctionne !", 
                    font=("Arial", 14, "bold"),
                    bg='red', fg='white')
    label.place(x=50, y=50)  # Utilise place au lieu de pack/grid
    
    # Bouton pour fermer
    btn = tk.Button(root, text="FERMER", command=root.destroy,
                   font=("Arial", 12), bg='white')
    btn.place(x=120, y=150)
    
    # Force l'affichage
    root.lift()
    root.attributes('-topmost', True)
    root.update()
    
    print("✅ Fenêtre rouge créée - VÉRIFIEZ VOTRE ÉCRAN")
    print("   Cliquez sur FERMER pour continuer")
    
    root.mainloop()
    print("✅ Test terminé")

if __name__ == "__main__":
    test_simple()