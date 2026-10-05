# Ejemplos Ratelimit (ES)

> Ejemplos mínimos del modo `ratelimit`. Requiere Redis (dependencia dura).
> Detalle en `references/ratelimit.md`.

## Sliding window en API

```typescript
import { Ratelimit } from "@upstash/ratelimit";
import { Redis } from "@upstash/redis";

const ratelimit = new Ratelimit({
  redis: Redis.fromEnv(), // dependencia dura
  limiter: Ratelimit.slidingWindow(10, "10 s"),
});

const { success, reset } = await ratelimit.limit(`api:${userId}`);
if (!success) {
  return Response.json(
    { error: "límite excedido" },
    {
      status: 429,
      headers: {
        "Retry-After": String(Math.ceil((reset - Date.now()) / 1000)),
      },
    }
  );
}
```

## Token bucket para trabajos pesados

```typescript
const pesado = new Ratelimit({
  redis: Redis.fromEnv(),
  limiter: Ratelimit.tokenBucket(5, "1 h", 10),
});
```
