# Índice de modos Upstash (ES)

> Recurso de la skill `construir-upstash`. Los 7 modos son internos (no skills separadas).

## Modos

| Modo | Entrada | Cubre |
|---|---|---|
| `redis` | `../modes/redis/MODE.md` | cache, sessions, KV, leaderboards, Lua, pipelines, réplicas, Redis Search, Scratch |
| `vector` | `../modes/vector/MODE.md` | embeddings, RAG, similarity, namespaces, semantic cache |
| `search` | `../modes/search/MODE.md` | full-text, typo-tolerance, facetas, reranking |
| `queue` | `../modes/queue/MODE.md` | QStash (colas, cron, DLQ) + workflows duraderos (extiende queue) |
| `ratelimit` | `../modes/ratelimit/MODE.md` | rate limiting (requiere Redis) |
| `blob` | `../modes/blob/MODE.md` | almacenamiento S3-compatible |
| `box` | `../modes/box/MODE.md` | contenedores sandbox (JS/Python/CLI) |

## Núcleo compartido

- `../core/config.md` — variables `UPSTASH_*` y `fromEnv()`.
- `../core/clientes.md` — factoría de clientes por runtime.
- `../core/errores.md` — errores, reintentos y DLQ.

## Transversales

- `comparativa-busqueda.md` — Redis Search vs Search SDK vs Vector Hybrid.
- `cli.md`, `cli-vendor.md` — CLI de Upstash (sin modo propio).
