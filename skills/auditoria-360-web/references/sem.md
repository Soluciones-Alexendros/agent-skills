# SEM/PPC y Analítica — auditoría, benchmarks y landings

Leer al ejecutar pilares SEM y ANA. Si no hay campañas activas ni infraestructura de pago, marcar SEM como N/A justificado y auditar solo la preparación (tracking, landings, CMP).

## Auditoría de cuenta Google Ads (SEM-01 a SEM-06)

### Estructura
- Naming consistente: `[Geografía]-[Producto]-[Tipo]`; separación brand vs. non-brand.
- 15–25 keywords por grupo; concordancias frase/exacta > broad; intents mezclados en un mismo grupo = FAIL.
- ≥50 términos negativos, alimentados por search terms report (<30 días).

### Anuncios
- RSA: mínimo 8 titulares (objetivo 15) y 4 descripciones (objetivo 8); evitar pinning salvo necesidad; ad strength Buena/Excelente.
- Extensiones: sitelinks (4–10), callouts (4–6), snippets estructurados, llamada, ubicación, precio y promoción según tipología.
- Destinos sin 404; congruencia anuncio → landing (keyword + oferta presentes en el H1/above the fold).

### Quality Score (SEM-03)
- QS ≥7 objetivo. Componentes: CTR esperado, relevancia del anuncio, experiencia en landing — cada uno "Above Average".
- Mejora de landing experience: message match, LCP <3 s móvil, CTA claro, responsive.

### Compliance (SEM-06)
- Policy Manager: 0 rechazos activos; claims de sectores restringidos (salud, finanzas, juego) verificados y aprobados; marcas de terceros según política.
- gclid auto-tagging activo; exclusiones de IP; sin double counting de conversiones.

### Presupuesto y puja
- CPA/ROAS vs. objetivo por campaña y dispositivo; estrategia de puja coherente con margen; pérdida de impresiones por presupuesto y por rango cuantificada; cobertura de subasta de brand documentada (SEM-05).

## Benchmarks por industria (orientativos)

| Industria | CTR | CPC (USD) | Conv. | QS objetivo |
|---|---|---|---|---|
| Servicios legales | 2.9% | 6.75 | 5.7% | 7+ |
| Finanzas/seguros | 3.8% | 5.42 | 4.6% | 7+ |
| Tecnología | 2.4% | 3.45 | 3.2% | 6+ |
| Retail e-commerce | 3.3% | 1.23 | 2.5% | 6+ |
| B2B | 2.1% | 5.89 | 3.4% | 7+ |

Usar solo como referencia de orden de magnitud; contrastar con datos propios de la cuenta.

## Landing pages para pago

Above the fold: headline que coincide con la keyword del anuncio, propuesta de valor (beneficio, no feature), CTA ≥48px con copy de acción ("Solicitar consulta gratis", no "Enviar"), social proof inmediato y trust badges.
Mid-fold: 3–5 beneficios en bullets, comparativa honesta, pricing transparente, FAQ de objeciones, CTAs secundarios cada 2–3 secciones.
Técnico: LCP <3 s móvil, formulario de 3–5 campos con validación inline y `autocomplete`, checkbox de privacidad con enlace, GA4 + tag de conversión + heatmap.
Post-conversión: thank-you page con siguientes pasos y email de confirmación <5 min.

## Analítica y medición (ANA-01 a ANA-03)

- **ANA-01 Consent Mode v2**: señales `ad_storage`, `analytics_storage`, `ad_user_data`, `ad_personalization` según estado del banner; verificar en GTM Preview que no se disparan tags de marketing pre-consentimiento (obligatorio EEE).
- **ANA-02 Conversiones**: paridad GA4 ↔ Google Ads (desviación <10%), deduplicación, enhanced conversions si hay datos, importación offline si aplica.
- **ANA-03 Gobernanza**: dataLayer estructurado, 0 PII en URLs/dataLayer, UTMs en lowercase con sheet de gobernanza, sin UTMs en enlaces internos, timezone de Ads = timezone de GA4.
