---
name: upstash
description: >-
  Router del ecosistema Upstash: Redis serverless, Vector/RAG, Search, QStash, workflows,
  ratelimit, Blob y Box. Usar ante Upstash, Redis serverless, embeddings/RAG gestionados o
  colas QStash. No usar para Postgres (→ datos-postgres).
license: MIT
metadata:
  author: Soluciones-Alexendros
  version: "0.2.0"
  dominio: datos
  idioma: es

---
# Upstash — Router de Namespace

Punto de entrada unificado para todo el ecosistema Upstash. Esta skill actúa como **router automático**: detecta la intención del usuario y dirige al submódulo correspondiente en `references/`.

## Qué hace / Propósito

Es el router namespace del ecosistema Upstash: punto de entrada unificado que detecta la intención del usuario y enruta automáticamente al submódulo correspondiente en `references/`. Cubre Redis, Vector, Search, QStash, Workflows, Ratelimit, Blob, Box y CLI para capacidades serverless/edge en Node.js, Next.js, Vercel, Cloudflare Workers y Deno.

## Cuándo usarme / Triggering

- **Mención genérica**: "Upstash", "ecosistema Upstash", "serverless Redis/Vector/Search"
- **Redis**: "cache serverless", "sessions Upstash", "KV store", "leaderboards", "Lua scripting", "pipelines"
- **Vector**: "embeddings", "RAG", "semantic search", "vector database", "similarity search", "namespaces"
- **Search**: "full-text search", "semantic search", "reranking", "site search", "product search"
- **QStash/Colas**: "message queue", "cron jobs", "background jobs", "workflows", "DLQ", "retries"
- **Workflows**: "durable workflows", "step functions", "long-running tasks", "sleep minutes/days"
- **Ratelimit**: "rate limiting", "throttling", "429 Too Many Requests", "fixed/sliding/token bucket"
- **Blob**: "S3-compatible", "browser uploads", "presigned URLs", "multipart upload"
- **Box**: "sandboxed containers", "AI agents in containers", "browser automation", "remote workspace"
- **CLI**: "upstash CLI", "gestión bases de datos", "crear índices", "automatización terminal"

## Referencias Internas (Submódulos)

- `references/redis.md` — **Redis serverless**: cache, sessions, KV, leaderboards, Lua, pipelines, MULTI/EXEC, read replicas, Redis Search. Skill independiente aspiracional: `datos-redis` (no existe en este repo; contenido completo aquí)
- `references/vector.md` — **Vector DB**: embeddings, RAG, similarity search, namespaces, dense/sparse/hybrid indexes. Skill independiente aspiracional: `datos-vectorial` (no existe en este repo; contenido completo aquí + `references/search.md`)
- `references/search.md` — **Search**: full-text, semantic, hybrid, reranking, SQL-like filters, paginación
- `references/queues.md` — **QStash**: message queue, cron, FIFO, DLQ, retries, deduplicación, fan-out, webhook signatures
- `references/workflow.md` — **Workflows**: durable execution, steps, sleep, call, retries, DLQ, concurrency, human-in-the-loop
- `references/ratelimit.md` — **Ratelimit**: fixed window, sliding window, token bucket, multi-region, deny lists, analytics
- `references/blob.md` — **Blob**: S3-compatible, direct browser uploads, presigned URLs, multipart, signed reads, cache headers
- `references/box.md` — **Box**: sandboxed containers, AI agents, shell, filesystem, git, cron, snapshots, headless browser (JS/Python/CLI)
- `references/cli.md` — **CLI**: `upstash` command, databases, indexes, teams, backups, Redis exec, usage stats

## Routing Automático (Lógica del Agente)

| Palabras clave detectadas | Submódulo referenciado | Skill independiente si aplica |
|---------------------------|------------------------|------------------------------|
| cache, session, KV, leaderboard, Lua, pipeline, MULTI, sorted set | `references/redis.md` | `datos-redis` (aspiracional) |
| embedding, RAG, vector, similarity, kNN, namespace, dense, sparse | `references/vector.md` | `datos-vectorial` (aspiracional) |
| full-text, semantic, rerank, filter SQL, paginación | `references/search.md` | — |
| queue, cron, message, background job, DLQ, retry, fan-out | `references/queues.md` | — |
| workflow, durable, step, sleep, call, human-in-the-loop | `references/workflow.md` | — |
| rate limit, throttle, 429, token bucket, multi-region | `references/ratelimit.md` | — |
| S3, blob, upload, presigned, multipart, browser direct | `references/blob.md` | — |
| container, sandbox, AI agent, browser, snapshot, remote workspace | `references/box.md` | `entorno-aislado` (aspiracional) |
| CLI, terminal, automatización, backup, redis exec | `references/cli.md` | `cli-upstash` (aspiracional) |

## Skills Independientes Derivadas

Para uso directo cuando el usuario pide específicamente:

1. **`datos-redis`** (aspiracional, no existe en este repo) — Redis serverless completo (cache, sessions, KV, leaderboards, Lua, pipelines). Contenido completo en `references/redis.md`
2. **`datos-vectorial`** (aspiracional, no existe en este repo) — Vector DB completo (embeddings, RAG, semantic search, namespaces). Contenido en `references/vector.md` + `references/search.md`
3. **`entorno-aislado`** (aspiracional, no existe en este repo) — Box containers (JS/Python/CLI). Contenido en `references/box.md`
4. **`cli-upstash`** (aspiracional, no existe en este repo) — Upstash CLI. Contenido en `references/cli.md`

## Notas Importantes

- **MCP Server**: Si Upstash MCP tools están disponibles en la sesión, preferirlos para operaciones de cuenta/datos (crear DBs, índices, stats, logs, DLQ). Estas skills son para **código de aplicación**.
- **Scratch Redis**: Para Redis temporal sin credenciales → sección "Scratch Redis" en `references/redis.md` (antes `upstash-redis-start`)
- **SDKs**: Referencias cubren JS/TS (Node, Edge, Vercel, Cloudflare, Deno). Python para Box.

---

*Esta skill implementa el patrón **namespace router** de OpenAI Agents SDK: <10 funciones por namespace, routing semántico automático.*

## Nota de fusión

Los submódulos Redis y Vector viven en `references/redis.md` y `references/vector.md` de esta misma skill. No existen skills independientes con esos nombres en este repositorio.

## Uso

Router Upstash: detectar la intención (tabla «Routing Automático») y cargar solo el submódulo `references/*.md` correspondiente. Para operaciones de cuenta/datos preferir Upstash MCP tools si están disponibles; estas referencias son para código de aplicación.

## Estructura

- `SKILL.md` — router, triggering por submódulo y tabla de routing.
- `references/` — 9 submódulos: redis, vector, search, queues, workflow, ratelimit, blob, box, cli.
- `upstash-*/` — 12 extras de docs de SDKs (redis-js, vector-js, search-js, qstash-js, workflow-js, ratelimit-js, blob-js, box-js, box-py, box-cli, cli, redis-start); no referenciados desde este SKILL.md salvo `upstash-redis-start` (ver «Notas Importantes»).
- Sin `scripts/`: skill puramente de routing documental.

## Referencias

- Internas: ver «Referencias Internas (Submódulos)» más arriba (las 9 existen).
- Ninguna skill `datos-redis`, `datos-vectorial`, `entorno-aislado` ni `cli-upstash` existe en este repo: son nombres aspiracionales.
