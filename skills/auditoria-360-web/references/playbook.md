# Playbook operativo — 8 fases (SEO técnico, on-page, off-page, legal)

Leer cuando se ejecuten las FASES 0–4 y LEG. Criterios WCAG en `wcag22.md`; SEM/ANA en `sem.md`.

## Índice
1. FASE 0 — Kick-off y alcance
2. FASE 1 — Inventario y crawling
3. FASE 3 — SEO técnico (checks TEC)
4. FASE 4 — On-page y E-E-A-T (checks ONP)
5. FASE 5 — Off-page (checks OFF)
6. Pilar LEG — Compliance legal y privacidad
7. Evidencia auditable

## FASE 0 — Kick-off y alcance

- Perímetro: dominio apex, subdominios, idiomas, entornos (prod/staging), secciones excluidas.
- RACI: SEO Lead (R), Auditor A11y (R), Dev (A), Legal (C), Marketing/Paid (I).
- Accesos: GSC, GA4, GTM, Google Ads, CMS, CDN, logs de servidor.
- KPIs baseline: tráfico orgánico, impresiones, CTR, violaciones Axe, CWV p75. Exportar antes de tocar nada.
- Congelar deploys durante el crawl crítico.
- Normativa aplicable: WCAG 2.2 AA siempre; EN 301 549 (EAA 2025) si B2C en UE; RD 1112/2018 + UNE 139803 si sector público ES; ADA/508 si EE. UU.; RGPD/ePrivacy/LOPD-GDD y LSSI-CE en España.

## FASE 1 — Inventario y crawling

1. Crawl sin render JS vs. con render JS; comparar contenido crítico.
2. Cruzar sitemap.xml vs. crawl vs. logs (30 días de Googlebot): páginas huérfanas, waste de crawl budget, 4xx/5xx por bot.
3. Validar robots.txt (RFC 9309): sintaxis, Allow/Disallow, sitemap declarado, lastmod veraz.
4. Inventariar plantillas: home, categoría, ficha/PDP, blog, landing PPC, checkout, formularios.
5. Detectar stack: CMS, framework JS (CSR/SSR/SSG), CDN, analítica presente.
- Criterio de salida: crawl del 100% de URLs indexables; delta sitemap vs. crawl <5%.

## FASE 3 — SEO técnico (checks TEC-01 a TEC-10)

Ejecutar `scripts/audit_page.py` por plantilla y complementar:

- **TEC-01 HTTPS/HSTS**: cert válido, 301 HTTP→HTTPS, HSTS (ideal preload), 0 mixed content (script).
- **TEC-02 Canonicals**: autorreferenciados, únicos; sin canonical a 404/noindex ni canonicals cruzadas injustificadas; paginación sin rel=next/prev (obsoleto) pero con enlazado interno correcto.
- **TEC-03 Indexabilidad**: meta robots/X-Robots-Tag; site: vs. sitemap; indexación excesiva (facetas/parámetros) o insuficiente.
- **TEC-04 Hreflang**: bidireccional, x-default, ISO 639-1/3166-1, sin conflicto con canonical.
- **TEC-06 CWV campo** (CrUX/PSI/GSC, p75 móvil): LCP ≤2.5s, INP ≤200ms, CLS ≤0.1, TTFB ≤0.8s auxiliar. Fixes típicos: preload imagen LCP, priority hints, reducir long tasks JS (INP), width/height en imágenes y ads (CLS).
- **TEC-07 Render**: contenido principal en HTML inicial (el script estima densidad de texto); auditoría CSR si aplica.
- **TEC-08 JSON-LD**: Organization + BreadcrumbList obligatorios; Article/Product/FAQPage/LocalBusiness según tipología; validar en Rich Results Test; sin @id duplicados; sin markup spam (manual action).
- **TEC-09 Sitemap**: 200 OK, solo URLs indexables (sin 4xx/noindex), declarado en robots.txt y GSC.
- **TEC-10 Errores y redirecciones**: 0 errores 4xx/5xx enlazados internamente; cadenas ≤1 salto; 404 personalizado útil.

## FASE 4 — On-page y E-E-A-T (checks ONP)

- **ONP-01**: un H1 por URL con keyword principal; sin saltos H1→H3; outline lógico.
- **ONP-02 Title**: único, 50–60 caracteres (30–65 aceptable), keyword al inicio, intent match.
- **ONP-03 Meta description**: única, 150–160 caracteres, CTA.
- **ONP-04 E-E-A-T**: autor con bio y credenciales, fecha de actualización visible, fuentes citadas, páginas About/Contact robustas, schema Person/Author, perfiles verificables (sameAs).
- **ONP-06 Thin/canibalización**: detectar <200 palabras indexables; mapa de canibalización por cluster con queries overlapping de GSC; consolidar con 301 o diferenciar intención.
- **ONP-07 Imágenes**: WebP/AVIF, width/height, lazy-load bajo el fold (nunca en la imagen LCP), alt dual SEO+A11y.
- **ONP-08 Móvil**: viewport correcto, paridad de contenido móvil/escritorio, touch targets.
- Keyword research (si se pide): head terms → long-tail → clasificación por intención (informacional/navegacional/comercial/transaccional) → gap vs. competidores → priorización por volumen/dificultad.

## FASE 5 — Off-page (checks OFF)

- **OFF-01**: toxicidad <10% dominios, anchor exact match <15%, sin PBN evidente, ratio dofollow/nofollow ~70/30, pérdida masiva de enlaces investigada.
- **OFF-02**: disavow solo con manual action confirmada; archivo documentado en GSC.
- **OFF-03**: NAP 100% consistente (GBP, Bing Places, directorios).
- Complementos: link intersect vs. 3 competidores, recuperación de lost links (90 días), broken link reclamation, menciones sin enlace.

## Pilar LEG — Compliance legal

- **LEG-01 CMP**: rechazo tan fácil como aceptar (sin dark patterns), granular por finalidad, bloqueo previo de cookies no esenciales (verificar en red antes de consentir), registro/prueba de consentimiento, renovación periódica.
- **LEG-02 Privacidad**: RGPD arts. 13–14 — responsable, finalidades, bases jurídicas, plazos, destinatarios, transferencias internacionales, derechos ARCO, DPO/contacto.
- **LEG-03 Aviso legal** (LSSI-CE art. 10): titular, NIF, datos registrales, contacto.
- **LEG-04 Cabeceras** (script): HSTS, CSP, X-Content-Type-Options, Referrer-Policy, Permissions-Policy (≥4/6).
- **LEG-05 EAA**: resolver aplicabilidad (B2C UE desde jun-2025) y declaración de conformidad.
- Newsletter: doble opt-in y baja funcional. GTM/URLs sin PII (cruce con ANA-03).

## Evidencia auditable

Todo hallazgo adjunta: captura con fecha, URL canónica, herramienta y versión, navegador/AT, snippet HTML. WCAG: vídeo NVDA ~30 s por plantilla crítica. CWV: enlace a informe PSI/CrUX. Analítica: captura DebugView/GTM Preview.
