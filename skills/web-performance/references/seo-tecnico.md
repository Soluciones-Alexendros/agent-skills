# SEO técnico — checklist de rastreo e indexación

Fuente migrada de `web-audit` (Etapa 3 + plantilla de estado). Cubre la parte técnica
del SEO necesaria en una auditoría de rendimiento; el SEO on-page/off-page, SEM y
posicionamiento profundo viven en `web-compliance`.

## Herramientas

Lectura HTML, robots.txt, sitemap.xml, meta tags.

## Checklist

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

## Estado actual (plantilla)

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

## Recomendaciones

- [ ] Corregir los checks ✗ empezando por los que afectan al rastreo (robots, sitemap, canonical)
- [ ] Completar los checks ~ con evidencia adjunta en el informe
- [ ] Re-auditar tras las correcciones y regenerar la tabla de estado
