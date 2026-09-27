# TypeScript moderno: tooling 2024-26

Modernización de la skill a TypeScript 5.5+ y ecosistema 2024-26. Complementa a `core-concepts.md` y `details.md` (fundamentos estables) con lo que cambió en el tooling reciente.

## TypeScript 5.5+: predicados de tipo inferidos

Desde TS 5.5 el compilador **infiere predicados de tipo** (`value is T`) en funciones con retorno booleano simple, sin anotación explícita:

```typescript
// Antes (anotación manual obligatoria para narrowing):
function isString(value: unknown): value is string {
  return typeof value === "string";
}

// TS 5.5+: el predicado se infiere en casos simples —
// `filter` estrecha sin anotar:
const mixed: unknown[] = ["a", 1, "b"];
const strings = mixed.filter((v) => typeof v === "string");
// Type: string[] (inferido)
```

Regla práctica: sigue anotando `value is T` en guards públicos de librería (documenta el contrato); confía en la inferencia dentro de funciones locales y callbacks.

## TypeScript 5.5+: `isolatedDeclarations`

`isolatedDeclarations` (estable desde 5.5) obliga a anotar los tipos exportados para que cada fichero sea transpilable de forma aislada (compatible con transpiladores rápidos como esbuild/swc y con `--isolatedModules`):

```jsonc
// tsconfig.json
{
  "compilerOptions": {
    "isolatedDeclarations": true,
    "isolatedModules": true,
    "verbatimModuleSyntax": true
  }
}
```

```typescript
// Con isolatedDeclarations: el tipo de retorno exportado debe ser explícito
export function getUser(id: string): User {
  return { id, name: "John" };
}
```

Cuándo activarlo: librerías publicadas y monorepos con builds distribuidos. Coste: más anotaciones explícitas en la superficie exportada; a cambio, builds incrementales fiables y errores de tipos de transpilación detectados en `tsc`.

## Builds: `--build` y `--noCheck`

- **`tsc --build` (`tsc -b`)**: modo proyecto con builds incrementales y referencias entre proyectos (`references` en `tsconfig.json`). Es la vía recomendada en monorepos: solo recompila lo cambiado y ordena los proyectos por dependencia.
- **`--noCheck`** (tsc 5.5+, también en transpiladores): omite el type checking y solo transpila. Útil en desarrollo/HMR y en CI para separar "compilar" de "verificar tipos":
  ```bash
  tsc --noCheck -p tsconfig.build.json   # transpile-only, rápido
  tsc --noEmit -p tsconfig.json          # verificación de tipos aparte
  ```
- Diagnóstico: `tsc --extendedDiagnostics` para localizar cuellos de botella (tipos lentos, normalmente conditional types recursivos — ver «Consideraciones de rendimiento» en SKILL.md).

## Pattern matching: ts-pattern

[ts-pattern](https://github.com/gvergnaud/ts-pattern) aporta matching exhaustivo sobre uniones, complementando a las discriminated unions de `details.md`:

```typescript
import { match } from "ts-pattern";

type State =
  | { type: "idle" }
  | { type: "fetching"; requestId: string }
  | { type: "success"; data: unknown }
  | { type: "error"; error: Error };

declare const state: State;

const text = match(state)
  .with({ type: "idle" }, () => "En espera")
  .with({ type: "fetching" }, ({ requestId }) => `Pidiendo ${requestId}…`)
  .with({ type: "success" }, ({ data }) => `OK: ${JSON.stringify(data)}`)
  .with({ type: "error" }, ({ error }) => `Fallo: ${error.message}`)
  .exhaustive(); // error de compilación si falta un caso
```

`.exhaustive()` convierte los casos olvidados en errores de compile-time: es el `switch` de `details.md` con garantía de exhaustividad.

## Efectos y errores tipados: effect-ts

[Effect](https://effect.website/) (effect-ts) tipa dependencias, errores y contexto en la firma, alternativa a lanzar excepciones sin tipar:

```typescript
import { Effect } from "effect";

class DbDown {
  readonly _tag = "DbDown";
}

declare const findUser: (id: string) => Effect.Effect<User, DbDown>;

// El error DbDown es visible en el tipo; se fuerza su tratamiento:
const program = Effect.map(findUser("1"), (u) => u.name);
const runnable = Effect.catchTag(program, "DbDown", () => Effect.succeed("invitado"));
```

Úsalo cuando el flujo tenga errores recuperables múltiples o dependencias inyectables; para scripts lineales, `try/catch` con tipos estrechados sigue bastando.

## Validación en runtime: arktype / valibot / zod v4

Los tipos desaparecen en runtime: valida la frontera (APIs, formularios, env) con esquemas que **derivan el tipo estático**:

```typescript
import { z } from "zod"; // v4: más rápido, API compatible en lo esencial

const UserSchema = z.object({
  id: z.string(),
  name: z.string(),
  age: z.number().int().nonnegative().optional(),
});

type User = z.infer<typeof UserSchema>;

// En la frontera: parsea, no castees
const user: User = UserSchema.parse(rawJson);
```

Alternativas 2024-26:

| Librería | Cuándo preferirla |
|---|---|
| **zod v4** | Ecosistema mayor (formularios, tRPC, OpenAPI); migración v3→v4 mayormente compatible |
| **valibot** | Bundle mínimo por diseño modular (tree-shakeable); misma filosofía `v.infer` |
| **arktype** | Sintaxis compacta orientada a tipos (`type("string>5")`); inferencia nativa TS |

Regla: **una sola** librería de esquemas por proyecto; el tipo canónico se deriva del esquema (`z.infer`), nunca duplicado a mano.

## Lint con tipos: typescript-eslint v8

[typescript-eslint](https://typescript-eslint.io/) v8 (2024): flat config obligatoria, reglas type-aware estables y soporte de las últimas versiones de TS y ESLint 9:

```js
// eslint.config.mjs (flat config)
import tseslint from "typescript-eslint";

export default tseslint.config(
  ...tseslint.configs.recommendedTypeChecked, // reglas con type checking
  {
    languageOptions: {
      parserOptions: {
        projectService: true, // sin listar tsconfigs a mano
        tsconfigRootDir: import.meta.dirname,
      },
    },
  },
);
```

Consejos:

- Activa `recommendedTypeChecked` solo en paquetes donde el type-aware lint aporte (código de dominio); en scripts efímeros basta `recommended`.
- Reglas clave de esta skill: `@typescript-eslint/no-explicit-any`, `no-unsafe-*`, `consistent-type-imports`, `no-unnecessary-type-assertion`.
- `projectService: true` sustituye a `project: [...]` y acelera el arranque en monorepos.

## Matriz de adopción rápida

| Necesidad | Opción 2024-26 | Alternativa estable |
|---|---|---|
| Exhaustividad en uniones | ts-pattern `.exhaustive()` | `switch` + `assertNever` |
| Errores tipados / DI | effect-ts | `try/catch` + guards |
| Validación frontera API/forms | zod v4 | valibot / arktype |
| Lint con tipos | typescript-eslint v8 flat + `projectService` | `recommended` sin tipos |
| Build monorepo incremental | `tsc --build` + `isolatedDeclarations` | `tsc -p` clásico |
