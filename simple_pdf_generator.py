#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Générateur PDF simple pour TCF utilisant weasyprint
"""

import os
import logging
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML, CSS

logger = logging.getLogger(__name__)

class SimplePDFGenerator:
    """Générateur PDF simple pour les convocations TCF"""
    
    def __init__(self, config=None):
        self.config = config or {}
        
    def generate_convocation(self, template_data, output_filename, template_name="convocation_tcf_template_modele.html"):
        """
        Générer une convocation PDF
        
        Args:
            template_data: Dictionnaire des données pour le template
            output_filename: Nom du fichier PDF de sortie
            template_name: Nom du template à utiliser
            
        Returns:
            bool: True si succès, False sinon
        """
        try:
            # 1. Charger et rendre le template
            template_dir = "templates"
            if not os.path.exists(template_dir):
                logger.error(f"Répertoire templates non trouvé: {template_dir}")
                return False
                
            template_path = os.path.join(template_dir, template_name)
            if not os.path.exists(template_path):
                logger.error(f"Template non trouvé: {template_path}")
                return False
            
            # Configurer Jinja2
            env = Environment(loader=FileSystemLoader(template_dir))
            template = env.get_template(template_name)
            
            # Rendre le template
            html_content = template.render(**template_data)
            
            logger.info(f"Template rendu: {len(html_content)} caractères")
            
            # 2. Sauvegarder le HTML temporaire pour debug
            temp_html = output_filename.replace('.pdf', '_temp.html')
            with open(temp_html, 'w', encoding='utf-8') as f:
                f.write(html_content)
            logger.info(f"HTML temporaire sauvegardé: {temp_html}")
            
            # 3. Générer le PDF
            html_doc = HTML(string=html_content, base_url=os.getcwd())
            
            # CSS pour l'impression
            css_print = CSS(string='''
                @page {
                    size: A4;
                    margin: 1cm 2cm 2cm 2cm;
                }
                
                body {
                    font-family: Tahoma, Arial, sans-serif;
                    font-size: 11pt;
                    color: #000;
                }
                
                .logo-left, .logo-right {
                    max-width: 150px;
                    max-height: 60px;
                }
            ''')
            
            html_doc.write_pdf(output_filename, stylesheets=[css_print])
            
            logger.info(f"PDF généré: {output_filename}")
            
            # Nettoyer le fichier temporaire
            if os.path.exists(temp_html):
                os.remove(temp_html)
            
            return True
            
        except Exception as e:
            logger.error(f"Erreur génération PDF: {e}")
            import traceback
            traceback.print_exc()
            return False