---
name: repo-precommit
description: >-
  Configura hooks git locales (Husky, lint-staged, Prettier, typecheck, tests en
  pre-commit). Usar al pedir pre-commit hooks, husky o lint-staged. No usar para
  CI de GitHub (→ repo-ending).
license: MIT
metadata:
  author: Soluciones-Alexendros
  version: "1.0.0"
  dominio: repo
  idioma: es

---
# Repo Pre-commit — Configuración de hooks locales

> Nota de formato: títulos normalizados a ES 2026-09-26 (`Qué configura`, `Pasos`, `Notas`); el cuerpo conserva términos técnicos EN (Husky, lint-staged, Prettier). Secciones estándar `Uso`, `Estructura`, `Herramientas` y `Referencias` al final.

## Qué hace / Propósito

Configura en el repositorio actual los pre-commit hooks con Husky, lint-staged y Prettier, y añade typecheck y tests al hook. Sirve para que cada commit pase por formateo, verificación de tipos y pruebas antes de quedar registrado.

## Cuándo usarme / Triggering

- Cuando se pida añadir pre-commit hooks o configurar Husky en el repositorio actual.
- Cuando se quiera configurar lint-staged o Prettier para los commits.
- Cuando se pida ejecutar formateo, typechecking o tests automáticamente al commitear.
- Frases como "setup pre-commit", "husky hooks" o "formatea antes de commit".
- **NO usar cuando**: el objetivo no sea el setup de Husky/lint-staged, sino operaciones Git generales (ramas, merges, rebases, conflictos) u otros linters sin hooks.

## Referencias internas

El contenido operativo vive íntegro en este SKILL.md. El único recurso auxiliar es `references/agents-openai.yaml` — metadatos de interfaz (nombre visible y descripción corta); consúltalo solo al publicar o registrar la skill.

## Qué configura

- **Husky** pre-commit hook
- **lint-staged** running Prettier on all staged files
- **Prettier** config (if missing)
- **typecheck** and **test** scripts in the pre-commit hook

## Pasos

### 1. Detectar el gestor de paquetes

Check for `package-lock.json` _(ejemplo: fichero del proyecto)_ (npm), `pnpm-lock.yaml` _(ejemplo)_ (pnpm), `yarn.lock` (yarn), `bun.lockb` (bun). Use whichever is present. Default to npm if unclear.

### 2. Instalar dependencias

Install as devDependencies:

```
husky lint-staged prettier
```

### 3. Inicializar Husky

```bash
npx husky init
```

This creates `.husky/` dir and adds `prepare: "husky"` to package.json.

### 4. Crear `.husky/pre-commit`

Write this file (no shebang needed for Husky v9+):

```
npx lint-staged
npm run typecheck
npm run test
```

**Adapt**: Replace `npm` with detected package manager. If repo has no `typecheck` or `test` script in package.json, omit those lines and tell the user.

### 5. Crear `.lintstagedrc`

```json
{
  "*": "prettier --ignore-unknown --write"
}
```

### 6. Crear `.prettierrc` (si falta)

Only create if no Prettier config exists. Use these defaults:

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

- [ ] `.husky/pre-commit` exists and is executable
- [ ] `.lintstagedrc` exists
- [ ] `prepare` script in package.json is `"husky"`
- [ ] `prettier` config exists
- [ ] Run `npx lint-staged` to verify it works

### 8. Commit

Stage all changed/created files and commit with message: `Add pre-commit hooks (husky + lint-staged + prettier)`

This will run through the new pre-commit hooks — a good smoke test that everything works.

## Notas

- Husky v9+ doesn't need shebangs in hook files
- `prettier --ignore-unknown` skips files Prettier can't parse (images, etc.)
- The pre-commit runs lint-staged first (fast, staged-only), then full typecheck and tests

## Uso

Configurar hooks git locales (Husky, lint-staged, typecheck, tests en pre-commit) ante «pre-commit hooks», «husky» o «lint-staged». No usar para CI de GitHub (ver `repo-ending`, skill existente fuera de ámbito). Ver frontmatter `description`.

## Estructura

- `SKILL.md` — procedimiento completo (Pasos 1–8) y verificaciones.
- `references/agents-openai.yaml` — metadatos de interfaz (nombre visible y descripción corta); consultar solo al publicar/registrar.
- Sin `references/`, `scripts/` ni `configs/` propios; artefactos `.husky/`, `.lintstagedrc`, `.prettierrc` son generados en el repo destino _(ejemplos)_, no fuentes versionadas.

## Herramientas

Sin `scripts/` propios. Herramientas externas invocadas:

| Herramienta | Propósito |
|---|---|
| Husky | Hook pre-commit |
| lint-staged + Prettier | Formateo de staged files |
| `npm run typecheck` / `npm run test` | Verificación y tests del repo destino |

## Referencias

- Pasos y Notas en este `SKILL.md` (referencia operativa).
- Recurso auxiliar: `references/agents-openai.yaml`.
- Producto distinto: `repo-ending` (CI de GitHub), fuera de ámbito.
