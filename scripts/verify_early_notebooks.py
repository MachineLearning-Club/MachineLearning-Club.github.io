#!/usr/bin/env python3
"""Execute all Week 1–7 notebooks with a tiny display-only SVG shim.

This is a local numerical/syntax smoke test, not a substitute for running
JupyterLite in the browser. The shim validates generated SVG markup while
suppressing rich display; it does not modify students' notebooks.
"""
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
import ast
import json
import sys
import types
from xml.etree import ElementTree

ROOT=Path(__file__).resolve().parents[1]
ipython=types.ModuleType("IPython")
ipython.get_ipython=lambda:None
ipython.version_info=(9,0,0)
display=types.ModuleType("IPython.display")
display.SVG=lambda svg:ElementTree.fromstring(svg)
display.display=lambda *items,**kwargs:None
ipython.display=display
sys.modules["IPython"]=ipython
sys.modules["IPython.display"]=display

def main():
    paths=[]
    for week in range(1,8):
        base=ROOT/f"w{week}/lab"
        paths.append(base/"starter.ipynb")
        paths.extend(sorted((base/"notebooks").glob("*.ipynb")))
    assert len(paths)==22,f"Expected 22 reviewed early notebooks, found {len(paths)}"
    failed=[]
    for path in paths:
        try:
            nb=json.loads(path.read_text(encoding="utf-8"))
            assert nb["nbformat"]==4
            assert any(c["cell_type"]=="code" for c in nb["cells"])
            namespace={"__name__":"__main__"}
            output=StringIO()
            for index,c in enumerate(nb["cells"]):
                if c["cell_type"]!="code":continue
                source="".join(c["source"])
                ast.parse(source,filename=str(path))
                with redirect_stdout(output):
                    exec(compile(source,str(path)+f" cell {index}","exec"),namespace)
            print("PASS",path.relative_to(ROOT))
        except Exception as exc:
            failed.append((path,repr(exc)))
    if failed:
        for path,why in failed:print("FAIL",path.relative_to(ROOT),why)
        raise SystemExit(f"{len(failed)} early notebooks failed")
    print(f"PASS — {len(paths)} notebooks executed, generated SVG parsed successfully")

if __name__=="__main__":
    main()
