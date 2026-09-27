# Performance web — Core Web Vitals, carga y caché

Fuente migrada de `web-audit` (Pre-flight + plan de acción). Ámbito de `web-rendimiento`:
rapidez de carga, estabilidad visual, compatibilidad, renderizado y tecnologías.

## Herramientas

Lighthouse (si disponible), curl timing, análisis de recursos.

## Métricas a medir

- **TTFB** (Time to First Byte)
- **FCP** (First Contentful Paint)
- **LCP** (Largest Contentful Paint) — umbral: ≤ 2.5 s
- **CLS** (Cumulative Layout Shift) — umbral: ≤ 0.1
- **INP** (Interaction to Next Paint) — umbral: ≤ 200 ms
- **Tamaño de página** (HTML, CSS, JS, imágenes)
- **Número de requests**
- **Compresión** (Gzip, Brotli)
- **Caché** (headers Cache-Control, ETag)

## Procedimiento

1. Detectar stack (headers, `__NEXT_DATA__`, generadores) y medir TTFB con curl.
2. Medir CWV con Lighthouse o web-vitals.js; anotar LCP, INP, CLS con evidencia.
3. Medir tamaño de página por tipo de recurso y número de requests.
4. Verificar compresión (Brotli/Gzip) y headers de caché (Cache-Control, ETag).
5. Registrar todo en el informe con semáforo por métrica.

## Acciones típicas (del plan priorizado)

| Prioridad | Acción | Esfuerzo |
|---|---|---|
| Alta | Corregir LCP/CLS (imágenes, lazy loading, layouts estables) | Medio |
| Baja | Compresión Brotli y caché agresiva de estáticos | Bajo |

## Límites

El compliance legal y la accesibilidad profunda no viven aquí: usar `web-compliance`.
El QA funcional E2E con evidencias de navegador no vive aquí: usar `web-playwright`.
