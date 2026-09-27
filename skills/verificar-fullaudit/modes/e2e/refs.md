# Refs modo e2e

## Motores y checks (42)

- **RT Rutas** (4): 200 sin 404/500 enlazados, ≤1 salto de redirección, sitemap/robots coherentes.
- **FN Funcional** (6): botones, dropdowns, navegación, estados vacíos/error, paginación (corte en 5).
- **FM Formularios** (6): triple pasada vacío → inválido → válido; mensajes asociados; foco en error.
- **UI/UX medida** (7): touch ≥44px, fuente ≥12px, line-height ≥1.4, grid 8pt, header ≤25% viewport,
  CTA prominente, gap ≥8px. Medir con `assets/measure.js` + `core/utils/measure_analyze.py`.
- **AC Accesibilidad** (5): axe-core 0 violaciones críticas + manuales (foco, nombres accesibles).
- **PF Performance** (4): LCP ≤2.5s, INP ≤200ms, CLS ≤0.1 (lab + field).
- **SE SEO** (3): title 50–60, description 120–158, canonical/OG.
- **SG Seguridad frontend** (4): HTTPS, headers, mixed content, formularios (CSRF/autocomplete).
- **MO Motion** (3): `prefers-reduced-motion`, transiciones ≤500ms, sin animación bloqueante.

## Prompts y assets

- `assets/auditor.agent.ts` — loop recolectar → pensar → actuar (self-healing locators).
- `assets/playwright.config.ts` — `storageState`, traces, timeouts.
- `prompts/SYSTEM_AUDITOR.md` — planificación de acciones del agente.
- `prompts/EVALUATOR_VISUAL.md` — jerarquía, alineación >4px, proporciones, overflow.

## Umbrales

Veredicto APTO: 0 FAIL Críticas + global ≥90%. Ver `core/configs/thresholds.json` → `veredicto_e2e`.
