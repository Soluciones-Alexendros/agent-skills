# Remediación Fullaudit — roadmap RICE fusionado

## Matriz RICE

Score = reach × impact × confidence / effort (`core/scoring/rice.py`).
Defaults por severidad: Crítico 9/9/8/3 · Alto 7/7/8/4 · Medio 5/5/7/5 · Bajo 3/3/7/3.

## Roadmap 4 sprints

| Sprint | Severidad | Plazo | Objetivo |
|---|---|---|---|
| Sprint 0 | Crítico | 48h | Estabilizar: la web no rompe ni pierde conversiones |
| Sprint 1 | Alto | Semana 1 | Usable y accesible: 100% funcional + WCAG AA |
| Sprint 2 | Medio | Semana 2 | Profesionalizar: CWV verde y UI unificada |
| Sprint 3 | Bajo | Semana 3 | SEO y delight: pulido final |

Cada tarea: problema → causa raíz → solución con código → criterio de aceptación
como test (Playwright en e2e, re-auditoría parcial en compliance).

## Templates de código

### Skip-link accesible

```html
<a class="skip-link" href="#contenido">Saltar al contenido</a>
<main id="contenido" tabindex="-1">…</main>
```

```css
.skip-link { position: absolute; left: -9999px; }
.skip-link:focus { left: 1rem; top: 1rem; z-index: 100; }
```

### Formulario accesible mínimo

```html
<form novalidate>
  <label for="email">Correo electrónico</label>
  <input id="email" name="email" type="email" required aria-describedby="err-email">
  <p id="err-email" role="alert" hidden>Indica un correo válido.</p>
</form>
```

### JSON-LD organización

```html
<script type="application/ld+json">
{"@context": "https://schema.org", "@type": "Organization",
 "name": "…", "url": "https://ejemplo.test/"}
</script>
```

## Formato de informe de cierre

Resumen ejecutivo (dictamen dual) → semáforo por dominio → top hallazgos RICE →
plan por sprints → verificación de cierre → próximos pasos. Generado por
`core/reporting/report.py`.
