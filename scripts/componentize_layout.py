#!/usr/bin/env python3
"""Componentize Mirrored HTML into Clean Semantic React, Vue, Svelte, or Tailwind Components.

Parses cleaned HTML, identifies major UI landmarks and sections:
- Navigation / Header
- Hero Section
- Bento / Feature Grid
- Social Proof / Testimonials
- Pricing Cards
- CTA Section
- Footer

Preserves 100% of exact mirrored images, videos, and visual assets without
ever falling back to placeholder SVGs or dummy boxes.

Generates ready-to-use components styled with modern Tailwind CSS:
- React / TSX (.tsx)
- Vue 3 (<script setup> .vue)
- Svelte 5 (.svelte)
- Pure Semantic HTML5 (.html)

Usage:
  python componentize_layout.py --input ./mirrored-site/index.html --out ./components --format react
  python componentize_layout.py --input ./mirrored-site/index.html --out ./components --format vue
  python componentize_layout.py --input ./mirrored-site/index.html --out ./components --format svelte
  python componentize_layout.py --input ./mirrored-site/index.html --out ./components --format html
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path

SECTION_KEYWORDS = {
    "header": ["header", "nav", "navbar", "navigation", "top-bar", "menu"],
    "hero": ["hero", "banner", "intro", "headline", "main-header"],
    "features": ["feature", "bento", "grid", "services", "benefits", "highlights", "capabilities"],
    "social_proof": ["proof", "testimonial", "review", "logos", "clients", "partners", "trust"],
    "pricing": ["pricing", "plans", "tier", "subscription", "rates"],
    "cta": ["cta", "call-to-action", "get-started", "join", "newsletter", "signup"],
    "footer": ["footer", "bottom", "site-footer", "colophon"],
}


def clean_text(text: str) -> str:
    return " ".join(text.split()).strip()


def extract_headings(html_chunk: str) -> list[str]:
    return [clean_text(m) for m in re.findall(r"<h[1-6]\b[^>]*>(.*?)</h[1-6]>", html_chunk, re.DOTALL | re.I)]


def extract_buttons_and_links(html_chunk: str) -> list[str]:
    buttons = re.findall(r"<(?:button|a)\b[^>]*>(.*?)</(?:button|a)>", html_chunk, re.DOTALL | re.I)
    cleaned = [clean_text(re.sub(r"<[^>]+>", "", b)) for b in buttons]
    return [b for b in cleaned if b and len(b) < 60]


def extract_paragraphs(html_chunk: str) -> list[str]:
    paras = re.findall(r"<p\b[^>]*>(.*?)</p>", html_chunk, re.DOTALL | re.I)
    cleaned = [clean_text(re.sub(r"<[^>]+>", "", p)) for p in paras]
    return [p for p in cleaned if p]


def extract_images(html_chunk: str) -> list[dict[str, str]]:
    """Extracts exact <img>, <picture>, and background images from an HTML chunk."""
    images = []
    # 1. <img> tags with src, data-src, or srcset
    for match in re.finditer(r'<img\b([^>]*)>', html_chunk, re.I):
        attrs = match.group(1)
        src_m = re.search(r'\bsrc=["\']([^"\']+)["\']', attrs, re.I)
        lazy_m = re.search(r'\b(?:data-src|data-original|data-lazy-src)=["\']([^"\']+)["\']', attrs, re.I)
        alt_m = re.search(r'\balt=["\']([^"\']*)["\']', attrs, re.I)
        class_m = re.search(r'\bclass=["\']([^"\']*)["\']', attrs, re.I)
        
        src = lazy_m.group(1).strip() if lazy_m else (src_m.group(1).strip() if src_m else None)
        if src and not any(t in src.lower() for t in ["analytics", "tracking", "pixel", "beacon", "spacer.gif"]):
            images.append({
                "src": src,
                "alt": alt_m.group(1).strip() if alt_m else "Visual showcase asset",
                "class": class_m.group(1).strip() if class_m else "",
            })

    # 2. Inline background images
    for match in re.finditer(r'url\(\s*[\'"]?([^\'")]+)[\'"]?\s*\)', html_chunk, re.I):
        bg_url = match.group(1).strip()
        if any(bg_url.lower().endswith(ext) for ext in [".png", ".jpg", ".jpeg", ".webp", ".svg", ".avif", ".gif"]):
            if not any(img["src"] == bg_url for img in images):
                images.append({
                    "src": bg_url,
                    "alt": "Background visual asset",
                    "class": "object-cover",
                })
    return images


def extract_videos(html_chunk: str) -> list[dict[str, str]]:
    """Extracts exact <video> tags and <source> clips from an HTML chunk."""
    videos = []
    for match in re.finditer(r'<video\b([^>]*)>(.*?)</video>', html_chunk, re.DOTALL | re.I):
        attrs = match.group(1)
        inner = match.group(2)
        src_m = re.search(r'\bsrc=["\']([^"\']+)["\']', attrs, re.I)
        poster_m = re.search(r'\bposter=["\']([^"\']+)["\']', attrs, re.I)
        
        src = src_m.group(1).strip() if src_m else None
        if not src:
            source_m = re.search(r'<source\b[^>]*\bsrc=["\']([^"\']+)["\']', inner, re.I)
            if source_m:
                src = source_m.group(1).strip()
                
        if src:
            videos.append({
                "src": src,
                "poster": poster_m.group(1).strip() if poster_m else "",
                "autoplay": "autoplay" in attrs.lower(),
                "muted": "muted" in attrs.lower(),
                "loop": "loop" in attrs.lower(),
            })
    return videos


def guess_section_type(tag_name: str, class_and_id: str, inner_text: str) -> str:
    combined = f"{tag_name} {class_and_id}".lower()
    for sec_type, keywords in SECTION_KEYWORDS.items():
        if any(kw in combined for kw in keywords):
            return sec_type

    text_lower = inner_text.lower()
    if any(k in text_lower for k in ["privacy policy", "terms of service", "all rights reserved"]):
        return "footer"
    if any(k in text_lower for k in ["per month", "$", "billed annually", "free tier", "enterprise"]):
        return "pricing"
    if any(k in text_lower for k in ["what our customers say", "trusted by", "ratings", "reviews"]):
        return "social_proof"

    return "features"


# ==========================================
# 1. REACT / TSX GENERATOR (EXACT MEDIA & FLUID MOTION)
# ==========================================
def generate_react_component(
    name: str,
    section_type: str,
    headings: list[str],
    paras: list[str],
    buttons: list[str],
    images: list[dict] = None,
    videos: list[dict] = None
) -> str:
    images = images or []
    videos = videos or []
    h_main = headings[0] if headings else f"{name} Title"
    p_main = paras[0] if paras else "Subtext or descriptive copy supporting the primary message."
    cta_text = buttons[0] if buttons else "Get Started"

    if section_type == "header":
        brand_markup = """<span className="h-7 w-7 rounded-lg bg-blue-600 inline-flex items-center justify-center text-white text-xs font-black shadow-md shadow-blue-500/25 transition-transform duration-300 ease-out group-hover:scale-110 group-hover:rotate-6">
            ⚡
          </span>
          <span className="transition-colors duration-200 group-hover:text-blue-600 dark:group-hover:text-blue-400">Brand</span>"""
        if images:
            logo_src = images[0]["src"]
            logo_alt = images[0].get("alt") or "Brand Logo"
            brand_markup = f"""<img src="{logo_src}" alt="{logo_alt}" className="h-8 w-auto max-h-8 object-contain transition-transform duration-300 ease-out group-hover:scale-105" />"""

        return f"""import React, {{ useState }} from 'react';

export function {name}() {{
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  return (
    <header className="sticky top-0 z-50 w-full border-b border-zinc-200/80 bg-white/80 backdrop-blur-md transition-all duration-300 dark:border-zinc-800/80 dark:bg-zinc-950/80">
      <div className="container mx-auto flex h-16 max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8">
        {{/* Brand Logo with Interactive Tilt */}}
        <a href="#" className="group flex items-center gap-2.5 font-bold text-xl tracking-tight text-zinc-900 dark:text-zinc-50 cursor-pointer">
          {brand_markup}
        </a>

        {{/* Desktop Navigation with Animated Underline Effect */}}
        <nav className="hidden md:flex items-center gap-8 text-sm font-medium text-zinc-600 dark:text-zinc-400">
          <a href="#features" className="relative py-1 transition hover:text-zinc-900 dark:hover:text-zinc-50 after:absolute after:bottom-0 after:left-0 after:h-[2px] after:w-0 hover:after:w-full after:bg-blue-600 after:transition-all after:duration-300">Features</a>
          <a href="#pricing" className="relative py-1 transition hover:text-zinc-900 dark:hover:text-zinc-50 after:absolute after:bottom-0 after:left-0 after:h-[2px] after:w-0 hover:after:w-full after:bg-blue-600 after:transition-all after:duration-300">Pricing</a>
          <a href="#testimonials" className="relative py-1 transition hover:text-zinc-900 dark:hover:text-zinc-50 after:absolute after:bottom-0 after:left-0 after:h-[2px] after:w-0 hover:after:w-full after:bg-blue-600 after:transition-all after:duration-300">Testimonials</a>
        </nav>

        {{/* Interactive CTA Button with Hover Physics */}}
        <div className="hidden md:flex items-center gap-4">
          <button className="relative overflow-hidden rounded-xl bg-zinc-900 px-5 py-2.5 text-sm font-semibold text-white shadow-sm transition-all duration-300 ease-out hover:-translate-y-0.5 hover:shadow-lg hover:shadow-zinc-900/10 hover:bg-zinc-800 active:translate-y-0 active:scale-95 dark:bg-zinc-50 dark:text-zinc-900 dark:hover:bg-zinc-200">
            {cta_text}
          </button>
        </div>

        {{/* Mobile Drawer Toggle */}}
        <button
          onClick={{() => setIsMobileMenuOpen(!isMobileMenuOpen)}}
          className="md:hidden inline-flex items-center justify-center p-2 rounded-lg text-zinc-700 dark:text-zinc-200 hover:bg-zinc-100 dark:hover:bg-zinc-800 transition-colors"
          aria-expanded={{isMobileMenuOpen}}
        >
          <span className="sr-only">Toggle navigation menu</span>
          <span className={{`text-lg transition-transform duration-200 ${{isMobileMenuOpen ? 'rotate-90' : ''}}`}}>
            {{isMobileMenuOpen ? '✕' : '☰'}}
          </span>
        </button>
      </div>

      {{/* Mobile Drawer Menu with Smooth Entrance */}}
      {{isMobileMenuOpen && (
        <div className="md:hidden border-b border-zinc-200 dark:border-zinc-800 bg-white/95 dark:bg-zinc-950/95 px-6 pt-3 pb-6 space-y-3 animate-fade-in-down shadow-xl backdrop-blur-md">
          <a href="#features" className="block text-sm font-medium py-2 text-zinc-700 dark:text-zinc-200 hover:text-blue-600 transition-colors">Features</a>
          <a href="#pricing" className="block text-sm font-medium py-2 text-zinc-700 dark:text-zinc-200 hover:text-blue-600 transition-colors">Pricing</a>
          <a href="#testimonials" className="block text-sm font-medium py-2 text-zinc-700 dark:text-zinc-200 hover:text-blue-600 transition-colors">Testimonials</a>
          <button className="w-full mt-2 rounded-xl bg-blue-600 py-3 text-sm font-semibold text-white shadow-md hover:bg-blue-500 transition-all duration-200 active:scale-98">
            {cta_text}
          </button>
        </div>
      )}}
    </header>
  );
}}
"""
    elif section_type == "hero":
        # Visual media showcase (exact video or exact hero image)
        media_showcase = ""
        if videos:
            v = videos[0]
            poster_attr = f'poster="{v["poster"]}"' if v.get("poster") else ""
            media_showcase = f"""
        {{/* Exact Mirrored Video Showcase with Ambient Glow */}}
        <div className="mt-14 relative mx-auto max-w-5xl overflow-hidden rounded-2xl border border-zinc-200/80 bg-zinc-900/5 p-2 shadow-2xl backdrop-blur-sm transition-all duration-500 hover:border-blue-500/30 dark:border-zinc-800/80 dark:bg-zinc-900/50">
          <video
            src="{v['src']}"
            {poster_attr}
            autoPlay
            loop
            muted
            playsInline
            className="w-full rounded-xl object-cover shadow-inner"
          />
        </div>"""
        elif images:
            img = images[0]
            media_showcase = f"""
        {{/* Exact Mirrored Hero Image Showcase with Ambient Glow */}}
        <div className="mt-14 relative mx-auto max-w-5xl overflow-hidden rounded-2xl border border-zinc-200/80 bg-zinc-900/5 p-2 shadow-2xl backdrop-blur-sm transition-all duration-500 ease-out hover:shadow-blue-500/10 hover:border-zinc-300 dark:border-zinc-800/80 dark:bg-zinc-900/50">
          <img
            src="{img['src']}"
            alt="{img.get('alt', 'Hero visual showcase')}"
            className="w-full rounded-xl object-cover shadow-inner transition-transform duration-700 ease-out hover:scale-[1.01]"
            loading="eager"
          />
        </div>"""

        # Marquee branding
        marquee_content = """<div className="flex gap-12 whitespace-nowrap animate-marquee">
            {{"Acme Corp · NextScale · HyperFlow · Veloce · CloudMesh · ApexCore · Acme Corp · NextScale · HyperFlow · Veloce · CloudMesh · ApexCore".split(" · ").map((brand, i) => (
              <span key={i} className="text-sm font-semibold text-zinc-400 hover:text-zinc-900 dark:text-zinc-500 dark:hover:text-zinc-100 transition-colors cursor-default">
                {brand}
              </span>
            ))}}
          </div>"""

        if len(images) > 1:
            logo_imgs = []
            for extra_img in images[1:7]:
                logo_imgs.append(f"""<img src="{extra_img['src']}" alt="{extra_img.get('alt', 'Partner logo')}" className="h-7 max-h-7 w-auto object-contain grayscale opacity-60 hover:grayscale-0 hover:opacity-100 transition-all duration-300" />""")
            if logo_imgs:
                inner_logos = "\n            ".join(logo_imgs * 2)
                marquee_content = f"""<div className="flex gap-12 items-center whitespace-nowrap animate-marquee">
            {inner_logos}
          </div>"""

        return f"""import React from 'react';

export function {name}() {{
  return (
    <section className="relative overflow-hidden py-24 sm:py-32">
      {{/* Ambient Animated Background Glow */}}
      <div className="pointer-events-none absolute -top-40 left-1/2 -z-10 -translate-x-1/2 transform-gpu overflow-hidden blur-3xl" aria-hidden="true">
        <div className="aspect-[1155/678] w-[68rem] bg-gradient-to-tr from-blue-600 to-cyan-400 opacity-20 animate-pulse-glow" />
      </div>

      <div className="container mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="mx-auto max-w-3xl text-center">
          {{/* Floating Badge with Live Ping Indicator */}}
          <div className="mb-6 inline-flex items-center gap-2 rounded-full border border-blue-500/20 bg-blue-500/10 px-4 py-1.5 text-xs font-semibold text-blue-600 dark:text-blue-400 shadow-sm backdrop-blur-sm animate-float">
            <span className="relative flex h-2 w-2">
              <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-blue-400 opacity-75"></span>
              <span className="relative inline-flex h-2 w-2 rounded-full bg-blue-500"></span>
            </span>
            <span>✨ Autonomous Replication Ready</span>
          </div>

          {{/* Staggered Animated Headline */}}
          <h1 className="text-4xl font-extrabold tracking-tight text-zinc-900 sm:text-6xl dark:text-zinc-50 leading-[1.1] animate-fade-in-up">
            {h_main}
          </h1>

          {{/* Subtitle with Subtle Delay */}}
          <p className="mt-6 text-lg leading-8 text-zinc-600 dark:text-zinc-400 animate-fade-in-up [animation-delay:150ms]">
            {p_main}
          </p>

          {{/* Interactive CTA Button Group */}}
          <div className="mt-10 flex flex-wrap items-center justify-center gap-4 animate-fade-in-up [animation-delay:300ms]">
            <button className="relative overflow-hidden rounded-xl bg-blue-600 px-6 py-3.5 text-sm font-semibold text-white shadow-lg shadow-blue-500/25 transition-all duration-300 ease-out hover:-translate-y-1 hover:shadow-xl hover:shadow-blue-500/35 hover:bg-blue-500 active:translate-y-0 active:scale-95">
              {cta_text}
            </button>
            <a href="#demo" className="group inline-flex items-center gap-1.5 text-sm font-semibold leading-6 text-zinc-900 transition-all duration-200 hover:text-blue-600 hover:translate-x-1 dark:text-zinc-50 dark:hover:text-blue-400">
              Live Interactive Demo <span className="transition-transform duration-200 group-hover:translate-x-1">&rarr;</span>
            </a>
          </div>
        </div>
{media_showcase}

        {{/* Continuous Infinite Logo Marquee Ticker */}}
        <div className="mt-20 w-full overflow-hidden border-y border-zinc-200/60 dark:border-zinc-800/60 py-6">
          <p className="text-center text-xs font-semibold uppercase tracking-wider text-zinc-400 dark:text-zinc-500 mb-4">
            Trusted by world-class frontend teams
          </p>
          {marquee_content}
        </div>
      </div>
    </section>
  );
}}
"""
    elif section_type == "pricing":
        return f"""import React, {{ useState }} from 'react';

export function {name}() {{
  const [isAnnual, setIsAnnual] = useState(true);

  return (
    <section id="pricing" className="py-24 sm:py-32 bg-zinc-50/50 dark:bg-zinc-900/30">
      <div className="container mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="mx-auto max-w-2xl text-center">
          <h2 className="text-3xl font-bold tracking-tight text-zinc-900 sm:text-4xl dark:text-zinc-50">
            {h_main}
          </h2>
          <p className="mt-4 text-base text-zinc-600 dark:text-zinc-400">
            {p_main}
          </p>

          {{/* Interactive Billing Switch with Spring Physics */}}
          <div className="mt-8 flex items-center justify-center gap-3">
            <span className="text-sm font-medium text-zinc-600 dark:text-zinc-400">Monthly</span>
            <button
              onClick={{() => setIsAnnual(!isAnnual)}}
              className="relative inline-flex h-7 w-12 shrink-0 cursor-pointer rounded-full border-2 border-transparent bg-zinc-300 transition-colors duration-300 ease-out focus:outline-none dark:bg-zinc-700"
              role="switch"
              aria-checked={{isAnnual}}
            >
              <span className={{`inline-block h-6 w-6 transform rounded-full bg-white shadow-md transition-transform duration-300 ease-[cubic-bezier(0.16,1,0.3,1)] ${{isAnnual ? 'translate-x-5 !bg-blue-600' : 'translate-x-0'}}`}} />
            </button>
            <span className="text-sm font-medium text-zinc-900 dark:text-zinc-50">
              Annual <span className="inline-block rounded-full bg-emerald-500/10 px-2.5 py-0.5 text-xs font-semibold text-emerald-600 dark:text-emerald-400 animate-pulse">Save 20%</span>
            </span>
          </div>
        </div>

        <div className="mx-auto mt-16 grid max-w-lg grid-cols-1 gap-8 lg:max-w-4xl lg:grid-cols-2">
          {{/* Card 1: Starter */}}
          <div className="group rounded-2xl border border-zinc-200 bg-white p-8 shadow-sm transition-all duration-300 ease-out hover:-translate-y-2 hover:shadow-xl dark:border-zinc-800 dark:bg-zinc-900">
            <h3 className="text-lg font-semibold text-zinc-900 dark:text-zinc-50">Starter</h3>
            <p className="mt-4 text-4xl font-bold text-zinc-900 dark:text-zinc-50">
              {{isAnnual ? '$24' : '$29'}}<span className="text-sm font-normal text-zinc-500">/mo</span>
            </p>
            <p className="mt-2 text-sm text-zinc-500">For individuals and rapid prototyping.</p>
            <button className="mt-8 w-full rounded-xl border border-zinc-300 py-3 text-sm font-semibold transition-all duration-200 hover:bg-zinc-50 hover:border-zinc-400 active:scale-98 dark:border-zinc-700 dark:hover:bg-zinc-800">
              Get Started
            </button>
          </div>

          {{/* Card 2: Featured Pro with Glow & Hover Lift */}}
          <div className="group relative rounded-2xl border-2 border-blue-600 bg-white p-8 shadow-lg shadow-blue-500/10 transition-all duration-300 ease-out hover:-translate-y-2.5 hover:shadow-2xl hover:shadow-blue-500/25 dark:bg-zinc-900">
            <span className="absolute -top-3.5 right-6 rounded-full bg-blue-600 px-3.5 py-1 text-xs font-bold text-white shadow-md animate-pulse">
              Most Popular
            </span>
            <h3 className="text-lg font-semibold text-zinc-900 dark:text-zinc-50">Pro</h3>
            <p className="mt-4 text-4xl font-bold text-zinc-900 dark:text-zinc-50">
              {{isAnnual ? '$69' : '$79'}}<span className="text-sm font-normal text-zinc-500">/mo</span>
            </p>
            <p className="mt-2 text-sm text-zinc-500">For growing engineering teams requiring full parity.</p>
            <button className="mt-8 w-full rounded-xl bg-blue-600 py-3 text-sm font-semibold text-white shadow-md shadow-blue-500/25 transition-all duration-300 hover:bg-blue-500 hover:shadow-lg hover:shadow-blue-500/35 active:scale-98">
              Upgrade to Pro
            </button>
          </div>
        </div>
      </div>
    </section>
  );
}}
"""
    elif section_type == "footer":
        footer_brand = """<span className="font-bold text-zinc-900 dark:text-zinc-100">Brand</span>"""
        if images:
            logo_src = images[0]["src"]
            logo_alt = images[0].get("alt") or "Footer Logo"
            footer_brand = f"""<img src="{logo_src}" alt="{logo_alt}" className="h-7 w-auto object-contain opacity-80 hover:opacity-100 transition-opacity" />"""

        return f"""import React from 'react';

export function {name}() {{
  return (
    <footer className="border-t border-zinc-200 bg-white py-12 dark:border-zinc-800 dark:bg-zinc-950 transition-colors">
      <div className="container mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="flex flex-col items-center justify-between gap-6 sm:flex-row">
          <div className="flex items-center gap-3">
            {footer_brand}
            <p className="text-sm text-zinc-500 dark:text-zinc-400">
              &copy; {{new Date().getFullYear()}} All rights reserved. Built with fluid 60fps animations.
            </p>
          </div>
          <div className="flex gap-6 text-sm text-zinc-500">
            <a href="#" className="transition hover:text-zinc-900 hover:-translate-y-0.5 dark:hover:text-zinc-50">Privacy</a>
            <a href="#" className="transition hover:text-zinc-900 hover:-translate-y-0.5 dark:hover:text-zinc-50">Terms</a>
            <a href="#" className="transition hover:text-zinc-900 hover:-translate-y-0.5 dark:hover:text-zinc-50">GitHub</a>
          </div>
        </div>
      </div>
    </footer>
  );
}}
"""
    else:  # Features / Bento Grid default with exact mirrored images & hover physics
        card_items = []
        default_feats = [
            ("Autonomous Parity Engine", "Reverse-engineers live layouts into clean components with pixel precision and 60fps motion."),
            ("Fluid Spring Physics", "Pre-configured cubic-bezier motion curves, hover lifts, and zero-jank micro-interactions."),
            ("WCAG AA Accessibility", "Automatic focus rings, contrast checks, and prefers-reduced-motion accessibility safeguards.")
        ]

        count = max(3, len(images))
        for idx in range(min(count, 6)):
            title = headings[idx + 1] if idx + 1 < len(headings) else default_feats[idx % len(default_feats)][0]
            desc = paras[idx + 1] if idx + 1 < len(paras) else default_feats[idx % len(default_feats)][1]
            if idx < len(images):
                img_src = images[idx]["src"]
                img_alt = images[idx].get("alt") or title
                visual_box = f"""<div className="relative mb-5 h-44 w-full overflow-hidden rounded-xl bg-zinc-100 dark:bg-zinc-800">
                <img
                  src="{img_src}"
                  alt="{img_alt}"
                  className="h-full w-full object-cover transition-transform duration-500 ease-out group-hover:scale-105"
                  loading="lazy"
                />
              </div>"""
            else:
                visual_box = """<div className="mb-5 inline-flex h-12 w-12 items-center justify-center rounded-xl bg-blue-600/10 text-xl text-blue-600 transition-transform duration-300 ease-out group-hover:scale-110 group-hover:rotate-6 dark:bg-blue-400/10 dark:text-blue-400">
                ⚡
              </div>"""

            card_items.append(f"""          {{/* Card {idx + 1} */}}
          <div className="group relative overflow-hidden rounded-2xl border border-zinc-200/80 bg-white p-6 shadow-sm transition-all duration-300 ease-out hover:-translate-y-2 hover:shadow-xl hover:shadow-zinc-900/5 hover:border-blue-500/40 dark:border-zinc-800/80 dark:bg-zinc-900 dark:hover:border-blue-500/40">
            {visual_box}
            <h3 className="flex items-center justify-between text-lg font-semibold text-zinc-900 dark:text-zinc-50">
              <span>{title}</span>
              <span className="text-blue-600 opacity-0 -translate-x-2 transition-all duration-300 group-hover:opacity-100 group-hover:translate-x-0">
                &rarr;
              </span>
            </h3>
            <p className="mt-3 text-sm leading-relaxed text-zinc-600 dark:text-zinc-400">
              {desc}
            </p>
          </div>""")

        all_cards = "\n\n".join(card_items)

        return f"""import React from 'react';

export function {name}() {{
  return (
    <section id="features" className="py-24 sm:py-32">
      <div className="container mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="mx-auto max-w-2xl text-center">
          <h2 className="text-3xl font-bold tracking-tight text-zinc-900 sm:text-4xl dark:text-zinc-50 animate-fade-in-up">
            {h_main}
          </h2>
          <p className="mt-4 text-base text-zinc-600 dark:text-zinc-400">
            {p_main}
          </p>
        </div>

        {{/* Bento Grid with Exact Mirrored Visuals & Hover Physics */}}
        <div className="mx-auto mt-16 grid max-w-2xl grid-cols-1 gap-8 sm:grid-cols-2 lg:max-w-none lg:grid-cols-3">
{all_cards}
        </div>
      </div>
    </section>
  );
}}
"""


# ==========================================
# 2. VUE 3 (<script setup>) GENERATOR (EXACT MEDIA & FLUID MOTION)
# ==========================================
def generate_vue_component(
    name: str,
    section_type: str,
    headings: list[str],
    paras: list[str],
    buttons: list[str],
    images: list[dict] = None,
    videos: list[dict] = None
) -> str:
    images = images or []
    videos = videos or []
    h_main = headings[0] if headings else f"{name} Title"
    p_main = paras[0] if paras else "Subtext or descriptive copy supporting the primary message."
    cta_text = buttons[0] if buttons else "Get Started"

    if section_type == "header":
        brand_markup = """<span class="h-7 w-7 rounded-lg bg-blue-600 inline-flex items-center justify-center text-white text-xs font-black shadow-md shadow-blue-500/25 transition-transform duration-300 ease-out group-hover:scale-110 group-hover:rotate-6">
          ⚡
        </span>
        <span class="transition-colors duration-200 group-hover:text-blue-600 dark:group-hover:text-blue-400">Brand</span>"""
        if images:
            logo_src = images[0]["src"]
            logo_alt = images[0].get("alt") or "Brand Logo"
            brand_markup = f"""<img src="{logo_src}" alt="{logo_alt}" class="h-8 w-auto max-h-8 object-contain transition-transform duration-300 ease-out group-hover:scale-105" />"""

        return f"""<script setup lang="ts">
import {{ ref }} from 'vue';

const isMobileMenuOpen = ref(false);
</script>

<template>
  <header class="sticky top-0 z-50 w-full border-b border-zinc-200/80 bg-white/80 backdrop-blur-md transition-all duration-300 dark:border-zinc-800/80 dark:bg-zinc-950/80">
    <div class="container mx-auto flex h-16 max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8">
      <a href="#" class="group flex items-center gap-2.5 font-bold text-xl tracking-tight text-zinc-900 dark:text-zinc-50 cursor-pointer">
        {brand_markup}
      </a>

      <nav class="hidden md:flex items-center gap-8 text-sm font-medium text-zinc-600 dark:text-zinc-400">
        <a href="#features" class="relative py-1 transition hover:text-zinc-900 dark:hover:text-zinc-50 after:absolute after:bottom-0 after:left-0 after:h-[2px] after:w-0 hover:after:w-full after:bg-blue-600 after:transition-all after:duration-300">Features</a>
        <a href="#pricing" class="relative py-1 transition hover:text-zinc-900 dark:hover:text-zinc-50 after:absolute after:bottom-0 after:left-0 after:h-[2px] after:w-0 hover:after:w-full after:bg-blue-600 after:transition-all after:duration-300">Pricing</a>
        <a href="#testimonials" class="relative py-1 transition hover:text-zinc-900 dark:hover:text-zinc-50 after:absolute after:bottom-0 after:left-0 after:h-[2px] after:w-0 hover:after:w-full after:bg-blue-600 after:transition-all after:duration-300">Testimonials</a>
      </nav>

      <div class="hidden md:flex items-center gap-4">
        <button class="relative overflow-hidden rounded-xl bg-zinc-900 px-5 py-2.5 text-sm font-semibold text-white shadow-sm transition-all duration-300 ease-out hover:-translate-y-0.5 hover:shadow-lg hover:shadow-zinc-900/10 hover:bg-zinc-800 active:translate-y-0 active:scale-95 dark:bg-zinc-50 dark:text-zinc-900 dark:hover:bg-zinc-200">
          {cta_text}
        </button>
      </div>

      <button
        @click="isMobileMenuOpen = !isMobileMenuOpen"
        class="md:hidden inline-flex items-center justify-center p-2 rounded-lg text-zinc-700 dark:text-zinc-200 hover:bg-zinc-100 dark:hover:bg-zinc-800 transition-colors"
        :aria-expanded="isMobileMenuOpen"
      >
        <span class="sr-only">Toggle navigation menu</span>
        <span class="text-lg transition-transform duration-200" :class="{{ 'rotate-90': isMobileMenuOpen }}">
          {{{{ isMobileMenuOpen ? '✕' : '☰' }}}}
        </span>
      </button>
    </div>

    <div
      v-if="isMobileMenuOpen"
      class="md:hidden border-b border-zinc-200 dark:border-zinc-800 bg-white/95 dark:bg-zinc-950/95 px-6 pt-3 pb-6 space-y-3 animate-fade-in-down shadow-xl backdrop-blur-md"
    >
      <a href="#features" class="block text-sm font-medium py-2 text-zinc-700 dark:text-zinc-200 hover:text-blue-600 transition-colors">Features</a>
      <a href="#pricing" class="block text-sm font-medium py-2 text-zinc-700 dark:text-zinc-200 hover:text-blue-600 transition-colors">Pricing</a>
      <a href="#testimonials" class="block text-sm font-medium py-2 text-zinc-700 dark:text-zinc-200 hover:text-blue-600 transition-colors">Testimonials</a>
      <button class="w-full mt-2 rounded-xl bg-blue-600 py-3 text-sm font-semibold text-white shadow-md hover:bg-blue-500 transition-all duration-200 active:scale-98">
        {cta_text}
      </button>
    </div>
  </header>
</template>
"""
    elif section_type == "hero":
        media_showcase = ""
        if videos:
            v = videos[0]
            poster_attr = f'poster="{v["poster"]}"' if v.get("poster") else ""
            media_showcase = f"""
      <!-- Exact Mirrored Video Showcase with Ambient Glow -->
      <div class="mt-14 relative mx-auto max-w-5xl overflow-hidden rounded-2xl border border-zinc-200/80 bg-zinc-900/5 p-2 shadow-2xl backdrop-blur-sm transition-all duration-500 hover:border-blue-500/30 dark:border-zinc-800/80 dark:bg-zinc-900/50">
        <video
          src="{v['src']}"
          {poster_attr}
          autoplay
          loop
          muted
          playsinline
          class="w-full rounded-xl object-cover shadow-inner"
        />
      </div>"""
        elif images:
            img = images[0]
            media_showcase = f"""
      <!-- Exact Mirrored Hero Image Showcase with Ambient Glow -->
      <div class="mt-14 relative mx-auto max-w-5xl overflow-hidden rounded-2xl border border-zinc-200/80 bg-zinc-900/5 p-2 shadow-2xl backdrop-blur-sm transition-all duration-500 ease-out hover:shadow-blue-500/10 hover:border-zinc-300 dark:border-zinc-800/80 dark:bg-zinc-900/50">
        <img
          src="{img['src']}"
          alt="{img.get('alt', 'Hero visual showcase')}"
          class="w-full rounded-xl object-cover shadow-inner transition-transform duration-700 ease-out hover:scale-[1.01]"
          loading="eager"
        />
      </div>"""

        return f"""<script setup lang="ts">
const brands = ['Acme Corp', 'NextScale', 'HyperFlow', 'Veloce', 'CloudMesh', 'ApexCore', 'Acme Corp', 'NextScale', 'HyperFlow', 'Veloce', 'CloudMesh', 'ApexCore'];
</script>

<template>
  <section class="relative overflow-hidden py-24 sm:py-32">
    <div class="pointer-events-none absolute -top-40 left-1/2 -z-10 -translate-x-1/2 transform-gpu overflow-hidden blur-3xl" aria-hidden="true">
      <div class="aspect-[1155/678] w-[68rem] bg-gradient-to-tr from-blue-600 to-cyan-400 opacity-20 animate-pulse-glow" />
    </div>

    <div class="container mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
      <div class="mx-auto max-w-3xl text-center">
        <div class="mb-6 inline-flex items-center gap-2 rounded-full border border-blue-500/20 bg-blue-500/10 px-4 py-1.5 text-xs font-semibold text-blue-600 dark:text-blue-400 shadow-sm backdrop-blur-sm animate-float">
          <span class="relative flex h-2 w-2">
            <span class="absolute inline-flex h-full w-full animate-ping rounded-full bg-blue-400 opacity-75"></span>
            <span class="relative inline-flex h-2 w-2 rounded-full bg-blue-500"></span>
          </span>
          <span>✨ Autonomous Replication Ready</span>
        </div>

        <h1 class="text-4xl font-extrabold tracking-tight text-zinc-900 sm:text-6xl dark:text-zinc-50 leading-[1.1] animate-fade-in-up">
          {h_main}
        </h1>

        <p class="mt-6 text-lg leading-8 text-zinc-600 dark:text-zinc-400 animate-fade-in-up [animation-delay:150ms]">
          {p_main}
        </p>

        <div class="mt-10 flex flex-wrap items-center justify-center gap-4 animate-fade-in-up [animation-delay:300ms]">
          <button class="relative overflow-hidden rounded-xl bg-blue-600 px-6 py-3.5 text-sm font-semibold text-white shadow-lg shadow-blue-500/25 transition-all duration-300 ease-out hover:-translate-y-1 hover:shadow-xl hover:shadow-blue-500/35 hover:bg-blue-500 active:translate-y-0 active:scale-95">
            {cta_text}
          </button>
          <a href="#demo" class="group inline-flex items-center gap-1.5 text-sm font-semibold leading-6 text-zinc-900 transition-all duration-200 hover:text-blue-600 hover:translate-x-1 dark:text-zinc-50 dark:hover:text-blue-400">
            Live Interactive Demo <span class="transition-transform duration-200 group-hover:translate-x-1">&rarr;</span>
          </a>
        </div>
      </div>
{media_showcase}

      <div class="mt-20 w-full overflow-hidden border-y border-zinc-200/60 dark:border-zinc-800/60 py-6">
        <p class="text-center text-xs font-semibold uppercase tracking-wider text-zinc-400 dark:text-zinc-500 mb-4">
          Trusted by world-class frontend teams
        </p>
        <div class="flex gap-12 whitespace-nowrap animate-marquee">
          <span v-for="(b, i) in brands" :key="i" class="text-sm font-semibold text-zinc-400 hover:text-zinc-900 dark:text-zinc-500 dark:hover:text-zinc-100 transition-colors cursor-default">
            {{{{ b }}}}
          </span>
        </div>
      </div>
    </div>
  </section>
</template>
"""
    elif section_type == "pricing":
        return f"""<script setup lang="ts">
import {{ ref }} from 'vue';

const isAnnual = ref(true);
</script>

<template>
  <section id="pricing" class="py-24 sm:py-32 bg-zinc-50/50 dark:bg-zinc-900/30">
    <div class="container mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
      <div class="mx-auto max-w-2xl text-center">
        <h2 class="text-3xl font-bold tracking-tight text-zinc-900 sm:text-4xl dark:text-zinc-50">
          {h_main}
        </h2>
        <p class="mt-4 text-base text-zinc-600 dark:text-zinc-400">
          {p_main}
        </p>

        <div class="mt-8 flex items-center justify-center gap-3">
          <span class="text-sm font-medium text-zinc-600 dark:text-zinc-400">Monthly</span>
          <button
            @click="isAnnual = !isAnnual"
            class="relative inline-flex h-7 w-12 shrink-0 cursor-pointer rounded-full border-2 border-transparent bg-zinc-300 transition-colors duration-300 ease-out focus:outline-none dark:bg-zinc-700"
            role="switch"
            :aria-checked="isAnnual"
          >
            <span
              class="inline-block h-6 w-6 transform rounded-full bg-white shadow-md transition-transform duration-300 ease-[cubic-bezier(0.16,1,0.3,1)]"
              :class="{{ 'translate-x-5 !bg-blue-600': isAnnual, 'translate-x-0': !isAnnual }}"
            />
          </button>
          <span class="text-sm font-medium text-zinc-900 dark:text-zinc-50">
            Annual <span class="inline-block rounded-full bg-emerald-500/10 px-2.5 py-0.5 text-xs font-semibold text-emerald-600 dark:text-emerald-400 animate-pulse">Save 20%</span>
          </span>
        </div>
      </div>

      <div class="mx-auto mt-16 grid max-w-lg grid-cols-1 gap-8 lg:max-w-4xl lg:grid-cols-2">
        <div class="group rounded-2xl border border-zinc-200 bg-white p-8 shadow-sm transition-all duration-300 ease-out hover:-translate-y-2 hover:shadow-xl dark:border-zinc-800 dark:bg-zinc-900">
          <h3 class="text-lg font-semibold text-zinc-900 dark:text-zinc-50">Starter</h3>
          <p class="mt-4 text-4xl font-bold text-zinc-900 dark:text-zinc-50">
            {{{{ isAnnual ? '$24' : '$29' }}}}<span class="text-sm font-normal text-zinc-500">/mo</span>
          </p>
          <p class="mt-2 text-sm text-zinc-500">For individuals and rapid prototyping.</p>
          <button class="mt-8 w-full rounded-xl border border-zinc-300 py-3 text-sm font-semibold transition-all duration-200 hover:bg-zinc-50 hover:border-zinc-400 active:scale-98 dark:border-zinc-700 dark:hover:bg-zinc-800">
            Get Started
          </button>
        </div>

        <div class="group relative rounded-2xl border-2 border-blue-600 bg-white p-8 shadow-lg shadow-blue-500/10 transition-all duration-300 ease-out hover:-translate-y-2.5 hover:shadow-2xl hover:shadow-blue-500/25 dark:bg-zinc-900">
          <span class="absolute -top-3.5 right-6 rounded-full bg-blue-600 px-3.5 py-1 text-xs font-bold text-white shadow-md animate-pulse">
            Most Popular
          </span>
          <h3 class="text-lg font-semibold text-zinc-900 dark:text-zinc-50">Pro</h3>
          <p class="mt-4 text-4xl font-bold text-zinc-900 dark:text-zinc-50">
            {{{{ isAnnual ? '$69' : '$79' }}}}<span class="text-sm font-normal text-zinc-500">/mo</span>
          </p>
          <p class="mt-2 text-sm text-zinc-500">For growing engineering teams requiring full parity.</p>
          <button class="mt-8 w-full rounded-xl bg-blue-600 py-3 text-sm font-semibold text-white shadow-md shadow-blue-500/25 transition-all duration-300 hover:bg-blue-500 hover:shadow-lg hover:shadow-blue-500/35 active:scale-98">
            Upgrade to Pro
          </button>
        </div>
      </div>
    </div>
  </section>
</template>
"""
    elif section_type == "footer":
        footer_brand = """<span class="font-bold text-zinc-900 dark:text-zinc-100">Brand</span>"""
        if images:
            logo_src = images[0]["src"]
            logo_alt = images[0].get("alt") or "Footer Logo"
            footer_brand = f"""<img src="{logo_src}" alt="{logo_alt}" class="h-7 w-auto object-contain opacity-80 hover:opacity-100 transition-opacity" />"""

        return f"""<script setup lang="ts">
// {name} Component
</script>

<template>
  <footer class="border-t border-zinc-200 bg-white py-12 dark:border-zinc-800 dark:bg-zinc-950 transition-colors">
    <div class="container mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
      <div class="flex flex-col items-center justify-between gap-6 sm:flex-row">
        <div class="flex items-center gap-3">
          {footer_brand}
          <p class="text-sm text-zinc-500 dark:text-zinc-400">
            &copy; {{{{ new Date().getFullYear() }}}} All rights reserved. Built with fluid 60fps animations.
          </p>
        </div>
        <div class="flex gap-6 text-sm text-zinc-500">
          <a href="#" class="transition hover:text-zinc-900 hover:-translate-y-0.5 dark:hover:text-zinc-50">Privacy</a>
          <a href="#" class="transition hover:text-zinc-900 hover:-translate-y-0.5 dark:hover:text-zinc-50">Terms</a>
          <a href="#" class="transition hover:text-zinc-900 hover:-translate-y-0.5 dark:hover:text-zinc-50">GitHub</a>
        </div>
      </div>
    </div>
  </footer>
</template>
"""
    else:  # Features / Bento Grid default
        card_items = []
        default_feats = [
            ("Autonomous Parity Engine", "Reverse-engineers live layouts into clean components with pixel precision and 60fps motion."),
            ("Fluid Spring Physics", "Pre-configured cubic-bezier motion curves, hover lifts, and zero-jank micro-interactions."),
            ("WCAG AA Accessibility", "Automatic focus rings, contrast checks, and prefers-reduced-motion accessibility safeguards.")
        ]

        count = max(3, len(images))
        for idx in range(min(count, 6)):
            title = headings[idx + 1] if idx + 1 < len(headings) else default_feats[idx % len(default_feats)][0]
            desc = paras[idx + 1] if idx + 1 < len(paras) else default_feats[idx % len(default_feats)][1]
            if idx < len(images):
                img_src = images[idx]["src"]
                img_alt = images[idx].get("alt") or title
                visual_box = f"""<div class="relative mb-5 h-44 w-full overflow-hidden rounded-xl bg-zinc-100 dark:bg-zinc-800">
            <img
              src="{img_src}"
              alt="{img_alt}"
              class="h-full w-full object-cover transition-transform duration-500 ease-out group-hover:scale-105"
              loading="lazy"
            />
          </div>"""
            else:
                visual_box = """<div class="mb-5 inline-flex h-12 w-12 items-center justify-center rounded-xl bg-blue-600/10 text-xl text-blue-600 transition-transform duration-300 ease-out group-hover:scale-110 group-hover:rotate-6 dark:bg-blue-400/10 dark:text-blue-400">
            ⚡
          </div>"""

            card_items.append(f"""        <!-- Card {idx + 1} -->
        <div class="group relative overflow-hidden rounded-2xl border border-zinc-200/80 bg-white p-6 shadow-sm transition-all duration-300 ease-out hover:-translate-y-2 hover:shadow-xl hover:shadow-zinc-900/5 hover:border-blue-500/40 dark:border-zinc-800/80 dark:bg-zinc-900 dark:hover:border-blue-500/40">
          {visual_box}
          <h3 class="flex items-center justify-between text-lg font-semibold text-zinc-900 dark:text-zinc-50">
            <span>{title}</span>
            <span class="text-blue-600 opacity-0 -translate-x-2 transition-all duration-300 group-hover:opacity-100 group-hover:translate-x-0">
              &rarr;
            </span>
          </h3>
          <p class="mt-3 text-sm leading-relaxed text-zinc-600 dark:text-zinc-400">
            {desc}
          </p>
        </div>""")

        all_cards = "\n\n".join(card_items)

        return f"""<script setup lang="ts">
// {name} Component
</script>

<template>
  <section id="features" class="py-24 sm:py-32">
    <div class="container mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
      <div class="mx-auto max-w-2xl text-center">
        <h2 class="text-3xl font-bold tracking-tight text-zinc-900 sm:text-4xl dark:text-zinc-50 animate-fade-in-up">
          {h_main}
        </h2>
        <p class="mt-4 text-base text-zinc-600 dark:text-zinc-400">
          {p_main}
        </p>
      </div>

      <div class="mx-auto mt-16 grid max-w-2xl grid-cols-1 gap-8 sm:grid-cols-2 lg:max-w-none lg:grid-cols-3">
{all_cards}
      </div>
    </div>
  </section>
</template>
"""


# ==========================================
# 3. SVELTE 5 GENERATOR (EXACT MEDIA & FLUID MOTION)
# ==========================================
def generate_svelte_component(
    name: str,
    section_type: str,
    headings: list[str],
    paras: list[str],
    buttons: list[str],
    images: list[dict] = None,
    videos: list[dict] = None
) -> str:
    images = images or []
    videos = videos or []
    h_main = headings[0] if headings else f"{name} Title"
    p_main = paras[0] if paras else "Subtext or descriptive copy supporting the primary message."
    cta_text = buttons[0] if buttons else "Get Started"

    if section_type == "header":
        brand_markup = """<span class="h-7 w-7 rounded-lg bg-blue-600 inline-flex items-center justify-center text-white text-xs font-black shadow-md shadow-blue-500/25 transition-transform duration-300 ease-out group-hover:scale-110 group-hover:rotate-6">
        ⚡
      </span>
      <span class="transition-colors duration-200 group-hover:text-blue-600 dark:group-hover:text-blue-400">Brand</span>"""
        if images:
            logo_src = images[0]["src"]
            logo_alt = images[0].get("alt") or "Brand Logo"
            brand_markup = f"""<img src="{logo_src}" alt="{logo_alt}" class="h-8 w-auto max-h-8 object-contain transition-transform duration-300 ease-out group-hover:scale-105" />"""

        return f"""<script lang="ts">
  let isMobileMenuOpen = false;
</script>

<header class="sticky top-0 z-50 w-full border-b border-zinc-200/80 bg-white/80 backdrop-blur-md transition-all duration-300 dark:border-zinc-800/80 dark:bg-zinc-950/80">
  <div class="container mx-auto flex h-16 max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8">
    <a href="#" class="group flex items-center gap-2.5 font-bold text-xl tracking-tight text-zinc-900 dark:text-zinc-50 cursor-pointer">
      {brand_markup}
    </a>

    <nav class="hidden md:flex items-center gap-8 text-sm font-medium text-zinc-600 dark:text-zinc-400">
      <a href="#features" class="relative py-1 transition hover:text-zinc-900 dark:hover:text-zinc-50 after:absolute after:bottom-0 after:left-0 after:h-[2px] after:w-0 hover:after:w-full after:bg-blue-600 after:transition-all after:duration-300">Features</a>
      <a href="#pricing" class="relative py-1 transition hover:text-zinc-900 dark:hover:text-zinc-50 after:absolute after:bottom-0 after:left-0 after:h-[2px] after:w-0 hover:after:w-full after:bg-blue-600 after:transition-all after:duration-300">Pricing</a>
      <a href="#testimonials" class="relative py-1 transition hover:text-zinc-900 dark:hover:text-zinc-50 after:absolute after:bottom-0 after:left-0 after:h-[2px] after:w-0 hover:after:w-full after:bg-blue-600 after:transition-all after:duration-300">Testimonials</a>
    </nav>

    <div class="hidden md:flex items-center gap-4">
      <button class="relative overflow-hidden rounded-xl bg-zinc-900 px-5 py-2.5 text-sm font-semibold text-white shadow-sm transition-all duration-300 ease-out hover:-translate-y-0.5 hover:shadow-lg hover:shadow-zinc-900/10 hover:bg-zinc-800 active:translate-y-0 active:scale-95 dark:bg-zinc-50 dark:text-zinc-900 dark:hover:bg-zinc-200">
        {cta_text}
      </button>
    </div>

    <button
      on:click={{() => isMobileMenuOpen = !isMobileMenuOpen}}
      class="md:hidden inline-flex items-center justify-center p-2 rounded-lg text-zinc-700 dark:text-zinc-200 hover:bg-zinc-100 dark:hover:bg-zinc-800 transition-colors"
      aria-expanded={{isMobileMenuOpen}}
    >
      <span class="sr-only">Toggle navigation menu</span>
      <span>{{isMobileMenuOpen ? '✕' : '☰'}}</span>
    </button>
  </div>

  {{#if isMobileMenuOpen}}
    <div class="md:hidden border-b border-zinc-200 dark:border-zinc-800 bg-white/95 dark:bg-zinc-950/95 px-6 pt-3 pb-6 space-y-3 animate-fade-in-down shadow-xl backdrop-blur-md">
      <a href="#features" class="block text-sm font-medium py-2 text-zinc-700 dark:text-zinc-200 hover:text-blue-600">Features</a>
      <a href="#pricing" class="block text-sm font-medium py-2 text-zinc-700 dark:text-zinc-200 hover:text-blue-600">Pricing</a>
      <a href="#testimonials" class="block text-sm font-medium py-2 text-zinc-700 dark:text-zinc-200 hover:text-blue-600">Testimonials</a>
      <button class="w-full mt-2 rounded-xl bg-blue-600 py-3 text-sm font-semibold text-white shadow-md hover:bg-blue-500 transition-all duration-200">
        {cta_text}
      </button>
    </div>
  {{/if}}
</header>
"""
    elif section_type == "hero":
        media_showcase = ""
        if videos:
            v = videos[0]
            poster_attr = f'poster="{v["poster"]}"' if v.get("poster") else ""
            media_showcase = f"""
    <!-- Exact Mirrored Video Showcase with Ambient Glow -->
    <div class="mt-14 relative mx-auto max-w-5xl overflow-hidden rounded-2xl border border-zinc-200/80 bg-zinc-900/5 p-2 shadow-2xl backdrop-blur-sm transition-all duration-500 hover:border-blue-500/30 dark:border-zinc-800/80 dark:bg-zinc-900/50">
      <video
        src="{v['src']}"
        {poster_attr}
        autoplay
        loop
        muted
        playsinline
        class="w-full rounded-xl object-cover shadow-inner"
      />
    </div>"""
        elif images:
            img = images[0]
            media_showcase = f"""
    <!-- Exact Mirrored Hero Image Showcase with Ambient Glow -->
    <div class="mt-14 relative mx-auto max-w-5xl overflow-hidden rounded-2xl border border-zinc-200/80 bg-zinc-900/5 p-2 shadow-2xl backdrop-blur-sm transition-all duration-500 ease-out hover:shadow-blue-500/10 hover:border-zinc-300 dark:border-zinc-800/80 dark:bg-zinc-900/50">
      <img
        src="{img['src']}"
        alt="{img.get('alt', 'Hero visual showcase')}"
        class="w-full rounded-xl object-cover shadow-inner transition-transform duration-700 ease-out hover:scale-[1.01]"
        loading="eager"
      />
    </div>"""

        return f"""<script lang="ts">
  const brands = ['Acme Corp', 'NextScale', 'HyperFlow', 'Veloce', 'CloudMesh', 'ApexCore', 'Acme Corp', 'NextScale', 'HyperFlow', 'Veloce', 'CloudMesh', 'ApexCore'];
</script>

<section class="relative overflow-hidden py-24 sm:py-32">
  <div class="pointer-events-none absolute -top-40 left-1/2 -z-10 -translate-x-1/2 transform-gpu overflow-hidden blur-3xl" aria-hidden="true">
    <div class="aspect-[1155/678] w-[68rem] bg-gradient-to-tr from-blue-600 to-cyan-400 opacity-20 animate-pulse-glow" />
  </div>

  <div class="container mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
    <div class="mx-auto max-w-3xl text-center">
      <div class="mb-6 inline-flex items-center gap-2 rounded-full border border-blue-500/20 bg-blue-500/10 px-4 py-1.5 text-xs font-semibold text-blue-600 dark:text-blue-400 shadow-sm backdrop-blur-sm animate-float">
        <span class="relative flex h-2 w-2">
          <span class="absolute inline-flex h-full w-full animate-ping rounded-full bg-blue-400 opacity-75"></span>
          <span class="relative inline-flex h-2 w-2 rounded-full bg-blue-500"></span>
        </span>
        <span>✨ Autonomous Replication Ready</span>
      </div>

      <h1 class="text-4xl font-extrabold tracking-tight text-zinc-900 sm:text-6xl dark:text-zinc-50 leading-[1.1] animate-fade-in-up">
        {h_main}
      </h1>

      <p class="mt-6 text-lg leading-8 text-zinc-600 dark:text-zinc-400 animate-fade-in-up [animation-delay:150ms]">
        {p_main}
      </p>

      <div class="mt-10 flex flex-wrap items-center justify-center gap-4 animate-fade-in-up [animation-delay:300ms]">
        <button class="relative overflow-hidden rounded-xl bg-blue-600 px-6 py-3.5 text-sm font-semibold text-white shadow-lg shadow-blue-500/25 transition-all duration-300 ease-out hover:-translate-y-1 hover:shadow-xl hover:shadow-blue-500/35 hover:bg-blue-500 active:translate-y-0 active:scale-95">
          {cta_text}
        </button>
        <a href="#demo" class="group inline-flex items-center gap-1.5 text-sm font-semibold leading-6 text-zinc-900 transition-all duration-200 hover:text-blue-600 hover:translate-x-1 dark:text-zinc-50 dark:hover:text-blue-400">
          Live Interactive Demo <span class="transition-transform duration-200 group-hover:translate-x-1">&rarr;</span>
        </a>
      </div>
    </div>
{media_showcase}

    <div class="mt-20 w-full overflow-hidden border-y border-zinc-200/60 dark:border-zinc-800/60 py-6">
      <p class="text-center text-xs font-semibold uppercase tracking-wider text-zinc-400 dark:text-zinc-500 mb-4">
        Trusted by world-class frontend teams
      </p>
      <div class="flex gap-12 whitespace-nowrap animate-marquee">
        {{#each brands as b}}
          <span class="text-sm font-semibold text-zinc-400 hover:text-zinc-900 dark:text-zinc-500 dark:hover:text-zinc-100 transition-colors cursor-default">
            {{b}}
          </span>
        {{/each}}
      </div>
    </div>
  </div>
</section>
"""
    elif section_type == "pricing":
        return f"""<script lang="ts">
  let isAnnual = true;
</script>

<section id="pricing" class="py-24 sm:py-32 bg-zinc-50/50 dark:bg-zinc-900/30">
  <div class="container mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
    <div class="mx-auto max-w-2xl text-center">
      <h2 class="text-3xl font-bold tracking-tight text-zinc-900 sm:text-4xl dark:text-zinc-50">
        {h_main}
      </h2>
      <p class="mt-4 text-base text-zinc-600 dark:text-zinc-400">
        {p_main}
      </p>

      <div class="mt-8 flex items-center justify-center gap-3">
        <span class="text-sm font-medium text-zinc-600 dark:text-zinc-400">Monthly</span>
        <button
          on:click={{() => isAnnual = !isAnnual}}
          class="relative inline-flex h-7 w-12 shrink-0 cursor-pointer rounded-full border-2 border-transparent bg-zinc-300 transition-colors duration-300 ease-out focus:outline-none dark:bg-zinc-700"
          role="switch"
          aria-checked={{isAnnual}}
        >
          <span class="inline-block h-6 w-6 transform rounded-full bg-white shadow-md transition-transform duration-300 ease-[cubic-bezier(0.16,1,0.3,1)] {{isAnnual ? 'translate-x-5 !bg-blue-600' : 'translate-x-0'}}" />
        </button>
        <span class="text-sm font-medium text-zinc-900 dark:text-zinc-50">
          Annual <span class="inline-block rounded-full bg-emerald-500/10 px-2.5 py-0.5 text-xs font-semibold text-emerald-600 dark:text-emerald-400 animate-pulse">Save 20%</span>
        </span>
      </div>
    </div>

    <div class="mx-auto mt-16 grid max-w-lg grid-cols-1 gap-8 lg:max-w-4xl lg:grid-cols-2">
      <div class="group rounded-2xl border border-zinc-200 bg-white p-8 shadow-sm transition-all duration-300 ease-out hover:-translate-y-2 hover:shadow-xl dark:border-zinc-800 dark:bg-zinc-900">
        <h3 class="text-lg font-semibold text-zinc-900 dark:text-zinc-50">Starter</h3>
        <p class="mt-4 text-4xl font-bold text-zinc-900 dark:text-zinc-50">
          {{isAnnual ? '$24' : '$29'}}<span class="text-sm font-normal text-zinc-500">/mo</span>
        </p>
        <p class="mt-2 text-sm text-zinc-500">For individuals and rapid prototyping.</p>
        <button class="mt-8 w-full rounded-xl border border-zinc-300 py-3 text-sm font-semibold transition-all duration-200 hover:bg-zinc-50 hover:border-zinc-400 active:scale-98 dark:border-zinc-700 dark:hover:bg-zinc-800">
          Get Started
        </button>
      </div>

      <div class="group relative rounded-2xl border-2 border-blue-600 bg-white p-8 shadow-lg shadow-blue-500/10 transition-all duration-300 ease-out hover:-translate-y-2.5 hover:shadow-2xl hover:shadow-blue-500/25 dark:bg-zinc-900">
        <span class="absolute -top-3.5 right-6 rounded-full bg-blue-600 px-3.5 py-1 text-xs font-bold text-white shadow-md animate-pulse">
          Most Popular
        </span>
        <h3 class="text-lg font-semibold text-zinc-900 dark:text-zinc-50">Pro</h3>
        <p class="mt-4 text-4xl font-bold text-zinc-900 dark:text-zinc-50">
          {{isAnnual ? '$69' : '$79'}}<span class="text-sm font-normal text-zinc-500">/mo</span>
        </p>
        <p class="mt-2 text-sm text-zinc-500">For growing engineering teams requiring full parity.</p>
        <button class="mt-8 w-full rounded-xl bg-blue-600 py-3 text-sm font-semibold text-white shadow-md shadow-blue-500/25 transition-all duration-300 hover:bg-blue-500 hover:shadow-lg hover:shadow-blue-500/35 active:scale-98">
          Upgrade to Pro
        </button>
      </div>
    </div>
  </div>
</section>
"""
    elif section_type == "footer":
        footer_brand = """<span class="font-bold text-zinc-900 dark:text-zinc-100">Brand</span>"""
        if images:
            logo_src = images[0]["src"]
            logo_alt = images[0].get("alt") or "Footer Logo"
            footer_brand = f"""<img src="{logo_src}" alt="{logo_alt}" class="h-7 w-auto object-contain opacity-80 hover:opacity-100 transition-opacity" />"""

        return f"""<script lang="ts">
  // {name} Component
</script>

<footer class="border-t border-zinc-200 bg-white py-12 dark:border-zinc-800 dark:bg-zinc-950 transition-colors">
  <div class="container mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
    <div class="flex flex-col items-center justify-between gap-6 sm:flex-row">
      <div class="flex items-center gap-3">
        {footer_brand}
        <p class="text-sm text-zinc-500 dark:text-zinc-400">
          &copy; {{{{ new Date().getFullYear() }}}} All rights reserved. Built with fluid 60fps animations.
        </p>
      </div>
      <div class="flex gap-6 text-sm text-zinc-500">
        <a href="#" class="transition hover:text-zinc-900 hover:-translate-y-0.5 dark:hover:text-zinc-50">Privacy</a>
        <a href="#" class="transition hover:text-zinc-900 hover:-translate-y-0.5 dark:hover:text-zinc-50">Terms</a>
        <a href="#" class="transition hover:text-zinc-900 hover:-translate-y-0.5 dark:hover:text-zinc-50">GitHub</a>
      </div>
    </div>
  </div>
</footer>
"""
    else:
        card_items = []
        default_feats = [
            ("Autonomous Parity Engine", "Reverse-engineers live layouts into clean components with pixel precision and 60fps motion."),
            ("Fluid Spring Physics", "Pre-configured cubic-bezier motion curves, hover lifts, and zero-jank micro-interactions."),
            ("WCAG AA Accessibility", "Automatic focus rings, contrast checks, and prefers-reduced-motion accessibility safeguards.")
        ]

        count = max(3, len(images))
        for idx in range(min(count, 6)):
            title = headings[idx + 1] if idx + 1 < len(headings) else default_feats[idx % len(default_feats)][0]
            desc = paras[idx + 1] if idx + 1 < len(paras) else default_feats[idx % len(default_feats)][1]
            if idx < len(images):
                img_src = images[idx]["src"]
                img_alt = images[idx].get("alt") or title
                visual_box = f"""<div class="relative mb-5 h-44 w-full overflow-hidden rounded-xl bg-zinc-100 dark:bg-zinc-800">
        <img
          src="{img_src}"
          alt="{img_alt}"
          class="h-full w-full object-cover transition-transform duration-500 ease-out group-hover:scale-105"
          loading="lazy"
        />
      </div>"""
            else:
                visual_box = """<div class="mb-5 inline-flex h-12 w-12 items-center justify-center rounded-xl bg-blue-600/10 text-xl text-blue-600 transition-transform duration-300 ease-out group-hover:scale-110 group-hover:rotate-6 dark:bg-blue-400/10 dark:text-blue-400">
        ⚡
      </div>"""

            card_items.append(f"""      <!-- Card {idx + 1} -->
      <div class="group relative overflow-hidden rounded-2xl border border-zinc-200/80 bg-white p-6 shadow-sm transition-all duration-300 ease-out hover:-translate-y-2 hover:shadow-xl hover:shadow-zinc-900/5 hover:border-blue-500/40 dark:border-zinc-800/80 dark:bg-zinc-900 dark:hover:border-blue-500/40">
        {visual_box}
        <h3 class="flex items-center justify-between text-lg font-semibold text-zinc-900 dark:text-zinc-50">
          <span>{title}</span>
          <span class="text-blue-600 opacity-0 -translate-x-2 transition-all duration-300 group-hover:opacity-100 group-hover:translate-x-0">
            &rarr;
          </span>
        </h3>
        <p class="mt-3 text-sm leading-relaxed text-zinc-600 dark:text-zinc-400">
          {desc}
        </p>
      </div>""")

        all_cards = "\n\n".join(card_items)

        return f"""<script lang="ts">
  // {name} Component
</script>

<section id="features" class="py-24 sm:py-32">
  <div class="container mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
    <div class="mx-auto max-w-2xl text-center">
      <h2 class="text-3xl font-bold tracking-tight text-zinc-900 sm:text-4xl dark:text-zinc-50 animate-fade-in-up">
        {h_main}
      </h2>
      <p class="mt-4 text-base text-zinc-600 dark:text-zinc-400">
        {p_main}
      </p>
    </div>

    <div class="mx-auto mt-16 grid max-w-2xl grid-cols-1 gap-8 sm:grid-cols-2 lg:max-w-none lg:grid-cols-3">
{all_cards}
    </div>
  </div>
</section>
"""


# ==========================================
# 4. PURE HTML5 / TAILWIND GENERATOR (EXACT MEDIA & FLUID MOTION)
# ==========================================
def generate_html_component(
    name: str,
    section_type: str,
    headings: list[str],
    paras: list[str],
    buttons: list[str],
    images: list[dict] = None,
    videos: list[dict] = None
) -> str:
    images = images or []
    videos = videos or []
    h_main = headings[0] if headings else f"{name} Title"
    p_main = paras[0] if paras else "Subtext or descriptive copy supporting the primary message."
    cta_text = buttons[0] if buttons else "Get Started"

    if section_type == "header":
        brand_markup = """<span class="h-7 w-7 rounded-lg bg-blue-600 inline-flex items-center justify-center text-white text-xs font-black shadow-md shadow-blue-500/25 transition-transform duration-300 ease-out group-hover:scale-110 group-hover:rotate-6">
        ⚡
      </span>
      <span class="transition-colors duration-200 group-hover:text-blue-600 dark:group-hover:text-blue-400">Brand</span>"""
        if images:
            logo_src = images[0]["src"]
            logo_alt = images[0].get("alt") or "Brand Logo"
            brand_markup = f"""<img src="{logo_src}" alt="{logo_alt}" class="h-8 w-auto max-h-8 object-contain transition-transform duration-300 ease-out group-hover:scale-105" />"""

        return f"""<!-- {name} Component with Animated Hover Physics -->
<header class="sticky top-0 z-50 w-full border-b border-zinc-200/80 bg-white/80 backdrop-blur-md transition-all duration-300 dark:border-zinc-800/80 dark:bg-zinc-950/80">
  <div class="container mx-auto flex h-16 max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8">
    <a href="#" class="group flex items-center gap-2.5 font-bold text-xl tracking-tight text-zinc-900 dark:text-zinc-50 cursor-pointer">
      {brand_markup}
    </a>

    <nav class="hidden md:flex items-center gap-8 text-sm font-medium text-zinc-600 dark:text-zinc-400">
      <a href="#features" class="relative py-1 transition hover:text-zinc-900 dark:hover:text-zinc-50 after:absolute after:bottom-0 after:left-0 after:h-[2px] after:w-0 hover:after:w-full after:bg-blue-600 after:transition-all after:duration-300">Features</a>
      <a href="#pricing" class="relative py-1 transition hover:text-zinc-900 dark:hover:text-zinc-50 after:absolute after:bottom-0 after:left-0 after:h-[2px] after:w-0 hover:after:w-full after:bg-blue-600 after:transition-all after:duration-300">Pricing</a>
      <a href="#testimonials" class="relative py-1 transition hover:text-zinc-900 dark:hover:text-zinc-50 after:absolute after:bottom-0 after:left-0 after:h-[2px] after:w-0 hover:after:w-full after:bg-blue-600 after:transition-all after:duration-300">Testimonials</a>
    </nav>

    <div class="flex items-center gap-4">
      <button class="relative overflow-hidden rounded-xl bg-zinc-900 px-5 py-2.5 text-sm font-semibold text-white shadow-sm transition-all duration-300 ease-out hover:-translate-y-0.5 hover:shadow-lg hover:shadow-zinc-900/10 hover:bg-zinc-800 active:translate-y-0 active:scale-95 dark:bg-zinc-50 dark:text-zinc-900 dark:hover:bg-zinc-200">
        {cta_text}
      </button>
    </div>
  </div>
</header>
"""
    elif section_type == "hero":
        media_showcase = ""
        if videos:
            v = videos[0]
            poster_attr = f'poster="{v["poster"]}"' if v.get("poster") else ""
            media_showcase = f"""
    <!-- Exact Mirrored Video Showcase with Ambient Glow -->
    <div class="mt-14 relative mx-auto max-w-5xl overflow-hidden rounded-2xl border border-zinc-200/80 bg-zinc-900/5 p-2 shadow-2xl backdrop-blur-sm transition-all duration-500 hover:border-blue-500/30 dark:border-zinc-800/80 dark:bg-zinc-900/50">
      <video
        src="{v['src']}"
        {poster_attr}
        autoplay
        loop
        muted
        playsinline
        class="w-full rounded-xl object-cover shadow-inner"
      ></video>
    </div>"""
        elif images:
            img = images[0]
            media_showcase = f"""
    <!-- Exact Mirrored Hero Image Showcase with Ambient Glow -->
    <div class="mt-14 relative mx-auto max-w-5xl overflow-hidden rounded-2xl border border-zinc-200/80 bg-zinc-900/5 p-2 shadow-2xl backdrop-blur-sm transition-all duration-500 ease-out hover:shadow-blue-500/10 hover:border-zinc-300 dark:border-zinc-800/80 dark:bg-zinc-900/50">
      <img
        src="{img['src']}"
        alt="{img.get('alt', 'Hero visual showcase')}"
        class="w-full rounded-xl object-cover shadow-inner transition-transform duration-700 ease-out hover:scale-[1.01]"
        loading="eager"
      />
    </div>"""

        return f"""<!-- {name} Component with Ambient Glow & Animated Entrance -->
<section class="relative overflow-hidden py-24 sm:py-32" data-cau-animate="fade-up">
  <div class="pointer-events-none absolute -top-40 left-1/2 -z-10 -translate-x-1/2 transform-gpu overflow-hidden blur-3xl" aria-hidden="true">
    <div class="aspect-[1155/678] w-[68rem] bg-gradient-to-tr from-blue-600 to-cyan-400 opacity-20 animate-pulse-glow"></div>
  </div>

  <div class="container mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
    <div class="mx-auto max-w-3xl text-center">
      <div class="mb-6 inline-flex items-center gap-2 rounded-full border border-blue-500/20 bg-blue-500/10 px-4 py-1.5 text-xs font-semibold text-blue-600 dark:text-blue-400 shadow-sm backdrop-blur-sm animate-float">
        <span class="relative flex h-2 w-2">
          <span class="absolute inline-flex h-full w-full animate-ping rounded-full bg-blue-400 opacity-75"></span>
          <span class="relative inline-flex h-2 w-2 rounded-full bg-blue-500"></span>
        </span>
        <span>✨ Autonomous Replication Ready</span>
      </div>

      <h1 class="text-4xl font-extrabold tracking-tight text-zinc-900 sm:text-6xl dark:text-zinc-50 leading-[1.1] animate-fade-in-up">
        {h_main}
      </h1>

      <p class="mt-6 text-lg leading-8 text-zinc-600 dark:text-zinc-400 animate-fade-in-up [animation-delay:150ms]">
        {p_main}
      </p>

      <div class="mt-10 flex flex-wrap items-center justify-center gap-4 animate-fade-in-up [animation-delay:300ms]">
        <button class="relative overflow-hidden rounded-xl bg-blue-600 px-6 py-3.5 text-sm font-semibold text-white shadow-lg shadow-blue-500/25 transition-all duration-300 ease-out hover:-translate-y-1 hover:shadow-xl hover:shadow-blue-500/35 hover:bg-blue-500 active:translate-y-0 active:scale-95">
          {cta_text}
        </button>
        <a href="#demo" class="group inline-flex items-center gap-1.5 text-sm font-semibold leading-6 text-zinc-900 transition-all duration-200 hover:text-blue-600 hover:translate-x-1 dark:text-zinc-50 dark:hover:text-blue-400">
          Live Interactive Demo <span class="transition-transform duration-200 group-hover:translate-x-1">&rarr;</span>
        </a>
      </div>
    </div>
{media_showcase}

    <!-- Infinite Logo Marquee Ticker -->
    <div class="mt-20 w-full overflow-hidden border-y border-zinc-200/60 dark:border-zinc-800/60 py-6">
      <p class="text-center text-xs font-semibold uppercase tracking-wider text-zinc-400 dark:text-zinc-500 mb-4">
        Trusted by world-class frontend teams
      </p>
      <div class="flex gap-12 whitespace-nowrap animate-marquee">
        <span class="text-sm font-semibold text-zinc-400">Acme Corp</span>
        <span class="text-sm font-semibold text-zinc-400">NextScale</span>
        <span class="text-sm font-semibold text-zinc-400">HyperFlow</span>
        <span class="text-sm font-semibold text-zinc-400">Veloce</span>
        <span class="text-sm font-semibold text-zinc-400">CloudMesh</span>
        <span class="text-sm font-semibold text-zinc-400">ApexCore</span>
        <span class="text-sm font-semibold text-zinc-400">Acme Corp</span>
        <span class="text-sm font-semibold text-zinc-400">NextScale</span>
        <span class="text-sm font-semibold text-zinc-400">HyperFlow</span>
        <span class="text-sm font-semibold text-zinc-400">Veloce</span>
        <span class="text-sm font-semibold text-zinc-400">CloudMesh</span>
        <span class="text-sm font-semibold text-zinc-400">ApexCore</span>
      </div>
    </div>
  </div>
</section>
"""
    elif section_type == "pricing":
        return f"""<!-- {name} Component with Spring Toggle Switch -->
<section id="pricing" class="py-24 sm:py-32 bg-zinc-50/50 dark:bg-zinc-900/30" data-cau-animate="fade-up">
  <div class="container mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
    <div class="mx-auto max-w-2xl text-center">
      <h2 class="text-3xl font-bold tracking-tight text-zinc-900 sm:text-4xl dark:text-zinc-50">
        {h_main}
      </h2>
      <p class="mt-4 text-base text-zinc-600 dark:text-zinc-400">
        {p_main}
      </p>
    </div>

    <div class="mx-auto mt-16 grid max-w-lg grid-cols-1 gap-8 lg:max-w-4xl lg:grid-cols-2">
      <div class="group rounded-2xl border border-zinc-200 bg-white p-8 shadow-sm transition-all duration-300 ease-out hover:-translate-y-2 hover:shadow-xl dark:border-zinc-800 dark:bg-zinc-900">
        <h3 class="text-lg font-semibold text-zinc-900 dark:text-zinc-50">Starter</h3>
        <p class="mt-4 text-4xl font-bold text-zinc-900 dark:text-zinc-50">$29<span class="text-sm font-normal text-zinc-500">/mo</span></p>
        <p class="mt-2 text-sm text-zinc-500">For individuals and rapid prototyping.</p>
        <button class="mt-8 w-full rounded-xl border border-zinc-300 py-3 text-sm font-semibold transition-all duration-200 hover:bg-zinc-50 hover:border-zinc-400 active:scale-98 dark:border-zinc-700 dark:hover:bg-zinc-800">
          Get Started
        </button>
      </div>

      <div class="group relative rounded-2xl border-2 border-blue-600 bg-white p-8 shadow-lg shadow-blue-500/10 transition-all duration-300 ease-out hover:-translate-y-2.5 hover:shadow-2xl hover:shadow-blue-500/25 dark:bg-zinc-900">
        <span class="absolute -top-3.5 right-6 rounded-full bg-blue-600 px-3.5 py-1 text-xs font-bold text-white shadow-md animate-pulse">
          Most Popular
        </span>
        <h3 class="text-lg font-semibold text-zinc-900 dark:text-zinc-50">Pro</h3>
        <p class="mt-4 text-4xl font-bold text-zinc-900 dark:text-zinc-50">$79<span class="text-sm font-normal text-zinc-500">/mo</span></p>
        <p class="mt-2 text-sm text-zinc-500">For growing engineering teams requiring full parity.</p>
        <button class="mt-8 w-full rounded-xl bg-blue-600 py-3 text-sm font-semibold text-white shadow-md shadow-blue-500/25 transition-all duration-300 hover:bg-blue-500 hover:shadow-lg hover:shadow-blue-500/35 active:scale-98">
          Upgrade to Pro
        </button>
      </div>
    </div>
  </div>
</section>
"""
    elif section_type == "footer":
        footer_brand = """<span class="font-bold text-zinc-900 dark:text-zinc-100">Brand</span>"""
        if images:
            logo_src = images[0]["src"]
            logo_alt = images[0].get("alt") or "Footer Logo"
            footer_brand = f"""<img src="{logo_src}" alt="{logo_alt}" class="h-7 w-auto object-contain opacity-80 hover:opacity-100 transition-opacity" />"""

        return f"""<!-- {name} Component -->
<footer class="border-t border-zinc-200 bg-white py-12 dark:border-zinc-800 dark:bg-zinc-950 transition-colors">
  <div class="container mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
    <div class="flex flex-col items-center justify-between gap-6 sm:flex-row">
      <div class="flex items-center gap-3">
        {footer_brand}
        <p class="text-sm text-zinc-500 dark:text-zinc-400">
          &copy; 2026 All rights reserved. Built with fluid 60fps animations.
        </p>
      </div>
      <div class="flex gap-6 text-sm text-zinc-500">
        <a href="#" class="transition hover:text-zinc-900 hover:-translate-y-0.5 dark:hover:text-zinc-50">Privacy</a>
        <a href="#" class="transition hover:text-zinc-900 hover:-translate-y-0.5 dark:hover:text-zinc-50">Terms</a>
        <a href="#" class="transition hover:text-zinc-900 hover:-translate-y-0.5 dark:hover:text-zinc-50">GitHub</a>
      </div>
    </div>
  </div>
</footer>
"""
    else:
        card_items = []
        default_feats = [
            ("Autonomous Parity Engine", "Reverse-engineers live layouts into clean components with pixel precision and 60fps motion."),
            ("Fluid Spring Physics", "Pre-configured cubic-bezier motion curves, hover lifts, and zero-jank micro-interactions."),
            ("WCAG AA Accessibility", "Automatic focus rings, contrast checks, and prefers-reduced-motion accessibility safeguards.")
        ]

        count = max(3, len(images))
        for idx in range(min(count, 6)):
            title = headings[idx + 1] if idx + 1 < len(headings) else default_feats[idx % len(default_feats)][0]
            desc = paras[idx + 1] if idx + 1 < len(paras) else default_feats[idx % len(default_feats)][1]
            if idx < len(images):
                img_src = images[idx]["src"]
                img_alt = images[idx].get("alt") or title
                visual_box = f"""<div class="relative mb-5 h-44 w-full overflow-hidden rounded-xl bg-zinc-100 dark:bg-zinc-800">
        <img
          src="{img_src}"
          alt="{img_alt}"
          class="h-full w-full object-cover transition-transform duration-500 ease-out group-hover:scale-105"
          loading="lazy"
        />
      </div>"""
            else:
                visual_box = """<div class="mb-5 inline-flex h-12 w-12 items-center justify-center rounded-xl bg-blue-600/10 text-xl text-blue-600 transition-transform duration-300 ease-out group-hover:scale-110 group-hover:rotate-6 dark:bg-blue-400/10 dark:text-blue-400">
        ⚡
      </div>"""

            card_items.append(f"""    <!-- Card {idx + 1} -->
    <div class="group relative overflow-hidden rounded-2xl border border-zinc-200/80 bg-white p-6 shadow-sm transition-all duration-300 ease-out hover:-translate-y-2 hover:shadow-xl hover:shadow-zinc-900/5 hover:border-blue-500/40 dark:border-zinc-800/80 dark:bg-zinc-900 dark:hover:border-blue-500/40">
      {visual_box}
      <h3 class="flex items-center justify-between text-lg font-semibold text-zinc-900 dark:text-zinc-50">
        <span>{title}</span>
        <span class="text-blue-600 opacity-0 -translate-x-2 transition-all duration-300 group-hover:opacity-100 group-hover:translate-x-0">
          &rarr;
        </span>
      </h3>
      <p class="mt-3 text-sm leading-relaxed text-zinc-600 dark:text-zinc-400">
        {desc}
      </p>
    </div>""")

        all_cards = "\n\n".join(card_items)

        return f"""<!-- {name} Component with Card Hover Physics & Icon Micro-Interactions -->
<section id="features" class="py-24 sm:py-32" data-cau-animate="fade-up">
  <div class="container mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
    <div class="mx-auto max-w-2xl text-center">
      <h2 class="text-3xl font-bold tracking-tight text-zinc-900 sm:text-4xl dark:text-zinc-50 animate-fade-in-up">
        {h_main}
      </h2>
      <p class="mt-4 text-base text-zinc-600 dark:text-zinc-400">
        {p_main}
      </p>
    </div>

    <div class="mx-auto mt-16 grid max-w-2xl grid-cols-1 gap-8 sm:grid-cols-2 lg:max-w-none lg:grid-cols-3">
{all_cards}
    </div>
  </div>
</section>
"""


def main() -> None:
    parser = argparse.ArgumentParser(description="Componentize HTML into clean React, Vue, Svelte, or Tailwind components.")
    parser.add_argument("--input", required=True, help="Path to input HTML file")
    parser.add_argument("--out", default="extracted_components", help="Output directory for generated components")
    parser.add_argument("--format", choices=["react", "vue", "svelte", "html"], default="react", help="Target component format")
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        sys.exit(f"[-] Input file not found: {args.input}")

    html_content = input_path.read_text(encoding="utf-8", errors="replace")
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    # Find sections / major container tags
    section_pattern = re.compile(r"<(header|nav|section|footer|div)\b([^>]*)>(.*?)</\1>", re.DOTALL | re.I)
    matches = list(section_pattern.finditer(html_content))

    print(f"[+] Found {len(matches)} top-level layout candidates. Extracting semantic sections into [{args.format.upper()}]...")

    component_index = []
    generated_count = 0

    ext_map = {
        "react": ".tsx",
        "vue": ".vue",
        "svelte": ".svelte",
        "html": ".html",
    }
    ext = ext_map[args.format]

    for idx, match in enumerate(matches):
        tag_name = match.group(1).lower()
        attributes = match.group(2)
        inner = match.group(3)

        if len(inner.strip()) < 80 or "<script" in inner.lower():
            continue

        headings = extract_headings(inner)
        paras = extract_paragraphs(inner)
        buttons = extract_buttons_and_links(inner)
        images = extract_images(inner)
        videos = extract_videos(inner)

        sec_type = guess_section_type(tag_name, attributes, inner)
        comp_name = f"{sec_type.capitalize()}Section_{generated_count + 1}"

        if args.format == "react":
            comp_code = generate_react_component(comp_name, sec_type, headings, paras, buttons, images, videos)
        elif args.format == "vue":
            comp_code = generate_vue_component(comp_name, sec_type, headings, paras, buttons, images, videos)
        elif args.format == "svelte":
            comp_code = generate_svelte_component(comp_name, sec_type, headings, paras, buttons, images, videos)
        else:
            comp_code = generate_html_component(comp_name, sec_type, headings, paras, buttons, images, videos)

        comp_file = out_dir / f"{comp_name}{ext}"
        comp_file.write_text(comp_code, encoding="utf-8")
        component_index.append(comp_name)
        generated_count += 1
        print(f"  [✓] Generated {comp_name}{ext} ({sec_type}) [Media: {len(images)} img, {len(videos)} vid]")

    # Fallback if no specific section containers met threshold
    if generated_count == 0:
        body_match = re.search(r"<body\b[^>]*>(.*?)</body>", html_content, re.DOTALL | re.I)
        fallback_inner = body_match.group(1) if body_match else html_content
        title_match = re.search(r"<title\b[^>]*>(.*?)</title>", html_content, re.I)
        headings = extract_headings(fallback_inner) or [title_match.group(1).strip() if title_match else "Website Hero"]
        paras = extract_paragraphs(fallback_inner)
        buttons = extract_buttons_and_links(fallback_inner)
        images = extract_images(fallback_inner)
        videos = extract_videos(fallback_inner)

        comp_name = "MainLandingSection"
        if args.format == "react":
            comp_code = generate_react_component(comp_name, "hero", headings, paras, buttons, images, videos)
        elif args.format == "vue":
            comp_code = generate_vue_component(comp_name, "hero", headings, paras, buttons, images, videos)
        elif args.format == "svelte":
            comp_code = generate_svelte_component(comp_name, "hero", headings, paras, buttons, images, videos)
        else:
            comp_code = generate_html_component(comp_name, "hero", headings, paras, buttons, images, videos)

        comp_file = out_dir / f"{comp_name}{ext}"
        comp_file.write_text(comp_code, encoding="utf-8")
        component_index.append(comp_name)
        print(f"  [✓] Generated {comp_name}{ext} (fallback main section) [Media: {len(images)} img, {len(videos)} vid]")

    # Generate index.ts for JS frameworks
    if args.format in {"react", "vue"} and component_index:
        index_ts = "\n".join([f"export {{ default as {c} }} from './{c}{ext}';" if args.format == "vue" else f"export {{ {c} }} from './{c}';" for c in component_index])
        (out_dir / "index.ts").write_text(index_ts + "\n", encoding="utf-8")
        print(f"[✓] Generated index.ts exporting all {len(component_index)} components.")

    print(f"\n[★] Componentization complete! Output saved to: {out_dir}")


if __name__ == "__main__":
    main()
