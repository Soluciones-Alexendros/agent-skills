---
name: datos-postgres
description: >-
  Buenas prácticas Postgres (índices, RLS, migraciones, EXPLAIN, conexiones, pgvector). Usar
  antes de diseñar o cambiar schema Postgres, políticas RLS, índices o diagnosticar queries
  lentas. No usar para Redis/Vector Upstash (→ upstash).
license: MIT
metadata:
  author: Soluciones-Alexendros
  version: "0.1.0"
  dominio: datos
  idioma: es

---
# Supabase Postgres Best Practices

Comprehensive performance optimization guide for Postgres, maintained by Supabase. Contains rules across 8 categories, prioritized by impact to guide automated query optimization and schema design.

## Qué hace / Propósito

Recopila buenas prácticas de Postgres mantenidas por Supabase, aplicables a cualquier instalación. Sirve para diseñar schemas, escribir SQL e índices, definir RLS, planificar migraciones y diagnosticar rendimiento, bloqueos, conexiones o visibilidad incorrecta de filas antes y durante los cambios.

## Cuándo usarme / Triggering

- Antes de escribir o cambiar algo en una base de datos Postgres: crear/alterar tablas y columnas, elegir tipos, migraciones y declarative schema files.
- Al definir o revisar RLS policies y sus tests, índices, triggers, database functions, colas y scheduled jobs (pg_cron, pgmq), búsqueda vectorial (pgvector), restoring dumps (pg_restore) o importación de datos.
- Al diagnosticar slow queries, high CPU, timeouts, planes EXPLAIN, agotamiento de conexiones, locking, bloat o filas visibles al usuario/tenant incorrecto.
- **NO usar cuando**: el motor no sea Postgres (por ejemplo Redis o una base vectorial gestionada) o el tema sea pagos (usar `datos-stripe` — canon externo, no existe en este repo); esta skill cubre exclusivamente Postgres.

## Referencias internas

Cada regla vive en su propio archivo bajo `references/`; consulta `_sections.md` primero para orientarte y carga solo las reglas relevantes:

- `references/_sections.md` — índice completo de reglas por categoría y prioridad.
- `references/_template.md` — plantilla para añadir o actualizar una regla.
- `references/_contributing.md` — convenciones de contribución de reglas nuevas.
- `references/query-missing-indexes.md` — detectar y crear índices faltantes.
- `references/query-partial-indexes.md` — índices parciales para consultas filtradas.
- `references/query-composite-indexes.md` — índices compuestos y orden de columnas.
- `references/query-covering-indexes.md` — índices cubrientes para evitar heap fetches.
- `references/query-index-types.md` — elegir entre B-tree, GIN, GiST, BRIN y Hash.
- `references/conn-pooling.md` — pooling de conexiones (PgBouncer/Supavisor).
- `references/conn-limits.md` — límites de conexiones y consumo de memoria.
- `references/conn-idle-timeout.md` — timeouts de conexiones idle.
- `references/conn-prepared-statements.md` — prepared statements con pooling en modo transacción.
- `references/security-rls-basics.md` — fundamentos de Row-Level Security.
- `references/security-rls-performance.md` — rendimiento de las políticas RLS.
- `references/security-privileges.md` — privilegios y roles con mínimo privilegio.
- `references/schema-primary-keys.md` — elección de claves primarias (identity, UUIDv7).
- `references/schema-data-types.md` — elección de tipos de columna.
- `references/schema-constraints.md` — constraints e integridad de datos.
- `references/schema-foreign-key-indexes.md` — índices para claves foráneas.
- `references/schema-lowercase-identifiers.md` — identificadores en minúsculas.
- `references/schema-partitioning.md` — particionado de tablas grandes.
- `references/lock-deadlock-prevention.md` — prevención de deadlocks.
- `references/lock-short-transactions.md` — transacciones cortas y orden de locks.
- `references/lock-advisory.md` — advisory locks.
- `references/lock-skip-locked.md` — `SKIP LOCKED` para colas de trabajo.
- `references/data-batch-inserts.md` — inserciones por lotes.
- `references/data-n-plus-one.md` — eliminar patrones N+1.
- `references/data-pagination.md` — paginación estable (keyset).
- `references/data-upsert.md` — upserts eficientes con `ON CONFLICT`.
- `references/monitor-explain-analyze.md` — leer `EXPLAIN (ANALYZE, BUFFERS)`.
- `references/monitor-pg-stat-statements.md` — `pg_stat_statements` y consultas top.
- `references/monitor-vacuum-analyze.md` — vacuum, analyze y autovacuum.
- `references/advanced-full-text-search.md` — búsqueda full-text en Postgres.
- `references/advanced-jsonb-indexing.md` — indexado de documentos JSONB.
- `references/supabase-source.md` — fuente Supabase original (procedencia de las reglas).

## When to Apply

Reference these guidelines when:
- Writing SQL queries or designing schemas
- Implementing indexes or query optimization
- Reviewing database performance issues
- Configuring connection pooling or scaling
- Optimizing for Postgres-specific features
- Working with Row-Level Security (RLS)

## Rule Categories by Priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Query Performance | CRITICAL | `query-` |
| 2 | Connection Management | CRITICAL | `conn-` |
| 3 | Security & RLS | CRITICAL | `security-` |
| 4 | Schema Design | HIGH | `schema-` |
| 5 | Concurrency & Locking | MEDIUM-HIGH | `lock-` |
| 6 | Data Access Patterns | MEDIUM | `data-` |
| 7 | Monitoring & Diagnostics | LOW-MEDIUM | `monitor-` |
| 8 | Advanced Features | LOW | `advanced-` |

## How to Use

Read individual rule files for detailed explanations and SQL examples:

```
references/query-missing-indexes.md
references/query-partial-indexes.md
references/_sections.md
```

Each rule file contains:
- Brief explanation of why it matters
- Incorrect SQL example with explanation
- Correct SQL example with explanation
- Optional EXPLAIN output or metrics
- Additional context and references
- Supabase-specific notes (when applicable)

## References

- https://www.postgresql.org/docs/current/
- https://supabase.com/docs
- https://wiki.postgresql.org/wiki/Performance_Optimization
- https://supabase.com/docs/guides/database/overview
- https://supabase.com/docs/guides/auth/row-level-security

## Nota de fusión

Incluye las prácticas Supabase Postgres (`references/` y `references/supabase-source.md` si existe). Aplicable a Postgres en cualquier hosting.

## Uso

Diseño, cambio y diagnóstico Postgres: consultar `_sections.md` primero y cargar solo las reglas relevantes antes de tocar schema, RLS, índices o conexiones.

## Estructura

- `SKILL.md` — triggering, categorías por prioridad y modo de uso.
- `CHANGELOG.md` — extra top-level no referenciado (historial upstream Supabase).
- `references/` — 36 reglas (`query-*`, `conn-*`, `security-*`, `schema-*`, `lock-*`, `data-*`, `monitor-*`, `advanced-*`) + `_sections.md`, `_template.md`, `_contributing.md` y `supabase-source.md`.
- Sin `scripts/`: skill puramente documental.

## Referencias

- Internas: ver «Referencias internas» más arriba (todas existen).
- Canon externo: documentación Postgres y Supabase enlazada al final de cada regla.
