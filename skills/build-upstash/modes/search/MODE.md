# Modo Search (ES)

> Modo interno de la skill `construir-upstash` (no es skill separada). Router: `construir-upstash` → este modo
> ante full-text, búsqueda, typo-tolerance, facetas, rerank o filtros SQL.

## Cubre

Full-text search, búsqueda semántica e híbrida con reranking, filtros SQL-like,
paginación y SDK `@upstash/search`.

## Referencias propias

Guía principal (ES): `references/search.md`.

| Fichero | Contenido |
|---|---|
| `references/search.md` | guía principal ES: índices, upsert, búsqueda, filtros |
| `references/overview.md` | visión general del SDK |
| `references/quick-start.md` | inicio rápido (upsert + search) |
| `references/sdk-overview.md` | métodos del SDK |

## Ejemplos

Ver `ejemplos.md` (índice de productos, búsqueda con typo, facetas).

## Dependencias

Ninguna. No confundir con Redis Search (índices sobre Redis, en
`../redis/references/search-overview.md`) ni con Vector Hybrid (en `../vector/MODE.md`):
cuándo usar cada uno en `../../references/comparativa-busqueda.md`.
Configuración y errores comunes: `../../core/config.md`, `../../core/errores.md`.
