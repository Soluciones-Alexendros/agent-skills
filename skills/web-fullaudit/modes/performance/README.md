# Modo performance — CWV, rendering y caching

Puente hacia la skill `web-performance` (Lighthouse 12, CWV lab+field, rendering,
caching). Este modo no tiene scripts propios: guía + puntúa CWV contra
`core/configs/thresholds.json`.

## Flujo

1. **Pre-flight**: stack + TTFB (curl). Fijar origen lab (Lighthouse) y field (CrUX/RUM).
2. **CWV**: LCP ≤2.5s · INP ≤200ms · CLS ≤0.1 · TTFB ≤800ms · FCP ≤1.8s.
   Anotar evidencia + origen; ante discrepancia manda field.
3. **Carga**: peso por recurso, nº requests, first vs third-party, waterfall de bloqueantes.
4. **Rendering**: SSR/SSG/ISR/streaming/islands; hidración parcial; code-splitting;
   imágenes AVIF/WebP + `fetchpriority`/`loading=lazy`; fuentes `font-display`.
5. **Caching**: Brotli/Gzip/Zstd, Cache-Control/ETag, política CDN.
6. **Scoring**: `run.py --checks cwv.json --outdir output/` (checks PF-01..PF-04 del registry).

## Entrada/salida

- Entrada: checks formato e2e (`{"id": "PF-01", "status": "PASS|FAIL|WARN", …}`) o compliance.
- Salida en `--outdir`: `score.json`, `REPORT.md`, `REPORT.html`, `issues.csv`.

## Refs específicas

Ver `refs.md` (Lighthouse, rendering, caching, detalle en skill `web-performance`).
