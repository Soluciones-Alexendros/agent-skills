# Modo e2e — QA E2E con evidencias de navegador

Fusión del flujo `web-playwright` (8 fases, 7 motores, 42 checks RT/FN/FM/UI/AC/PF/SE/SG/MO).

## Flujo

1. **Pre-flight**: `TARGET_URL`, stack, auth (credenciales de prueba), personas
   (`visitante_nuevo`, `usuario_logueado`, `mobile_user`), viewports 1440/768/390.
   Sin Playwright → modo degradado (crawler + estáticos) declarado en el informe.
2. **Discovery**: `core/utils/discovery.py <URL> --out site-map.json`
   (`--root-dir` para sitio estático local).
3. **Loop auditor**: por persona y nodo — ariaSnapshot, consola, pageerrors,
   `page.evaluate(assets/measure.js)`; locators resilientes
   (getByRole > getByTestId > getByText; ver `assets/auditor.agent.ts`,
   `prompts/SYSTEM_AUDITOR.md`).
4. **7 motores**: funcional, formularios (triple pasada), UI/responsive (3 viewports),
   a11y (axe + manual), performance/SEO (Lighthouse), seguridad frontend, motion.
5. **Evaluación visual LLM**: desktop + mobile con `prompts/EVALUATOR_VISUAL.md`.
6. **Compliance**: consolidar `compliance.json` (array formato e2e) y validar con
   `core/utils/validate_compliance.py` (schema `core/assets/schemas/`).
7. **Scoring e informe**: `run.py --compliance compliance.json --outdir output/`
   → veredicto APTO/APTO CON OBSERVACIONES/NO APTO.
8. **Plan RICE**: 4 sprints con código de solución y criterio de aceptación Playwright.

## Regla de oro

Nunca reportar un fallo sin evidencia (`locator` + screenshot + console).
No verificable → N/A o PENDING, jamás PASS.

## Refs específicas

Ver `refs.md` (motores, medición UI, seguridad frontend, prompts).
