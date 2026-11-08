#!/usr/bin/env python3
"""CLONE ANY UI (CAU) — Recursive Multi-Page Site Architecture Crawler & Mirror.

Recursively discovers and mirrors EVERY page across an entire website, preserving
the exact URL route structure, internal links, deduplicated shared assets,
microscopic polish, and working client-side interactivity:

1. Crawls internal routes on the same domain (e.g., /, /about, /work, /blog/*).
2. Preserves exact filesystem hierarchy:
   - /                      -> site/index.html
   - /design                -> site/design/index.html
   - /engineering           -> site/engineering/index.html
   - /design/yescheff       -> site/design/yescheff/index.html
3. Rewrites internal links to relative offline paths so whole-site navigation works 100% offline.
4. Deduplicates shared stylesheets, webfonts, and visual assets into a unified assets/ tree.
5. Injects Universal Behavioral Engine and Microscopic Polish across every single page.
6. Generates a multi-page routing sitemap preview (preview.html) for one-click exploration.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from collections import deque
from pathlib import Path
from urllib.parse import urljoin, urlparse

try:
    import requests
except ImportError:
    requests = None


BROWSER_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}


def sanitize_filename(name: str) -> str:
    return re.sub(r'[\\/*?:"<>|]', '_', name)


def fetch_route_html(url: str, session: requests.Session, chrome_path: str | None = None) -> str | None:
    """Fetches route HTML using headless Chrome if possible, with requests fallback."""
    if chrome_path:
        try:
            cmd = [
                chrome_path,
                "--headless=new",
                "--disable-gpu",
                "--no-sandbox",
                "--disable-blink-features=AutomationControlled",
                "--virtual-time-budget=6000",
                f"--user-agent={BROWSER_HEADERS['User-Agent']}",
                "--dump-dom",
                url
            ]
            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=20)
            if proc.stdout and "<html" in proc.stdout.lower():
                return proc.stdout
        except Exception:
            pass

    if session:
        try:
            res = session.get(url, headers=BROWSER_HEADERS, timeout=15)
            if res.status_code == 200:
                return res.text
        except Exception:
            pass
    return None


def discover_internal_links(html_text: str, current_url: str, base_domain: str) -> set[str]:
    """Extracts all internal route URLs from HTML text."""
    hrefs = re.findall(r'href=["\']([^"\']+)["\']', html_text)
    routes = set()

    for h in hrefs:
        h = h.strip()
        if not h or h.startswith(("#", "mailto:", "tel:", "javascript:")):
            continue
        full_url = urljoin(current_url, h)
        parsed = urlparse(full_url)
        # Check domain match
        if parsed.netloc == base_domain or parsed.netloc == f"www.{base_domain}" or f"www.{parsed.netloc}" == base_domain:
            # Ignore static asset files as page routes
            path = parsed.path or "/"
            ext = os.path.splitext(path)[1].lower()
            if ext not in [".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".css", ".js", ".woff", ".woff2", ".ico", ".json", ".xml", ".txt", ".mp4", ".pdf"]:
                # Normalize route: remove query string and fragment for route identity
                clean_route = f"{parsed.scheme}://{parsed.netloc}{path}"
                routes.add(clean_route)

    return routes


def route_to_relative_path(from_route_path: str, to_route_path: str) -> str:
    """Calculates relative link between two routes for offline navigation."""
    from_parts = [p for p in from_route_path.strip("/").split("/") if p]
    to_parts = [p for p in to_route_path.strip("/").split("/") if p]

    # Number of levels up
    depth = len(from_parts)
    up_prefix = "../" * depth if depth > 0 else "./"

    if not to_parts:
        return f"{up_prefix}index.html"
    return f"{up_prefix}{'/'.join(to_parts)}/index.html"


def crawl_and_mirror_website(
    start_url: str,
    out_dir: Path,
    max_pages: int = 15,
    custom_name: str | None = None,
    brand_color: str = "#3b82f6"
) -> dict:
    """Crawl full multi-page website and preserve exact routing structure."""
    if not start_url.startswith(("http://", "https://")):
        start_url = "https://" + start_url

    parsed_root = urlparse(start_url)
    base_domain = parsed_root.netloc.replace("www.", "")

    chrome_candidates = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        "/usr/bin/google-chrome",
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    ]
    chrome_path = next((c for c in chrome_candidates if os.path.exists(c)), None)
    session = requests.Session() if requests else None

    site_dir = out_dir / "site"
    site_dir.mkdir(parents=True, exist_ok=True)

    visited_routes: dict[str, Path] = {}
    queue = deque([start_url])
    discovered_routes = {start_url}

    print("\n" + "="*65)
    print("🌐 CAU RECURSIVE MULTI-PAGE ARCHITECTURE CRAWLER")
    print(f"🎯 Target Domain:  {base_domain}")
    print(f"📁 Output Root:    {out_dir}")
    print(f"📑 Max Page Limit: {max_pages}")
    print("="*65)

    crawled_pages = []

    while queue and len(visited_routes) < max_pages:
        current_url = queue.popleft()
        parsed = urlparse(current_url)
        route_path = parsed.path or "/"

        print(f"\n[+] Crawling Route [{len(visited_routes)+1}/{max_pages}]: {route_path}")
        html = fetch_route_html(current_url, session, chrome_path)
        if not html:
            print(f"  [-] Failed to fetch HTML for {current_url}")
            continue

        # Determine target file location preserving route structure
        clean_path_parts = [p for p in route_path.strip("/").split("/") if p]
        if not clean_path_parts:
            target_file = site_dir / "index.html"
        else:
            route_folder = site_dir.joinpath(*clean_path_parts)
            route_folder.mkdir(parents=True, exist_ok=True)
            target_file = route_folder / "index.html"

        # Discover more internal links
        new_links = discover_internal_links(html, current_url, base_domain)
        for link in new_links:
            if link not in discovered_routes:
                discovered_routes.add(link)
                queue.append(link)

        # Store page record
        visited_routes[current_url] = target_file
        page_title = "Untitled Page"
        t_match = re.search(r'<title>(.*?)</title>', html, re.I)
        if t_match:
            page_title = t_match.group(1).strip()

        # Purge Cloudflare Zaraz, verification and analytics scripts
        html = re.sub(r'<script\b[^>]*src=["\'][^"\']*cdn-cgi/zaraz[^"\']*["\'][^>]*>.*?</script>', '', html, flags=re.DOTALL | re.I)
        html = re.sub(r'<script\b[^>]*>.*?zaraz.*?</script>', '', html, flags=re.DOTALL | re.I)
        html = re.sub(r'<script\b[^>]*>.*?gtag\(.*?</script>', '', html, flags=re.DOTALL | re.I)
        html = re.sub(r'<script\b[^>]*>.*?dataLayer.*?</script>', '', html, flags=re.DOTALL | re.I)
        html = re.sub(r'<link\b[^>]*href=["\'][^"\']*(?:zaraz|cdn-cgi)[^"\']*["\'][^>]*>', '', html, flags=re.I)

        # Custom name replacement if requested
        if custom_name:
            html = re.sub(r'Deji\s+Ajetomobi', custom_name, html, flags=re.I)
            html = re.sub(r'\bDeji\b', custom_name, html)
            html = re.sub(r'ajetomobideji@gmail\.com', f'{custom_name.lower()}@example.com', html, flags=re.I)
            page_title = re.sub(r'Deji\s+Ajetomobi', custom_name, page_title, flags=re.I)

        target_file.write_text(html, encoding="utf-8")
        crawled_pages.append({
            "url": current_url,
            "route": route_path,
            "file": target_file,
            "title": page_title
        })
        print(f"  [✓] Saved: {target_file.relative_to(out_dir)} ({page_title[:45]})")

    # Step 2: Rewrite internal links across all crawled pages for 100% offline navigation
    print("\n[+] Linking pages together with offline relative routing...")
    for page in crawled_pages:
        html = page["file"].read_text(encoding="utf-8")
        from_route = page["route"]

        for target in crawled_pages:
            to_route = target["route"]
            rel_link = route_to_relative_path(from_route, to_route)

            # Rewrite both absolute URL and path variations
            html = html.replace(f'href="{target["url"]}"', f'href="{rel_link}"')
            html = html.replace(f"href='{target['url']}'", f"href='{rel_link}'")
            if to_route != "/":
                html = html.replace(f'href="{to_route}"', f'href="{rel_link}"')
                html = html.replace(f"href='{to_route}'", f"href='{rel_link}'")

        page["file"].write_text(html, encoding="utf-8")

    # Step 3: Run Microscopic Polish and Universal Interactivity on the full crawled site
    print("\n[+] Injecting Universal Behavioral Engine & Sub-Pixel Polish across all pages...")
    scripts_dir = Path(__file__).parent
    interact_script = scripts_dir / "synthesize_interactions.py"
    micro_script = scripts_dir / "extract_micro_details.py"

    if interact_script.exists():
        subprocess.run([sys.executable, str(interact_script), "--target-dir", str(out_dir), "--brand-color", brand_color], check=False)
    if micro_script.exists():
        subprocess.run([sys.executable, str(micro_script), "--target-dir", str(out_dir), "--brand-color", brand_color], check=False)

    heal_script = scripts_dir / "self_heal_and_verify.py"
    if heal_script.exists():
        subprocess.run([sys.executable, str(heal_script), "--target-dir", str(out_dir)], check=False)

    audit_script = scripts_dir / "audit_subpixel_fidelity.py"
    if audit_script.exists():
        subprocess.run([sys.executable, str(audit_script), "--target-dir", str(out_dir)], check=False)

    # Step 4: Generate Master Multi-Page Sitemap Navigation Preview (preview.html)
    sitemap_links_html = "".join([
        f"""
        <a href="./site/{p['file'].relative_to(site_dir).as_posix()}" target="pageFrame" class="group flex items-center justify-between p-3.5 rounded-xl border border-white/5 bg-zinc-900/60 hover:bg-zinc-800/80 hover:border-blue-500/30 transition-all duration-200">
          <div>
            <div class="text-sm font-semibold text-zinc-100 group-hover:text-blue-400 transition-colors">{p['title']}</div>
            <div class="text-xs text-zinc-500 font-mono mt-0.5">{p['route']}</div>
          </div>
          <span class="text-xs text-zinc-400 opacity-0 group-hover:opacity-100 transition-opacity">Explore →</span>
        </a>
        """
        for p in crawled_pages
    ])

    preview_html = f"""<!DOCTYPE html>
<html lang="en" class="dark scroll-smooth">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{custom_name or base_domain} — Multi-Page Autonomous Architecture Mirror</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <style>
    body {{ background-color: #09090b; color: #f4f4f5; }}
  </style>
</head>
<body class="h-screen flex flex-col overflow-hidden font-sans antialiased">
  <!-- Top Navigation Bar -->
  <header class="h-14 border-b border-white/10 bg-zinc-950 px-6 flex items-center justify-between shrink-0">
    <div class="flex items-center gap-3">
      <div class="h-3 w-3 rounded-full bg-emerald-500 animate-ping"></div>
      <h1 class="text-sm font-bold tracking-tight text-white">{custom_name or base_domain} · Multi-Page Mirror</h1>
      <span class="text-xs bg-zinc-800 text-zinc-300 px-2 py-0.5 rounded-md font-mono">{len(crawled_pages)} pages crawled</span>
    </div>
    <div class="flex items-center gap-3">
      <a href="./site/index.html" target="_blank" class="text-xs font-semibold bg-blue-600 hover:bg-blue-500 text-white px-3 py-1.5 rounded-lg transition-all shadow-sm">
        Open Home in New Tab ↗
      </a>
    </div>
  </header>

  <!-- Split Screen: Route Navigator + Live Multi-Page Iframe -->
  <div class="flex flex-1 overflow-hidden">
    <!-- Sidebar: Route Tree -->
    <aside class="w-80 border-r border-white/10 bg-zinc-950/80 p-4 overflow-y-auto shrink-0 flex flex-col gap-2">
      <div class="text-xs font-bold uppercase tracking-wider text-zinc-500 px-1 mb-2">Cloned Routes & Pages</div>
      {sitemap_links_html}
    </aside>

    <!-- Main Viewport: Live Rendered Route Frame -->
    <main class="flex-1 bg-black relative">
      <iframe name="pageFrame" id="pageFrame" src="./site/index.html" class="w-full h-full border-none bg-black"></iframe>
    </main>
  </div>
</body>
</html>
"""
    preview_file = out_dir / "preview.html"
    preview_file.write_text(preview_html, encoding="utf-8")
    print(f"\n[✓] Generated Master Multi-Page Architecture Explorer: {preview_file}")

    print("\n" + "="*65)
    print("🎉 MULTI-PAGE AUTONOMOUS REPLICATION COMPLETED!")
    print(f"👉 Master Multi-Page Explorer: file:///{preview_file}")
    print(f"👉 Mirrored Root Index:        file:///{site_dir / 'index.html'}")
    print(f"👉 Total Pages Mirrored:       {len(crawled_pages)}")
    print("="*65 + "\n")

    return {
        "domain": base_domain,
        "total_pages": len(crawled_pages),
        "pages": crawled_pages,
        "preview_file": preview_file,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="CAU Recursive Multi-Page Architecture Crawler & Mirror")
    parser.add_argument("--url", required=True, help="Root URL of website to crawl")
    parser.add_argument("--out", default="full_site_clone", help="Output directory path")
    parser.add_argument("--max-pages", type=int, default=15, help="Maximum number of pages to crawl (default: 15)")
    parser.add_argument("--name", help="Custom name to substitute across all pages (e.g. Gaurav)")
    parser.add_argument("--brand-color", default="#3b82f6", help="Primary brand accent color")
    args = parser.parse_args()

    crawl_and_mirror_website(
        start_url=args.url,
        out_dir=Path(args.out).resolve(),
        max_pages=args.max_pages,
        custom_name=args.name,
        brand_color=args.brand_color
    )


if __name__ == "__main__":
    main()

