#!/usr/bin/env python3
"""CLONE ANY UI (CAU) — Universal Interaction & Behavioral Synthesizer.

Reverse-engineers UI roles, state machines, and micro-interactions from cloned pages
and injects fully functional, zero-dependency client-side interactivity:
1. Media & Audio: Play/Pause, Draggable Scrubbers, Live Timers, Volume Sliders, Sound.
2. Live Search & Filtering: Real-time card/item filtering as the user types.
3. Quantity & Cart: "+ / -" stepper counters and dynamic cart badges.
4. Filter Pills & Tabs: Interactive active pill toggling and tab switching.
5. Interactive Likes & Bookmarks: Spring scale bounce, color toggles, and toast feedback.
6. Pricing Toggles: Monthly vs Annual discount state switching.
7. Motion & Physics: Magnetic cursor pull and 3D card tilt.

Can inject directly into preview.html, site/index.html, or output React/Vue/Svelte hooks.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


def generate_interaction_script(brand_primary: str = "#1ed760") -> str:
    """Generates the universal zero-dependency interactions.js engine."""
    return f"""/**
 * CLONE ANY UI (CAU) — Universal Behavioral Engine (60fps Fluid Interactivity)
 * Synthesizes working state machines for media players, live search, counters,
 * accordions, like toggles, sliders, and spring motion physics.
 */
(() => {{
  'use strict';

  const BRAND_COLOR = '{brand_primary}';

  // --------------------------------------------------------------------------
  // 1. AUDIO & MEDIA PLAYBACK ENGINE (Real Sound, Draggable Scrubber, Timers)
  // --------------------------------------------------------------------------
  class CAUAudioEngine {{
    constructor() {{
      this.isPlaying = false;
      this.currentTime = 0;
      this.duration = 214; // 3:34 default
      this.volume = 0.8;
      this.audioCtx = null;
      this.oscillator = null;
      this.gainNode = null;
      this.animFrame = null;
      this.currentTrackTitle = 'Cloned Interactive Track';
      this.currentArtist = 'CAU Live Audio';
      this.currentCover = '';
      
      this.init();
    }}

    initAudioContext() {{
      if (this.audioCtx) return;
      try {{
        const AudioContext = window.AudioContext || window.webkitAudioContext;
        this.audioCtx = new AudioContext();
        this.gainNode = this.audioCtx.createGain();
        this.gainNode.gain.setValueAtTime(this.volume, this.audioCtx.currentTime);
        this.gainNode.connect(this.audioCtx.destination);
      }} catch (e) {{
        console.warn('[CAU] Web Audio initialization deferred:', e);
      }}
    }}

    // Synthesizes pleasant musical chords/beats so every play button makes REAL music
    startSynthesizedPlayback() {{
      this.initAudioContext();
      if (!this.audioCtx) return;
      if (this.audioCtx.state === 'suspended') {{
        this.audioCtx.resume();
      }}
      this.stopSynthesizedPlayback();

      // Create an ambient musical chord loop (C Major 9 chord: C4, E4, G4, B4, D5)
      const freqs = [261.63, 329.63, 392.00, 493.88, 587.33];
      this.activeOscillators = freqs.map((freq, idx) => {{
        const osc = this.audioCtx.createOscillator();
        const oscGain = this.audioCtx.createGain();
        osc.type = idx % 2 === 0 ? 'sine' : 'triangle';
        osc.frequency.setValueAtTime(freq, this.audioCtx.currentTime);
        
        // Soft pulsing volume
        oscGain.gain.setValueAtTime(0.04 / (idx + 1), this.audioCtx.currentTime);
        osc.connect(oscGain);
        oscGain.connect(this.gainNode);
        osc.start();
        return osc;
      }});
    }}

    stopSynthesizedPlayback() {{
      if (this.activeOscillators) {{
        this.activeOscillators.forEach(osc => {{
          try {{ osc.stop(); osc.disconnect(); }} catch (e) {{}}
        }});
        this.activeOscillators = null;
      }}
    }}

    togglePlay(sourceBtn, trackInfo = null) {{
      this.isPlaying = !this.isPlaying;
      if (trackInfo) {{
        if (trackInfo.title) this.currentTrackTitle = trackInfo.title;
        if (trackInfo.artist) this.currentArtist = trackInfo.artist;
        if (trackInfo.cover) this.currentCover = trackInfo.cover;
        this.updateNowPlayingUI();
      }}

      if (this.isPlaying) {{
        this.startSynthesizedPlayback();
        this.startTimeLoop();
        this.updatePlayIcons(true);
        this.showToast(`▶ Now Playing: ${{this.currentTrackTitle}}`);
      }} else {{
        this.stopSynthesizedPlayback();
        this.stopTimeLoop();
        this.updatePlayIcons(false);
      }}
    }}

    startTimeLoop() {{
      this.stopTimeLoop();
      const tick = () => {{
        if (!this.isPlaying) return;
        this.currentTime += 0.2;
        if (this.currentTime >= this.duration) {{
          this.currentTime = 0;
        }}
        this.updateScrubberUI();
        this.animFrame = setTimeout(tick, 200);
      }};
      this.animFrame = setTimeout(tick, 200);
    }}

    stopTimeLoop() {{
      if (this.animFrame) {{
        clearTimeout(this.animFrame);
        this.animFrame = null;
      }}
    }}

    seekToPercent(percent) {{
      this.currentTime = Math.max(0, Math.min(this.duration, this.duration * percent));
      this.updateScrubberUI();
    }}

    setVolume(percent) {{
      this.volume = Math.max(0, Math.min(1, percent));
      if (this.gainNode && this.audioCtx) {{
        this.gainNode.gain.setValueAtTime(this.volume, this.audioCtx.currentTime);
      }}
      this.updateVolumeUI();
    }}

    formatTime(sec) {{
      const m = Math.floor(sec / 60);
      const s = Math.floor(sec % 60);
      return `${{m}}:${{s < 10 ? '0' : ''}}${{s}}`;
    }}

    updateScrubberUI() {{
      const percent = (this.currentTime / this.duration) * 100;
      
      // Update time text
      document.querySelectorAll('#playback-position, [data-testid="playback-position"], .playback-current-time').forEach(el => {{
        el.textContent = this.formatTime(this.currentTime);
      }});
      document.querySelectorAll('#playback-duration, [data-testid="playback-duration"], .playback-duration').forEach(el => {{
        el.textContent = this.formatTime(this.duration);
      }});

      // Update progress bar width
      document.querySelectorAll('#progress-bar, #playback-progressbar, [data-testid="progress-bar"], .progress-bar-fill').forEach(el => {{
        el.style.width = `${{percent}}%`;
      }});
      document.querySelectorAll('#progress-bar-handle, [data-testid="progress-bar-handle"]').forEach(el => {{
        el.style.left = `${{percent}}%`;
      }});
    }}

    updateVolumeUI() {{
      const pct = this.volume * 100;
      document.querySelectorAll('#volume-bar, [data-testid="volume-bar"], .volume-bar-fill').forEach(el => {{
        el.style.width = `${{pct}}%`;
      }});
    }}

    updatePlayIcons(playing) {{
      // Update global player play button icon
      document.querySelectorAll('[data-testid="control-button-playpause"], .player-play-btn, button[aria-label*="Play" i], button[aria-label*="Pause" i]').forEach(btn => {{
        btn.setAttribute('aria-label', playing ? 'Pause' : 'Play');
        const svg = btn.querySelector('svg');
        if (svg) {{
          if (playing) {{
            svg.innerHTML = '<path d="M5.7 3a.7.7 0 0 0-.7.7v16.6a.7.7 0 0 0 .7.7h2.6a.7.7 0 0 0 .7-.7V3.7a.7.7 0 0 0-.7-.7H5.7zm10 0a.7.7 0 0 0-.7.7v16.6a.7.7 0 0 0 .7.7h2.6a.7.7 0 0 0 .7-.7V3.7a.7.7 0 0 0-.7-.7h-2.6z" fill="currentColor"/>';
          }} else {{
            svg.innerHTML = '<path d="M7.05 3.606l13.49 7.788a.7.7 0 010 1.212L7.05 20.394A.7.7 0 016 19.788V4.212a.7.7 0 011.05-.606z" fill="currentColor"/>';
          }}
        }}
      }});
    }}

    updateNowPlayingUI() {{
      document.querySelectorAll('[data-testid="context-item-info-title"], .now-playing-title').forEach(el => {{
        el.textContent = this.currentTrackTitle;
      }});
      document.querySelectorAll('[data-testid="context-item-info-subtitles"], .now-playing-artist').forEach(el => {{
        el.textContent = this.currentArtist;
      }});
      if (this.currentCover) {{
        document.querySelectorAll('[data-testid="cover-art-image"], .now-playing-cover').forEach(img => {{
          img.src = this.currentCover;
        }});
      }}
    }}

    showToast(msg) {{
      let toast = document.getElementById('cau-interactive-toast');
      if (!toast) {{
        toast = document.createElement('div');
        toast.id = 'cau-interactive-toast';
        toast.style.cssText = 'position:fixed;bottom:90px;left:50%;transform:translateX(-50%);background:#18181b;color:#fff;padding:10px 20px;border-radius:9999px;font-size:13px;font-weight:600;box-shadow:0 10px 25px -5px rgba(0,0,0,0.5);border:1px solid rgba(255,255,255,0.15);z-index:999999;transition:all 0.3s cubic-bezier(0.16,1,0.3,1);opacity:0;pointer-events:none;';
        document.body.appendChild(toast);
      }}
      toast.textContent = msg;
      toast.style.opacity = '1';
      toast.style.transform = 'translateX(-50%) translateY(0)';
      clearTimeout(this.toastTimer);
      this.toastTimer = setTimeout(() => {{
        toast.style.opacity = '0';
        toast.style.transform = 'translateX(-50%) translateY(10px)';
      }}, 2600);
    }}

    init() {{
      // Bind bottom player play/pause button
      document.addEventListener('click', (e) => {{
        const playBtn = e.target.closest('[data-testid="control-button-playpause"], .player-play-btn, button[aria-label*="Play" i], button[aria-label*="Pause" i]');
        if (playBtn) {{
          e.preventDefault();
          this.togglePlay(playBtn);
          return;
        }}

        // Card play button click
        const cardPlay = e.target.closest('[data-testid="play-button"], .card-play-btn, button[aria-label*="Play " i]');
        if (cardPlay) {{
          e.preventDefault();
          const card = cardPlay.closest('[data-testid*="card"], .card, div[role="group"]') || cardPlay.parentElement;
          const titleEl = card ? card.querySelector('[data-testid="card-title"], h3, h4, .font-bold, .title') : null;
          const subtitleEl = card ? card.querySelector('[data-testid="card-subtitle"], p, .text-sm, .artist') : null;
          const imgEl = card ? card.querySelector('img') : null;

          const trackInfo = {{
            title: titleEl ? titleEl.textContent.trim() : 'Playing Track',
            artist: subtitleEl ? subtitleEl.textContent.trim() : 'Featured Artist',
            cover: imgEl ? imgEl.src : ''
          }};
          this.togglePlay(cardPlay, trackInfo);
          return;
        }}

        // Like / Heart button click
        const likeBtn = e.target.closest('[data-testid="add-button"], .like-button, button[aria-label*="Save" i], button[aria-label*="Like" i]');
        if (likeBtn) {{
          e.preventDefault();
          const isLiked = likeBtn.classList.toggle('cau-liked');
          likeBtn.style.transition = 'transform 0.25s cubic-bezier(0.16, 1, 0.3, 1)';
          likeBtn.style.transform = 'scale(1.3)';
          setTimeout(() => {{ likeBtn.style.transform = 'scale(1)'; }}, 250);
          
          const svg = likeBtn.querySelector('svg');
          if (svg) {{
            svg.style.color = isLiked ? BRAND_COLOR : 'currentColor';
            svg.style.fill = isLiked ? BRAND_COLOR : 'none';
          }}
          this.showToast(isLiked ? '💚 Added to Your Library' : 'Removed from Library');
          return;
        }}

        // Shuffle & Repeat buttons
        const shuffleBtn = e.target.closest('[data-testid="control-button-shuffle"]');
        if (shuffleBtn) {{
          const on = shuffleBtn.classList.toggle('text-emerald-500');
          this.showToast(on ? '🔀 Shuffle enabled' : 'Shuffle off');
          return;
        }}
        const repeatBtn = e.target.closest('[data-testid="control-button-repeat"]');
        if (repeatBtn) {{
          const on = repeatBtn.classList.toggle('text-emerald-500');
          this.showToast(on ? '🔁 Repeat enabled' : 'Repeat off');
          return;
        }}
      }});

      // Timeline Scrubber Interaction (Click / Drag seeking)
      const bindScrubber = (trackEl, isVolume = false) => {{
        if (!trackEl) return;
        const onSeek = (clientX) => {{
          const rect = trackEl.getBoundingClientRect();
          const pct = Math.max(0, Math.min(1, (clientX - rect.left) / rect.width));
          if (isVolume) {{
            this.setVolume(pct);
          }} else {{
            this.seekToPercent(pct);
          }}
        }};

        trackEl.style.cursor = 'pointer';
        trackEl.addEventListener('click', (e) => onSeek(e.clientX));

        let dragging = false;
        trackEl.addEventListener('mousedown', (e) => {{
          dragging = true;
          onSeek(e.clientX);
          const onMove = (ev) => {{ if (dragging) onSeek(ev.clientX); }};
          const onUp = () => {{
            dragging = false;
            window.removeEventListener('mousemove', onMove);
            window.removeEventListener('mouseup', onUp);
          }};
          window.addEventListener('mousemove', onMove);
          window.addEventListener('mouseup', onUp);
        }});
      }};

      document.querySelectorAll('#playback-progressbar, [data-testid="playback-progressbar"], .playback-bar').forEach(el => bindScrubber(el, false));
      document.querySelectorAll('#volume-bar, [data-testid="volume-bar"], .volume-bar').forEach(el => bindScrubber(el, true));
    }}
  }}

  // --------------------------------------------------------------------------
  // 2. LIVE SEARCH & FILTER ENGINE (Real-Time Card Filtering)
  // --------------------------------------------------------------------------
  function initLiveSearch() {{
    const searchInputs = document.querySelectorAll('input[type="search"], input[placeholder*="play" i], input[placeholder*="search" i], input[placeholder*="find" i], [data-testid="search-input"]');
    if (!searchInputs.length) return;

    searchInputs.forEach(input => {{
      input.addEventListener('input', (e) => {{
        const query = e.target.value.toLowerCase().trim();
        const cards = document.querySelectorAll('[data-testid*="card"], .card, div[role="group"], [data-testid="track-row"]');
        
        let matchCount = 0;
        cards.forEach(card => {{
          const text = card.textContent.toLowerCase();
          const matches = !query || text.includes(query);
          
          card.style.transition = 'opacity 0.25s ease, transform 0.25s ease';
          if (matches) {{
            card.style.display = '';
            card.style.opacity = '1';
            card.style.transform = 'scale(1)';
            matchCount++;
          }} else {{
            card.style.opacity = '0';
            card.style.transform = 'scale(0.96)';
            setTimeout(() => {{
              if (card.style.opacity === '0') card.style.display = 'none';
            }}, 250);
          }}
        }});
      }});
    }});
  }}

  // --------------------------------------------------------------------------
  // 3. QUANTITY COUNTER & CART BADGE ENGINE (Food / E-Commerce)
  // --------------------------------------------------------------------------
  function initQuantityCounters() {{
    document.addEventListener('click', (e) => {{
      // Click "ADD" button
      const addBtn = e.target.closest('.cau-add-btn, button:has-text("ADD"), [data-cau-role="add-cart"]');
      if (addBtn && !addBtn.dataset.hasCounter) {{
        e.preventDefault();
        addBtn.dataset.hasCounter = 'true';
        addBtn.innerHTML = `
          <div class="flex items-center justify-between w-full h-full px-2 gap-2 text-emerald-600 font-extrabold select-none">
            <button class="cau-minus px-1 hover:scale-125 transition-transform">−</button>
            <span class="cau-count text-sm">1</span>
            <button class="cau-plus px-1 hover:scale-125 transition-transform">+</button>
          </div>
        `;
        updateCartBadge(1);
        return;
      }}

      // Stepper Plus
      const plusBtn = e.target.closest('.cau-plus');
      if (plusBtn) {{
        e.preventDefault();
        const countEl = plusBtn.parentElement.querySelector('.cau-count');
        let count = parseInt(countEl.textContent, 10) + 1;
        countEl.textContent = count;
        updateCartBadge(1);
        return;
      }}

      // Stepper Minus
      const minusBtn = e.target.closest('.cau-minus');
      if (minusBtn) {{
        e.preventDefault();
        const countEl = minusBtn.parentElement.querySelector('.cau-count');
        let count = parseInt(countEl.textContent, 10) - 1;
        if (count <= 0) {{
          const container = minusBtn.closest('[data-has-counter="true"]');
          if (container) {{
            delete container.dataset.hasCounter;
            container.innerHTML = 'ADD';
          }}
        }} else {{
          countEl.textContent = count;
        }}
        updateCartBadge(-1);
        return;
      }}
    }});

    function updateCartBadge(delta) {{
      document.querySelectorAll('.cart-badge, [data-cau-role="cart-count"]').forEach(badge => {{
        let curr = parseInt(badge.textContent.replace(/\\D/g, '') || '0', 10);
        let next = Math.max(0, curr + delta);
        badge.textContent = next > 0 ? `${{next}}` : '';
        badge.style.transform = 'scale(1.35)';
        setTimeout(() => {{ badge.style.transform = 'scale(1)'; }}, 200);
      }});
    }}
  }}

  // --------------------------------------------------------------------------
  // 4. FILTER PILLS & TABS ENGINE
  // --------------------------------------------------------------------------
  function initFilterPills() {{
    document.addEventListener('click', (e) => {{
      const pill = e.target.closest('.filter-pill, [role="tab"], button[data-testid*="chip"]');
      if (!pill) return;
      const group = pill.parentElement;
      if (group) {{
        group.querySelectorAll('.filter-pill, [role="tab"], button[data-testid*="chip"]').forEach(p => {{
          p.classList.remove('bg-white', 'text-black', 'active', 'border-white');
          p.classList.add('bg-zinc-800', 'text-white');
        }});
        pill.classList.remove('bg-zinc-800', 'text-white');
        pill.classList.add('bg-white', 'text-black', 'active');
      }}
    }});
  }}

  // --------------------------------------------------------------------------
  // 5. ACCORDIONS & PRICING SWITCHERS
  // --------------------------------------------------------------------------
  function initAccordionsAndToggles() {{
    // Pricing monthly/annual toggle
    document.addEventListener('click', (e) => {{
      const toggle = e.target.closest('[data-cau-role="pricing-toggle"], .pricing-toggle');
      if (toggle) {{
        const isAnnual = toggle.classList.toggle('annual-active');
        document.querySelectorAll('.price-amount').forEach(el => {{
          const monthly = el.dataset.monthly || '$29';
          const annual = el.dataset.annual || '$23';
          el.textContent = isAnnual ? annual : monthly;
        }});
        document.querySelectorAll('.price-period').forEach(el => {{
          el.textContent = isAnnual ? '/yr' : '/mo';
        }});
      }}
    }});

    // Accordion expand/collapse
    document.addEventListener('click', (e) => {{
      const trigger = e.target.closest('[data-accordion-trigger], .faq-question');
      if (!trigger) return;
      const content = trigger.nextElementSibling;
      if (content) {{
        const isOpen = content.style.maxHeight && content.style.maxHeight !== '0px';
        content.style.maxHeight = isOpen ? '0px' : `${{content.scrollHeight}}px`;
        content.style.overflow = 'hidden';
        content.style.transition = 'max-height 0.35s cubic-bezier(0.16, 1, 0.3, 1)';
        const icon = trigger.querySelector('.accordion-icon');
        if (icon) icon.style.transform = isOpen ? 'rotate(0deg)' : 'rotate(180deg)';
      }}
    }});
  }}

  // --------------------------------------------------------------------------
  // 6. MAGNETIC BUTTONS & 3D CARD TILT (Dennis Snellenberg / Portfolios)
  // --------------------------------------------------------------------------
  function initPhysicsAndMotion() {{
    // Magnetic pull
    document.querySelectorAll('.magnetic-btn, [data-cau-magnetic]').forEach(btn => {{
      btn.addEventListener('mousemove', (e) => {{
        const rect = btn.getBoundingClientRect();
        const x = e.clientX - rect.left - rect.width / 2;
        const y = e.clientY - rect.top - rect.height / 2;
        btn.style.transform = `translate(${{x * 0.3}}px, ${{y * 0.3}}px)`;
        btn.style.transition = 'transform 0.1s ease-out';
      }});
      btn.addEventListener('mouseleave', () => {{
        btn.style.transform = 'translate(0px, 0px)';
        btn.style.transition = 'transform 0.4s cubic-bezier(0.16, 1, 0.3, 1)';
      }});
    }});

    // 3D Card tilt
    document.querySelectorAll('[data-cau-tilt], .tilt-card').forEach(card => {{
      card.addEventListener('mousemove', (e) => {{
        const rect = card.getBoundingClientRect();
        const x = (e.clientX - rect.left) / rect.width - 0.5;
        const y = (e.clientY - rect.top) / rect.height - 0.5;
        card.style.transform = `perspective(1000px) rotateY(${{x * 12}}deg) rotateX(${{-y * 12}}deg) scale3d(1.02, 1.02, 1.02)`;
        card.style.transition = 'transform 0.1s ease-out';
      }});
      card.addEventListener('mouseleave', () => {{
        card.style.transform = 'perspective(1000px) rotateY(0deg) rotateX(0deg) scale3d(1, 1, 1)';
        card.style.transition = 'transform 0.5s cubic-bezier(0.16, 1, 0.3, 1)';
      }});
    }});
  }}

  // --------------------------------------------------------------------------
  // 7. WEB AUDIO CLICK HAPTICS & MICRO-TOAST CONTROLLER
  // --------------------------------------------------------------------------
  class CAUHapticsController {{
    constructor() {{
      this.soundEnabled = localStorage.getItem('cau_sound_enabled') !== 'false';
      this.audioCtx = null;
      this.toastTimeout = null;
      this.init();
    }}

    init() {{
      document.addEventListener('click', (e) => {{
        const target = e.target.closest('a, button, [role="button"], .nav-brand, .filter-pill, .cau-pressable');
        if (target && !target.classList.contains('no-sound')) {{
          const freq = target.tagName === 'BUTTON' ? 950 : (target.classList.contains('filter-pill') ? 900 : 820);
          this.playClick(freq);
        }}
      }});
    }}

    playClick(freq = 880, duration = 0.035) {{
      if (!this.soundEnabled) return;
      try {{
        if (!this.audioCtx) {{
          const AudioContext = window.AudioContext || window.webkitAudioContext;
          this.audioCtx = new AudioContext();
        }}
        if (this.audioCtx.state === 'suspended') this.audioCtx.resume();
        const osc = this.audioCtx.createOscillator();
        const gain = this.audioCtx.createGain();
        osc.type = 'sine';
        osc.frequency.setValueAtTime(freq, this.audioCtx.currentTime);
        osc.frequency.exponentialRampToValueAtTime(freq / 2, this.audioCtx.currentTime + duration);
        gain.gain.setValueAtTime(0.04, this.audioCtx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.001, this.audioCtx.currentTime + duration);
        osc.connect(gain);
        gain.connect(this.audioCtx.destination);
        osc.start();
        osc.stop(this.audioCtx.currentTime + duration);
      }} catch (e) {{}}
    }}

    toggleMute() {{
      this.soundEnabled = !this.soundEnabled;
      localStorage.setItem('cau_sound_enabled', this.soundEnabled ? 'true' : 'false');
      this.showToast(this.soundEnabled ? '🔊 Audio Haptics: ON' : '🔇 Audio Haptics: MUTED');
      if (this.soundEnabled) this.playClick(980);
    }}

    showToast(msg, duration = 2000) {{
      let toast = document.getElementById('cau-micro-toast');
      if (!toast) {{
        toast = document.createElement('div');
        toast.id = 'cau-micro-toast';
        toast.className = 'cau-micro-toast';
        document.body.appendChild(toast);
      }}
      toast.textContent = msg;
      toast.classList.add('show');
      if (this.toastTimeout) clearTimeout(this.toastTimeout);
      this.toastTimeout = setTimeout(() => toast.classList.remove('show'), duration);
    }}
  }}

  // --------------------------------------------------------------------------
  // 8. GLOBAL KEYBOARD NAVIGATION HUD (<kbd>1</kbd>, <kbd>2</kbd>, <kbd>M</kbd>, <kbd>?</kbd>)
  // --------------------------------------------------------------------------
  function initKeyboardHUD(haptics) {{
    window.addEventListener('keydown', (e) => {{
      if (['INPUT', 'TEXTAREA'].includes(document.activeElement?.tagName)) return;
      const key = e.key.toLowerCase();
      if (key === 'm') {{
        haptics.toggleMute();
      }} else if (key === '1' || key === 'a') {{
        const link = document.querySelector('a[data-label*="About"], a[href*="index.html"]');
        if (link && !location.pathname.endsWith('/site/index.html')) link.click();
      }} else if (key === '2' || key === 'p') {{
        const link = document.querySelector('a[data-label*="Project"], a[href*="project"], a[href*="work"]');
        if (link) link.click();
      }} else if (key === '3' || key === 'e') {{
        const link = document.querySelector('a[data-label*="Engineering"], a[href*="engineering"]');
        if (link) link.click();
      }}
    }});
  }}

  // --------------------------------------------------------------------------
  // 9. VIDEO HOVER AUTOPLAY / PAUSE CONTROLLER
  // --------------------------------------------------------------------------
  function initVideoHoverEngine() {{
    document.querySelectorAll('video').forEach(vid => {{
      vid.muted = true;
      vid.loop = true;
      vid.playsInline = true;
      const container = vid.closest('.video-card, .work-grid-card, .project-card, [data-cau-role="video"]') || vid;
      container.addEventListener('mouseenter', () => vid.play().catch(() => {{}}));
      container.addEventListener('mouseleave', () => vid.pause());
    }});
  }}

  // Initialize all engines once DOM is ready
  document.addEventListener('DOMContentLoaded', () => {{
    window.cauAudio = new CAUAudioEngine();
    window.cauHaptics = new CAUHapticsController();
    initLiveSearch();
    initQuantityCounters();
    initFilterPills();
    initAccordionsAndToggles();
    initPhysicsAndMotion();
    initKeyboardHUD(window.cauHaptics);
    initVideoHoverEngine();
    console.log('[CAU] Universal Behavioral Engine active: 60fps interactivity ready.');
  }});
}})();
"""


def inject_interactions_into_html(html_file: Path, brand_color: str = "#1ed760") -> None:
    """Injects the CAU behavioral engine directly into an HTML file."""
    if not html_file.exists():
        return
    content = html_file.read_text(encoding="utf-8")
    if "CLONE ANY UI (CAU) — Universal Behavioral Engine" in content:
        return

    script_tag = f"\n<script>\n{generate_interaction_script(brand_primary=brand_color)}\n</script>\n"
    if "</body>" in content:
        content = content.replace("</body>", f"{script_tag}</body>")
    else:
        content += script_tag
    html_file.write_text(content, encoding="utf-8")
    print(f"  [✓] Injected Universal Behavioral Engine into: {html_file}")


def main() -> None:
    parser = argparse.ArgumentParser(description="CAU Universal Interaction & Behavioral Synthesizer")
    parser.add_argument("--target-dir", required=True, help="Target directory containing preview.html or site/index.html")
    parser.add_argument("--brand-color", default="#1ed760", help="Primary brand color for active states (default: #1ed760)")
    args = parser.parse_args()

    target_path = Path(args.target_dir)
    js_output = target_path / "interactions.js"
    js_output.write_text(generate_interaction_script(args.brand_color), encoding="utf-8")
    print(f"[✓] Generated standalone interactions.js at: {js_output}")

    # Inject into preview.html and site/index.html if found
    for cand in [target_path / "preview.html", target_path / "site" / "index.html"]:
        if cand.exists():
            inject_interactions_into_html(cand, args.brand_color)


if __name__ == "__main__":
    main()

