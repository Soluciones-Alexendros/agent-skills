---
name: verificar-hooks
description: >-
  Configura y ejecuta hooks git locales (Husky, lint-staged, Prettier, typecheck,
  tests en pre-commit; e2e en pre-push si existe). Usar cuando el operador pida
  pre-commit hooks, husky, lint-staged o el gate local de un cierre de trabajo.
  No usar para CI de GitHub (→ operar-release).
license: MIT
metadata:
  author: Soluciones-Alexendros
  version: "3.2.0"
  dominio: verificar
  tipo: atomic
  idioma: es
---

# verificar-hooks — Configuración de hooks locales

## Propósito

Configurar en el repositorio actual los pre-commit hooks con Husky, lint-staged y Prettier, y añadir typecheck y tests al hook para que cada commit pase por formateo, tipos y pruebas.

## Cuándo usar

Cuando se pida añadir pre-commit hooks, configurar Husky, lint-staged o Prettier, ejecutar formateo/typecheck/tests al commitear, o correr el gate local en un cierre de trabajo (`operar-release` G).

## Procedimiento

### 1. Detectar el gestor de paquetes

Buscar `package-lock.json` (npm), `pnpm-lock.yaml` (pnpm), `yarn.lock` (yarn) o `bun.lockb` (bun). Usar el que esté presente; por defecto npm.

### 2. Instalar dependencias

Instalar como devDependencies: `husky lint-staged prettier`.

### 3. Inicializar Husky

```bash
npx husky init
```

Crea `.husky/` y añade `prepare: "husky"` a package.json.

### 4. Crear `.husky/pre-commit`

Husky v9+ no necesita shebang:

```
npx lint-staged
npm run typecheck
npm run test
```

Sustituir `npm` por el gestor detectado. Si package.json no tiene `typecheck` o `test`, omitir esas líneas y avisar.

### 5. Crear `.lintstagedrc`

```json
{
  "*": "prettier --ignore-unknown --write"
}
```

### 6. Crear `.prettierrc` (si falta)

```json
{
  "useTabs": false,
  "tabWidth": 2,
  "printWidth": 80,
  "singleQuote": false,
  "trailingComma": "es5",
  "semi": true,
  "arrowParens": "always"
}
```

### 7. Verificar

- `.husky/pre-commit` existe y es ejecutable
- `.lintstagedrc` existe
- El script `prepare` de package.json es `"husky"`
- Existe configuración de Prettier
- `npx lint-staged` funciona

### 8. Commit (solo modo instalar)

Añadir los ficheros creados y commitear con: `Add pre-commit hooks (husky + lint-staged + prettier)`. El commit pasa por los nuevos hooks.

### 9. pre-push con e2e (si el repo ya lo tiene)

Si `package.json` declara `e2e`, `test:e2e` o un script que invoca Playwright, crear `.husky/pre-push` que ejecute ese script con el gestor detectado. El pre-commit sigue siendo rápido (lint-staged, typecheck, unit). El e2e largo no entra en pre-commit.

### 10. Modo gate (ejecutar)

Cuando `operar-release` G (cierre de trabajo) o el operador pida validar el PR en local:

1. Si falta `.husky/pre-commit`, correr los pasos 1–7 (instalar) y luego este modo.
2. En cada head del plan, con el árbol a commitear o ya commiteado:
   - `npx lint-staged` (o el hook `.husky/pre-commit` entero).
   - Script `typecheck` si existe.
   - Script `test` si existe.
   - Script e2e/Playwright si existe (paso 9 o invocación directa).
3. Rojo → corregir en esa rama y repetir. Verde → devolver el control a `operar-release` G.

## Herramientas

| Script                      | Propósito                                                                   |
| --------------------------- | --------------------------------------------------------------------------- |
| `scripts/gate-husky.sh`     | Modo gate: instala hooks si faltan y ejecuta lint-staged, typecheck y tests |
| `scripts/tests/smoke_sh.sh` | Smoke test del gate sobre un repo temporal mínimo                           |

## Casos límite

- Husky v9+ no necesita shebangs en los hooks.
- `prettier --ignore-unknown` omite ficheros que Prettier no procesa.
- El pre-commit ejecuta primero lint-staged (solo staged), luego typecheck y tests.
- El e2e Playwright del cierre de trabajo se corre en modo gate o en pre-push; el procedimiento de UI está en `webapp-testing` (catálogo compartido).

## Referencias

- Recurso auxiliar: `references/agents-openai.yaml` (metadatos de interfaz; consultar al registrar).
- Canon de commits: [commitlint.config.cjs](../../docs/repo-standard/templates/commitlint.config.cjs).
- CI de GitHub y cierre de trabajo → `operar-release`.
