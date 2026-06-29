from pdf_generator import PDFGenerator
from tcf_excel_processor import TCFExcelProcessor

processor = TCFExcelProcessor('JURYS FINAL TCF.xlsx')
candidates = processor.parse_excel()
first_candidate = candidates[0]

gen = PDFGenerator('templates/convocation_tcf_template_simple.html', {})
data = gen._prepare_template_data(first_candidate)
template = gen._select_template(first_candidate['tcf_type'])
html = template.render(**data)

with open('test_output.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('HTML generated')
