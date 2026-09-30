---
name: verificar-hooks
description: >-
  Configura hooks git locales (Husky, lint-staged, Prettier, typecheck, tests en
  pre-commit). Usar al pedir pre-commit hooks, husky o lint-staged. No usar para
  CI de GitHub (→ operar-release).
license: MIT
metadata:
  author: Soluciones-Alexendros
  version: "3.1.0"
  dominio: verificar
  tipo: atomic
  idioma: es
---

# verificar-hooks — Configuración de hooks locales

> Alcance: hooks git locales (Husky, lint-staged, Prettier). La CI de GitHub vive en `operar-release` y el canon en [docs/repo-standard](../../docs/repo-standard/structure.md). Secciones estándar `Uso`, `Estructura`, `Herramientas` y `Referencias` al final.

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

- Hook pre-commit con **Husky**
- **lint-staged** con Prettier sobre los ficheros staged
- Configuración de **Prettier** (si falta)
- Scripts **typecheck** y **test** dentro del hook pre-commit

## Pasos

### 1. Detectar el gestor de paquetes

Buscar `package-lock.json` (npm), `pnpm-lock.yaml` (pnpm), `yarn.lock` (yarn) o `bun.lockb` (bun). Usar el que esté presente; por defecto npm si no está claro.

### 2. Instalar dependencias

Instalar como devDependencies:

```
husky lint-staged prettier
```

### 3. Inicializar Husky

```bash
npx husky init
```

Crea el directorio `.husky/` y añade `prepare: "husky"` a package.json.

### 4. Crear `.husky/pre-commit`

Escribir este fichero (sin shebang en Husky v9+):

```
npx lint-staged
npm run typecheck
npm run test
```

**Adaptación**: sustituir `npm` por el gestor detectado. Si package.json no tiene script `typecheck` o `test`, omitir esas líneas y avisar al usuario.

### 5. Crear `.lintstagedrc`

```json
{
  "*": "prettier --ignore-unknown --write"
}
```

### 6. Crear `.prettierrc` (si falta)

Solo crear si no existe configuración de Prettier. Valores por defecto:

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

- [ ] `.husky/pre-commit` existe y es ejecutable
- [ ] `.lintstagedrc` existe
- [ ] El script `prepare` de package.json es `"husky"`
- [ ] Existe configuración de `prettier`
- [ ] Ejecutar `npx lint-staged` para comprobar que funciona

### 8. Commit

Añadir al stage los ficheros creados/modificados y commitear con el mensaje: `Add pre-commit hooks (husky + lint-staged + prettier)`

El commit pasará por los nuevos hooks: sirve como prueba de que todo funciona.

## Notas

- Husky v9+ no necesita shebangs en los ficheros de hook
- `prettier --ignore-unknown` omite ficheros que Prettier no puede procesar (imágenes, etc.)
- El pre-commit ejecuta primero lint-staged (rápido, solo staged), luego typecheck y tests completos

## Uso

Configurar hooks git locales (Husky, lint-staged, typecheck, tests en pre-commit) ante «pre-commit hooks», «husky» o «lint-staged». No usar para CI de GitHub (ver `operar-release`). Ver frontmatter `description`.

## Estructura

- `SKILL.md` — procedimiento completo (Pasos 1–8) y verificaciones.
- `references/agents-openai.yaml` — metadatos de interfaz (nombre visible y descripción corta); consultar solo al publicar/registrar.
- Sin `references/`, `scripts/` ni `configs/` propios; artefactos `.husky/`, `.lintstagedrc`, `.prettierrc` son generados en el repo destino _(ejemplos)_, no fuentes versionadas.

## Herramientas

Sin `scripts/` propios. Herramientas externas invocadas:

| Herramienta                          | Propósito                             |
| ------------------------------------ | ------------------------------------- |
| Husky                                | Hook pre-commit                       |
| lint-staged + Prettier               | Formateo de staged files              |
| `npm run typecheck` / `npm run test` | Verificación y tests del repo destino |

## Referencias

- Pasos y Notas en este `SKILL.md` (referencia operativa).
- Recurso auxiliar: `references/agents-openai.yaml`.
- Canon de commits: [commitlint.config.cjs](../../docs/repo-standard/templates/commitlint.config.cjs).
- Producto distinto: `operar-release` (CI de GitHub), fuera de ámbito.
