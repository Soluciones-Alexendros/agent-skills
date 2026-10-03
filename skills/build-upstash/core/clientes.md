# Factoría de clientes Upstash (ES)

> Recurso interno de la skill `construir-upstash`. Creación de clientes por servicio y runtime. Detalle de credenciales en `config.md`.

## Node.js / Edge / Vercel (`@upstash/*`)

```typescript
import { Redis } from "@upstash/redis";
import { Index } from "@upstash/vector";
import { Search } from "@upstash/search";
import { Client as QStash } from "@upstash/qstash";
import { Ratelimit } from "@upstash/ratelimit";
import { Bucket } from "@upstash/blob";
import { Box } from "@upstash/box";

export const redis = Redis.fromEnv(); // REST, sin conexión persistente
export const vector = Index.fromEnv();
export const search = Search.fromEnv();
export const qstash = QStash.fromEnv();
export const bucket = Bucket.fromEnv();

// Ratelimit: dependencia dura de Redis (ver ../modes/ratelimit/MODE.md)
export const ratelimit = new Ratelimit({
  redis,
  limiter: Ratelimit.slidingWindow(10, "10 s"),
});
```

## Cloudflare Workers / Deno

Los mismos paquetes funcionan sin `fromEnv()` si el runtime no expone `process.env`:

```typescript
import { Redis } from "@upstash/redis";

export const redis = new Redis({
  url: (globalThis as any).UPSTASH_REDIS_REST_URL,
  token: (globalThis as any).UPSTASH_REDIS_REST_TOKEN,
});
```

## Python (solo Box)

```bash
pip install upstash-box
```

```python
from upstash_box import Box

box = Box(api_key="...")  # snake_case; espejo del SDK JS
```

Ver `../modes/box/MODE.md` para el mapeo JS ↔ Python.

## Cliente TCP clásico (migraciones)

Para `node-redis` / `ioredis` contra Upstash con TLS, ver
`../modes/redis/references/from-ioredis.md`,
`../modes/redis/references/from-redis-node.md` y `../modes/redis/references/search-adapters.md`.
