# Search (Upstash) — Full-Text & Semántico con Reranking

> **Submódulo de `upstash`** — Router: `upstash` → `references/search.md`. Skill independiente aspiracional: `datos-vectorial` (no existe en este repo) incluye esto.

---

## Instalación

```bash
npm install @upstash/search
```

```typescript
import { Search } from "@upstash/search";

const client = new Search({
  url: process.env.UPSTASH_SEARCH_REST_URL!,
  token: process.env.UPSTASH_SEARCH_REST_TOKEN!,
});

const index = client.index("my-index");
```

---

## Conceptos Clave

| Concepto | Descripción |
|----------|-------------|
| **Content** | Texto buscable (full-text + semántico). Lo que el usuario busca. |
| **Metadata** | Campos filtrables (categoría, autor, fecha, tags, precio). No se busca, se filtra. |
| **Reranking** | Re-ordenamiento de resultados por relevancia semántica (cross-encoder). |

---

## Operaciones Principales

### Crear Índice

```typescript
// Índice se crea automáticamente al primer upsert
const index = client.index("products");
```

### Upsert (Insertar/Actualizar Documentos)

```typescript
await index.upsert([
  {
    id: "prod-1",
    content: "Zapatillas running Nike Air Zoom - ligeras, amortiguadas, para maratón",
    metadata: {
      category: "calzado",
      brand: "Nike",
      price: 129.99,
      tags: ["running", "maraton", "hombre"],
      in_stock: true
    }
  },
  {
    id: "prod-2",
    content: "Raqueta tenis Wilson Pro Staff - control, precisión, grafito",
    metadata: {
      category: "deportes",
      brand: "Wilson",
      price: 189.00,
      tags: ["tenis", "competicion"],
      in_stock: true
    }
  }
]);
```

### Search (Búsqueda)

```typescript
// Búsqueda simple
const results = await index.search({
  query: "zapatillas running",
  topK: 10
});

// Búsqueda con reranking (mejor relevancia semántica)
const reranked = await index.search({
  query: "zapatillas para correr larga distancia",
  topK: 10,
  rerank: true  // Usa cross-encoder para re-ordenar
});

// Búsqueda híbrida (keyword + semántico)
const hybrid = await index.search({
  query: "nike running",
  topK: 10,
  // Combina BM25 + embeddings automáticamente
});
```

### Filtrado (SQL-like / Estructurado)

```typescript
// Filtros estructurados
const filtered = await index.search({
  query: "running",
  topK: 10,
  filter: "category = 'calzado' AND price < 150 AND in_stock = true"
});

// Filtros SQL-like
const sqlFiltered = await index.search({
  query: "tenis",
  topK: 10,
  filter: "brand IN ('Nike', 'Adidas') AND tags CONTAINS 'competicion'"
});

// Operadores soportados:
// =, !=, >, <, >=, <=
// IN, NOT IN
// CONTAINS, NOT CONTAINS (arrays/strings)
// AND, OR, NOT, paréntesis
```

### Paginación con Range

```typescript
// Cursor-based pagination
let cursor: string | undefined;
do {
  const page = await index.search({
    query: "running",
    topK: 20,
    cursor
  });

  // procesa page.results
  cursor = page.cursor; // undefined = fin
} while (cursor);
```

### Fetch / Delete / Reset

```typescript
// Fetch por ID
const doc = await index.fetch("prod-1");

// Delete
await index.delete("prod-1");
await index.delete(["prod-1", "prod-2"]);
await index.delete({ filter: "category = 'old'" });

// Reset índice completo
await index.reset();
```

### Info del Índice

```typescript
const info = await index.info();
// { documentCount: 150, sizeBytes: 2048000, ... }
```

---

## Reranking (Re-ordenamiento Semántico)

```typescript
// Sin reranking: BM25 / vector similarity (rápido, ~10ms)
const fast = await index.search({ query: "nike air", topK: 20 });

// Con reranking: Cross-encoder (preciso, ~50-100ms)
const precise = await index.search({
  query: "nike air",
  topK: 20,
  rerank: true
});

// Diferencia: rerank entiende "air" como tecnología Nike, no solo palabra
```

**Cuándo usar reranking:**
- Búsquedas de usuario final (precisión > velocidad)
- Consultas ambiguas o conversacionales
- Top-K pequeño (≤20) donde calidad importa

**Cuándo NO usar:**
- Autocomplete / typeahead (velocidad crítica)
- Top-K grande (>50)
- Filtros estrictos ya reducen resultados

---

## Mejores Prácticas

1. **Content vs Metadata**: `content` = lo que se busca; `metadata` = lo que se filtra
2. **Reranking selectivo**: Solo en búsquedas de usuario, no en autocomplete
3. **Filtros estrictos primero**: Reducen candidatos antes de rerank
4. **Batch upsert**: Hasta 1000 docs por request
5. **IDs deterministas**: Usa IDs de tu dominio (`prod-123`, no UUID aleatorios)
5. **Índices por dominio**: `products`, `docs`, `users` — no todo en uno

---

## Recursos

- [Documentación Oficial](https://upstash.com/docs/search)
- [GitHub @upstash/search](https://github.com/upstash/search-js)
- [Reranking Guide](https://upstash.com/docs/search/reranking)