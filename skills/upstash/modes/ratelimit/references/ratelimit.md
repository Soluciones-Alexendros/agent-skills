# Rate Limiting (Upstash Ratelimit) — Referencia Completa

> **Submódulo de `upstash`** — Modo interno de `upstash` (`modes/ratelimit/MODE.md`)

---

## Instalación

```bash
npm install @upstash/ratelimit @upstash/redis
```

```typescript
import { Ratelimit } from "@upstash/ratelimit";
import { Redis } from "@upstash/redis";

const redis = new Redis({
  url: process.env.UPSTASH_REDIS_REST_URL!,
  token: process.env.UPSTASH_REDIS_REST_TOKEN!,
});

const limiter = new Ratelimit({
  redis,
  limiter: Ratelimit.slidingWindow(10, "10s"), // 10 requests per 10 seconds
  prefix: "ratelimit",        // Key prefix en Redis
  analytics: true,            // Habilitar analytics
});
```

---

## Algoritmos Disponibles

| Algoritmo | Descripción | Caso de Uso |
|-----------|-------------|-------------|
| **Fixed Window** | Ventana fija (reset en frontera) | Simple, bajo overhead, edge cases en fronteras |
| **Sliding Window** | Ventana deslizante suave | **Recomendado general** - suave, sin picos en fronteras |
| **Token Bucket** | Cubo de tokens (burst + rate) | Permite bursts controlados, rate sostenido |

```typescript
// Fixed Window
Ratelimit.fixedWindow(100, "1m")  // 100 req/min

// Sliding Window (recomendado)
Ratelimit.slidingWindow(10, "10s") // 10 req/10s suave

// Token Bucket
Ratelimit.tokenBucket(100, 10, "1s") // 100 tokens, rellena 10/s
```

---

## Uso Básico

```typescript
// En API route / middleware
const { success, limit, remaining, reset, pending } = await limiter.limit("user-123");

if (!success) {
  return new Response("Too Many Requests", {
    status: 429,
    headers: {
      "X-RateLimit-Limit": limit.toString(),
      "X-RateLimit-Remaining": remaining.toString(),
      "X-RateLimit-Reset": reset.toString(),
      "Retry-After": Math.ceil((reset - Date.now()) / 1000).toString()
    }
  });
}

// success = true → continuar
// success = false → throttled (429)
```

---

## Claves de Limitación (Identificadores)

```typescript
// Por usuario autenticado
await limiter.limit(`user:${userId}`);

// Por IP (para endpoints públicos)
await limiter.limit(`ip:${request.headers.get("x-forwarded-for") || "unknown"}`);

// Por API Key
await limiter.limit(`apikey:${apiKey}`);

// Por tenant (multi-tenant SaaS)
await limiter.limit(`tenant:${tenantId}:user:${userId}`);

// Prefijo personalizado (configurado en Ratelimit constructor)
prefix: "api:ratelimit" // → keys: "api:ratelimit:user:123"
```

---

## Protección de Endpoints Críticos

```typescript
// Login / Signup (estricto)
const authLimiter = new Ratelimit({
  redis,
  limiter: Ratelimit.slidingWindow(5, "15m"), // 5 intentos / 15 min
  prefix: "auth:ratelimit"
});

// Form submissions
const formLimiter = new Ratelimit({
  redis,
  limiter: Ratelimit.fixedWindow(10, "1h"),
  prefix: "form:ratelimit"
});

// AI / LLM endpoints (costoso)
const aiLimiter = new Ratelimit({
  redis,
  limiter: Ratelimit.tokenBucket(20, 5, "1m"), // 20 req, burst 5/s
  prefix: "ai:ratelimit"
});

// API pública (generoso)
const publicLimiter = new Ratelimit({
  redis,
  limiter: Ratelimit.slidingWindow(100, "1m"),
  prefix: "public:ratelimit"
});
```

---

## Deny Lists (Listas de Bloqueo)

```typescript
const limiter = new Ratelimit({
  redis,
  limiter: Ratelimit.slidingWindow(100, "1m"),
  prefix: "api:ratelimit",
  // Bloquear IPs/keys específicas
  denyList: ["ip:1.2.3.4", "user:spammer-123", "apikey:compromised-key"]
});

// Verificar si está en deny list
const isDenied = await limiter.isDenied("ip:1.2.3.4");
```

---

## Caché Efímera (Ephemeral Cache)

```typescript
// Cache simple con TTL (usa mismo Redis)
await redis.setex("cache:user:123", 300, JSON.stringify(userData)); // 5 min TTL
const cached = await redis.get("cache:user:123");
```

---

## Analytics y Métricas

```typescript
const limiter = new Ratelimit({
  redis,
  limiter: Ratelimit.slidingWindow(100, "1m"),
  analytics: true // Habilita métricas
});

// Métricas disponibles (periodic flush a Redis)
const metrics = await limiter.getMetrics();
// { totalRequests, blockedRequests, averageLatency, ... }
```

---

## Timeouts y Multi-Región

```typescript
const limiter = new Ratelimit({
  redis,
  limiter: Ratelimit.slidingWindow(100, "1m"),
  timeout: 5000, // Timeout Redis (ms) - default: 5000
  // Multi-región: configurar réplicas en dashboard Upstash
});
```

---

## Estimación de Costos Redis

| Operación | Comandos Redis | Costo aprox. |
|-----------|----------------|--------------|
| `limit()` | 2-4 (INCR, EXPIRE, GET, PEXPIRE) | ~$0.0001 per 10k requests |
| `block()` | 1 (SET con NX) | Mínimo |
| Analytics | Batch writes periódicos | Bajo |

**Optimización**: Usar `slidingWindow` > `fixedWindow` para menos comandos en fronteras.

---

## Next.js Middleware Example

```typescript
// middleware.ts
import { NextResponse } from "next/server";
import { Ratelimit } from "@upstash/ratelimit";
import { Redis } from "@upstash/redis";

const redis = Redis.fromEnv();
const limiter = new Ratelimit({ redis, limiter: Ratelimit.slidingWindow(20, "1m") });

export async function middleware(request: NextRequest) {
  const ip = request.headers.get("x-forwarded-for") || "anonymous";
  const { success } = await limiter.limit(`ip:${ip}`);

  if (!success) {
    return new NextResponse("Rate limited", { status: 429 });
  }
  return NextResponse.next();
}

export const config = { matcher: "/api/:path*" };
```

---

## Mejores Prácticas

1. **Sliding Window** como default — suave, sin picos en fronteras
2. **Token Bucket** para endpoints con burst legítimo (AI, uploads)
3. **Prefixes descriptivos** — `auth:`, `api:`, `form:` para debugging
4. **Deny lists** para abusers conocidos
5. **Headers estándar** — `X-RateLimit-*`, `Retry-After` para clientes
6. **Analytics habilitado** — monitoring de patrones de abuso
7. **Timeouts conservadores** — 5s default, ajustar por latencia región

---

## Recursos

- [Documentación Oficial](https://upstash.com/docs/ratelimit)
- [GitHub @upstash/ratelimit](https://github.com/upstash/ratelimit-js)
- [Algorithms Deep Dive](https://upstash.com/docs/ratelimit/algorithms)