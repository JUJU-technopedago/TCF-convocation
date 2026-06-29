"""
Script pour installer automatiquement toutes les dépendances requises
"""
import subprocess
import sys
import os

def install_package(package):
    """Installe un package Python via pip"""
    try:
        print(f"📦 Installation de {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✅ {package} installé avec succès")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur lors de l'installation de {package}: {e}")
        return False

def main():
    """Installe toutes les dépendances requises"""
    print("🚀 INSTALLATION DES DÉPENDANCES")
    print("=" * 50)
    
    # Liste des packages requis
    required_packages = [
        "msal>=1.24.0",
        "keyring>=24.0.0", 
        "flask>=2.3.0",
        "requests>=2.31.0"
    ]
    
    # Installer depuis requirements.txt si disponible
    requirements_file = "requirements.txt"
    if os.path.exists(requirements_file):
        print(f"📋 Installation depuis {requirements_file}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", requirements_file])
            print("✅ Toutes les dépendances installées depuis requirements.txt")
            return
        except subprocess.CalledProcessError:
            print("⚠️ Erreur avec requirements.txt, installation manuelle...")
    
    # Installation manuelle
    failed_packages = []
    for package in required_packages:
        if not install_package(package):
            failed_packages.append(package)
    
    print("\n" + "=" * 50)
    if failed_packages:
        print(f"❌ Packages non installés: {', '.join(failed_packages)}")
        print("Essayez d'installer manuellement avec:")
        for pkg in failed_packages:
            print(f"   pip install {pkg}")
    else:
        print("🎉 Toutes les dépendances sont installées!")
        print("Vous pouvez maintenant utiliser oauth_entraid.py")

if __name__ == "__main__":
    main()
