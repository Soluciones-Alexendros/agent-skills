---
name: operar-lifecycle
description: >-
  Enruta el ciclo de vida del repositorio: deriva a verificar-repo (diagnóstico,
  health check e inicio de plan / repo starting), verificar-hooks (Husky) o
  operar-release (cierre, publicación y cierre de trabajo post-plan). Usar cuando
  el operador pregunte por dónde empezar, abra modo plan, o mezcle auditar,
  hooks, release o repo ending. No usar para ejecutar auditorías, hooks ni
  publicaciones (→ verificar-repo, verificar-hooks, operar-release).
license: MIT
metadata:
  author: Soluciones-Alexendros
  version: "1.3.0"
  dominio: operar
  tipo: router
  idioma: es
---

# operar-lifecycle — Enrutador del ciclo de vida del repo

## Propósito

Thin-router: ante una petición ambigua del ciclo de vida, decidir qué skill la atiende y derivar. No diagnostica, no configura hooks, no publica: delega.

Canon vigente: [docs/repo-standard](../../docs/repo-standard/structure.md) (`structure.md`, `ci-cd.md`, `release.md`, `security.md`, `templates/`).

## Cuándo usar

Peticiones del tipo «¿por dónde empiezo con este repo?», repo starting, inicio de plan, modo plan, repo ending, o que mezclan auditar, hooks y release.

## Reglas

1. **Una petición, una skill**: si la petición mezcla fases, ordenarlas (inicio/auditar → hooks → release) y ejecutarlas en secuencia, una cada vez. El inicio de plan es `verificar-repo` I; el cierre de trabajo post-plan es `operar-release` G.
2. **No duplicar el health check**: vive en `verificar-repo`. `operar-release` lo consume vía Fase 8, no lo repite.
3. **No absorber lógica**: el procedimiento vive en la skill destino; aquí solo el criterio de enrutado.
4. **Derivar con contexto**: al derivar a `operar-release`, pasar perfil, informe y checklist §8 (formato de la Fase 8 de `verificar-repo`).

## Enrutado

| Petición                                                                                                          | Destino                                                       |
| ----------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------- |
| Escanear, auditar, alinear con el estándar, «pon al día este proyecto», health check                              | `verificar-repo`                                              |
| Repo starting, inicio de plan, modo plan, «por dónde empiezo esta tarea»                                          | `verificar-repo` modo I (`references/inicio-plan.md`)         |
| Pre-commit hooks, Husky, lint-staged, Prettier local                                                              | `verificar-hooks`                                             |
| Cerrar el repo, preparar release, publicar versión, auditoría de CI/CD, labels, changelog, seguridad de workflows | `operar-release`                                              |
| Repo ending, cierre de trabajo, finalizar el plan, mergear el plan, ship del plan                                 | `operar-release` modo G (`references/cierre-trabajo.md`)      |
| Mezcla («audítalo y publícalo»)                                                                                   | `verificar-repo` primero; su Fase 8 deriva a `operar-release` |

## Referencias

- `verificar-repo` — diagnóstico, health check, inicio de plan (I) y Fase 8 de handoff.
- `verificar-hooks` — hooks locales.
- `operar-release` — cierre, publicación y cierre de trabajo (modo G).
- Canon: [structure.md](../../docs/repo-standard/structure.md), [ci-cd.md](../../docs/repo-standard/ci-cd.md), [release.md](../../docs/repo-standard/release.md), [security.md](../../docs/repo-standard/security.md).
