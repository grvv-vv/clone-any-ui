@echo off
setlocal
echo ========================================================
echo    CLONE ANY UI (CAU) — Automated Setup
echo ========================================================

python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python 3 is not installed or not in PATH.
    echo Please install Python 3.10+ from https://python.org
    pause
    exit /b 1
)

echo [+] Upgrading pip...
python -m pip install --upgrade pip

echo [+] Installing core dependencies (requests, beautifulsoup4, pillow)...
python -m pip install -r requirements.txt

echo [+] Installing local editable package 'cau'...
python -m pip install -e .

echo ========================================================
echo [SUCCESS] CLONE ANY UI is installed and ready!
echo.
echo Launch the Visual Studio GUI:
echo    python run_studio.py
echo.
echo Or clone any website via CLI:
echo    cau --url https://example.com --out ./my-clone --all
echo ========================================================
pause

