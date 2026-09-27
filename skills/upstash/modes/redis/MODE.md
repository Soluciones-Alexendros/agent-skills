# Modo Redis (ES)

> Modo interno de la skill `upstash` (no es skill separada). Router: `upstash` → este modo
> ante cache, session, KV, leaderboard, Lua, pipeline, MULTI/EXEC o Scratch Redis.

## Cubre

Cache serverless, sessions, KV, leaderboards (sorted sets), locks distribuidos,
streams/consumer groups, pipelines y transacciones, scripting Lua, réplicas de lectura,
serialización, TTL, migraciones desde `ioredis`/`node-redis`, Redis Search sobre Redis
y Scratch Redis temporal.

## Referencias propias

Guía principal (ES): `references/redis.md`.

| Fichero | Contenido |
|---|---|
| `references/redis.md` | guía principal ES: instalación, config, patrones |
| `references/sdk-overview.md` | visión general del SDK `@upstash/redis` |
| `references/caching.md` | patrón cache-aside / write-through, TTL |
| `references/session-management.md` | sesiones |
| `references/leaderboard.md` | leaderboards con sorted sets |
| `references/distributed-locks.md` | locks distribuidos |
| `references/rate-limiting.md` | rate limiting con Redis (ver también modo `ratelimit`) |
| `references/strings.md`, `hashes.md`, `lists.md`, `sets.md`, `sorted-sets.md`, `streams.md`, `json.md` | estructuras de datos |
| `references/auto-pipeline.md`, `references/pipeline-and-transactions.md`, `references/pipeline-optimization.md`, `references/batching-operations.md` | pipelines y batching |
| `references/scripting.md` | Lua scripting |
| `references/redis-replicas.md` | réplicas de lectura |
| `references/data-serialization.md`, `references/error-handling.md`, `references/ttl-expiration.md` | rendimiento y errores |
| `references/from-ioredis.md`, `references/from-redis-node.md` | migraciones |
| `references/search-overview.md`, `references/search-adapters.md`, `references/search-querying.md`, `references/search-aggregating.md`, `references/search-index-management.md`, `references/search-aliases.md` | Redis Search (índices sobre Redis; si dudas entre motores, ver `../../references/comparativa-busqueda.md`) |
| `references/scratch-redis.md` | Scratch Redis temporal sin credenciales (3 días) |

## Ejemplos

Ver `ejemplos.md` (cache, sesión, leaderboard, lock).

## Dependencias

Ninguna. Este modo es backend del modo `ratelimit` (dependencia dura).
Configuración y errores comunes: `../../core/config.md`, `../../core/errores.md`.
