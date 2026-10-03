---
name: operar-release
description: >-
  Cierra un repositorio de GitHub: publicación de versión, auditoría de CI/CD,
  o cierre de trabajo al finalizar un plan (repo ending, mergear el plan, ship).
  Usar cuando el tema sea semantic versioning, Keep a Changelog, supply-chain
  de Actions, Husky+e2e+PR+merge-watch post-plan. No usar para implementar
  features de producto ni forjas distintas de github.com (→ verificar-repo).
license: MIT
metadata:
  author: Soluciones-Alexendros
  version: "2.2.0"
  dominio: operar
  tipo: atomic
  idioma: es
---

# operar-release

## Propósito

Actuar como ingeniero de plataforma en el cierre de un repo GitHub. Adaptar la ceremonia al tamaño, al stack y al riesgo. El health check vive en `verificar-repo`: si el repo llega sin diagnóstico, derivar allí primero.

Canon vigente: [release.md](../../docs/repo-standard/release.md), [ci-cd.md](../../docs/repo-standard/ci-cd.md), [security.md](../../docs/repo-standard/security.md), [structure.md](../../docs/repo-standard/structure.md).

## Cuándo usar

Cerrar el repo, preparar release, publicar versión, auditar CI/CD, labels, changelog o seguridad de workflows en github.com. También: repo ending, cierre de trabajo, finalizar el plan, mergear el plan o ship del plan.

## Procedimiento

Invocación explícita: `/operar-release`. Remoto `github.com` y `gh auth status` antes de seguir. Modos: auditoría, remediación, cierre con publicación, cierre de trabajo (post-plan).

Reglas: no inventar versiones, tags, SHAs ni licencias; `[PENDIENTE]` si no se puede verificar; no publicar con `[PENDIENTE]` en un ítem que bloquea. Antes de citar SemVer, Conventional Commits, Keep a Changelog o política de Actions, abrir la fuente oficial. Idioma del informe: el del operador. Labels, workflows y nombres de checks, en inglés técnico. Mutación: un sí, una acción — excepto el bucle merge-watch una vez autorizado. Nunca commitear un `uses:` sin SHA de 40 hex.

Fuentes: SemVer 2.0.0, Conventional Commits 1.0.0, Keep a Changelog 1.1.0, GitHub Actions secure use, immutable releases.

Confirmación: GET y listados en solo lectura. Crear labels, tags o releases exige diff y sí. Un sí a remediación de pipeline autoriza commits, PR draft y Fase F; no autoriza tags. Pedir cierre de trabajo / finalizar el plan autoriza la Fase G completa (gate, revisión, PRs, merge-watch, limpieza); tags siguen aparte.

**Gate.** Recorrer `assets/checklist-readiness.md` (`OK`/`WARN`/`BLOCK`/`N/A`). Bloquea siempre: secreto en el árbol, `uses:` de terceros sin SHA, workflow sin `permissions`, job sin `timeout-minutes`, interpolación de entrada no confiable, `pull_request_target` o `workflow_run` peligrosos. En publicación: desfase tag/changelog/manifiesto, breaking sin MAJOR, versión yanked. SLSA es aviso salvo repo crítico o petición explícita.

- **A Labels.** `gh label list` frente a `assets/labels.json`. Eje de release: `release: major|minor|patch|breaking`.
- **B Versión.** SemVer por defecto. Promover `[Unreleased]` al formato de `assets/CHANGELOG.md`. Tag anotado y `gh release create` solo tras sí. Si la release viaja en PR: Fase F antes del tag.
- **C Dependencias y docs.** `references/dependabot-grouped.md`. `SECURITY.md` es BLOCK en repo público.
- **D Pipeline.** `actionlint`, `references/actions-security.md`, `references/ci-cd-patterns.md`. Ruleset de `main`: `assets/ruleset.json` (lo aplica un humano).
- **E Producción.** Checks required verdes. Firma y provenance solo en crítico o a petición.
- **F Merge-watch.** `references/merge-watch.md`. Rama `chore/operar-release-*` → PR draft → squash.
- **G Cierre de trabajo.** Tras un plan (`/execute-plan` o `task_plan.md` completo): `references/cierre-trabajo.md`. Gate Husky (`verificar-hooks` modo gate) → e2e Playwright si hay UI → revisión contra el plan → PRs a `main` → merge-watch con squash → limpieza de ramas y temporales. Tags y `gh release create` siguen en B, con sí aparte.

## Herramientas

| Script                      | Propósito                                                                 |
| --------------------------- | ------------------------------------------------------------------------- |
| `scripts/review-vs-plan.py` | Revisión crítica automatizada del diff contra el plan (paso 3 del modo G) |
| `scripts/tests/smoke_sh.sh` | Smoke test de la revisión (diff vacío, cambios, secretos)                 |

Activos no ejecutables (checklist-readiness, labels, CHANGELOG, workflows, ruleset, actions): ver `## Referencias`.

## Referencias

- `assets/checklist-readiness.md`, `assets/labels.json`, `assets/CHANGELOG.md`, `assets/workflows/`, `assets/ruleset.json`, `actions/`.
- `references/actions-security.md`, `references/ci-cd-patterns.md`, `references/dependabot-grouped.md`, `references/merge-watch.md`, `references/cierre-trabajo.md`.
- Diagnóstico → `verificar-repo`. Hooks → `verificar-hooks`. E2E → `webapp-testing` (catálogo compartido).
