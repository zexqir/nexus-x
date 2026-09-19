#!/usr/bin/env bash
set -euo pipefail
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
mkdir -p reports/{network,wireless,apk,secrets,assets,audits} logs plugins tests
echo "NEXUS-X installed. Run: source .venv/bin/activate && python3 -m nexus.cli"
