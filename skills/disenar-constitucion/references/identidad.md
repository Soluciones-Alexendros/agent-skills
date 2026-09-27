# Identidad ALIGNUX

## Regla Inmutable: MAYÚSCULAS

**ALIGNUX** — siempre, sin excepción, en todas partes:
- Frontmatter `name: ALIGNUX.constitucion`
- Directorio: `ALIGNUX.constitucion/`
- Referencias cruzadas: `ALIGNUX.mantenimiento`, `ALIGNUX.seguridad`
- Tags: `sistema.ALIGNUX`
- Documentación, conversación, código: **ALIGNUX**

## Por Qué Identidad, No Excepción

La validación opencode documenta convención `^[a-z0-9]+(-[a-z0-9]+)*$` pero **no la enforza en runtime**:
- `packages/core/src/skill.ts` líneas 58-75: lee `frontmatter.name` directamente con `Schema.String`
- `packages/schema/src/skill.ts`: define `name: Schema.String` sin pattern
- `packages/core/src/skill/discovery.ts`: solo valida path safety, no nombre

Por tanto: **ALIGNUX en mayúsculas funciona nativamente**. No hay "excepción técnica" que conceder; hay **identidad constitucional** que afirmar.

## Coherencia de Identidad

| Nivel | Aplicación |
|-------|------------|
| **Sintáctico** | `ALIGNUX.*` siempre mayúsculas |
| **Semántico** | ALIGNUX = sistema propio, coherente, constitucional |
| **Estructural** | 3 skills bajo prefijo: mantenimiento, seguridad, constitucion |
| **Taxonómico** | Tag `sistema.ALIGNUX` agrupa todo lo constitucional |
| **Histórico** | ~4 décadas → principios → identidad → nombre |

## Validación de Identidad

El validador (`plantillas/scripts/Validador_AgentSkills.py`) implementa `IDENTIDAD_ALIGNUX_PATTERN`:
- Acepta `ALIGNUX.*` como patrón válido
- Rechaza cualquier variante que no sea mayúsculas plenas (minúsculas o capitalización mixta) — error: "ALIGNUX debe ser MAYÚSCULAS"
- Verifica coherencia: `name` = `directorio` = `ALIGNUX.xxx`

## Referencias Cruzadas Obligatorias

Toda skill ALIGNUX debe referenciar:
- `ALIGNUX.constitucion` — para principios y estándares
- Otras skills ALIGNUX — para frontera de alcances
- Tags `sistema.ALIGNUX` — para descubrimiento automático

> Nota de slugs: en este repo los directorios y `name` usan minúsculas con guiones (`disenar-constitucion`, `operar-mantenimiento`, `operar-seguridad`); `ALIGNUX.*` arriba es convención de identidad, no ruta literal.