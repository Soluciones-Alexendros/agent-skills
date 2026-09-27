# Refs modo performance

## Lighthouse 12 y web-vitals

- Auditar lab (reproducible) + field (CrUX p75 real); documentar ambos valores.
- `web-vitals/attribution` para diagnosticar causa de LCP/CLS/INP (elemento, fase, long task).
- Third-parties: "Reduce the impact of third-party code"; diferir GTM/ads/chat; fachadas para embeds.

## Rendering

- SSR/SSG/ISR/streaming-Suspense/islands: elegir por dinamismo; hidración parcial/selectiva.
- JS: `defer`/`async`, code-splitting por ruta, presupuesto JS (long tasks >50ms bajo lupa).
- Imágenes: AVIF/WebP, `srcset`+`sizes`, `fetchpriority="high"` en LCP, dimensiones anti-CLS.
- Fuentes: `font-display: swap/optional`, subsetting, preload solo crítica.

## Caching y compresión

- `Cache-Control: public, max-age + immutable` en estáticos con hash; `stale-while-revalidate` en HTML dinámico.
- Brotli (nivel 11 en build) o Zstd; verificar `content-encoding` + ETag en respuesta real.
- CDN: política de borde, purge en deploy, medir TTFB por región.

## Checks del registry

PF-01..PF-04 (CWV y carga). Detalle ampliado: skill `verificar-performance`.
