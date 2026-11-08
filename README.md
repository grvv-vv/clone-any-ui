# ⚡ CLONE ANY UI (CAU)

### Advanced Web UI Reverse-Engineering, Design System & Motion Replication Agent Skill

**Design Token Extraction · 60fps Motion & Keyframe Extraction · Exact Media & Video Downloader (Zero-Placeholder Guarantee) · Multi-Framework Componentization (React / Vue / Svelte / HTML) · Purged Asset Mirroring · Micro-Interaction Physics · Visual & Motion Parity Auditing**

---

## 🚀 Overview

**CLONE ANY UI (CAU)** is a precision agent skill that turns arbitrary web interfaces into clean, production-grade codebases with living animations, interactive movements, and exact visual media.

Unlike standard screen-scraping or naive LLM prompting:
* **Extracts design & motion tokens automatically**: Pulls color palettes, typography hierarchies, border-radii, shadows, CSS `@keyframes`, and cubic-bezier easing curves directly into `tokens.json`, `tailwind.config.js`, `tokens.css`, and `theme.v4.css`.
* **Exact visual media replication (Zero-Placeholder Guarantee)**: Downloads exact images (PNG, WebP, JPG, SVG, AVIF) and video clips (MP4, WebM, MOV) using referer spoofing and streaming chunking. Never substitutes generic SVG placeholder boxes. Embeds real media directly into component showcases, cards, and video players.
* **Captures authentic UI movement & micro-interactions**: Replicates card hover lifts (`hover:-translate-y-2 hover:shadow-xl`), interactive icon rotations, spring physics toggle switches, floating ambient badges, continuous infinite marquee tickers, and staggered scroll entrance reveals.
* **Transforms raw HTML into clean components**: Converts messy, minified DOM trees into clean **React (.tsx)**, **Vue 3 (.vue)**, **Svelte 5 (.svelte)**, or **Tailwind HTML** components.
* **Purges tracking & analytics bloat**: Automatically removes Google Tag Manager, Meta Pixel, Hotjar, Sentry, and broken hydration scripts.
* **Performs automated visual & motion parity QA**: Measures computed styles, bounding-box geometry tolerances (within 2px), and transition durations.
* **Guarantees accessibility**: Enforces WCAG 2.1 AA text contrast and `@media (prefers-reduced-motion: reduce)` compliance.

---

## 🧰 Bundled Scripts

| Script | Purpose |
| :--- | :--- |
| `scripts/extract_micro_details.py` | Master Microscopic Polish Engine: Injects sub-pixel typography (OpenType `tnum`, `cv01`-`cv11`, negative tracking, `text-wrap: balance`), 4-layer stacked ambient shadows, 1px hairlines, sleek custom scrollbars, tactile active press physics, accessible focus rings, and organic SVG grain texture. |
| `scripts/audit_subpixel_fidelity.py` | Sub-Pixel Precision Auditor: Evaluates clone fidelity down to 0.5px tolerances across 10 sub-pixel metrics and outputs a Micro-Fidelity Precision Score (0-100%). |
| `scripts/synthesize_interactions.py` | Universal Behavioral Engine: Injects zero-dependency 60fps working interactivity (audio playback, scrubbers, live search, counters, cart badges, tabs, and spring likes) across any website. |
| `scripts/extract_motion_physics.py` | Extracts CSS `@keyframes`, animations, spring timing curves, and hover physics into JSON & CSS. |
| `scripts/extract_design_tokens.py` | Extracts CSS variables, colors, typography, radii, shadows, and motion tokens into JSON & Tailwind config. |
| `scripts/mirror_clean_ui.py` | Mirrors HTML, webfonts, SVGs, and stylesheets while stripping all tracking beacons. |
| `scripts/componentize_layout.py` | Segments HTML into clean React, Vue 3, Svelte 5, or HTML components with built-in micro-interactions and motion. |
| `scripts/style_snapshot.js` | In-browser / DevTools console helper to extract computed styles, geometry, and keyframe catalogs. |
| `scripts/compare_visual_parity.py` | Audits style, geometry, and motion drift between reference and replica, generating a Markdown report. |

---

## ⚡ Quick Start: One-Click Exact Clone

### 🚀 The Master Unified Command
Paste any URL and clone it completely with full asset and motion parity in a single step:
```bash
# Clone any live website into clean React + Tailwind components with 60fps animations:
python clone_any_ui.py --url https://target-site.com --out ./my-clone

# Clone into ALL frameworks (React, Vue 3, Svelte 5, HTML):
python clone_any_ui.py --url https://target-site.com --out ./my-clone --all

# Clone from a local HTML file or capture:
python clone_any_ui.py --file ./path/to/page.html --out ./my-clone --all

# Ingest live DOM from clipboard (bypasses Cloudflare / CAPTCHA):
python clone_any_ui.py --clipboard --url https://target-site.com --out ./my-clone --all
```

Outputs produced automatically:
* `site/index.html`: Offline mirrored site with all fonts, SVGs, and stylesheets.
* `tokens/`: Extracted design & motion tokens (`tokens.json`, `tailwind.config.js`, `tokens.css`, `theme.v4.css`).
* `components/`: Modular, production-ready React (`.tsx`), Vue (`.vue`), Svelte (`.svelte`), or HTML components with hover physics and micro-interactions.
* `preview.html`: Zero-build instant live preview with Tailwind pre-configured, keyframes injected, and scroll reveal observer active.
* `CLONE_REPORT.md`: Comprehensive audit report with WCAG 2.1 AA and Motion Parity checklist.

---

### 🌊 Motion & Movement Workflow

```bash
# Extract motion tokens, CSS keyframes, and spring curves:
python scripts/extract_motion_physics.py --url https://target-site.com --out ./motion-tokens

# Extract complete design system (colors + typography + motion):
python scripts/extract_design_tokens.py --url https://target-site.com --out ./design-tokens
```

---

## 📦 Directory Structure

```text
clone-any-ui/
├── SKILL.md                          # Main agent skill definition (10 operating modes)
├── README.md                         # Complete documentation & usage guide
├── LICENSE                           # MIT License
├── clone_any_ui.py                   # Master unified autonomous pipeline
├── run_studio.py                     # Studio GUI dashboard launcher
├── studio/                           # Local split-screen visual dashboard with Motion Tab
├── templates/
│   ├── tailwind.config.template.js   # Production-ready Tailwind template with keyframes
│   └── tokens.schema.json            # Design & motion tokens schema
├── scripts/
│   ├── extract_micro_details.py      # Master microscopic polish & sub-pixel engine
│   ├── audit_subpixel_fidelity.py    # 10-point sub-pixel fidelity auditor
│   ├── synthesize_interactions.py    # Universal 60fps working interactivity engine
│   ├── extract_motion_physics.py     # CSS keyframes, easings & hover physics extractor
│   ├── extract_design_tokens.py      # Token & CSS variable extractor (includes motion)
│   ├── mirror_clean_ui.py            # Sanitized asset & HTML scraper
│   ├── componentize_layout.py        # Semantic component generator with fluid motion
│   ├── style_snapshot.js             # Computed styles & live keyframe catalog extractor
│   └── compare_visual_parity.py      # Visual & motion parity audit engine
└── CLONE_EXAMPLES/                   # 6 production-grade verified reference clones
    ├── gaurav_portfolio/             # 4-route agency portfolio (About, Projects, Engineering, YesCheff)
    ├── spotify/                      # 59 components, working Web Audio synth & draggable scrubber
    ├── dennis_snellenberg/           # Magnetic cursor physics & inertial smooth scroll
    ├── swiggy/                       # Food delivery UI with cart state & item steppers
    ├── rafael_varona/                # Interactive SVG loop & 3D card tilt
    └── brittany_chiang/              # Minimalist portfolio with mouse spotlight glow
```

---

## 💻 Installing as an AI Agent Skill

You can use **CLONE ANY UI** directly in your terminal, or install it into your favorite agentic AI coding environment:

### In Google Antigravity
Copy the directory into your global skills folder:
```bash
# Windows
xcopy /E /I clone-any-ui %USERPROFILE%\.gemini\config\skills\clone-any-ui

# macOS / Linux
cp -r clone-any-ui ~/.gemini/config/skills/clone-any-ui
```

### In Claude Code
Add to your project's skills directory:
```bash
mkdir -p .claude/skills
cp -r clone-any-ui .claude/skills/clone-any-ui
```

---

## 👨‍💻 Author & Credits

Crafted with obsessive precision by **Gaurav** — AI Engineer & Systems Builder.  
Open-source under the [MIT License](LICENSE). Contributions, issues, and feature requests welcome!

