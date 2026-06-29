# Script PowerShell pour résoudre le problème CAST5
Write-Host "🔧 RESOLUTION PROBLEME CRYPTOGRAPHY/CAST5" -ForegroundColor Blue
Write-Host "============================================" -ForegroundColor Blue
Write-Host ""

Write-Host "1. Diagnostic du problème..." -ForegroundColor Yellow
Write-Host "   Le problème CAST5 vient d'une incompatibilité entre cryptography et mailjet"
Write-Host ""

Write-Host "2. Nettoyage des packages problématiques..." -ForegroundColor Yellow
pip uninstall -y cryptography pyOpenSSL mailjet-rest paramiko 2>$null

Write-Host ""
Write-Host "3. Installation des versions compatibles..." -ForegroundColor Green
pip install cryptography==41.0.7
pip install mailjet-rest==1.3.4  
pip install pyinstaller>=5.0
pip install pandas openpyxl jinja2 xhtml2pdf

Write-Host ""
Write-Host "4. Test des imports..." -ForegroundColor Yellow
$testResult = python -c "
try:
    import cryptography; print('✅ cryptography OK')
    import mailjet_rest; print('✅ mailjet_rest OK')
    import pandas; print('✅ pandas OK')  
    import jinja2; print('✅ jinja2 OK')
    print('SUCCESS')
except Exception as e:
    print(f'ERROR: {e}')
" 2>&1

if ($testResult -notcontains "SUCCESS") {
    Write-Host "⚠️  Tentative de solution alternative..." -ForegroundColor Yellow
    pip install --force-reinstall cryptography==40.0.2
}

Write-Host ""
Write-Host "5. Nettoyage des anciens builds..." -ForegroundColor Yellow
if (Test-Path "dist") { Remove-Item -Recurse -Force "dist" }
if (Test-Path "build") { Remove-Item -Recurse -Force "build" }
if (Test-Path "*.spec") { Remove-Item "*.spec" }

Write-Host ""
Write-Host "6. Construction avec exclusions CAST5..." -ForegroundColor Green

$buildResult = pyinstaller --onefile `
    --windowed `
    --name "ConvocationGenerator" `
    --add-data "templates;templates" `
    --add-data "templates_fixed;templates_fixed" `
    --add-data "assets;assets" `
    --add-data "*.json;." `
    --add-data "*.xlsx;." `
    --add-data "*.docx;." `
    --add-data "*.svg;." `
    --add-data "*.png;." `
    --hidden-import tkinter `
    --hidden-import tkinter.ttk `
    --hidden-import tkinter.filedialog `
    --hidden-import tkinter.messagebox `
    --hidden-import pandas `
    --hidden-import openpyxl `
    --hidden-import jinja2 `
    --hidden-import xhtml2pdf `
    --hidden-import mailjet_rest `
    --hidden-import pdf_generator `
    --hidden-import jury_file_processor `
    --hidden-import mailjet_bridge `
    --exclude-module cryptography.hazmat.decrepit.ciphers.algorithms.cast5 `
    --exclude-module CAST5 `
    --exclude-module numpy `
    --exclude-module matplotlib `
    --exclude-module scipy `
    main.py 2>&1

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✅ CONSTRUCTION REUSSIE!" -ForegroundColor Green
    Write-Host "📁 Exécutable: dist\ConvocationGenerator.exe" -ForegroundColor Cyan
    Write-Host "🔧 Problème CAST5 résolu" -ForegroundColor Green
    
    if (Test-Path "dist\ConvocationGenerator.exe") {
        $size = (Get-Item "dist\ConvocationGenerator.exe").Length / 1MB
        Write-Host "📊 Taille: $([math]::Round($size, 1)) MB" -ForegroundColor Cyan
    }
} else {
    Write-Host ""
    Write-Host "❌ CONSTRUCTION ECHOUEE" -ForegroundColor Red
    Write-Host "💡 Solutions alternatives:" -ForegroundColor Yellow
    Write-Host "   - Essayez build_no_crypto.bat (sans mailjet)" -ForegroundColor White
    Write-Host "   - Ou redémarrez et re-essayez" -ForegroundColor White
}

Write-Host ""
Write-Host "Appuyez sur une touche pour continuer..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")