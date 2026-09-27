# Workflows Duraderos (Upstash Workflow) — Referencia Completa

> **Submódulo de `upstash`** — Modo interno de `upstash` (`modes/queue/MODE.md`). Basado en QStash.

---

## Instalación

```bash
npm install @upstash/workflow
```

---

## Concepto Central

**Workflow = función serverless que sobrevive a timeouts, retries, reinicios.**
Cada `context.run()` = checkpoint. Si falla, reanuda desde el último paso exitoso.

---

## Definir Endpoint (serve)

```typescript
// app/api/workflow/route.ts (Next.js App Router)
import { serve } from "@upstash/workflow";

export const { POST } = serve(async (context) => {
  // Paso 1: Procesar pedido
  const order = await context.run("process-order", async () => {
    const order = await db.orders.create(context.requestPayload);
    await notifyUser(order.id, "created");
    return order;
  });

  // Paso 2: Pago (puede tardar, timeout largo)
  const payment = await context.run("charge-payment", async () => {
    return await stripe.charge(order.amount, order.paymentMethod);
  }, { retries: 3, timeout: "10m" });

  // Paso 3: Llamar API externa (con context.call)
  const shipping = await context.call("create-shipment", {
    url: "https://logistics.example.com/api/shipments",
    method: "POST",
    body: { orderId: order.id, address: order.shippingAddress }
  });

  // Paso 4: Sleep sin mantener función viva (minutos a días)
  await context.sleep("wait-for-carrier", "24h"); // Reanuda automáticamente

  // Paso 5: Wait for event (webhook externo)
  const delivery = await context.waitForEvent("delivery-confirmed", {
    timeout: "7d"
  });

  // Paso 6: Completar
  await context.run("complete-order", async () => {
    await db.orders.update(order.id, { status: "delivered" });
    await notifyUser(order.id, "delivered");
  });
});
```

---

## API del Contexto (context)

| Método | Descripción |
|--------|-------------|
| `context.run(name, fn, options?)` | Paso con checkpoint. `options`: retries, timeout |
| `context.call(name, fetchOptions)` | Llamada HTTP externa con retry automático |
| `context.sleep(name, duration)` | Duerme sin mantener función (`"5m"`, `"2h"`, `"7d"`) |
| `context.waitForEvent(name, options)` | Espera evento/webhook externo |
| `context.invoke(name, workflowUrl, payload)` | Invocar otro workflow |
| `context.set(key, value)` / `context.get(key)` | Estado persistente entre pasos |
| `context.headers` / `context.requestPayload` | Input del trigger |

---

## Trigger y Cliente

```typescript
import { Client } from "@upstash/workflow";

const client = new Client({ token: process.env.QSTASH_TOKEN! });

// Trigger simple
await client.trigger({
  url: "https://app.example.com/api/workflow",
  body: { orderId: "ORD-123" }
});

// Trigger con headers
await client.trigger({
  url: "https://app.example.com/api/workflow",
  body: { orderId: "ORD-123" },
  headers: { "Idempotency-Key": "ORD-123" }
});

// Cancelar run
await client.cancel({ workflowRunId: "run_abc123" });

// Inspeccionar run
const run = await client.getRun({ workflowRunId: "run_abc123" });
// { status: "running" | "completed" | "failed", steps: [...], ... }
```

---

## Confiabilidad (Retries, Callbacks, DLQ)

```typescript
export const { POST } = serve(async (context) => {
  await context.run("flaky-step", async () => {
    await unreliableApi.call();
  }, {
    retries: 5,              // Reintentos (default: 3)
    retryDelay: "exponential", // "constant" | "exponential"
    timeout: "5m",           // Timeout del paso
    failureCallback: "https://api.example.com/failure-webhook", // Si falla todo
  });
});

// Dead Letter Queue (configurar en dashboard QStash)
// Mensajes fallados tras retries → DLQ para inspección manual
```

---

## Control de Flujo (Concurrencia, Rate, Paralelismo)

```typescript
export const { POST } = serve(async (context) => {
  // Rate limiting global
  await context.run("step-1", ..., { rateLimit: { max: 100, window: "1m" } });

  // Concurrencia: máx runs simultáneos
  await context.run("step-2", ..., { concurrency: 10 });

  // Paralelismo dentro de un run
  const [users, products] = await Promise.all([
    context.run("fetch-users", () => db.users.list()),
    context.run("fetch-products", () => db.products.list())
  ]);
});
```

---

## Human-in-the-Loop (Aprobación)

```typescript
// Paso que espera aprobación humana
const approval = await context.waitForEvent("manager-approval", {
  timeout: "48h" // Expira si no aprueban
});

// Frontend llama a client.notifyEvent({ workflowRunId, eventName: "manager-approval", payload: { approved: true } })
if (!approval?.payload?.approved) {
  throw new Error("Rechazado por manager");
}
```

---

## Realtime Updates (SSE / WebSocket)

```typescript
// Cliente se suscribe a updates
const eventSource = new EventSource(`/api/workflow/stream?runId=${runId}`);
eventSource.onmessage = (e) => {
  const step = JSON.parse(e.data);
  updateUI(step); // step.name, step.status, step.output
};

// Workflow emite automáticamente cada step
```

---

## Desarrollo Local (QStash Dev Server)

```bash
# Terminal 1: Dev server QStash
npx qstash dev --port 8080

# Terminal 2: Tu app (Next.js, etc.)
QSTASH_DEV=true npm run dev
# O en código:
const client = new Client({ token: "dev", devMode: true });
```

---

## Migración Segura de Workflows

```typescript
// Versionar workflows
export const { POST } = serve(async (context) => {
  const version = context.get("version") || 1;

  if (version === 1) {
    // Lógica v1
    await context.run("old-step", ...);
    await context.set("version", 2); // Migrar estado
  }

  if (version >= 2) {
    // Lógica v2 (nuevos pasos)
    await context.run("new-step", ...);
  }
});
```

---

## Agentes y Orquestadores

```typescript
// Workflow como agente
export const { POST } = serve(async (context) => {
  const task = context.requestPayload.task;

  // Planificar
  const plan = await context.run("plan", async () => {
    return await llm.plan(task);
  });

  // Ejecutar pasos del plan
  for (const step of plan.steps) {
    await context.run(`execute-${step.id}`, async () => {
      return await executeStep(step);
    });
  }

  // Completar
  await context.run("finalize", async () => {
    return await llm.summarize(plan);
  });
});
```

---

## Middleware

```typescript
import { serve } from "@upstash/workflow";
import { loggingMiddleware } from "@upstash/workflow/middleware";

export const { POST } = serve(
  async (context) => { /* workflow */ },
  { middleware: [loggingMiddleware] }
);

// Custom middleware
const authMiddleware = async (context, next) => {
  const auth = context.headers.get("Authorization");
  if (!auth) throw new Error("Unauthorized");
  return next(context);
};
```

---

## Mejores Prácticas

1. **Idempotencia**: Cada `context.run` debe ser idempotente (mismo input = mismo output)
2. **Checkpoints granulares**: Un paso = una unidad lógica de trabajo
3. **Timeouts realistas**: API externas = 30s-10m; DB = 5-30s
4. **Retries exponenciales**: Para APIs inestables
5. **Estado mínimo en context.set**: Solo lo necesario para reanudar
6. **Testing**: Usa `QSTASH_DEV=true` + `npx qstash dev` en local
7. **Observabilidad**: Logs estructurados + `client.getRun()` para debugging

---

## Recursos

- [Documentación Oficial](https://upstash.com/docs/workflow)
- [GitHub @upstash/workflow](https://github.com/upstash/workflow-js)
- [Durable Execution Patterns](https://upstash.com/docs/workflow/patterns)