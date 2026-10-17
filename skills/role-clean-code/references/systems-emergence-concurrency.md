# Systems, Emergence, Concurrency and Refinement

Read this reference only when the task reaches beyond local names, functions and
formatting. These topics can change architecture or runtime semantics; they are
not routine cosmetic cleanup.

## Systems and dependency composition

A clean system keeps domain policy understandable while making infrastructure
choices explicit.

- Separate object construction and dependency composition from runtime use when
  the project already has a composition root, factory or dependency-injection
  convention.
- Keep lifecycle, configuration and infrastructure setup out of domain rules when
  moving them improves clarity without changing initialization behavior.
- Use factories or dependency injection to resolve an existing construction or
  testing problem, not to add ceremony to every object.
- Delay reversible design decisions until requirements are understood; do not
  build layers for imagined scale or providers.
- Keep cross-cutting concerns behind the project's established mechanisms. Do not
  introduce aspect frameworks, event buses or service locators as a cleanup.
- Preserve startup order, teardown, lazy/eager initialization and ownership of
  resources when moving composition logic.

For a broad dependency or architecture assessment without implementation, use
→ project-architecture. For API or persistence implementation, use → role-back.

## Emergent design

Use the four rules of simple design as an ordered feedback loop:

1. **Run all relevant tests.** Correctness and observable behavior come first.
2. **Reveal intent.** Names and structure should make the domain and flow clear.
3. **Remove meaningful duplication.** Eliminate repeated knowledge and competing
   sources of truth while respecting different reasons to change.
4. **Minimize unnecessary elements.** Do not retain classes, methods, layers or
   extension points that no longer earn their complexity.

The ordering is pragmatic, not an excuse to skip tests or tolerate duplication.
A smaller design is not automatically simpler: excessive indirection can reduce
the element count while increasing cognitive load.

## Successive refinement

Clean code normally emerges through verified iterations rather than a single
large rewrite. The book's JUnit and SerialDate case studies are useful as process
examples, not as Java implementations to copy.

1. Establish a working baseline and identify one reader obstacle.
2. Make the smallest transformation that improves that obstacle.
3. Run focused checks and inspect the resulting diff.
4. Re-read the changed code in context; stop when the code is clear and further
   changes would add indirection or scope without proportional benefit.
5. Run the full relevant suite and leave behavior-compatible code ready for the
   next change.

Do not turn successive refinement into endless polishing. Time-box cleanup to the
task and record remaining opportunities separately.

## Concurrency

Concurrency cleanup can alter timing, visibility and deadlock behavior. Treat it
as a specialized behavioral change, not a formatting or extraction exercise.

- Reduce shared mutable state where the design already permits; prefer clear
  ownership and isolation over ad hoc synchronization.
- Keep synchronization scopes as small as correctness allows, but never narrow a
  critical section without proving the required invariant remains protected.
- Respect happens-before, visibility, atomicity and ordering guarantees of the
  actual language/runtime. Similar keywords have different semantics across platforms.
- Make shutdown, cancellation, timeout and error propagation explicit. Preserve
  backpressure and resource ownership when reorganizing concurrent work.
- Avoid sharing mutable objects across threads/tasks unless the synchronization
  contract is explicit and tested. Immutable snapshots may help, but copying can
  change identity, memory and performance semantics.
- Use established executors, structured concurrency, actors, channels or locks
  already present in the project. Do not introduce a new concurrency model merely
  to make code look cleaner.
- Tests should expose interleaving-sensitive behavior where the project provides
  suitable tools, but a passing stress test alone does not prove race freedom.

Before changing concurrency semantics, consult current official language or
framework documentation and use → plan-validators for the behavioral safety net.
If concurrency is outside the requested scope, document the smell and stop there.

## Final restraint check

Before finishing a system-level cleanup, ask:

- Is every new abstraction tied to a present requirement?
- Did the design become easier to explain, not merely more modular?
- Are construction, lifecycle and concurrency semantics unchanged unless an
  intentional, tested change was requested?
- Can each transformation be reviewed and verified independently?
