#!/usr/bin/env bash
set -euo pipefail

# Run the Flask API locally on localhost:5000.
# Usage:
#   chmod +x run.sh
#   ./run.sh

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

exec python3 app.py
