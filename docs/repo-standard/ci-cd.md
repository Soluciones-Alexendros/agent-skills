# CI/CD — canon repo-standard

### Propósito de este documento

- **Objetivos:** Fijar el contrato de pipelines de la flota: workflows reutilizables (`workflow_call`), actions compuestas, rulesets de protección, Renovate agrupado y escaneo de secretos. Solo lectura: los andamios ejecutables viven en `operar-release/assets/` y `operar-release/actions/`.
- **Estructura:** Esta meta-sección → Orden de gates → Workflows reutilizables → Composite actions → Rulesets → Renovate/Dependabot → Verificación local.
- **Contenido a integrar según contexto:** En un producto, adaptar los comandos al stack (tabla de stacks) sin cambiar los nombres de jobs. Los SHA de pins se reverifican siempre antes de copiar.

## Orden de gates

```text
quality → test → [build] → smoke   (+ e2e opcional en webs)
```

- `quality`: format, lint, types, estructura, `actionlint`.
- `test`: unitarios/funcionales. Un script ausente debe fallar el job (nunca `--if-present` ni equivalentes que lo silencien).
- `build`: solo si hay artefacto. Produce el artefacto versionado que `smoke` y `release` consumen.
- `smoke`: health post-build (`/` o `/api/health`, binario `--help`/`version`, `make validate`).
- `integration`/`e2e`: declaran `needs` del job rápido y reinstalan el runtime (`needs` no arrastra el workspace).

Todo job lleva `timeout-minutes` (partida: lint 10, unit 15, integración 30) y `permissions:` explícito (defecto `contents: read`).

## Workflows reutilizables (`workflow_call`)

Los repos de producto no duplican lógica de CI: llaman a los workflows reutilizables versionados en `operar-release/assets/workflows/reusable/`:

| Reutilizable | Propósito | Entradas principales |
|---|---|---|
| `reusable-quality.yml` | `actionlint` + lint del stack | `stack: node\|python\|rust\|go`, `node-version` / `python-version` |
| `reusable-test.yml` | tests unitarios con caché por lockfile | `stack`, `lockfile-hash` implícito en la clave de caché |
| `reusable-smoke.yml` | health post-build | `smoke-command`, `artifact-name` |
| `reusable-release.yml` | verificar tag+changelog+manifiesto y crear la Release | `tag`, notas extraídas solo de `CHANGELOG.md` |

Ejemplo de llamada (producto Node):

```yaml
jobs:
  quality:
    uses: <org>/repo-standard/.github/workflows/reusable-quality.yml@vX.Y.Z  # pin a SHA antes de commitear
    with:
      stack: node
  test:
    needs: quality
    uses: <org>/repo-standard/.github/workflows/reusable-test.yml@vX.Y.Z
    with:
      stack: node
```

Reglas:

- El caller fija `permissions:` mínimos y `concurrency` por rama (`cancel-in-progress: true` en CI; en despliegue el grupo es el entorno y `cancel-in-progress: false`).
- Ningún caller interpola entradas no confiables en `run:`: se pasan por `env:` y se validan (ver `security.md`).
- Los workflows finos (`ci.yml`, `workflow-lint.yml`) que quedan en `operar-release/assets/workflows/` son andamios de ejemplo por stack, no el contrato: el contrato son los reutilizables.

## Composite actions (`operar-release/actions/`)

| Action | Qué hace |
|---|---|
| `setup-node/` (`action.yml`) | `actions/setup-node` pineado + caché npm + lectura de `.nvmrc` |
| `actionlint/` (`action.yml`) | Descarga el binario de la release fijada, verifica SHA-256 y ejecuta `actionlint -color` |
| `secret-scan/` (`action.yml`) | Ejecuta `gitleaks` con `fetch-depth: 0`, comentarios solo en `pull_request`, sin subir SARIF |

Toda action compuesta fija sus `uses:` internos con SHA completo + comentario de versión, y se consume también pineada a SHA.

## Rulesets (contrato versionado, lo aplica un humano)

El agente no cambia rulesets ni protección de `main`: informa y deja el paso manual. Contrato de referencia en `operar-release/assets/ruleset.json`:

- PR obligatorio; reviews: repo de un solo owner → 0 approvals + checks; con equipo → ≥1 o code owners.
- Required checks: `quality`, `test`, `smoke` (+ `build` solo si el job existe; + `e2e` si es web P1). Nunca marcar required un check que el workflow no define.
- Conversaciones resueltas, historia lineal, sin bypass, sin force-push.
- Auto-merge ON, auto-delete head branches ON. Automerge humano solo con label `automerge`.
- No desactivar secret scanning / push protection de la org.

## Renovate agrupado (único bot de version-updates)

- Dependabot `version-updates` prohibido (eliminar el bloque en el mismo PR que añade Renovate). Dependabot Alerts de seguridad pueden quedar ON.
- Base en `operar-release/references/dependabot-grouped.md`: schedule de madrugada `Europe/Madrid`, automerge `patch`+`minor`, minors agrupados con label `dependencies`, majors solo con revisión humana.
- Prerrequisito humano: la GitHub App Renovate instalada en la org o habilitada en el repo; sin ella el JSON no genera PRs.
- Pins de Actions (`package-ecosystem: github-actions` o Renovate `github-actions`) se actualizan en PRs revisables, manteniendo SHA completo + comentario de versión.

## Stacks (los jobs se llaman igual; los comandos no)

| Stack | Setup | Comprobación mínima |
|---|---|---|
| Node | `actions/setup-node` con `.nvmrc` o `node-version`, `cache: npm` | `npm ci` + scripts declarados (`lint`, `test`, `build`) |
| Python | `actions/setup-python` | Instalar desde el lockfile (`uv.lock`, `poetry.lock`, `requirements.txt` pineado) |
| Rust | toolchain fijada (`rust-toolchain.toml` o acción pineada) | `cargo test --locked` |
| Go | `actions/setup-go` | `go test ./...` con `go.sum` presente |

Preferir la caché integrada del setup oficial a `actions/cache` manual. Si hace falta caché manual, la clave incluye el hash del lockfile. No cachear `~/.aws`, `~/.ssh` ni tokens.

## Verificación local

```bash
actionlint -color
bash run-validation.sh
```

El mismo `actionlint` pineado que en CI debe poder correr en local (ver `operar-release/actions/actionlint/`). Documentar el comando en CONTRIBUTING o README si el repo ya tiene esa guía; no crear CONTRIBUTING solo para alojarlo.
