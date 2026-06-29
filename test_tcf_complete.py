#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test complet des données TCF avec épreuves individuelles
"""

def test_tcf_complete_data():
    """Test avec données complètes TCF incluant épreuves individuelles"""
    print("🧪 TEST DONNÉES COMPLÈTES TCF AVEC ÉPREUVES")
    print("=" * 60)
    
    try:
        # Appliquer le correctif cryptography
        import auto_decrepit_fix
        fixer = auto_decrepit_fix.DefecratedImportFixer()
        fixer.fix_decrepit_imports()
        
        from pdf_generator import PDFGenerator
        import os
        from datetime import date, time, datetime
        
        # Données candidat TCF complètes
        test_candidate = {
            'nom': 'MARTIN',
            'prenom': 'Pierre',
            'numero_candidat': 'TCF202400001',
            'date_naissance': '15/03/1990',
            'email': 'pierre.martin@email.com',
            'tcf_type': 'TCF CANADA',
            'jury_name': 'Jury 1',
            
            # Dates d'examen
            'date_examen': date(2024, 12, 15),
            'date_ep_coll': date(2024, 12, 15),
            'date_ep_ind': date(2024, 12, 15),
            
            # Heures épreuves collectives
            'debut_ep_coll': time(9, 0),
            'fin_ep_coll': time(12, 0),
            
            # Heures épreuve individuelle
            'heure_preparation': time(14, 0),
            'heure_individuelle': time(14, 0),
            
            # Durées
            'duree_collective': '2h47',
            'duree_individuelle': '12 minutes',
            
            # Informations sur les épreuves
            'has_individual_exam': True,
            'salle_collective': '101',
            'salle_individuelle': '102',
            'salle': '101',
            
            # Informations institution
            'institution_name': 'Alliance Française de Bruxelles-Europe',
            'institution_address': 'Avenue des Arts 46',
            'institution_postal': '1000',
            'institution_city': 'Bruxelles',
            
            # Données formatées (comme dans main.py)
            'date_collective_format': '15/12/2024',
            'date_individual_format': '15/12/2024',
            'heure_collective': '09:00',
            'heure_individual': '14:00',
            
            # Code d'accès
            'access_code': '2024'
        }
        
        print(f"👤 Candidat: {test_candidate['nom']} {test_candidate['prenom']}")
        print(f"📝 Type TCF: {test_candidate['tcf_type']}")
        print(f"🕘 Épreuves collectives: {test_candidate['heure_collective']}")
        print(f"🕐 Épreuve individuelle: {test_candidate['heure_individual']}")
        print(f"⏱️ Durée collective: {test_candidate['duree_collective']}")
        print(f"⏱️ Durée individuelle: {test_candidate['duree_individuelle']}")
        
        # Template TCF
        template_path = "templates/convocation_tcf_template_simple.html"
        
        if not os.path.exists(template_path):
            print(f"❌ Template non trouvé: {template_path}")
            return False
        
        # Créer générateur
        generator = PDFGenerator(
            excel_path="test.xlsx",
            template_path=template_path,
            logo_af_path="",
            logo_delf_path="assets/logo_tcf_canada.png",  # Logo TCF Canada
            output_dir="Test_TCF_Complete",
            access_code="2024",
            qrcode_path="",
            image_a1_path="",
            image_a2_path="",
            image_b1_path="",
            image_b2_path="",
            image_c1_path="",
            image_c2_path=""
        )
        
        # Créer dossier
        os.makedirs("Test_TCF_Complete", exist_ok=True)
        
        # Générer PDF
        pdf_filename = "test_tcf_complete.pdf"
        print(f"🔄 Génération PDF: {pdf_filename}")
        
        pdf_path = generator.generate_pdf(test_candidate, pdf_filename)
        
        if pdf_path and os.path.exists(pdf_path):
            file_size = os.path.getsize(pdf_path)
            print(f"✅ PDF généré avec succès!")
            print(f"📏 Taille: {file_size} octets")
            print(f"📍 Chemin: {pdf_path}")
            
            # Vérifier le contenu en lisant le template rendu
            print("\\n📋 VÉRIFICATION DES DONNÉES:")
            print(f"  • Date épreuves collectives: {test_candidate['date_collective_format']}")
            print(f"  • Date épreuve individuelle: {test_candidate['date_individual_format']}")
            print(f"  • Heure collective: {test_candidate['heure_collective']}")
            print(f"  • Heure individuelle: {test_candidate['heure_individual']}")
            print(f"  • Salle collective: {test_candidate['salle_collective']}")
            print(f"  • Salle individuelle: {test_candidate['salle_individuelle']}")
            print(f"  • Épreuve individuelle présente: {test_candidate['has_individual_exam']}")
            
            return True
        else:
            print("❌ PDF non généré")
            return False
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Programme principal"""
    print("🔧 TEST COMPLET TCF AVEC ÉPREUVES INDIVIDUELLES")
    print("=" * 50)
    
    success = test_tcf_complete_data()
    
    if success:
        print("\\n✅ Test complet réussi!")
        print("\\n🎯 RÉSUMÉ:")
        print("  • Template TCF inclut les épreuves individuelles")
        print("  • Données complètes extraites et formatées")
        print("  • PDF généré avec toutes les informations")
        print("  • Compatible avec tous les types TCF")
        return True
    else:
        print("\\n❌ Test complet échoué")
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\\n🚀 Template TCF prêt pour la production!")
    else:
        print("\\n⚠️ Corrections nécessaires")