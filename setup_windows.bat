@echo off
REM Screen Translator - Enhanced Setup Script for Windows with Error Handling

echo.
echo ========================================
echo   Screen Translator - Setup
echo ========================================
echo.

REM Check Python installation
echo [1/5] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH!
    echo Please install Python 3.10-3.13 from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation.
    echo.
    echo NOTE: Python 3.14 may have compatibility issues. We recommend Python 3.10-3.11
    pause
    exit /b 1
)

python --version
echo [OK] Python found!
echo.

REM Check Python version and warn if too new
for /f "tokens=2" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo [INFO] Detected Python version: %PYTHON_VERSION%
if "%PYTHON_VERSION:~0,4%"=="3.14" (
    echo [WARNING] Python 3.14 is very new and some packages may not have pre-built wheels.
    echo [WARNING] If installation fails, please consider using Python 3.10 or 3.11.
    echo.
    timeout /t 3
)

REM Create virtual environment
echo [2/5] Creating virtual environment...
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
echo [3/5] Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip and install build tools
echo [4/5] Upgrading pip and setuptools...
python -m pip install --upgrade pip setuptools wheel
if errorlevel 1 (
    echo [WARNING] Failed to upgrade pip/setuptools
)
echo.

REM Install dependencies with error handling
echo [5/5] Installing dependencies...
echo [INFO] This may take 5-10 minutes...
echo.

REM Try Windows-optimized requirements first
if exist "requirements_windows.txt" (
    echo [INFO] Using Windows-optimized requirements...
    pip install -r requirements_windows.txt
) else (
    pip install -r requirements.txt
)

if errorlevel 1 (
    echo.
    echo [WARNING] Some packages failed to install!
    echo.
    echo Let's try installing core packages individually...
    echo.

    REM Install core packages one by one
    echo [1/7] Installing mss...
    pip install mss>=9.0.1

    echo [2/7] Installing Pillow...
    pip install pillow>=10.0.0

    echo [3/7] Installing numpy...
    pip install "numpy>=1.24.0,<2.0"

    echo [4/7] Installing opencv-python...
    pip install opencv-python>=4.8.0

    echo [5/7] Installing googletrans...
    pip install googletrans==4.0.0rc1

    echo [6/7] Installing torch (this may take a while)...
    pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu

    echo [7/7] Installing easyocr...
    pip install easyocr>=1.7.0 --no-deps
    pip install python-bidi>=0.4.2 PyYAML>=5.3.1 opencv-python-headless>=4.1.2.30

    if errorlevel 1 (
        echo.
        echo [ERROR] Installation failed!
        echo.
        echo Common solutions:
        echo   1. Try Python 3.10 or 3.11 instead of 3.14
        echo   2. Install Visual Studio Build Tools from:
        echo      https://visualstudio.microsoft.com/visual-cpp-build-tools/
        echo   3. Check your internet connection
        echo.
        pause
        deactivate
        exit /b 1
    )
)

echo.
echo [INFO] Testing installation...
python -c "import mss, PIL, cv2, numpy; print('[OK] Core packages imported successfully!')" 2>nul
if errorlevel 1 (
    echo [WARNING] Some imports failed, but basic functionality may still work
) else (
    echo [OK] All core packages working!
)

echo.
echo ========================================
echo   Setup Complete!
echo ========================================
echo.
echo Next steps:
echo   1. Run: run_optimized.bat
echo   2. Click "Initialize OCR Engine" (first time only)
echo      - This will download OCR models (~500MB-1GB)
echo      - May take 3-5 minutes depending on internet speed
echo   3. Select preset and start translating!
echo.
echo Quick Start:
echo   For anime subtitles: Use "Subtitle Mode" + Auto Mode
echo   For manga: Use "Manga Mode" + Manual capture
echo.
echo If OCR initialization fails, you may need to install it manually:
echo   pip install easyocr
echo.
echo Troubleshooting:
echo   - If app doesn't start, try: python screen_translator.py
echo   - For detailed help, see INSTALLATION.md
echo.
echo Enjoy!
echo.

deactivate
pause
