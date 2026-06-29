#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test du main.py modifié pour vérifier l'intégration TCF
"""

import os
import sys
import logging

# Ajouter le répertoire actuel au path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_main_tcf_integration():
    """Test de l'intégration TCF dans main.py"""
    
    print("🚀 TEST DE L'INTÉGRATION TCF DANS MAIN.PY")
    print("=" * 50)
    
    try:
        # 1. Import du main
        print("1. Import de l'application principale...")
        from main import ConvocationGenerator
        
        print("✅ Import réussi")
        
        # 2. Création de l'instance (sans démarrer l'interface)
        print("2. Création de l'instance ConvocationGenerator...")
        
        # Créer une instance sans afficher l'interface
        import tkinter as tk
        root = tk.Tk()
        root.withdraw()  # Masquer la fenêtre
        
        app = ConvocationGenerator()
        app.root = root  # Remplacer par notre root masqué
        
        print("✅ Instance créée")
        
        # 3. Test des variables TCF
        print("3. Vérification des variables TCF...")
        
        # Vérifier que les nouvelles variables existent
        assert hasattr(app, 'exam_type'), "Variable exam_type manquante"
        assert hasattr(app, 'logo_tcf_path'), "Variable logo_tcf_path manquante"
        
        print(f"   exam_type: {app.exam_type.get()}")
        print(f"   logo_tcf_path: {app.logo_tcf_path.get()}")
        
        print("✅ Variables TCF présentes")
        
        # 4. Test du changement de type d'examen
        print("4. Test du changement vers TCF...")
        
        original_template = app.template_path.get()
        print(f"   Template original: {original_template}")
        
        app.exam_type.set("TCF")
        app.on_exam_type_changed()
        
        new_template = app.template_path.get()
        print(f"   Nouveau template: {new_template}")
        
        assert "tcf" in new_template.lower(), f"Template TCF non défini: {new_template}"
        
        print("✅ Changement vers TCF fonctionnel")
        
        # 5. Test du retour vers DELF
        print("5. Test du retour vers DELF/DALF...")
        
        app.exam_type.set("DELF/DALF")
        app.on_exam_type_changed()
        
        delf_template = app.template_path.get()
        print(f"   Template DELF: {delf_template}")
        
        assert "delf" in delf_template.lower(), f"Template DELF non défini: {delf_template}"
        
        print("✅ Changement vers DELF/DALF fonctionnel")
        
        # 6. Test des méthodes de génération
        print("6. Vérification des méthodes de génération...")
        
        assert hasattr(app, '_generate_tcf_pdfs'), "Méthode _generate_tcf_pdfs manquante"
        assert hasattr(app, '_generate_delf_pdfs'), "Méthode _generate_delf_pdfs manquante"
        
        print("✅ Méthodes de génération présentes")
        
        # 7. Nettoyage
        root.destroy()
        
        print("\n🎉 TOUS LES TESTS RÉUSSIS!")
        print("L'intégration TCF dans main.py est fonctionnelle.")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    # Configurer le logging pour les tests
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    
    success = test_main_tcf_integration()
    
    if success:
        print("\n✨ L'APPLICATION EST PRÊTE POUR LES EXAMENS TCF!")
        print("Vous pouvez maintenant lancer l'application avec:")
        print("python main.py")
    else:
        print("\n❌ DES PROBLÈMES ONT ÉTÉ DÉTECTÉS")
        print("Vérifiez les erreurs ci-dessus avant de lancer l'application.")