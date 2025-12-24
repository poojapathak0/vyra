@echo off
REM IntentLang Setup Script for Windows
echo ================================
echo  IntentLang Setup
echo ================================
echo.

REM Check Python installation
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found! Please install Python 3.8 or higher.
    echo Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [1/4] Checking Python version...
python --version

echo.
echo [2/4] Installing dependencies...
pip install -r requirements.txt

echo.
echo [3/4] Installing IntentLang...
pip install -e .

echo.
echo [4/4] Running tests...
pytest tests/ -v

echo.
echo ================================
echo  Setup Complete!
echo ================================
echo.
echo Try these commands:
echo   python -m intentlang run examples\hello.intent
echo   python -m intentlang repl
echo.
pause
