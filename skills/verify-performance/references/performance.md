# Performance web — Core Web Vitals, rendering y caché

Ámbito de `verify-performance`: rapidez de carga, estabilidad visual, estrategia de
renderizado, caching HTTP/CDN y tecnologías. Todo en español.

## Herramientas

Lighthouse 12 (si disponible), web-vitals.js v4/5 (atributo `web-vitals/attribution`
para diagnosticar LCP/CLS/INP), curl timing, DevTools Performance/Network,
análisis de recursos y waterfall.

## Métricas a medir

- **TTFB** (Time to First Byte) — bueno ≤800 ms; medir con curl y con CrUX/lab
- **FCP** (First Contentful Paint) — bueno ≤1.8 s (lab)
- **LCP** (Largest Contentful Paint) — umbral: ≤ 2.5 s (bueno), >4 s pobre
- **CLS** (Cumulative Layout Shift) — umbral: ≤ 0.1 (bueno), >0.25 pobre
- **INP** (Interaction to Next Paint) — umbral: ≤ 200 ms (bueno), >500 ms pobre
- **Tamaño de página** (HTML, CSS, JS, imágenes, fuentes, third-parties)
- **Número de requests** y peso por dominio (first vs third-party)
- **Compresión** (Brotli, Gzip, Zstd)
- **Caché** (headers Cache-Control, ETag, `stale-while-revalidate`, política CDN)

Distinguir siempre **lab** (Lighthouse, reproducible) de **field** (CrUX/RUM, p75
real de usuarios). Ante discrepancia, manda field.

## Rendering

- Estrategia: SSR, SSG, ISR, streaming/Suspense, islands/archipiélagos, SPA clásica.
- Hidratación: coste JS, hidración parcial/selectiva, `defer`/`async`, code-splitting por ruta.
- Imágenes: formatos modernos (AVIF/WebP), `srcset`+`sizes`, `fetchpriority="high"`
  en LCP, `loading="lazy"`+`decoding="async"` bajo el pliegue, dimensiones explícitas anti-CLS.
- Fuentes: `font-display: swap/optional`, subsetting, preload solo de la crítica.
- Third-parties: auditar con Lighthouse "Reduce the impact of third-party code";
  diferir GTM/ads/chat, fachadas (facade) para embeds.

## Procedimiento

1. Detectar stack (headers, `__NEXT_DATA__`, generadores) y medir TTFB con curl.
2. Medir CWV con Lighthouse 12 o web-vitals.js; anotar LCP, INP, CLS con evidencia y origen lab/field.
3. Medir tamaño de página por tipo de recurso y número de requests; waterfall de bloqueantes.
4. Verificar compresión (Brotli/Gzip/Zstd) y headers de caché (Cache-Control, ETag, CDN).
5. Revisar estrategia de rendering e hidración; listar JS bloqueante y third-parties.
6. Registrar todo en el informe con semáforo por métrica (Verde ≥90 / Ámbar 70–89 / Rojo <70).

## Acciones típicas (del plan priorizado)

| Prioridad | Acción | Esfuerzo |
|---|---|---|
| Alta | Corregir LCP/CLS (imagen LCP con fetchpriority, layouts estables, fuentes) | Medio |
| Alta | Recortar JS bloqueante e hidración (code-splitting, diferir third-parties) | Medio |
| Media | Imágenes responsive AVIF/WebP + lazy-load | Bajo |
| Baja | Compresión Brotli/Zstd y caché agresiva de estáticos + CDN | Bajo |

## Límites

El compliance legal y la accesibilidad profunda no viven aquí: usar `verify-compliance`.
La auditoría E2E completa con evidencias de navegador vive en `verify-fullaudit` (modos e2e/full).
