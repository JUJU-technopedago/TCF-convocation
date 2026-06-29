# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all

datas = [('templates', 'templates'), ('templates_fixed', 'templates_fixed'), ('assets', 'assets'), ('logoAF.svg', '.'), ('logoDELF.svg', '.'), ('modele_convocation.docx', '.'), ('graphics_config.json', '.'), ('*.json', '.'), ('requirements.txt', '.')]
binaries = []
hiddenimports = ['tkinter', 'tkinter.ttk', 'tkinter.filedialog', 'tkinter.messagebox', 'tkinter.font', 'pandas', 'pandas.core', 'numpy', 'numpy.core', 'numpy.core._multiarray_umath', 'openpyxl', 'openpyxl.workbook', 'openpyxl.worksheet', 'jinja2', 'jinja2.ext', 'xhtml2pdf', 'xhtml2pdf.default', 'mailjet_rest', 'cryptography', 'reportlab', 'reportlab.graphics', 'reportlab.graphics.barcode', 'reportlab.graphics.barcode.code128', 'pdf_generator', 'jury_file_processor', 'mailjet_bridge', 'email_auth', 'oauth_auth', 'login_dialog']
tmp_ret = collect_all('pandas')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('numpy')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['matplotlib', 'scipy', 'IPython', 'jupyter', 'pytest', 'sphinx', 'numba'],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='ConvocationGenerator',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['assets\\logo.ico'],
)
