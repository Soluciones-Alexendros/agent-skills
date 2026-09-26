---
name: web-audit
description: >-
  Auditoría web de sitios o frontends: stack, rendimiento (Lighthouse/CWV), SEO,
  accesibilidad WCAG y plan de saneamiento basado en evidencia. Usar ante 'audita esta web',
  SEO, a11y o Lighthouse. No usar para auditoría de código/repo (→ repo-starting) ni
  dirección visual creativa (→ web-diseno).
license: MIT
metadata:
  author: Soluciones-Alexendros
  version: "0.1.0"
  dominio: web
  idioma: es

---

# web-audit — Auditoría web completa

## Pre-flight

Herramientas: Lighthouse (si disponible), curl timing, análisis de recursos

Métricas a medir:

- **TTFB** (Time to First Byte)
- **FCP** (First Contentful Paint)
- **LCP** (Largest Contentful Paint)
- **CLS** (Cumulative Layout Shift)
- **INP** (Interaction to Next Paint)
- **Tamaño de página** (HTML, CSS, JS, imágenes)
- **Número de requests**
- **Compresión** (Gzip, Brotli)
- **Caché** (headers Cache-Control, ETag)

### Etapa 3 — SEO

Herramientas: lectura HTML, robots.txt, sitemap.xml, meta tags

Checklist:

- **Meta tags**: title, description, canonical, robots
- **Open Graph**: og:title, og:description, og:image, og:url
- **Twitter Cards**: twitter:card, twitter:title, twitter:description
- **Estructura de encabezados**: H1-H6 jerarquía
- **Imágenes**: alt attributes, lazy loading
- **Enlaces**: internal/external, nofollow
- **Sitemap**: exists, valid, submitted
- **Robots.txt**: exists, correcto
- **Schema.org**: structured data
- **Mobile-friendly**: responsive design
- **HTTPS**: certificate, mixed content

### Etapa 4 — Accesibilidad

Herramientas: axe-core (si disponible), análisis manual de HTML

Checklist WCAG 2.1 AA:

- **Contraste de colores**: ratio mínimo 4.5:1
- **Alternativas de texto**: alt en imágenes, labels en formularios
- **Navegación por teclado**: tabindex, focus visible
- **Lectores de pantalla**: ARIA roles, landmarks
- **Formularios**: error messages, required fields
- **Multimedia**: captions, transcripts
- **Timing**: time limits adjustable
- **Seizures**: no flashing content

### Etapa 5 — Informe y recomendaciones

Estructura del informe:

---------------|
...
### Optimizaciones
- [ ] Acción 1 (prioridad alta)
- [ ] Acción 2 (prioridad media)

## 3. SEO
### Estado actual
...
### Recomendaciones
- [ ] Acción 1
- [ ] Acción 2

## 4. ACCESIBILIDAD
### Violaciones WCAG
| Regla | Elemento | Severidad | Fix |
|-------|----------|-----------|-----|
...
### Mejoras sugeridas
- [ ] Mejora 1

## 5. RESUMEN Y PLAN DE ACCIÓN
| Prioridad | Área | Acción | Esfuerzo |
|-----------|------|--------|----------|
...

## Fuentes fusionadas

- SEO: `references/seo-source.md`
- Accesibilidad: `references/a11y-source.md`
- La crítica de *código* de producto no vive aquí: usar `repo-starting`.

## Uso

Usar ante "audita esta web", revisión SEO, accesibilidad WCAG o métricas Lighthouse/CWV. No usar para auditoría de código/repo (→ `repo-starting`) ni dirección visual creativa (→ `web-diseno`).

## Estructura

- `SKILL.md` — flujo Pre-flight y Etapas 3–5 + plantilla de informe.
- `references/seo-source.md` — detalle SEO avanzado.
- `references/a11y-source.md` — detalle accesibilidad y UX.

## Herramientas

Sin scripts en esta skill. Herramientas externas citadas:

| Herramienta | Propósito |
|---|---|
| Lighthouse / CWV | Rendimiento (TTFB, FCP, LCP, CLS, INP) |
| Lectura HTML / robots.txt / sitemap.xml | SEO técnico |
| axe-core | Accesibilidad WCAG 2.1 AA |

## Referencias

- `references/seo-source.md` — SEO.
- `references/a11y-source.md` — Accesibilidad.
- Skills relacionadas: `repo-starting`, `web-diseno`.
