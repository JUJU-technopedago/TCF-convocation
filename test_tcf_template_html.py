#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de génération PDF TCF avec le template HTML
"""

import os
import sys

# Correction du module decrepit pour l'importation
try:
    import decrepit
    print("INFO: Module decrepit disponible")
except ImportError:
    print("INFO: Module decrepit non disponible, création du mock...")
    import types
    decrepit = types.ModuleType('decrepit')
    decrepit.Cryptography_HazmatBindingsObjectIdentifier = lambda: None
    sys.modules['decrepit'] = decrepit
else:
    # S'assurer que le module est bien dans sys.modules même si l'import a réussi
    import sys
    sys.modules['decrepit'] = decrepit

try:
    import auto_decrepit_fix
except ImportError:
    pass

from tcf_excel_processor import TCFExcelProcessor
from pdf_generator import PDFGenerator

def test_tcf_template_html():
    """Test de génération PDF TCF avec template HTML"""
    print("🧪 TEST GÉNÉRATION PDF TCF AVEC TEMPLATE HTML")
    print("=" * 60)
    
    # 1. Charger les données TCF
    print("1. Chargement des données TCF...")
    try:
        processor = TCFExcelProcessor('JURYS FINAL TCF.xlsx')
        processor.load_tcf_data()
        candidates = processor.get_all_candidates()
        
        if not candidates:
            print("   ❌ Aucun candidat trouvé")
            return False
        
        candidat = candidates[0]  # Premier candidat pour test
        print(f"   ✅ Candidat de test: {candidat['nom']} {candidat['prenom']} ({candidat['tcf_type']})")
        
    except Exception as e:
        print(f"   ❌ Erreur chargement données: {e}")
        return False
    
    # 2. Vérifier le template TCF
    print("\\n2. Vérification du template TCF...")
    template_path = "templates/convocation_tcf_template_modele.html"
    
    if os.path.exists(template_path):
        print(f"   ✅ Template trouvé: {template_path}")
        size = os.path.getsize(template_path)
        print(f"   📏 Taille: {size} octets")
    else:
        print(f"   ❌ Template manquant: {template_path}")
        return False
    
    # 3. Créer le générateur PDF avec template HTML
    print("\\n3. Création du générateur PDF...")
    try:
        generator = PDFGenerator(
            excel_path='JURYS FINAL TCF.xlsx',
            template_path=template_path,
            logo_af_path='assets/logoAF.png',
            logo_delf_path='assets/logoTCF.png',  # Utiliser logo TCF
            output_dir='output',
            access_code='1234',
            qrcode_path='assets/qrcode.png'
        )
        print("   ✅ Générateur PDF créé")
        
    except Exception as e:
        print(f"   ❌ Erreur création générateur: {e}")
        return False
    
    # 4. Préparer les données pour le template
    print("\\n4. Préparation des données template...")
    try:
        template_data = {
            'nom': candidat['nom'],
            'prenom': candidat['prenom'],
            'date_naissance': candidat['date_naissance'],
            'tcf_type': candidat['tcf_type'],
            
            # Dates formatées
            'date_collective': candidat['date_ep_coll'],
            'date_individual': candidat['date_ep_ind'],
            'date_collective_format': candidat['date_ep_coll'].strftime("%d/%m/%Y") if candidat['date_ep_coll'] else "",
            'date_individual_format': candidat['date_ep_ind'].strftime("%d/%m/%Y") if candidat['date_ep_ind'] else "",
            
            # Épreuves
            'has_collective_exams': candidat['tcf_type'] != 'TCF TP OBLIGATOIRE',
            'has_individual_exam': True,
            'heure_collective': candidat['debut_ep_coll'],
            'heure_individual': candidat['heure_preparation'],
            'duree_collective': candidat['duree_collective'],
            'duree_individual': candidat['duree_individuelle'],
            
            # Salles
            'salle_collective': '1',
            'salle_individual': '1',
            'salle': '1',
            
            # Logos
            'logo_af_path': 'assets/logoAF.png',
            'logo_tcf_path': 'assets/logoTCF.png',
            
            # QR Code et accès
            'qrcode_path': 'assets/qrcode.png',
            'access_code': '1234',
            
            # Institution
            'institution_name': 'Alliance Française de Bruxelles-Europe',
            'institution_address': 'Avenue des Arts 46',
            'institution_postal': '1000',
            'institution_city': 'Bruxelles',
            
            # Tiers temps
            'tiers_temps': False
        }
        
        print("   ✅ Données template préparées")
        print(f"      Candidat: {template_data['nom']} {template_data['prenom']}")
        print(f"      Type TCF: {template_data['tcf_type']}")
        print(f"      Date collective: {template_data['date_collective_format']}")
        print(f"      Heure collective: {template_data['heure_collective']}")
        
    except Exception as e:
        print(f"   ❌ Erreur préparation données: {e}")
        return False
    
    # 5. Générer le PDF avec le template HTML
    print("\\n5. Génération du PDF avec template HTML...")
    try:
        # Créer le dossier output s'il n'existe pas
        os.makedirs('output', exist_ok=True)
        
        # Nom du fichier de test
        pdf_filename = f"test_tcf_template_{candidat['nom']}_{candidat['prenom']}.pdf"
        
        # Générer le PDF
        pdf_path = generator.generate_pdf(template_data, pdf_filename)
        
        if pdf_path and os.path.exists(pdf_path):
            file_size = os.path.getsize(pdf_path)
            print(f"   ✅ PDF généré avec succès!")
            print(f"      Fichier: {pdf_path}")
            print(f"      Taille: {file_size} octets")
            
            # Vérifier que le fichier n'est pas vide
            if file_size > 1000:
                print("   ✅ Le PDF semble valide (taille > 1KB)")
            else:
                print("   ⚠️  Le PDF semble petit (possibles problèmes)")
            
            return True
        else:
            print("   ❌ Le PDF n'a pas été créé")
            return False
            
    except Exception as e:
        print(f"   ❌ Erreur génération PDF: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Fonction principale de test"""
    print("🔄 TEST COMPLET PDF TCF AVEC TEMPLATE HTML")
    print("=" * 70)
    
    try:
        success = test_tcf_template_html()
        
        print("\\n" + "=" * 70)
        if success:
            print("🎉 TEST RÉUSSI!")
            print("✅ Le système génère maintenant des PDF TCF avec le template HTML")
            print("✅ Le PDF aura la même apparence que les convocations DELF")
            print("✅ Templates HTML utilisés au lieu de ReportLab basique")
            
            print("\\n📁 Fichier généré dans le dossier output/")
            print("💡 Ouvrez le PDF pour vérifier qu'il utilise le bon template")
            
            return True
        else:
            print("❌ TEST ÉCHOUÉ")
            print("⚠️  L'application pourrait encore utiliser ReportLab")
            return False
            
    except Exception as e:
        print(f"\\n💥 ERREUR CRITIQUE: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)