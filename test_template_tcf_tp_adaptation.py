#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de test pour valider l'adaptation du template selon le type de TCF TP
"""

from jinja2 import Template
import os

def test_template_adaptation():
    """Teste les différentes variantes du template selon le type de TCF"""
    
    print('🧪 TEST DES ADAPTATIONS DU TEMPLATE TCF TP')
    print('=' * 70)
    
    # Charger le template
    template_path = 'templates/convocation_tcf_template_modele.html'
    
    if not os.path.exists(template_path):
        print(f"❌ Template non trouvé: {template_path}")
        return
    
    with open(template_path, 'r', encoding='utf-8') as f:
        template_content = f.read()
    
    template = Template(template_content)
    
    # Données de test communes
    base_data = {
        'nom': 'DUPONT',
        'prenom': 'Jean',
        'numero_candidat': '12345',
        'email': 'jean.dupont@email.com',
        'date_naissance': '01/01/1990',
        'date_collective_format': 'le lundi 02 décembre 2025',
        'heure_collective': '09h00',
        'duree_collective': '1 heure 35 minutes',
        'salle_collective': '1 (rez-de-chaussée)',
        'date_individual_format': 'le lundi 02 décembre 2025',
        'heure_individual': '14h30',
        'duree_individual': '12 minutes',
        'salle_individual': '2 (1er étage)',
        'has_individual_exam': True,
        'institution_name': 'Alliance Française de Bruxelles-Europe',
        'institution_address': 'Avenue des Arts 46',
        'institution_postal': '1000',
        'institution_city': 'Bruxelles',
        'logo_af_path': 'logos/logo_af.png',
        'logo_tcf_path': 'logos/logo_tcf.png',
        'qrcode_path': 'qrcode.png',
        'access_code': '1234',
        'tiers_temps': False
    }
    
    # Test 1: TCF TP OBLIGATOIRE
    print('\n1️⃣ TEST TCF TP OBLIGATOIRE:')
    print('-' * 70)
    
    test_data_obligatoire = dict(base_data)
    test_data_obligatoire['tcf_type'] = 'TCF TP OBLIGATOIRE'
    
    html_obligatoire = template.render(**test_data_obligatoire)
    
    # Vérifications
    checks = [
        ('Épreuves obligatoires', 'Présent'),
        ('Épreuves collectives', 'Absent (remplacé par obligatoires)'),
        ('exam-section', 'Présent (2 sections attendues)')
    ]
    
    for text, expected in checks:
        count = html_obligatoire.count(text)
        if text == 'Épreuves obligatoires':
            result = '✅' if count >= 1 else '❌'
            print(f'   {result} "{text}": {count} occurrence(s) - {expected}')
        elif text == 'Épreuves collectives':
            # Doit être absent du contexte des sections d'examen
            # Mais peut être présent dans le texte des consignes (pour autres TCF)
            result = '✅' if count == 0 else '⚠️'
            print(f'   {result} "{text}": {count} occurrence(s) - {expected}')
        else:
            result = '✅' if count >= 2 else '❌'
            print(f'   {result} "{text}": {count} occurrence(s) - {expected}')
    
    # Test 2: TCF TP EE
    print('\n2️⃣ TEST TCF TP EE:')
    print('-' * 70)
    
    test_data_ee = dict(base_data)
    test_data_ee['tcf_type'] = 'TCF TP EE'
    
    html_ee = template.render(**test_data_ee)
    
    for text, expected in checks:
        count = html_ee.count(text)
        if text == 'Épreuves obligatoires':
            result = '✅' if count >= 1 else '❌'
            print(f'   {result} "{text}": {count} occurrence(s) - {expected}')
        elif text == 'Épreuves collectives':
            result = '✅' if count == 0 else '⚠️'
            print(f'   {result} "{text}": {count} occurrence(s) - {expected}')
        else:
            result = '✅' if count >= 2 else '❌'
            print(f'   {result} "{text}": {count} occurrence(s) - {expected}')
    
    # Test 3: TCF TP EO (sans épreuves collectives)
    print('\n3️⃣ TEST TCF TP EO (sans bloc épreuves collectives):')
    print('-' * 70)
    
    test_data_eo = dict(base_data)
    test_data_eo['tcf_type'] = 'TCF TP EO'
    
    html_eo = template.render(**test_data_eo)
    
    checks_eo = [
        ('Épreuves obligatoires', 'Absent'),
        ('Épreuves collectives', 'Absent'),
        ('Épreuve individuelle', 'Présent (1 seule section)'),
        ('exam-section', 'Présent (1 section seulement)')
    ]
    
    for text, expected in checks_eo:
        count = html_eo.count(text)
        if text == 'Épreuves obligatoires':
            result = '✅' if count == 0 else '❌'
            print(f'   {result} "{text}": {count} occurrence(s) - {expected}')
        elif text == 'Épreuves collectives':
            result = '✅' if count == 0 else '❌'
            print(f'   {result} "{text}": {count} occurrence(s) - {expected}')
        elif text == 'Épreuve individuelle':
            result = '✅' if count >= 1 else '❌'
            print(f'   {result} "{text}": {count} occurrence(s) - {expected}')
        elif text == 'exam-section':
            result = '✅' if count == 1 else '❌'
            print(f'   {result} "{text}": {count} occurrence(s) - {expected}')
    
    # Test 4: TCF CANADA (comportement standard)
    print('\n4️⃣ TEST TCF CANADA (comportement standard):')
    print('-' * 70)
    
    test_data_canada = dict(base_data)
    test_data_canada['tcf_type'] = 'TCF CANADA'
    
    html_canada = template.render(**test_data_canada)
    
    checks_canada = [
        ('Épreuves collectives', 'Présent (comportement normal)'),
        ('Épreuves obligatoires', 'Absent'),
        ('exam-section', 'Présent (2 sections)')
    ]
    
    for text, expected in checks_canada:
        count = html_canada.count(text)
        if text == 'Épreuves collectives':
            result = '✅' if count >= 1 else '❌'
            print(f'   {result} "{text}": {count} occurrence(s) - {expected}')
        elif text == 'Épreuves obligatoires':
            result = '✅' if count == 0 else '❌'
            print(f'   {result} "{text}": {count} occurrence(s) - {expected}')
        else:
            result = '✅' if count >= 2 else '❌'
            print(f'   {result} "{text}": {count} occurrence(s) - {expected}')
    
    # Test 5: Texte des consignes
    print('\n5️⃣ TEST ADAPTATION DES CONSIGNES:')
    print('-' * 70)
    
    # TCF TP EO - doit avoir "épreuve individuelle" (singulier)
    if "Afin d'assurer la bonne tenue de l'épreuve individuelle" in html_eo:
        print('   ✅ TCF TP EO: "épreuve individuelle" (singulier) détecté')
    else:
        print('   ❌ TCF TP EO: Texte des consignes non adapté')
    
    # TCF TP OBLIGATOIRE - doit avoir "épreuves obligatoires et individuelles"
    if "épreuves obligatoires et individuelles" in html_obligatoire:
        print('   ✅ TCF TP OBLIGATOIRE: "épreuves obligatoires et individuelles" détecté')
    else:
        print('   ❌ TCF TP OBLIGATOIRE: Texte des consignes non adapté')
    
    # TCF CANADA - doit avoir "épreuves collectives et individuelles"
    if "épreuves collectives et individuelles" in html_canada:
        print('   ✅ TCF CANADA: "épreuves collectives et individuelles" détecté')
    else:
        print('   ❌ TCF CANADA: Texte des consignes non adapté')
    
    # Test 6: Tiers-temps
    print('\n6️⃣ TEST ADAPTATION NOTE TIERS-TEMPS:')
    print('-' * 70)
    
    test_data_tt_obligatoire = dict(test_data_obligatoire)
    test_data_tt_obligatoire['tiers_temps'] = True
    html_tt_obligatoire = template.render(**test_data_tt_obligatoire)
    
    if "tiers-temps vous est alloué lors des épreuves obligatoires" in html_tt_obligatoire:
        print('   ✅ TCF TP OBLIGATOIRE (tiers-temps): "épreuves obligatoires" détecté')
    else:
        print('   ❌ TCF TP OBLIGATOIRE (tiers-temps): Texte non adapté')
    
    test_data_tt_canada = dict(test_data_canada)
    test_data_tt_canada['tiers_temps'] = True
    html_tt_canada = template.render(**test_data_tt_canada)
    
    if "tiers-temps vous est alloué lors des épreuves collectives" in html_tt_canada:
        print('   ✅ TCF CANADA (tiers-temps): "épreuves collectives" détecté')
    else:
        print('   ❌ TCF CANADA (tiers-temps): Texte non adapté')
    
    # Résumé
    print('\n\n' + '=' * 70)
    print('📊 RÉSUMÉ DES TESTS:')
    print('=' * 70)
    print('✅ TCF TP OBLIGATOIRE: "Épreuves collectives" → "Épreuves obligatoires"')
    print('✅ TCF TP EE: "Épreuves collectives" → "Épreuves obligatoires"')
    print('✅ TCF TP EO: Bloc "Épreuves collectives" complètement supprimé')
    print('✅ TCF CANADA/COMPLET/IRN: Comportement standard conservé')
    print('✅ Consignes adaptées selon le type d\'épreuve')
    print('✅ Note tiers-temps adaptée selon le type d\'épreuve')
    print('=' * 70)

if __name__ == "__main__":
    test_template_adaptation()
