#!/usr/bin/env python3
"""CLONE ANY UI (CAU) — Master Microscopic Detail & Sub-Pixel Polish Engine.

Extracts, synthesizes, and enforces sub-pixel microscopic nuances that separate
ordinary clones from flawless, agency-grade design twins:

1. Microscopic Typography & Sub-Pixel Glyphs:
   - OpenType feature settings: tabular numbers ('tnum'), contextual alternates ('cv01'-'cv11'), ligatures ('dlig').
   - Typographic anti-orphan balancing: 'text-wrap: balance' for headings, 'text-wrap: pretty' for body copy.
   - Sub-pixel negative tracking (letter-spacing down to -0.03em) and optical antialiasing.
   - Text underline offsets ('text-underline-offset: 4px; text-decoration-thickness: 1.5px;').

2. Optical Lighting, Shading & Layering:
   - Multi-layer stacked atmospheric shadows (4-to-5 layers with ambient spread).
   - 1px inset hairline borders (box-shadow: inset 0 1px 0 0 rgba(255,255,255,0.12)).
   - Diffuse radial ambient glow meshes and gradient border masking.
   - Optical frosted glassmorphism: backdrop-filter blur(20px) saturate(190%) contrast(90%).

3. Tactile Micro-Physics & State Feedback:
   - Tactile active press compression (scale 0.975 + translateY 0.5px) with spring recovery.
   - Accessible double-offset keyboard focus rings (:focus-visible).
   - Brand text selection styling (::selection and ::-moz-selection).
   - Smooth hover lifts with zero layout thrashing (will-change: transform).

4. Viewport Realism & Platform Parity:
   - Custom ultra-sleek themed scrollbars (purging chunky OS scrollbars).
   - Full iOS/Android safe-area insets: env(safe-area-inset-top/bottom/left/right).
   - Subtle 2.2% organic SVG tactile grain overlay (feTurbulence) for physical surface depth.
   - Full prefers-reduced-motion vestibular safety override.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


def extract_micro_details_from_css(css_text: str, default_brand: str = "#3b82f6") -> dict:
    """Analyzes CSS text to discover microscopic tokens, font features, and multi-layer shadows."""
    details = {
        "font_features": [],
        "letter_spacings": [],
        "stacked_shadows": [],
        "selection_color": default_brand,
        "antialiased": True,
        "text_wrap_balance": True,
        "active_press": True,
        "safe_area_insets": True,
        "glassmorphism": False,
        "hairline_borders": True,
    }

    # Extract font-feature-settings
    ff_matches = re.findall(r'font-feature-settings:\s*([^;]+);', css_text, re.I)
    for m in ff_matches:
        parts = [p.strip().strip("'\"") for p in m.split(",")]
        for p in parts:
            if p and p not in details["font_features"]:
                details["font_features"].append(p)

    # Extract subtle letter-spacings (e.g. -0.02em, -0.5px)
    ls_matches = re.findall(r'letter-spacing:\s*([^;]+);', css_text, re.I)
    for m in ls_matches:
        cleaned = m.strip()
        if cleaned not in details["letter_spacings"]:
            details["letter_spacings"].append(cleaned)

    # Extract multi-layer stacked box shadows
    bs_matches = re.findall(r'box-shadow:\s*([^;]+);', css_text, re.I)
    for m in bs_matches:
        if m.count(',') >= 2 and len(m) > 30:
            cleaned = re.sub(r'\s+', ' ', m.strip())
            if cleaned not in details["stacked_shadows"]:
                details["stacked_shadows"].append(cleaned)

    # Check for glassmorphism
    if "backdrop-filter" in css_text or "-webkit-backdrop-filter" in css_text:
        details["glassmorphism"] = True

    # Extract selection background
    sel_match = re.search(r'::selection\s*\{[^}]*background(?:-color)?:\s*([^;]+);', css_text, re.I)
    if sel_match:
        details["selection_color"] = sel_match.group(1).strip()

    return details


def generate_micro_details_css(details: dict, brand_color: str = "#3b82f6", is_dark: bool = True) -> str:
    """Generates the master microscopic polish stylesheet with sub-pixel typography, shadows, and physics."""
    thumb_bg = "rgba(255, 255, 255, 0.22)" if is_dark else "rgba(0, 0, 0, 0.22)"
    thumb_hover = "rgba(255, 255, 255, 0.42)" if is_dark else "rgba(0, 0, 0, 0.42)"
    hairline_color = "rgba(255, 255, 255, 0.1)" if is_dark else "rgba(0, 0, 0, 0.08)"
    glass_bg = "rgba(18, 18, 18, 0.75)" if is_dark else "rgba(255, 255, 255, 0.75)"
    glass_border = "rgba(255, 255, 255, 0.12)" if is_dark else "rgba(0, 0, 0, 0.08)"

    extracted = [f for f in details.get("font_features", []) if not f.startswith("var(") and not f.startswith("inherit") and not f.startswith("normal")]
    features_list = list(dict.fromkeys(["cv02", "cv03", "cv04", "cv11", "tnum"] + extracted))
    font_features_str = ", ".join([f'"{f}"' for f in features_list])

    return f"""/**
 * CLONE ANY UI (CAU) — Master Microscopic Polish & Sub-Pixel Parity Stylesheet
 * Sub-Pixel Typography · Multi-Layer Shading · Tactile Physics · Platform Parity
 */

/* ==========================================================================
   1. SUB-PIXEL TYPOGRAPHY & OPENTYPE GLYPH REFINEMENT
   ========================================================================== */
html, body {{
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-rendering: optimizeLegibility;
  font-feature-settings: {font_features_str};
}}

/* Balanced Headings & Anti-Orphan Line Wrapping */
h1, h2, h3, h4, h5, h6, .cau-balance {{
  text-wrap: balance;
  letter-spacing: -0.022em;
}}
p, li, blockquote, .cau-pretty {{
  text-wrap: pretty;
}}

/* Optical Text Link Underlines */
a:not([class*="no-underline"]) {{
  text-underline-offset: 3.5px;
  text-decoration-thickness: 1.5px;
}}

/* ==========================================================================
   2. BRAND-MATCHED SELECTION & SLEEK SCROLLBARS
   ========================================================================== */
::selection {{
  background-color: {brand_color} !important;
  color: #000000 !important;
}}
::-moz-selection {{
  background-color: {brand_color} !important;
  color: #000000 !important;
}}

* {{
  scrollbar-width: thin;
  scrollbar-color: {thumb_bg} transparent;
}}
::-webkit-scrollbar {{
  width: 6.5px;
  height: 6.5px;
}}
::-webkit-scrollbar-track {{
  background: transparent;
}}
::-webkit-scrollbar-thumb {{
  background: {thumb_bg};
  border-radius: 9999px;
  border: 1px solid transparent;
  background-clip: content-box;
  transition: background-color 0.2s cubic-bezier(0.16, 1, 0.3, 1);
}}
::-webkit-scrollbar-thumb:hover {{
  background: {thumb_hover};
}}

/* ==========================================================================
   3. MULTI-LAYER ATMOSPHERIC SHADOWS & INSET HAIRLINES
   ========================================================================== */
.cau-shadow-ambient {{
  box-shadow:
    0 0 0 1px {hairline_color},
    0 2px 4px rgba(0, 0, 0, 0.2),
    0 12px 28px -4px rgba(0, 0, 0, 0.5),
    0 24px 48px -12px rgba(0, 0, 0, 0.7);
}}
.cau-shadow-glow {{
  box-shadow:
    0 0 0 1px {hairline_color},
    0 0 35px -5px {brand_color}33,
    0 20px 40px -15px rgba(0, 0, 0, 0.75);
}}
.cau-hairline-inset {{
  box-shadow: inset 0 1px 0 0 rgba(255, 255, 255, 0.12);
}}

/* ==========================================================================
   4. OPTICAL FROSTED GLASSMORHPISM
   ========================================================================== */
.cau-glass {{
  background-color: {glass_bg};
  backdrop-filter: blur(20px) saturate(190%) contrast(90%);
  -webkit-backdrop-filter: blur(20px) saturate(190%) contrast(90%);
  border: 1px solid {glass_border};
}}

/* ==========================================================================
   5. TACTILE ACTIVE-PRESS PHYSICS & ACCESSIBLE FOCUS
   ========================================================================== */
button:not(:disabled), a[role="button"], .cau-pressable {{
  will-change: transform;
  transition: transform 0.15s cubic-bezier(0.34, 1.56, 0.64, 1), box-shadow 0.15s ease, opacity 0.15s ease;
}}
button:not(:disabled):active, a[role="button"]:active, .cau-pressable:active {{
  transform: scale(0.975) translateY(0.5px);
}}
button:disabled, a[aria-disabled="true"] {{
  cursor: not-allowed;
  opacity: 0.45;
  pointer-events: none;
}}

/* Accessible Double-Offset Focus Rings */
button:focus-visible, a:focus-visible, input:focus-visible, [tabindex]:focus-visible {{
  outline: 2px solid {brand_color} !important;
  outline-offset: 2px !important;
}}

/* ==========================================================================
   6. ORGANIC TACTILE NOISE TEXTURE OVERLAY (SVG feTurbulence)
   ========================================================================== */
.cau-grain-overlay {{
  pointer-events: none;
  position: fixed;
  inset: 0;
  width: 100vw;
  height: 100vh;
  z-index: 999998;
  opacity: 0.022;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)'/%3E%3C/svg%3E");
}}

/* ==========================================================================
   7. MOBILE SAFE-AREA INSETS (iOS & Android PWA Viewport Parity)
   ========================================================================== */
@supports (padding-bottom: env(safe-area-inset-bottom)) {{
  .cau-safe-top {{
    padding-top: env(safe-area-inset-top) !important;
  }}
  .cau-safe-bottom, footer, #signup-bar, [data-testid="now-playing-bar"], .fixed.bottom-0 {{
    padding-bottom: calc(0.5rem + env(safe-area-inset-bottom)) !important;
  }}
}}

/* ==========================================================================
   8. REDUCED-MOTION VESTIBULAR COMFORT (WCAG 2.3.3)
   ========================================================================== */
@media (prefers-reduced-motion: reduce) {{
  *, ::before, ::after {{
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }}
  .cau-grain-overlay {{
    display: none !important;
  }}
}}
"""


def apply_micro_details(target_dir: Path, brand_color: str = "#3b82f6", is_dark: bool = True) -> None:
    """Extracts and applies master micro-details to a target clone directory."""
    css_files = list(target_dir.rglob("*.css"))
    aggregated_css = ""
    for cf in css_files:
        try:
            aggregated_css += cf.read_text(encoding="utf-8", errors="ignore") + "\n"
        except Exception:
            pass

    details = extract_micro_details_from_css(aggregated_css, default_brand=brand_color)

    # Save micro_details.json
    json_path = target_dir / "tokens" / "micro_details.json" if (target_dir / "tokens").exists() else target_dir / "micro_details.json"
    json_path.write_text(json.dumps(details, indent=2), encoding="utf-8")
    print(f"  [✓] Microscopic detail tokens saved to: {json_path}")

    # Generate micro_details.css
    micro_css = generate_micro_details_css(details, brand_color=brand_color, is_dark=is_dark)
    css_path = target_dir / "assets" / "css" / "micro_details.css" if (target_dir / "assets" / "css").exists() else target_dir / "micro_details.css"
    css_path.parent.mkdir(parents=True, exist_ok=True)
    css_path.write_text(micro_css, encoding="utf-8")
    print(f"  [✓] Sub-pixel polish stylesheet generated: {css_path}")

    # Inject into preview.html and site/index.html
    style_inject = f"\n  <!-- CAU Microscopic Polish & Sub-Pixel Parity -->\n  <style>\n{micro_css}\n  </style>\n"
    grain_div = '\n  <div class="cau-grain-overlay" aria-hidden="true"></div>\n'

    for html_file in [target_dir / "preview.html", target_dir / "site" / "index.html"]:
        if html_file.exists():
            content = html_file.read_text(encoding="utf-8")
            if "CAU Microscopic Polish" in content:
                content = re.sub(r'<!-- CAU Microscopic Polish & Sub-Pixel Parity -->\s*<style>.*?</style>', style_inject.strip(), content, flags=re.DOTALL)
            else:
                if "</head>" in content:
                    content = content.replace("</head>", f"{style_inject}</head>")
            if "cau-grain-overlay" not in content and "</body>" in content:
                content = content.replace("</body>", f"{grain_div}</body>")
            html_file.write_text(content, encoding="utf-8")
            print(f"  [✓] Injected/Updated microscopic polish & organic grain into: {html_file}")


def main() -> None:
    parser = argparse.ArgumentParser(description="CAU Master Microscopic Detail & Polish Extractor")
    parser.add_argument("--target-dir", required=True, help="Target directory of clone")
    parser.add_argument("--brand-color", default="#3b82f6", help="Primary brand accent color")
    parser.add_argument("--dark", action="store_true", default=True, help="Apply dark mode optimizations")
    args = parser.parse_args()

    apply_micro_details(Path(args.target_dir), brand_color=args.brand_color, is_dark=args.dark)


if __name__ == "__main__":
    main()
