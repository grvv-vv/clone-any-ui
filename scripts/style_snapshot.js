/**
 * Style Snapshot Extractor for Web UI Replicator
 * 
 * Injects into browser context or DevTools console to extract computed styles,
 * CSS variables, and geometry for targeted selectors.
 * 
 * Usage in Console or Playwright:
 *   const result = window.webUiReplicatorSnapshot(['h1', 'header', '.hero', '.card', 'button']);
 *   copy(JSON.stringify(result, null, 2));
 */
(function setupWebUiReplicatorSnapshot(global) {
  const CORE_PROPERTIES = [
    'fontFamily', 'fontSize', 'fontWeight', 'lineHeight', 'letterSpacing',
    'color', 'backgroundColor', 'backgroundImage',
    'borderTopColor', 'borderTopWidth', 'borderTopStyle', 'borderRadius', 'boxShadow',
    'paddingTop', 'paddingRight', 'paddingBottom', 'paddingLeft',
    'marginTop', 'marginRight', 'marginBottom', 'marginLeft',
    'display', 'flexDirection', 'justifyContent', 'alignItems', 'gap',
    'width', 'height', 'maxWidth', 'position',
    // Motion & Movement Properties
    'transform', 'transformOrigin', 'willChange',
    'transition', 'transitionProperty', 'transitionDuration', 'transitionTimingFunction', 'transitionDelay',
    'animation', 'animationName', 'animationDuration', 'animationTimingFunction', 'animationIterationCount'
  ];

  function extractNode(selector) {
    const el = document.querySelector(selector);
    if (!el) {
      return { selector, found: false };
    }
    const computed = window.getComputedStyle(el);
    const rect = el.getBoundingClientRect();

    const styles = {};
    for (const prop of CORE_PROPERTIES) {
      styles[prop] = computed[prop];
    }

    return {
      selector,
      found: true,
      tagName: el.tagName.toLowerCase(),
      className: typeof el.className === 'string' ? el.className : '',
      textSnippet: (el.textContent || '').trim().replace(/\s+/g, ' ').slice(0, 100),
      rect: {
        x: Math.round(rect.x * 10) / 10,
        y: Math.round(rect.y * 10) / 10,
        width: Math.round(rect.width * 10) / 10,
        height: Math.round(rect.height * 10) / 10
      },
      style: styles
    };
  }

  function extractLiveMotionCatalog() {
    const keyframes = {};
    const hoverInteractions = [];

    try {
      for (const sheet of document.styleSheets) {
        try {
          const rules = sheet.cssRules || sheet.rules;
          if (!rules) continue;
          for (const rule of rules) {
            if (rule.type === CSSRule.KEYFRAMES_RULE || rule.constructor.name === 'CSSKeyframesRule') {
              const name = rule.name;
              keyframes[name] = rule.cssText;
            } else if (rule.type === CSSRule.STYLE_RULE) {
              const sel = rule.selectorText || '';
              if (sel.includes(':hover') || sel.includes(':active') || sel.includes(':focus')) {
                const text = rule.style.cssText;
                if (/transform|transition|scale|translate|box-shadow|opacity/i.test(text)) {
                  hoverInteractions.push({
                    selector: sel,
                    cssText: text
                  });
                }
              }
            }
          }
        } catch (e) {
          // Cross-origin stylesheet access restriction - continue
        }
      }
    } catch (err) {
      // Ignore
    }

    return {
      keyframesCount: Object.keys(keyframes).length,
      keyframes,
      hoverInteractionsCount: hoverInteractions.length,
      hoverInteractions: hoverInteractions.slice(0, 25)
    };
  }

  function takeSnapshot(selectors) {
    const list = selectors || ['header', 'h1', 'h2', 'main', 'button', 'footer', '.card'];
    const targets = list.map(extractNode);
    const motionCatalog = extractLiveMotionCatalog();

    return {
      url: window.location.href,
      title: document.title,
      timestamp: new Date().toISOString(),
      viewport: {
        width: window.innerWidth,
        height: window.innerHeight,
        devicePixelRatio: window.devicePixelRatio
      },
      motionCatalog,
      targets
    };
  }

  global.cauSnapshot = takeSnapshot;
  global.cauExtractMotionCatalog = extractLiveMotionCatalog;
  global.cloneAnyUiSnapshot = takeSnapshot;
  global.webUiReplicatorSnapshot = takeSnapshot;
})(window);

