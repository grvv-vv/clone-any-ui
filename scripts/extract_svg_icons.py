#!/usr/bin/env python3
"""CLONE ANY UI (CAU) — SVG Icon Extractor & React Component Generator.

Extracts all inline SVGs from a webpage or HTML file and converts them into:
1. Clean standalone .svg files
2. Type-safe React JSX icon components (with currentColor support & custom className)
3. Barrel index.ts export

Usage:
  python extract_svg_icons.py --input ./site/index.html --out ./icons
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


def clean_svg(svg_str: str) -> str:
    # Remove width/height attributes in favor of viewBox + CSS classes
    cleaned = re.sub(r'\s+width=["\']\d+px?["\']', '', svg_str, flags=re.I)
    cleaned = re.sub(r'\s+height=["\']\d+px?["\']', '', cleaned, flags=re.I)
    # Ensure currentColor is used if fill/stroke is fixed
    return cleaned.strip()


def generate_react_icon(name: str, svg_inner: str, viewbox: str) -> str:
    # Convert SVG attributes to camelCase for React JSX
    inner = svg_inner
    replacements = {
        'stroke-width': 'strokeWidth',
        'stroke-linecap': 'strokeLinecap',
        'stroke-linejoin': 'strokeLinejoin',
        'stroke-miterlimit': 'strokeMiterlimit',
        'fill-rule': 'fillRule',
        'clip-rule': 'clipRule',
        'fill-opacity': 'fillOpacity',
        'stroke-opacity': 'strokeOpacity',
        'xmlns:xlink': 'xmlnsXlink',
        'xlink:href': 'xlinkHref',
    }
    for old, new in replacements.items():
        inner = inner.replace(old, new)

    return f"""import React from 'react';

export interface IconProps extends React.SVGProps<SVGSVGElement> {{
  size?: number | string;
}}

export function {name}({{ size = 20, className = '', ...props }}: IconProps) {{
  return (
    <svg
      width={{size}}
      height={{size}}
      viewBox="{viewbox}"
      fill="none"
      stroke="currentColor"
      className={{`inline-block shrink-0 ${{className}}`}}
      {{...props}}
    >
      {inner}
    </svg>
  );
}}
"""


def main() -> None:
    parser = argparse.ArgumentParser(description="CAU — Extract inline SVGs into clean SVG and React icon components.")
    parser.add_argument("--input", required=True, help="Input HTML file path")
    parser.add_argument("--out", default="extracted_icons", help="Output directory for icons")
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        sys.exit(f"[-] Input file not found: {args.input}")

    html_text = input_path.read_text(encoding="utf-8", errors="replace")
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    svg_raw_dir = out_dir / "svg"
    svg_raw_dir.mkdir(parents=True, exist_ok=True)
    react_icons_dir = out_dir / "react"
    react_icons_dir.mkdir(parents=True, exist_ok=True)

    svg_pattern = re.compile(r"<svg\b([^>]*)>(.*?)</svg>", re.DOTALL | re.I)
    matches = list(svg_pattern.finditer(html_text))

    print(f"[+] Found {len(matches)} inline SVG candidates...")

    seen_hashes = set()
    icons_exported = []

    for idx, match in enumerate(matches):
        attrs = match.group(1)
        inner = match.group(2).strip()

        # Deduplicate identical icons
        h = hash(inner)
        if h in seen_hashes:
            continue
        seen_hashes.add(h)

        # Extract viewBox
        viewbox_match = re.search(r'viewBox=["\']([^"\']+)["\']', attrs, re.I)
        viewbox = viewbox_match.group(1) if viewbox_match else "0 0 24 24"

        icon_name = f"Icon_{idx + 1}"
        react_name = f"Icon{idx + 1}"

        # 1. Save raw .svg
        raw_svg_content = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{viewbox}" fill="currentColor">\n  {inner}\n</svg>'
        (svg_raw_dir / f"{icon_name}.svg").write_text(raw_svg_content, encoding="utf-8")

        # 2. Save React .tsx component
        react_code = generate_react_icon(react_name, inner, viewbox)
        (react_icons_dir / f"{react_name}.tsx").write_text(react_code, encoding="utf-8")
        icons_exported.append(react_name)

    # 3. Save index.ts barrel export
    if icons_exported:
        index_ts = "\n".join([f"export {{ {name} }} from './{name}';" for name in icons_exported])
        (react_icons_dir / "index.ts").write_text(index_ts + "\n", encoding="utf-8")

    print(f"[✓] Extracted {len(icons_exported)} unique icons into: {out_dir}")
    print(f"  • Standalone SVGs: {svg_raw_dir}")
    print(f"  • React Icon Components: {react_icons_dir}")


if __name__ == "__main__":
    main()

