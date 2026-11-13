#!/usr/bin/env python3
"""Offline regression checks for the beginner Python guide."""
import json
import ast
import subprocess
import sys
from pathlib import Path

root = Path(__file__).resolve().parent.parent
lessons = json.loads((root / "data/python_foundations_lessons.json").read_text(encoding="utf-8"))["lessons"]
page = (root / "guides/python/index.html").read_text(encoding="utf-8")
home = (root / "index.html").read_text(encoding="utf-8")
publisher = (root / "scripts/publish_v3.py").read_text(encoding="utf-8")

assert len(lessons) == 21
assert page.count('class="foundation-lesson"') == len(lessons)
assert page.count('class="foundation-solution"') == len(lessons)
assert page.count('class="python-runner"') == 2 * len(lessons)
assert '/guides/python/' in home and '/guides/python/' in publisher
assert 'assets/academic-ui.js' in page
assert 'assets/python-foundations.css' in page

for number, lesson in enumerate(lessons, 1):
    assert f'id="topic-{number:02d}"' in page
    for key in ("code", "solution"):
        code = lesson[key]
        compile(code, f"topic-{number}-{key}", "exec")
        tree = ast.parse(code)
        assert not any(isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "input" for node in ast.walk(tree)), (number, key, "browser runner lacks stdin")
        proc = subprocess.run([sys.executable, "-c", code],
                              text=True, capture_output=True, timeout=3, check=False)
        assert proc.returncode == 0, (number, key, proc.stderr)
print(f"PASS: {len(lessons)} lessons, {len(lessons)*2} executable scripts, links, toggles and editor widgets")
