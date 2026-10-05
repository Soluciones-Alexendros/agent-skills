# Plan Templates

Copy-paste templates for tasks, checkpoints, and the plan document, plus the
output-file rules. Referenced by the planning-task-breakdown skill.

## Task Structure

Each task follows this structure, whether it lands in the markdown task list
or as an item in an external tracker:

```text
## Task [N]: [Short descriptive title]

**Description:** One paragraph explaining what this task accomplishes.

**Acceptance criteria:**
- [ ] [Specific, testable condition]
- [ ] [Specific, testable condition]

**Verification:**
- [ ] Tests pass: [the repository's focused-test command]
- [ ] Build succeeds: [the repository's build command]
- [ ] Manual check: [description of what to verify]

**Dependencies:** [Task numbers this depends on, or "None"]

**Files likely touched:**
- `src/path/to/file.ts`
- `tests/path/to/test.ts`

**Estimated scope:** [Small: 1-2 files | Medium: 3-5 files | Large: 5+ files]
```

## Checkpoint Template

Add explicit checkpoints to the task list target every 2-3 tasks:

```text
## Checkpoint: After Tasks 1-3
- [ ] All tests pass
- [ ] Application builds without errors
- [ ] Core user flow works end-to-end
- [ ] Review with human before proceeding
```

Arrange tasks so dependencies are satisfied, each task leaves the system in a
working state, and high-risk tasks come early (fail fast).

## Output Files

- **Plan document:** save the implementation plan to `tasks/plan.md`. This is
  always a markdown file — design decisions, risks, and open questions do not
  map cleanly onto individual tracker issues.
- **Task list:** record each task in the task list target (defined below).

Create the `tasks/` directory if it does not exist.

**Never overwrite an incomplete plan.** Before writing `tasks/plan.md` or
`tasks/todo.md`, check whether they already exist and still contain unchecked
tasks:

- Same work being replanned (the user asked to revise or extend this plan)
  → update the existing files in place.
- Different work → **stop and ask.** The unchecked tasks may be mid-build in
  another session. Do not delete, overwrite, or rename the existing files on
  your own; present the conflict and let the user decide (finish the old plan
  first, explicitly discard it, or tell you where the new plan should go).

The same rule applies to an external task list target: never bulk-close or
delete another plan's open tracker items to make room for new ones.

## Task List Target

The task list target is where tasks and checkpoints are recorded. It is
defined once, here; every other reference in this skill defers to it.

- **Default: a checklist-style markdown file at `tasks/todo.md`.** This is the
  convention the `/build` command and other downstream tooling expect. Use it
  unless the project says otherwise.
- **External tracker:** if the project's agent rules (`AGENTS.md`, etc.) or
  the user designate an issue tracker (e.g. GitHub Issues, Jira, Linear,
  `bd`/beads), create one tracker item per task instead of writing
  `tasks/todo.md`. Map the task structure onto the tracker's fields:
  acceptance criteria and verification steps in the item body, dependencies via
  the tracker's linking mechanism (`bd dep add`, "blocked by", etc.). Record
  checkpoints as tracker items too, or as a checklist in the plan document if
  the tracker has no natural equivalent.

When using an external tracker, note it in `tasks/plan.md` (e.g. "Tasks
tracked in Linear project FOO") so downstream steps and future sessions know
where to look, and keep the plan document's Task List section as an ordered
index of tracker item IDs or links rather than a duplicate checklist.

## Plan Document Template

```text
# Implementation Plan: [Feature/Project Name]

## Overview
[One paragraph summary of what we're building]

## Architecture Decisions
- [Key decision 1 and rationale]
- [Key decision 2 and rationale]

## Task List

### Phase 1: Foundation
- [ ] Task 1: ...
- [ ] Task 2: ...

### Checkpoint: Foundation
- [ ] Tests pass, builds clean

### Phase 2: Core Features
- [ ] Task 3: ...
- [ ] Task 4: ...

### Checkpoint: Core Features
- [ ] End-to-end flow works

### Phase 3: Polish
- [ ] Task 5: ...
- [ ] Task 6: ...

### Checkpoint: Complete
- [ ] All acceptance criteria met
- [ ] Ready for review

## Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| [Risk] | [High/Med/Low] | [Strategy] |

## Open Questions
- [Question needing human input]
```

When tasks live in an external tracker, keep the Task List section above as an
ordered index of tracker item IDs or links instead of a duplicate checklist.
