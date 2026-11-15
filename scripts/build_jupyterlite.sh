#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
VENV="/tmp/mlclub-jlite-venv"
LITE_CONFIG="/tmp/mlclub-jlite-src"
python3 -m venv "$VENV"
"$VENV/bin/pip" install --disable-pip-version-check -q -r "$ROOT/scripts/jupyterlite-requirements.txt"
python3 "$ROOT/scripts/generate_week1_notebooks.py"
mkdir -p "$LITE_CONFIG"
"$VENV/bin/jupyter" lite build --lite-dir="$LITE_CONFIG" --contents="$ROOT/w1/lab/notebooks" --output-dir="$ROOT/jupyter"
# Source maps are unnecessary developer assets (~50MB).
find "$ROOT/jupyter" -type f -name "*.map" -delete
echo "JupyterLite generated in $ROOT/jupyter; open /jupyter/lab/index.html?path=01-nearest-prototype.ipynb"
