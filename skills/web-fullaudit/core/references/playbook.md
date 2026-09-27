# Playbook Fullaudit — procedimiento fusionado

Fusión de `web-compliance` (matriz FASE 0→8, 51 checks) + `web-playwright`
(8 fases E2E, 7 motores) + `webapp-testing` (apps locales). Detalle por modo
en `modes/<modo>/README.md`; esto es el mapa común.

## Reglas de oro (todos los modos)

- **Evidencia o nada**: un PASS sin evidencia medible (URL, dato, salida de script,
  captura, locator) es PENDING. Un fallo sin evidencia (locator + screenshot +
  console/network en e2e) no se reporta.
- **ID permanente**: todo hallazgo cita su ID del registry (`core/configs/checks.json`,
  93 checks unificados) + severidad (Crítico/Alto/Medio/Bajo) + acción correctiva.
- **N/A justificado**: SEM/ANA sin campañas ni accesos, checks no ejecutables
  (login sin credenciales, JS sin render) → PENDING/N/A con motivo, nunca PASS.
- **Dictamen dual**: compliance POSITIVO/PARCIAL/NEGATIVO + veredicto e2e
  APTO/APTO CON OBSERVACIONES/NO APTO. 1 FAIL Crítico ⇒ NEGATIVO / NO APTO.

## FASE 0 — Alcance y modo

1. Fijar objetivo (URL pública, sitio estático local o `localhost`).
2. Elegir modo: `orchestrator.py --list-modes`. Al lanzar la skill, el modo se
   aplica automáticamente si el usuario lo indicó (`full`, `compliance`, `e2e`,
   `performance`, `local`); si no, la IA pregunta antes de auditar.
3. Personas y viewports e2e: `visitante_nuevo`, `usuario_logueado`, `mobile_user`;
   1440/768/390 (`core/configs/thresholds.json`).
4. Normativa: WCAG 2.2 AA siempre; EN 301 549/EAA si B2C en UE; ADA/508 si EE. UU.

## FASE 1 — Inventario y crawl

- Sitio público: `core/utils/audit_page.py` por plantilla + `robots.txt`/`sitemap.xml`.
- E2E: `core/utils/discovery.py <URL> --out site-map.json` (anti-trampas:
  MAX_DEPTH=12, MAX_PAGES=150, ignora `/logout`, `/admin`; `--root-dir` para local).
- Local: confirmar servidor dev arriba (o helper del proyecto) antes de Playwright.

## FASES 2–7 — Motores de evaluación

| Motor | Checks | Método |
|---|---|---|
| Compliance SEO/A11y/SEM/legal | ACC/TEC/ONP/OFF/SEM/ANA/LEG (51) | script + manual (teclado, zoom 200%, contraste) |
| Funcional + formularios | RT/FN/FM | triple pasada (vacío → inválido → válido), locators resilientes |
| UI/Responsive | UI-01..UI-07 | `modes/e2e/assets/measure.js` + `measure_analyze.py` |
| A11y navegador | AC-01..AC-05 | axe-core + manuales |
| Performance/SEO/Motion | PF/SE/MO/SG | Lighthouse 12 + `web-performance` |
| Evaluación visual LLM | — | `modes/e2e/prompts/EVALUATOR_VISUAL.md` (desktop+mobile) |

## FASE 8 — Scoring, informe y RICE

1. Fusionar (si hay varias fuentes): `merge_results.py a.json b.json`.
2. Puntuar: `orchestrator.py --mode <modo> --checks … --outdir output/`
   (semáforo Verde ≥90 / Ámbar 70–89 / Rojo <70; CWV LCP ≤2.5s, INP ≤200ms, CLS ≤0.1).
3. Informar: `REPORT.md` + `REPORT.html` + `issues.csv` (Jira/Linear).
4. Plan RICE 4 sprints: Sprint 0 Crítico (48h) → S1 Alto (sem. 1) → S2 Medio (sem. 2) → S3 Bajo (sem. 3).
