# Modo Queue (ES)

> Modo interno de la skill `construir-upstash` (no es skill separada). Router: `construir-upstash` → este modo
> ante queue, cola, cron, mensaje, background job, DLQ, retry, fan-out, workflow, durable
> o step.

## Cubre

QStash (colas de mensajes, cron/schedules, FIFO con paralelismo configurable, URL groups,
callbacks, deduplicación, DLQ, reintentos, verificación de firmas, multi-region) y
**Workflows duraderos, que extienden queue**: los workflows corren sobre QStash
(`serve`, `context.run()` como checkpoint, `sleep`/`call`, `wait-for-event`, `invoke`,
flow-control, webhooks, realtime, middleware, migraciones, REST API, troubleshooting).

## Referencias propias

Guías principales (ES): `references/queues.md` (QStash) y `references/workflow.md` (workflows).

| Fichero | Contenido |
|---|---|
| `references/queues.md` | guía principal ES de QStash |
| `references/qstash-overview.md` | visión general del SDK `@upstash/qstash` |
| `references/publishing-messages.md` | publicar mensajes |
| `references/schedules.md` | cron y mensajes diferidos |
| `references/queues-and-flow-control.md` | FIFO, paralelismo, flow-control |
| `references/url-groups.md` | fan-out a grupos de URLs |
| `references/local-development.md` | desarrollo local (`devMode`) |
| `references/receiver.md` | verificación de firmas |
| `references/nextjs.md` | verificación en Next.js (App/Pages/Edge) |
| `references/callbacks.md` | callbacks (alternativa a sondear DLQ) |
| `references/dlq.md` | dead-letter queue |
| `references/deduplication.md` | deduplicación |
| `references/multi-region-summary.md` | multi-region |
| `references/workflow.md` | guía principal ES de workflows |
| `references/workflow-overview.md` | visión general del SDK `@upstash/workflow` |
| `references/client.md`, `references/context.md`, `references/serve.md` | conceptos base |
| `references/flow-control.md`, `references/invoke.md`, `references/retries-failures-reliability.md`, `references/wait-for-event.md`, `references/webhooks.md` | capacidades |
| `references/local-dev.md`, `references/middleware.md`, `references/migrations.md`, `references/realtime.md` | cómo-tos |
| `references/agents.md` | workflows para agentes |
| `references/rest-api.md` | REST API |
| `references/troubleshooting.md` | diagnóstico |

Script heredado: `examples/verify-multi-region-setup.ts` (verificación de variables
multi-region, ejecutable sin argumentos).

## Ejemplos

Ver `ejemplos.md` (publicar + cron, workflow con `sleep`, verificación de firma).

## Dependencias

Workflows extiende queue: este modo es el único lugar de workflows, no hay modo separado.
Configuración y errores comunes: `../../core/config.md`, `../../core/errores.md`.
