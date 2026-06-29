#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test pour vérifier que chaque candidat reçoit son propre PDF personnalisé
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tcf_excel_processor import TCFExcelProcessor
from main import ConvocationGenerator
import tempfile
import tkinter as tk

def test_pdf_matching():
    """Test la correspondance entre candidats et PDF"""
    
    print("🧪 TEST : Correspondance candidats-PDF personnalisés")
    print("=" * 60)
    
    # Créer une instance temporaire pour tester
    root = tk.Tk()
    root.withdraw()  # Cacher la fenêtre
    
    app = ConvocationGenerator()
    app.root = root
    
    # Configurer pour TCF
    app.exam_type.set("TCF")
    app.excel_file_path.set("juries_20250919_162205.xlsx")
    app.output_dir.set("output")
    
    try:
        # Charger les candidats TCF
        processor = TCFExcelProcessor("juries_20250919_162205.xlsx")
        processor.load_tcf_data()
        candidates = processor.get_all_candidates()
        
        print(f"📊 Candidats chargés: {len(candidates)}")
        
        # Tester avec les 5 premiers candidats
        test_candidates = candidates[:5]
        
        print(f"\n🔍 Test de correspondance PDF pour {len(test_candidates)} candidats:")
        print("-" * 50)
        
        for i, candidat in enumerate(test_candidates, 1):
            nom = candidat.get('nom', 'INCONNU')
            prenom = candidat.get('prenom', '')
            numero = candidat.get('numero_candidat', 'N/A')
            
            print(f"\n{i}. Candidat: {prenom} {nom}")
            print(f"   Numéro: {numero}")
            
            # Tester la fonction de recherche PDF
            pdf_path, pdf_filename = app._find_pdf_file_robust(candidat, "output")
            
            if pdf_path:
                print(f"   ✅ PDF trouvé: {pdf_filename}")
                print(f"   📁 Chemin: {pdf_path}")
                
                # Vérifier que le PDF existe réellement
                if os.path.exists(pdf_path):
                    file_size = os.path.getsize(pdf_path)
                    print(f"   📊 Taille: {file_size} bytes")
                    
                    # Vérifier que c'est un PDF unique pour ce candidat
                    if nom.lower() in pdf_filename.lower() and prenom.lower() in pdf_filename.lower():
                        print(f"   ✅ PDF correspond au candidat (nom/prénom match)")
                    else:
                        print(f"   ⚠️ PDF pourrait ne pas correspondre au candidat")
                else:
                    print(f"   ❌ Fichier PDF n'existe pas sur le disque")
            else:
                print(f"   ❌ Aucun PDF trouvé pour ce candidat")
                
                # Afficher les patterns qui ont été testés
                print(f"   🔍 Patterns testés:")
                if hasattr(app, 'exam_type') and app.exam_type.get() == "TCF":
                    print(f"     - convocation_tcf_{nom}_{prenom}.pdf")
                    print(f"     - convocation_tcf_{nom.upper()}_{prenom}.pdf")
                else:
                    print(f"     - convocation_{nom}_{prenom}_{numero}.pdf")
        
        print(f"\n" + "=" * 60)
        print("🏁 Test terminé")
        
    except Exception as e:
        print(f"❌ Erreur durant le test: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        root.destroy()

if __name__ == "__main__":
    test_pdf_matching()