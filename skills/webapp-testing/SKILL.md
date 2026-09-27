---
name: webapp-testing
description: >-
  Pruebas de aplicaciones web locales con Playwright: flujos UI, capturas y depuración de
  comportamiento. Usar ante tests E2E, verificar UI en el navegador o capturar regresiones
  visuales. No usar para auditoría SEO/a11y de un sitio público (→ web-compliance).
license: MIT
metadata:
  author: Soluciones-Alexendros
  version: "0.2.1"
  dominio: web
  idioma: es

---

# Pruebas de aplicaciones web (Playwright)

## Propósito

Verificar flujos UI en apps locales con Playwright: navegación, formularios, estados y capturas. Preferir scripts invocables del proyecto auditado antes de ingerir código largo en el contexto (esta skill no tiene `scripts/` propios; ver Herramientas).

## Cuándo usar

- Tests E2E o comprobación manual asistida de una app en `localhost`.
- Depurar comportamiento de UI tras un cambio.
- Capturar regresiones visuales o de flujo.

No usar para auditoría SEO/a11y de un sitio público (→ `web-compliance`).

## Enfoque

1. Confirmar que el servidor de desarrollo está arriba (o arrancarlo con el helper del proyecto).
2. Si existe un helper del proyecto auditado _(ejemplo: `scripts/with_server.py` del proyecto, no de esta skill)_ u otro helper, ejecutar `--help` primero y usarlo como caja negra.
3. Escribir un script Playwright corto (Chromium headless) que:
   - abra la URL local,
   - espere `networkidle` o el selector estable,
   - ejercite el flujo,
   - falle con mensaje claro.
4. No leer el fuente completo de helpers grandes salvo que `--help` no baste.

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

## Recursos

Esta skill no incluye `scripts/` propios; para helpers invocables ver `web-playwright`. Documentación Playwright oficial _(externo)_ para APIs nuevas.

## Uso

Tests E2E o comprobación asistida de una app en `localhost` _(ejemplo: URL local)_; depurar UI tras un cambio; capturar regresiones visuales. No usar para auditoría SEO/a11y de un sitio público (ver `web-compliance`). Ver frontmatter `description`.

## Estructura

- `SKILL.md` — enfoque y ejemplo mínimo.
- `references/playwright-config.md` — `playwright.config.ts` mínimo para testing local.
- `references/test-patterns.md` — page objects, fixtures y mocking de API.
- Ejemplo mínimo Playwright en este fichero (URL local _(ejemplo)_).

## Herramientas

Sin `scripts/` propios (corregido a la realidad: no existe `scripts/` en esta skill; las menciones a `scripts/` se refieren al proyecto auditado o a `web-playwright`).

| Recurso | Propósito |
|---|---|
| `web-playwright` (skills/scripts) | Helpers invocables E2E (discovery, measure, scoring, report) |
| Documentación Playwright oficial _(externo)_ | APIs nuevas |

## Referencias

- Enfoque y ejemplo mínimo en este `SKILL.md`.
- Productos distintos: `web-playwright` (auditoría E2E con evidencias y RICE), `web-compliance` (auditoría SEO/a11y de sitio público).
