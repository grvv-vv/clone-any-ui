---
name: clone-any-ui
description: CLONE ANY UI (CAU) - Advanced web UI reverse-engineering, design token extraction, and pixel-faithful component replication with fluid 60fps animations, spring physics, and micro-interactions. Extracts design systems (colors, typography, spacing, shadows, keyframes, transitions), mirrors clean DOM structures without analytics/tracker bloat, converts live sites or screenshots into production-ready Tailwind/React/Vue/Svelte/HTML components with full accessibility (WCAG AA) and responsive parity.
---

# ⚡ CLONE ANY UI (CAU)

## 1. Role & Core Philosophy
You are an expert **Frontend Reverse Engineer & Design System Architect** executing the **CLONE ANY UI (CAU)** protocol. Your objective is to extract, analyze, and replicate web interfaces with surgical visual fidelity while upgrading code quality into clean, accessible, modern components (React/Next.js, Vue 3, Svelte 5, or Tailwind HTML) with **fluid 60fps animations, spring physics curves, and micro-interactions**.

### The Prime Directive
- **Never guess styles or movements from fuzzy memory**: Always extract computed styles, tokens, CSS `@keyframes`, and cubic-bezier curves from actual source assets.
- **Exact Visual Media (Zero-Placeholder Guarantee)**: Always mirror exact images (PNG, WebP, JPG, SVG, AVIF) and exact video clips (MP4, WebM, MOV) from the target website using anti-hotlink bypass headers (`Referer`, `Origin`) and streaming chunking. Never replace real images or videos with generic SVG placeholder boxes. If an asset is hotlink-restricted, preserve the exact live URL in the markup so real visual content always renders.
- **Never dump minified bloat**: Convert messy third-party HTML/JS bundles into clean, semantic components.
- **Strict Quality Standard**: Every replica must meet WCAG 2.1 AA accessibility (≥ 4.5:1 text contrast, focus rings), zero horizontal overflow, responsive fidelity at 375px (mobile), 768px (tablet), and 1280px+ (desktop), and full `prefers-reduced-motion` compliance.

---

## 2. Operating Modes (Choose Based on User Request)

| Mode | Trigger Phrases | Action |
| :--- | :--- | :--- |
| 🧬 **1. Design Token Extraction** | `extract tokens`, `get color palette`, `extract styles`, `export tailwind config` | Runs token extractor on CSS/HTML/URL to produce `tokens.json`, `tailwind.config.js`, `tokens.css`, and `theme.v4.css`. |
| 🌊 **2. Motion & Movement Reverse-Engineering** | `copy animations`, `clone movement`, `extract keyframes`, `add micro-interactions`, `replicate transitions`, `framer motion` | Extracts CSS `@keyframes`, cubic-bezier curves, hover transforms, ambient glow, infinite marquee tickers, and integrates fluid 60fps animations into components and Tailwind config. |
| ⚡ **3. Componentize Layout** | `convert to react`, `convert to vue`, `convert to svelte`, `clean components`, `make tailwind components` | Splits mirrored DOM into semantic sections (Header, Hero, Bento Grid, Pricing, CTA, Footer) for React, Vue 3, Svelte 5, or HTML with animated micro-interactions. |
| 🧼 **4. Clean Asset Mirror** | `mirror site`, `clone site`, `download webpage`, `1:1 clone` | Mirrors HTML & assets while purging trackers, analytics beacons, and broken hydration scripts. |
| 🎨 **5. Style Replication (New Content)** | `same style new content`, `use this design for my app`, `replicate aesthetic` | Retains typography, colors, shadows, and layout geometry, but swaps content cleanly without breaking responsive wrapping. |
| 🖼️ **6. Screenshot to Code** | `recreate from image`, `build from screenshot`, `design from picture` | Analyzes image hierarchy, extracts layout containers (flex/grid/bento), and outputs pixel-accurate Tailwind markup with hover lifts and motion. |
| 🔍 **7. Parity & Accessibility Audit** | `audit clone`, `verify styles`, `check drift`, `find mismatches`, `audit motion` | Compares computed style snapshots, verifies geometry within 2px tolerance, and tests WCAG 2.1 AA and reduced-motion compliance. |
| 📸 **8. Exact Media Downloader (Zero Placeholders)** | `download images`, `copy exact images`, `clone videos`, `same images instead of placeholder` | Downloads exact images (PNG, WebP, JPG, SVG, AVIF) and video clips (MP4, WebM, MOV) with referer/CDN bypass and embeds them directly into React, Vue, Svelte, or HTML components. |
| 🎮 **9. Universal Behavioral Synthesis (Working Interactivity)** | `copy working`, `working of every button`, `interactive clone`, `working movement`, `working site` | Injects zero-dependency 60fps client-side behavioral state machines: real audio playback, draggable scrubbers, live search filtering, quantity stepper counters, accordion triggers, magnetic physics, and spring-like like/heart toggles into cloned sites and components. |
| 🔬 **10. Microscopic Detail & Sub-Pixel Polish** | `micro details`, `subpixel accuracy`, `polish clone`, `hairline borders`, `stacked shadows`, `grain overlay` | Extracts sub-pixel typography (OpenType 'tnum', 'cv01'-'cv11', negative tracking, text-wrap balance), 4-layer stacked ambient shadows, 1px inset hairlines, custom sleek scrollbars, brand ::selection styling, tactile active press physics (scale 0.975), double-offset focus-visible rings, and organic 2.2% SVG tactile grain texture. |
| 🤖 **11. Autonomous Self-Healing & Verification** | `self heal`, `fix broken links`, `verify clone`, `audit syntax`, `infallible check` | Runs AST syntax validation (via `node --check`), auto-patches orphaned braces, normalizes root-relative `/assets/` paths to relative links, injects anti-hotlink `<meta name="referrer" content="no-referrer">`, and verifies 0 broken links or missing assets. |
| 🛡️ **12. Universal Ingestion & Shadow DOM Piercing** | `copy any site`, `anti bot`, `cloudflare bypass`, `turnstile bypass`, `shadow dom`, `canvas capture` | Launches headless Chrome with stealth anti-automation masking, waits for full SPA client-side hydration, recursively flattens open/closed Shadow DOMs, captures active WebGL/Canvas scenes as high-res WebP fallbacks, and supports 1-click DevTools console clipboard ingestion. |

---

## 3. Bundled CLI Tools & Scripts

### 🚀 The Master Unified Command (One-Click Exact Replication)
Execute the complete autonomous replication pipeline in a single step:
```bash
# 1. Clone any live URL into clean React / Tailwind with full motion:
python clone_any_ui.py --url https://target-site.com --out ./my-clone

# 2. Clone into ALL frameworks simultaneously (React, Vue 3, Svelte 5, HTML):
python clone_any_ui.py --url https://target-site.com --out ./my-clone --all

# 3. Clone from a local HTML file (skips network):
python clone_any_ui.py --file path/to/index.html --out ./my-clone --all

# 4. Ingest live DOM from clipboard (bypasses Cloudflare / CAPTCHA):
python clone_any_ui.py --clipboard --url https://target-site.com --out ./my-clone --all
```
What this produces automatically:
* `site/`: Sanitized, 100% mirrored offline-ready site with all CSS, webfonts, and media.
* `tokens/`: Extracted design & motion tokens (`tokens.json`, `tailwind.config.js`, `tokens.css`, `theme.v4.css`).
* `components/`: Modular React (`.tsx`), Vue (`.vue`), Svelte (`.svelte`), or HTML components with built-in spring physics and hover lifts.
* `preview.html`: Zero-build instant live preview with Tailwind CDN, preconfigured keyframes, and scroll reveal observer.
* `CLONE_REPORT.md`: Master architectural audit report with WCAG 2.1 AA and Motion Parity checklist.

---

### Dedicated Modular Scripts (In `scripts/`)

### A. `extract_micro_details.py` (Master Microscopic Polish Engine)
Extracts and synthesizes sub-pixel microscopic nuances that elevate clones into agency-grade twins:
- **Sub-Pixel Typography**: OpenType `font-feature-settings` (`"tnum"`, `"cv02"`-`"cv11"`), negative tracking down to `-0.025em`, text anti-orphan balancing (`text-wrap: balance` / `pretty`), and sub-pixel hardware antialiasing.
- **Multi-Layer Atmospheric Shading**: Stacked 4-to-5 layer box shadows with 1px inset hairlines and diffuse ambient glow meshes.
- **Tactile Click Physics & Focus**: Active press compression (`scale(0.975) translateY(0.5px)`), accessible double-offset `:focus-visible` rings, and brand `::selection` styling.
- **Sleek Custom Scrollbars & Grain**: Themed thin scrollbars and subtle 2.2% organic SVG tactile grain overlay (`feTurbulence`) for physical realism.
- **Platform Viewport Parity**: iOS & Android mobile safe-area insets (`env(safe-area-inset-bottom)`).
```bash
python scripts/extract_micro_details.py --target-dir ./my-clone --brand-color "#1ed760"
```

### B. `audit_subpixel_fidelity.py` (Sub-Pixel Precision Auditor)
Runs automated verification down to 0.5px tolerances across 10 sub-pixel metrics (antialiasing, OpenType features, stacked shadows, scrollbars, selection, press physics, focus rings, grain, safe-area, reduced motion) and generates an exact Sub-Pixel Micro-Fidelity Score (0-100%).
```bash
python scripts/audit_subpixel_fidelity.py --target-dir ./my-clone
```

### C. `synthesize_interactions.py` (Universal Behavioral Engine)
Reverse-engineers UI roles, state machines, and micro-interactions from cloned pages and injects zero-dependency 60fps client-side interactivity across any website:
- **Audio & Media**: Real sound playback, draggable scrubbers, live time clocks, volume drag, and mute toggles.
- **Live Search & Filtering**: Real-time card/item filtering as the user types with smooth spring transitions.
- **Quantity & Cart**: "+ / -" stepper counters and floating cart badge incrementing.
- **Filter Pills & Tabs**: Active pill switching and category toggling.
- **Interactive Likes & Bookmarks**: Spring bounce (`scale(1.25)` -> `scale(1.0)`), green brand color fill, and toast feedback.
- **Pricing Switcher**: Monthly vs annual billing toggles with discount math.
- **Magnetic Buttons & 3D Tilt**: Magnetic cursor pull and 3D card tilt for creative portfolios.
```bash
python scripts/synthesize_interactions.py --target-dir ./my-clone --brand-color "#1ed760"
```

### D. `self_heal_and_verify.py` (Autonomous Self-Healing & Verification Engine)
Scans, repairs, and guarantees zero-defect codebases before reporting completion:
- **Zero-Syntax-Error Validator**: Runs `node --check` across all extracted and inline JavaScript scripts, auto-repairing orphaned closing braces, mismatched tags, and syntax leaks.
- **Anti-Hotlink Injection**: Guarantees `<meta name="referrer" content="no-referrer">` is inlined in every `<head>`, ensuring images and videos from BunnyCDN, Cloudflare, or AWS never 403 on localhost.
- **Relative Path Normalization**: Resolves root-relative `/assets/` into depth-aware relative links (`./`, `../`, `../../`).
- **Asset Integrity Audit**: Checks 100% of stylesheets, scripts, and local links, reporting 0 missing files.
```bash
python scripts/self_heal_and_verify.py --target-dir ./my-clone
```

### E. `universal_extractor.py` (Anti-Bot & Shadow DOM Extraction Engine)
Captures complex single-page apps (React 19, Next.js, Vue, Angular) and heavy client-side architectures:
- **Headless Chrome Stealth**: Anti-automation flags (`--disable-blink-features=AutomationControlled`), realistic window viewport, and user-agent emulation.
- **Post-Hydration Stabilization**: Waits for client-side frameworks to finish rendering components into the DOM.
- **Recursive Shadow DOM Piercing**: Traverses `#shadow-root` trees and inlines them into clean semantic HTML.
- **Canvas / WebGL Capture**: Grabs active WebGL and Three.js canvas frames as high-res WebP image fallbacks so 3D scenes never render blank.
```bash
python scripts/universal_extractor.py --url https://target-site.com --out ./site/index.html
```

### F. `browser_extract.js` (1-Click DevTools Console Bypass)
When facing impenetrable Cloudflare Turnstile, CAPTCHA, or authenticated dashboard paywalls:
1. Open target URL in your desktop browser.
2. Press <kbd>F12</kbd> -> Console -> Paste `browser_extract.js` -> Press Enter.
3. It inlines SVGs, snapshots canvases, flattens Shadow DOMs, and copies the complete hydrated DOM to your clipboard.
4. Run in your terminal: `python clone_any_ui.py --clipboard --url <site-url> --out ./my-clone --all`.

### B. `extract_motion_physics.py`
Extracts CSS `@keyframes`, transition curves, easing functions, and hover physics from live URLs or stylesheets.
```bash
python scripts/extract_motion_physics.py --url https://target-site.com --out ./motion-tokens
python scripts/extract_motion_physics.py --file ./mirrored/style.css --out ./motion-tokens
```
Outputs:
- `motion.json`: Complete dictionary of `@keyframes`, animations, transitions, and easings.
- `tailwind.motion.config.js`: Plug-and-play `theme.extend.keyframes`, `animation`, and `transitionTimingFunction`.
- `motion.css`: Standalone CSS with `@keyframes`, `.cau-*` classes, and `@media (prefers-reduced-motion: reduce)`.

### B. `extract_design_tokens.py`
Extracts CSS custom properties, HEX/RGB/OKLCH color frequencies, typography rules, border-radii, box-shadows, and motion tokens.
```bash
python scripts/extract_design_tokens.py --url https://target-site.com --out ./design-tokens
python scripts/extract_design_tokens.py --file ./mirrored/style.css --out ./design-tokens
```
Outputs:
- `tokens.json`: Structured design token dictionary including `"motion"` block.
- `tailwind.config.js`: Complete Tailwind `theme.extend` snippet with colors, typography, radii, keyframes, and easings.
- `tokens.css`: Clean `:root` CSS custom properties and `@keyframes`.
- `theme.v4.css`: Tailwind v4 `@theme` configuration.

### C. `mirror_clean_ui.py`
Captures HTML, downloads stylesheets, webfonts, SVGs, and images while stripping tracker scripts (GTM, Meta Pixel, Hotjar, Sentry, Cloudflare challenges).
```bash
python scripts/mirror_clean_ui.py --url https://target-site.com --out ./mirrored-site
```

### D. `componentize_layout.py`
Transforms raw or mirrored HTML into modular components with fluid animations and micro-interactions:
```bash
# React / Next.js (.tsx)
python scripts/componentize_layout.py --input ./mirrored-site/index.html --out ./src/components --format react

# Vue 3 (<script setup> .vue)
python scripts/componentize_layout.py --input ./mirrored-site/index.html --out ./src/components --format vue

# Svelte 5 (.svelte)
python scripts/componentize_layout.py --input ./mirrored-site/index.html --out ./src/components --format svelte

# Semantic Tailwind HTML (.html)
python scripts/componentize_layout.py --input ./mirrored-site/index.html --out ./src/components --format html
```

### E. `compare_visual_parity.py` & `style_snapshot.js`
In-browser snapshot capture and automated drift evaluation (geometry, color, and motion):
```bash
# In browser DevTools / Playwright console:
copy(JSON.stringify(window.cauSnapshot(['h1', 'header', '.hero', '.card', 'button'])))

# In terminal:
python scripts/compare_visual_parity.py --source source.json --copy replica.json --out parity_report.md
```

---

## 4. End-to-End Replication Workflows

### Workflow A: Replicating Animations, Movements & Physics
1. **Extract Keyframes & Easing Curves**:
   - Run `extract_motion_physics.py` on the target site or stylesheet.
   - Inspect custom cubic-bezier curves (e.g. `cubic-bezier(0.16, 1, 0.3, 1)` for Apple/Vercel fluid springs).
   - Check continuous animations: `float` (subtle floating bob), `marquee` (infinite ticker), `pulse-glow` (ambient mesh glow), `shimmer` (gradient loading).
2. **Weave Micro-Interactions into Components**:
   - **Interactive Card Hover**: `group relative overflow-hidden rounded-2xl border border-zinc-200/80 bg-white p-8 shadow-sm transition-all duration-300 ease-out hover:-translate-y-2 hover:shadow-xl hover:border-blue-500/40 dark:border-zinc-800/80 dark:bg-zinc-900`
   - **Icon Rotation & Scale**: `group-hover:scale-110 group-hover:rotate-6 transition-transform duration-300 ease-out`
   - **Card Hover Arrow Slide**: `text-blue-600 opacity-0 -translate-x-2 transition-all duration-300 group-hover:opacity-100 group-hover:translate-x-0`
   - **Magnetic Button Feedback**: `transition-all duration-300 ease-out hover:-translate-y-1 hover:shadow-xl hover:shadow-blue-500/25 active:translate-y-0 active:scale-95`
   - **Animated Underline**: `relative py-1 transition after:absolute after:bottom-0 after:left-0 after:h-[2px] after:w-0 hover:after:w-full after:bg-blue-600 after:transition-all after:duration-300`
3. **Viewport & Scroll Entrance Reveals**:
   - Use `data-cau-animate="fade-up"` or `.cau-reveal` with staggered delays (`[animation-delay:150ms]`, `[animation-delay:300ms]`).
   - The zero-dependency `IntersectionObserver` in `preview.html` reveals sections smoothly as they enter the viewport.
4. **Framer Motion Parity (React / Next.js)**:
   - When requested or utilizing Framer Motion, translate Tailwind classes into `motion.div`:
     ```tsx
     <motion.div
       initial={{ opacity: 0, y: 20 }}
       animate={{ opacity: 1, y: 0 }}
       transition={{ duration: 0.5, ease: [0.16, 1, 0.3, 1] }}
       whileHover={{ y: -6, transition: { duration: 0.2 } }}
       whileTap={{ scale: 0.98 }}
     />
     ```

### Workflow B: Replicating a Live Website's Visual System with New Content
1. **Extract & Lock Tokens**:
   - Run `extract_design_tokens.py --url <URL>`.
   - Inspect primary brand colors, background tints, font family chains, and motion tokens.
   - Configure the workspace `tailwind.config.js` or global CSS variables.
2. **Mirror & Clean the Architecture**:
   - Run `mirror_clean_ui.py --url <URL>` to inspect section hierarchy.
   - Run `componentize_layout.py` to draft modular component skeletons (React, Vue, Svelte, or HTML).
3. **Inject New Semantic Content**:
   - Retain exact DOM layout classes (grid columns, gap sizes, padding, container constraints).
   - Replace headings, copy, and badges with target copy.
   - Keep text lengths balanced to avoid layout shifting or awkward line wrapping.
4. **Audit Visual, Motion & Accessibility Parity**:
   - Check contrast ratios: text must meet 4.5:1 against its background.
   - Test responsive layout at 375px (mobile nav collapsible, cards stacked) and 1280px (full desktop grid).
   - Verify hover transforms and keyframe fluidity run at 60fps without layout jank.

### Workflow C: Exact Media & Video Re-embedding (Zero-Placeholder Guarantee)
1. **Asset Scraper & CDN Bypass**:
   - `mirror_clean_ui.py` detects responsive `srcset`, picture tags, inline background-images, video posters, and `<video>` source tags.
   - Extracts unoptimized high-res URLs from Next.js (`/_next/image?url=...`).
   - Requests images and video streams with spoofed `Referer: <origin_url>` and `Origin` headers to bypass CDN hotlink protections.
   - Promotes lazy-loaded `data-src` / `data-original` attributes to direct `src`.
   - Never injects placeholder boxes or dummy SVGs; if an asset cannot be mirrored locally, it preserves the exact remote URL.
2. **Component Integration**:
   - `componentize_layout.py` inspects extracted images and videos per section:
     - **Header**: Embeds exact logo image asset into the brand anchor.
     - **Hero**: Embeds exact `<video>` clip with autoplay, loop, muted, and playsinline, or hero showcase image.
     - **Features**: Embeds exact cards/illustrations directly in feature cards with hover zoom micro-interactions.
     - **Footer**: Embeds exact footer brand logo.
3. **Local Assets Alignment**:
   - `clone_any_ui.py` mirrors assets to `./assets` at root so both `site/index.html` and `preview.html` display all media with 100% fidelity.

---

## 5. Non-Negotiable Quality Gates (Audit Checklist)

Before concluding any UI replication task, verify:
* [ ] **Semantic Markup**: Exactly one `<h1>` per page; linear heading hierarchy (`h1` → `h2` → `h3`); semantic landmark tags used.
* [ ] **Exact Visual Media**: Exact images and video clips replicated; zero generic placeholder SVG boxes.
* [ ] **Font Fidelity**: Font weights, letter-spacing, and line-heights match source tokens.
* [ ] **Fluid 60fps Motion**: Keyframe animations, cubic-bezier spring physics, and hover lifts without layout thrashing (use `transform` and `opacity` only).
* [ ] **Motion Accessibility (WCAG 2.3.3)**: Full `@media (prefers-reduced-motion: reduce)` override in CSS and Tailwind configs.
* [ ] **No Tracker Bloat**: Zero residual analytics scripts, tracking pixels, or broken third-party module imports.
* [ ] **Responsive Integrity**: No horizontal scrollbar at 375px, 768px, or 1440px viewports.
* [ ] **Accessibility (WCAG AA)**: Focus rings configured on interactive controls (`focus-visible:ring-2`); accessible image alt tags provided.
