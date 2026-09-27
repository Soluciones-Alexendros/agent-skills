---
name: construir-upstash
description: >-
  Router del ecosistema Upstash (Redis, Vector/RAG, Search, QStash/Workflows, Ratelimit,
  Blob, Box) con 7 modos internos. Usar ante Upstash, Redis serverless, embeddings/RAG
  gestionados, colas QStash o rate limiting. No cubre Postgres.
license: MIT
metadata:
  author: Soluciones-Alexendros
  version: "1.0.1"
  dominio: construir
  idioma: es
---
# construir-upstash — Router con 7 modos internos

Punto de entrada unificado al ecosistema Upstash. Esta skill actúa como **router
automático**: detecta la intención y dirige a uno de los 7 modos internos en `modes/`.
Los modos **no son skills separadas**: son recursos internos de esta skill, cada uno con
su `MODE.md`, sus `references/` propias y sus `ejemplos.md`.

## Routing automático (palabras clave → modo)

| Palabras clave detectadas | Modo | Entrada |
|---|---|---|
| cache, session, KV, leaderboard, sorted set, Lua, pipeline, MULTI/EXEC, réplica, `start-redis`, Scratch | `redis` | `modes/redis/MODE.md` |
| embedding, RAG, vector, similarity, kNN, namespace, dense, sparse, semantic cache | `vector` | `modes/vector/MODE.md` |
| full-text, búsqueda, typo-tolerance, facetas, rerank, filtro SQL, paginación | `search` | `modes/search/MODE.md` |
| queue, cola, cron, mensaje, background job, DLQ, retry, fan-out, deduplicación, firma webhook | `queue` | `modes/queue/MODE.md` |
| workflow, durable, step, sleep, call, human-in-the-loop, agente con pasos | `queue` (workflows extiende queue) | `modes/queue/MODE.md` |
| rate limit, throttle, 429, token bucket, ventana fija/deslizante, multi-region | `ratelimit` | `modes/ratelimit/MODE.md` |
| S3, blob, upload, presigned URL, multipart, subida directa desde navegador | `blob` | `modes/blob/MODE.md` |
| container, sandbox, agente IA, browser headless, snapshot, workspace remoto | `box` | `modes/box/MODE.md` |
| CLI, terminal, backup, automatización, `upstash` command | transversal | `references/cli.md`, `references/cli-vendor.md` |

## Dependencias entre modos (declarativo)

- **Workflows extiende queue**: los workflows duraderos corren sobre QStash; todo el
  material de workflows vive en `modes/queue/` (`workflow.md`, `workflow-overview.md`,
  `basics/*`, `features/*`, `how-to/*`). No hay modo `workflow` separado.
- **Ratelimit requiere Redis (dependencia dura)**: `@upstash/ratelimit` exige un cliente
  `@upstash/redis` como backend (`new Ratelimit({ redis, limiter })`). Sin Redis no hay
  ratelimit; ver `modes/ratelimit/MODE.md` y `core/clientes.md`.

## Núcleo compartido (`core/`)

Helpers comunes a todos los modos, extraídos de las referencias para no duplicar:

- `core/config.md` — variables de entorno `UPSTASH_*` y factoría `fromEnv()` por SDK.
- `core/clientes.md` — factoría de clientes (Redis, Vector, Search, QStash, Blob, Box)
  para Node, Edge, Vercel, Cloudflare Workers y Deno.
- `core/errores.md` — errores compartidos, reintentos, backoff y DLQ.

## Estructura

- `SKILL.md` — este router: triggering por palabras clave y tabla de routing.
- `core/` — configuración, factoría de clientes y errores compartidos (recurso interno).
- `modes/<modo>/` — 7 modos internos; cada uno: `MODE.md` (guía ES del modo),
  `references/` (lectura progresiva, plana) y `ejemplos.md` (ejemplos mínimos ES).
  - `redis`: cache, sessions, KV, leaderboards. → `modes/redis/MODE.md`
  - `vector`: embeddings, RAG, semantic cache. → `modes/vector/MODE.md`
  - `search`: full-text, typo-tolerance, facetas. → `modes/search/MODE.md`
  - `queue`: QStash (colas, cron) + workflows + consumer groups. → `modes/queue/MODE.md`
  - `ratelimit`: algoritmos sobre Redis. → `modes/ratelimit/MODE.md`
  - `blob`: S3-compatible. → `modes/blob/MODE.md`
  - `box`: sandboxed containers. → `modes/box/MODE.md`
- `references/` — índice y transversales (lectura progresiva, plana):
  `references/index.md` (índice de modos), `references/comparativa-busqueda.md`
  (Redis Search vs Search SDK vs Vector Hybrid: cuándo usar cada uno),
  `references/cli.md` y `references/cli-vendor.md` (CLI, sin modo propio).
- Sin `scripts/`: skill de routing documental. El único script heredado vive en
  `modes/queue/examples/verify-multi-region-setup.ts`.

## Referencias

- Índice: `references/index.md`.
- Comparativa de búsqueda: `references/comparativa-busqueda.md`.
- CLI: `references/cli.md`, `references/cli-vendor.md`.
- Modos: `modes/<modo>/MODE.md` (ver tabla de routing).

## Notas

- **MCP Server**: si hay herramientas MCP de Upstash en la sesión, preferirlas para
  operaciones de cuenta/datos (crear DBs, índices, stats, logs, DLQ). Los modos son
  para **código de aplicación**.
- **Scratch Redis**: Redis temporal sin credenciales (3 días) en
  `modes/redis/references/scratch-redis.md`.
- **SDKs**: JS/TS (Node, Edge, Vercel, Cloudflare, Deno); Box también en Python
  (`modes/box/references/box-py-overview.md`).

## Uso

Detectar la intención (tabla «Routing automático»), cargar `core/config.md` si hacen
falta credenciales, y luego solo el `modes/<modo>/MODE.md` correspondiente más las
`references/` que indique. Para operaciones de cuenta preferir MCP si está disponible.
