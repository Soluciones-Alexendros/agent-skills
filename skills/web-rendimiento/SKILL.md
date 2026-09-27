---
name: web-rendimiento
version: "1.0.0"
description: >
  Auditoría de rendimiento y calidad técnica web: Core Web Vitals (LCP, INP, CLS), TTFB, FCP,
  tamaño de página, requests, compresión, caché, rendering, estabilidad, compatibilidad,
  tecnologías y stack. Usar para auditoría de performance, Lighthouse/CWV, optimización
  de carga, estabilidad visual, diagnóstico técnico de frontend.
license: MIT
metadata:
  author: Soluciones-Alexendros
  dominio: web
  idioma: es
---

# Web Rendimiento — Auditoría de performance y calidad técnica web

Auditoría enfocada en métricas de rendimiento, calidad de renderizado, estabilidad visual,
compatibilidad y stack tecnológico. Entrega métricas medibles, diagnóstico técnico y plan
de optimización priorizado.

## Flujo de auditoría

1. **Pre-flight** — Detectar stack (headers, `__NEXT_DATA__`, generadores), medir TTFB con curl.
2. **Core Web Vitals** — LCP, INP, CLS via Lighthouse o web-vitals.js; umbrales: LCP ≤2.5s, INP ≤200ms, CLS ≤0.1.
3. **Métricas de carga** — FCP, tamaño de página (HTML/CSS/JS/imágenes), número de requests, compresión (Brotli/Gzip), headers de caché (Cache-Control, ETag).
4. **SEO técnico** — Meta tags, canonical, robots.txt, sitemap.xml, Open Graph, Twitter Cards, estructura H1-H6, Schema.org, HTTPS, mobile-friendly.
5. **Accesibilidad técnica** — Contraste (ratio 4.5:1), alt en imágenes, labels en formularios, navegación por teclado, ARIA, focus visible.
6. **Informe y plan** — Resumen ejecutivo, semáforo por área, top 3 acciones, tabla priorizada (prioridad, área, acción, esfuerzo).

## Herramientas externas

| Herramienta | Propósito |
|---|---|
| Lighthouse / web-vitals.js | CWV (LCP, INP, CLS), TTFB, FCP |
| curl / timing | TTFB, headers, compresión |
| Lectura HTML / robots.txt / sitemap.xml | SEO técnico |
| axe-core | Accesibilidad WCAG 2.1 AA |

## Entregables

1. Informe con métricas CWV, carga, SEO técnico, accesibilidad.
2. Plan de acción priorizado: Alta (LCP/CLS, WCAG alta, rastreo), Media (meta tags, formularios), Baja (Brotli, caché agresiva).

## Uso

Usar para auditoría de performance web, Lighthouse/CWV, optimización de carga, estabilidad, compatibilidad, diagnóstico técnico de frontend. No usar para compliance legal/accesibilidad profundo (→ `web-compliance`) ni QA funcional E2E (→ `web-playwright`).

## Estructura

- `SKILL.md` — flujo de auditoría, métricas CWV y entregables.
- `references/performance.md` — CWV, carga, compresión y caché (migrada de `web-audit`).
- `references/seo-tecnico.md` — checklist SEO técnico de rastreo (migrado de `web-audit`).

## Referencias

- `references/performance.md` — métricas y procedimiento.
- `references/seo-tecnico.md` — checklist y plantilla de estado.
- Origen: split 2026-09 de `auditoria-360-web` + absorción parcial de `web-audit`; compliance en `web-compliance`, E2E en `web-playwright`.