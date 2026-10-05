---
name: planning-spec-driven-development
description:
  "Write a structured specification before writing any code. The spec is the shared source of truth between you and the human engineer — it defines what we're building, why, and how we'll know it's done. Code without a spec is guessing. Use when starting a new project or feature, when requirements are ambiguous, or when the change touches multiple modules. Not for single-line fixes or typo corrections.

  "
license: MIT
metadata:
  author: addyosmani (adapted)
  version: 3.0.0
  domain: planning
  type: atomic
  language: en
  keywords: planning-spec-driven-development
compatibility: opencode, codex, cursor, copilot
allowed-tools: Read, Grep, Glob, Bash, Write
---

# Spec-Driven Development

## Overview

Write a structured specification before writing any code. The spec is the shared source of truth between you and the human engineer — it defines what we're building, why, and how we'll know it's done. Code without a spec is guessing.

## When to Use

- Starting a new project or feature
- Requirements are ambiguous or incomplete
- The change touches multiple files or modules
- You're about to make an architectural decision
- The task would take more than 30 minutes to implement

**When NOT to use:** Single-line fixes, typo corrections, or changes where requirements are unambiguous and self-contained.

## Process

Spec-driven development has four phases, preceded by a scope check (Phase 0) that activates only when one request bundles several independently testable capabilities. Do not advance to the next phase until the current one is validated.

```text
SPECIFY ────→ PLAN ────→ TASKS ────→ IMPLEMENT
  │          │        │          │
  ▼          ▼        ▼          ▼
Human  reviews  Human  reviews  Human  reviews  Human
reviews  │       reviews  │       reviews  │       reviews
```

### Phase 0: Scope Check

Most requests describe one capability. If this one does, skip this phase and go straight to Specify — Phase 0 exists for the exception, not the rule, and it puts no hierarchy on single-capability features.

**Detection.** Decompose before specifying when a single requirement bundles several independently testable capabilities:

- The requirement names distinct capabilities with their own consumers or data (e.g. identity, billing, notifications, reporting)
- Acceptance criteria cluster into groups that could ship and be verified separately
- One capability could be cut or replaced without rewriting the others' requirements

**Propose a capability map before writing any spec** — a small module table plus build order (stable kebab-case ids, one-way dependencies), reviewed by the human before any module spec is written. Then run Specify → Plan → Tasks → Implement per module in dependency order. Full example and naming rules: [spec-templates.md](references/spec-templates.md).

### Phase 1: Specify

Start with a high-level vision. Ask the human clarifying questions until requirements are concrete.

**Surface assumptions immediately.** Before writing spec content, list what you are assuming (stack, auth, data store, target platform) and ask the human to correct you. Never silently fill in ambiguous requirements — assumptions are the most dangerous form of misunderstanding. Example block: [spec-templates.md](references/spec-templates.md).

**Write a spec covering six areas:** Objective, Commands (full executable commands with flags), Project Structure, Code Style (one real snippet beats three paragraphs), Testing Strategy, and Boundaries (Always / Ask first / Never) — plus Success Criteria and Open Questions. Full template with example snippets: [spec-templates.md](references/spec-templates.md).

**Stop after writing the spec (CRITICAL).** Once the spec is saved:

1. Summarize it and list any Open Questions.
2. Ask the human to approve it or request changes.
3. **STOP YOUR TURN IMMEDIATELY.** Do NOT start Phase 2, invoke planning-and-task-breakdown, or write code in this turn. Planning starts only after the human approves the spec in a later turn.

### Phase 2: Plan

With the validated spec, generate a technical implementation plan:

1. Identify the major components and their dependencies
2. Determine the implementation order (what must be built first)
3. Note risks and mitigation strategies
4. Identify what can be built in parallel vs. what must be sequential
5. Define verification checkpoints between phases

> Follow → planning-task-breakdown for dependency-graph and vertical-slicing mechanics; it takes precedence over this summary.

**Output convention:** Save the plan to `tasks/plan.md` and record the task list in the task list target defined by planning-and-task-breakdown (default `tasks/todo.md; projects may designate an external tracker instead`). Create `tasks/` if it does not exist. Downstream commands (`/build`, etc.) expect these defaults.

The plan should be reviewable: the human should be able to read it and say "yes, that's the right approach" or "no, change X."

### Phase 3: Tasks

Break the plan into discrete, implementable tasks:

- Each task should be completable in a single focused session
- Each task has explicit acceptance criteria
- Each task includes a verification step (test, build, manual check)
- Tasks are ordered by dependency, not by perceived importance
- No task should require changing more than ~5 files

> Follow → planning-task-breakdown for task-sizing and dependency-ordering mechanics; it takes precedence. Task template: [spec-templates.md](references/spec-templates.md).

### Phase 4: Implement

Execute tasks one at a time following → planning-test-driven-development, delivering incrementally via → planning-task-breakdown. Load only the spec sections and source files needed per step.

Keep the spec alive: update it when decisions or scope change, commit it alongside code, and link it from PRs. Detail: [spec-quality.md](references/spec-quality.md).

## Tools

Use Read, Grep, and Glob to inspect the codebase before specifying; use Write to save specs, plans, and task lists; use Bash only to run the project's own build, test, and lint commands for verification. Related skills: → planning-task-breakdown (plan and task mechanics), → planning-test-driven-development (implementation loop), → verify-dependencies (supply-chain checks before adding dependencies), → operate-maintenance (routine upkeep context), → operate-security (defensive posture), → operate-health (system health checks).

## References

- [spec-templates.md](references/spec-templates.md) — capability map, assumptions block, spec and task templates, output conventions.
- [spec-quality.md](references/spec-quality.md) — living-spec rules, rationalizations table, red flags, verification checklist.

## Examples

Minimal capability map (full version in references):

```text
Build order: identity → billing, notifications → reporting
```

Minimal stop-gate: the spec is approved in a later turn before Plan begins; the plan is approved before Tasks; tasks are approved before Implement.
