---
name: verificar-performance
description: >-
  Auditoría de rendimiento web: Core Web Vitals (LCP, INP, CLS), Lighthouse 12,
  TTFB/FCP, rendering (SSR/SSG/ISR/islands), caching HTTP/CDN, optimización de
  carga y diagnóstico técnico frontend. Usar cuando el operador pida auditoría
  de performance, Lighthouse/CWV, optimización de carga, estabilidad visual,
  caching o rendering. No usar para compliance legal o accesibilidad (→
  verificar-compliance) ni para una auditoría holística sin foco (→
  verificar-fullaudit).
license: MIT
metadata:
  author: Soluciones-Alexendros
  version: "3.1.1"
  dominio: verificar
  tipo: atomic
  idioma: es
---

# verificar-performance — Auditoría de rendimiento y calidad técnica web

## Propósito

Auditar métricas de rendimiento, calidad de renderizado, estabilidad visual, caching y stack tecnológico. Entregar métricas medibles, diagnóstico técnico y plan de optimización priorizado.

## Cuándo usar

Auditoría de performance web, Lighthouse/CWV, optimización de carga, estabilidad, rendering, caching y diagnóstico técnico de frontend.

## Procedimiento

1. **Pre-flight** — Detectar stack (headers, `__NEXT_DATA__`, generadores), medir TTFB con curl.
2. **Core Web Vitals** — LCP ≤2.5s, INP ≤200ms, CLS ≤0.1 vía Lighthouse 12 o web-vitals.js v4/5; distinguir lab vs field (CrUX).
3. **Métricas de carga** — FCP, TTFB, tamaño por recurso (HTML/CSS/JS/imágenes), nº de requests, compresión (Brotli/Gzip/Zstd), headers de caché (Cache-Control, ETag, CDN).
4. **Rendering** — Estrategia SSR/SSG/ISR/streaming/islands; hidración parcial; code-splitting y lazy-load; imágenes responsive (AVIF/WebP, `fetchpriority`, `loading=lazy`).
5. **SEO técnico** — Meta tags, canonical, robots.txt, sitemap.xml, Open Graph, estructura H1-H6, Schema.org, HTTPS, mobile-friendly.
6. **Informe y plan** — Resumen ejecutivo, semáforo por área (Verde ≥90 / Ámbar 70–89 / Rojo <70), top 3 acciones, tabla priorizada (prioridad, área, acción, esfuerzo).

## Formato de salida

1. Informe con métricas CWV, carga, rendering, caching, SEO técnico.
2. Plan de acción priorizado: Alta (LCP/CLS, rastreo), Media (meta tags, imágenes), Baja (Brotli, caché agresiva).

## Referencias

- `references/performance.md` — métricas y procedimiento.
- `references/seo-tecnico.md` — checklist y plantilla de estado.
- Compliance legal/a11y → `verificar-compliance`. Auditoría holística → `verificar-fullaudit`.
