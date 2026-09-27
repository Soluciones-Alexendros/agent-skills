# Playbook operativo — 8 fases de la auditoría E2E

## Índice
1. FASE 0 Pre-flight · 2. FASE 1 Discovery · 3. FASE 2 Loop del agente · 4. FASE 3 Los 7 motores · 5. FASE 4 Evaluación visual · 6. FASES 5–7 Compliance, informe y RICE

## FASE 0 — Pre-flight

1. Resolver `TARGET_URL` (canonical, incl. redirección www/apex).
2. Detectar stack: cabeceras (`x-powered-by`, `server`), `window.__NEXT_DATA__`, meta generator, patrones de assets (`/wp-content/`, `/_next/`).
3. Autenticación: si hay login, pedir credenciales de prueba; nunca auditar con credenciales reales del usuario. Generar `auth.json` _(ejemplo: credencial local generada)_ (storageState) para la persona `usuario_logueado`.
4. Personas: `visitante_nuevo` (sin cookies), `usuario_logueado` (storageState), `mobile_user` (viewport 390 + user agent móvil). La auditoría se repite por persona.
5. Seguridad del auditor: **nunca** ejecutar submits con efectos reales en producción (pagos, emails masivos, borrados). Si se detecta un formulario de este tipo, registrar como PENDING y probar en staging.
6. Config: `assets/playwright.config.ts` (trace on-first-retry, actionTimeout 10s, navigationTimeout 30s).

## FASE 1 — Discovery Engine (state machine)

- Estado = URL + storage + cookies + rol. Acciones = elementos con role button/link/combobox/textbox, `a[href]`, `[data-testid]`, contenido de shadow DOM e iframes.
- Ejecutar `scripts/discovery.py` (anti-trampas: MAX_DEPTH 12, MAX_PAGES 150, ignora `/logout`,`/admin`,`/wp-admin`, corta `?page=` a 5). El crawler de red es la primera pasada; el agente con navegador enriquece el mapa con estados dinámicos (modales, drawers) que el crawler HTTP no ve.
- Salida: `output/site-map.json` _(ejemplo: fichero generado)_ con `{url, depth, parentAction, status, type: page|modal|drawer|form, discoveredElements}` y la lista de formularios únicos.

## FASE 2 — Loop del agente auditor

Por nodo y persona: cargar → `networkidle` → capturar ariaSnapshot + consola + pageerrors + requests ≥400 → medir (`assets/measure.js` vía `page.evaluate`) → planificar con `prompts/SYSTEM_AUDITOR.md` → actuar con self-healing locators (getByRole > getByTestId > getByText; si un selector falla, proponer 2 alternativas; nunca XPath absoluto). Referencia: `assets/auditor.agent.ts`.

Reglas: cada acción declara qué prueba y qué espera; si el éxito no es verificable (visual o de red), el check es FAIL, nunca "asumido".

## FASE 3 — Los 7 motores de checks

1. **Funcional** (FN): click en todo lo accionable (trial-click), pageerror/console.error, requests ≥400, dropdowns que cierran con ESC y click fuera, modales con foco atrapado y retorno de foco, doble submit.
2. **Formularios** (FM) triple pasada: A) vacío → errores visibles y asociados (`aria-describedby`, `aria-invalid`); B) inválidos (email `test@`, pass `123`) → bloquean submit; C) válidos con datos contextuales (faker + LLM según el label) → éxito (toast/redirect) sin 500 ni doble submit. Autocomplete correcto.
3. **UI/Responsive** (UI): 3 viewports (1440/768/390), screenshot diff, `scripts/measure_analyze.py` para touch targets 44px (mín. 24px), font ≥12px, line-height ≥1.4, grid 8pt, distorsión de imágenes, overflow horizontal (Crítica).
4. **Accesibilidad** (AC): `new AxeBuilder({ page }).analyze()` por URL (0 critical/serious), más manual: orden de foco, h1 único, skip link, landmarks, lang.
5. **Performance/SEO** (PF/SE): Lighthouse por URL clave (LCP ≤2.5s, CLS ≤0.1, INP ≤200ms; si falla, grabar trace); title 50–60, description 120–158, canonical, OG, schema.org, sitemap.
6. **Seguridad frontend** (SG): `type=password` + `autocomplete=new-password`, sin tokens/PII en localStorage, cookies `Secure; SameSite`, mixed content, cabeceras CSP/HSTS/X-Content-Type-Options/Referrer-Policy.
7. **Motion** (MO): `prefers-reduced-motion` respetado (emular y verificar), `transitionDuration` ≤500ms, animaciones infinitas con control de pausa, sin bloqueo de pointer-events ni layout thrashing.

## FASE 4 — Evaluación visual LLM

Por URL: `desktop.png`, `mobile.png`, `trace.zip`, `console.log` en `output/evidence/` _(ejemplos: evidencias generadas)_. Aplicar `prompts/EVALUATOR_VISUAL.md` (jerarquía, CTA 15–20% más prominente, desalineaciones >4px, distorsión, overflow, gaps <8px). Salida JSON: `{visualScore: 0-100, issues: [{type, description, bbox, severity, recommendation}]}`.

## FASES 5–7 — Compliance, informe y RICE

1. Consolidar todo en `output/compliance.json` _(ejemplo: fichero generado)_ (schema `checklist.schema.json`; validar con `scripts/validate_compliance.py`).
2. `scripts/score.py` → veredicto APTO / APTO CON OBSERVACIONES / NO APTO (1 FAIL Crítica ⇒ NO APTO).
3. `scripts/report.py` → REPORT.md + REPORT.html + issues.csv _(ejemplos: informes generados)_.
4. Plan RICE según `references/remediation.md` con criterio de aceptación Playwright por tarea y fecha de re-auditoría.
