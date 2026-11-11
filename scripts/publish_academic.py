#!/usr/bin/env python3
"""Compatibility wrapper for the current 3 + 6 + 6 academic publisher."""
from pathlib import Path
import runpy
runpy.run_path(str(Path(__file__).with_name("publish_v3.py")),run_name="__main__")
