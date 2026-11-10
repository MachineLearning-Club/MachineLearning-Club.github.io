#!/usr/bin/env python3
"""Compatibility entrypoint. The academic publisher owns the public design."""
from pathlib import Path
import runpy
runpy.run_path(str(Path(__file__).with_name("publish_academic.py")), run_name="__main__")
