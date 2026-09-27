# Configuración común Upstash (ES)

> Recurso interno de la skill `construir-upstash`. Variables de entorno y patrón `fromEnv()` compartidos por los 7 modos.

## Variables de entorno por servicio

```bash
# Redis (modos redis, ratelimit)
UPSTASH_REDIS_REST_URL=https://xxx.upstash.io
UPSTASH_REDIS_REST_TOKEN=xxx

# Vector (modo vector)
UPSTASH_VECTOR_REST_URL=https://xxx.upstash.io
UPSTASH_VECTOR_REST_TOKEN=xxx

# Search (modo search)
UPSTASH_SEARCH_REST_URL=https://xxx.upstash.io
UPSTASH_SEARCH_REST_TOKEN=xxx

# QStash / Workflows (modo queue)
QSTASH_TOKEN=xxx
QSTASH_CURRENT_SIGNING_KEY=xxx
QSTASH_NEXT_SIGNING_KEY=xxx

# Blob (modo blob)
UPSTASH_BLOB_TOKEN=xxx

# Box (modo box)
UPSTASH_BOX_API_KEY=xxx
```

## Patrón `fromEnv()`

Todos los SDK JS/TS leen las variables anteriores sin argumentos explícitos:

```typescript
import { Redis } from "@upstash/redis";
import { Index } from "@upstash/vector";
import { Search } from "@upstash/search";
import { Client as QStash } from "@upstash/qstash";
import { Bucket } from "@upstash/blob";

const redis = Redis.fromEnv();
const index = Index.fromEnv();
const search = Search.fromEnv();
const qstash = new QStash({ token: process.env.QSTASH_TOKEN! });
const bucket = Bucket.fromEnv();
```

Reglas:

- Nunca commitear tokens; solo variables de entorno o secretos del proveedor (Vercel, Cloudflare, Deno Deploy).
- El token de Blob es bearer del bucket completo: solo en servidor, jamás en `NEXT_PUBLIC_*`.
- Scratch Redis (temporal, 3 días, sin cuenta) en `../modes/redis/references/scratch-redis.md`.
