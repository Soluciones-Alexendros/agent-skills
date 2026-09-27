# Modo local — app en localhost (fusión `webapp-testing`)

Verifica flujos UI de una app local con Playwright: navegación, formularios,
estados y capturas. Sin `scripts/` propios de test: scripts ad-hoc cortos
(Chromium headless) + helpers del proyecto auditado.

## Flujo

1. Confirmar servidor dev arriba (o arrancarlo con el helper del proyecto;
   ejecutar `--help` del helper primero y usarlo como caja negra).
2. Escribir script Playwright corto: abrir URL local → esperar `networkidle` o
   selector estable → ejercitar flujo → fallar con mensaje claro.
3. Capturar regresiones visuales/flujo (screenshots, traces).
4. Si el flujo valida OK, registrar checks FN/FM/UI del registry como PASS con
   evidencia (script + captura); puntuar con `run.py --checks …`.

## Ejemplo mínimo

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("http://localhost:5173")  # _(ejemplo: URL local)_
    page.wait_for_load_state("networkidle")
    # ... aserciones del flujo
    browser.close()
```

## No usar para

Auditoría SEO/a11y de sitio público → modo `compliance`. QA E2E completo remoto → modo `e2e`.

## Refs específicas

Ver `refs.md` (config mínima, page objects, fixtures, mocking, helpers invocables).
