# Refs modo local

## `playwright.config.ts` mínimo para testing local

```ts
import { defineConfig } from "@playwright/test";

export default defineConfig({
  testDir: "./tests",
  use: { baseURL: "http://localhost:5173", trace: "on-first-retry" },
  webServer: { command: "npm run dev", url: "http://localhost:5173", reuseExistingServer: true },
});
```

## Patrones de test

- **Page objects**: una clase por vista (LoginPage, CheckoutPage); selectores por rol
  (`getByRole`), nunca XPath absoluto; 2 alternativas si falla (self-healing manual).
- **Fixtures**: `storageState` por persona (nuevo/logueado/mobile); datos faker para altas.
- **Mocking de API**: `page.route()` para bordes (500, latencia, vacío); el resto contra API real local.
- **Aserciones**: estados visibles + URL + sin `pageerrors`; captura solo al fallar.

## Helpers invocables del core

- `core/utils/discovery.py --root-dir <build-estático> --out site-map.json` (offline).
- `core/utils/measure_analyze.py` sobre mediciones de `modes/e2e/assets/measure.js`.
- `core/utils/validate_compliance.py` + `modes/e2e/run.py --compliance …` para cerrar.
