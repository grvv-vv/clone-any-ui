#!/usr/bin/env python3
"""Motion, Animation & Micro-Interaction Extractor for Web UI Replication.

Extracts CSS @keyframes, animation properties, transition timing curves (cubic-bezier),
hover physics, and micro-interactions from local CSS/HTML or live URLs.
Generates:
1. motion.json (Structured keyframes, animations, transitions, and easings)
2. tailwind.motion.config.js (Tailwind theme.extend.keyframes and animation snippet)
3. motion.css (Native @keyframes, CSS custom properties, and utility classes with prefers-reduced-motion)

Usage:
  python extract_motion_physics.py --file path/to/style.css --out ./extracted_motion
  python extract_motion_physics.py --file path/to/index.html --out ./extracted_motion
  python extract_motion_physics.py --url https://example.com --out ./extracted_motion
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections import Counter
from pathlib import Path
from urllib.parse import urljoin
from urllib.request import Request, urlopen

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"

# Regex patterns for motion extraction
KEYFRAMES_START_RE = re.compile(r"@(?:-webkit-)?keyframes\s+([a-zA-Z0-9_\-]+)\s*\{", re.I)
ANIMATION_PROP_RE = re.compile(r"(?:^|[;{\s])animation(?:-name)?\s*:\s*([^;!}]+)", re.I)
ANIMATION_DURATION_RE = re.compile(r"(?:^|[;{\s])animation-duration\s*:\s*([^;!}]+)", re.I)
ANIMATION_TIMING_RE = re.compile(r"(?:^|[;{\s])animation-timing-function\s*:\s*([^;!}]+)", re.I)
TRANSITION_PROP_RE = re.compile(r"(?:^|[;{\s])transition(?:-property)?\s*:\s*([^;!}]+)", re.I)
TRANSITION_DURATION_RE = re.compile(r"(?:^|[;{\s])transition-duration\s*:\s*([^;!}]+)", re.I)
TRANSITION_TIMING_RE = re.compile(r"(?:^|[;{\s])transition-timing-function\s*:\s*([^;!}]+)", re.I)
CUBIC_BEZIER_RE = re.compile(r"cubic-bezier\(\s*[\d.]+\s*,\s*[\d.-]+\s*,\s*[\d.]+\s*,\s*[\d.-]+\s*\)", re.I)
TRANSFORM_RE = re.compile(r"(?:^|[;{\s])transform\s*:\s*([^;!}]+)", re.I)

# High-fidelity motion presets for modern SaaS & web apps
ESSENTIAL_KEYFRAME_PRESETS = {
    "fade-in-up": {
        "0%": {"opacity": "0", "transform": "translateY(16px)"},
        "100%": {"opacity": "1", "transform": "translateY(0)"},
    },
    "fade-in-down": {
        "0%": {"opacity": "0", "transform": "translateY(-16px)"},
        "100%": {"opacity": "1", "transform": "translateY(0)"},
    },
    "float": {
        "0%, 100%": {"transform": "translateY(0)"},
        "50%": {"transform": "translateY(-6px)"},
    },
    "pulse-glow": {
        "0%, 100%": {"opacity": "0.35", "transform": "scale(1)"},
        "50%": {"opacity": "0.75", "transform": "scale(1.04)"},
    },
    "marquee": {
        "0%": {"transform": "translateX(0%)"},
        "100%": {"transform": "translateX(-50%)"},
    },
    "shimmer": {
        "0%": {"background-position": "-200% 0"},
        "100%": {"background-position": "200% 0"},
    },
    "accordion-down": {
        "0%": {"height": "0", "opacity": "0"},
        "100%": {"height": "var(--radix-accordion-content-height, auto)", "opacity": "1"},
    },
    "accordion-up": {
        "0%": {"height": "var(--radix-accordion-content-height, auto)", "opacity": "1"},
        "100%": {"height": "0", "opacity": "0"},
    },
    "scale-subtle": {
        "0%, 100%": {"transform": "scale(1)"},
        "50%": {"transform": "scale(1.02)"},
    },
    "badge-ping": {
        "0%": {"transform": "scale(1)", "opacity": "0.8"},
        "75%, 100%": {"transform": "scale(2)", "opacity": "0"},
    },
}

ESSENTIAL_ANIMATION_PRESETS = {
    "fade-in-up": "fade-in-up 0.5s cubic-bezier(0.16, 1, 0.3, 1) forwards",
    "fade-in-down": "fade-in-down 0.5s cubic-bezier(0.16, 1, 0.3, 1) forwards",
    "float": "float 4s ease-in-out infinite",
    "pulse-glow": "pulse-glow 3.5s ease-in-out infinite",
    "marquee": "marquee 30s linear infinite",
    "shimmer": "shimmer 2s linear infinite",
    "accordion-down": "accordion-down 0.2s ease-out",
    "accordion-up": "accordion-up 0.2s ease-out",
    "scale-subtle": "scale-subtle 3s ease-in-out infinite",
    "badge-ping": "badge-ping 1.5s cubic-bezier(0, 0, 0.2, 1) infinite",
}

ESSENTIAL_EASING_PRESETS = {
    "spring": "cubic-bezier(0.16, 1, 0.3, 1)",
    "bounce-soft": "cubic-bezier(0.34, 1.56, 0.64, 1)",
    "smooth-out": "cubic-bezier(0, 0, 0.2, 1)",
    "smooth-in-out": "cubic-bezier(0.4, 0, 0.2, 1)",
    "accelerate": "cubic-bezier(0.4, 0, 1, 1)",
}


def fetch_url_text(url: str, timeout: int = 15) -> str:
    req = Request(url, headers={"User-Agent": USER_AGENT})
    with urlopen(req, timeout=timeout) as res:
        charset = res.headers.get_content_charset() or "utf-8"
        return res.read().decode(charset, errors="replace")


def extract_balanced_block(text: str, start_index: int) -> tuple[str, int]:
    """Finds matching closing brace for a block starting at start_index."""
    depth = 0
    i = start_index
    length = len(text)
    while i < length:
        char = text[i]
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return text[start_index:i+1], i + 1
        i += 1
    return text[start_index:], length


def parse_keyframes(css_text: str) -> dict[str, dict]:
    """Extracts all @keyframes definitions with their steps and styles."""
    keyframes_dict = {}
    pos = 0

    while True:
        match = KEYFRAMES_START_RE.search(css_text, pos)
        if not match:
            break

        name = match.group(1).strip()
        open_brace_idx = match.end() - 1
        raw_block, end_idx = extract_balanced_block(css_text, open_brace_idx)
        pos = end_idx

        # Strip outer braces
        inner_body = raw_block[1:-1].strip()

        # Parse individual steps like 0% { ... }, from { ... }, 100% { ... }
        step_pattern = re.compile(r"([0-9\s,%a-zA-Z_\-]+)\s*\{([^}]+)\}")
        steps = {}
        for s_match in step_pattern.finditer(inner_body):
            selectors = s_match.group(1).strip()
            declarations_raw = s_match.group(2).strip()
            decl_map = {}
            for decl in declarations_raw.split(";"):
                decl = decl.strip()
                if ":" in decl:
                    k, v = decl.split(":", 1)
                    decl_map[k.strip()] = v.strip()
            if decl_map:
                steps[selectors] = decl_map

        if steps:
            keyframes_dict[name] = steps

    return keyframes_dict


def parse_hover_micro_interactions(css_text: str) -> list[dict]:
    """Extracts hover, active, and focus transform and motion rules."""
    hover_pattern = re.compile(r"([^{}\n]*:(?:hover|active|focus|focus-visible|focus-within|group-hover)[^{}\n]*)\s*\{([^}]+)\}", re.I)
    micro_interactions = []

    for match in hover_pattern.finditer(css_text):
        selector = match.group(1).strip()
        body = match.group(2).strip()

        # Check for transform, transition, scale, shadow, translate
        has_motion = any(prop in body.lower() for prop in ["transform", "translate", "scale", "rotate", "box-shadow", "filter", "opacity"])
        if has_motion:
            declarations = {}
            for item in body.split(";"):
                item = item.strip()
                if ":" in item:
                    k, v = item.split(":", 1)
                    k_clean = k.strip()
                    if any(p in k_clean.lower() for p in ["transform", "transition", "box-shadow", "opacity", "filter", "color"]):
                        declarations[k_clean] = v.strip()
            if declarations:
                micro_interactions.append({
                    "selector": selector,
                    "declarations": declarations
                })

    return micro_interactions[:30]


def extract_motion_tokens(css_text: str) -> dict:
    """Master motion extractor combining parsed keyframes, animations, transitions, and hover physics."""
    # 1. Parse Keyframes
    parsed_keyframes = parse_keyframes(css_text)

    # Merge with essential presets to ensure baseline smoothness
    merged_keyframes = dict(ESSENTIAL_KEYFRAME_PRESETS)
    merged_keyframes.update(parsed_keyframes)

    # 2. Extract Animation Declarations
    animation_names = []
    for anim_match in ANIMATION_PROP_RE.findall(css_text):
        anim_str = anim_match.strip()
        # animation can be 'name duration timing-function ...' or just 'name'
        tokens = anim_str.split()
        if tokens:
            name_candidate = tokens[0]
            if not any(token_unit in name_candidate for token_unit in ["s", "ms", "cubic-bezier", "infinite", "ease", "linear"]):
                animation_names.append(name_candidate)

    # 3. Extract Transition Properties & Timing Functions
    transitions = Counter([t.strip() for t in TRANSITION_PROP_RE.findall(css_text) if t.strip()])
    transition_durations = Counter([d.strip() for d in TRANSITION_DURATION_RE.findall(css_text) if d.strip()])
    transition_timings = Counter([t.strip() for t in TRANSITION_TIMING_RE.findall(css_text) if t.strip()])
    cubic_beziers = Counter([cb.strip() for cb in CUBIC_BEZIER_RE.findall(css_text)])

    # 4. Extract Hover Micro-Interactions
    hover_interactions = parse_hover_micro_interactions(css_text)

    # 5. Build Animation Map for Tailwind
    tailwind_animations = dict(ESSENTIAL_ANIMATION_PRESETS)
    for name in parsed_keyframes.keys():
        if name not in tailwind_animations:
            tailwind_animations[name] = f"{name} 0.5s cubic-bezier(0.16, 1, 0.3, 1) forwards"

    # 6. Build Easings Map
    easings = dict(ESSENTIAL_EASING_PRESETS)
    for idx, (cb, _) in enumerate(cubic_beziers.most_common(5)):
        easings[f"custom-ease-{idx+1}"] = cb

    return {
        "keyframes": merged_keyframes,
        "animations": tailwind_animations,
        "transitions": {
            "mostCommon": [t for t, _ in transitions.most_common(8)],
            "durations": [d for d, _ in transition_durations.most_common(6)],
            "timings": [t for t, _ in transition_timings.most_common(6)],
        },
        "easings": easings,
        "hoverMicroInteractions": hover_interactions,
    }


def generate_tailwind_motion_config(motion_tokens: dict) -> str:
    """Generates plug-and-play theme.extend snippet for Tailwind animation."""
    keyframes = motion_tokens.get("keyframes", {})
    animations = motion_tokens.get("animations", {})
    easings = motion_tokens.get("easings", {})

    lines = [
        "    // --- Extracted Motion & Animation Tokens ---",
        "    keyframes: {",
    ]

    for name, steps in keyframes.items():
        lines.append(f"      '{name}': {{")
        for step_key, decls in steps.items():
            lines.append(f"        '{step_key}': {{")
            for prop, val in decls.items():
                # Sanitize single quotes
                safe_val = val.replace("'", "\\'")
                lines.append(f"          '{prop}': '{safe_val}',")
            lines.append("        },")
        lines.append("      },")

    lines.append("    },")
    lines.append("    animation: {")
    for name, rule in animations.items():
        lines.append(f"      '{name}': '{rule}',")
    lines.append("    },")

    lines.append("    transitionTimingFunction: {")
    for name, curve in easings.items():
        lines.append(f"      '{name}': '{curve}',")
    lines.append("    },")

    return "\n".join(lines)


def generate_motion_css(motion_tokens: dict) -> str:
    """Generates complete motion.css with @keyframes, utility classes, and reduced-motion guard."""
    lines = [
        "/* ========================================================",
        "   CLONE ANY UI (CAU) — Motion & Micro-Interaction System",
        "   Fluid 60fps animations, physics curves, and WCAG AA guard",
        "   ======================================================== */",
        "",
        ":root {",
        "  /* Spring & Easing Physics */",
    ]

    for name, curve in motion_tokens.get("easings", {}).items():
        lines.append(f"  --ease-{name}: {curve};")

    lines.extend([
        "  --duration-instant: 150ms;",
        "  --duration-normal: 300ms;",
        "  --duration-slow: 500ms;",
        "  --duration-ambient: 3500ms;",
        "}",
        "",
        "/* --- CSS Keyframes --- */",
    ])

    for name, steps in motion_tokens.get("keyframes", {}).items():
        lines.append(f"@keyframes {name} {{")
        for step_key, decls in steps.items():
            lines.append(f"  {step_key} {{")
            for prop, val in decls.items():
                lines.append(f"    {prop}: {val};")
            lines.append("  }")
        lines.append("}")
        lines.append("")

    lines.extend([
        "/* --- Reusable Motion Utility Classes --- */",
        ".cau-animate-fade-up {",
        "  animation: fade-in-up 0.6s var(--ease-spring, cubic-bezier(0.16, 1, 0.3, 1)) forwards;",
        "}",
        ".cau-animate-float {",
        "  animation: float 4s ease-in-out infinite;",
        "}",
        ".cau-animate-pulse-glow {",
        "  animation: pulse-glow 3.5s ease-in-out infinite;",
        "}",
        ".cau-animate-marquee {",
        "  display: flex;",
        "  width: max-content;",
        "  animation: marquee 30s linear infinite;",
        "}",
        ".cau-animate-shimmer {",
        "  background: linear-gradient(90deg, rgba(255,255,255,0) 0%, rgba(255,255,255,0.08) 50%, rgba(255,255,255,0) 100%);",
        "  background-size: 200% 100%;",
        "  animation: shimmer 2.5s linear infinite;",
        "}",
        "",
        "/* Interactive Micro-Interactions (Hover Lift, Active Spring, Magnetic Feedback) */",
        ".cau-hover-lift {",
        "  transition: transform 0.25s var(--ease-spring, cubic-bezier(0.16, 1, 0.3, 1)), box-shadow 0.25s ease-out, border-color 0.25s ease-out;",
        "  will-change: transform;",
        "}",
        ".cau-hover-lift:hover {",
        "  transform: translateY(-4px);",
        "  box-shadow: 0 12px 24px -8px rgba(0, 0, 0, 0.25);",
        "}",
        ".cau-hover-lift:active {",
        "  transform: translateY(-1px) scale(0.99);",
        "}",
        "",
        ".cau-interactive-btn {",
        "  position: relative;",
        "  overflow: hidden;",
        "  transition: all 0.2s var(--ease-spring, cubic-bezier(0.16, 1, 0.3, 1));",
        "}",
        ".cau-interactive-btn:hover {",
        "  transform: translateY(-1px);",
        "}",
        ".cau-interactive-btn:active {",
        "  transform: translateY(0.5px) scale(0.98);",
        "}",
        "",
        "/* Viewport Scroll Entrance (IntersectionObserver Hook) */",
        ".cau-reveal {",
        "  opacity: 0;",
        "  transform: translateY(24px);",
        "  transition: opacity 0.7s cubic-bezier(0.16, 1, 0.3, 1), transform 0.7s cubic-bezier(0.16, 1, 0.3, 1);",
        "  will-change: opacity, transform;",
        "}",
        ".cau-reveal.cau-visible {",
        "  opacity: 1;",
        "  transform: translateY(0);",
        "}",
        "",
        "/* Stagger Delays */",
        ".cau-delay-100 { transition-delay: 100ms; }",
        ".cau-delay-200 { transition-delay: 200ms; }",
        ".cau-delay-300 { transition-delay: 300ms; }",
        ".cau-delay-400 { transition-delay: 400ms; }",
        "",
        "/* Accessibility: Respect User Reduced Motion Preferences (WCAG 2.3.3) */",
        "@media (prefers-reduced-motion: reduce) {",
        "  *, ::before, ::after {",
        "    animation-duration: 0.01ms !important;",
        "    animation-iteration-count: 1 !important;",
        "    transition-duration: 0.01ms !important;",
        "    scroll-behavior: auto !important;",
        "  }",
        "  .cau-reveal {",
        "    opacity: 1 !important;",
        "    transform: none !important;",
        "  }",
        "}",
    ])

    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract motion, animations, and micro-interactions from CSS, HTML, or live URL.")
    parser.add_argument("--file", help="Path to local CSS or HTML file")
    parser.add_argument("--url", help="URL of live webpage")
    parser.add_argument("--out", default="motion_output", help="Directory to save extracted motion tokens")
    args = parser.parse_args()

    content = ""
    if args.url:
        print(f"[+] Fetching live page for motion extraction from: {args.url}")
        try:
            content = fetch_url_text(args.url)
        except Exception as exc:
            sys.exit(f"[-] Failed to fetch URL: {exc}")
    elif args.file:
        file_path = Path(args.file)
        if not file_path.exists():
            sys.exit(f"[-] File not found: {args.file}")
        content = file_path.read_text(encoding="utf-8", errors="replace")
    else:
        sys.exit("[-] Error: Please specify either --file or --url.")

    print("[+] Extracting motion tokens (@keyframes, transitions, easings, hover physics)...")
    motion_tokens = extract_motion_tokens(content)

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    # 1. Save motion.json
    motion_json_path = out_dir / "motion.json"
    motion_json_path.write_text(json.dumps(motion_tokens, indent=2), encoding="utf-8")
    print(f"[✓] Saved Motion Tokens to: {motion_json_path}")

    # 2. Save motion.css
    motion_css_path = out_dir / "motion.css"
    motion_css_path.write_text(generate_motion_css(motion_tokens), encoding="utf-8")
    print(f"[✓] Saved Motion CSS & Keyframes to: {motion_css_path}")

    # 3. Save tailwind.motion.config.js
    tw_config_path = out_dir / "tailwind.motion.config.js"
    tw_config_path.write_text("module.exports = {\n" + generate_tailwind_motion_config(motion_tokens) + "\n};\n", encoding="utf-8")
    print(f"[✓] Saved Tailwind Motion Config to: {tw_config_path}")

    print(f"[★] Extracted {len(motion_tokens['keyframes'])} keyframes and {len(motion_tokens['hoverMicroInteractions'])} hover interactions!")


if __name__ == "__main__":
    main()

