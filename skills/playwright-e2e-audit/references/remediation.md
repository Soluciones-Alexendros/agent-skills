# Plan de remediación RICE y criterios de aceptación

Leer en FASE 7. Cada tarea del plan sigue: **PROBLEMA → CAUSA RAÍZ → SOLUCIÓN CON CÓDIGO → CRITERIO DE ACEPTACIÓN (test Playwright que debe pasar)**.

## Sprints (configs/thresholds.json)

| Sprint | Plazo | Severidades | Objetivo |
|---|---|---|---|
| Sprint 0 | 48 h | Crítica | Estabilizar: la web no rompe ni pierde conversiones |
| Sprint 1 | Semana 1 | Alta | Usable y accesible: 100% funcional + WCAG AA |
| Sprint 2 | Semana 2 | Media | Profesionalizar: CWV verde y UI unificada |
| Sprint 3 | Semana 3 | Baja | SEO y delight: pulido final |

RICE = Reach × Impact × Confidence / Effort. Defaults por severidad: Crítica 9·9·8/3=216, Alta 7·7·8/4=98, Media 5·5·7/5=35, Baja 3·3·7/3=21. Ajustar R/I/C/E por hallazgo cuando haya datos (tráfico de la URL, tasa de conversión afectada); `score.py` recalcula.

## Templates de solución por patrón de hallazgo

### Touch targets pequeños (UI-01)
```css
.btn, a[role="button"] { min-height: 44px; min-width: 44px; padding: 12px 24px; }
/* Iconos: mantener hit-area 44px aunque el glyph sea 24px (padding transparente) */
```
Criterio de aceptación:
```typescript
test('UI-01 touch targets', async ({ page }) => {
  await page.goto('/pricing');
  for (const b of await page.getByRole('button').all()) {
    const box = await b.boundingBox();
    expect(Math.min(box!.width, box!.height)).toBeGreaterThanOrEqual(24);
  }
});
```

### Validación de formulario accesible (FM-01)
```html
<label for="email">Email *</label>
<input id="email" type="email" required aria-describedby="email-error">
<span id="email-error" role="alert"></span>
```
```typescript
test('FM-01 submit vacío muestra error accesible', async ({ page }) => {
  await page.goto('/contacto');
  await page.getByRole('button', { name: /enviar/i }).click();
  await expect(page.locator('#email-error')).toBeVisible();
  await expect(page.locator('#email')).toHaveAttribute('aria-invalid', 'true');
});
```

### Overflow horizontal (UI-05)
```typescript
test('UI-05 sin overflow', async ({ page }) => {
  await page.goto('/');
  const overflow = await page.evaluate(() =>
    document.documentElement.scrollWidth - window.innerWidth);
  expect(overflow).toBeLessThanOrEqual(1);
});
```

### prefers-reduced-motion (MO-01)
```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { animation-duration: 0.01ms !important; transition-duration: 0.01ms !important; }
}
```
```typescript
test('MO-01 reduced motion', async ({ page }) => {
  await page.emulateMedia({ reducedMotion: 'reduce' });
  await page.goto('/');
  const d = await page.locator('.carousel').evaluate(el => getComputedStyle(el).transitionDuration);
  expect(parseFloat(d)).toBeLessThanOrEqual(0.01);
});
```

### Seguridad de sesión (SG-02)
```typescript
test('SG-02 sin tokens en localStorage', async ({ page }) => {
  await page.goto('/');
  const keys = await page.evaluate(() => Object.keys(localStorage));
  expect(keys.filter(k => /token|jwt|secret|password/i.test(k))).toEqual([]);
});
```

## Cierre

1. Todo Sprint 0 verificado con su test de aceptación en CI antes de declarar estabilizado.
2. Re-auditoría parcial tras Sprint 1 (axe + formularios + teclado) y completa tras Sprint 3.
3. Verificación de cierre: 0 FAIL Críticas + % por categoría + veredicto, como en la tabla final de REPORT.md.
