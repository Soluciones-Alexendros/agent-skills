# Matriz de checks — vista rápida

Fuente de verdad: `configs/checks.json` (42 checks). Estados: PASS ✅ / FAIL ❌ / WARN ⚠️ / N/A ➖ / PENDING 🔎. WARN cuenta como incumplimiento parcial; FAIL exige evidencia (locator/screenshot/console/network) — el validador lo fuerza.

## Rutas (RT, peso 0.10)
RT-01 rutas 200 sin 404/500 (Crítica) · RT-02 sin cadenas/bucles de redirect · RT-03 404 personalizada · RT-04 crawl acotado

## Funcional (FN, peso 0.20)
FN-01 todo botón/enlace responde sin pageerror (Crítica) · FN-02 sin requests ≥400 · FN-03 dropdowns cierran ESC/click-fuera · FN-04 modales con focus trap + retorno de foco · FN-05 sin doble submit · FN-06 estados de carga/empty states

## Formularios (FM, peso 0.15)
FM-01 pasada A vacío → validación visible + aria-describedby (Crítica) · FM-02 pasada B inválidos bloquean · FM-03 pasada C válido → éxito sin 500 (Crítica) · FM-04 labels asociados (Crítica) · FM-05 datos contextuales · FM-06 autocomplete

## UI/UX (UI, peso 0.15)
UI-01 touch targets ≥44px (mín 24px, WCAG 2.5.8) · UI-02 font ≥12px, line-height ≥1.4 · UI-03 grid 8pt · UI-04 imágenes sin distorsión · UI-05 sin overflow horizontal (Crítica) · UI-06 jerarquía CTA/header ≤25% · UI-07 consistencia desktop/mobile

## Accesibilidad (AC, peso 0.15)
AC-01 0 violaciones axe critical/serious (Crítica) · AC-02 contraste 4.5:1/3:1 · AC-03 teclado + foco visible (Crítica) · AC-04 skip link/landmarks/h1/lang · AC-05 alt y nombres accesibles

## Performance (PF, peso 0.10)
PF-01 LCP ≤2.5s · PF-02 CLS ≤0.1 · PF-03 INP ≤200ms · PF-04 sin bloqueo de render por terceros

## SEO (SE, peso 0.05)
SE-01 title 50–60 + description 120–158 · SE-02 h1 único/canonical/OG/schema · SE-03 robots + sitemap

## Seguridad (SG, peso 0.05)
SG-01 password + autocomplete=new-password · SG-02 sin tokens/PII en localStorage, cookies Secure+SameSite (Crítica) · SG-03 sin mixed content · SG-04 cabeceras de seguridad

## Motion (MO, peso 0.05)
MO-01 prefers-reduced-motion · MO-02 transiciones ≤500ms, animaciones pausables · MO-03 sin bloqueo de pointer-events/thrashing

## Veredicto (configs/thresholds.json)
- **APTO**: 0 FAIL Críticas y global ≥90%.
- **APTO CON OBSERVACIONES**: 0 FAIL Críticas y 70–89%.
- **NO APTO**: cualquier FAIL Crítica, o global <70%.
- N/A excluido del denominador; PENDING se lista como verificación pendiente en el informe.
