# Fase F — Remediación y merge-watch (escuchar, no vigilar)

Cuando la auditoría deja `BLOCK` remediables o el usuario pide aplicar correcciones de `/project-publish`, esta fase es **parte del workflow**, no un favor opcional.

## Cuándo aplica

- El usuario dice sí a remediación de pipeline / labels / docs de cierre.
- El usuario pide mergear / auto-merge tras abrir PRs de remediación o de cierre BUILD.
- Modo **cierre con publicación**: tras el PR de changelog/version bump.

No aplica en modo **auditoría pura** (solo informe).

## Autorización

Un sí a «aplica remediación», «abre el PR» o cierre BUILD autoriza:

1. Commits en rama de trabajo (`chore/project-publish-*`, `cursor/*`, etc.).
2. Push + PR (draft si el plan lo pide) a `main`.
3. **Auto-merge con merge commit** + suscripción a eventos (ver abajo).

Sigue exigiendo sí aparte: borrar labels legacy, tags, `gh release create`, rulesets, rotar secretos.

## Política de merge (normativa)

| Permitido                                      | Prohibido                                      |
| ---------------------------------------------- | ---------------------------------------------- |
| `gh pr merge <n> --auto --merge --delete-branch` | `--squash`, `--rebase`                         |
| Esperar checks required vía auto-merge         | `--admin` / bypass de protección o merge queue |

Si el repo exige otro método en branch protection, documentarlo en el informe y **no** inventar squash.

## Flujo: publicar y escuchar

Tras abrir el PR (y `gh pr ready` si deja de ser draft):

1. Activar auto-merge:

```bash
gh pr merge <n> --auto --merge --delete-branch
```

2. Suscribir la conversación del agente (Cursor):

- `subscribe_github_ci` → `repo: owner/name`, `branch: <head-del-PR>`
- `subscribe_github_pr` → `scope: pr`, mismo repo + `pullNumber` (o `prUrl`)

3. Declarar en una frase qué se espera (CI terminal o PR merged) y **terminar el turno**.
   No hacer `gh pr checks --watch` ni bucles de polling: el aviso llega como notificación.

   En Cursor (usuario): `~/.cursor/hooks.json` refuerza esto —
   `beforeShellExecution` (`pr_policy.py`, `failClosed`) deniega `--squash`/
   `--rebase`/`--admin` y exige `--merge` en invocaciones reales de `gh pr merge`
   (ignora texto en comillas/heredocs para evitar falsos positivos);
   `afterShellExecution` (`pr_listen.py`) inyecta el recordatorio de suscribir
   solo si la salida parece éxito, sin reinyectar el output crudo (anti-fuga).
   El aviso de fallo/éxito **no** lo emite el hook local: lo emiten
   `subscribe_github_ci` / `subscribe_github_pr` como notificación de la conversación.

4. Cuando llegue el evento:

- **CI failure** → corregir en alcance del PR, push (`--force-with-lease` solo si rebase local lo exige; nunca `--force`), reactivar `--auto --merge` si hace falta, volver a suscribir si la suscripción se cerró, terminar turno otra vez.
- **PR merged** → limpieza de ramas/worktrees (`cierre-trabajo.md` paso 6); actualizar informe.
- **PR closed without merge** → informar bloqueo; no reabrir sin instrucción.

## Grok / otros harnesses

Si no hay `subscribe_github_*`, equivalente: webhook/notificación del forge, o un único `gh pr checks --watch` no bloqueante en background que avise al completar — nunca revisión manual periódica en el chat.

## Multi-repo

Un PR por repo; una suscripción CI + PR por cada uno. Informe final: tabla repo · PR · MERGED/blocked · SHA.

## Entregable

```markdown
## Merge-watch

| Repo       | PR  | Estado | SHA / bloqueo |
| ---------- | --- | ------ | ------------- |
| owner/repo | #N  | MERGED | abc1234       |
```

Actualiza el readiness: los `BLOCK` remediados pasan a `OK` o `WARN` justificado.
