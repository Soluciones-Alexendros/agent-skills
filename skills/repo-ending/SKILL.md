---
name: repo-ending
description: >
  Cierra o audita un repositorio de GitHub cuando el usuario pide cerrar el repo,
  preparar una release, publicar una versión, dejarlo listo para producción,
  un health check, o una auditoría de CI/CD, labels, changelog o seguridad de
  workflows. También ante semantic versioning, Keep a Changelog, supply-chain
  de Actions, immutable releases o SLSA en ese cierre. Tras remediación, incluye
  abrir PR draft, monitorizar checks y mergear cuando estén verdes. No aplica a
  implementar features de producto genéricas ni a forjas que no sean github.com.
license: MIT
metadata:
  author: Soluciones-Alexendros
  version: "0.1.0"
  dominio: repo
  idioma: es

---

# repo-ending

Actúa como ingeniero de plataforma. Adapta la ceremonia al tamaño, al stack y al riesgo. Un repo pequeño no recibe un proceso enterprise. La línea mínima de seguridad no se negocia.

Invocación explícita: `/repo-ending`. No uses esta skill para implementar código de producto ajeno al cierre, ni para forjas que no sean GitHub.

Lee solo el recurso de la fase en curso. No abras todas las referencias a la vez.

## Reglas duras

- No inventes versiones, tags, SHAs, licencias ni rutas de documentación. Si no puedes verificarlo, márcalo `[PENDIENTE]` y pídelo. No publiques con `[PENDIENTE]` abierto en un ítem que bloquea.
- Antes de citar SemVer, Conventional Commits, Keep a Changelog o una política de Actions, abre la fuente oficial listada abajo. Si la URL ya no responde, dilo y no cites de memoria.
- Idioma del informe: el del usuario. Labels, workflows, commits y nombres de checks, en inglés técnico.
- La auditoría es de solo lectura y sigue sola. Cualquier mutación espera un sí explícito, de una en una — **excepto** el bucle merge-watch una vez el usuario autorizó la remediación o el PR de cierre (ver Fase F).
- Nunca hagas commit de un `uses:` sin SHA completo de 40 hex, ni del placeholder de pin, ni de `@v*`, `@main` o `@master`.
- Los SHA de `assets/workflows/` se verificaron el 2026-09-23. Antes de copiarlos a un repo, repite el procedimiento de `references/actions-security.md`. Si no cuadra, no reutilices el pin.

Fuentes a contrastar:

- SemVer 2.0.0: https://semver.org/spec/v2.0.0.html
- Conventional Commits 1.0.0: https://www.conventionalcommits.org/en/v1.0.0/
- Keep a Changelog 1.1.0: https://keepachangelog.com/en/1.1.0/
- Actions secure use: https://docs.github.com/en/actions/reference/security/secure-use
- Política de SHA pinning: https://github.blog/changelog/2025-08-15-github-actions-policy-now-supports-blocking-and-sha-pinning-actions/
- Immutable releases: https://docs.github.com/en/code-security/concepts/supply-chain-security/immutable-releases

## Arranque

1. Confirma el remoto. Solo sigue si `git remote get-url origin` apunta a `github.com`. Si es otra forja, detente y dilo. No uses `gh` contra un host que no sea GitHub.
2. Confirma `gh auth status`. Si falla, detente. No llames a la API con un token pegado en el shell.
3. Declara el modo: **auditoría** (informe, sin cambios), **remediación** (sí a fixes + merge-watch), o **cierre con publicación** (release/tag; añade bloqueos de versionado).

## Confirmación antes de mutar

Solo lectura, sin preguntar: `gh label list`, `gh run list`, `gh run view`, `gh api` GET, lectura de tags, workflows, manifiestos y documentación.

Exigen diff y un sí, una acción cada vez: crear, renombrar o borrar labels; `git tag`; `gh release create`; editar rulesets o branch protection; rotar secretos.

Un sí a **remediación de pipeline/docs de cierre** autoriza en bloque: commits en rama de remediación, push, PR draft, y **Fase F (merge-watch hasta merge)**. No autoriza tags ni borrar labels.

Responde con:

1. **Acción** — una frase con el comando y el objetivo.
2. **Impacto** — qué se rompe si el cambio está mal.
3. **Recuperación** — cómo deshacerlo, si se puede.
4. **¿Sigo? (sí / no)**

Un sí para la release no autoriza borrar labels, ni al revés.

## Gate proporcional

Recorre `assets/checklist-readiness.md`. Estados del informe: `OK`, `WARN`, `BLOCK`, `N/A`.

**Bloquea siempre**

- Secreto en el árbol o en el historial reciente que el escaneo señale.
- `uses:` de terceros (y, en repo crítico, también `actions/*` y `github/*`) sin SHA completo verificado.
- Workflow sin `permissions:` explícito.
- Job sin `timeout-minutes`.
- Entrada no confiable interpolada en `run:` o en `github-script`.
- `pull_request_target` o `workflow_run` que haga checkout y ejecute código no confiable.

**Bloquea solo si el modo es publicación**

- Tag, `CHANGELOG.md` y manifiesto de versión no coinciden, o no hay manifiesto verificable.
- Breaking change sin marcar en el changelog o sin bump MAJOR.
- Sección de la versión marcada `[YANKED]`, o reutilización de un número ya publicado.

**Aviso, no bloqueo**, salvo que el repo sea crítico (público con consumidores externos, despliega a producción, o el usuario lo declara crítico):

- Taxonomía de labels, issues sin mapear, CODEOWNERS, CONTRIBUTING.
- Tests de integración que el proyecto no tiene.
- SLSA, cosign o attestations.
- Estrategia de despliegue cuando el repo no despliega.

Un `WARN` lleva justificación en el informe. Un `BLOCK` impide el cierre: lista de bloqueos por severidad, cada uno con remediación. Solo con la línea mínima en verde emite el informe de `assets/checklist-readiness.md`.

## Fase A — Labels

1. Inventaría con `gh label list`. Busca duplicados, huérfanos y solapes.
2. Propón el mapeo con `assets/labels.json`. Adapta el eje `area` al dominio. Los labels de `preserve_unless_mapped` se quedan si no hay alias.
3. Muestra el diff de renombres y borrados. No ejecutes `gh label` hasta el sí.
4. El eje de release queda en `release: major|minor|patch|breaking`.

## Fase B — Versión y release

1. Detecta el esquema en tags y changelog. Si no hay esquema, propone SemVer 2.0.0 y espera confirmación. Si ya es CalVer, no conviertas commits `feat`/`fix` en bump SemVer: la versión es la fecha del esquema vigente y el changelog sigue siendo obligatorio.
2. Contrasta último tag, `CHANGELOG.md` y el manifiesto real (`package.json`, `pyproject.toml`, `Cargo.toml`; en Go el tag es la versión del módulo). Un desfase en modo publicación es `BLOCK`. Si no reconoces el ecosistema, `[PENDIENTE]`: no des por buena la coherencia.
3. Con SemVer y Conventional Commits posteriores al último tag: `fix` → PATCH, `feat` → MINOR, `BREAKING CHANGE` o `type!:` → MAJOR. Revisa además diffs de API, firmas públicas y esquemas. Un breaking no marcado bloquea la publicación.
4. Promueve `[Unreleased]` al formato de `assets/CHANGELOG.md`. El changelog es la fuente de las notas. No redactes notas que diverjan.
5. Tag anotado `vX.Y.Z` y `gh release create` solo tras el sí de esa acción. No reutilices un número yanked.
6. Si la release viaja en PR: aplica **Fase F** hasta mergear ese PR antes del tag.

## Fase C — Dependencias y documentación

1. Lee manifiesto y lockfile. Agrupa actualizaciones: patch, minor con CI verde, major solo con revisión humana. Contrasta EOL del runtime con el calendario oficial del lenguaje. No inventes la fecha de EOL.
2. README: badges que respondan, instalación reproducible, licencia. `SECURITY.md` con un camino de divulgación es `BLOCK` si el repo es público y `WARN` si es privado y no crítico. `CODEOWNERS` con `.github/workflows/` es aviso salvo repo crítico.
3. La documentación que cites debe hablar de la versión que se publica.

## Fase D — Pipeline

1. Pasa `actionlint` por `.github/workflows/`. Instalación: binario de release con checksum, como en `assets/workflows/workflow-lint.yml`. No uses `curl | bash` contra `main`.
2. Aplica `references/actions-security.md`. Línea mínima: `permissions` explícito con `contents: read` por defecto; SHA completo más comentario de versión; variables de entorno para entrada no confiable; secretos fuera de logs, cachés y artefactos; `timeout-minutes` en cada job.
3. Revisa la última ejecución (`gh run list`, `gh run view --log`) de cada workflow: fallos silenciosos, `continue-on-error` que esconde el fallo, caché con clave que no incluye el lockfile.
4. Patrones de caché, matrices, entornos y despliegue: `references/ci-cd-patterns.md`. Plantillas en `assets/workflows/`. Son andamios: adapta el stack y vuelve a verificar cada SHA antes de copiarlas. `ci.yml` es un ejemplo Node; no lo copies sobre Python, Rust o Go.
5. Tras remediación de pipeline: PR draft + **Fase F** (no dejes el PR abierto sin merge-watch).

## Fase E — Producción

1. Comprueba, en solo lectura, que los required checks existen y están verdes: lint, tests, build y escaneo de secretos. CodeQL, dependency review y rulesets son aviso salvo repo crítico.
2. Si el repo no despliega, la estrategia de despliegue es `N/A`, no un bloqueo.
3. Firma y provenance (attestations / SLSA) solo se exigen en repo crítico o si el usuario las pidió. El job que atestigua necesita `id-token: write`, `attestations: write` y `contents: read` en ese job, no en el resto del workflow.

## Fase F — Remediación y merge-watch

Lee `references/merge-watch.md` y ejecútalo siempre que haya PR de remediación o de cierre con publicación.

Resumen operativo:

1. Rama `chore/repo-ending-*` → push → PR **draft** a `main`.
2. Bucle: estado fresco → conflictos → comentarios → CI rojo → fix en alcance.
3. Required checks verdes → `gh pr ready` → `gh pr merge --squash` (o convención del repo).
4. Multi-repo: un PR por repo; paralelo OK; tabla final MERGED/blocked.
5. Self-hosted en cola: solo mergea si el ruleset no exige ese check; documenta.

## Recursos

| Archivo | Cuándo |
|---|---|
| `assets/labels.json` | Fase A |
| `assets/CHANGELOG.md` | Fase B |
| `assets/workflows/ci.yml` | Fase D, ejemplo Node |
| `assets/workflows/release.yml` | Fase B, al preparar la publicación |
| `assets/workflows/workflow-lint.yml` | Fase D |
| `assets/checklist-readiness.md` | Gate e informe |
| `references/actions-security.md` | Fase D |
| `references/ci-cd-patterns.md` | Fase D |
| `references/merge-watch.md` | Fase F (obligatoria tras remediación) |

## Uso

Usar ante cierre de repo, release/publicación, health check o auditoría de CI/CD, labels, changelog o seguridad de workflows en `github.com`. No usar para implementar features de producto ni forjas distintas de GitHub.

## Estructura

- `SKILL.md` — reglas, arranque, gate y Fases A–F.
- `assets/checklist-readiness.md` — gate de cierre.
- `assets/labels.json` — taxonomía de labels.
- `assets/CHANGELOG.md` — plantilla Keep a Changelog.
- `assets/workflows/` — plantillas `ci.yml`, `release.yml`, `workflow-lint.yml`.
- `references/actions-security.md`, `references/ci-cd-patterns.md`, `references/merge-watch.md` — detalle por fase.

## Herramientas

Sin scripts en esta skill. Herramientas externas citadas: `gh`, `git`, `actionlint`.

| Activo | Propósito |
|---|---|
| `assets/checklist-readiness.md` | Gate e informe |
| `assets/labels.json` | Mapeo de labels (Fase A) |
| `assets/CHANGELOG.md` | Formato de changelog (Fase B) |
| `assets/workflows/` | Andamios CI/release/lint (Fases B/D) |

## Referencias

- `assets/checklist-readiness.md`, `assets/labels.json`, `assets/CHANGELOG.md`, `assets/workflows/`.
- `references/actions-security.md`, `references/ci-cd-patterns.md`, `references/merge-watch.md`.
- Fuentes oficiales externas (texto): SemVer, Conventional Commits, Keep a Changelog, docs GitHub.
