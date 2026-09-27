---
name: web-playwright
version: "1.0.0"
description: >
  Auditoría E2E autónoma con Playwright: crawling, testing funcional de
  botones/dropdowns/formularios (triple pasada), medición de componentes (touch targets,
  grid 8pt), accesibilidad WCAG 2.2 AA (axe), performance/CWV, SEO, seguridad frontend
  y motion. Checklist PASS/FAIL con evidencias (locator + screenshot + console),
  informe ejecutivo y plan RICE en 4 sprints. Usar para auditoría E2E completa,
  QA automatizado con Playwright, checklist de compliance con evidencias.
license: MIT
metadata:
  author: Soluciones-Alexendros
  dominio: web
  idioma: es

---

# Web Playwright — Auditoría E2E autónoma con evidencias

Playwright = manos y ojos. LLM = cerebro. Regla de oro: **nunca reportar un fallo sin evidencia** (`locator` + screenshot + console/network). Un check no verificable es `N/A` o `PENDING`, jamás `PASS`.

## Flujo one-shot (8 fases)

1. **FASE 0 — Pre-flight.** Resolver `TARGET_URL`; detectar stack (headers, `__NEXT_DATA__`, generadores); detectar auth (si hay login, pedir credenciales de prueba o registrar cuenta con datos faker); fijar 3 personas (`visitante_nuevo`, `usuario_logueado`, `mobile_user`) y viewports (1440/768/390). Si Playwright no está disponible en el entorno, ejecutar modo degradado con los scripts Python (crawler + checks estáticos) y declarar la limitación.
2. **FASE 1 — Discovery.** `python3 scripts/discovery.py <TARGET_URL> --out output/site-map.json` _(ejemplo: ruta de salida generada)_ (state-machine crawl con anti-trampas: MAX_DEPTH=12, MAX_PAGES=150, ignora `/logout`, `/admin`, `/wp-admin`, corta paginación `?page=` a 5). Identificar formularios y componentes interactivos únicos.
3. **FASE 2 — Loop del agente auditor** (por persona y por nodo): cargar página, capturar `ariaSnapshot`, consola, pageerrors y requests ≥400; medir componentes inyectando `assets/measure.js` con `page.evaluate`; planificar acciones con `prompts/SYSTEM_AUDITOR.md`; actuar con locators resilientes (getByRole > getByTestId > getByText; nunca XPath absoluto; si falla, 2 alternativas). Referencia de implementación: `assets/auditor.agent.ts`.
4. **FASE 3 — 7 motores de checks.** Detalle en `references/playbook.md`: Funcional, Formularios (triple pasada: vacío → inválido → válido), UI/Responsive (3 viewports + screenshot diff), A11y (axe-core + checks manuales), Performance/SEO (Lighthouse + tags), Seguridad frontend, Motion (`prefers-reduced-motion`, transiciones >500ms).
5. **FASE 4 — Evaluación visual LLM.** Por URL: `desktop.png` + `mobile.png` evaluados con `prompts/EVALUATOR_VISUAL.md` (jerarquía, alineación >4px, proporciones, overflow).
6. **FASE 5 — Compliance.** Consolidar hallazgos en `output/compliance.json` _(ejemplo: fichero generado)_ y validarlo: `python3 scripts/validate_compliance.py output/compliance.json` (schema `checklist.schema.json`). Analizar mediciones: `python3 scripts/measure_analyze.py output/measurements.json` _(ejemplo: fichero generado)_.
7. **FASE 6 — Scoring e informe.** `python3 scripts/score.py output/compliance.json --json output/score.json` → `python3 scripts/report.py output/score.json --outdir output/` genera `REPORT.md`, `REPORT.html` _(ejemplos: informes generados)_ (dashboard con filtros) e `issues.csv` (importable a Jira/Linear).
8. **FASE 7 — Plan RICE.** Sprint 0 (Críticas, 48h) → Sprint 1 (Altas, sem. 1) → Sprint 2 (Medias, sem. 2) → Sprint 3 (Bajas, sem. 3). Cada tarea: problema → causa raíz → solución con código → criterio de aceptación como test Playwright. Ver `references/remediation.md`.

## Herramientas

| Script | Función |
|---|---|
| `scripts/discovery.py <url> [--root-dir DIR] [--max-pages N]` | Crawler con anti-trampas → `site-map.json`. `--root-dir` audita un sitio estático local (offline/tests) |
| `scripts/measure_analyze.py <measurements.json>` | Convierte mediciones del navegador en checks UI-01..UI-07 (touch targets, tipografía, grid 8pt, distorsión, overflow) |
| `scripts/validate_compliance.py <compliance.json>` | Valida contra `checklist.schema.json` (required, enums, URI) sin dependencias |
| `scripts/score.py <compliance.json>` | % compliance por categoría, semáforo, score RICE por hallazgo, asignación de sprint |
| `scripts/report.py <score.json> --outdir DIR` | Genera REPORT.md + REPORT.html + issues.csv |
| `scripts/selftest.py` | Suite de tests integrada (exit 0/1). Ejecutar tras cualquier cambio |

Scripts en Python stdlib puro, sin dependencias.

## Assets para el navegador (Playwright)

- `assets/measure.js` — snippet para `page.evaluate`: bounding boxes, computed styles, grid 8pt, distorsión de imágenes, overflow.
- `assets/auditor.agent.ts` — loop autónomo de referencia (recolectar → pensar → actuar con self-healing locators).
- `assets/playwright.config.ts` — config con `storageState`, traces y timeouts.

## Umbrales y checks

Fuente de verdad: `configs/checks.json` (42 checks con ID, categoría, método, severidad, referencia WCAG) y `configs/thresholds.json` (touch target 44px/24px, font ≥12px, line-height ≥1.4, grid 8pt, CWV LCP/INP/CLS, transiciones ≤500ms, sprints RICE). Vista rápida en `references/checklist.md`.

## Referencias

- `references/playbook.md` — procedimiento detallado de las 8 fases y los 7 motores.
- `references/checklist.md` — matriz de checks por categoría y criterios de dictamen.
- `references/remediation.md` — plan RICE, templates de código y criterios de aceptación Playwright.
- `references/troubleshooting.md` — problemas conocidos de scripts y Playwright, con resolución.
- Producto distinto: `web-compliance` — auditoría de compliance SEO/A11y/SEM/legal con scoring ponderado y dictamen; no duplicar: esta skill es QA E2E funcional/UI con evidencias de navegador y RICE por sprint, aquella es matriz de compliance y dictamen.

## Entregables

`output/site-map.json` _(ejemplo: generado)_ · `output/compliance.json` _(ejemplo: generado, validado)_ · `output/evidence/` _(ejemplo: generado)_ (screenshots, traces) · `REPORT.md` + `REPORT.html` _(ejemplos: generados)_ · `issues.csv` _(ejemplo: generado)_ · `REMEDIATION_PLAN.md` _(ejemplo: generado)_ (RICE).

## Uso

Usar cuando el usuario pida auditar una web E2E, test completo, revisión de formularios/botones, auditoría UX/UI/accesibilidad/performance, checklist de compliance con evidencias, QA automatizado con Playwright o plan de remediación. Ver frontmatter `description` y flujo one-shot de 8 fases.

## Estructura

- `SKILL.md` — flujo one-shot y regla de oro de evidencia.
- `configs/checks.json` — registry de 42 checks (fuente de verdad); `configs/thresholds.json` — umbrales CWV/UI/SEO y veredicto; `assets/schemas/checklist.schema.json` — schema de `compliance.json`.
- `references/` — `playbook.md`, `checklist.md`, `remediation.md`, `troubleshooting.md` (leer bajo demanda).
- `prompts/` — `SYSTEM_AUDITOR.md`, `EVALUATOR_VISUAL.md`; `assets/` — `measure.js`, `auditor.agent.ts`, `playwright.config.ts`.
- `scripts/` — 6 scripts stdlib (ver Herramientas); `tests/` — fixtures y tests (no tocar).
- Rutas `output/*`, `REPORT.md`, `REPORT.html`, `issues.csv`, `REMEDIATION_PLAN.md`, `site-map.json` y `auth.json` son artefactos generados o credenciales locales _(ejemplos)_, no fuentes versionadas.
