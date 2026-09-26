# Troubleshooting — problemas conocidos y resolución

Diagnóstico rápido: `python3 scripts/selftest.py` (exit 0 = todo OK). Incidencias detectadas durante el desarrollo y guía de fallos en ejecución.

## Incidencias resueltas en desarrollo (v2.1)

1. **WCAG 2.5.5 vs 2.5.8 en touch targets.** El material original fijaba FAIL crítico a <44px citando WCAG 2.5.5 (que es nivel AAA). El criterio AA real de WCAG 2.2 es 2.5.8 (24px). Resolución: `measure_analyze.py` emite **FAIL Crítica solo bajo 24px** y WARN Alta entre 24–44px; el objetivo de diseño sigue siendo 44px.
2. **Clicks destructivos en la versión original.** `auditor.agent.ts` v2.0 hacía `click()` real sobre todos los botones, incluidos posibles "logout" o submits con efectos. Resolución: v2.1 usa `click({trial: true})` (verifica accionabilidad sin ejecutar) y la pasada C de formularios queda limitada a staging o marcada PENDING (ver playbook FASE 0.5).
3. **Validación de schema sin dependencias.** `jsonschema` no es stdlib; `validate_compliance.py` implementa la validación necesaria (required, enums, URI, tipos) en stdlib puro y añade la regla de negocio "FAIL exige evidencia".
4. **Paginación infinita.** El crawler corta `?page=N` a N≤5 y descarta valores no numéricos; cubierto por test con fixture paginado hasta page=7.
5. **Crawler offline bloqueado por su propio filtro de esquema.** En modo `--root-dir` las URLs internas usan esquema `local://`, que `is_trap` rechazaba por no ser http/https, dejando el mapa vacío (0 páginas). Detectado por el test de minisite y resuelto admitiendo `local` como esquema interno.
6. **Fixture de compliance con veredicto incoherente.** El fixture válido de muestra tenía 2 PASS/1 FAIL (67% global ⇒ NO APTO) pero el test esperaba APTO/observaciones. Resuelto añadiendo un PASS (75% ⇒ APTO CON OBSERVACIONES). Lección: los fixtures deben calcularse contra las reglas de `thresholds.json`, no asumirse.

## Fallos de ejecución habituales

| Síntoma | Causa probable | Resolución |
|---|---|---|
| `discovery.py` exit 2 | URL raíz inalcanzable / DNS / WAF | Verificar URL; si hay WAF, ejecutar desde red permitida o usar `--root-dir` con volcado estático |
| `discovery.py` encuentra 1 sola página | Sitio SPA con enlaces renderizados por JS | El crawler HTTP no ejecuta JS: complementar con navegador (Playwright) o sitemap.xml |
| `measure_analyze.py` sin checks | El JSON no tiene `elements` | Regenerar mediciones con `assets/measure.js` vía `page.evaluate` |
| UI-03 WARN masivo | Componentes con dimensiones fraccionarias (subpixel) | Es esperado en layouts fluidos; revisar solo si off-grid >80% |
| `validate_compliance.py` exit 1 "FAIL sin evidencia" | Hallazgo reportado sin locator/screenshot/console | Regla de oro: todo FAIL lleva evidencia; si no es verificable, usar N/A o PENDING |
| `score.py` veredicto "SIN DATOS" | compliance.json vacío o todo N/A | Ejecutar primero discovery + motores de checks |
| Playwright: `net::ERR_CERT` en staging | Certificado autofirmado | `launch({ ignoreHTTPSErrors: true })` solo en staging, nunca en producción |
| `networkidle` nunca se alcanza | Polling/websockets permanentes | Cambiar a `waitUntil: 'domcontentloaded'` + espera explícita de selector clave |
| axe-core no instalado | Falta `npm i -D @axe-core/playwright` | Instalar en el proyecto de tests; los scripts Python no lo requieren |
| Screenshots con banner de cookies | CMP interfiere en la medición | Aceptar/rechazar cookies en FASE 0 por persona y guardar storageState |

## Convenciones de los scripts

- Stdlib puro (Python ≥3.9), códigos de salida: 0 OK, 1 validación fallida, 2 error de entrada/red.
- Ningún script aborta por una URL rota: registra `status` y sigue el crawl.
- Los IDs de checks emitidos por scripts (UI-xx) coinciden con el registry de `configs/checks.json`.
