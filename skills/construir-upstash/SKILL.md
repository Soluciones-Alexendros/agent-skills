---
name: construir-upstash
description: >-
  Router del ecosistema Upstash (Redis, Vector/RAG, Search, QStash/Workflows,
  Ratelimit, Blob, Box) con 7 modos internos. Usar cuando el operador pida
  Upstash, Redis serverless, embeddings/RAG gestionados, colas QStash o rate
  limiting. No usar para Postgres ni otras bases relacionales.
license: MIT
metadata:
  author: Soluciones-Alexendros
  version: "1.1.1"
  dominio: construir
  tipo: router
  idioma: es
---

# construir-upstash — Router con 7 modos internos

## Propósito

Punto de entrada unificado al ecosistema Upstash. Esta skill actúa como router: detecta la intención y dirige a uno de los 7 modos internos en `modes/`. Los modos no son skills separadas: cada uno tiene `MODE.md`, `references/` planas y `ejemplos.md`.

## Cuándo usar

Peticiones de Upstash, Redis serverless, embeddings/RAG, colas QStash, workflows duraderos, rate limiting, Blob o Box.

## Enrutado

| Palabras clave detectadas                                                                               | Modo                               | Entrada                                         |
| ------------------------------------------------------------------------------------------------------- | ---------------------------------- | ----------------------------------------------- |
| cache, session, KV, leaderboard, sorted set, Lua, pipeline, MULTI/EXEC, réplica, `start-redis`, Scratch | `redis`                            | `modes/redis/MODE.md`                           |
| embedding, RAG, vector, similarity, kNN, namespace, dense, sparse, semantic cache                       | `vector`                           | `modes/vector/MODE.md`                          |
| full-text, búsqueda, typo-tolerance, facetas, rerank, filtro SQL, paginación                            | `search`                           | `modes/search/MODE.md`                          |
| queue, cola, cron, mensaje, background job, DLQ, retry, fan-out, deduplicación, firma webhook           | `queue`                            | `modes/queue/MODE.md`                           |
| workflow, durable, step, sleep, call, human-in-the-loop, agente con pasos                               | `queue` (workflows extiende queue) | `modes/queue/MODE.md`                           |
| rate limit, throttle, 429, token bucket, ventana fija/deslizante, multi-region                          | `ratelimit`                        | `modes/ratelimit/MODE.md`                       |
| S3, blob, upload, presigned URL, multipart, subida directa desde navegador                              | `blob`                             | `modes/blob/MODE.md`                            |
| container, sandbox, agente IA, browser headless, snapshot, workspace remoto                             | `box`                              | `modes/box/MODE.md`                             |
| CLI, terminal, backup, automatización, `upstash` command                                                | transversal                        | `references/cli.md`, `references/cli-vendor.md` |

## Dependencias entre modos

- **Workflows extiende queue**: los workflows duraderos corren sobre QStash; el material vive en `modes/queue/`.
- **Ratelimit requiere Redis**: `@upstash/ratelimit` exige un cliente `@upstash/redis`. Ver `modes/ratelimit/MODE.md` y `core/clientes.md`.

Núcleo compartido: `core/config.md` (env `UPSTASH_*`), `core/clientes.md` (factoría de clientes), `core/errores.md` (reintentos, backoff, DLQ).

Cargar `core/config.md` si hacen falta credenciales y luego solo el `MODE.md` del modo. Si hay MCP de Upstash en la sesión, preferirlo para operaciones de cuenta.

## Referencias

- Índice: `references/index.md`.
- Comparativa de búsqueda: `references/comparativa-busqueda.md`.
- CLI: `references/cli.md`, `references/cli-vendor.md`.
- Modos: `modes/<modo>/MODE.md`.
- Scratch Redis: `modes/redis/references/scratch-redis.md`.
