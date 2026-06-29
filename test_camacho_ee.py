"""
Test de génération PDF pour CAMACHO GONZALEZ Amys (EE + EO)
"""
from tcf_excel_processor import TCFExcelProcessor
from pdf_generator import PDFGenerator

parser = TCFExcelProcessor('JURYS FINAL TCF.xlsx')
parser.load_tcf_data()

# Trouver CAMACHO dans EE
candidates_ee = parser.get_candidates_by_tcf_type('TCF TP EE')
camacho_ee = [c for c in candidates_ee if 'CAMACHO' in c['nom']][0]

print("Génération convocation CAMACHO EE...")
print(f"Durée collective: {camacho_ee['duree_collective']}")
print(f"Début: {camacho_ee['debut_ep_coll']}")
print(f"Fin: {camacho_ee['fin_ep_coll']}")

# Générer le PDF
gen = PDFGenerator(
    template_path='templates/convocation_tcf_template_modele.html',
    output_dir='output',
    logo_path='logo_afbe_couleur.png',
    logo_tcf_path='logo_tcf_tout_public.png',
    qrcode_path='qrcode_afbe.png',
    access_code='121391#'
)

pdf_path = gen.generate_pdf(camacho_ee, 'test_CAMACHO_EE.pdf')
print(f"\n✅ PDF généré: {pdf_path}")
