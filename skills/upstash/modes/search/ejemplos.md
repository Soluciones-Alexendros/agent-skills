# Ejemplos Search (ES)

> Ejemplos mínimos del modo `search`. Detalle en `references/search.md`.

## Índice de productos + búsqueda con typo

```typescript
import { Search } from "@upstash/search";
const client = Search.fromEnv();
const idx = client.index("productos");

await idx.upsert([
  { id: "p-1", content: { nombre: "teclado mecánico", precio: 89 } },
]);
const res = await idx.search({ query: "teclado mecanico", limit: 5 }); // typo OK
```

## Facetas y filtros

```typescript
const baratos = await idx.search({
  query: "teclado",
  filter: "precio < 100",
  limit: 10,
});
```
