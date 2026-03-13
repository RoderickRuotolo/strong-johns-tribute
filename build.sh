#!/usr/bin/env bash
set -euo pipefail

python3 -m pip install -r requirements.txt
python3 -m pip install pyinstaller
pyinstaller --onefile --name strong_johns game.py

echo "Build complete: dist/strong_johns"
