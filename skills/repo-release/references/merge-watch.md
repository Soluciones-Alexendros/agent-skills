# Fase F — Remediación y merge-watch

Cuando la auditoría deja `BLOCK` remediables o el usuario pide aplicar correcciones de `/repo-release`, esta fase es **parte del workflow**, no un favor opcional.

## Cuándo aplica

- El usuario dice sí a remediación de pipeline / labels / docs de cierre.
- El usuario pide «monitoriza hasta mergear» o equivalente tras abrir PRs de remediación.
- Modo **cierre con publicación**: tras el PR de changelog/version bump, el mismo bucle aplica antes del tag.

No aplica en modo **auditoría pura** (solo informe).

## Autorización

Un sí a «aplica remediación» o «sigue con el pipeline» autoriza:

1. Commits en rama `chore/repo-release-*` (o `audit/AAAAMMDD` si ya existe).
2. Push + PR **draft** a `main`.
3. **Monitorización hasta merge** de ese PR (ver abajo).

Sigue exigiendo sí aparte: borrar labels legacy, tags, `gh release create`, rulesets, rotar secretos.

## Bucle merge-watch (obligatorio tras abrir el PR)

1. **Estado fresco** cada pasada: `gh pr view`, `gh pr checks` (o `gh pr checks --watch` mientras corren).
2. Prioridad de bloqueos: conflictos → comentarios no resueltos → CI en rojo.
3. Fallos de CI **en alcance del PR**: corrige, verifica en local lo mínimo, push (sin force).
4. Cuando required checks están verdes y `mergeable`:
   - `gh pr ready <n>` si sigue en draft.
   - `gh pr merge <n> --squash` (o el método que use el repo; no inventes política).
5. Si un check no requerido falla (p. ej. job de draft/`pr-summary`) y los required están verdes: documenta y mergea.
6. Self-hosted en cola indefinida: solo mergea si el ruleset/branch protection **no** exige ese check; anótalo en el informe.
7. Nunca force-push. Nunca cambies workflows solo para silenciar un fallo.

## Multi-repo

Si el alcance es N repos, abre un PR por repo y ejecuta el bucle en paralelo (subagentes o `gh pr checks --watch` por PR). El informe final es una tabla: repo · PR · MERGED/blocked · SHA o bloqueo.

## Entregable

Tras mergear (o al bloquearse):

```markdown
## Merge-watch
| Repo | PR | Estado | SHA / bloqueo |
|---|---|---|---|
| owner/repo | #N | MERGED | abc1234 |
```

Actualiza el readiness: los `BLOCK` remediados pasan a `OK` o `WARN` justificado.
