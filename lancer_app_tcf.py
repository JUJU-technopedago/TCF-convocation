#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script pour lancer l'application avec l'intégration TCF
"""

import os
import sys

# Ajouter le répertoire actuel au path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def lancer_application_tcf():
    """Lance l'application de génération de convocations avec support TCF"""
    
    print("🚀 LANCEMENT DE L'APPLICATION AVEC SUPPORT TCF")
    print("=" * 50)
    
    try:
        # Importer et lancer l'application
        from main import ConvocationGenerator
        
        print("✅ Application chargée avec succès")
        print("Interface disponible:")
        print("  📋 DELF/DALF - Examens traditionnels")
        print("  📋 TCF - Test de Connaissance du Français")
        print("")
        print("🎯 Nouvelles fonctionnalités TCF:")
        print("  • Sélection automatique du template TCF")
        print("  • Support des 4 variantes TCF (CANADA, TP COMPLET, IRN, TP OBLIGATOIRE)")
        print("  • Durées spécifiques par type de TCF")
        print("  • Logo TCF intégré")
        print("")
        print("🔄 Démarrage de l'interface graphique...")
        
        # Créer et lancer l'application
        app = ConvocationGenerator()
        app.root.mainloop()
        
        print("✅ Application fermée normalement")
        
    except KeyboardInterrupt:
        print("\n⚠️ Application interrompue par l'utilisateur")
    except Exception as e:
        print(f"❌ Erreur lors du lancement: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    lancer_application_tcf()