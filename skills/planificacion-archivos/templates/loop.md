# Planning-aware loop

Maintenance prompt read by Claude Code's bare `/loop` on every tick.
Replace the default bare-loop prompt with this file to keep long sessions anchored to disk state.

## Every tick

1. Resolve the active plan directory (`.planning/<id>/` or legacy root) with `scripts/resolve-plan-dir.sh`.
2. Re-read `task_plan.md` and `progress.md` before acting. Disk state is the source of truth.
3. Run `scripts/check-complete.sh` for the active plan.
4. If no `progress.md` entry was written since the previous tick, append one: what the loop did, found, or decided (or why it did nothing).
5. Pick the next unchecked task. Never start a phase whose gate is unsatisfied.
6. Stop the tick cleanly when the plan is complete or blocked; report the blocker instead of improvising scope.

## Guardrails

- One task per tick unless the plan explicitly batches.
- Log before acting; a tick without a progress entry is a failed tick.
- If the plan directory is missing, re-run `scripts/init-session.sh` instead of creating files ad hoc.
