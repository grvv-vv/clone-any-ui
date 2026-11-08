/**
 * ⚡ CLONE ANY UI (CAU) — Universal 1-Click In-Browser DOM & Asset Extractor
 * 
 * Paste this in your browser DevTools Console (F12 -> Console) on ANY website in the world.
 * It bypasses Cloudflare, Turnstile, Auth walls & CAPTCHAs by extracting the live, fully
 * hydrated DOM directly from your active browser session into your clipboard!
 * 
 * Usage:
 * 1. Open target website in Chrome/Edge/Firefox/Brave
 * 2. Press F12 -> Console -> Paste this script -> Press Enter
 * 3. In terminal run: python clone_any_ui.py --clipboard --url <site-url> --out ./clone --all
 */
(() => {
  'use strict';

  console.log('%c⚡ [CAU] Starting Universal Deep DOM & Asset Extraction...', 'color: #3b82f6; font-size: 14px; font-weight: bold;');

  // 1. Clone Document Root
  const cloneDoc = document.documentElement.cloneNode(true);

  // 2. Snapshot Active Canvas & WebGL Scenes
  const originalCanvases = document.querySelectorAll('canvas');
  const clonedCanvases = cloneDoc.querySelectorAll('canvas');

  originalCanvases.forEach((origCanvas, i) => {
    try {
      const dataUrl = origCanvas.toDataURL('image/webp', 0.95);
      if (dataUrl && dataUrl.length > 100) {
        const clonedCanvas = clonedCanvases[i];
        if (clonedCanvas) {
          const img = cloneDoc.createElement('img');
          img.className = 'cau-canvas-fallback';
          img.src = dataUrl;
          img.setAttribute('alt', 'Canvas snapshot');
          img.style.cssText = 'position:absolute; inset:0; width:100%; height:100%; object-fit:cover; pointer-events:none; z-index:0;';
          if (clonedCanvas.parentElement) {
            clonedCanvas.parentElement.style.position = 'relative';
            clonedCanvas.parentElement.insertBefore(img, clonedCanvas.nextSibling);
          }
        }
      }
    } catch (e) {}
  });

  // 3. Inline SVG <use> references from symbols
  cloneDoc.querySelectorAll('svg use').forEach(use => {
    try {
      const href = use.getAttribute('href') || use.getAttribute('xlink:href');
      if (href && href.startsWith('#')) {
        const symbol = document.querySelector(href);
        if (symbol) {
          const parentSvg = use.closest('svg');
          if (parentSvg) {
            Array.from(symbol.childNodes).forEach(c => parentSvg.appendChild(c.cloneNode(true)));
            use.remove();
          }
        }
      }
    } catch (e) {}
  });

  // 4. Flatten Accessible Shadow DOMs
  function unshadow(sourceEl, targetEl) {
    if (!sourceEl || !targetEl) return;
    if (sourceEl.shadowRoot) {
      const shadowContainer = cloneDoc.createElement('div');
      shadowContainer.setAttribute('data-cau-shadow-root', 'true');
      shadowContainer.innerHTML = sourceEl.shadowRoot.innerHTML;
      targetEl.appendChild(shadowContainer);
    }
    const sourceChildren = Array.from(sourceEl.children || []);
    const targetChildren = Array.from(targetEl.children || []);
    sourceChildren.forEach((child, idx) => {
      if (targetChildren[idx]) unshadow(child, targetChildren[idx]);
    });
  }
  unshadow(document.body, cloneDoc.querySelector('body'));

  // 5. Inject Anti-Hotlink Referrer Policy
  let head = cloneDoc.querySelector('head');
  if (head && !head.querySelector('meta[name="referrer"]')) {
    const meta = cloneDoc.createElement('meta');
    meta.name = 'referrer';
    meta.content = 'no-referrer';
    head.insertBefore(meta, head.firstChild);
  }

  // 6. Purge Tracker Scripts & Beacons
  cloneDoc.querySelectorAll('script').forEach(s => {
    const src = (s.getAttribute('src') || '').toLowerCase();
    const content = s.textContent.toLowerCase();
    if (
      src.includes('google-analytics') ||
      src.includes('googletagmanager') ||
      src.includes('facebook') ||
      src.includes('hotjar') ||
      src.includes('clarity.ms') ||
      src.includes('sentry') ||
      content.includes('gtag(') ||
      content.includes('fbq(')
    ) {
      s.remove();
    }
  });

  // 7. Output to Clipboard & Download Option
  const finalHtml = '<!DOCTYPE html>\n' + cloneDoc.outerHTML;

  // Copy to clipboard
  if (navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard.writeText(finalHtml).then(() => {
      console.log('%c✅ [CAU] Live Hydrated DOM copied to clipboard! (' + Math.round(finalHtml.length / 1024) + ' KB)', 'color: #10b981; font-size: 14px; font-weight: bold;');
      console.log('%c👉 Now run in your terminal:\\npython clone_any_ui.py --clipboard --url ' + window.location.href + ' --out ./my-clone --all', 'color: #f59e0b; font-size: 13px;');
    }).catch(() => {
      fallbackDownload(finalHtml);
    });
  } else {
    fallbackDownload(finalHtml);
  }

  function fallbackDownload(html) {
    const blob = new Blob([html], { type: 'text/html' });
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = 'cau_dom_dump.html';
    document.body.appendChild(a);
    a.click();
    a.remove();
    console.log('%c✅ [CAU] DOM saved as cau_dom_dump.html (Copy to your clone workspace)', 'color: #10b981; font-size: 14px; font-weight: bold;');
  }
})();

