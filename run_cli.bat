@echo off
REM Screen Translator - CLI Quick Run

call venv\Scripts\activate.bat

echo.
echo Screen Translator CLI
echo =====================
echo.
echo Usage examples:
echo   Translate full screen:
echo     python translate_cli.py
echo.
echo   Translate to specific language:
echo     python translate_cli.py --lang en
echo.
echo   Translate region:
echo     python translate_cli.py --region 100 100 800 600
echo.
echo Running default (full screen to Vietnamese)...
echo.

python translate_cli.py %*

deactivate
pause
