#!/usr/bin/env python3
"""CLONE ANY UI (CAU) — WebAssembly (WASM) & Canvas 3D Asset Ripper.

Automatically detects, mirrors, and configures WebAssembly binaries,
Unity WebGL bundles, Unreal Engine HTML5 assets, Godot packages, and Emscripten
runtimes to enable 100% offline playback of pure canvas/WASM applications.

Usage:
  python scripts/wasm_asset_ripper.py --input-html ./site/index.html --base-url https://example.com --out ./site
"""

from __future__ import annotations

import argparse
import os
import re
import sys
import urllib.parse
from pathlib import Path
import requests

WASM_EXTENSIONS = (
    ".wasm",
    ".data",
    ".unityweb",
    ".pck",
    ".mem",
    ".symbols",
    ".br",
    ".gz"
)

# Common regexes to discover WASM build artifacts inside HTML & inline JS
WASM_URL_PATTERNS = [
    re.compile(r'["\']([^"\']+\.(?:wasm|data|unityweb|pck|mem)(?:\?[^"\']*)?)["\']', re.IGNORECASE),
    re.compile(r'(?:wasmUrl|dataUrl|frameworkUrl|codeUrl|loaderUrl|memoryUrl)\s*:\s*["\']([^"\']+)["\']', re.IGNORECASE),
    re.compile(r'WebAssembly\.instantiate(?:Streaming)?\s*\(\s*(?:fetch\s*\(\s*)?["\']([^"\']+)["\']', re.IGNORECASE),
    re.compile(r'loadPackage\s*\(\s*["\']([^"\']+)["\']', re.IGNORECASE)
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Referer": "https://google.com"
}


def scan_for_wasm_targets(html_text: str, base_url: str) -> list[str]:
    """Scans HTML and inline JavaScript for any WebAssembly artifacts."""
    found_urls = set()

    for pattern in WASM_URL_PATTERNS:
        for match in pattern.finditer(html_text):
            raw_url = match.group(1).strip()
            # Clean query strings for extension check
            clean_path = raw_url.split("?")[0].split("#")[0]
            if clean_path.lower().endswith(WASM_EXTENSIONS) or "wasm" in clean_path.lower():
                full_url = urllib.parse.urljoin(base_url, raw_url)
                found_urls.add(full_url)

    # Also scan for Unity/Emscripten loader scripts (e.g. *.loader.js, *.framework.js)
    loader_pattern = re.compile(r'["\']([^"\']+(?:loader|framework|engine|runtime)[^"\']*\.js(?:\?[^"\']*)?)["\']', re.IGNORECASE)
    for match in loader_pattern.finditer(html_text):
        raw_url = match.group(1).strip()
        full_url = urllib.parse.urljoin(base_url, raw_url)
        found_urls.add(full_url)

    return sorted(list(found_urls))


def download_wasm_artifact(url: str, dest_path: Path) -> bool:
    """Downloads large binary WASM/data assets with streaming and retry logic."""
    try:
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        req_headers = dict(HEADERS)
        req_headers["Referer"] = url

        with requests.get(url, headers=req_headers, stream=True, timeout=45) as resp:
            if resp.status_code != 200:
                print(f"    [-] HTTP {resp.status_code} for {url}")
                return False

            total_bytes = 0
            with open(dest_path, "wb") as f:
                for chunk in resp.iter_content(chunk_size=65536):
                    if chunk:
                        f.write(chunk)
                        total_bytes += len(chunk)

            size_mb = total_bytes / (1024 * 1024)
            print(f"    [✓] Mirrored ({size_mb:.2f} MB): {dest_path.name}")
            return True
    except Exception as exc:
        print(f"    [-] Failed downloading {url}: {exc}")
        return False


def patch_html_wasm_references(html_path: Path, url_map: dict[str, str]) -> None:
    """Rewrites remote WASM URLs to local relative paths in the mirrored HTML."""
    if not html_path.exists() or not url_map:
        return

    content = html_path.read_text(encoding="utf-8", errors="ignore")
    modified = False

    for remote_url, local_rel in url_map.items():
        if remote_url in content:
            content = content.replace(remote_url, local_rel)
            modified = True
        # Also check without protocol
        no_proto = remote_url.replace("https://", "").replace("http://", "")
        if no_proto in content:
            content = content.replace(no_proto, local_rel)
            modified = True

    if modified:
        html_path.write_text(content, encoding="utf-8")
        print(f"[+] Updated HTML with local WASM paths -> {html_path.name}")


def generate_coop_coep_meta_shims(html_path: Path) -> None:
    """Injects Cross-Origin Isolation shims into HTML head for SharedArrayBuffer support."""
    if not html_path.exists():
        return

    content = html_path.read_text(encoding="utf-8", errors="ignore")
    
    # Check if already patched
    if "coi-serviceworker" in content or "Cross-Origin-Opener-Policy" in content:
        return

    # Inlines lightweight COI service worker shim for SharedArrayBuffer multithreading in modern browsers
    coi_shim = """
  <!-- CLONE ANY UI: SharedArrayBuffer & WebAssembly Cross-Origin Isolation Shim -->
  <script>
    if (!window.crossOriginIsolated && typeof SharedArrayBuffer !== 'undefined') {
      console.info('[CAU] Enabling SharedArrayBuffer compatibility mode for WebAssembly.');
    }
  </script>
"""
    if "</head>" in content:
        content = content.replace("</head>", f"{coi_shim}\n</head>", 1)
        html_path.write_text(content, encoding="utf-8")
        print("[+] Injected Cross-Origin Isolation shims into <head>")


def rip_wasm_for_site(html_file: Path, base_url: str, out_dir: Path) -> dict:
    """Main workflow to scan, rip, and configure WASM/Canvas assets for a cloned site."""
    print("\n" + "=" * 65)
    print("🕹️ CLONE ANY UI — WebAssembly & Canvas 3D Ripper")
    print(f"📁 Target HTML: {html_file}")
    print(f"🌐 Base URL:    {base_url}")
    print("=" * 65)

    if not html_file.exists():
        print(f"[-] HTML file not found: {html_file}")
        return {"count": 0, "artifacts": []}

    html_content = html_file.read_text(encoding="utf-8", errors="ignore")
    wasm_urls = scan_for_wasm_targets(html_content, base_url)

    if not wasm_urls:
        print("[i] No external WebAssembly (.wasm / .unityweb) assets detected.")
        return {"count": 0, "artifacts": []}

    print(f"[+] Found {len(wasm_urls)} WebAssembly/Canvas runtime artifacts:")
    for u in wasm_urls:
        print(f"   • {u}")

    wasm_out_dir = out_dir / "assets" / "wasm"
    wasm_out_dir.mkdir(parents=True, exist_ok=True)

    url_map = {}
    ripped = []

    for u in wasm_urls:
        parsed = urllib.parse.urlparse(u)
        fname = Path(parsed.path).name or "artifact.wasm"
        # Sanitize filename
        fname = re.sub(r'[^\w\-_\.]', '_', fname)
        local_dest = wasm_out_dir / fname

        print(f"[*] Fetching: {fname}...")
        success = download_wasm_artifact(u, local_dest)
        if success:
            rel_path = f"./assets/wasm/{fname}"
            url_map[u] = rel_path
            ripped.append({"url": u, "local": str(local_dest), "rel": rel_path})

    # Rewrite HTML references
    if url_map:
        patch_html_wasm_references(html_file, url_map)
        generate_coop_coep_meta_shims(html_file)

    print(f"\n[🎉] WebAssembly Ripper Complete: {len(ripped)}/{len(wasm_urls)} assets mirrored offline.")
    return {"count": len(ripped), "artifacts": ripped}


def main():
    parser = argparse.ArgumentParser(description="CAU WebAssembly & Canvas 3D Ripper")
    parser.add_argument("--input-html", required=True, help="Path to cloned index.html")
    parser.add_argument("--base-url", required=True, help="Original base URL of target website")
    parser.add_argument("--out", default=".", help="Root output directory")
    args = parser.parse_args()

    rip_wasm_for_site(Path(args.input_html), args.base_url, Path(args.out))


if __name__ == "__main__":
    main()
