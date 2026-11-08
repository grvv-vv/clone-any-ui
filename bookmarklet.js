// CLONE ANY UI (CAU) — 1-Click Browser Bookmarklet
// Drag this to your browser's bookmarks bar or create a new bookmark with this URL:
javascript:(function(){
  try {
    const clone = document.documentElement.cloneNode(true);

    // 1. Snapshot Canvases / WebGL
    const origCanvases = document.querySelectorAll('canvas');
    const cloneCanvases = clone.querySelectorAll('canvas');
    origCanvases.forEach((c, i) => {
      try {
        const u = c.toDataURL('image/webp', 0.95);
        if (u && u.length > 100 && cloneCanvases[i]) {
          const img = clone.createElement('img');
          img.className = 'cau-canvas-fallback';
          img.src = u;
          img.style.cssText = 'position:absolute;inset:0;width:100%;height:100%;object-fit:cover;pointer-events:none;z-index:0;';
          if (cloneCanvases[i].parentElement) {
            cloneCanvases[i].parentElement.style.position = 'relative';
            cloneCanvases[i].parentElement.insertBefore(img, cloneCanvases[i].nextSibling);
          }
        }
      } catch(e){}
    });

    // 2. Inline SVG symbols
    clone.querySelectorAll('svg use').forEach(u => {
      try {
        const h = u.getAttribute('href') || u.getAttribute('xlink:href');
        if (h && h.startsWith('#')) {
          const s = document.querySelector(h);
          if (s && u.closest('svg')) {
            Array.from(s.childNodes).forEach(ch => u.closest('svg').appendChild(ch.cloneNode(true)));
            u.remove();
          }
        }
      } catch(e){}
    });

    // 3. Inject Anti-Hotlink Policy
    const head = clone.querySelector('head');
    if (head && !head.querySelector('meta[name="referrer"]')) {
      const m = clone.createElement('meta');
      m.name = 'referrer';
      m.content = 'no-referrer';
      head.insertBefore(m, head.firstChild);
    }

    // 4. Purge Trackers
    clone.querySelectorAll('script').forEach(s => {
      const src = (s.getAttribute('src') || '').toLowerCase();
      const txt = s.textContent.toLowerCase();
      if (src.includes('analytics') || src.includes('googletagmanager') || src.includes('facebook') || src.includes('hotjar') || src.includes('sentry') || txt.includes('gtag(')) {
        s.remove();
      }
    });

    const finalHtml = '<!DOCTYPE html>\n' + clone.outerHTML;

    // 5. Copy to clipboard
    navigator.clipboard.writeText(finalHtml).then(() => {
      showToast('⚡ CAU: Live DOM copied to clipboard (' + Math.round(finalHtml.length/1024) + ' KB)! Paste into your clone command.');
    }).catch(() => {
      const b = new Blob([finalHtml], { type: 'text/html' });
      const a = document.createElement('a');
      a.href = URL.createObjectURL(b);
      a.download = 'cau_dom_dump.html';
      document.body.appendChild(a);
      a.click();
      a.remove();
      showToast('⚡ CAU: Saved to cau_dom_dump.html');
    });

    function showToast(msg) {
      const t = document.createElement('div');
      t.textContent = msg;
      t.style.cssText = 'position:fixed;top:20px;right:20px;z-index:999999;background:#18181b;color:#f4f4f5;padding:12px 18px;border-radius:10px;font-family:system-ui,sans-serif;font-size:13px;font-weight:600;box-shadow:0 10px 25px rgba(0,0,0,0.5);border:1px solid rgba(255,255,255,0.15);transition:opacity 0.3s;';
      document.body.appendChild(t);
      setTimeout(() => { t.style.opacity = '0'; setTimeout(() => t.remove(), 300); }, 3500);
    }
  } catch(err) {
    alert('CAU Bookmarklet error: ' + err.message);
  }
})();
