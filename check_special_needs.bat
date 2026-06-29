cd /d "d:\convoc generator"
python -c "import pandas as pd; import numpy as np; df = pd.read_excel('JURYS.xlsx', sheet_name='Niveau B2', header=None, engine='openpyxl'); found = False; [print(f'Row {i+1}, Col G: {row[6]}') for i, row in df.iterrows() if isinstance(row[6], str) and 'oui' in row[6].lower()]"
pause