#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test simple de génération PDF avec xhtml2pdf - template minimal
"""

from xhtml2pdf import pisa
import os

# Template HTML minimal
html = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
    body { font-family: Arial, sans-serif; margin: 20px; }
    table { width: 100%; border-collapse: collapse; }
    td { border: 1px solid black; padding: 5px; }
</style>
</head>
<body>
<h1>Test Convocation</h1>
<p>Candidat: DUPONT Jean</p>
<table>
<tr>
<td style="width: 40%;">Gauche</td>
<td style="width: 60%;">Droite</td>
</tr>
</table>
</body>
</html>
"""

# Générer le PDF
output_path = "output/test_minimal.pdf"
os.makedirs("output", exist_ok=True)

with open(output_path, "wb") as f:
    pisa_status = pisa.CreatePDF(html.encode('utf-8'), dest=f)

if pisa_status.err:
    print(f"[ERREUR] Generation PDF echouee")
else:
    print(f"[OK] PDF genere: {output_path}")
