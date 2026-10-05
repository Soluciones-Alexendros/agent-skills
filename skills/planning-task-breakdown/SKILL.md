---
name: planning-task-breakdown
description:
  "Decompose work into small, verifiable tasks with explicit acceptance criteria. Good task breakdown is the difference between an agent that completes work reliably and one that produces a tangled mess. Every task should be small enough to implement, test, and verify in a single focused session. Use when you have a spec to break into implementable units or when work must be parallelized. Not for single-file changes with obvious scope.

  "
license: MIT
metadata:
  author: addyosmani (adapted)
  version: 3.0.0
  domain: planning
  type: atomic
  language: en
  keywords: planning-task-breakdown
compatibility: opencode, codex, cursor, copilot
allowed-tools: Read, Grep, Glob, Bash, Write
---

# Planning and Task Breakdown

## Overview

Decompose work into small, verifiable tasks with explicit acceptance criteria.
Good task breakdown is the difference between an agent that completes work reliably
and one that produces a tangled mess. Every task should be small enough to implement,
test, and verify in a single focused session.

## When to Use

- You have a spec and need to break it into implementable units.
- A task feels too large or vague to start.
- Work must be parallelized across agents or sessions.
- Implementation order is unclear, or scope must be communicated to a human.

**When NOT to use:** single-file changes with obvious scope, or when the spec
already contains well-defined tasks.

## Process

### 1. Plan in read-only mode

Read the spec and relevant codebase sections. Identify existing patterns, map
component dependencies, and note risks and unknowns. Do NOT write code during
planning. The output is a plan document plus a task list, not implementation.

### 2. Map dependencies

Sketch the dependency graph (foundations at the bottom) and implement
bottom-up. Graph pattern and sizing rules: [task-patterns](references/task-patterns.md).

### 3. Slice vertically

Build one complete feature path at a time (schema + API + UI per slice), so
each task delivers working, testable functionality. Comparison and examples:
[task-patterns](references/task-patterns.md).

### 4. Write tasks

One task = one outcome, with acceptance criteria, verification steps,
dependencies, likely files, and a size estimate (XS-M preferred; split L+).
Full field template: [plan-templates](references/plan-templates.md).

### 5. Order and checkpoint

Satisfy dependencies, keep every task leaving the system working, put
high-risk tasks early (fail fast), and add a verification checkpoint every
2-3 tasks. Never overwrite an incomplete plan for different work:

- Same work being replanned → update the existing files in place.
- Different work → **stop and ask** before touching existing `tasks/` files.

Checkpoint and plan-document templates: [plan-templates](references/plan-templates.md).

## Tools

- `Read`, `Grep`, `Glob`: inspect the spec and codebase during planning.
- `Write`: create `tasks/plan.md` and the task list target (default `tasks/todo.md`).
- `Bash`: run the repo's focused-test and build commands for verification.

## References

- [Task patterns: dependency graphs, vertical slicing, sizing](references/task-patterns.md)
- [Plan templates: task fields, checkpoints, plan document, output files](references/plan-templates.md)
- [Anti-patterns: parallelization, rationalizations, red flags, verification](references/anti-patterns.md)

## Examples

Vertical slices for an accounts feature:

```text
Task 1: User can register (schema + API + UI for registration)
Task 2: User can log in (auth schema + API + UI for login)
Task 3: User can create a task (task schema + API + UI for creation)
```

Checkpoint after Tasks 1-3:

```text
## Checkpoint: After Tasks 1-3
- [ ] All tests pass
- [ ] Application builds without errors
- [ ] Core user flow works end-to-end
- [ ] Review with human before proceeding
```
