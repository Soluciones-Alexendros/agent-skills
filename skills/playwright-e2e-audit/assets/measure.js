/**
 * measure.js — snippet para page.evaluate() en Playwright.
 * Devuelve mediciones listas para scripts/measure_analyze.py.
 *
 * Uso:
 *   const m = await page.evaluate(MEASURE_SNIPPET);
 *   fs.writeFileSync('output/measurements.json', JSON.stringify(m));
 */
() => {
  const clickableSel = 'button, a[href], [role="button"], [role="link"], input, select, textarea, [tabindex]:not([tabindex="-1"])';
  const clickableSet = new Set();
  document.querySelectorAll(clickableSel).forEach(el => clickableSet.add(el));

  const selectorOf = (el) => {
    let s = el.tagName.toLowerCase();
    if (el.id) s += '#' + el.id;
    if (el.classList.length) s += '.' + [...el.classList].slice(0, 3).join('.');
    return s;
  };

  const elements = [...document.querySelectorAll('body *')]
    .map(el => {
      const r = el.getBoundingClientRect();
      if (r.width <= 0 || r.height <= 0 || r.width > window.innerWidth * 2) return null;
      const s = getComputedStyle(el);
      const e = {
        selector: selectorOf(el),
        tag: el.tagName,
        w: Math.round(r.width), h: Math.round(r.height),
        x: Math.round(r.x), y: Math.round(r.y),
        clickable: clickableSet.has(el),
        text: (el.innerText || el.value || el.getAttribute('aria-label') || '').slice(0, 60),
      };
      if (el.tagName === 'IMG') {
        e.naturalW = el.naturalWidth; e.naturalH = el.naturalHeight;
      }
      const fs = parseFloat(s.fontSize);
      if (el.innerText && el.innerText.trim().length > 20) {
        e.fontSize = s.fontSize; e.lineHeight = s.lineHeight;
      }
      if (el.tagName === 'HEADER') e.tag = 'HEADER';
      return e;
    })
    .filter(Boolean);

  return {
    url: location.href,
    viewport: { w: window.innerWidth, h: window.innerHeight },
    documentWidth: document.documentElement.scrollWidth,
    documentHeight: document.documentElement.scrollHeight,
    elements,
  };
}
