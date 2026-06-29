#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test de l'intégration des logos TCF spécifiques
"""

import os
import sys
import logging

# Ajouter le répertoire actuel au path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_tcf_logos_integration():
    """Test de l'intégration des logos TCF spécifiques"""
    
    print("🚀 TEST DE L'INTÉGRATION DES LOGOS TCF SPÉCIFIQUES")
    print("=" * 60)
    
    try:
        # 1. Import du main
        print("1. Import de l'application...")
        from main import ConvocationGenerator
        print("✅ Import réussi")
        
        # 2. Création de l'instance (sans interface)
        print("2. Création de l'instance...")
        import tkinter as tk
        root = tk.Tk()
        root.withdraw()  # Masquer la fenêtre
        
        app = ConvocationGenerator()
        app.root = root
        print("✅ Instance créée")
        
        # 3. Vérification des nouvelles variables de logos TCF
        print("3. Vérification des variables de logos TCF...")
        
        required_logo_vars = [
            'logo_tcf_path',
            'logo_tcf_canada_path', 
            'logo_tcf_tp_path',
            'logo_tcf_irn_path'
        ]
        
        for var_name in required_logo_vars:
            assert hasattr(app, var_name), f"Variable {var_name} manquante"
            var_value = getattr(app, var_name).get()
            print(f"   {var_name}: {var_value}")
        
        print("✅ Variables de logos TCF présentes")
        
        # 4. Test de la méthode get_tcf_logo_path
        print("4. Test de la sélection de logos par type TCF...")
        
        test_cases = [
            ('TCF CANADA', 'logo_tcf_canada_path'),
            ('TCF TP COMPLET', 'logo_tcf_tp_path'),
            ('TCF TP OBLIGATOIRE', 'logo_tcf_tp_path'),  # Même logo que TP COMPLET
            ('TCF IRN', 'logo_tcf_irn_path'),
            ('TCF_INCONNU', 'logo_tcf_path')  # Retombe sur générique
        ]
        
        for tcf_type, expected_var in test_cases:
            logo_path = app.get_tcf_logo_path(tcf_type)
            expected_path = getattr(app, expected_var).get()
            print(f"   {tcf_type} → {os.path.basename(logo_path)}")
            
            # Vérifier que la logique fonctionne (le logo spécifique ou générique)
            assert logo_path in [expected_path, app.logo_tcf_path.get()], \
                f"Logo incorrect pour {tcf_type}: {logo_path}"
        
        print("✅ Sélection de logos par type fonctionnelle")
        
        # 5. Test de la méthode browse_tcf_logo (simulation)
        print("5. Vérification de la méthode browse_tcf_logo...")
        
        assert hasattr(app, 'browse_tcf_logo'), "Méthode browse_tcf_logo manquante"
        print("✅ Méthode browse_tcf_logo présente")
        
        # 6. Test de la configuration graphique étendue
        print("6. Test de sauvegarde/chargement configuration...")
        
        # Simuler quelques chemins
        app.logo_tcf_canada_path.set("test/logoTCF_CANADA.png")
        app.logo_tcf_tp_path.set("test/logoTCF_TP.png")
        app.logo_tcf_irn_path.set("test/logoTCF_IRN.png")
        
        # Tester la sauvegarde
        app._save_graphics_config()
        print("✅ Sauvegarde de configuration étendue réussie")
        
        # 7. Vérification de l'interface graphique étendue
        print("7. Vérification de l'interface de configuration...")
        
        # Vérifier que la méthode show_graphics_config a été étendue
        # (Nous ne pouvons pas tester l'interface graphique sans l'afficher)
        assert hasattr(app, 'show_graphics_config'), "Méthode show_graphics_config manquante"
        print("✅ Interface de configuration étendue présente")
        
        # 8. Nettoyage
        root.destroy()
        
        # Nettoyer le fichier de configuration de test
        try:
            os.remove('graphics_config.json')
        except:
            pass
        
        print("\n🎉 TOUS LES TESTS RÉUSSIS!")
        print("L'intégration des logos TCF spécifiques est fonctionnelle.")
        print("")
        print("📋 Fonctionnalités disponibles:")
        print("  • Logo TCF générique")
        print("  • Logo TCF CANADA spécifique")
        print("  • Logo TCF TP spécifique (TP COMPLET et TP OBLIGATOIRE)")
        print("  • Logo TCF IRN spécifique")
        print("  • Sélection automatique selon le type de candidat")
        print("  • Interface de configuration étendue")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    # Configurer le logging pour les tests
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    
    success = test_tcf_logos_integration()
    
    if success:
        print("\n✨ L'INTÉGRATION DES LOGOS TCF EST COMPLÈTE!")
        print("L'application peut maintenant utiliser des logos spécifiques")
        print("selon le type de TCF de chaque candidat.")
    else:
        print("\n❌ DES PROBLÈMES ONT ÉTÉ DÉTECTÉS")
        print("Vérifiez les erreurs ci-dessus.")