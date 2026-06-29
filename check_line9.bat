cd /d "d:\convoc generator"
python -c "import pandas as pd; import numpy as np; df = pd.read_excel('JURYS.xlsx', sheet_name='Niveau B2', header=None, engine='openpyxl'); row = df.iloc[8]; print(f'Candidat ligne 9: {row[0]} {row[1]} {row[2]} {row[3]} {row[4]}'); print(f'Besoins spéciaux (Col G): {row[6]}'); print(f'Première ligne: {df.iloc[0][7]} {df.iloc[0][9]}')"
pause