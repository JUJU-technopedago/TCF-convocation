#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de diagnostic pour la génération de PDF
"""

import os
import sys
from pathlib import Path

# Configurer l'encodage pour les sorties
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

print("=== DIAGNOSTIC DE GÉNÉRATION PDF ===")

# 1. Vérifier les moteurs PDF disponibles
print("\n1. MOTEURS PDF DISPONIBLES:")

try:
    import pdfkit
    print("✅ pdfkit est installé")
    PDF_ENGINE_PDFKIT = True
except ImportError:
    print("❌ pdfkit n'est pas installé")
    PDF_ENGINE_PDFKIT = False

try:
    import weasyprint
    print("✅ weasyprint est installé")
    PDF_ENGINE_WEASYPRINT = True
except ImportError:
    print("❌ weasyprint n'est pas installé")
    PDF_ENGINE_WEASYPRINT = False

try:
    from xhtml2pdf import pisa
    print("✅ xhtml2pdf est installé")
    PDF_ENGINE_XHTML2PDF = True
except ImportError:
    print("❌ xhtml2pdf n'est pas installé")
    PDF_ENGINE_XHTML2PDF = False

# 2. Vérifier si wkhtmltopdf est installé (requis pour pdfkit)
if PDF_ENGINE_PDFKIT:
    print("\n2. VÉRIFICATION WKHTMLTOPDF:")
    try:
        path_wk = pdfkit.configuration().wkhtmltopdf
        if path_wk and os.path.exists(path_wk):
            print(f"✅ wkhtmltopdf trouvé: {path_wk}")
        else:
            print(f"⚠️ wkhtmltopdf path configuré mais non trouvé: {path_wk}")
    except Exception as e:
        print(f"❌ Erreur lors de la vérification de wkhtmltopdf: {e}")
else:
    print("\n2. VÉRIFICATION WKHTMLTOPDF: Ignoré (pdfkit non installé)")

# 3. Tester la génération d'un PDF simple
print("\n3. TEST DE GÉNÉRATION PDF SIMPLE:")

html_content = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Test PDF</title>
</head>
<body>
    <h1>Test PDF Génération</h1>
    <p>Ceci est un test de génération PDF avec caractères spéciaux: éàçùïö</p>
    <p>Test de caractères spéciaux avancés: ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖØÙÚÛÜÝ</p>
</body>
</html>
"""

output_dir = "output_test"
os.makedirs(output_dir, exist_ok=True)

# Tester pdfkit
if PDF_ENGINE_PDFKIT:
    print("\nTest pdfkit:")
    try:
        output_path = os.path.join(output_dir, "test_pdfkit.pdf")
        options = {
            'page-size': 'A4',
            'encoding': "UTF-8",
            'enable-local-file-access': None
        }
        pdfkit.from_string(html_content, output_path, options=options)
        if os.path.exists(output_path):
            print(f"✅ PDF généré avec succès: {output_path} ({os.path.getsize(output_path)} bytes)")
        else:
            print(f"❌ Échec: Fichier non créé")
    except Exception as e:
        print(f"❌ Erreur: {e}")

# Tester weasyprint
if PDF_ENGINE_WEASYPRINT:
    print("\nTest WeasyPrint:")
    try:
        output_path = os.path.join(output_dir, "test_weasyprint.pdf")
        html_doc = weasyprint.HTML(string=html_content)
        html_doc.write_pdf(output_path)
        if os.path.exists(output_path):
            print(f"✅ PDF généré avec succès: {output_path} ({os.path.getsize(output_path)} bytes)")
        else:
            print(f"❌ Échec: Fichier non créé")
    except Exception as e:
        print(f"❌ Erreur: {e}")

# Tester xhtml2pdf
if PDF_ENGINE_XHTML2PDF:
    print("\nTest xhtml2pdf:")
    try:
        output_path = os.path.join(output_dir, "test_xhtml2pdf.pdf")
        with open(output_path, "w+b") as result_file:
            pisa_status = pisa.CreatePDF(
                html_content,
                dest=result_file,
                encoding='utf-8'
            )
        if pisa_status.err:
            print(f"❌ Erreur: {pisa_status.err}")
        elif os.path.exists(output_path):
            print(f"✅ PDF généré avec succès: {output_path} ({os.path.getsize(output_path)} bytes)")
        else:
            print(f"❌ Échec: Fichier non créé")
    except Exception as e:
        print(f"❌ Erreur: {e}")

# 4. Tester la génération avec un nom de fichier contenant des caractères spéciaux
print("\n4. TEST DE NOM DE FICHIER AVEC CARACTÈRES SPÉCIAUX:")

# Fonction pour tester les noms de fichiers
def test_filename(filename):
    try:
        output_path = os.path.join(output_dir, filename)
        with open(output_path, "w+b") as result_file:
            pisa_status = pisa.CreatePDF(
                html_content,
                dest=result_file,
                encoding='utf-8'
            )
        if pisa_status.err:
            return False, f"Erreur: {pisa_status.err}"
        elif os.path.exists(output_path):
            return True, f"Fichier créé: {output_path} ({os.path.getsize(output_path)} bytes)"
        else:
            return False, "Fichier non créé"
    except Exception as e:
        return False, f"Exception: {e}"

# Tester différents noms de fichiers
filenames = [
    "test_normal.pdf",
    "test_accent_é.pdf",
    "test_multiple_àçêüñ.pdf",
    "Müller_Hans.pdf",
    "convocation_Müller_Hans_123456.pdf"
]

for filename in filenames:
    success, message = test_filename(filename)
    status = "✅" if success else "❌"
    print(f"{status} {filename}: {message}")

# 5. Vérifier la configuration de l'encodage système
print("\n5. CONFIGURATION ENCODAGE SYSTÈME:")
print(f"Encodage par défaut: {sys.getdefaultencoding()}")
print(f"Encodage fichier: {sys.getfilesystemencoding()}")
print(f"Locale: {', '.join([f'{k}={v}' for k, v in os.environ.items() if k.startswith('LC_') or k == 'LANG'])}")

print("\n=== FIN DU DIAGNOSTIC ===")
print("Veuillez consulter le répertoire 'output_test' pour les fichiers PDF générés.")