---
name: verificar-fullaudit
version: "2.0.0"
description: >
  Auditoría web completa en 5 modos (compliance, e2e, performance, local, full):
  matriz de 93 checks unificados (SEO, accesibilidad WCAG 2.2 AA/EN 301 549, RGPD,
  Core Web Vitals, QA E2E con evidencias), dictamen dual compliance+e2e, informe
  de cierre y roadmap RICE en 4 sprints. Usar para auditoría web completa, QA E2E
  con Playwright, compliance SEO/a11y/legal, performance CWV o tests en localhost.
license: MIT
metadata:
  author: Soluciones-Alexendros
  dominio: verificar
  idioma: es
---

# verificar-fullaudit — Auditoría web completa (5 modos)

Fusión de `web-playwright` (QA E2E con evidencias) + `webapp-testing` (apps locales)
+ `arquitectura` (procedimiento y scoring). Registry unificado de **93 checks**
(`core/configs/checks.json`): 51 compliance (ACC/TEC/ONP/OFF/SEM/ANA/LEG) + 42 e2e
(RT/FN/FM/UI/AC/PF/SE/SG/MO). Umbrales y RICE unificados en `core/configs/thresholds.json`.

## Modos (automatizado al lanzar o preguntado a IA)

Al lanzar la skill: si el usuario indicó modo (`full`, `compliance`, `e2e`,
`performance`, `local`), aplicarlo directamente; si no, la IA pregunta antes de auditar.

| Modo | Origen | Cuándo | Entrada |
|---|---|---|---|
| `compliance` | verificar-compliance | Matriz SEO/A11y/SEM/legal de sitio público | `modes/compliance/run.py --checks …` |
| `e2e` | web-playwright | QA E2E con evidencias de navegador | `modes/e2e/run.py --compliance …` |
| `performance` | web-rendimiento→verificar-performance | CWV/rendering/caching (puente a skill `verificar-performance`) | `modes/performance/run.py --checks …` |
| `local` | webapp-testing | App en `localhost`: flujos UI y capturas | `modes/local/run.py --target …` |
| `full` | fusión (defecto en "auditoría completa") | compliance + e2e, dictamen dual | `modes/full/run.py --checks a.json b.json` |

Detalle por modo: `modes/<modo>/README.md` + `modes/<modo>/refs.md` + `modes/<modo>/run.py`.

## Reglas de calidad (obligatorias)

- Toda marca **PASS requiere evidencia medible**; sin evidencia → PENDING, nunca PASS.
- En e2e: **nunca reportar un fallo sin evidencia** (`locator` + screenshot + console/network).
- Cada hallazgo lleva ID permanente del registry, severidad (Crítico/Alto/Medio/Bajo) y acción correctiva.
- **Dictamen dual**: compliance POSITIVO/PARCIAL/NEGATIVO + veredicto e2e
  APTO/APTO CON OBSERVACIONES/NO APTO. 1 FAIL Crítico ⇒ NEGATIVO / NO APTO.
- **Umbrales CWV**: LCP ≤2.5s · INP ≤200ms · CLS ≤0.1 · TTFB ≤800ms.
  **Semáforo**: Verde ≥90 / Ámbar 70–89 / Rojo <70.
- **RICE 4 sprints**: Sprint 0 Crítico (48h) → S1 Alto (sem. 1) → S2 Medio (sem. 2) → S3 Bajo (sem. 3).

## Flujo común

1. **Alcance**: objetivo + modo (ver tabla); normativa WCAG 2.2 AA siempre (EN 301 549/EAA si B2C UE).
2. **Inventario**: `core/utils/discovery.py` (crawl, `--root-dir` para local) y/o
   `core/utils/audit_page.py` por plantilla.
3. **Evaluación**: checks del registry según modo; manual obligatorio en a11y (teclado, zoom 200%, contraste).
4. **Fusión** (si varias fuentes): `core/utils/merge_results.py a.json b.json`.
5. **Scoring**: `core/utils/orchestrator.py --mode <modo> --checks … --outdir output/`
   (o `modes/<modo>/run.py`).
6. **Informe**: `REPORT.md` + `REPORT.html` + `issues.csv` + roadmap RICE.

## Herramientas (core, stdlib Python sin dependencias)

| Script | Uso |
|---|---|
| `core/utils/orchestrator.py --mode=…` | Pipeline scoring→informe por modo (`--list-modes`) |
| `core/utils/merge_results.py` | Fusiona resultados compliance+e2e |
| `core/scoring/score.py` | % por dominio, semáforo, dictamen dual, RICE+sprint |
| `core/scoring/rice.py` | `rice_score`, `sprint_for`, `deuda_horas` (librería) |
| `core/reporting/report.py` | Informe Markdown/HTML + CSV |
| `core/reporting/contrast.py` | Ratio de contraste WCAG |
| `core/utils/discovery.py` | Crawler con anti-trampas → `site-map.json` |
| `core/utils/audit_page.py` | Auditoría estática de una URL → JSON |
| `core/utils/measure_analyze.py` | Mediciones navegador → checks UI-01..UI-07 |
| `core/utils/validate_compliance.py` | Valida `compliance.json` contra el schema |
| `core/utils/selftest.py` | Smoke ejecutable (exit 0/1) |

Ejecutar **siempre** `python3 core/utils/selftest.py` tras modificar scripts o configs;
detalle en `core/references/troubleshooting.md`.

## Entregables

1. `output/score.json` (trazabilidad) · `REPORT.md` + `REPORT.html` · `issues.csv` (Jira/Linear).
2. Dictamen dual + roadmap RICE 4 sprints con owners y KPIs.

## Uso

Usar cuando el usuario pida auditoría web completa, auditoría E2E/Playwright, QA funcional,
tests en localhost, compliance SEO/a11y/legal, performance CWV o plan de remediación RICE.
Para performance profunda → skill `verificar-performance`; compliance puro aislado → `verificar-compliance`;
diseño → `disenar-interfaz` / `disenar-design-system`. Ver frontmatter `description`.

## Estructura

- `SKILL.md` — modos, reglas, flujo y herramientas.
- `core/configs/` — `checks.json` (93 checks unificados), `thresholds.json` (umbrales + RICE unificados).
- `core/scoring/` — `score.py` + `rice.py` unificados.
- `core/reporting/` — `report.py` + `contrast.py`.
- `core/utils/` — `orchestrator.py` (`--mode=compliance|e2e|performance|local|full`),
  `merge_results.py`, `selftest.py` + `audit_page/discovery/measure_analyze/validate_compliance.py` migrados.
- `core/assets/schemas/` — schema de `compliance.json`.
- `core/references/` — `playbook.md`, `remediation.md`, `troubleshooting.md`, `checklist.md`, `glossary.md` fusionados.
- `modes/compliance|e2e|performance|local|full/` — README + `refs.md` + `run.py` (+ assets/prompts en e2e).
- `tests/unit/` + `tests/integration/` — pytest (ver Tests).

## Tests

- `python3 core/utils/selftest.py` — smoke sin dependencias.
- `pytest tests/` — al menos 1 test por modo que importa `orchestrator`/`score` sin errores
  (`tests/integration/test_modes.py`) + unitarios de scoring/RICE/merge.

## Referencias

- `core/references/playbook.md` — procedimiento fusionado y reglas de oro.
- `core/references/checklist.md` — matriz de 93 checks y umbrales.
- `core/references/remediation.md` — roadmap RICE, templates de código.
- `core/references/glossary.md` — glosario.
- `core/references/troubleshooting.md` — problemas conocidos y resolución.
- Origen: fusión 2026-09 de `web-playwright` + `webapp-testing` (+ procedimiento de arquitectura);
  `verificar-compliance` y `verificar-performance` siguen como skills independientes.
