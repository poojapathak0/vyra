#!/bin/bash
# Vyra Setup Script for Linux/Mac

echo "================================"
echo " Vyra Setup"
echo "================================"
echo ""

# Check Python installation
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 not found! Please install Python 3.8 or higher."
    exit 1
fi

echo "[1/4] Checking Python version..."
python3 --version

echo ""
echo "[2/4] Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

echo ""
echo "[3/4] Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
pip install -e .

echo ""
echo "[4/4] Running tests..."
pytest tests/ -v

echo ""
echo "================================"
echo " Setup Complete!"
echo "================================"
echo ""
echo "Activate the virtual environment with:"
echo "  source venv/bin/activate"
echo ""
echo "Try these commands:"
echo "  python -m vyra run examples/hello.vyra"
echo "  python -m vyra repl"
echo ""
