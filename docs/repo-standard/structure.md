# Estructura de repositorio — canon repo-standard

### Propósito de este documento

- **Objetivos:** Fijar el árbol canónico de ficheros, las reglas de nombrado y el formato de commits que todo repo de la flota debe cumplir por perfil (P0/P1/P2). Solo lectura: la remediación vive en las skills `verificar-repo` (diagnóstico) y `operar-release` (cierre).
- **Estructura:** Esta meta-sección → Perfiles → Árbol canónico → Nombrado → Commits → Verificación.
- **Contenido a integrar según contexto:** En un producto, este archivo no se copia: se declara «cumple `repo-standard`» y se adapta el árbol al stack. La validación se hace con `check-product-structure.sh` de `verificar-repo`.

## Perfiles

| Perfil | Cuándo aplica | Mínimo exigible |
|--------|---------------|-----------------|
| **P0 Base** | Todo repo activo | README, LICENSE, CHANGELOG, SECURITY, CONTRIBUTING, CI `quality`+`test`, CODEOWNERS, descripción, ≥4 topics, `main` protegida |
| **P1 Producto** | Hay runtime | + `docs/` (architecture, guides, runbooks), AGENTS.md, ARCHITECTURE.md, `.env.example`, job `smoke` required, Renovate, plantillas de issue/PR, meta-sección en markdown contractuales |
| **P2 Público** | Community / SaaS público | + CODE_OF_CONDUCT, SUPPORT, topics ≥6, `security.yml`, coverage gate publicado |

## Árbol canónico (producto P1)

```text
README.md
LICENSE
CHANGELOG.md
SECURITY.md
CONTRIBUTING.md
AGENTS.md
ARCHITECTURE.md
Makefile
.env.example
docs/
  README.md
  architecture/          # overview.md + decisions/ (ADR-0001… + template.md)
  guides/                # local-setup, coding-standards, testing
  runbooks/              # deploy, rollback, rotate-secrets
.github/
  CODEOWNERS
  PULL_REQUEST_TEMPLATE.md
  ISSUE_TEMPLATE/
    bug.yml
    feature.yml
  renovate.json
  workflows/
    ci.yml               # jobs: quality → test → [build?] → smoke
```

Reglas:

- `build` solo existe si hay artefacto (compilado, imagen, paquete). Si no hay artefacto, el job no existe y ningún required check lo exige.
- Sin Dependabot `version-updates`: el único bot de actualizaciones es Renovate (las alertas de seguridad de Dependabot pueden quedar activadas).
- `docs/architecture/decisions/` conserva `template.md` y numera `ADR-0001…` sin reutilizar números.
- Cada markdown contractual lleva la meta-sección «Propósito de este documento» justo tras el H1. Excepción: `CHANGELOG.md` sigue Keep a Changelog (párrafo breve o nada). No aplica a `LICENSE`, JSON/YAML, scripts ni binarios.

## Nombrado

- Ramas: `audit/AAAAMMDD` (diagnóstico `verificar-repo`), `chore/operar-release-*` (remediación de cierre), `feat/*`, `fix/*`. Sin force-push. Un PR de alineación por repo.
- Tags: anotados `vX.Y.Z` (SemVer) o fecha vigente si el repo es CalVer (no convertir uno en otro).
- Workflows y jobs con nombres estables en inglés técnico: `quality`, `test`, `build`, `smoke`, `actionlint`, `Secret scanning`. Un required check nunca cambia de nombre ni lleva filtro `paths` que lo oculte en un PR.
- Labels por ejes `type:`, `priority:`, `status:`, `area:`, `release:` (ver `operar-release/assets/labels.json`). Solo el eje `area` se adapta al dominio.
- Ficheros: `kebab-case` para markdown y workflows; el código sigue la convención local del repo (esta prima sobre el canon en estilo).

## Commits

Formato Conventional Commits 1.0.0 (`https://www.conventionalcommits.org/en/v1.0.0/`):

```text
<type>(<scope>)<!>: <descripción breve en imperativo>
```

- Types: `feat`, `fix`, `docs`, `chore`, `refactor`, `test`, `ci`, `revert`. `BREAKING CHANGE:` en el pie o `!` tras el tipo/scope obliga a bump MAJOR.
- Un commit = un cambio lógico. Commits solo a petición del operador; nunca commitear secretos ni placeholders `[PENDIENTE]`.
- Reglas automáticas en `templates/commitlint.config.cjs` de este canon (type-enum, subject-case, header-max-length).

## Verificación

```bash
bash <verificar-repo>/scripts/check-product-structure.sh <repo> --profile P1
```

Criterio: faltantes = 0 y errores = 0. Los avisos (`ISSUE_TEMPLATE/*.yml` ausente, `SUPPORT.md` en P2) no bloquean salvo repo crítico.
