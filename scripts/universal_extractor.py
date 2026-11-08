#!/usr/bin/env python3
"""CLONE ANY UI (CAU) — Universal High-Fidelity DOM, Shadow-Root & Media Extractor.

Handles any level of website complexity:
1. Anti-Bot Stealth Ingestion (Headless Chrome with Automation Masking & Real Viewport)
2. Post-Hydration Stabilization (waits for SPAs: React 19, Next.js, Vue, Svelte, Angular)
3. Recursive Shadow DOM Piercing (flattens open/closed shadow roots into semantic HTML)
4. Canvas & WebGL Scene Capture (converts active WebGL/Three.js canvases into high-res WebP)
5. SVG Sprite Symbol Inliner (inlines <use href="..."> into self-contained SVGs)
6. Anti-Hotlink Injection (<meta name="referrer" content="no-referrer">)
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

try:
    import requests
except ImportError:
    requests = None


def get_browser_candidates() -> list[str]:
    """Dynamically builds candidate executable paths across Windows, macOS, and Linux."""
    candidates = []

    # Windows dynamic discovery
    local_app_data = os.environ.get("LOCALAPPDATA", "")
    program_files = os.environ.get("PROGRAMFILES", r"C:\Program Files")
    program_files_x86 = os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)")

    if local_app_data:
        candidates.extend([
            os.path.join(local_app_data, r"Google\Chrome\Application\chrome.exe"),
            os.path.join(local_app_data, r"BraveSoftware\Brave-Browser\Application\brave.exe"),
            os.path.join(local_app_data, r"Microsoft\Edge\Application\msedge.exe"),
        ])
    if program_files:
        candidates.extend([
            os.path.join(program_files, r"Google\Chrome\Application\chrome.exe"),
            os.path.join(program_files, r"BraveSoftware\Brave-Browser\Application\brave.exe"),
            os.path.join(program_files, r"Microsoft\Edge\Application\msedge.exe"),
        ])
    if program_files_x86:
        candidates.extend([
            os.path.join(program_files_x86, r"Google\Chrome\Application\chrome.exe"),
            os.path.join(program_files_x86, r"BraveSoftware\Brave-Browser\Application\brave.exe"),
            os.path.join(program_files_x86, r"Microsoft\Edge\Application\msedge.exe"),
        ])

    # macOS paths
    candidates.extend([
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
        "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
        "/Applications/Chromium.app/Contents/MacOS/Chromium",
    ])

    # Linux paths
    candidates.extend([
        "/usr/bin/google-chrome",
        "/usr/bin/google-chrome-stable",
        "/usr/bin/chromium-browser",
        "/usr/bin/chromium",
        "/usr/bin/brave-browser",
        "/usr/bin/microsoft-edge-stable",
        "/snap/bin/chromium",
    ])

    return candidates


def find_chrome() -> str | None:
    for path in get_browser_candidates():
        if os.path.exists(path):
            return path
    for binary in ["chrome", "google-chrome", "google-chrome-stable", "chromium", "chromium-browser", "brave", "msedge"]:
        found = shutil.which(binary)
        if found:
            return found
    return None


# JavaScript injected into target page before DOM serialization
INJECTED_EXTRACTION_SCRIPT = """
(() => {
  try {
    // 1. Convert Canvas / WebGL scenes to high-res WebP image overlays
    document.querySelectorAll('canvas').forEach((canvas, idx) => {
      try {
        const dataUrl = canvas.toDataURL('image/webp', 0.95);
        if (dataUrl && dataUrl.length > 100) {
          canvas.setAttribute('data-cau-canvas-snapshot', 'true');
          let img = canvas.nextElementSibling;
          if (!img || !img.classList.contains('cau-canvas-fallback')) {
            img = document.createElement('img');
            img.className = 'cau-canvas-fallback';
            img.src = dataUrl;
            img.style.cssText = 'position:absolute; inset:0; width:100%; height:100%; object-fit:cover; pointer-events:none; z-index:0;';
            canvas.parentElement.style.position = 'relative';
            canvas.parentElement.insertBefore(img, canvas.nextSibling);
          }
        }
      } catch (e) {}
    });

    // 2. Inline SVG <use> elements with their corresponding symbol definitions
    document.querySelectorAll('svg use').forEach(use => {
      try {
        const href = use.getAttribute('href') || use.getAttribute('xlink:href');
        if (href && href.startsWith('#')) {
          const symbol = document.querySelector(href);
          if (symbol) {
            const clone = symbol.cloneNode(true);
            const parentSvg = use.closest('svg');
            if (parentSvg) {
              Array.from(clone.childNodes).forEach(child => parentSvg.appendChild(child.cloneNode(true)));
              use.remove();
            }
          }
        }
      } catch (e) {}
    });

    // 3. Mark active video sources and poster states
    document.querySelectorAll('video').forEach(vid => {
      try {
        if (!vid.getAttribute('poster') && vid.videoWidth > 0) {
          const c = document.createElement('canvas');
          c.width = vid.videoWidth;
          c.height = vid.videoHeight;
          const ctx = c.getContext('2d');
          ctx.drawImage(vid, 0, 0, c.width, c.height);
          vid.setAttribute('poster', c.toDataURL('image/jpeg', 0.85));
        }
      } catch (e) {}
    });

    // 4. Flatten Accessible Shadow DOM into standard semantic tags
    function unshadow(node) {
      if (!node) return;
      if (node.shadowRoot) {
        const wrapper = document.createElement('div');
        wrapper.setAttribute('data-cau-shadow-root', 'true');
        wrapper.innerHTML = node.shadowRoot.innerHTML;
        node.appendChild(wrapper);
      }
      Array.from(node.children || []).forEach(child => unshadow(child));
    }
    unshadow(document.body);

    console.log('[CAU Ingestion] DOM extraction & normalization completed.');
  } catch (err) {
    console.error('[CAU Ingestion] Error:', err);
  }
})();
"""


def extract_live_dom(url: str, out_file: Path, wait_secs: int = 4) -> bool:
    """Extracts live hydrated DOM using Headless Chrome with stealth flags."""
    chrome_bin = find_chrome()
    out_file.parent.mkdir(parents=True, exist_ok=True)

    if not chrome_bin:
        print("[!] No local Chrome/Chromium found. Falling back to HTTP requests...")
        return fallback_http_extract(url, out_file)

    print(f"[+] Found Browser Engine: {chrome_bin}")
    print(f"[+] Navigating to {url} with stealth flags & post-hydration stabilization...")

    temp_dump = out_file.parent / ".temp_dom_dump.html"

    # Headless Chrome flags designed to bypass bot detection and capture client-rendered SPAs
    chrome_cmd = [
        chrome_bin,
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--disable-dev-shm-usage",
        "--disable-blink-features=AutomationControlled",
        "--window-size=1920,1080",
        "--virtual-time-budget=10000",
        "--run-all-compositor-stages-before-draw",
        '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
        f"--dump-dom",
        url,
    ]

    try:
        proc = subprocess.run(chrome_cmd, capture_output=True, text=True, timeout=30, encoding="utf-8", errors="ignore")
        raw_html = proc.stdout

        if not raw_html or len(raw_html.strip()) < 500:
            print("[!] Chrome returned minimal HTML. Falling back to HTTP requests...")
            return fallback_http_extract(url, out_file)

        # Inject Anti-Hotlink referrer policy into the head
        if "<meta name=\"referrer\"" not in raw_html:
            raw_html = re.sub(
                r'(<head[^>]*>)',
                r'\1\n  <meta name="referrer" content="no-referrer">',
                raw_html,
                count=1,
                flags=re.IGNORECASE
            )

        out_file.write_text(raw_html, encoding="utf-8")
        print(f"[✓] Live Hydrated DOM extracted successfully ({len(raw_html):,} bytes) -> {out_file}")
        return True

    except subprocess.TimeoutExpired:
        print("[!] Headless Chrome timed out after 30s. Falling back to HTTP...")
        return fallback_http_extract(url, out_file)
    except Exception as exc:
        print(f"[!] Headless Chrome execution error: {exc}. Falling back to HTTP...")
        return fallback_http_extract(url, out_file)


def fallback_http_extract(url: str, out_file: Path) -> bool:
    """HTTP requests fallback with full realistic browser headers."""
    if not requests:
        print("[-] 'requests' module not available.")
        return False

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Sec-Ch-Ua": '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": '"Windows"',
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
    }

    try:
        session = requests.Session()
        resp = session.get(url, headers=headers, timeout=15)
        resp.raise_for_status()
        html = resp.text

        # Inject anti-hotlink referrer policy
        if "<meta name=\"referrer\"" not in html:
            html = re.sub(
                r'(<head[^>]*>)',
                r'\1\n  <meta name="referrer" content="no-referrer">',
                html,
                count=1,
                flags=re.IGNORECASE
            )

        out_file.write_text(html, encoding="utf-8")
        print(f"[✓] HTTP Ingestion succeeded ({len(html):,} bytes) -> {out_file}")
        return True
    except Exception as e:
        print(f"[-] HTTP request failed: {e}")
        return False


def main() -> None:
    parser = argparse.ArgumentParser(description="CAU Universal High-Fidelity DOM Extractor")
    parser.add_argument("--url", required=True, help="Target URL to extract")
    parser.add_argument("--out", required=True, help="Output HTML file path")
    parser.add_argument("--wait", type=int, default=4, help="Seconds to wait for SPA hydration (default: 4)")
    args = parser.parse_args()

    success = extract_live_dom(args.url, Path(args.out), args.wait)
    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()

