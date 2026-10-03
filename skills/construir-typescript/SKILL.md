---
name: construir-typescript
description: >-
  Tipado avanzado de TypeScript: generics, conditional types, infer, branded types y
  patrones de API tipada. Usar cuando haya tipos complejos, errores de inferencia
  difíciles o diseño de APIs tipadas. No usar para revisión de seguridad (→
  verificar-owasp) ni arquitectura general (→ disenar-arquitectura).
license: MIT
metadata:
  author: Soluciones-Alexendros
  version: "2.1.1"
  dominio: construir
  tipo: tecnologia
  idioma: es
---

# TypeScript: tipos avanzados

## Propósito

Dominar el sistema de tipos avanzado de TypeScript (generics, conditional types, mapped types, template literals y utility types) para construir aplicaciones type-safe (TypeScript 5.5+).

## Cuándo usar

Lógica de tipos compleja (`infer`, distributivos), generics reutilizables, mapped types, template literal types, utility types, clientes de API tipados, migración JS→TS, tests de tipos y modernización TS 5.5+.

## Procedimiento

1. Leer `references/core-concepts.md` cuando el resumen no baste: generics, conditional types, mapped types, template literals, utility types.
2. Leer `references/details.md` para patrones: event emitter, API client, builder, deep readonly/partial, validación, discriminated unions, `infer`.
3. Leer `references/modern-typescript-2024-2026.md` para TS 5.5+, ts-pattern, effect-ts, arktype/valibot/zod v4, typescript-eslint v8.

Buenas prácticas: `unknown` en vez de `any`; `interface` para formas de objeto; `type` para uniones; inferencia antes que anotación; type guards antes que aserciones; modo estricto; tests de tipos; `isolatedDeclarations`; validación runtime en la frontera.

## Formato de salida

Tests de aserción de tipos:

```typescript
type AssertEqual<T, U> = [T] extends [U]
  ? [U] extends [T]
    ? true
    : false
  : false;
type ExpectError<T extends never> = T;
```

## Casos límite

Abusar de `any`, ignorar strict null checks, tipos demasiado anidados (ralentizan `tsc`), referencias circulares, no cubrir arrays vacíos o null. Medir con `tsc --extendedDiagnostics`.

## Referencias

- `references/core-concepts.md`, `references/details.md`, `references/modern-typescript-2024-2026.md`.
- Arquitectura general → `disenar-arquitectura`. Seguridad de código → `verificar-owasp`.
