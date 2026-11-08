#!/usr/bin/env bash
set -e

echo "========================================================"
echo "   CLONE ANY UI (CAU) — Automated Setup (macOS / Linux)"
echo "========================================================"

if ! command -v python3 &> /dev/null; then
    echo "[-] Python 3 could not be found. Please install Python 3.10+."
    exit 1
fi

echo "[+] Upgrading pip..."
python3 -m pip install --upgrade pip

echo "[+] Installing core dependencies..."
python3 -m pip install -r requirements.txt

echo "[+] Installing local editable package 'cau'..."
python3 -m pip install -e .

echo "========================================================"
echo "[SUCCESS] CLONE ANY UI is installed and ready!"
echo ""
echo "Launch the Visual Studio GUI:"
echo "   python3 run_studio.py"
echo ""
echo "Or clone any website via CLI:"
echo "   cau --url https://example.com --out ./my-clone --all"
echo "========================================================"
