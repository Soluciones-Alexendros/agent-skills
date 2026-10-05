# Ejemplos Redis (ES)

> Ejemplos mínimos del modo `redis`. Detalle en `references/redis.md`.

## Cache con TTL

```typescript
import { Redis } from "@upstash/redis";
const redis = Redis.fromEnv();

await redis.set("usuario:42", JSON.stringify({ nombre: "Ana" }), { ex: 3600 });
const cached = await redis.get("usuario:42");
```

## Sesión

```typescript
const sid = crypto.randomUUID();
await redis.hset(`sesion:${sid}`, { userId: "42", rol: "admin" });
await redis.expire(`sesion:${sid}`, 1800);
```

## Leaderboard

```typescript
await redis.zadd("ranking", { score: 1500, member: "jugador:7" });
const top = await redis.zrange("ranking", 0, 9, {
  rev: true,
  withScores: true,
});
```

## Lock distribuido

```typescript
const lock = await redis.set("lock:pedido:9", "worker-1", { nx: true, ex: 30 });
if (!lock) throw new Error("recurso ocupado");
try {
  // ... sección crítica ...
} finally {
  await redis.del("lock:pedido:9");
}
```
