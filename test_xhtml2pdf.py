#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de test pour diagnostiquer les problèmes xhtml2pdf avec le template TCF
"""

import os
import sys
from xhtml2pdf import pisa
from jinja2 import Template

def test_basic_html():
    """Test avec HTML basique"""
    print("🔬 Test 1: HTML basique")
    
    basic_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body { font-family: Arial, sans-serif; }
        </style>
    </head>
    <body>
        <h1>Test basique</h1>
        <p>Candidat: DUPONT Jean</p>
    </body>
    </html>
    """
    
    try:
        with open("test_basic.pdf", "w+b") as result_file:
            pisa_status = pisa.CreatePDF(
                src=basic_html,
                dest=result_file,
                encoding='utf-8'
            )
        
        if pisa_status.err:
            print(f"❌ Erreur: {pisa_status.err}")
        else:
            print("✅ HTML basique fonctionne")
    except Exception as e:
        print(f"❌ Exception: {e}")

def test_tcf_template_minimal():
    """Test avec version minimale du template TCF"""
    print("\n🔬 Test 2: Template TCF minimal")
    
    minimal_tcf = """
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <title>Convocation TCF</title>
        <style>
            @page { size: A4; margin: 2cm; }
            body { font-family: Arial, sans-serif; font-size: 12pt; }
            .title-box { border: 1px solid #000; text-align: center; padding: 10px; }
            .highlight { background-color: #ffff00; }
        </style>
    </head>
    <body>
        <div class="title-box">CONVOCATION À UN EXAMEN</div>
        <h2>{{ nom|upper }} {{ prenom|title }}</h2>
        <p><strong>Né.e le :</strong> {{ date_naissance }}</p>
        <div style="border: 2px solid #000; padding: 10px; margin: 20px 0;">
            Examen {{ tcf_type or "TCF" }}
        </div>
        <div>
            <strong>Épreuves collectives :</strong><br>
            Date : <span class="highlight">{{ date_collective_format }}</span><br>
            Heure : {{ heure_collective }}<br>
            Salle : {{ salle_collective }}
        </div>
        <div>
            <strong>Épreuve individuelle :</strong><br>
            Date : <span class="highlight">{{ date_individual_format }}</span><br>
            Heure : {{ heure_individual }}<br>
            Salle : {{ salle_individuelle }}
        </div>
        <p>Alliance Française de Bruxelles-Europe</p>
    </body>
    </html>
    """
    
    # Données de test
    test_data = {
        'nom': 'DUPONT',
        'prenom': 'Jean',
        'date_naissance': '15/03/1990',
        'tcf_type': 'TCF IRN',
        'date_collective_format': 'le mardi 21 octobre 2025',
        'date_individual_format': 'le mardi 21 octobre 2025',
        'heure_collective': '10:00',
        'heure_individual': '16:00',
        'salle_collective': '1',
        'salle_individuelle': '2'
    }
    
    try:
        template = Template(minimal_tcf)
        html_content = template.render(**test_data)
        
        with open("test_tcf_minimal.pdf", "w+b") as result_file:
            pisa_status = pisa.CreatePDF(
                src=html_content,
                dest=result_file,
                encoding='utf-8'
            )
        
        if pisa_status.err:
            print(f"❌ Erreur: {pisa_status.err}")
        else:
            print("✅ Template TCF minimal fonctionne")
    except Exception as e:
        print(f"❌ Exception: {e}")

def test_tcf_template_with_tables():
    """Test avec tableaux comme dans le template original"""
    print("\n🔬 Test 3: Template TCF avec tableaux")
    
    table_tcf = """
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <style>
            @page { size: A4; margin: 2cm; }
            body { font-family: Arial, sans-serif; }
            .address-table {
                width: 100%;
                border-collapse: collapse;
                margin: 10px 0;
            }
            .qrcode-cell {
                width: 150px;
                vertical-align: middle;
                padding: 0;
            }
            .address-cell {
                width: 450px;
                vertical-align: middle;
                padding: 0 0 0 20px;
            }
        </style>
    </head>
    <body>
        <h1>Test avec tableaux</h1>
        <table class="address-table">
            <tr>
                <td class="qrcode-cell">
                    [QR Code]
                </td>
                <td class="address-cell">
                    Alliance Française<br>
                    Avenue des Arts 46<br>
                    1000 Bruxelles
                </td>
            </tr>
        </table>
    </body>
    </html>
    """
    
    try:
        with open("test_tcf_tables.pdf", "w+b") as result_file:
            pisa_status = pisa.CreatePDF(
                src=table_tcf,
                dest=result_file,
                encoding='utf-8'
            )
        
        if pisa_status.err:
            print(f"❌ Erreur: {pisa_status.err}")
        else:
            print("✅ Template avec tableaux fonctionne")
    except Exception as e:
        print(f"❌ Exception: {e}")

def test_current_tcf_template():
    """Test avec le template TCF actuel"""
    print("\n🔬 Test 4: Template TCF actuel")
    
    template_path = "templates/convocation_tcf_template_simple.html"
    
    if not os.path.exists(template_path):
        print(f"❌ Template non trouvé: {template_path}")
        return
    
    # Données de test complètes
    test_data = {
        'nom': 'DUPONT',
        'prenom': 'Jean',
        'date_naissance': '15/03/1990',
        'tcf_type': 'TCF IRN',
        'date_collective_format': 'le mardi 21 octobre 2025',
        'date_individual_format': 'le mardi 21 octobre 2025',
        'heure_collective': '10:00',
        'heure_individual': '16:00',
        'debut_ep_coll': '10:00',
        'heure_preparation': '16:00',
        'duree_collective': '2h30',
        'duree_individuelle': '30min',
        'salle_collective': '1',
        'salle_individuelle': '2',
        'salle': '1',
        'institution_name': 'Alliance Française de Bruxelles-Europe',
        'institution_address': 'Avenue des Arts 46',
        'institution_postal': '1000',
        'institution_city': 'Bruxelles',
        'access_code': '1234'
    }
    
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            template_content = f.read()
        
        template = Template(template_content)
        html_content = template.render(**test_data)
        
        print(f"📄 HTML généré (premiers 500 caractères):")
        print(html_content[:500] + "...")
        
        with open("test_tcf_current.pdf", "w+b") as result_file:
            pisa_status = pisa.CreatePDF(
                src=html_content,
                dest=result_file,
                encoding='utf-8'
            )
        
        if pisa_status.err:
            print(f"❌ Erreur avec template actuel: {pisa_status.err}")
        else:
            print("✅ Template TCF actuel fonctionne")
            
    except Exception as e:
        print(f"❌ Exception avec template actuel: {e}")

def main():
    """Fonction principale de test"""
    print("🧪 DIAGNOSTIC XHTML2PDF - TEMPLATE TCF")
    print("=" * 50)
    
    # Tester différents niveaux de complexité
    test_basic_html()
    test_tcf_template_minimal()
    test_tcf_template_with_tables()
    test_current_tcf_template()
    
    print("\n📋 RÉSUMÉ:")
    print("- Vérifiez quels tests passent et lesquels échouent")
    print("- Les PDFs générés sont dans le répertoire courant")
    print("- Si seul le template actuel échoue, il faut simplifier le CSS")

if __name__ == "__main__":
    main()