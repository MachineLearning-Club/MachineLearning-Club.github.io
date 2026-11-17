#!/usr/bin/env python3
"""Compatibility entrypoint. The academic publisher owns the public design."""
from pathlib import Path
import runpy
runpy.run_path(str(Path(__file__).with_name("publish_academic.py")), run_name="__main__")
runpy.run_path(str(Path(__file__).with_name("generate_week89_notebooks.py")), run_name="__main__")
runpy.run_path(str(Path(__file__).with_name("generate_week89_quizzes.py")), run_name="__main__")
runpy.run_path(str(Path(__file__).with_name("update_week89.py")), run_name="__main__")
runpy.run_path(str(Path(__file__).with_name("update_week1011.py")), run_name="__main__")
runpy.run_path(str(Path(__file__).with_name("generate_week1011_starters.py")), run_name="__main__")
from apply_site_footer import main as apply_footer
apply_footer()
