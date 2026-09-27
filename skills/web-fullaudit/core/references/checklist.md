# Checklist Fullaudit — matriz de 93 checks unificados

Fuente de verdad máquina-legible: `core/configs/checks.json`
(`registry_version 3.0.0`). Vista rápida humana:

## Origen web-compliance (51) — matriz SEO/A11y/SEM/legal

| Prefijo | Dominio | Nº |
|---|---|---|
| ACC | Accesibilidad WCAG 2.2 AA / EN 301 549 | 16 |
| TEC | SEO técnico y seguridad base | 10 |
| ONP | SEO on-page | 8 |
| OFF | SEO off-page | 3 |
| SEM | Publicidad PPC / landing | 6 |
| ANA | Analítica y Consent Mode v2 | 3 |
| LEG | Legal RGPD/cookies/aviso | 5 |

Dictamen: POSITIVO (0 FAIL Críticos + ACC ≥90% + TEC ≥85% + global ≥85%) ·
PARCIAL (global ≥70%) · NEGATIVO (resto). N/A y PENDING fuera del denominador.

## Origen web-playwright (42) — QA E2E con evidencias

| Prefijo | Categoría | Nº |
|---|---|---|
| RT | Rutas/crawl | 4 |
| FN | Funcional | 6 |
| FM | Formularios (triple pasada) | 6 |
| UI | UI/Responsive medido | 7 |
| AC | Accesibilidad navegador | 5 |
| PF | Performance/CWV | 4 |
| SE | SEO en navegador | 3 |
| SG | Seguridad frontend | 4 |
| MO | Motion | 3 |

Veredicto: APTO (0 FAIL Críticas + global ≥90%) · APTO CON OBSERVACIONES
(70–89%) · NO APTO (resto). Cada FAIL lleva locator + screenshot + console.

## Umbrales comunes (`core/configs/thresholds.json`)

- CWV: LCP ≤2.5s · INP ≤200ms · CLS ≤0.1 · TTFB ≤800ms · FCP ≤1.8s.
- Semáforo: Verde ≥90 · Ámbar 70–89 · Rojo <70.
- Contraste WCAG: 4.5:1 texto normal · 3:1 grande/componentes.
- UI medida: touch ≥44px (duro 24px) · fuente ≥12px · line-height ≥1.4 · grid 8pt.
