# Troubleshooting Fullaudit

## Scripts

- `ModuleNotFoundError: score/rice/report` → ejecutar desde su directorio o usar
  `orchestrator.py` / `selftest.py`, que ajustan `sys.path` solos. En pytest, `tests/conftest.py` lo hace.
- `JSON inválido` (exit 2) → validar con `python3 -m json.tool fichero.json`.
- `validate_compliance.py` exit 1 → el `compliance.json` no cumple
  `core/assets/schemas/checklist.schema.json` (revisar `required`, enums `category`/`status`/`severity`, URIs).
- `discovery.py` no avanza → mirar `ignore_paths` y `max_pages` en
  `core/configs/thresholds.json` → `crawler`; webs con anti-bot requieren modo degradado declarado.
- `measure_analyze.py` sin elementos → `assets/measure.js` debe inyectarse con
  `page.evaluate` tras `networkidle`; sin Playwright no hay mediciones.

## Playwright / navegador

- Playwright no instalado → modo degradado (crawler + checks estáticos) y declarar
  la limitación en el informe; nunca marcar PASS lo no verificado.
- Timeouts en SPAs pesadas → subir `timeout_ms`, esperar selector estable en vez de `networkidle`.
- Login con MFA/captcha → pedir credenciales de prueba o cuenta dedicada; sin acceso, PENDING.

## Scoring

- `SIN DATOS` → ningún check evaluable (todo PENDING/N/A); revisar fusión de entradas.
- Dictamen NEGATIVO inesperado → listar FAIL Críticos (`fails_criticos` en `score.json`).
- Discrepancia lab vs field en CWV → manda field (CrUX/RUM p75); documentar ambas.

## Tras cualquier cambio

`python3 core/utils/selftest.py` (exit 0/1) y `pytest tests/` (ver `tests/`).
