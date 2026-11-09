#!/usr/bin/env python3
"""CLONE ANY UI (CAU) — Studio Web Application Launcher.

Starts the CAU Web Studio dashboard:
  python run_studio.py
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

STUDIO_DIR = Path(__file__).parent / "studio"
if not STUDIO_DIR.exists():
    sys.exit(f"[-] Studio directory not found at: {STUDIO_DIR}")

sys.path.insert(0, str(STUDIO_DIR))

try:
    from server import start_studio
except ImportError as e:
    sys.exit(f"[-] Failed to import studio server: {e}")

def main():
    start_studio(port=3000, open_browser=True)

if __name__ == "__main__":
    main()

