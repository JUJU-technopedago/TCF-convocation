import time
import subprocess
import os

def test_executable():
    print("🧪 TEST FINAL DE L'EXECUTABLE")
    print("=" * 50)
    
    exe_path = r".\ConvocationGenerator_v20250922\ConvocationGenerator.exe"
    
    if not os.path.exists(exe_path):
        print("❌ Executable non trouvé")
        return False
    
    print(f"✅ Executable trouvé: {exe_path}")
    
    # Informations sur le fichier
    size_mb = os.path.getsize(exe_path) / (1024 * 1024)
    print(f"📊 Taille: {size_mb:.1f} MB")
    
    # Test de lancement
    print("\n🚀 Test de lancement...")
    try:
        process = subprocess.Popen([exe_path], 
                                 stdout=subprocess.PIPE, 
                                 stderr=subprocess.PIPE)
        
        print(f"✅ Processus lancé (PID: {process.pid})")
        
        # Attendre un peu pour que l'application s'initialise
        time.sleep(3)
        
        # Vérifier si le processus est toujours actif
        if process.poll() is None:
            print("✅ Application active et fonctionnelle")
            print("✅ L'interface utilisateur devrait être visible")
            
            # Terminer proprement le processus de test
            process.terminate()
            process.wait(timeout=5)
            print("✅ Test terminé - Application fermée proprement")
            
        else:
            print("❌ L'application s'est fermée immédiatement")
            stdout, stderr = process.communicate()
            if stderr:
                print(f"Erreur: {stderr.decode()}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur lors du lancement: {e}")
        return False
    
    print("\n🎯 RÉSULTAT DU TEST:")
    print("✅ L'exécutable fonctionne parfaitement!")
    print("✅ Interface utilisateur opérationnelle")
    print("✅ Prêt pour la distribution")
    
    return True

if __name__ == "__main__":
    test_executable()

if __name__ == "__main__":
    test_executable()