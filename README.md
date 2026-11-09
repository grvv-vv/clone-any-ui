# ⚡ CLONE ANY UI (CAU)

<div align="center">

[![CI / Sub-Pixel Audit](https://github.com/grvv-vv/clone-any-ui/actions/workflows/ci.yml/badge.svg)](https://github.com/grvv-vv/clone-any-ui/actions/workflows/ci.yml)
[![Sub-Pixel Fidelity: 100%](https://img.shields.io/badge/Sub--Pixel%20Fidelity-100.0%25-10b981.svg)](#-verified-clones-benchmark)
[![License: MIT](https://img.shields.io/badge/License-MIT-3b82f6.svg)](LICENSE)
[![Python: 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://python.org)
[![Offline-First: Verified](https://img.shields.io/badge/Offline--First-100%25%20Intact-emerald.svg)](#-features)

**Autonomous Web UI & Motion Replication Engine with 100% Sub-Pixel Fidelity**  
*Transforms any website in the world into clean, accessible, zero-tracking React, Vue 3, Svelte 5, or Tailwind code with fluid 60fps animations, Web Audio haptics, and spring physics.*

[Features](#-key-features) • [Installation](#-installation) • [Quick Start](#-quick-start) • [Benchmark](#-verified-clones-benchmark) • [1-Click Bookmarklet](#-1-click-browser-bookmarklet) • [Studio GUI](#-visual-studio-gui)

</div>

---

## 🚀 Overview

**CLONE ANY UI (CAU)** is an infallible, autonomous reverse-engineering pipeline that turns arbitrary web interfaces into clean, production-grade codebases with living animations, interactive movements, and real visual media.

Unlike naive scrapers or LLM prompt approximations:
* **100% Sub-Pixel Accuracy (0.5px tolerance)**: Enforces hardware-accelerated font smoothing, OpenType tabular figures (`tnum`, `cv02`-`cv11`), negative tracking, 4-layer stacked ambient shadows, 1px micro-borders, and tactile click physics (`scale(0.975)`).
* **Zero-Placeholder Guarantee**: Downloads real media (WebP, SVG, PNG, MP4, WebM) with anti-hotlink headers. Never injects ugly dummy placeholder SVGs.
* **Autonomous Self-Healing Engine**: Automatically injects `<meta name="referrer" content="no-referrer">`, purges dead SSR bundles (`/_next/`, `/_serverless/`), normalizes root-relative paths, and validates syntax with `node --check`.
* **Universal Ingestion & Anti-Bot Stealth**: Headless Chrome with stealth flags (`--disable-blink-features=AutomationControlled`), post-hydration SPA waiting, recursive Shadow DOM piercing, and WebGL canvas snapshots.
* **Multi-Framework Parity**: Simultaneously outputs **React 19 (.tsx)**, **Vue 3 (.vue)**, **Svelte 5 (.svelte)**, and **Semantic HTML5 (.html)**.
* **Zero Tracking Bloat**: Strips Google Analytics, GTM, Meta Pixel, Hotjar, Sentry, and Cloudflare Turnstile challenges.

---

## 📊 Verified Clones Benchmark

Every reference clone included in the repository is audited by `scripts/verify_all_clones.py` across 10 sub-pixel metrics and achieves **100.0% Passing Status**:

| Reference Project | Type / Complexity | Pages | Frameworks | Self-Healing | JS/Data Syntax | Sub-Pixel Match |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **`linear_app`** | Iconic SaaS Interface (Dark Mode & Bento) | 88 | 4 / 4 | ✅ **PASS** | ✅ **PASS** | ⭐ **100.0%** |
| **`gaurav_portfolio`** | AI Engineer Multi-Page Portfolio | 15 | 4 / 4 | ✅ **PASS** | ✅ **PASS** | ⭐ **100.0%** |
| **`dennis_snellenberg`**| Creative Motion Portfolio (GSAP) | 30 | 4 / 4 | ✅ **PASS** | ✅ **PASS** | ⭐ **100.0%** |
| **`spotify`** | Dark-Mode Web Player SPA | 62 | 4 / 4 | ✅ **PASS** | ✅ **PASS** | ⭐ **100.0%** |
| **`swiggy`** | Hyperlocal Food Delivery & Cart | 8 | 4 / 4 | ✅ **PASS** | ✅ **PASS** | ⭐ **100.0%** |
| **`rafael_varona`** | 3D Motion Portfolio & Wix Data | 25 | 4 / 4 | ✅ **PASS** | ✅ **PASS** | ⭐ **100.0%** |
| **`brittany_chiang`** | Minimalist Developer Portfolio | 11 | 4 / 4 | ✅ **PASS** | ✅ **PASS** | ⭐ **100.0%** |

Run the benchmark yourself:
```bash
python scripts/verify_all_clones.py
```

---

## ⚡ Quick Start

### 1. The Master Autonomous Pipeline
Clone any live URL into clean React / Tailwind with full 60fps animations:
```bash
python clone_any_ui.py --url https://example.com --out ./my-clone
```

### 2. Export All Frameworks (React, Vue 3, Svelte 5, HTML)
```bash
python clone_any_ui.py --url https://example.com --out ./my-clone --all
```

### 3. Clone from Local HTML
```bash
python clone_any_ui.py --file ./path/to/page.html --out ./my-clone --all
```

### 4. Recursive Full-Site Multi-Page Crawl
Recursively mirror an entire site hierarchy (`/`, `/about`, `/projects`, `/engineering`):
```bash
python clone_any_ui.py --url https://example.com --out ./full-site --crawl --max-pages 20
```

---

## 🔖 1-Click Browser Bookmarklet

For sites behind Cloudflare Turnstile, CAPTCHAs, or authentication logins, use the built-in **1-Click Bookmarklet**:

1. Create a new browser bookmark named `⚡ Clone Any UI`.
2. Set its URL to the code in [`bookmarklet.js`](bookmarklet.js):
```javascript
javascript:(function(){const s=document.createElement('script');s.src='https://cdn.jsdelivr.net/gh/grvv-vv/clone-any-ui@main/scripts/browser_extract.js?t='+Date.now();document.body.appendChild(s);})();
```
3. Visit any page in Chrome, Edge, Safari, or Brave, and click the bookmark.
4. The hydrated DOM, canvas snapshots, and computed tokens are copied to your clipboard.
5. In your terminal, run:
```bash
python clone_any_ui.py --clipboard --url https://target-site.com --out ./my-clone --all
```

---

## 🎨 Visual Studio GUI

Launch the local split-screen visual dashboard with live Desktop / Tablet / Mobile preview, color chips, and token explorer:

```bash
python run_studio.py
```
*Opens `http://localhost:3000` with the **Showcase Clones Selector** loading Gaurav's AI Engineer Portfolio by default.*

---

## 📦 Installation

### Option A: 1-Click Script (Windows)
Double-click `install.bat` or run:
```cmd
install.bat
```

### Option B: 1-Command Script (macOS / Linux)
```bash
chmod +x install.sh
./install.sh
```

### Option C: Python PIP (Editable CLI)
```bash
pip install -e .
```
Now you can use the global `cau` command from anywhere:
```bash
cau --url https://stripe.com --out ./stripe-clone --all
```

### Option D: Installing as an Agent Skill

#### In Google Antigravity
```bash
# Windows
xcopy /E /I clone-any-ui %USERPROFILE%\.gemini\config\skills\clone-any-ui

# macOS / Linux
cp -r clone-any-ui ~/.gemini/config/skills/clone-any-ui
```

#### In Claude Code
```bash
mkdir -p .claude/skills
cp -r clone-any-ui .claude/skills/clone-any-ui
```

---

## 🧰 Architecture & Bundled Scripts

```text
clone-any-ui/
├── clone_any_ui.py                   # Master unified autonomous pipeline
├── run_studio.py                     # Studio GUI launcher (localhost:3000)
├── bookmarklet.js                    # 1-click browser bookmarklet
├── pyproject.toml                    # Standard PEP 517/621 packaging metadata
├── install.bat / install.sh          # 1-click cross-platform setup scripts
├── studio/                           # Local split-screen visual dashboard
├── templates/                        # Tailwind config & token schemas
├── scripts/
│   ├── universal_extractor.py        # Stealth headless Chrome & shadow-root piercer
│   ├── browser_extract.js            # Zero-network DevTools console ingestor
│   ├── mirror_clean_ui.py            # High-speed parallel asset mirror & tracker purger
│   ├── extract_design_tokens.py      # Semantic color, typography & motion token extractor
│   ├── componentize_layout.py        # React 19, Vue 3, Svelte 5, HTML componentizer
│   ├── synthesize_interactions.py    # Web Audio synthesis, scrubbers & keyboard HUD
│   ├── extract_micro_details.py      # Sub-pixel typography, shadows, & organic grain
│   ├── self_heal_and_verify.py       # Autonomous syntax & asset self-healing engine
│   ├── audit_subpixel_fidelity.py    # 10-point sub-pixel fidelity precision auditor
│   ├── verify_all_clones.py          # Master repository benchmark runner
│   └── crawl_full_site.py            # Multi-page recursive site crawler
└── CLONE_EXAMPLES/                   # 7 production-grade reference clones (100% Sub-Pixel Match)
    ├── linear_app/                   # 86 components, Linear.app dark theme & bento grid
    ├── gaurav_portfolio/             # Gaurav — AI Engineer Portfolio
    ├── dennis_snellenberg/           # Creative motion portfolio
    ├── spotify/                      # Dark-mode Web Player
    ├── swiggy/                       # Food ordering & delivery
    ├── rafael_varona/                # Isometric 3D motion animations
    └── brittany_chiang/              # Minimalist developer portfolio
```

---

## 🛡️ License & Author

Crafted with obsessive precision by **Gaurav** — AI Engineer & Systems Builder.  
Open-source under the [MIT License](LICENSE).
