# Glosario y stack de herramientas

## Glosario

- **Core Web Vitals**: métricas de experiencia (LCP carga, INP interactividad, CLS estabilidad visual). Umbrales buenos: LCP ≤2.5 s, INP ≤200 ms, CLS ≤0.1 (p75).
- **E-E-A-T**: Experience, Expertise, Authoritativeness, Trustworthiness — marco de calidad de contenido de Google, crítico en sitios YMYL.
- **Canonical**: `<link rel="canonical">` que define la URL preferida ante duplicados.
- **Hreflang**: atributo de idioma/región para sitios internacionales; requiere reciprocidad y `x-default`.
- **Quality Score**: métrica Google Ads (1–10) de CTR esperado, relevancia y experiencia de landing; afecta CPC y posición.
- **WCAG 2.2**: pautas de accesibilidad; niveles A/AA/AAA. Novedades 2.2: Focus Not Obscured, Dragging Movements, Target Size (24px), Consistent Help, Accessible Authentication.
- **EN 301 549**: estándar europeo de accesibilidad TIC; referencia de la EAA (Directiva 2019/882, obligatoria B2C desde jun-2025) y del RD 1112/2018 (sector público ES).
- **Consent Mode v2**: marco de Google para ajustar el comportamiento de tags según el consentimiento (ad_storage, analytics_storage, ad_user_data, ad_personalization).
- **Crawl budget**: páginas que Googlebot rastrea por período; se desperdicia con facetas, parámetros y soft 404.
- **Orphan page**: página sin enlaces internos entrantes.
- **Canibalización**: varias URLs compitiendo por la misma intención de búsqueda.
- **RICE**: priorización Reach × Impact × Confidence / Effort.
- **Skip link**: enlace "saltar al contenido" visible al recibir foco (WCAG 2.4.1).
- **Thin content**: página con contenido escaso o sin valor añadido.
- **NAP**: Name, Address, Phone — consistencia de datos de negocio local.
- **SERP / CTR / CVR / CPA / ROAS**: página de resultados; tasas de clic y conversión; coste por adquisición; retorno de inversión publicitaria.

## Stack de herramientas

| Categoría | Herramientas |
|---|---|
| Crawl | Screaming Frog (render JS), Sitebulb, logs de servidor |
| Accesibilidad | Axe DevTools, WAVE, Lighthouse A11y, NVDA/VoiceOver, Colour Contrast Analyser |
| CWV | PageSpeed Insights, CrUX, GSC (informe CWV), WebPageTest |
| SEO | Google Search Console, Ahrefs/Semrush/Majestic, Siteliner |
| SEM | Google Ads Editor, Policy Manager, Auction Insights |
| Analítica | GA4 DebugView, GTM Preview, validador de CMP |
| Validación | W3C Validator, Rich Results Test, hreflang validators |

## Herramientas internas de la skill (sin dependencias externas)

- `scripts/audit_page.py` — checks automatizables de una URL o fichero HTML.
- `scripts/contrast.py` — contraste WCAG entre dos colores.
- `scripts/score.py` — % por pilar, semáforo y dictamen.
- `scripts/report.py` — informe de cierre en Markdown.
- `scripts/selftest.py` — suite de tests (ejecutar tras cualquier cambio).
