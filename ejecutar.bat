@echo off
title AHORCADO PREMIUM - Christian Lera
color 0A

echo =======================================================================
echo                        AHORCADO PREMIUM
echo =======================================================================
echo.
echo Autor: Christian Lera
echo Version: 1.0
echo.
echo Iniciando el juego...
echo.

:: Verificar si Python está instalado
python --version > nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python no esta instalado en el sistema.
    echo.
    echo Por favor, instala Python desde: https://www.python.org/downloads/
    echo Asegurate de marcar la opcion "Add Python to PATH" durante la instalacion.
    echo.
    pause
    exit /b 1
)

:: Mostrar versión de Python
echo [INFO] Python detectado:
python --version
echo.

echo =======================================================================
echo                         INICIANDO JUEGO
echo =======================================================================
echo.

:: Ejecutar el juego directamente (sin verificaciones lentas)
python Ahorcado.py

echo.
echo =======================================================================
echo                    ¡Gracias por jugar! - Christian Lera
echo =======================================================================
echo.
pause