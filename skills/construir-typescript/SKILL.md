---
name: construir-typescript
description: >-
  Tipado avanzado de TypeScript: generics, conditional types, infer, branded types y
  patrones de API tipada. Usar ante tipos complejos, errores de inferencia difíciles o
  diseño de APIs tipadas. No usar para revisión de seguridad ni arquitectura general.
license: MIT
metadata:
  author: Soluciones-Alexendros
  version: "2.1.0"
  dominio: construir
  tipo: tecnologia
  idioma: es
---

# TypeScript: tipos avanzados

> Nota de formato: sección `Cuándo usarme`/`When to Use` fusionada 2026-09-26 en una única sección ES (`Cuándo usarme / Triggering`, con equivalencias EN entre paréntesis); se conservan las secciones estándar `Uso`, `Estructura`, `Herramientas` y `Referencias`.

Guía completa para dominar el sistema de tipos avanzado de TypeScript: generics, conditional types, mapped types, template literal types y utility types para construir aplicaciones robustas y type-safe (TypeScript 5.5+).

## Qué hace / Propósito

Domina el sistema de tipos avanzado de TypeScript (generics, conditional types, mapped types, template literals y utility types) para construir aplicaciones type-safe. Sirve para implementar lógica de tipos compleja, crear utilidades de tipos reutilizables y asegurar type safety en compile-time en proyectos TypeScript.

## Cuándo usarme / Triggering

- **Lógica de tipos compleja**: conditional types, `infer`, tipos distributivos y anidados (complex type inference logic)
- **Generics reutilizables**: funciones, componentes y constraints genéricos (reusable generic components; type-safe libraries/frameworks)
- **Mapped types**: transformación de tipos, key remapping y filtrado de propiedades
- **Template literal types**: tipos de string con patrón, manipulación y path building
- **Utility types**: `Partial`, `Required`, `Readonly`, `Pick`, `Omit`, `Record`, `Exclude`, `Extract`, `NonNullable`
- **Type-safe libraries/APIs**: clientes de API tipados (type-safe API clients), configuración fuertemente tipada (strongly-typed configuration), form validation y state management
- **Migración JavaScript → TypeScript**: adopción progresiva de type safety (migrating JS codebases)
- **Type testing**: `AssertEqual`, `ExpectError` y verificación de tipos en compile-time
- **Modernización TS 5.5+**: predicados de tipo inferidos, `isolatedDeclarations`, validación con arktype/valibot/zod v4, pattern matching con ts-pattern, efectos con effect-ts (ver `references/modern-typescript-2024-2026.md`)

**NO usar cuando**: la tarea sea sintaxis básica de TypeScript (tipos primitivos, interfaces simples) o desarrollo React/Next.js (frameworks fuera de alcance de esta skill).

## Referencias internas

- `references/core-concepts.md` — Conceptos fundamentales con código completo: generics, conditional types, mapped types, template literal types y utility types. Léelo cuando el resumen de este SKILL.md no baste.
- `references/details.md` — Ejemplos trabajados y patrones avanzados: type-safe event emitter, API client tipado, builder pattern, deep readonly/partial, form validation, discriminated unions y técnicas de inferencia (`infer`, type guards, assertion functions). Léelo cuando el resumen de este SKILL.md no baste para implementar el caso concreto.
- `references/modern-typescript-2024-2026.md` — Modernización 2024-26: TypeScript 5.5+ (predicados inferidos, `isolatedDeclarations`, `--build`/`--noCheck`), ts-pattern, effect-ts, arktype/valibot/zod v4 y typescript-eslint v8.

## Conceptos fundamentales

Conceptos esenciales con ejemplos de código: **Generics** (funciones reutilizables, constraints, múltiples parámetros de tipo), **Conditional types** (tipos basados en condiciones, extracción de return types, distributivos, anidados), **Mapped types** (transformación de propiedades, opcionales, key remapping, filtrado), **Template literal types** (strings con patrón, manipulación, path building) y **Utility types** (`Partial`, `Required`, `Readonly`, `Pick`, `Omit`, `Exclude`, `Extract`, `NonNullable`, `Record`).

> Ver [references/core-concepts.md](references/core-concepts.md) para el código completo de cada concepto.

## Ejemplos detallados y patrones

Las secciones detalladas (desde `## Patrones avanzados`) viven en `references/details.md`. Lee ese fichero cuando el resumen de navegación de arriba no baste.

## Buenas prácticas

1. **Usa** `unknown` **en vez de** `any`: fuerza el type checking
2. **Prefiere** `interface` **para formas de objeto**: mejores mensajes de error
3. **Usa** `type` **para uniones y tipos complejos**: más flexible
4. **Aprovecha la inferencia de tipos**: deja que TypeScript infiera cuando sea posible
5. **Crea tipos auxiliares**: construye utilidades de tipos reutilizables
6. **Usa const assertions**: preserva los tipos literales
7. **Evita las aserciones de tipo**: usa type guards en su lugar
8. **Documenta los tipos complejos**: añade comentarios JSDoc
9. **Usa el modo estricto**: activa todas las opciones estrictas del compilador
10. **Testea tus tipos**: usa tests de tipos para verificar el comportamiento
11. **Activa** `isolatedDeclarations`: declaraciones aisladas para builds más rápidos y compatibilidad con transpiladores (ver `references/modern-typescript-2024-2026.md`)
12. **Valida en runtime con esquemas**: zod v4, valibot o arktype en la frontera (APIs, formularios); no confíes solo en tipos de compile-time

## Test de tipos

```typescript
// Tests de aserción de tipos
type AssertEqual<T, U> = [T] extends [U]
  ? [U] extends [T]
    ? true
    : false
  : false;

type Test1 = AssertEqual<string, string>; // true
type Test2 = AssertEqual<string, number>; // false
type Test3 = AssertEqual<string | number, string>; // false

// Auxiliar para esperar error
type ExpectError<T extends never> = T;

// Ejemplo de uso
type ShouldError = ExpectError<AssertEqual<string, number>>;
```

## Errores comunes

1. **Abusar de** `any`: anula el propósito de TypeScript
2. **Ignorar strict null checks**: puede provocar errores en runtime
3. **Tipos demasiado complejos**: pueden ralentizar la compilación
4. **No usar discriminated unions**: se pierden oportunidades de narrowing
5. **Olvidar modificadores readonly**: permite mutaciones no deseadas
6. **Referencias circulares de tipos**: pueden causar errores del compilador
7. **No cubrir casos borde**: como arrays vacíos o valores null

## Consideraciones de rendimiento

- Evita conditional types profundamente anidados
- Usa tipos simples cuando sea posible
- Cachea los cómputos de tipos complejos
- Limita la profundidad de recursión en tipos recursivos
- Usa `--build` para builds incrementales y `--noCheck` (transpile-only) en desarrollo para saltar el type checking en producción/desarrollo rápido
- Mide con `tsc --extendedDiagnostics` y `typescript-eslint` v8 con type-aware lint solo donde aporte

## Uso

Tipado avanzado (generics, conditional types, `infer`, branded types, patrones de API tipada) ante tipos complejos, errores de inferencia o diseño de APIs tipadas. No usar para revisión de seguridad ni arquitectura general. Ver frontmatter `description`.

## Estructura

- `SKILL.md` — resumen, conceptos y buenas prácticas.
- `references/core-concepts.md` — código completo de cada concepto fundamental.
- `references/details.md` — ejemplos trabajados y patrones avanzados (event emitter, API client, builder, deep readonly/partial, validación, discriminated unions, `infer`).
- `references/modern-typescript-2024-2026.md` — tooling 2024-26: TS 5.5+, ts-pattern, effect-ts, arktype/valibot/zod v4, typescript-eslint v8.
- Sin `scripts/`, `configs/` ni `assets/` propios.

## Herramientas

Sin `scripts/` propios. Recursos versionados:

| Recurso                                     | Propósito                                  |
| ------------------------------------------- | ------------------------------------------ |
| `references/core-concepts.md`               | Código completo de conceptos fundamentales |
| `references/details.md`                     | Patrones avanzados y ejemplos trabajados   |
| `references/modern-typescript-2024-2026.md` | Modernización y tooling 2024-26            |

## Referencias

- `references/core-concepts.md`, `references/details.md` (leer cuando el resumen no baste).
- `references/modern-typescript-2024-2026.md` (tooling 2024-26).
- `disenar-arquitectura` — solo como frontera declarada (arquitectura general), no como enlace.
