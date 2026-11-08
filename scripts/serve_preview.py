#!/usr/bin/env python3
"""CLONE ANY UI (CAU) — Instant Local Server & Live Preview Launcher.

Launches a lightweight local HTTP server, automatically selects an available port,
and opens your default browser directly to the clone preview or mirrored site.

Usage:
  python serve_preview.py --dir ./my-clone
  python serve_preview.py --dir ./my-clone --port 3000
"""

from __future__ import annotations

import argparse
import http.server
import socket
import socketserver
import sys
import webbrowser
from pathlib import Path


def find_free_port(start_port: int = 3000) -> int:
    port = start_port
    while port < 65535:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(('127.0.0.1', port)) != 0:
                return port
        port += 1
    return start_port


def main() -> None:
    parser = argparse.ArgumentParser(description="CAU — Instant Local Server & Live Preview.")
    parser.add_argument("--dir", default=".", help="Root directory to serve")
    parser.add_argument("--port", type=int, help="Optional specific port")
    parser.add_argument("--no-browser", action="store_true", help="Do not open browser automatically")
    args = parser.parse_args()

    serve_dir = Path(args.dir).resolve()
    if not serve_dir.exists():
        sys.exit(f"[-] Directory not found: {serve_dir}")

    port = args.port or find_free_port(3000)

    # Check for target files
    preview_file = "preview.html" if (serve_dir / "preview.html").exists() else ("site/index.html" if (serve_dir / "site/index.html").exists() else "index.html")
    url = f"http://localhost:{port}/{preview_file}"

    class CustomHandler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *h_args, **h_kwargs):
            super().__init__(*h_args, directory=str(serve_dir), **h_kwargs)

    print("=" * 60)
    print("⚡ CLONE ANY UI (CAU) — LOCAL PREVIEW SERVER ACTIVE")
    print("=" * 60)
    print(f"📁 Serving Directory: {serve_dir}")
    print(f"🌐 Local URL:         {url}")
    print("👉 Press Ctrl+C to terminate the server.\n")

    if not args.no_browser:
        try:
            webbrowser.open(url)
        except Exception:
            pass

    try:
        with socketserver.TCPServer(("", port), CustomHandler) as httpd:
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[✓] Server gracefully stopped.")


if __name__ == "__main__":
    main()

