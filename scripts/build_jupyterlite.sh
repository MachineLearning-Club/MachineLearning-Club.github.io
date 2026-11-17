#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
VENV="/tmp/mlclub-jlite-venv"
LITE_CONFIG="/tmp/mlclub-jlite-src"
python3 -m venv "$VENV"
"$VENV/bin/pip" install --disable-pip-version-check -q -r "$ROOT/scripts/jupyterlite-requirements.txt"
python3 "$ROOT/scripts/generate_week1_notebooks.py"
python3 "$ROOT/scripts/generate_week23_notebooks.py"
python3 "$ROOT/scripts/generate_week47_notebooks.py"
python3 "$ROOT/scripts/generate_week89_notebooks.py"
mkdir -p "$LITE_CONFIG/contents"
rm -f "$LITE_CONFIG"/contents/*.ipynb
cp "$ROOT"/w1/lab/notebooks/*.ipynb "$ROOT"/w2/lab/notebooks/*.ipynb "$ROOT"/w3/lab/notebooks/*.ipynb "$ROOT"/w4/lab/notebooks/*.ipynb "$ROOT"/w5/lab/notebooks/*.ipynb "$ROOT"/w6/lab/notebooks/*.ipynb "$ROOT"/w7/lab/notebooks/*.ipynb "$ROOT"/w8/lab/notebooks/*.ipynb "$ROOT"/w9/lab/notebooks/*.ipynb "$LITE_CONFIG/contents/"
"$VENV/bin/jupyter" lite build --lite-dir="$LITE_CONFIG" --contents="$LITE_CONFIG/contents" --output-dir="$ROOT/jupyter"
# The JupyterLite builder may merge its new index with old output contents.
# Remove entries for files that were intentionally renamed or removed.
python3 - "$ROOT/jupyter" <<'PY_CLEAN'
import json,sys
from pathlib import Path
root=Path(sys.argv[1])
manifest=root/'api/contents/all.json'
obj=json.loads(manifest.read_text())
if isinstance(obj.get('content'),list):
    before=len(obj['content'])
    obj['content']=[row for row in obj['content']
        if not str(row.get('name','')).endswith('.ipynb') or (root/'files'/str(row['name'])).exists()]
    if len(obj['content'])!=before:
        manifest.write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
        print('Pruned',before-len(obj['content']),'stale notebook entries')
PY_CLEAN
# Source maps are unnecessary developer assets (~50MB).
find "$ROOT/jupyter" -type f -name "*.map" -delete
echo "JupyterLite generated in $ROOT/jupyter; open /jupyter/lab/index.html?path=01-nearest-prototype.ipynb"
