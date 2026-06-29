import pandas as pd
import sys

# Read Excel file
df = pd.read_excel('JURYS FINAL TCF 11-18.xlsx', sheet_name='TCF CANADA', header=None)

print('First 10 rows (columns 0-7):')
print(df.iloc[0:10, 0:8])
print('\n' + '='*80 + '\n')

print('Checking for email column:')
for i in range(min(15, len(df.columns))):
    col_data = df.iloc[2:12, i].dropna()
    has_email = any('@' in str(v) for v in col_data)
    if has_email:
        print(f'\nColumn {i} contains emails:')
        print(col_data.tolist()[:5])  # Show first 5

print('\n' + '='*80 + '\n')
print('Column structure summary:')
for i in range(min(8, len(df.columns))):
    sample = df.iloc[5, i] if len(df) > 5 else None
    print(f'Column {i}: {sample}')
