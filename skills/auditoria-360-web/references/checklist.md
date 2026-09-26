# Matriz canónica de checks (51)

Fuente de verdad: `configs/checks.json` (no duplicar aquí umbrales; este archivo es la vista rápida para el informe). Resultado por check: PASS ✅ / FAIL ❌ / WARN ⚠️ / N/A ➖ / PENDING 🔎. WARN cuenta como incumplimiento parcial a efectos de dictamen.

## Accesibilidad (ACC, peso 0.30, umbral dictamen ≥90%)
ACC-01 alt text · ACC-02 contraste 4.5:1 · ACC-03 no solo color · ACC-04 teclado + skip link (Crítico) · ACC-05 orden de foco · ACC-06 foco visible/no oculto · ACC-07 zoom 200%/reflow · ACC-08 lang · ACC-09 labels y errores de formulario (Crítico) · ACC-10 subtítulos/audiodescripción · ACC-11 HTML válido · ACC-12 ARIA nombre/rol/valor · ACC-13 mensajes de estado · ACC-14 target size 24px (2.2) · ACC-15 autenticación accesible (2.2) · ACC-16 declaración EN 301 549

## SEO Técnico (TEC, peso 0.25, umbral ≥85%)
TEC-01 HTTPS+HSTS+sin mixed (Crítico) · TEC-02 canonicals (Crítico) · TEC-03 indexabilidad/noindex (Crítico) · TEC-04 hreflang · TEC-05 robots.txt + sitemap declarado (Crítico) · TEC-06 CWV campo (LCP/INP/CLS) · TEC-07 contenido en HTML inicial · TEC-08 JSON-LD válido · TEC-09 sitemap limpio, delta <5% (Crítico) · TEC-10 sin 4xx/5xx internos ni cadenas >1

## On-Page / E-E-A-T (ONP, peso 0.20, umbral ≥80%)
ONP-01 H1 único + jerarquía · ONP-02 title 50–60 · ONP-03 meta description 150–160 · ONP-04 E-E-A-T (autor, fuentes, fechas, About) · ONP-05 OG/Twitter Cards · ONP-06 thin/canibalización · ONP-07 imágenes optimizadas + dimensiones · ONP-08 viewport móvil + paridad (Crítico)

## Off-Page (OFF, peso 0.05, umbral ≥70%)
OFF-01 toxicidad <10% + anchors naturales · OFF-02 disavow solo con manual action · OFF-03 NAP consistente

## SEM (SEM, peso 0.10, umbral ≥75%)
SEM-01 estructura por intención · SEM-02 concordancias + negativas SQR · SEM-03 QS ≥7 / landing Above Average · SEM-04 RSA completo + extensiones + destinos sin 404 · SEM-05 canibalización SEO/SEM + subasta brand · SEM-06 políticas de ads, 0 strikes (Crítico)

## Analítica (ANA, peso 0.05, umbral ≥80%)
ANA-01 Consent Mode v2 (Crítico) · ANA-02 paridad de conversiones <10% · ANA-03 GTM sin PII + UTMs gobernadas

## Compliance Legal (LEG, peso 0.05, umbral ≥90%)
LEG-01 CMP conforme RGPD/ePrivacy (Crítico) · LEG-02 política de privacidad completa · LEG-03 aviso legal LSSI · LEG-04 cabeceras de seguridad ≥4/6 · LEG-05 aplicabilidad EAA resuelta

## Reglas del dictamen (configs/thresholds.json)
- **POSITIVO**: 0 FAIL Críticos, ACC ≥90%, TEC ≥85%, LEG ≥90%, global ≥85%.
- **NEGATIVO**: cualquier FAIL Crítico, o global <70%.
- **PARCIAL**: resto de casos con global ≥70%.
- N/A y PENDING se excluyen del denominador; PENDING se lista explícitamente en el informe como verificación pendiente.
