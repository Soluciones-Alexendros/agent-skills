# Tasks: taxonomía v5 con role-clean-code

Origen: `tasks/plan.md` (aprobado) y `.autoworkspace/SPEC.md`.
El producto ya está en `ac85b9e`. Estas fichas no reabren esa implementación.

## Task 1: Paridad de catálogo

**Description:** El árbol vivo nombra las mismas 16 skills que el índice, con dominio `local` y con `role-clean-code` enlazado desde los harnesses.

**Acceptance criteria:**

- [x] `skills/` y `skill-index.json` listan los mismos 16 nombres
- [x] README, AGENTS, TAXONOMY y harness dicen 16 skills y dominio `local`
- [x] Los handoffs vivos de tests apuntan a `plan-validators`

**Verification:**

- [x] Tests pass: `npm test` en `ac85b9e` (34 pytest y humo del router, `role-clean-code` resuelto)
- [x] Build succeeds: no hay build de aplicación
- [x] Manual check: índice generado con `python3 tools/skill-router/build_index.py` antes del merge

**Dependencies:** None

**Implementation roles:** Ninguno. Verificación de documentación e índice, sin superficie de implementación.

**Test surfaces:** Router de skills (`tools/skill-router`) y el inventario de `skills/`. Sin rutas HTTP, jobs ni UI.

**Files likely touched:**

- `skills/`
- `skill-index.json`
- `docs/TAXONOMY.md`
- `README.md`
- `AGENTS.md`
- `docs/harness-integration.md`

**Estimated scope:** Medium: 3-5 files. Cerrada en el merge.

## Task 2: Suite estándar del merge

**Description:** El commit que integra `main` deja los gates locales en verde.

**Acceptance criteria:**

- [x] `npm test` termina en verde
- [x] `npm run typecheck` termina en verde
- [x] No quedan rutas sin fusionar

**Verification:**

- [x] Tests pass: `bash run-validation.sh --pytest-only --smoke-only` (34 passed)
- [x] Build succeeds: `npm run typecheck` durante el hook del commit `ac85b9e`
- [x] Manual check: `git diff --name-only --diff-filter=U` vacío tras el commit

**Dependencies:** Task 1

**Implementation roles:** Ninguno. El cambio de handoffs dentro de `role-clean-code` ya se hizo en el merge; no queda edición.

**Test surfaces:** Pytest de `tools/` y humo del router. Sin rutas, jobs ni E2E de navegador.

**Files likely touched:**

- `run-validation.sh`
- `skills/role-clean-code/`

**Estimated scope:** Small: 1-2 files. Cerrada en el merge.

## Checkpoint: After Tasks 1-2

- [x] All tests pass
- [x] Application builds without errors (typecheck; no hay artefacto)
- [x] Core user flow works end-to-end: el router resuelve `role-clean-code` y el índice tiene 16 skills
- [x] Review with human before proceeding (plan aprobado el 2026-10-17)

## Task 3: Registrar spec y plan

**Description:** Un commit aparte guarda la spec aprobada, el plan aprobado y esta lista. No cambia el catálogo ni la versión publicada.

**Acceptance criteria:**

- [x] El commit contiene `.autoworkspace/SPEC.md`, `tasks/plan.md` y `tasks/todo.md`
- [x] No incluye push, bump de `package.json` ni ficheros de la deuda P1
- [x] El mensaje es Conventional Commits y el árbol queda limpio

**Verification:**

- [x] Tests pass: `npm test` (lo dispara el hook de pre-commit)
- [x] Build succeeds: `npm run typecheck` en ese mismo hook
- [x] Manual check: `git status -sb` limpio y `git show --stat` limitado a esos tres ficheros

**Dependencies:** Tasks 1 y 2

**Implementation roles:** Ninguno. Alta de documentos de plan, sin editar skills ni código de producto.

**Test surfaces:** La suite estándar del hook. Sin rutas, funciones de producto, jobs ni E2E.

**Files likely touched:**

- `.autoworkspace/SPEC.md`
- `tasks/plan.md`
- `tasks/todo.md`

**Estimated scope:** Small: 1-2 files de producto, tres documentos de plan.

## Task 4: Publicar la rama

**Description:** Empujar `feat/local-taxonomy-validators` a origin para que el PR #13 deje de estar `CONFLICTING`. No se ejecuta sin un sí explícito.

**Acceptance criteria:**

- [ ] El push incluye `ac85b9e` y el commit de la Task 3
- [ ] `gh pr view 13` deja de informar `CONFLICTING`
- [ ] No se mergea el PR en esta tarea

**Verification:**

- [ ] Tests pass: los del commit que se empuja, ya en verde en local
- [ ] Build succeeds: sin build adicional
- [ ] Manual check: `gh pr view 13 --json mergeable,mergeStateStatus,url`

**Dependencies:** Task 3

**Implementation roles:** Ninguno. Operación de git sobre la rama ya verificada.

**Test surfaces:** Estado del PR en GitHub. Sin superficie de aplicación.

**Files likely touched:**

- Ninguno en el árbol. Actualiza `origin/feat/local-taxonomy-validators`.

**Estimated scope:** XS: un push, cero ficheros nuevos.

## Checkpoint: After Tasks 3-4

- [ ] All tests pass en el commit de documentación
- [ ] Application builds without errors
- [ ] Core user flow works end-to-end: PR #13 mergeable, o el push sigue pendiente porque no se ha pedido
- [ ] Review with human before INTEGRATE (`project-publish`)
