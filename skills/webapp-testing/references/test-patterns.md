# Playwright — patrones de prueba comunes

Patrones reutilizables para pruebas E2E de aplicaciones web locales.

## Page Objects

Encapsular selectores y acciones de una página en una clase; el test habla de
intenciones, no de selectores.

```python
class LoginPage:
    def __init__(self, page):
        self.page = page

    def goto(self):
        self.page.goto("/login")

    def login(self, user, password):
        self.page.fill("[data-testid=username]", user)
        self.page.fill("[data-testid=password]", password)
        self.page.click("[data-testid=submit]")
        self.page.wait_for_url("/dashboard")
```

Beneficios: si cambia un selector, se actualiza un solo lugar; los tests se leen como
el flujo de negocio.

## Fixtures

Estado compartido por fixture en vez de setup manual en cada test.

```python
# conftest.py
import pytest
from playwright.sync_api import sync_playwright

@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        yield p.chromium.launch(headless=True)

@pytest.fixture()
def page(browser):
    pg = browser.new_page()
    yield pg
    pg.close()
```

Regla: scope `session` para el navegador (coste de arranque), scope `function` para la
 página (aislamiento entre tests).

## Mocking de API

Interceptar peticiones de red para tests deterministas, sin backend real.

```python
def test_pago_sin_backend(page):
    page.route("**/api/pay", lambda route: route.fulfill(
        status=200,
        content_type="application/json",
        body='{"status": "ok"}',
    ))
    page.goto("/checkout")
    page.click("[data-testid=pay]")
    expect(page.locator("[data-testid=receipt]")).to_be_visible()
```

- `page.route("**/api/**")` — patrón glob sobre la URL.
- `route.fulfill(...)` — respuesta simulada con status, headers y body.
- `page.waitForResponse("**/api/pay")` — aserción de que la llamada ocurrió.

## Patrones adicionales

| Patrón | Cuándo usarlo |
|---|---|
| `expect(locator).to_be_visible()` | Aserciones auto-reintentan; mejor que asserts instantáneos. |
| `page.wait_for_load_state("networkidle")` | Esperar a que la app local estabilice su carga. |
| `data-testid` | Selectores estables que no se rompen con cambios de CSS. |
| `test.describe("flujo login")` | Agrupar tests por flujo en el informe. |

## Anti-patrones

- Tiempos fijos (`time.sleep`) — sustituir por esperas de estado/selector.
- Selectores por texto frágil — preferir `data-testid` o roles ARIA (`getByRole`).
- Depender de datos remotos — mockear la API y semillar estado propio en la BD local.
