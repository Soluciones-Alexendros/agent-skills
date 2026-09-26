# Playwright — configuración mínima para testing local

Configuración de referencia para probar una app web en `localhost`. Pensada para scripts
invocables del proyecto auditado (Chromium headless).

## `playwright.config.ts` mínimo

```ts
import { defineConfig } from "@playwright/test";

export default defineConfig({
  testDir: "./tests/e2e",
  timeout: 30_000,
  retries: process.env.CI ? 2 : 0,
  use: {
    baseURL: "http://localhost:5173",
    headless: true,
    viewport: { width: 1280, height: 720 },
    screenshot: "only-on-failure",
    trace: "retain-on-failure",
  },
  projects: [
    { name: "chromium", use: { browserName: "chromium" } },
  ],
  webServer: {
    command: "npm run dev",
    url: "http://localhost:5173",
    reuseExistingServer: !process.env.CI,
  },
});
```

## Claves explicadas

| Opción | Por qué |
|---|---|
| `baseURL` | Las pruebas usan rutas relativas (`page.goto("/login")`). |
| `headless: true` | Sin display; el modo headed es solo para depuración manual. |
| `screenshot: "only-on-failure"` | Evita ruido; la evidencia del fallo va al informe. |
| `trace: "retain-on-failure"` | Traza reproducible (red, consola, DOM) solo cuando falla. |
| `webServer` | Playwright arranca el dev server y espera a que responda antes de testear. |
| `reuseExistingServer` | En local reutiliza un server ya arriba; en CI siempre uno limpio. |

## Equivalente en Python

```python
# conftest.py
import pytest
from playwright.sync_api import sync_playwright

@pytest.fixture()
def page():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        pg = browser.new_page(base_url="http://localhost:5173")
        yield pg
        browser.close()
```

## Instalación

```bash
npm init -y
npm install -D @playwright/test
npx playwright install chromium   # solo el navegador necesario
```

## Uso

- `npx playwright test` — ejecuta toda la suite.
- `npx playwright test --ui` — modo interactivo para depurar (no en CI).
- `npx playwright show-report` — informe HTML tras la ejecución.
