# Errores compartidos Upstash (ES)

> Recurso interno de la skill `upstash`. Estrategia común de reintentos y fallos para los 7 modos.

## Reglas generales

1. Los SDK REST (`redis`, `vector`, `search`, `qstash`) no mantienen conexión: un fallo
   es un HTTP fallido, reintentable por defecto con backoff exponencial.
2. Nunca reintentar de forma no idempotente sin clave de deduplicación (ver
   `../modes/queue/references/deduplication.md`).
3. Todo trabajo que deba sobrevivir a timeouts/reinicios va a QStash o Workflows
   (modo `queue`), no a reintentos en memoria.

## Backoff recomendado

```typescript
async function conReintentos<T>(fn: () => Promise<T>, intentos = 3): Promise<T> {
  let espera = 250;
  for (let i = 1; ; i++) {
    try {
      return await fn();
    } catch (err) {
      if (i >= intentos) throw err;
      await new Promise((r) => setTimeout(r, espera));
      espera *= 2;
    }
  }
}
```

## Por servicio

| Servicio | Error típico | Respuesta |
|---|---|---|
| Redis | `429` / timeout REST | backoff + pipeline (`../modes/redis/references/pipeline-optimization.md`) |
| Redis réplicas | lectura obsoleta | solo lecturas tolerantes a eventualidad (`../modes/redis/references/redis-replicas.md`) |
| QStash | firma inválida | verificar con `Receiver` (`../modes/queue/references/receiver.md`), no reintentar |
| QStash | reintentos agotados | DLQ (`../modes/queue/references/dlq.md`), callbacks (`../modes/queue/references/callbacks.md`) |
| Workflows | paso fallido | `context.run()` reanuda desde el último checkpoint (`../modes/queue/references/workflow-overview.md`) |
| Ratelimit | `success=false` | responder `429` con `Retry-After`; listas de denegación (`../modes/ratelimit/references/traffic-protection.md`) |
| Blob | subida interrumpida | multipart resume (`../modes/blob/references/blob.md`) |
| Box | contenedor caído | snapshots y recreación (`../modes/box/references/box.md`) |

## Límites y coste (ratelimit)

Cuotas y precios en `../modes/ratelimit/references/pricing-cost.md`.
