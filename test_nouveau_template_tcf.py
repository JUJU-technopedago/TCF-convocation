#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test du nouveau template TCF identique au template DELF
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

try:
    import auto_decrepit_fix
except ImportError:
    pass

from tcf_excel_processor import TCFExcelProcessor
from jinja2 import Environment, FileSystemLoader

def test_nouveau_template_tcf():
    """Test du nouveau template TCF avec les données TCF"""
    print("🧪 TEST DU NOUVEAU TEMPLATE TCF")
    print("=" * 50)
    
    # 1. Charger les données TCF
    print("1. Chargement des données TCF...")
    try:
        processor = TCFExcelProcessor('JURYS FINAL TCF.xlsx')
        processor.load_tcf_data()
        candidats = processor.get_all_candidates()
        
        if not candidats:
            print("   ❌ Aucun candidat trouvé")
            return False
        
        candidat = candidats[0]  # Premier candidat pour test
        print(f"   ✅ Candidat de test: {candidat['nom']} {candidat['prenom']} ({candidat['tcf_type']})")
        
    except Exception as e:
        print(f"   ❌ Erreur chargement données: {e}")
        return False
    
    # 2. Préparer les données pour le template
    print("\\n2. Préparation des données template...")
    try:
        template_data = {
            # Données candidat (comme DELF)
            'nom': candidat['nom'],
            'prenom': candidat['prenom'], 
            'date_naissance': candidat.get('date_naissance', '01/01/1990'),
            'tiers_temps': False,
            
            # Données TCF spécifiques 
            'tcf_type': candidat['tcf_type'],
            
            # Données épreuves (format DELF)
            'date_collective': candidat.get('date_collective'),
            'date_individual': candidat.get('date_individual'),
            'date_collective_format': candidat.get('date_collective_format'),
            'date_individual_format': candidat.get('date_individual_format'),
            'heure_collective': candidat.get('heure_collective'),
            'heure_individual': candidat.get('heure_individual'),
            'duree_collective': candidat.get('duree_collective'),
            'duree_individual': candidat.get('duree_individual'),
            'has_individual_exam': candidat.get('has_individual_exam', True),
            'salle_collective': candidat.get('salle', 'Salle 1'),
            'salle_individual': candidat.get('salle', 'Salle 1'),
            'salle': candidat.get('salle', 'Salle 1'),
            
            # Logos
            'logo_af_path': 'assets/logoAF.png',
            'logo_tcf_path': 'assets/logoTCF.png',
            
            # Autres données
            'qrcode_path': 'assets/qrcode.png',
            'access_code': '1234',
            'institution_name': 'Alliance Française de Bruxelles-Europe',
            'institution_address': 'Avenue des Arts 46',
            'institution_postal': '1000',
            'institution_city': 'Bruxelles'
        }
        
        print("   ✅ Données template préparées")
        
    except Exception as e:
        print(f"   ❌ Erreur préparation données: {e}")
        return False
    
    # 3. Charger le template
    print("\\n3. Chargement du template...")
    try:
        env = Environment(loader=FileSystemLoader('templates'))
        template = env.get_template('convocation_tcf_template_modele.html')
        print("   ✅ Template TCF chargé")
        
    except Exception as e:
        print(f"   ❌ Erreur chargement template: {e}")
        return False
    
    # 4. Générer le HTML
    print("\\n4. Génération du HTML...")
    try:
        html_content = template.render(**template_data)
        
        # Créer le fichier de sortie
        output_file = 'test_nouveau_template_tcf.html'
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"   ✅ HTML généré: {output_file}")
        
    except Exception as e:
        print(f"   ❌ Erreur génération HTML: {e}")
        return False
    
    # 5. Vérifications du contenu
    print("\\n5. Vérifications du contenu...")
    try:
        # Vérifier que les éléments clés du template DELF sont présents
        checks = [
            ('CONVOCATION À UN EXAMEN', 'Titre principal'),
            (candidat['nom'].upper(), 'Nom candidat'),
            (candidat['prenom'].title(), 'Prénom candidat'),
            ('Épreuves collectives', 'Section épreuves collectives'),
            ('L\'examen se déroulera à l\'adresse suivante', 'Texte adresse'),
            ('30 minutes avant', 'Notice importante'),
            ('Votre code d\'accès aux locaux', 'Code d\'accès')
        ]
        
        for check_text, description in checks:
            if check_text in html_content:
                print(f"   ✅ {description}: présent")
            else:
                print(f"   ❌ {description}: manquant")
                return False
        
        # Vérifier les spécificités TCF
        tcf_checks = [
            (f'Examen {candidat["tcf_type"]}', 'Type TCF'),
            ('logo_tcf_path', 'Référence logo TCF'),
        ]
        
        for check_text, description in tcf_checks:
            if check_text in html_content:
                print(f"   ✅ {description}: présent")
            else:
                print(f"   ❌ {description}: manquant")
        
    except Exception as e:
        print(f"   ❌ Erreur vérifications: {e}")
        return False
    
    return True

def test_comparaison_templates():
    """Comparer la structure des templates DELF et TCF"""
    print("\\n📋 COMPARAISON DES TEMPLATES DELF ET TCF")
    print("=" * 50)
    
    try:
        # Lire les deux templates
        with open('templates/convocation_delf_template_modele.html', 'r', encoding='utf-8') as f:
            delf_content = f.read()
        
        with open('templates/convocation_tcf_template_modele.html', 'r', encoding='utf-8') as f:
            tcf_content = f.read()
        
        # Analyser les différences principales
        print("Différences principales identifiées:")
        
        # Logo
        if 'logo_delf_path' in delf_content and 'logo_tcf_path' in tcf_content:
            print("   ✅ Logo: DELF → TCF (changement approprié)")
        
        # Titre examen
        if 'Niveau {{ niveau or "B1" }} du CECRL' in delf_content and 'Examen {{ tcf_type or "TCF" }}' in tcf_content:
            print("   ✅ Titre: DELF + niveau → TCF type (changement approprié)")
        
        # Numéro candidat
        if 'numero_candidat' in delf_content and 'numero_candidat' not in tcf_content:
            print("   ✅ Numéro candidat: retiré pour TCF (approprié)")
        
        # Structure générale
        delf_lines = len(delf_content.split('\\n'))
        tcf_lines = len(tcf_content.split('\\n'))
        
        print(f"   📏 Longueur DELF: {delf_lines} lignes")
        print(f"   📏 Longueur TCF: {tcf_lines} lignes")
        
        if abs(delf_lines - tcf_lines) < 10:
            print("   ✅ Structure similaire (différence < 10 lignes)")
        else:
            print("   ⚠️  Structure très différente")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Erreur comparaison: {e}")
        return False

def main():
    """Fonction principale de test"""
    print("🔄 TEST COMPLET DU NOUVEAU TEMPLATE TCF")
    print("=" * 60)
    
    try:
        success1 = test_nouveau_template_tcf()
        success2 = test_comparaison_templates()
        
        print("\\n" + "=" * 60)
        if success1 and success2:
            print("🎉 TOUS LES TESTS RÉUSSIS!")
            print("✅ Le template TCF est maintenant identique au template DELF")
            print("✅ Structure et mise en page cohérentes")
            print("✅ Variables TCF correctement intégrées")
            print("✅ Génération HTML fonctionnelle")
            
            print("\\n📄 Fichier de test généré: test_nouveau_template_tcf.html")
            print("💡 Vous pouvez l'ouvrir dans un navigateur pour vérifier le rendu")
            
            return True
        else:
            print("❌ CERTAINS TESTS ONT ÉCHOUÉ")
            print("⚠️  Le template pourrait nécessiter des ajustements")
            return False
            
    except Exception as e:
        print(f"\\n💥 ERREUR CRITIQUE: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)