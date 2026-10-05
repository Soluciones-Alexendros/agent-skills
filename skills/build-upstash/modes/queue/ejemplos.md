# Ejemplos Queue (ES)

> Ejemplos mínimos del modo `queue` (QStash + workflows). Detalle en
> `references/queues.md` y `references/workflow.md`.

## Publicar + cron

```typescript
import { Client } from "@upstash/qstash";
const qstash = Client.fromEnv();

await qstash.publishJSON({ url: "https://app.com/api/job", body: { id: 1 } });
await qstash.schedules.create({
  destination: "https://app.com/api/diario",
  cron: "0 9 * * *",
});
```

## Workflow con sleep

```typescript
import { serve } from "@upstash/workflow/nextjs";

export const { POST } = serve(async (context) => {
  const pedido = await context.run("crear-pedido", async () => crearPedido());
  await context.sleep("espera-pago", 60 * 60 * 24); // 1 día
  await context.run("recordar-pago", async () => recordarPago(pedido.id));
});
```

## Verificar firma (receiver)

```typescript
import { Receiver } from "@upstash/qstash";

const receiver = new Receiver({
  currentSigningKey: process.env.QSTASH_CURRENT_SIGNING_KEY!,
  nextSigningKey: process.env.QSTASH_NEXT_SIGNING_KEY!,
});
const ok = await receiver.verify({ signature, body });
```
