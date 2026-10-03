# Ejemplos Vector (ES)

> Ejemplos mínimos del modo `vector`. Detalle en `references/vector.md`.

## Upsert + query

```typescript
import { Index } from "@upstash/vector";
const index = Index.fromEnv();

await index.upsert([
  { id: "doc-1", vector: [0.1, 0.2, 0.3], metadata: { tema: "redis" } },
]);
const res = await index.query({ vector: [0.1, 0.2, 0.3], topK: 3 });
```

## RAG mínimo

```typescript
const pregunta = [0.1, 0.2, 0.3]; // embedding de la pregunta
const ctx = await index.query({ vector: pregunta, topK: 5, includeMetadata: true });
const contexto = ctx.map((r) => JSON.stringify(r.metadata)).join("\n");
// const respuesta = await llm(`Responde usando:\n${contexto}`);
```

## Semantic cache

```typescript
const hit = await index.query({ vector: pregunta, topK: 1 });
if (hit[0] && hit[0].score > 0.95) return hit[0].metadata!.respuesta; // reutiliza
```
