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
  version: "0.2.0"
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

| Sección | Contenido | Origen |
|---------|-----------|--------|
| 1. Resumen ejecutivo | Hallazgo principal, semáforo (verde/ámbar/rojo), top 3 acciones | Fusión de secciones 3–4 |
| 2. Rendimiento | CWV (LCP, INP, CLS), tamaño de página, requests, caché | Etapa 2 (Pre-flight) |
| 3. SEO | Tabla de checks con estado y evidencia | Etapa 3 |
| 4. Accesibilidad | Violaciones WCAG y mejoras sugeridas | Etapa 4 |
| 5. Plan de acción | Tabla priorizada: prioridad, área, acción, esfuerzo | Fusión de 2–4 |

### Optimizaciones
- [ ] Acción 1 (prioridad alta)

## 3. SEO
### Estado actual

| Check | Estado | Evidencia |
|-------|--------|-----------|
| Title único y < 60 caracteres | ✓ / ✗ / ~ | Lectura HTML |
| Meta description presente (150–160 caracteres) | ✓ / ✗ / ~ | Lectura HTML |
| Canonical apunta a la URL final | ✓ / ✗ / ~ | Lectura HTML |
| robots.txt existe y no bloquea contenido | ✓ / ✗ / ~ | `curl /robots.txt` |
| sitemap.xml válido y enviado a buscadores | ✓ / ✗ / ~ | `curl /sitemap.xml` |
| Open Graph completo (title, description, image, url) | ✓ / ✗ / ~ | Lectura HTML |
| Jerarquía H1–H6 sin saltos | ✓ / ✗ / ~ | Lectura HTML |
| Imágenes con alt descriptivo | ✓ / ✗ / ~ | Lectura HTML |
| HTTPS sin contenido mixto | ✓ / ✗ / ~ | Lighthouse |
| Schema.org (JSON-LD) | ✓ / ✗ / ~ | Lectura HTML |

Leyenda: ✓ conforme · ✗ incumple · ~ parcial (detallar en evidencia).

### Recomendaciones
- [ ] Corregir los checks ✗ empezando por los que afectan al rastreo (robots, sitemap, canonical)
- [ ] Completar los checks ~ con evidencia adjunta en el informe
- [ ] Re-auditar tras las correcciones y regenerar la tabla de estado

## 4. ACCESIBILIDAD
### Violaciones WCAG

| Regla WCAG | Elemento | Severidad | Fix |
|------------|----------|----------|-----|
| 1.4.3 Contraste (mínimo) | Texto con ratio < 4.5:1 | Alta | Ajustar color de texto/fondo y re-medir |
| 1.1.1 Contorno no textual | Imagen sin alt | Alta | Añadir `alt` descriptivo o `alt=""` si decorativa |
| 4.1.2 Nombre, rol, valor | Botón sin nombre accesible | Alta | Añadir `aria-label` o texto visible |
| 2.1.1 Teclado | Control no alcanzable por teclado | Alta | Sustituir por elemento enfocable o `tabindex` |
| 3.3.1 Identificación de errores | Formulario sin mensaje de error asociado | Media | `aria-describedby` + texto de error visible |
| 2.4.7 Foco visible | `outline:none` sin alternativa | Media | Restaurar estilo de foco visible |

### Mejoras sugeridas
- [ ] Revisar landmarks y roles ARIA en cada plantilla
- [ ] Verificar navegación completa por teclado en los flujos críticos
- [ ] Añadir captions/transcripts al multimedia

## 5. RESUMEN Y PLAN DE ACCIÓN
| Prioridad | Área | Acción | Esfuerzo |
|-----------|------|--------|----------|
| Alta | Rendimiento | Corregir LCP/CLS (imágenes, lazy loading, layouts estables) | Medio |
| Alta | Accesibilidad | Resolver violaciones WCAG de severidad alta | Medio |
| Alta | SEO | Desbloquear rastreo (robots/sitemap/canonical) | Bajo |
| Media | SEO | Completar meta tags, Open Graph y Schema.org | Bajo |
| Media | Accesibilidad | Formularios: errores visibles y asociados | Medio |
| Baja | Rendimiento | Compresión Brotli y caché agresiva de estáticos | Bajo |

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
- Para pruebas E2E → `webapp-testing`.
