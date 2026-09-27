---
name: web-compliance
description: >
  Auditoría de compliance web: accesibilidad (WCAG 2.2 AA / EN 301 549), legal
  (RGPD, Consent Mode v2, aviso legal, cookies), SEO on-page/off-page/SEM/analítica.
  Matriz de checks PASS/FAIL/N/A, scoring ponderado, dictamen POSITIVO/NEGATIVO/PARCIAL
  y plan de remediación RICE. Usar para auditoría de cumplimiento, dictamen de
  compliance web, plan de remediación SEO/accesibilidad/legal.
license: MIT
metadata:
  author: Soluciones-Alexendros
  version: "1.0.0"
  dominio: web
  idioma: es

---

# Web Compliance — Auditoría de cumplimiento web

Auditoría extremo a extremo de un website objetivo con evidencia medible, matriz de compliance y dictamen. Flujo único (one-shot): FASE 0→8, matriz, dictamen, roadmap.

## Reglas de calidad (obligatorias)

- Toda marca **PASS requiere evidencia medible** (URL, dato, salida de script o captura). Nunca marcar ✅ sin evidencia; usar PENDING si no es verificable.
- Cada hallazgo lleva ID permanente del registry (`configs/checks.json`), severidad (Crítico/Alto/Medio/Bajo), evidencia y acción correctiva.
- Declarar limitaciones: checks no ejecutables (sin acceso GSC/GAds, login, JS sin render) quedan como PENDING con motivo, nunca como PASS.
- Criterio de dictamen enterprise: **POSITIVO** solo si 0 FAIL Críticos, ≥90% PASS en pilar Accesibilidad, ≥85% en SEO Técnico y Consent Mode v2 conforme si hay analítica/pauta. Un FAIL Crítico fuerza **NEGATIVO**. Intermedio: **PARCIAL**.
- Idioma del informe: el del operador.

## Flujo one-shot

1. **FASE 0 — Alcance.** Confirmar/obtener: dominio (apex + subdominios), idiomas, entorno, accesos (GSC, GA4, GTM, GAds) y si hay campañas SEM activas (si no, SEM y parte de ANA → N/A justificado). Fijar normativa aplicable: WCAG 2.2 AA siempre; EN 301 549 / EAA si servicio B2C en UE; ADA/508 si EE. UU.
2. **FASE 1 — Inventario y crawl.** Ejecutar `scripts/audit_page.py` sobre la home y cada plantilla detectable (categoría, ficha/artículo, landing, contacto). Descargar `robots.txt` y `sitemap.xml`. Complementar con crawl externo (Screaming Frog/Sitebulb) si está disponible; si no, muestreo manual documentado.
3. **FASES 2–7 — Evaluación por pilares.** Rellenar la matriz usando el registry `configs/checks.json` (51 checks: ACC, TEC, ONP, OFF, SEM, ANA, LEG). Detalle de criterios, umbrales y protocolos manuales en `references/` (leer solo la referencia del pilar en curso):
   - Accesibilidad → `references/wcag22.md` (50% automatizado vía script + 50% manual obligatorio: teclado, zoom 200%, contraste vía `scripts/contrast.py`).
   - SEO técnico y on-page → `references/playbook.md`.
   - SEM/PPC y analítica → `references/sem.md`.
   - Legal/compliance → `references/playbook.md` §Fase LEG.
4. **FASE 8 — Scoring y dictamen.** Ejecutar `scripts/score.py` con los resultados para calcular % por pilar, semáforo (Verde ≥90 / Ámbar 70–89 / Rojo <70) y dictamen según `configs/thresholds.json`.
5. **Informe de cierre.** Generar con `scripts/report.py` (o manualmente siguiendo `references/remediation.md` §formato): resumen ejecutivo, matriz completa con evidencias, hallazgos detallados, roadmap RICE 90 días (Sprint 1 <72h Críticos, Sprint 2 <2 semanas Altos, Sprint 3 <30 días Medios) y fecha de re-auditoría.
6. **Plan de soluciones + mejoras.** Todo FAIL → acción correctiva con owner, esfuerzo y KPI de validación. Añadir siempre un bloque de mejoras proactivas más allá del cumplimiento (ver `references/remediation.md`).

## Herramientas

| Script | Uso | Salida |
|---|---|---|
| `scripts/audit_page.py <url> [--json out.json]` | Audita una URL: HTTPS, headers, meta, headings, alt, lang, canonical, hreflang, JSON-LD, skip-link, labels, mixed content, robots/sitemap | JSON de checks automatizables |
| `scripts/contrast.py <fg> <bg> [--large]` | Ratio de contraste WCAG y veredicto AA/AAA | JSON |
| `scripts/score.py <results.json>` | % compliance por pilar, semáforo, dictamen, deuda en horas | JSON |
| `scripts/report.py <results.json> [--md out.md]` | Informe de cierre en Markdown con matriz y dictamen | Markdown |
| `scripts/selftest.py` | Suite de tests integrada (fixtures PASS/FAIL, contraste, scoring, report) | exit 0/1 |

Scripts en stdlib de Python, sin dependencias externas.

Ejecutar **siempre** `python3 scripts/selftest.py` tras cualquier modificación de scripts o configs; ante fallo, consultar `references/troubleshooting.md`.

## Entregables al usuario

1. Informe de cierre (Markdown/HTML) con matriz ✅/❌/⚠️/➖ y dictamen.
2. Roadmap de remediación priorizado RICE con owners y KPIs.
3. JSON de resultados (trazabilidad máquina-legible).

## Referencias

- `references/playbook.md` — procedimiento detallado de las 8 fases y criterios SEO/LEGAL.
- `references/checklist.md` — matriz canónica de 51 checks con estándar, método y severidad.
- `references/wcag22.md` — criterios WCAG 2.2 AA, protocolos manuales (teclado, NVDA, zoom, daltonismo, formularios).
- `references/sem.md` — auditoría Google Ads, benchmarks por industria, checklist de landing pages.
- `references/seo-source.md` — SEO avanzado (absorbida de `web-audit`).
- `references/a11y-source.md` — accesibilidad y UX (absorbida de `web-audit`).
- Rendimiento/CWV: ver `web-performance` (antes `web-rendimiento`, renombrada 2026-09; esta skill conserva compliance).
- `references/remediation.md` — roadmap 5 fases, matriz esfuerzo-impacto, templates de código (skip-link, form accesible, JSON-LD).
- `references/glossary.md` — glosario técnico y stack de herramientas.
- `references/troubleshooting.md` — problemas conocidos de los scripts y su resolución.
- Producto distinto: `web-fullaudit` (modos e2e/full) — auditoría E2E con Playwright (UI funcional y RICE por sprint); no duplicar: esta skill es scoring de compliance SEO/A11y/SEM/legal, aquella es QA funcional/UI con evidencias de navegador.

## Caso de referencia: alexendros.dev

Si el objetivo es `alexendros.dev` _(ejemplo)_ (Astro + Vercel), aplicar hallazgos conocidos documentados en `references/caso-alexendros.md` (skip-link ausente, falta JSON-LD Person, CMP pendiente) como baseline a re-verificar, nunca como evidencia vigente.

## Uso

Usar cuando el usuario pida auditar un sitio web, revisar posicionamiento/SEO/SEM, verificar accesibilidad WCAG/EN 301 549/EAA, comprobar cumplimiento legal web (cookies, consentimiento, aviso legal), generar informe de cierre con checks de verificación o plan de remediación SEO/accesibilidad. Ver frontmatter `description` y flujo one-shot FASE 0→8.

## Estructura

- `SKILL.md` — flujo one-shot, reglas de calidad y entregables.
- `configs/checks.json` — registry de 51 checks (fuente de verdad); `configs/thresholds.json` — umbrales y dictamen.
- `references/` — `playbook.md`, `checklist.md`, `wcag22.md`, `sem.md`, `remediation.md`, `glosario` en `glossary.md`, `troubleshooting.md`, `caso-alexendros.md` _(ejemplo)_, `seo-source.md` y `a11y-source.md` (absorbidas de `web-audit`).
- Nota v0.1.0: el Playbook legacy v1.0 (duplicado de `playbook.md`) fue eliminado del repo; `references/playbook.md` es la fuente vigente.
- `scripts/` — 5 scripts stdlib (ver Herramientas); `tests/` — fixtures y tests (no tocar).
