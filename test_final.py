import tkinter as tk
from tkinter import messagebox
import main
import sys

def test_final():
    """Test final avec notifications système"""
    print("=== TEST FINAL AVEC NOTIFICATIONS ===")
    
    # Test 1: MessageBox système
    try:
        response = messagebox.askyesno(
            "Test Affichage", 
            "Voyez-vous cette boîte de dialogue ?\n\n"
            "OUI = Continuer le test de l'application\n"
            "NON = Arrêter (problème d'affichage système)"
        )
        
        if not response:
            print("❌ Problème d'affichage système détecté")
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ Erreur messagebox: {e}")
        sys.exit(1)
    
    # Test 2: Application avec messagebox de confirmation
    try:
        app = main.ConvocationGenerator()
        root = app.root
        
        # Centre la fenêtre
        root.geometry("800x600+200+100")
        root.configure(bg='yellow')
        root.title("CONVOCATION GENERATOR - TEST FINAL")
        
        # Ajoute un label visible
        info_label = tk.Label(
            root,
            text="APPLICATION CONVOCATION GENERATOR\n\nSi vous voyez ceci, l'application fonctionne !",
            font=("Arial", 16),
            bg='yellow',
            fg='blue'
        )
        
        # Utilise place pour éviter les conflits de gestionnaire
        info_label.place(x=50, y=50, width=700, height=100)
        
        # Force l'affichage
        root.lift()
        root.focus_force()
        root.attributes('-topmost', True)
        
        print("✅ APPLICATION LANCÉE - FENÊTRE JAUNE DEVRAIT ÊTRE VISIBLE")
        print("✅ Fermez la fenêtre pour continuer")
        
        # Popup de confirmation après 2 secondes
        def show_confirmation():
            try:
                messagebox.showinfo(
                    "Application Active", 
                    "L'application ConvocationGenerator est maintenant active !\n\n"
                    "Vous devriez voir une fenêtre jaune avec du texte bleu.\n\n"
                    "Fermez cette boîte puis fermez l'application."
                )
            except:
                pass
        
        root.after(2000, show_confirmation)
        
        app.run()
        
        print("✅ Application fermée avec succès")
        
    except Exception as e:
        print(f"❌ Erreur application: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_final()