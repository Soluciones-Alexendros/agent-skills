# Canon de flota: repo-standard

Fuente de verdad: [Soluciones-Alexendros/repo-standard](https://github.com/Soluciones-Alexendros/repo-standard) (plantilla GitHub, contrato SemVer en ADRs).

Esta referencia resume estructura, perfiles y normas cerradas. Para alinear un repo existente, leer `reutilizacion.md` completo. No copiar a ciegas el `ci.yml` del meta-canon: usar snippets de `stacks/` en el repo remoto.

## Perfiles

| Perfil | Cuándo | Mínimo |
|--------|--------|--------|
| **P0 Base** | Todo repo activo | README, LICENSE, CHANGELOG, SECURITY, CONTRIBUTING, CI `quality`+`test`, CODEOWNERS, description, ≥4 topics, `main` protegida |
| **P1 Producto** | Hay runtime | + `docs/` (architecture, guides, runbooks), AGENTS.md, ARCHITECTURE.md, `.env.example`, job `smoke` required, Renovate, issue/PR templates, meta-sección en markdown contractuales |
| **P2 Público** | Community / SaaS público | + CODE_OF_CONDUCT, SUPPORT, topics ≥6, `security.yml`, coverage gate publicado |

## Árbol esperado (producto P1)

```
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
  architecture/          # overview + decisions/
  guides/                # local-setup, coding-standards, testing
  runbooks/              # deploy, rollback, rotate-secrets
.github/
  CODEOWNERS
  PULL_REQUEST_TEMPLATE.md
  ISSUE_TEMPLATE/
  renovate.json
  workflows/ci.yml       # jobs: quality → test → [build?] → smoke
```

`build` solo si hay artefacto (ADR-0003). Sin Dependabot version-updates.

## Decisiones cerradas (no reabrir)

- Renovate es el único bot de version-updates; Dependabot Alerts pueden quedar ON.
- Docs en español. Coverage por defecto ≥70% (80% en críticos); gate de coverage opcional hasta suite estable.
- Automerge humano/agente solo con label `automerge` + CI verde + review.
- Orden de gates: `quality` → `test` → `build` → `smoke` (`e2e` opcional en webs).
- Meta-sección obligatoria en markdown contractuales (excepto CHANGELOG Keep a Changelog):

```markdown
### Propósito de este documento
- **Objetivos:** …
- **Estructura:** …
- **Contenido a integrar según contexto:** …
```

## Makefile canónico

| Target | Significado |
|--------|-------------|
| `make validate` | integridad / check-env / estructura |
| `make lint` | format + lint + types |
| `make test` | unit/function (+ coverage) |
| `make smoke` | health/rutas/`--help` post-build |

## Cómo usar en auditoría (verify-repo)

1. Detectar perfil (P0/P1/P2) según runtime, público y docs existentes.
2. Ejecutar `scripts/check-product-structure.sh <repo> --profile P0|P1|P2`.
3. Contrastar hallazgos con checklist §8 de `reutilizacion.md`.
4. Plan de alineación = un PR, sin force-push; copiar vs adaptar según tabla de `reutilizacion.md`.
5. Settings de org/protección de `main`: solo informar; lo aplica un humano.

## Archivos en esta carpeta

| Archivo | Contenido |
|---------|-----------|
| `reutilizacion.md` | Checklist y orden de alineación (upstream) |
| `overview.md` | Límites y flujos del canon |
| `architecture-resumen.md` | Resumen 1 página |
| `coding-standards.md` / `testing.md` | Guías de flota |
| `adrs-indice.md` | Índice de ADRs; detalle en el repo remoto |
