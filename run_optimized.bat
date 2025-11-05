@echo off
REM Screen Translator - Quick Start (Windows 11 Optimized Version)

echo.
echo ========================================
echo   Screen Translator - Windows 11
echo ========================================
echo.

REM Check if venv exists
if not exist "venv\" (
    echo [ERROR] Virtual environment not found!
    echo Please run setup.bat first to install dependencies.
    echo.
    pause
    exit /b 1
)

echo [INFO] Activating virtual environment...
call venv\Scripts\activate.bat

echo [INFO] Starting Screen Translator (Optimized Version)...
echo.
echo Press Ctrl+C to stop the application
echo.

python screen_translator_optimized.py

deactivate
