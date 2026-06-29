# Script de construction simple pour ConvocationGenerator
# Utilise PyInstaller avec une configuration basique mais stable

# Installation des dépendances nécessaires
Write-Host "🔧 Installation de PyInstaller..." -ForegroundColor Blue
pip install pyinstaller>=5.0

Write-Host "🔧 Nettoyage des anciens builds..." -ForegroundColor Blue
if (Test-Path "dist") { Remove-Item -Recurse -Force "dist" }
if (Test-Path "build") { Remove-Item -Recurse -Force "build" }
if (Test-Path "*.spec") { Remove-Item "*.spec" }

Write-Host "🚀 Construction de l'exécutable..." -ForegroundColor Green

# Commande PyInstaller optimisée pour cette application
pyinstaller --onefile `
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
    --add-data "requirements.txt;." `
    --hidden-import tkinter `
    --hidden-import tkinter.ttk `
    --hidden-import tkinter.filedialog `
    --hidden-import tkinter.messagebox `
    --hidden-import pandas `
    --hidden-import numpy `
    --hidden-import openpyxl `
    --hidden-import jinja2 `
    --hidden-import xhtml2pdf `
    --hidden-import mailjet_rest `
    --hidden-import pdf_generator `
    --hidden-import jury_file_processor `
    --hidden-import mailjet_bridge `
    --hidden-import pytz `
    --collect-all pandas `
    --collect-all numpy `
    --exclude-module matplotlib `
    --exclude-module scipy `
    main.py

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Exécutable créé avec succès!" -ForegroundColor Green
    Write-Host "📁 Emplacement: dist\ConvocationGenerator.exe" -ForegroundColor Yellow
    
    # Vérification de la taille
    $exeFile = "dist\ConvocationGenerator.exe"
    if (Test-Path $exeFile) {
        $size = (Get-Item $exeFile).Length / 1MB
        Write-Host "📊 Taille: $([math]::Round($size, 1)) MB" -ForegroundColor Cyan
    }
    
    Write-Host "`n💡 Instructions:" -ForegroundColor Magenta
    Write-Host "   1. Testez l'exécutable: dist\ConvocationGenerator.exe"
    Write-Host "   2. Copiez le fichier .exe où vous voulez"
    Write-Host "   3. L'exécutable est portable (pas d'installation requise)"
    
} else {
    Write-Host "❌ Erreur lors de la construction" -ForegroundColor Red
    Write-Host "🔍 Vérifiez les erreurs ci-dessus" -ForegroundColor Yellow
}

Write-Host "`nAppuyez sur une touche pour continuer..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")