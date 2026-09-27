# Modo Vector (ES)

> Modo interno de la skill `construir-upstash` (no es skill separada). Router: `construir-upstash` → este modo
> ante embedding, RAG, vector, similarity, kNN, namespace, dense o sparse.

## Cubre

Embeddings, similarity search, índices dense/sparse/híbridos, filtrado por metadata
(SQL-like), namespaces multi-tenant, RAG completo y semantic cache.

## Referencias propias

Guía principal (ES): `references/vector.md`.

| Fichero | Contenido |
|---|---|
| `references/vector.md` | guía principal ES: instalación, RAG, namespaces |
| `references/overview.md` | visión general del SDK `@upstash/vector` |
| `references/sdk-methods.md` | métodos del SDK (upsert, query, fetch, range, delete) |
| `references/filtering-and-metadata.md` | filtrado por metadata |
| `references/index-structure.md` | estructura de índices dense/sparse/híbridos |
| `references/namespaces.md` | namespaces multi-tenant |

## Ejemplos

Ver `ejemplos.md` (upsert + query, RAG mínimo, semantic cache).

## Dependencias

Ninguna. Si dudas entre Vector, Search SDK o Redis Search, ver
`../../references/comparativa-busqueda.md`.
Configuración y errores comunes: `../../core/config.md`, `../../core/errores.md`.
