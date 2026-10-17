# Implementation Plan: taxonomía v5 con role-clean-code

## Overview

El catálogo de 16 skills ya está en `feat/local-taxonomy-validators` @ `ac85b9e`
(merge de `main` `39af374` sobre `0ffe519`). Este plan no reimplementa la
taxonomía. Ordena la evidencia que ya cumple la spec, deja fuera la deuda de
estructura P1 y deja el push del PR #13 detrás de una confirmación.

Spec: `.autoworkspace/SPEC.md` (aprobada). Lista de tareas detallada: aún no.
Se escribirá en `tasks/todo.md` solo después de aprobar este plan.

## Architecture Decisions

- Un solo incremento. No hay mapa de módulos: el catálogo, el índice y los
  handoffs se publican juntos.
- `main` ya contenía `role-clean-code` 1.0.0 sobre la taxonomía `system-*` de
  19 skills. La rama lo incorpora como 1.1.0 y reescribe los handoffs vivos a
  `plan-validators`. Las entradas históricas del changelog no se reescriben.
- `package.json` permanece en 4.1.0. El breaking de taxonomía sigue en
  `[Unreleased]` hasta un cierre con `project-publish`.
- La estructura P1 que falta (CONTRIBUTING en la raíz, `ci.yml`,
  ARCHITECTURE, Makefile, `.env.example`, `docs/{architecture,guides,runbooks}`,
  plantilla de PR y la meta-sección de propósito) no entra en este plan.
- Sin trabajo de frontend, backend ni design system. Si una tarea posterior
  edita prosa de una skill, el rol es `role-clean-code`. Verificar el índice
  y el router no lleva rol de implementación.

## Components and order

Secuencial. No hay trabajo paralelo: cada paso lee el resultado del anterior
y el árbol debe seguir en verde.

1. **Evidencia del catálogo.** Contrastar `skills/`, `skill-index.json`,
   `docs/TAXONOMY.md`, README, AGENTS y harness con los criterios 1–3 de la
   spec. Hecho en `ac85b9e`: 16 nombres coinciden y el router resuelve
   `role-clean-code`.
2. **Evidencia de tests.** `npm test` y `npm run typecheck`. Hecho en el
   commit de merge: 34 pytest en verde y typecheck del hook en verde.
3. **Registrar spec y plan** en git cuando este plan esté aprobado. No forma
   parte del merge ya cerrado.
4. **Push** de `feat/local-taxonomy-validators` solo con confirmación. Hasta
   entonces el PR #13 sigue `CONFLICTING` en GitHub.
5. **INTEGRATE** (`project-publish`) queda fuera de este plan. Entra después
   de las tareas y de otro sí.

## Task List

El desglose con criterios, roles, ficheros y verificación vive en
`tasks/todo.md` y no se escribe en este paso.

### Phase 1: Evidence

- [x] Task 1: Paridad de catálogo (16 skills, dominio `local`, `role-clean-code`)
- [x] Task 2: Suite estándar en verde sobre el merge

### Checkpoint: Evidence

- [x] `npm test` pasó en `ac85b9e` (34 pytest, humo del router)
- [x] `npm run typecheck` pasó en el hook de ese commit
- [x] Revisión humana de este plan antes de abrir `tasks/todo.md` (2026-10-17)

### Phase 2: Record and publish gate

- [x] Task 3: Commit de `.autoworkspace/SPEC.md`, `tasks/plan.md` y `tasks/todo.md`
- [ ] Task 4: Push a `origin/feat/local-taxonomy-validators` solo si se pide

### Checkpoint: Branch matches origin

- [ ] PR #13 ya no está `CONFLICTING`, o el push sigue pendiente a propósito
- [x] La deuda de estructura P1 sigue fuera de la rama

## Risks and Mitigations

| Risk                                                       | Impact | Mitigation                                                                    |
| ---------------------------------------------------------- | ------ | ----------------------------------------------------------------------------- |
| Push no pedido deja el PR #13 en conflicto                 | Med    | El plan no empuja. El criterio 5 de la spec sigue abierto hasta un sí.        |
| Reescribir el changelog 4.1.0 (19 skills) para que diga 16 | Med    | Esa cifra es la del release en `main`. El estado vivo está en `[Unreleased]`. |
| Colar la remediación P1 en el mismo PR                     | Med    | Fuera de alcance. Un chore posterior, con su propia spec.                     |
| `role-clean-code` 1.1.0 solo en local                      | Low    | Viaja con el push del merge. No hay otro commit de producto pendiente.        |

## Verification checkpoints

- Tras el merge: `npm test` y typecheck. Ya ejecutados, en verde.
- Tras el commit de spec y plan: `npm test` otra vez, porque el hook de
  pre-commit lo exige.
- Tras un push futuro: `gh pr view 13 --json mergeable,mergeStateStatus`.
- No hay build de aplicación ni flujo de navegador.

## Open Questions

- ¿Empujo `ac85b9e` (y los commits de spec/plan, si ya existen) a origin?
- ¿La deuda de estructura P1 se planifica como incremento distinto?
- Resuelta el 2026-10-17: el plan está aprobado y las tareas viven en `tasks/todo.md`.
