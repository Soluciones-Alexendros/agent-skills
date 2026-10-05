# QStash — Message Queue, Cron & Scheduling

> **Submódulo de `build-upstash`** — Modo interno de `build-upstash` (`modes/queue/MODE.md`)

---

## Instalación

```bash
npm install @upstash/qstash
```

```typescript
import { Client } from "@upstash/qstash";

const client = new Client({
  token: process.env.QSTASH_TOKEN!,
});
```

---

## Publicación de Mensajes

```typescript
// Publicar JSON a endpoint
const result = await client.publishJSON({
  url: "https://api.example.com/webhook",
  body: { event: "user.created", userId: "123", timestamp: Date.now() },
  // Opciones opcionales:
  retries: 3,           // Reintentos (default: 3)
  delay: "10m",         // Delay: "10s", "5m", "1h", "1d"
  callback: "https://api.example.com/callback", // Callback al completar
  deduplicationId: "user-created-123", // Deduplicación
});

// Publicar a URL Group (fan-out)
await client.publishJSON({
  urlGroup: "notifications", // Pre-configurado en dashboard
  body: { type: "email", to: "user@example.com", subject: "Welcome!" }
});
```

---

## Programación (Schedules / Cron)

```typescript
// Schedule recurrente (cron)
await client.schedules.create({
  cron: "0 9 * * *",        // Cada día a las 9:00 UTC
  url: "https://api.example.com/daily-report",
  body: { reportType: "daily" },
  retries: 2,
});

// Schedule único (delayed)
await client.schedules.create({
  delay: "2h",              // En 2 horas
  url: "https://api.example.com/reminder",
  body: { userId: "123", reminder: "appointment" }
});

// Listar schedules
const schedules = await client.schedules.list();

// Eliminar schedule
await client.schedules.delete(scheduleId);
```

---

## Colas FIFO (Queues + Flow Control)

```typescript
// Crear cola
await client.queues.create("email-queue", {
  maxRetries: 3,
  parallelism: 5,           // Procesar 5 mensajes en paralelo
  pauseOnFailure: true,     // Pausar cola si falla
});

// Encolar mensaje (FIFO garantizado)
await client.enqueueJSON("email-queue", {
  to: "user@example.com",
  template: "welcome",
  data: { name: "Alice" }
});

// Procesar cola (consumer)
const messages = await client.queue.pop("email-queue", { count: 10 });
for (const msg of messages) {
  await sendEmail(msg.body);
  await client.queue.ack("email-queue", msg.messageId); // Confirmar procesado
}

// Pausar/Reanudar cola
await client.queues.pause("email-queue");
await client.queues.resume("email-queue");
```

---

## Dead Letter Queue (DLQ)

```typescript
// Configurar DLQ al crear cola
await client.queues.create("critical-queue", {
  dlq: "critical-queue-dlq",  // Cola para mensajes fallidos
  maxRetries: 3,
});

// Reprocesar desde DLQ
const dlqMessages = await client.queue.pop("critical-queue-dlq", { count: 50 });
for (const msg of dlqMessages) {
  await client.enqueueJSON("critical-queue", msg.body); // Re-encolar
  await client.queue.ack("critical-queue-dlq", msg.messageId);
}
```

---

## Deduplicación de Mensajes

```typescript
// Deduplicación por ID personalizado
await client.publishJSON({
  url: "https://api.example.com/webhook",
  body: { orderId: "ORD-123" },
  deduplicationId: "order-ORD-123" // Mismo ID = no duplicado en 24h
});

// TTL de deduplicación configurable
```

---

## Fan-Out (URL Groups)

```typescript
// En dashboard: crear URL Group "notifications" con múltiples endpoints
// Luego publicar una vez:
await client.publishJSON({
  urlGroup: "notifications",
  body: { alert: "Server down!", severity: "critical" }
});
// QStash entrega a TODOS los endpoints del group en paralelo
```

---

## Verificación de Webhooks (Next.js, Vercel, Cloudflare, Deno)

```typescript
import { Receiver } from "@upstash/qstash";

const receiver = new Receiver({
  currentSigningKey: process.env.QSTASH_CURRENT_SIGNING_KEY!,
  nextSigningKey: process.env.QSTASH_NEXT_SIGNING_KEY!,
});

// Next.js App Router (app/api/qstash/route.ts)
export async function POST(req: Request) {
  const verified = await receiver.verify(req, {
    // headers: req.headers, // auto-detectado
  });

  if (!verified) return new Response("Invalid signature", { status: 401 });

  const body = await req.json();
  await processWebhook(body);
  return new Response("OK");
}
```

---

## Desarrollo Local (Dev Server)

```typescript
// En desarrollo local
const client = new Client({
  token: "dev-token", // Cualquier string
  devMode: true,      // Inicia servidor local automáticamente
});

// O CLI: npx qstash dev --port 8080
```

---

## Migración Multi-Región

```typescript
// Verificar setup multi-región
import { verifyMultiRegionSetup } from "@upstash/qstash/advanced/multi-region/verify-multi-region-setup";

await verifyMultiRegionSetup({
  primaryToken: process.env.QSTASH_TOKEN!,
  secondaryToken: process.env.QSTASH_SECONDARY_TOKEN!,
});
```

---

## Mejores Prácticas

1. **Siempre verifica webhooks** con `Receiver` class
2. **Variables de entorno** para tokens y signing keys
3. **Retries y timeouts** apropiados por caso de uso
4. **Colas para orden** + parallelism controlado
5. **DLQ obligatoria** para recuperación de fallos
6. **Deduplicación** para idempotencia (pagos, emails)
7. **Callbacks** para tracking de estado asíncrono

---

## Recursos

- [Documentación Oficial](https://upstash.com/docs/qstash)
- [GitHub @upstash/qstash](https://github.com/upstash/qstash-js)
- [Next.js Verification](https://upstash.com/docs/qstash/verification/nextjs)