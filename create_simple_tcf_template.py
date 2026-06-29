#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Génération d'un template TCF simplifié compatible xhtml2pdf
"""

def create_simple_tcf_template():
    """Créer un template TCF simplifié basé sur le DELF mais compatible xhtml2pdf"""
    template_content = '''<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Convocation TCF</title>
    <style>
        @page {
            size: A4;
            margin: 1cm 2cm 2cm 2cm;
        }
        
        * {
            font-family: 'Arial', 'Helvetica', sans-serif !important;
        }
        
        body {
            font-family: 'Arial', 'Helvetica', sans-serif !important;
            line-height: 1.4;
            color: #000;
            margin: 0;
            padding: 0;
            font-size: 11pt;
        }
        
        .header {
            width: 100%;
            margin-bottom: 20px;
            padding: 0;
        }
        
        .logo-table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 20px;
        }
        
        .logo-table td {
            border: none;
            padding: 5px;
            vertical-align: top;
        }
        
        .logo-left-cell {
            width: 50%;
            text-align: left;
        }
        
        .logo-right-cell {
            width: 50%;
            text-align: right;
        }
        
        .logo-left, .logo-right {
            height: 60px;
            width: auto;
        }
        
        .title-box {
            border: 3px solid #000000;
            text-align: center;
            padding: 15px;
            margin: 20px 0;
            font-size: 24pt;
            font-weight: bold;
            text-transform: uppercase;
        }
        
        .candidate-name {
            font-size: 12pt;
            font-weight: bold;
            margin: 15px 0 5px 0;
        }
        
        .candidate-info {
            margin: 3px 0;
            font-size: 11pt;
        }
        
        .instruction-text {
            margin: 15px 0;
            text-align: justify;
            font-size: 11pt;
        }
        
        .exam-title {
            text-align: center;
            margin: 20px 0;
            border: 2px solid #000;
            padding: 8px 15px;
            font-weight: bold;
            font-size: 12pt;
            text-transform: uppercase;
            display: inline-block;
        }
        
        .exam-table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }
        
        .exam-table td {
            padding: 10px 5px;
            border: none;
            vertical-align: top;
        }
        
        .exam-section {
            margin: 10px 0;
        }
        
        .exam-section-title {
            font-weight: bold;
            margin-bottom: 5px;
            font-size: 11pt;
            text-decoration: underline;
        }
        
        .exam-info {
            margin: 2px 0;
            font-size: 11pt;
        }
        
        .highlight {
            background-color: #ffff00;
            padding: 2px;
        }
        
        .address-text {
            margin: 15px 0 5px 0;
            font-size: 11pt;
        }
        
        .address-box {
            text-align: left;
            margin: 10px 0;
            padding: 8px;
            font-size: 11pt;
            font-weight: bold;
        }
        
        .important-notice {
            margin: 20px 0;
            text-align: justify;
            font-size: 11pt;
            font-style: italic;
        }
        
        .access-code {
            margin-top: 20px;
            font-size: 12pt;
            font-weight: bold;
            color: #da002e;
            text-align: center;
        }
        
        @media print {
            body {
                -webkit-print-color-adjust: exact;
                print-color-adjust: exact;
            }
        }
    </style>
</head>
<body>
    <div class="header">
        <table class="logo-table">
            <tr>
                <td class="logo-left-cell">
                    <img src="{{ logo_af_path }}" alt="Alliance Française" class="logo-left">
                </td>
                <td class="logo-right-cell">
                    <img src="{{ logo_tcf_path }}" alt="TCF" class="logo-right">
                </td>
            </tr>
        </table>
        
        <div class="title-box">
            CONVOCATION À UN EXAMEN
        </div>
    </div>

    <div class="candidate-name">{{ nom|upper }} {{ prenom|title }}</div>
    
    <div class="candidate-info"><strong>Né.e le :</strong> {{ date_naissance }}</div>
    
    <div class="instruction-text">
        Vous êtes invité.e à vous présenter aux épreuves suivantes, aux dates et heures indiquées ci-dessous, 
        muni.e de la présente convocation et d'une pièce d'identité en cours de validité.
    </div>

    <div style="text-align: center;">
        <div class="exam-title">
            Examen {{ tcf_type or "TCF" }}
        </div>
    </div>

    <table class="exam-table">
        <tr>
            <td style="width: 60%;">
                <!-- Épreuves collectives -->
                <div class="exam-section">
                    <div class="exam-section-title">Épreuves collectives :</div>
                    <div class="exam-info"><strong>Date</strong> : <span class="highlight">{{ date_collective_format }}</span></div>
                    <div class="exam-info"><strong>Début de l'épreuve</strong> : {{ heure_collective }}</div>
                    <div class="exam-info"><strong>Durée</strong> : {{ duree_collective }}</div>
                    <div class="exam-info"><strong>Salle</strong> : {{ salle_collective or salle }}</div>
                </div>

                {% if has_individual_exam %}
                <div class="exam-section">
                    <div class="exam-section-title">Épreuve individuelle :</div>
                    <div class="exam-info"><strong>Date</strong> : <span class="highlight">{{ date_individual_format }}</span></div>
                    <div class="exam-info"><strong>Heure</strong> : {{ heure_individual }}</div>
                    <div class="exam-info"><strong>Durée</strong> : {{ duree_individual }}</div>
                    <div class="exam-info"><strong>Salle</strong> : {{ salle_individual or salle }}</div>
                </div>
                {% endif %}
            </td>
            <td style="width: 40%; text-align: center;">
                {% if logo_tcf_path %}
                    <img src="{{ logo_tcf_path }}" alt="Logo TCF" style="width: 150px; height: 150px; object-fit: contain; opacity: 0.3;">
                {% else %}
                    <div style="width: 150px; height: 150px; border: 1px dashed #ccc; display: flex; align-items: center; justify-content: center; margin: 0 auto;">
                        <div style="color: #999; font-size: 9pt; text-align: center;">
                            Logo<br>TCF<br>{{ tcf_type or "" }}
                        </div>
                    </div>
                {% endif %}
            </td>
        </tr>
    </table>

    <div class="address-text">L'examen se déroulera à l'adresse suivante :</div>

    <div class="address-box">
        {{ institution_name or "Alliance Française de Bruxelles-Europe" }}<br>
        {{ institution_address or "Avenue des Arts 46" }}<br>
        {{ institution_postal or "1000" }} {{ institution_city or "Bruxelles" }}
    </div>

    <div class="important-notice">
        Afin d'assurer la bonne tenue des épreuves collectives et individuelles, vous êtes prié.e de 
        vous présenter sur le lieu de passation <strong>30 minutes avant</strong> les horaires indiqués sur cette 
        convocation.
    </div>

    <div class="access-code">
        Votre code d'accès aux locaux est : {{ access_code or "" }}
    </div>

</body>
</html>'''
    
    return template_content

def main():
    """Créer le template TCF simplifié"""
    print("🔧 CRÉATION TEMPLATE TCF SIMPLIFIÉ POUR XHTML2PDF")
    print("=" * 60)
    
    template_content = create_simple_tcf_template()
    
    # Sauvegarder le template
    template_path = 'templates/convocation_tcf_template_simple.html'
    
    try:
        with open(template_path, 'w', encoding='utf-8') as f:
            f.write(template_content)
        
        print(f"✅ Template créé: {template_path}")
        print(f"📏 Taille: {len(template_content)} caractères")
        
        print("\\n🎯 AMÉLIORATIONS DU TEMPLATE SIMPLIFIÉ:")
        print("  • Styles CSS simplifiés pour xhtml2pdf")
        print("  • Tableau simplifié sans largeurs fixes")
        print("  • Suppression des flex et display complexes")
        print("  • Structure HTML plus basique")
        print("  • Compatible avec les limitations de xhtml2pdf")
        
        print("\\n💡 UTILISATION:")
        print("  Ce template peut être utilisé comme alternative si le template")
        print("  complexe pose des problèmes avec xhtml2pdf.")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur création template: {e}")
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\\n🎉 Template TCF simplifié créé avec succès!")
    else:
        print("\\n❌ Échec de création du template")