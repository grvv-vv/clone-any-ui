/**
 * ⚡ CLONE ANY UI (CAU) — Portfolio Runtime Engine for Gaurav
 * Web Audio Synthesizer · Keyboard HUD Navigation · Micro-Toasts · Live Search & Counter
 */
(() => {
  'use strict';

  class GauravPortfolioRuntime {
    constructor() {
      this.soundEnabled = localStorage.getItem('gaurav_portfolio_sound') !== 'false';
      this.audioCtx = null;
      this.toastTimeout = null;
      this.init();
    }

    init() {
      this.setupSoundButton();
      this.setupKeyboardShortcuts();
      this.setupClickHaptics();
      this.setupShortcutsModal();
      this.setupVideoHoverPlay();
    }

    showToast(message, duration = 2200) {
      let toast = document.getElementById('cau-toast');
      if (!toast) {
        toast = document.createElement('div');
        toast.id = 'cau-toast';
        toast.className = 'cau-micro-toast';
        document.body.appendChild(toast);
      }
      toast.textContent = message;
      toast.classList.add('show');
      if (this.toastTimeout) clearTimeout(this.toastTimeout);
      this.toastTimeout = setTimeout(() => {
        toast.classList.remove('show');
      }, duration);
    }

    playTone(freq = 880, duration = 0.035, type = 'sine') {
      if (!this.soundEnabled) return;
      try {
        if (!this.audioCtx) {
          const AudioContext = window.AudioContext || window.webkitAudioContext;
          this.audioCtx = new AudioContext();
        }
        if (this.audioCtx.state === 'suspended') {
          this.audioCtx.resume();
        }
        const osc = this.audioCtx.createOscillator();
        const gain = this.audioCtx.createGain();
        osc.type = type;
        osc.frequency.setValueAtTime(freq, this.audioCtx.currentTime);
        osc.frequency.exponentialRampToValueAtTime(freq / 2, this.audioCtx.currentTime + duration);

        gain.gain.setValueAtTime(0.04, this.audioCtx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.001, this.audioCtx.currentTime + duration);

        osc.connect(gain);
        gain.connect(this.audioCtx.destination);
        osc.start();
        osc.stop(this.audioCtx.currentTime + duration);
      } catch (e) {}
    }

    toggleSound() {
      this.soundEnabled = !this.soundEnabled;
      localStorage.setItem('gaurav_portfolio_sound', this.soundEnabled ? 'true' : 'false');
      this.updateSoundButtonUI();
      if (this.soundEnabled) {
        this.playTone(980, 0.04);
        this.showToast('🔊 Audio Haptics: ON (Press M to mute)');
      } else {
        this.showToast('🔇 Audio Haptics: OFF (Press M to unmute)');
      }
    }

    setupSoundButton() {
      const navViewport = document.querySelector('.nav-viewport') || document.querySelector('.nav-wrapper');
      if (!navViewport || document.getElementById('sound-toggle')) return;

      const btn = document.createElement('button');
      btn.id = 'sound-toggle';
      btn.type = 'button';
      btn.className = `sound-toggle-btn ${this.soundEnabled ? 'is-active' : ''}`;
      btn.setAttribute('aria-label', 'Toggle audio haptics');
      btn.title = 'Toggle audio feedback (Key: M)';
      btn.innerHTML = `
        <span class="sound-bars" aria-hidden="true">
          <span></span><span></span><span></span>
        </span>
        <span class="sound-label">${this.soundEnabled ? 'Audio' : 'Muted'}</span>
      `;

      btn.addEventListener('click', (e) => {
        e.stopPropagation();
        this.toggleSound();
      });

      // Place next to nav or floated cleanly
      btn.style.cssText = `
        position: absolute;
        right: 1.25rem;
        top: 50%;
        transform: translateY(-50%);
        z-index: 50;
      `;
      navViewport.style.position = 'relative';
      navViewport.appendChild(btn);
    }

    updateSoundButtonUI() {
      const btn = document.getElementById('sound-toggle');
      if (!btn) return;
      if (this.soundEnabled) {
        btn.classList.add('is-active');
        const lbl = btn.querySelector('.sound-label');
        if (lbl) lbl.textContent = 'Audio';
      } else {
        btn.classList.remove('is-active');
        const lbl = btn.querySelector('.sound-label');
        if (lbl) lbl.textContent = 'Muted';
      }
    }

    setupClickHaptics() {
      document.addEventListener('click', (e) => {
        const target = e.target.closest('a, button, .nav-brand, .work-grid-card, .engineering-sidenav-item');
        if (target && target.id !== 'sound-toggle') {
          const freq = target.tagName === 'BUTTON' ? 950 : (target.classList.contains('nav-brand') ? 880 : 780);
          this.playTone(freq);
        }
      });
    }

    setupKeyboardShortcuts() {
      window.addEventListener('keydown', (e) => {
        // Ignore if focus is in an input or textarea
        if (['INPUT', 'TEXTAREA'].includes(document.activeElement?.tagName)) return;

        const key = e.key.toLowerCase();

        // 1 or A: About
        if (key === '1' || (key === 'a' && !e.metaKey && !e.ctrlKey)) {
          const aboutLink = document.querySelector('a[data-label="About"]') || document.querySelector('a[href*="index.html"]');
          if (aboutLink && !location.pathname.endsWith('/site/index.html') && location.pathname !== '/') {
            this.showToast('Navigating to About [1]...');
            this.playTone(880);
            setTimeout(() => aboutLink.click(), 120);
          }
        }
        // 2 or P: Projects
        else if (key === '2' || (key === 'p' && !e.metaKey && !e.ctrlKey)) {
          const projLink = document.querySelector('a[data-label="Projects"]') || document.querySelector('a[href*="projects"]');
          if (projLink && !location.pathname.includes('/projects/index.html')) {
            this.showToast('Navigating to Projects [2]...');
            this.playTone(920);
            setTimeout(() => projLink.click(), 120);
          }
        }
        // 3 or E: Engineering
        else if (key === '3' || (key === 'e' && !e.metaKey && !e.ctrlKey)) {
          const engLink = document.querySelector('a[data-label="& Engineering"]') || document.querySelector('a[href*="engineering"]');
          if (engLink && !location.pathname.includes('/engineering/index.html')) {
            this.showToast('Navigating to Engineering [3]...');
            this.playTone(960);
            setTimeout(() => engLink.click(), 120);
          }
        }
        // M: Mute/Audio toggle
        else if (key === 'm' && !e.metaKey && !e.ctrlKey) {
          this.toggleSound();
        }
        // ?: Help modal
        else if (key === '?' || (e.key === '/' && e.shiftKey)) {
          this.toggleShortcutsModal();
        }
        // Escape: Close shortcuts modal or case studies
        else if (e.key === 'Escape') {
          this.closeShortcutsModal();
        }
      });
    }

    setupShortcutsModal() {
      if (document.getElementById('shortcuts-modal')) return;

      const modal = document.createElement('div');
      modal.id = 'shortcuts-modal';
      modal.className = 'shortcuts-modal-backdrop';
      modal.innerHTML = `
        <div class="shortcuts-modal-card" role="dialog" aria-modal="true" aria-label="Keyboard Shortcuts">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:16px;">
            <h3 style="margin:0; font-size:15px; font-weight:700; color:#fff;">Keyboard Navigation HUD</h3>
            <button id="close-shortcuts-btn" style="background:none; border:none; color:#71717a; font-size:16px; cursor:pointer;">✕</button>
          </div>
          <div class="shortcut-row">
            <span>About Page</span>
            <kbd class="shortcut-key">1</kbd> or <kbd class="shortcut-key">A</kbd>
          </div>
          <div class="shortcut-row">
            <span>Projects Showcase</span>
            <kbd class="shortcut-key">2</kbd> or <kbd class="shortcut-key">P</kbd>
          </div>
          <div class="shortcut-row">
            <span>&amp; Engineering</span>
            <kbd class="shortcut-key">3</kbd> or <kbd class="shortcut-key">E</kbd>
          </div>
          <div class="shortcut-row">
            <span>Toggle Audio Haptics</span>
            <kbd class="shortcut-key">M</kbd>
          </div>
          <div class="shortcut-row">
            <span>Close Modals / Overlays</span>
            <kbd class="shortcut-key">ESC</kbd>
          </div>
          <div style="margin-top:16px; font-size:11px; color:#71717a; text-align:center;">
            Designed for Gaurav — AI Engineer
          </div>
        </div>
      `;

      modal.addEventListener('click', (e) => {
        if (e.target === modal) this.closeShortcutsModal();
      });

      document.body.appendChild(modal);

      document.getElementById('close-shortcuts-btn')?.addEventListener('click', () => {
        this.closeShortcutsModal();
      });
    }

    toggleShortcutsModal() {
      const modal = document.getElementById('shortcuts-modal');
      if (!modal) return;
      if (modal.classList.contains('is-open')) {
        this.closeShortcutsModal();
      } else {
        modal.classList.add('is-open');
        this.playTone(950);
      }
    }

    closeShortcutsModal() {
      const modal = document.getElementById('shortcuts-modal');
      if (modal && modal.classList.contains('is-open')) {
        modal.classList.remove('is-open');
        this.playTone(600);
      }
    }

    setupVideoHoverPlay() {
      document.querySelectorAll('video').forEach((vid) => {
        vid.muted = true;
        vid.loop = true;
        vid.playsInline = true;

        const container = vid.closest('.work-grid-card-shell, .video-item, .project-card, div') || vid;
        container.addEventListener('mouseenter', () => {
          vid.play().catch(() => {});
        });
        container.addEventListener('mouseleave', () => {
          vid.pause();
        });
      });
    }
  }

  // Auto-initialize when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
      window.gauravRuntime = new GauravPortfolioRuntime();
    });
  } else {
    window.gauravRuntime = new GauravPortfolioRuntime();
  }
})();
