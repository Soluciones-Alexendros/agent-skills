---
name: typescript-avanzado
description: >-
  Tipado avanzado de TypeScript: generics, conditional types, infer, branded types y
  patrones de API tipada. Usar ante tipos complejos, errores de inferencia difíciles o
  diseño de APIs tipadas. No usar para revisión de seguridad ni arquitectura general.
license: MIT
metadata:
  author: Soluciones-Alexendros
  version: "0.2.0"
  dominio: codigo
  idioma: es

---
# TypeScript Advanced Types

> Nota de formato: sección `Cuándo usarme`/`When to Use` fusionada 2026-09-26 en una única sección ES (`Cuándo usarme / Triggering`, con equivalencias EN entre paréntesis); se conservan las secciones estándar `Uso`, `Estructura`, `Herramientas` y `Referencias`.

Comprehensive guidance for mastering TypeScript's advanced type system including generics, conditional types, mapped types, template literal types, and utility types for building robust, type-safe applications.

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

**NO usar cuando**: la tarea sea sintaxis básica de TypeScript (tipos primitivos, interfaces simples) o desarrollo React/Next.js; para Next.js usar `web-nextjs` _(pendiente: skill no existente en este repo; texto plano, no enlace)_.

## Referencias internas

- `references/details.md` — Ejemplos trabajados y patrones avanzados: type-safe event emitter, API client tipado, builder pattern, deep readonly/partial, form validation, discriminated unions y técnicas de inferencia (`infer`, type guards, assertion functions). Léelo cuando el resumen de este SKILL.md no baste para implementar el caso concreto.



## Core Concepts

Conceptos fundamentales con ejemplos de código: **Generics** (funciones reutilizables, constraints, múltiples parámetros de tipo), **Conditional Types** (tipos basados en condiciones, extracción de return types, distributivos, anidados), **Mapped Types** (transformación de propiedades, optional, key remapping, filtrado), **Template Literal Types** (strings con patrón, manipulación, path building) y **Utility Types** (`Partial`, `Required`, `Readonly`, `Pick`, `Omit`, `Exclude`, `Extract`, `NonNullable`, `Record`).

> Ver [references/core-concepts.md](references/core-concepts.md) para el código completo de cada concepto.

## Detailed worked examples and patterns

Detailed sections (starting with `## Advanced Patterns`) live in `references/details.md`. Read that file when the navigation summary above is insufficient.

## Best Practices

1. **Use** `unknown` **over** `any`: Enforce type checking
2. **Prefer** `interface` **for object shapes**: Better error messages
3. **Use** `type` **for unions and complex types**: More flexible
4. **Leverage type inference**: Let TypeScript infer when possible
5. **Create helper types**: Build reusable type utilities
6. **Use const assertions**: Preserve literal types
7. **Avoid type assertions**: Use type guards instead
8. **Document complex types**: Add JSDoc comments
9. **Use strict mode**: Enable all strict compiler options
10. **Test your types**: Use type tests to verify type behavior



## Type Testing

```typescript
// Type assertion tests
type AssertEqual<T, U> = [T] extends [U]
  ? [U] extends [T]
    ? true
    : false
  : false;

type Test1 = AssertEqual<string, string>; // true
type Test2 = AssertEqual<string, number>; // false
type Test3 = AssertEqual<string | number, string>; // false

// Expect error helper
type ExpectError<T extends never> = T;

// Example usage
type ShouldError = ExpectError<AssertEqual<string, number>>;
```



## Common Pitfalls

1. **Over-using** `any`: Defeats the purpose of TypeScript
2. **Ignoring strict null checks**: Can lead to runtime errors
3. **Too complex types**: Can slow down compilation
4. **Not using discriminated unions**: Misses type narrowing opportunities
5. **Forgetting readonly modifiers**: Allows unintended mutations
6. **Circular type references**: Can cause compiler errors
7. **Not handling edge cases**: Like empty arrays or null values



## Performance Considerations

- Avoid deeply nested conditional types
- Use simple types when possible
- Cache complex type computations
- Limit recursion depth in recursive types
- Use build tools to skip type checking in production

## Uso

Tipado avanzado (generics, conditional types, `infer`, branded types, patrones de API tipada) ante tipos complejos, errores de inferencia o diseño de APIs tipadas. No usar para revisión de seguridad ni arquitectura general. Ver frontmatter `description`.

## Estructura

- `SKILL.md` — resumen, conceptos y buenas prácticas.
- `references/details.md` — ejemplos trabajados y patrones avanzados (event emitter, API client, builder, deep readonly/partial, validación, discriminated unions, `infer`).
- Sin `scripts/`, `configs/` ni `assets/` propios.

## Herramientas

Sin `scripts/` propios. Recurso versionado:

| Recurso | Propósito |
|---|---|
| `references/details.md` | Patrones avanzados y ejemplos trabajados |

## Referencias

- `references/details.md` (leer cuando el resumen no baste).
- `web-nextjs` _(pendiente: no existe en este repo)_ — solo como frontera declarada, no como enlace.
