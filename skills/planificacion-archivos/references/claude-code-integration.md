# Integración Claude Code y modos autónomos (planificacion-archivos)

> Extraído de SKILL.md en v0.1.0 para mantener el cuerpo bajo el límite recomendado de 500 líneas.

## Claude Code Turn-Loop Integration (v2.38.0+)

Claude Code shipped three new turn-loop primitives in May 2026: `/loop` (v2.1.72), `/goal` (v2.1.139), and the `PreCompact` hook event. v2.38.0 wires the planning workflow into all three.

### Install scope: plugin vs skill-only (v2.42.0 clarification)

Not every install path ships every surface in this section. Two distinct install routes exist:

| Install route | What you get | `/plan-goal`, `/plan-loop` available? |
|---|---|---|
| `/plugin marketplace add OthmanAdi/planning-with-files` then `/plugin install` | SKILL.md, scripts, templates, **plus `commands/` folder** | Yes, as `/plan-goal` and `/plan-loop` |
| `npx skills add OthmanAdi/planning-with-files` (or ClawHub) | SKILL.md, scripts, templates only | No, follow the manual fallback below |

The PreCompact hook is registered in the SKILL.md frontmatter and works for both routes. The `/plan-goal` and `/plan-loop` slash commands live in `commands/` at the repo root, which only the plugin route copies into `~/.claude/plugins/marketplaces/`. Skill-only installs land at `~/.claude/skills/planning-with-files/` and do not see `commands/`.

Both slash commands also carry `disable-model-invocation: true`, which means the model will not auto-trigger them. You type them. Per known Claude Code behavior (anthropics/claude-code issues #26251, #41417), some sessions interpret `disable-model-invocation: true` as "I cannot use the Skill tool for this entry at all" and refuse to fire even when you type the slash. If that happens, the manual fallback below produces the same effect.

### PreCompact hook (auto)

The skill registers a `PreCompact` hook with matcher `"*"`. It fires on both `/compact` (manual) and autoCompact (context-full). When `task_plan.md` is present, the hook:

- Reminds the agent to flush in-context progress to `progress.md` before compaction completes.
- Prints `Plan-SHA256` if an attestation is set, so the post-compaction agent can verify the plan is still the one you approved.
- Stays silent when no plan exists. Exit code 0 always — never blocks compaction.

Compaction still proceeds. The protection model is "the plan is on disk, the plan will be re-read after compaction" — not "the plan survives compaction unchanged in context."

### `/plan-goal` slash command

Composes with Claude Code's `/goal`. Derives a goal condition from the active plan and forwards it to `/goal`, so the agent keeps working until the plan file actually reports complete.

```
/plan-goal                                # default: "all phases report Status: complete"
/plan-goal until all tests pass           # appends user clause to default
```

`/plan-goal` does not replace `/goal`. `/goal "anything"` still works.

### `/plan-loop` slash command

Composes with Claude Code's `/loop`. Default 10-minute tick re-reads the planning files, runs `check-complete`, and writes a `progress.md` entry if nothing changed since the last tick.

```
/plan-loop                                # default 10m cadence, default tick prompt
/plan-loop 5m                             # override interval
/plan-loop 15m custom prompt              # override interval + prompt
```

For a "babysit until done" workflow, combine `/plan-loop` (cadence) with `/plan-goal` (termination criterion).

### Manual fallback when `/plan-goal` / `/plan-loop` are unavailable (v2.42.0)

For skill-only installs (no `commands/` folder) or sessions where the slash command refuses to fire, the model can produce the same effect by executing the wrapper steps inline.

**Manual `/plan-goal` procedure:**

1. Resolve the active plan: prefer `${PLAN_ID}` env var, then `.planning/.active_plan`, then newest `.planning/<dir>/`, then legacy `./task_plan.md`.
2. Read the resolved `task_plan.md`.
3. Compose a goal condition. Default: `"all phases in task_plan.md report Status: complete and check-complete.sh reports ALL PHASES COMPLETE"`. If the user passed additional clauses, append them.
4. Issue Claude Code's native `/goal <condition>` (CC primitive, always available).
5. Confirm to the user: print the condition + active plan ID + remind that `/goal clear` cancels.
6. Refuse if `task_plan.md` does not exist; direct the user to run init first.

**Manual `/plan-loop` procedure:**

1. Parse args: first arg matching `^\d+[smhd]$` is the interval (default `10m`), remaining args are an optional task prompt.
2. Resolve the active plan as above.
3. Compose the loop tick prompt. If user passed a task prompt, use it verbatim. Otherwise use the planning-aware default that re-reads `task_plan.md` and `progress.md`, runs `scripts/check-complete.sh`, and writes a `progress.md` entry if no progress was logged since the last tick.
4. Issue Claude Code's native `/loop <interval> <prompt>` (CC primitive, always available).
5. Confirm to the user: print interval + active plan ID + remind that bare `/loop` runs the built-in maintenance prompt.

Both procedures match what the `commands/plan-goal.md` and `commands/plan-loop.md` files _(ejemplo: ruta upstream del plugin, no incluida en esta skill)_ would have fed the model when invoked. The native `/loop` and `/goal` primitives are always available in Claude Code; only the planning-aware wrapper is plugin-scoped.

### `loop.md` template

Claude Code's bare `/loop` reads `.claude/loop.md` (project) or `~/.claude/loop.md` (user). v2.38 ships a planning-aware template at `templates/loop.md`. Install once:

```bash
# user-wide
cp ${CLAUDE_PLUGIN_ROOT}/templates/loop.md ~/.claude/loop.md

# project-specific
cp ${CLAUDE_PLUGIN_ROOT}/templates/loop.md .claude/loop.md
```

After install, bare `/loop <interval>` runs the planning-aware tick.

## Autonomous and Gated Modes (v3)

v3 adds two opt-in modes for long-running agentic work with strong models (Opus 4.8, Fable 5, GPT 5.5 class). Both key off an explicit marker file in the plan directory. With no marker present, behavior is exactly v2.43: nothing in this section changes the legacy path.

The mode is set by writing a `.mode` file next to the plan (`.planning/<id>/.mode`, or `./.mode` in legacy root mode). `init-session` writes it for you when you pass `--autonomous` or `--gated`.

### The legacy invariant (promise)

With no `.mode` file and no other v3 marker, the hooks produce byte-identical output to v2.43, including the raw `progress.md` tail and the `===BEGIN PLAN DATA===` / `===END PLAN DATA===` delimiters. Every v3 behavior is additive and opt-in. No existing workflow changes.

### What each mode does

| | Legacy (default) | Autonomous | Gated |
|---|---|---|---|
| Turn-start injection (UserPromptSubmit) | Full plan head + raw progress tail | Full plan head + structured ledger summary | Full plan head + structured ledger summary |
| Per-tool-call injection (PreToolUse) | Plan head every call | Dropped (recitation policy) | Dropped (recitation policy) |
| Stop event | Advisory only, never blocks | Advisory only, never blocks | Completion gate may block (host-aware) |
| Attestation | Opt-in | Default-on at init | Default-on at init |
| Progress injection | Raw `tail -20 progress.md` | `ledger-summary.sh` synthesized block | `ledger-summary.sh` synthesized block |

Autonomous mode answers the recitation question: strong models drift less, so the per-tool-call plan re-injection (about 90 tokens per matched tool call, the component that scales with tool use) is dropped. Turn-start injection stays because the evidence (arxiv 2603.03258, claudefa.st on Opus 4.7+ subagents) shows drift is real and the full plan file still matters once per turn. Eliminating recitation entirely is not supported by evidence.

Gated mode adds the completion gate on top of autonomous behavior. The gate is the termination oracle: it judges the plan artifact on disk, not the conversation transcript, which is why it beats a transcript-bound evaluator that can be hallucinated.

### Structure-aware injection (v3.8.0, opt-in)

The default injection is `head -50` (turn start) and `head -30` (per tool call), which is position-blind: late in a long plan the in_progress phase, the Decisions journal, and the Errors table all sit past the injected window, so every injection pays the token cost while the window no longer carries the active phase. Opt in with `PWF_INJECT=smart` in the environment, or an `inject-smart` token in the plan's `.mode` file, and the injection instead emits: the plan title, the Goal / Next Step / Current Phase sections, a phase count, the full first in_progress phase section, and the last 3 rows of Decisions Made. Plans without `### Phase` headings fall back to the plain head. `inject-smart` alone does not activate any other v3 behavior; it composes with autonomous and gated modes (`init-session` mode tokens are space-separated in `.mode`). With neither the env var nor the token present, output is byte-identical to the legacy shape.

### Gate decision table

The Stop gate blocks ONLY when all of these hold. Any single failure allows the stop. This is the lesson from issue #178: an incomplete plan is a normal state, not an error, and accidental blocking infuriates users.

1. Mode is gated (the `.mode` file contains `gate`).
2. An `in_progress` phase exists (not merely COMPLETE < TOTAL).
3. `stop_hook_active` is false on the Stop hook stdin (already inside a forced continuation means allow stop).
4. Block count is below the cap (default 20, `PWF_GATE_CAP` to override, reset at init-session).
5. The ledger progressed since the previous block (a stall means allow stop).

The block reason is a fixed template plus the phase NAME only. Plan body text never enters the reason. Outside gated mode the wording is always advisory, never imperative (PR #180 lesson: imperative text in a `reason` field becomes a continuation command).

### Host capability tiers

The gate mechanism is host-aware. Not every host can hard-block a stop.

| Tier | Hosts | Gate mechanism |
|---|---|---|
| 1: hard block | Claude Code, Codex CLI, OpenAI Codex API, Continue.dev | `{"decision":"block"}` / exit 2 |
| 2: follow-up inject | Cursor, Pi, Kiro | agent_end follow-up message + own counter |
| 3: notify only | OpenCode, Gemini CLI, rest | systemMessage only, no enforcement |

Hosts without a blocking Stop hook still get autonomous mode (low recitation + ledger). They do not get gate enforcement; the gate degrades to a notification. This is documented honestly: the gate is real enforcement only on Tier 1.

### Runaway guards

The gate carries its own guards so a runaway loop cannot run unbounded, independent of any undocumented host behavior:

- Persistent block counter in `.planning/<id>/.stop_blocks`, reset at init-session. Without the reset, a previous run's count would let the next run stop instantly.
- Cap (default 20) on consecutive blocks. At the cap, the gate allows the stop.
- Stall detection: no new ledger line since the previous block means the model is not progressing, so the gate allows the stop.
- `stop_hook_active` and the host block cap are backstops, not the primary guard. The counter and stall detector are deterministic and do not depend on undocumented platform fields.

### Ledger contract summary

In autonomous and gated mode the raw `progress.md` tail injection is replaced by a synthesized summary from `scripts/ledger-summary.sh`. The summary reports tick count, phase complete/total, the in_progress phase heading, and the last event type per agent. No free text from disk reaches the model context, and the block carries no timestamps, so it is KV-cache stable by construction.

The machine ledger lives at `.planning/<id>/ledger-<agent>.jsonl`, append-only, one JSON object per line. Workers append to their own ledger; the orchestrator owns `task_plan.md`. The gate's stall detector reads the ledger (a semantic signal) rather than `progress.md` mtime (which moves on any touch). See `scripts/ledger-append.sh` and `scripts/ledger-summary.sh`.

### Trying it

```bash
# autonomous: low recitation + default-on attestation + ledger summary
sh scripts/init-session.sh --autonomous "Long Research Run"

# gated: autonomous behavior plus the completion gate
sh scripts/init-session.sh --gated "Build Pipeline"
```
