#!/usr/bin/env python3
"""Design System & Token Extractor for Web UI Replication.

Extracts colors, typography, spacing, border-radii, box-shadows, and CSS variables
from local HTML/CSS files or live URLs, generating:
1. tokens.json (Structured design tokens)
2. tailwind.config.js (Tailwind theme.extend snippet)
3. tokens.css (CSS custom properties)

Usage:
  python extract_design_tokens.py --file path/to/style.css --out ./extracted
  python extract_design_tokens.py --file path/to/index.html --out ./extracted
  python extract_design_tokens.py --url https://example.com --out ./extracted
"""

from __future__ import annotations

import argparse
import json
import math
import os
import re
import sys
from collections import Counter
from pathlib import Path
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen

# Support importing local motion extraction engine
try:
    from extract_motion_physics import (
        extract_motion_tokens,
        generate_tailwind_motion_config,
        generate_motion_css,
    )
except ImportError:
    try:
        from scripts.extract_motion_physics import (
            extract_motion_tokens,
            generate_tailwind_motion_config,
            generate_motion_css,
        )
    except ImportError:
        extract_motion_tokens = None
        generate_tailwind_motion_config = None
        generate_motion_css = None

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0 Safari/537.36"

# Color regex patterns
HEX_RE = re.compile(r"#(?:[0-9a-fA-F]{3,4}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8})\b")
RGB_RE = re.compile(r"rgba?\(\s*[\d.]+%?\s*,\s*[\d.]+%?\s*,\s*[\d.]+%?(?:\s*,\s*[\d.]+%?)?\s*\)", re.I)
HSL_RE = re.compile(r"hsla?\(\s*[\d.]+(?:deg|rad|turn)?\s*,\s*[\d.]+%?\s*,\s*[\d.]+%?(?:\s*,\s*[\d.]+%?)?\s*\)", re.I)
OKLCH_RE = re.compile(r"oklch\([^)]+\)", re.I)

# CSS Custom Properties regex
CSS_VAR_RE = re.compile(r"(--[a-zA-Z0-9_-]+)\s*:\s*([^;!}\n]+)")

# Typography and styling regex
FONT_FAMILY_RE = re.compile(r"font-family\s*:\s*([^;!}]+)", re.I)
FONT_SIZE_RE = re.compile(r"font-size\s*:\s*([^;!}]+)", re.I)
FONT_WEIGHT_RE = re.compile(r"font-weight\s*:\s*([^;!}]+)", re.I)
LINE_HEIGHT_RE = re.compile(r"line-height\s*:\s*([^;!}]+)", re.I)
BORDER_RADIUS_RE = re.compile(r"border-radius\s*:\s*([^;!}]+)", re.I)
BOX_SHADOW_RE = re.compile(r"box-shadow\s*:\s*([^;!}]+)", re.I)


def fetch_url(url: str, timeout: int = 15) -> str:
    req = Request(url, headers={"User-Agent": USER_AGENT})
    with urlopen(req, timeout=timeout) as res:
        charset = res.headers.get_content_charset() or "utf-8"
        return res.read().decode(charset, errors="replace")


def parse_hex_color(hex_str: str) -> tuple[int, int, int] | None:
    s = hex_str.lstrip("#")
    if len(s) == 3:
        return int(s[0] * 2, 16), int(s[1] * 2, 16), int(s[2] * 2, 16)
    if len(s) == 6 or len(s) == 8:
        return int(s[0:2], 16), int(s[2:4], 16), int(s[4:6], 16)
    return None


def calculate_luminance(r: int, g: int, b: int) -> float:
    # Standard relative luminance formula (WCAG)
    def channel(c: float) -> float:
        c /= 255.0
        return c / 12.92 if c <= 0.03928 else math.pow((c + 0.055) / 1.055, 2.4)
    return 0.2126 * channel(r) + 0.7152 * channel(g) + 0.0722 * channel(b)


def categorize_color(hex_color: str) -> str:
    rgb = parse_hex_color(hex_color)
    if not rgb:
        return "other"
    r, g, b = rgb
    lum = calculate_luminance(r, g, b)
    max_c = max(r, g, b)
    min_c = min(r, g, b)
    saturation = (max_c - min_c) / max_c if max_c > 0 else 0

    if lum > 0.95:
        return "background-light"
    if lum < 0.05:
        return "text-dark"
    if saturation < 0.12:
        return "neutral"
    if saturation >= 0.12:
        return "accent"
    return "other"


def clean_prop(value: str) -> str:
    return value.strip().strip("'\"").strip()


def clean_font_family(val: str) -> str:
    parts = [p.strip().strip("'\"") for p in val.split(",") if p.strip()]
    return ", ".join(parts)


def extract_tokens_from_css(css_text: str) -> dict:
    # 1. CSS Variables
    css_vars = {}
    for match in CSS_VAR_RE.finditer(css_text):
        var_name = match.group(1).strip()
        var_val = match.group(2).strip()
        css_vars[var_name] = var_val

    # 2. Colors
    hex_colors = [c.lower() for c in HEX_RE.findall(css_text)]
    rgb_colors = [c.lower() for c in RGB_RE.findall(css_text)]
    hsl_colors = [c.lower() for c in HSL_RE.findall(css_text)]
    oklch_colors = [c.lower() for c in OKLCH_RE.findall(css_text)]

    color_counter = Counter(hex_colors)
    categorized_colors: dict[str, list[dict]] = {
        "accent": [],
        "neutral": [],
        "text-dark": [],
        "background-light": [],
        "other": []
    }

    for color, count in color_counter.most_common(50):
        cat = categorize_color(color)
        categorized_colors[cat].append({"value": color, "occurrences": count})

    # 3. Typography
    font_families = Counter([clean_font_family(f) for f in FONT_FAMILY_RE.findall(css_text) if f.strip()])
    font_sizes = Counter([clean_prop(s) for s in FONT_SIZE_RE.findall(css_text)])
    font_weights = Counter([clean_prop(w) for w in FONT_WEIGHT_RE.findall(css_text)])
    line_heights = Counter([clean_prop(l) for l in LINE_HEIGHT_RE.findall(css_text)])

    # 4. Radii & Shadows
    radii = Counter([clean_prop(r) for r in BORDER_RADIUS_RE.findall(css_text)])
    shadows = Counter([clean_prop(s) for s in BOX_SHADOW_RE.findall(css_text) if s.lower() != "none"])

    # 5. Motion, Animations & Easings
    motion_tokens = {}
    if extract_motion_tokens:
        try:
            motion_tokens = extract_motion_tokens(css_text)
        except Exception:
            pass

    return {
        "cssVariables": css_vars,
        "colors": {
            "summary": {
                "hex": dict(color_counter.most_common(25)),
                "rgb": dict(Counter(rgb_colors).most_common(15)),
                "hsl": dict(Counter(hsl_colors).most_common(10)),
                "oklch": dict(Counter(oklch_colors).most_common(10)),
            },
            "byRole": categorized_colors,
        },
        "typography": {
            "fontFamilies": [f for f, _ in font_families.most_common(8)],
            "fontSizes": [s for s, _ in font_sizes.most_common(12)],
            "fontWeights": [w for w, _ in font_weights.most_common(8)],
            "lineHeights": [l for l, _ in line_heights.most_common(8)],
        },
        "shape": {
            "borderRadii": [r for r, _ in radii.most_common(8)],
            "boxShadows": [s for s, _ in shadows.most_common(6)],
        },
        "motion": motion_tokens,
    }


def generate_tailwind_config(tokens: dict) -> str:
    colors = tokens["colors"]["byRole"]
    primary = colors["accent"][0]["value"] if colors["accent"] else "#3b82f6"
    secondary = colors["accent"][1]["value"] if len(colors["accent"]) > 1 else "#6366f1"
    neutral = colors["neutral"][0]["value"] if colors["neutral"] else "#71717a"
    dark = colors["text-dark"][0]["value"] if colors["text-dark"] else "#09090b"
    light = colors["background-light"][0]["value"] if colors["background-light"] else "#fafafa"

    fonts = tokens["typography"]["fontFamilies"]
    sans_font = fonts[0] if fonts else "Inter, system-ui, sans-serif"

    radii = tokens["shape"]["borderRadii"]
    shadows = tokens["shape"]["boxShadows"]

    motion = tokens.get("motion", {})
    keyframes = motion.get("keyframes", {})
    animations = motion.get("animations", {})
    easings = motion.get("easings", {})

    config = f"""/** @type {{import('tailwindcss').Config}} */
module.exports = {{
  theme: {{
    extend: {{
      colors: {{
        brand: {{
          primary: '{primary}',
          secondary: '{secondary}',
          muted: '{neutral}',
          surface: '{light}',
          foreground: '{dark}',
        }},
      }},
      fontFamily: {{
        sans: [{', '.join(repr(p.strip().strip("'\"")) for p in sans_font.split(','))}],
      }},
      borderRadius: {{
"""
    for i, r in enumerate(radii[:4]):
        name = ["sm", "md", "lg", "xl"][i]
        config += f"        'custom-{name}': '{r}',\n"

    config += "      },\n      boxShadow: {\n"
    for i, s in enumerate(shadows[:3]):
        name = ["card", "elevated", "hover"][i]
        config += f"        'custom-{name}': '{s}',\n"

    config += "      },\n"

    # Inject Motion Tokens into Tailwind Config
    if keyframes:
        config += "      keyframes: {\n"
        for k_name, steps in list(keyframes.items())[:12]:
            config += f"        '{k_name}': {{\n"
            for step_key, decls in steps.items():
                config += f"          '{step_key}': {json.dumps(decls)},\n"
            config += "        },\n"
        config += "      },\n"

    if animations:
        config += "      animation: {\n"
        for a_name, a_rule in list(animations.items())[:12]:
            config += f"        '{a_name}': '{a_rule}',\n"
        config += "      },\n"

    if easings:
        config += "      transitionTimingFunction: {\n"
        for e_name, e_curve in list(easings.items())[:6]:
            config += f"        '{e_name}': '{e_curve}',\n"
        config += "      },\n"

    config += """    },
  },
  plugins: [],
};
"""
    return config


def generate_tailwind_v4_theme(tokens: dict) -> str:
    lines = ["@theme {", "  /* Tailwind v4 CSS-First Theme Configuration */"]
    accents = tokens["colors"]["byRole"]["accent"]
    for i, col in enumerate(accents[:5]):
        lines.append(f"  --color-brand-{i+1}: {col['value']};")

    neutrals = tokens["colors"]["byRole"]["neutral"]
    for i, col in enumerate(neutrals[:5]):
        lines.append(f"  --color-neutral-{i+1}: {col['value']};")

    if tokens["typography"]["fontFamilies"]:
        clean_font = tokens["typography"]["fontFamilies"][0].split(",")[0].strip().strip("'\"")
        lines.append(f"  --font-sans: '{clean_font}', system-ui, sans-serif;")

    for i, r in enumerate(tokens["shape"]["borderRadii"][:4]):
        name = ["sm", "md", "lg", "xl"][i]
        lines.append(f"  --radius-custom-{name}: {r};")

    # Tailwind v4 Motion Directives
    motion = tokens.get("motion", {})
    for e_name, e_curve in list(motion.get("easings", {}).items())[:4]:
        lines.append(f"  --ease-{e_name}: {e_curve};")

    for a_name, a_rule in list(motion.get("animations", {}).items())[:6]:
        lines.append(f"  --animate-{a_name}: {a_rule};")

    lines.append("}\n")
    return "\n".join(lines)


def generate_css_variables(tokens: dict) -> str:
    lines = [":root {"]
    # Re-export discovered CSS variables
    if tokens["cssVariables"]:
        lines.append("  /* Original CSS Custom Properties */")
        for k, v in list(tokens["cssVariables"].items())[:40]:
            lines.append(f"  {k}: {v};")

    lines.append("\n  /* Synthesized Design Tokens */")
    accents = tokens["colors"]["byRole"]["accent"]
    for i, col in enumerate(accents[:5]):
        lines.append(f"  --color-brand-{i+1}: {col['value']};")

    neutrals = tokens["colors"]["byRole"]["neutral"]
    for i, col in enumerate(neutrals[:5]):
        lines.append(f"  --color-neutral-{i+1}: {col['value']};")

    if tokens["typography"]["fontFamilies"]:
        lines.append(f"  --font-primary: {tokens['typography']['fontFamilies'][0]};")

    motion = tokens.get("motion", {})
    if motion.get("easings"):
        lines.append("\n  /* Motion & Spring Physics */")
        for e_name, e_curve in list(motion.get("easings", {}).items())[:4]:
            lines.append(f"  --ease-{e_name}: {e_curve};")
        lines.append("  --duration-normal: 300ms;")
        lines.append("  --duration-fast: 150ms;")

    lines.append("}\n")

    # Append @keyframes directly to tokens.css
    keyframes = motion.get("keyframes", {})
    if keyframes:
        lines.append("/* --- Extracted & Baseline Keyframes --- */")
        for k_name, steps in list(keyframes.items())[:8]:
            lines.append(f"@keyframes {k_name} {{")
            for step_key, decls in steps.items():
                lines.append(f"  {step_key} {{")
                for prop, val in decls.items():
                    lines.append(f"    {prop}: {val};")
                lines.append("  }")
            lines.append("}\n")

    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract design tokens from HTML, CSS, or live URL.")
    parser.add_argument("--file", help="Path to local CSS or HTML file")
    parser.add_argument("--url", help="URL of live webpage")
    parser.add_argument("--out", default="tokens_output", help="Directory to save extracted tokens")
    args = parser.parse_args()

    content = ""
    if args.url:
        print(f"[+] Fetching live page from {args.url}...")
        try:
            content = fetch_url(args.url)
        except Exception as e:
            sys.exit(f"[-] Failed to fetch URL: {e}")
    elif args.file:
        file_path = Path(args.file)
        if not file_path.exists():
            sys.exit(f"[-] File not found: {args.file}")
        content = file_path.read_text(encoding="utf-8", errors="replace")
    else:
        sys.exit("[-] Error: Please specify either --file or --url.")

    print("[+] Extracting tokens (colors, typography, radii, shadows, variables)...")
    tokens = extract_tokens_from_css(content)

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    # 1. Save tokens.json
    tokens_json_path = out_dir / "tokens.json"
    tokens_json_path.write_text(json.dumps(tokens, indent=2), encoding="utf-8")
    print(f"[✓] Saved JSON tokens to: {tokens_json_path}")

    # 2. Save tailwind.config.js
    tailwind_path = out_dir / "tailwind.config.js"
    tailwind_path.write_text(generate_tailwind_config(tokens), encoding="utf-8")
    print(f"[✓] Saved Tailwind config to: {tailwind_path}")

    # 3. Save tokens.css (CSS variables)
    css_path = out_dir / "tokens.css"
    css_path.write_text(generate_css_variables(tokens), encoding="utf-8")
    print(f"[✓] Saved CSS custom properties to: {css_path}")

    # 4. Save theme.v4.css (Tailwind v4 @theme)
    theme_v4_path = out_dir / "theme.v4.css"
    theme_v4_path.write_text(generate_tailwind_v4_theme(tokens), encoding="utf-8")
    print(f"[✓] Saved Tailwind v4 @theme config to: {theme_v4_path}")

    print("\n[★] Token extraction completed successfully!")


if __name__ == "__main__":
    main()
