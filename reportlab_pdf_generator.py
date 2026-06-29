#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Générateur PDF simple pour TCF utilisant reportlab
"""

import os
import logging
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors

logger = logging.getLogger(__name__)

class ReportLabPDFGenerator:
    """Générateur PDF simple pour les convocations TCF avec ReportLab"""
    
    def __init__(self, config=None):
        self.config = config or {}

    def _format_birth_date(self, date_value):
        """Formate une date de naissance au format '12 février 1997'"""
        if not date_value:
            return ''

        mois_francais = {
            1: 'janvier', 2: 'février', 3: 'mars', 4: 'avril', 5: 'mai', 6: 'juin',
            7: 'juillet', 8: 'août', 9: 'septembre', 10: 'octobre', 11: 'novembre', 12: 'décembre'
        }

        if isinstance(date_value, str) and any(mois in date_value.lower() for mois in mois_francais.values()):
            return date_value

        parsed_date = None
        if hasattr(date_value, 'to_pydatetime'):
            parsed_date = date_value.to_pydatetime()
        elif hasattr(date_value, 'year') and hasattr(date_value, 'month') and hasattr(date_value, 'day'):
            parsed_date = date_value
        elif isinstance(date_value, str):
            for date_format in ('%Y-%m-%d %H:%M:%S', '%Y-%m-%d', '%d/%m/%Y', '%d-%m-%Y'):
                try:
                    parsed_date = datetime.strptime(date_value.strip(), date_format)
                    break
                except ValueError:
                    continue

        if parsed_date is None:
            return str(date_value)

        return f"{parsed_date.day:02d} {mois_francais[parsed_date.month]} {parsed_date.year}"
        
    def generate_convocation(self, template_data, output_filename, template_name="convocation_tcf_template_modele.html"):
        """
        Générer une convocation PDF simple
        
        Args:
            template_data: Dictionnaire des données pour le template
            output_filename: Nom du fichier PDF de sortie
            template_name: Nom du template à utiliser (ignoré pour cette version)
            
        Returns:
            bool: True si succès, False sinon
        """
        try:
            # Créer le document PDF
            doc = SimpleDocTemplate(output_filename, pagesize=A4,
                                  rightMargin=2*cm, leftMargin=2*cm,
                                  topMargin=1*cm, bottomMargin=2*cm)
            
            # Styles
            styles = getSampleStyleSheet()
            
            # Créer le contenu
            story = []
            
            # Titre principal
            title_style = styles['Title']
            title_style.fontSize = 24
            title_style.textColor = colors.black
            title_style.alignment = 1  # Centré
            
            story.append(Paragraph("CONVOCATION À UN EXAMEN", title_style))
            story.append(Spacer(1, 1*cm))
            
            # Informations candidat
            heading_style = styles['Heading2']
            heading_style.fontSize = 14
            
            story.append(Paragraph(f"<b>{template_data['nom']} {template_data['prenom']}</b>", heading_style))
            story.append(Spacer(1, 0.3*cm))
            
            # Informations de base
            normal_style = styles['Normal']
            normal_style.fontSize = 11
            
            template_data = dict(template_data)
            template_data['date_naissance'] = self._format_birth_date(template_data.get('date_naissance', ''))

            story.append(Paragraph(f"<b>Né.e le :</b> {template_data['date_naissance']}", normal_style))
            story.append(Spacer(1, 0.2*cm))
            
            # Instruction
            story.append(Paragraph(
                "Vous êtes invité.e à vous présenter aux épreuves suivantes, aux dates et heures "
                "indiquées ci-dessous, muni.e de la présente convocation et d'une pièce d'identité "
                "en cours de validité.", normal_style))
            story.append(Spacer(1, 0.5*cm))
            
            # Type d'examen
            exam_style = styles['Heading2']
            exam_style.fontSize = 12
            exam_style.alignment = 1
            story.append(Paragraph(f"Examen {template_data['tcf_type']}", exam_style))
            story.append(Spacer(1, 0.5*cm))
            
            # Tableau des épreuves
            table_data = []
            
            # En-tête du tableau
            table_data.append(['ÉPREUVE', 'DATE', 'HEURE', 'DURÉE', 'SALLE'])
            
            # Épreuves collectives
            if template_data.get('has_collective_exams', True):
                table_data.append([
                    'Épreuves collectives',
                    template_data.get('date_collective_format', ''),
                    template_data.get('heure_collective', ''),
                    template_data.get('duree_collective', ''),
                    template_data.get('salle_collective', '')
                ])
            
            # Épreuve individuelle
            if template_data.get('has_individual_exam', True):
                table_data.append([
                    'Épreuve individuelle',
                    template_data.get('date_individual_format', ''),
                    template_data.get('heure_individual', ''),
                    template_data.get('duree_individual', ''),
                    template_data.get('salle_individuelle', '')
                ])
            
            # Créer le tableau
            table = Table(table_data, colWidths=[4*cm, 3*cm, 2.5*cm, 2.5*cm, 2*cm])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ]))
            
            story.append(table)
            story.append(Spacer(1, 1*cm))
            
            # Adresse
            story.append(Paragraph("<b>L'examen se déroulera à l'adresse suivante :</b>", normal_style))
            story.append(Spacer(1, 0.3*cm))
            
            address_text = f"""
            <b>{template_data.get('institution_name', 'Alliance Française')}</b><br/>
            {template_data.get('institution_address', 'Avenue des Arts 46')}<br/>
            {template_data.get('institution_postal', '1000')} {template_data.get('institution_city', 'Bruxelles')}
            """
            
            story.append(Paragraph(address_text, normal_style))
            story.append(Spacer(1, 1*cm))
            
            # Instructions finales
            instructions = """
            <b>IMPORTANT :</b><br/>
            • Vous devez vous présenter 15 minutes avant l'heure indiquée<br/>
            • Munissez-vous d'une pièce d'identité en cours de validité<br/>
            • Aucun retard ne sera toléré<br/>
            • Cette convocation est obligatoire pour accéder aux épreuves
            """
            
            story.append(Paragraph(instructions, normal_style))
            
            # Construire le PDF
            doc.build(story)
            
            logger.info(f"PDF généré avec succès: {output_filename}")
            return True
            
        except Exception as e:
            logger.error(f"Erreur génération PDF: {e}")
            import traceback
            traceback.print_exc()
            return False