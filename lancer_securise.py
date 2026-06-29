import tkinter as tk
import sys
import traceback

def launch_app_safe():
    """Lance l'application avec gestion d'erreur complète"""
    print("=== LANCEMENT SÉCURISÉ CONVOCATION GENERATOR ===")
    
    try:
        print("1. Import du module main...")
        import main
        print("✅ Module main importé")
        
        print("2. Création de l'application...")
        app = main.ConvocationGenerator()
        print("✅ Application créée")
        
        print("3. Vérification de l'interface...")
        if not hasattr(app, 'root'):
            print("❌ ERREUR: Pas d'attribut 'root' dans l'application")
            return
            
        root = app.root
        print(f"✅ Root trouvé: {root}")
        
        # Vérifications de base
        try:
            title = root.title()
            print(f"✅ Titre: {title}")
        except Exception as e:
            print(f"❌ Erreur titre: {e}")
            
        try:
            geometry = root.geometry()
            print(f"✅ Géométrie: {geometry}")
        except Exception as e:
            print(f"❌ Erreur géométrie: {e}")
        
        # Force l'affichage
        try:
            print("4. Force l'affichage...")
            root.lift()
            root.attributes('-topmost', True)
            root.focus_force()
            root.update()
            print("✅ Commandes d'affichage exécutées")
        except Exception as e:
            print(f"❌ Erreur affichage: {e}")
        
        print("5. Démarrage de la boucle principale...")
        print("   L'APPLICATION DEVRAIT MAINTENANT ÊTRE VISIBLE")
        print("   Fermez-la normalement pour voir les logs de fin")
        
        # Lancement avec try/catch
        try:
            app.run()
            print("✅ Application fermée normalement")
        except tk.TclError as e:
            print(f"❌ Erreur Tkinter: {e}")
            traceback.print_exc()
        except KeyboardInterrupt:
            print("⚠️  Interruption clavier")
            root.destroy()
        except Exception as e:
            print(f"❌ Erreur durant l'exécution: {e}")
            traceback.print_exc()
            
    except ImportError as e:
        print(f"❌ Erreur d'import: {e}")
        traceback.print_exc()
    except Exception as e:
        print(f"❌ Erreur générale: {e}")
        traceback.print_exc()
    
    print("=== FIN DU LANCEMENT SÉCURISÉ ===")

if __name__ == "__main__":
    launch_app_safe()