@echo off
REM Screen Translator - Setup Script for Windows

echo.
echo ========================================
echo   Screen Translator - Setup
echo ========================================
echo.

REM Check Python installation
echo [1/4] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH!
    echo Please install Python 3.8+ from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)

python --version
echo [OK] Python found!
echo.

REM Create virtual environment
echo [2/4] Creating virtual environment...
if exist "venv\" (
    echo [INFO] Virtual environment already exists, skipping...
) else (
    python -m venv venv
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment!
        pause
        exit /b 1
    )
    echo [OK] Virtual environment created!
)
echo.

REM Activate venv
echo [3/4] Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo [INFO] Upgrading pip...
python -m pip install --upgrade pip

REM Install dependencies
echo [4/4] Installing dependencies...
echo [INFO] This may take 5-10 minutes...
echo.
pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo [ERROR] Failed to install dependencies!
    echo Please check your internet connection and try again.
    pause
    deactivate
    exit /b 1
)

echo.
echo ========================================
echo   Setup Complete!
echo ========================================
echo.
echo Next steps:
echo   1. Run: run_optimized.bat
echo   2. Click "Initialize OCR Engine" (first time only)
echo   3. Select preset and start translating!
echo.
echo For subtitle translation:
echo   - Use "Subtitle Mode" preset
echo   - Enable Auto Mode
echo.
echo For manga translation:
echo   - Use "Manga Mode" preset
echo   - Manual capture
echo.
echo Enjoy!
echo.

deactivate
pause
