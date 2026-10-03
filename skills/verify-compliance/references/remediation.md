# Plan de remediación, RICE y templates de código

Leer en la FASE 8 (informe + plan de soluciones y mejoras).

## Roadmap 90 días

| Sprint | Plazo | Contenido | Criterio de éxito |
|---|---|---|---|
| Sprint 1 | <72 h – 2 sem | FAILs Críticos: skip-link, teclado, robots/canonicals, HTTPS/mixed content, Consent Mode v2 + CMP | 0 FAIL críticos; re-auditoría parcial (Axe + GSC) |
| Sprint 2 | 2–6 semanas | Severidad Alta: JSON-LD, CWV, formularios accesibles, E-E-A-T (bios, schema, fechas), QS ≥7, SQR negativas | ACC ≥90% PASS, TEC ≥85%, tracking 100% operativo |
| Sprint 3 | 7–12 semanas | Medios/Bajos: contenido y clusters, enlazado interno, declaración de accesibilidad + VPAT, mejoras proactivas | Dictamen POSITIVO en re-auditoría completa |

## Priorización RICE

Score = (Reach × Impact × Confidence) / Effort. Ejemplo real: skip-link R9·I9·C9/E1 = 810 (Sprint 1, ~15 min); JSON-LD Person R9·I10·C9/E2 = 405; Consent Mode v2 R8·I9·C8/E4 = 144. Documentar R/I/C/E de cada acción en el roadmap.

## Matriz esfuerzo-impacto

- **Quick wins (hacer ya)**: titles duplicados (~2 h), alt text (~4 h), enlazado interno básico (~3 h), meta descriptions (~6 h).
- **Proyectos mayores (roadmap)**: CWV (40+ h), remediación A11y completa (80+ h), pillar content (100+ h), rebuild de landings (30+ h).
- **No hacer**: keyword stuffing (>3%), anchors exact match 100%, compra de backlinks, contenido auto-generado sin valor.

## Mejoras proactivas (más allá del cumplimiento)

- Contenido: topic clusters (pillar + satélites), fechas de actualización visibles, FAQ orientadas a featured snippets.
- CRO: mapas de calor, A/B de CTAs y formularios, reducción de campos, social proof accesible.
- Accesibilidad avanzada: declaración pública, canal de feedback, auditoría trimestral con usuarios reales, tokens de diseño con contraste verificado.
- Datos: dashboard SEO+SEM+CWV+A11y con alertas; validación de datos estructurados y presupuestos de rendimiento en CI (Lighthouse CI); monitoring RUM.
- Gobernanza: checklist SEO+A11y obligatorio en cada publicación; revisión trimestral de keywords y competencia.

## Templates de código

### Skip link (ACC-04)
```html
<a href="#main" class="skip-link">Saltar al contenido principal</a>
<nav aria-label="Menú principal">…</nav>
<main id="main">…</main>
<style>
.skip-link{position:absolute;top:-40px;left:0;background:#111;color:#fff;
  padding:8px 16px;z-index:1000;transition:top .2s}
.skip-link:focus{top:0;outline:3px solid #6d4aff}
</style>
```

### Formulario accesible (ACC-09)
```html
<label for="email">Correo electrónico *</label>
<input type="email" id="email" name="email" required aria-required="true"
       aria-describedby="email-error" autocomplete="email">
<span id="email-error" role="alert"></span>
<!-- Al validar: input.setAttribute('aria-invalid','true') y escribir el
     mensaje de error con instrucción de corrección en #email-error -->
```

### JSON-LD mínimo (TEC-08 / ONP-04)
```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "Nombre", "url": "https://ejemplo.com",
  "logo": {"@type": "ImageObject", "url": "https://ejemplo.com/logo.png"},
  "sameAs": ["https://www.linkedin.com/company/ejemplo"]
}
```
Añadir `BreadcrumbList` en todas las páginas salvo home; `Person` (con `sameAs` verificables) en páginas de autor.

## Formato del informe de cierre

1. **Encabezado**: objetivo, alcance, fechas, herramientas y versiones, normativa de referencia.
2. **Resumen ejecutivo** (≤1 página): semáforo global, % por pilar, 5 hallazgos críticos, prioridad #1.
3. **Matriz de compliance**: los 51 checks con resultado ✅/❌/⚠️/➖/🔎, evidencia y severidad (generable con `scripts/report.py`).
4. **Hallazgos detallados**: ID, severidad, criterio, estándar, evidencia, impacto, acción, esfuerzo.
5. **Roadmap RICE 90 días** con owners RACI y KPI de validación por acción.
6. **Check de verificación de cierre**: tabla ✅/❌ de condiciones de dictamen + fecha de re-auditoría.
7. **Anexos**: URLs auditadas, mediciones CWV, transcripciones de lector de pantalla, capturas.
