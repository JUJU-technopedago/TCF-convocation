cd /d "d:\convoc generator"
python -c "import pandas as pd; xls = pd.ExcelFile('JURYS.xlsx', engine='openpyxl'); print('Onglets trouves:'); [print(f'  - {sheet}') for sheet in xls.sheet_names]"
pause