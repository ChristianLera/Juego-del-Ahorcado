# ejecutar.ps1 - Script para ejecutar el Ahorcado Premium en PowerShell
# Autor: Christian Lera

Write-Host "=======================================================================" -ForegroundColor Cyan
Write-Host "                        🎮 AHORCADO PREMIUM 🎮" -ForegroundColor Yellow
Write-Host "=======================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Autor: Christian Lera" -ForegroundColor White
Write-Host "Versión: 1.0" -ForegroundColor White
Write-Host ""
Write-Host "Iniciando el juego..." -ForegroundColor Green
Write-Host ""

# Verificar si Python está instalado
try {
    $pythonVersion = python --version 2>&1
    Write-Host "[INFO] Python detectado:" -ForegroundColor Cyan
    Write-Host $pythonVersion -ForegroundColor White
    Write-Host ""
}
catch {
    Write-Host "[ERROR] Python no está instalado en el sistema." -ForegroundColor Red
    Write-Host ""
    Write-Host "Por favor, instala Python desde: https://www.python.org/downloads/" -ForegroundColor Yellow
    Write-Host "Asegúrate de marcar la opción 'Add Python to PATH' durante la instalación." -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Presiona Enter para salir"
    exit 1
}

# Verificar si está instalado el módulo 'datasets'
Write-Host "[INFO] Verificando dependencias..." -ForegroundColor Cyan

$datasetsInstalled = python -c "import datasets" 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "[ADVERTENCIA] El módulo 'datasets' no está instalado." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Para instalarlo, ejecuta: pip install datasets" -ForegroundColor White
    Write-Host "O usa el script: .\install_requirements.ps1" -ForegroundColor White
    Write-Host ""
    $respuesta = Read-Host "¿Deseas instalar las dependencias ahora? (S/N)"
    
    if ($respuesta -eq "S" -or $respuesta -eq "s") {
        Write-Host ""
        Write-Host "Instalando datasets..." -ForegroundColor Cyan
        pip install datasets
        
        if ($LASTEXITCODE -ne 0) {
            Write-Host "[ERROR] Falló la instalación de dependencias." -ForegroundColor Red
            Read-Host "Presiona Enter para salir"
            exit 1
        }
        Write-Host "[OK] Dependencias instaladas correctamente." -ForegroundColor Green
    }
    else {
        Write-Host ""
        Write-Host "[INFO] Continuando sin el módulo 'datasets'." -ForegroundColor Yellow
        Write-Host "Se usará el diccionario de respaldo." -ForegroundColor Yellow
        Start-Sleep -Seconds 2
    }
}
else {
    Write-Host "[OK] Dependencias verificadas." -ForegroundColor Green
}

Write-Host ""
Write-Host "=======================================================================" -ForegroundColor Cyan
Write-Host "                         🎮 INICIANDO JUEGO 🎮" -ForegroundColor Yellow
Write-Host "=======================================================================" -ForegroundColor Cyan
Write-Host ""

# Ejecutar el juego
try {
    python Ahorcado.py
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host ""
        Write-Host "[ERROR] El juego se cerró inesperadamente." -ForegroundColor Red
        Write-Host ""
        Read-Host "Presiona Enter para salir"
        exit 1
    }
}
catch {
    Write-Host "[ERROR] No se pudo ejecutar el juego." -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    Read-Host "Presiona Enter para salir"
    exit 1
}

Write-Host ""
Write-Host "=======================================================================" -ForegroundColor Cyan
Write-Host "                    ¡Gracias por jugar! - Christian Lera" -ForegroundColor Green
Write-Host "=======================================================================" -ForegroundColor Cyan
Write-Host ""
Read-Host "Presiona Enter para salir"