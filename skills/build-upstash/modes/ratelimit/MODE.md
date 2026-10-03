# Modo Ratelimit (ES)

> Modo interno de la skill `construir-upstash` (no es skill separada). Router: `construir-upstash` → este modo
> ante rate limit, throttle, 429, token bucket o ventanas fija/deslizante.

## Cubre

Rate limiting con `@upstash/ratelimit`: fixed window, sliding window, token bucket,
multi-region, listas de denegación, analytics, métodos de inicio y precios.

## Dependencia dura

**Requiere Redis**: el limitador exige un cliente `@upstash/redis` como backend
(`new Ratelimit({ redis, limiter })`). Crear primero el cliente del modo `redis`
(`../redis/MODE.md`, `../../core/clientes.md`).

## Referencias propias

Guía principal (ES): `references/ratelimit.md`.

| Fichero | Contenido |
|---|---|
| `references/ratelimit.md` | guía principal ES |
| `references/overview.md` | inicio rápido del SDK |
| `references/algorithms.md` | algoritmos (fixed/sliding/token bucket) |
| `references/features.md` | capacidades |
| `references/methods-getting-started.md` | métodos y puesta en marcha |
| `references/traffic-protection.md` | protección de tráfico, deny lists, analytics |
| `references/pricing-cost.md` | precios y coste |

## Ejemplos

Ver `ejemplos.md` (sliding window en API, respuesta 429 con `Retry-After`).

## Errores

Responder `429` ante `success=false`; ver `../../core/errores.md`.
