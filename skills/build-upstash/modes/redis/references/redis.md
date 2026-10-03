# Redis Serverless (Upstash) — Referencia Completa

> **Modo interno de `construir-upstash`** (`modes/redis/MODE.md`) — referencia completa de nivel standalone.

---

## Instalación y Configuración

```bash
npm install @upstash/redis
```

```typescript
import { Redis } from "@upstash/redis";

// Inicialización explícita
const redis = new Redis({
  url: "UPSTASH_REDIS_REST_URL",
  token: "UPSTASH_REDIS_REST_TOKEN",
});

// O desde variables de entorno
const redis = Redis.fromEnv();
```

**Variables de entorno:**
```bash
UPSTASH_REDIS_REST_URL=https://your-redis.upstash.io
UPSTASH_REDIS_REST_TOKEN=your-token-here
```

> **Sin credenciales?** Scratch Redis temporal: `POST https://upstash.com/start-redis` (3 días, no signup). Ver sección "Scratch Redis" abajo.

---

## Estructuras de Datos (Auto-Serialización)

| Tipo | Comandos Principales | Caso de Uso |
|------|---------------------|-------------|
| **Strings** | `get`, `set`, `incr`, `decr`, `append`, `mget`, `mset` | Valores simples, contadores, cache |
| **Hashes** | `hset`, `hget`, `hmget`, `hgetall`, `hdel` | Objetos, perfiles usuario, configs |
| **Lists** | `lpush`, `rpush`, `lpop`, `rpop`, `lrange`, `llen` | Colas, historial, logs recientes |
| **Sets** | `sadd`, `smembers`, `sismember`, `srem`, `sunion` | Tags, únicos, pertenencia |
| **Sorted Sets** | `zadd`, `zrange`, `zrank`, `zscore`, `zrem` | **Leaderboards**, rankings, rate limiting |
| **JSON** | `json.set`, `json.get`, `json.del`, `json.arrpush` | Documentos anidados, paths JSONPath |
| **Streams** | `xadd`, `xread`, `xrange`, `xgroup`, `xack` | Consumer groups, event sourcing |

**Auto-serialización:** Pasar tipos nativos JS (number, object, array) — el SDK serializa/deserializa automáticamente.

```typescript
// ✅ CORRECTO - tipos nativos
await redis.set("count", 42);
await redis.set("user", { name: "Alice", roles: ["admin"] });
const user = await redis.get("user"); // { name: "Alice", roles: ["admin"] }

// ❌ INCORRECTO - serialización manual
await redis.set("count", "42");
await redis.set("user", JSON.stringify({ name: "Alice" }));
```

---

## Patrones Comunes

### Cache (Cache-Aside / Write-Through / TTL)

```typescript
// Cache-aside
async function getUser(id: string) {
  const cached = await redis.get(`user:${id}`);
  if (cached) return cached;

  const user = await db.users.find(id);
  await redis.setex(`user:${id}`, 3600, user); // TTL 1h
  return user;
}

// Write-through
async function updateUser(id: string, data: User) {
  await db.users.update(id, data);
  await redis.set(`user:${id}`, data); // Invalidate/update cache
}
```

### Sesiones y Almacén Clave-Valor

```typescript
// Sesión con TTL
await redis.setex(`session:${sessionId}`, 86400, { userId: "123", prefs: {...} });
const session = await redis.get(`session:${sessionId}`);

// KV simple
await redis.set("config:feature-flags", { darkMode: true, beta: false });
const flags = await redis.get("config:feature-flags");
```

### Leaderboards y Rankings (Sorted Sets)

```typescript
// Añadir puntuación
await redis.zadd("leaderboard:global", { score: 1500, member: "player1" });

// Top 10
const top10 = await redis.zrange("leaderboard:global", 0, 9, { rev: true, withScores: true });

// Rank de un jugador
const rank = await redis.zrank("leaderboard:global", "player1"); // 0-indexed
```

### Contadores y Bloques Distribuidos

```typescript
// Contador atómico
const views = await redis.incr("pageviews:home");

// Lock distribuido simple
const lock = await redis.set("lock:resource", "owner", { nx: true, ex: 30 });
if (lock) {
  try { /* critical section */ }
  finally { await redis.del("lock:resource"); }
}
```

### Colas y Streams (Consumer Groups)

```typescript
// Producer
await redis.xadd("events", "*", { type: "user.signup", payload: { email: "a@b.com" } });

// Consumer group
await redis.xgroup("CREATE", "events", "workers", "$", { mkstream: true });
const events = await redis.xreadgroup("GROUP", "workers", "consumer1", "COUNT", 10, "STREAMS", "events", ">");
```

---

## Características Avanzadas

### Pipelines y Transacciones (MULTI/EXEC)

```typescript
// Pipeline automático (batching)
const results = await redis.mget("key1", "key2", "key3"); // Auto-pipelined

// Pipeline manual
const pipeline = redis.pipeline();
pipeline.set("a", 1);
pipeline.set("b", 2);
pipeline.incr("counter");
await pipeline.exec(); // Todas en una request HTTP

// Transacción atómica (MULTI/EXEC)
const multi = redis.multi();
multi.incr("counter");
multi.set("flag", "done");
await multi.exec(); // Todo o nada
```

### Lua Scripting

```typescript
// Script atómico en servidor
const script = `
  local current = redis.call('GET', KEYS[1])
  if current and tonumber(current) >= tonumber(ARGV[1]) then
    return 0
  end
  return redis.call('INCR', KEYS[1])
`;
const result = await redis.eval(script, 1, "rate:limit", "100");
```

### Réplicas de Lectura (Read Replicas)

```typescript
// Configuración global con réplicas
const redis = new Redis({
  url: "UPSTASH_REDIS_REST_URL",
  token: "UPSTASH_REDIS_REST_TOKEN",
  // Réplicas automáticas para read-your-writes consistency
});
```

---

## Redis Search (Extensión Full-Text)

> Diferente de `FT.SEARCH` estándar. También disponible para TCP clients via `@upstash/search-redis` y `@upstash/search-ioredis`.

```typescript
// Crear índice
await redis.ft.create("idx:users", {
  "$.name": { type: "TEXT", weight: 5.0 },
  "$.email": { type: "TEXT" },
  "$.age": { type: "NUMERIC", sortable: true },
  "$.tags": { type: "TAG", separator: "," }
}, { on: "JSON" });

// Buscar
const results = await redis.ft.search("idx:users", "Alice @age:[20 30] @tags:{admin|premium}");

// Agregaciones
const stats = await redis.ft.aggregation("idx:users", "*", {
  load: ["$.age"],
  groupby: ["$.tags"],
  apply: ["avg($.age) as avg_age"]
});
```

---

## Migración desde ioredis / node-redis

| Aspecto | ioredis / node-redis | @upstash/redis |
|---------|---------------------|----------------|
| **Conexión** | TCP persistente | HTTP REST (serverless-friendly) |
| **Pooling** | Requerido | No necesario (stateless) |
| **Serialización** | Manual (strings) | **Automática** (tipos nativos) |
| **Pipelining** | `pipeline()` | Automático + manual |
| **Lua** | `eval` | `eval` / `evalsha` |
| **Pub/Sub** | Sí | No (usar Streams) |
| **Cluster** | Sí | No (sharding automático) |

**Guías detalladas:** `migrations/from-ioredis.md`, `migrations/from-redis-node.md`

---

## Scratch Redis (Sin Credenciales)

Para agentes que necesitan Redis **ya** sin credenciales del usuario:

```bash
# Crear/recuperar DB temporal (3 días TTL)
curl -X POST https://upstash.com/start-redis \
  -H "Content-Type: application/json" \
  -d '{"region": "eu-west-1"}'  # opcional
```

**Respuesta:**
```json
{
  "url": "https://redis-abc123.upstash.io",
  "token": "token-xyz789",
  "region": "eu-west-1",
  "expires_at": "2026-09-17T10:30:00Z"
}
```

- **Idempotente**: misma IP → misma DB (hasta expiración)
- **No para producción**: no PII, no secretos, 3 días máx.
- **Claim**: Usuario puede reclamarla en dashboard Upstash

---

## Mejores Prácticas

1. **Variables de entorno** para credenciales, nunca hardcode
2. **Aprovecha auto-serialización** — pasa tipos nativos JS
3. **TypeScript types** para type safety
4. **TTL apropiados** para gestión de memoria
5. **Pipelines** para operaciones múltiples
6. **Namespacing keys**: `user:123`, `session:abc`, `cache:page:home`
7. **Manejo de errores**: retry con backoff, timeouts, logging

---

## Recursos

- [Documentación Oficial](https://upstash.com/docs/redis)
- [GitHub @upstash/redis](https://github.com/upstash/redis-js)
- [API Reference](https://upstash.com/docs/redis/sdks/ts/overview)
- [Ejemplos](https://github.com/upstash/redis-js/tree/main/examples)