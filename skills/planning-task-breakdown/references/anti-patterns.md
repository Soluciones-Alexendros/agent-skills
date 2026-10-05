# Anti-Patterns and Verification

Parallelization rules, common rationalizations, red flags, and the
pre-implementation verification checklist for the planning-task-breakdown skill.

## Parallelization Opportunities

When multiple agents or sessions are available:

- **Safe to parallelize:** independent feature slices, tests for
  already-implemented features, documentation.
- **Must be sequential:** database migrations, shared state changes,
  dependency chains.
- **Needs coordination:** features that share an API contract (define the
  contract first, then parallelize).

## Common Rationalizations

| Rationalization                | Reality                                                                                      |
| ------------------------------ | -------------------------------------------------------------------------------------------- |
| "I'll figure it out as I go"   | That's how you end up with a tangled mess and rework. 10 minutes of planning saves hours.    |
| "The tasks are obvious"        | Write them down anyway. Explicit tasks surface hidden dependencies and forgotten edge cases. |
| "Planning is overhead"         | Planning is the task. Implementation without a plan is just typing.                          |
| "I can hold it all in my head" | Context windows are finite. Written plans survive session boundaries and compaction.         |

## Red Flags

- Starting implementation without a written task list.
- Overwriting a `tasks/plan.md` or `tasks/todo.md` that still has unchecked
  tasks for different work, without asking.
- Writing `tasks/todo.md` when the project has designated an external tracker
  (or scattering tasks across both).
- Tasks that say "implement the feature" without acceptance criteria.
- No verification steps in the plan.
- All tasks are XL-sized.
- No checkpoints between tasks.
- Dependency order is not considered.

## Verification Checklist

Before starting implementation, confirm:

- Every task has acceptance criteria.
- Every task has a verification step.
- Task dependencies are identified and ordered correctly.
- Tasks are recorded in the task list target (default `tasks/todo.md`).
- No pre-existing incomplete plan was overwritten without explicit user
  confirmation.
- No task touches more than ~5 files.
- Checkpoints exist between major phases.
- The human has reviewed and approved the plan.

Acceptance criteria are per-task and answer "did we build the right thing?".
They sit on top of the project-wide Definition of Done, the standing bar every
task clears before it counts as done.
