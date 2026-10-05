# Vector Database (Upstash) — Referencia Completa

> **Modo interno de `build-upstash`** (`modes/vector/MODE.md`) — referencia completa de nivel standalone; incluye búsqueda (`references/search.md`).

---

## Instalación y Configuración

```bash
npm install @upstash/vector
```

```typescript
import { Index } from "@upstash/vector";

const index = new Index({
  url: process.env.UPSTASH_VECTOR_REST_URL!,
  token: process.env.UPSTASH_VECTOR_REST_TOKEN!,
});

// O desde entorno
const index = Index.fromEnv();
```

**Variables de entorno:**
```bash
UPSTASH_VECTOR_REST_URL=https://your-vector.upstash.io
UPSTASH_VECTOR_REST_TOKEN=your-token-here
```

---

## Tipos de Índice

| Tipo | Descripción | Caso de Uso |
|------|-------------|-------------|
| **Dense** | Vectores densos (ej. 1536-dim OpenAI, 768-dim BERT) | Semantic search, RAG, embeddings estándar |
| **Sparse** | Vectores dispersos (BM25, SPLADE) | Keyword search, exact match, híbrido |
| **Hybrid** | Dense + Sparse combinados | **Mejor de ambos mundos**: semántico + keyword |

**Crear índice híbrido (recomendado):**
```typescript
const index = new Index({
  url: process.env.UPSTASH_VECTOR_REST_URL!,
  token: process.env.UPSTASH_VECTOR_REST_TOKEN!,
  // Hybrid = dense + sparse automático
});
```

---

## Operaciones Principales

### Upsert (Insertar/Actualizar)

```typescript
// Vectores con metadata
await index.upsert([
  {
    id: "doc-1",
    vector: [0.1, 0.2, 0.3, ...], // 1536-dim
    metadata: {
      title: "Introducción a RAG",
      category: "ai",
      author: "user-123",
      tags: ["rag", "llm", "vector-db"]
    }
  },
  {
    id: "doc-2",
    vector: [0.4, 0.5, 0.6, ...],
    metadata: { title: "Vector DBs", category: "db" }
  }
]);

// Texto crudo (embedding model integrado)
await index.upsert([
  {
    id: "doc-3",
    data: "Texto completo del documento...", // Upstash genera embedding
    metadata: { source: "blog", lang: "es" }
  }
]);
```

### Query (Búsqueda por Similitud)

```typescript
// Búsqueda vectorial
const results = await index.query({
  vector: [0.1, 0.2, 0.3, ...], // query vector
  topK: 10,
  includeVectors: false,
  includeMetadata: true,
});

// Búsqueda con filtro de metadata
const filtered = await index.query({
  vector: queryVector,
  topK: 5,
  filter: "category = 'ai' AND author = 'user-123'",
});

// Búsqueda híbrida (dense + sparse)
const hybrid = await index.query({
  vector: denseVector,
  topK: 10,
  // sparse vector automático si índice hybrid
});
```

### Fetch / Range / Delete

```typescript
// Fetch por IDs
const docs = await index.fetch(["doc-1", "doc-2"]);

// Range (paginación por cursor)
for await (const batch of index.range({ prefix: "doc-", limit: 100 })) {
  // procesa batch
}

// Delete
await index.delete(["doc-1", "doc-2"]);
await index.delete({ filter: "category = 'old'" }); // bulk delete
```

---

## Namespaces (Organización de Datos)

```typescript
// Índice por namespace
const aiIndex = new Index({ ..., namespace: "ai-docs" });
const blogIndex = new Index({ ..., namespace: "blog-posts" });

// Upsert en namespace específico
await aiIndex.upsert([{ id: "1", vector: [...], metadata: {...} }]);

// Query en namespace
const results = await aiIndex.query({ vector: [...], topK: 5 });
```

**Casos de uso:** Multi-tenant, separación por proyecto, aislamiento de dominios.

---

## Filtrado por Metadata (Server-Side)

```typescript
// Filtros SQL-like
const results = await index.query({
  vector: queryVector,
  topK: 10,
  filter: "category = 'ai' AND tags CONTAINS 'rag' AND year >= 2024"
});

// Operadores soportados:
// =, !=, >, <, >=, <=
// IN, NOT IN
// CONTAINS, NOT CONTAINS (arrays/strings)
// AND, OR, NOT
// Paréntesis para precedencia
```

---

## Resumable Queries (Consultas Reanudables)

Para queries grandes que pueden timeout:

```typescript
const query = index.resumableQuery({
  vector: largeQueryVector,
  topK: 1000,
  filter: "status = 'published'"
});

// Ejecutar en chunks
for await (const page of query) {
  // procesa page (100 resultados)
  // query reanuda automáticamente si se interrumpe
}
```

---

## RAG (Retrieval-Augmented Generation) — Patrón Completo

```typescript
// 1. Embedding de la pregunta del usuario
const questionEmbedding = await openai.embeddings.create({
  model: "text-embedding-3-small",
  input: userQuestion
});

// 2. Buscar documentos relevantes
const context = await index.query({
  vector: questionEmbedding.data[0].embedding,
  topK: 5,
  includeMetadata: true,
  filter: "lang = 'es'"
});

// 3. Construir prompt con contexto
const contextText = context.map(r => r.metadata?.content).join("\n---\n");
const prompt = `Contexto:\n${contextText}\n\nPregunta: ${userQuestion}\nRespuesta:`;

// 4. Generar respuesta
const answer = await openai.chat.completions.create({
  model: "gpt-4o-mini",
  messages: [{ role: "user", content: prompt }]
});
```

---

## SDK Methods Reference

| Método | Descripción |
|--------|-------------|
| `upsert(records)` | Insertar/actualizar vectores (batch hasta 1000) |
| `query(options)` | Búsqueda k-NN con filtros |
| `fetch(ids)` | Obtener vectores por ID |
| `range(options)` | Paginación por cursor/prefix |
| `delete(ids \| filter)` | Eliminar por IDs o filtro |
| `reset()` | Vaciar índice completo |
| `resumableQuery(options)` | Query reanudable para grandes volúmenes |
| `info()` | Info del índice (dimensión, count, namespaces) |

---

## Integración con LLM / AI Apps

```typescript
// Semantic Cache (cache de respuestas por similitud)
async function cachedCompletion(prompt: string) {
  const embedding = await embed(prompt);
  const cached = await index.query({ vector: embedding, topK: 1, filter: "type = 'completion'" });

  if (cached[0]?.score > 0.95) {
    return cached[0].metadata.response; // Cache hit
  }

  const response = await llm.complete(prompt);
  await index.upsert([{
    id: `completion-${Date.now()}`,
    vector: embedding,
    metadata: { type: "completion", prompt, response }
  }]);
  return response;
}

// Recommendations
const similar = await index.query({
  vector: userProfileEmbedding,
  topK: 10,
  filter: "category = 'product' AND price < 100"
});
```

---

## Mejores Prácticas

1. **Dimensión consistente**: Todos los vectores en un índice deben tener misma dimensión
2. **Metadata enriquecida**: Incluye campos filterables (category, tags, dates, authors)
3. **Hybrid index**: Default para mejores resultados (semántico + keyword)
4. **Namespaces**: Aísla tenants, proyectos, entornos
5. **Batch upsert**: Hasta 1000 vectores por request
6. **Resumable queries**: Para exports, migraciones, grandes topK
7. **Monitoring**: Usa `index.info()` para tracking de count, namespaces

---

## Recursos

- [Documentación Oficial](https://upstash.com/docs/vector)
- [GitHub @upstash/vector](https://github.com/upstash/vector-js)
- [API Reference](https://upstash.com/docs/vector/sdks/ts/overview)
- [RAG Tutorial](https://upstash.com/docs/vector/rag)