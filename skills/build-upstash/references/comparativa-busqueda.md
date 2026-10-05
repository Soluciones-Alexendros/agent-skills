# Redis Search vs Search SDK vs Vector Hybrid (ES)

> Recurso de la skill `build-upstash`. Cuándo usar cada motor de búsqueda.

## Regla rápida

| Caso | Motor | Modo |
|---|---|---|
| Ya guardas los datos en Redis y necesitas índice secundario (texto, agregaciones, facetas) sobre esos mismos datos | **Redis Search** (módulo RediSearch sobre tu DB) | `../modes/redis/MODE.md` (`search-overview.md` y `search-*.md`) |
| Búsqueda de sitio/productos standalone con typo-tolerance y reranking, sin Redis previo | **Search SDK** (`@upstash/search`, índice gestionado) | `../modes/search/MODE.md` |
| Búsqueda por significado (embeddings), RAG o híbrida vectorial + keyword | **Vector** (índices dense/sparse/híbridos) | `../modes/vector/MODE.md` |

## Diferenciación

- **Redis Search**: vive dentro de tu base Redis; consultas, agregaciones (`$avg`, `$sum`,
  `$terms`, `$range`), aliases para reindexado sin downtime. Ideal si el dato ya está en
  Redis y quieres filtrar/agregar sobre él. No es un índice gestionado aparte.
- **Search SDK**: servicio de búsqueda dedicado; creas un índice, haces upsert de
  documentos y buscas con tolerancia a typos, filtros SQL-like y reranking. Ideal para
  site/product search sin operar Redis.
- **Vector Hybrid**: similaridad semántica por embeddings; el modo híbrido combina vector
  + keyword y el filtrado por metadata recorta el espacio. Ideal para RAG, semantic
  search y semantic cache. Si además necesitas texto exacto con facetas, combina Vector
  (recall semántico) + Search SDK o Redis Search (precisión/facetas).

## Combinaciones típicas

- Catálogo con typo + facetas y stock en Redis → Search SDK (búsqueda) + Redis (stock).
- Chat con RAG sobre docs propios → Vector (retrieval) + LLM.
- Analítica sobre eventos ya en Redis → Redis Search (agregaciones).
