# Smells and Heuristics

A language-neutral inspection guide derived from the heuristics in *Clean Code*.
Use it to select and review changes, not to generate a larger diff automatically.
A smell is evidence to investigate; it is not proof that a transformation is safe
or beneficial.

## Triage

- **P0 — correctness risk:** hidden side effects, swallowed errors, broken ownership,
  duplicated sources of truth or unclear contracts that can cause defects.
- **P1 — comprehension and change cost:** misleading names, mixed responsibilities,
  deep nesting and repeated decisions that make the current task harder.
- **P2 — structural friction:** leakage across boundaries, weak cohesion and
  abstractions that no longer match real variation.
- **P3 — hygiene:** stale comments, dead code, formatting noise and redundant
  elements with low behavioral risk.

Address in-scope P0/P1 items with verification first. Fix P2 only when the task
and safety net support it. Bundle P3 only when it remains easy to review. Record
out-of-scope findings instead of silently expanding the change.

## Comments and documentation

- [ ] Comments explain why, intent or constraints rather than narrating syntax.
- [ ] No comment contradicts the code it describes.
- [ ] No journal, attribution noise, decorative banners or position markers remain.
- [ ] Commented-out code has no active operational purpose and can be recovered
      from version control before deletion.
- [ ] Public documentation matches actual contracts and behavior.
- [ ] TODOs have clear relevance; they are not used to avoid a required fix.

## Names

- [ ] Names reveal intent and use the domain's established vocabulary.
- [ ] Similar names represent genuinely different concepts.
- [ ] No misleading type hints, encoding, arbitrary prefixes or mental mappings.
- [ ] Names are searchable and consistent across declarations, callers and tests.
- [ ] Boolean names read naturally at decision points.
- [ ] Public and serialized names remain compatible unless migration is in scope.

## Functions and control flow

- [ ] Each function has one coherent responsibility and abstraction level.
- [ ] The caller can understand the main flow without chasing trivial indirection.
- [ ] Arguments form a clear contract; flags do not select hidden behaviors.
- [ ] Queries do not unexpectedly mutate and commands do not hide meaningful results.
- [ ] Guard clauses reduce nesting without changing evaluation order.
- [ ] Switch/conditional structures match real variation and are not speculative.
- [ ] Temporary variables add clarity and do not prolong mutable state unnecessarily.
- [ ] Resource acquisition, use and release remain paired on every path.

## Duplication and abstraction

- [ ] Repeated knowledge has one authoritative representation.
- [ ] Similar code with different reasons to change is not forced together.
- [ ] Base classes and shared helpers contain real common behavior, not conveniences
      that couple unrelated consumers.
- [ ] Every abstraction names a present concept or variation.
- [ ] No wrapper merely forwards calls without adding boundary value.
- [ ] The solution uses the fewest elements that remain expressive and testable.

## Objects, classes and modules

- [ ] State and behavior that protect the same invariant are cohesive.
- [ ] Classes do not expose mutable internals while claiming to enforce invariants.
- [ ] Feature envy and message chains reveal whether behavior belongs elsewhere.
- [ ] Dependencies point toward stable concepts rather than incidental details.
- [ ] Static/global state is not hiding lifecycle, testing or concurrency problems.
- [ ] Constructors perform valid initialization without hidden expensive work.
- [ ] No speculative extension points remain without a present requirement.

## Data and boundaries

- [ ] Transport shapes are explicit where external contracts require them.
- [ ] Third-party types and errors do not leak farther than the project intends.
- [ ] Input validation occurs at the trust boundary without duplicate drift.
- [ ] Boundary mappings preserve unknown fields, defaults and compatibility rules.
- [ ] Time zones, units, precision and empty/absent values are unambiguous.
- [ ] External calls have deliberate timeout, retry, cancellation and error behavior
      according to the existing application contract.

## Error handling

- [ ] No empty catch/except blocks or ignored error results remain.
- [ ] Errors include actionable operation context without sensitive data.
- [ ] Error translation preserves causes and the caller's expected contract.
- [ ] Happy-path flow is clear, but failure behavior has not been weakened.
- [ ] Nulls and sentinel values are deliberate and idiomatic, not accidental.
- [ ] Cleanup and rollback occur on both success and failure paths.

## Tests

- [ ] Tests assert observable behavior rather than irrelevant implementation detail.
- [ ] Tests are Fast, Independent, Repeatable, Self-validating and Timely.
- [ ] Test names and setup make the scenario understandable.
- [ ] Failing tests are investigated, never weakened to accommodate a refactor.
- [ ] Characterization tests cover risky behavior before structural changes.
- [ ] Focused and full-suite results are reported exactly as executed.

Use → plan-validation to author or repair tests and → project-testing for a
whole-suite quality assessment.

## Concurrency and runtime

- [ ] Shared mutable state has explicit ownership and synchronization.
- [ ] Critical sections protect the complete invariant without unnecessary work.
- [ ] Visibility, atomicity and ordering rely on documented runtime guarantees.
- [ ] Cancellation, shutdown, timeout and backpressure semantics are preserved.
- [ ] No new concurrency model or optimization is disguised as cleanup.

Read [systems-emergence-concurrency.md](systems-emergence-concurrency.md) before
acting on these findings. Treat concurrency changes as behavioral and verify them
through → plan-validation.

## Final review questions

1. Is the changed code easier to explain to the next reader?
2. Was every modification justified by a named smell or requirement?
3. Did the diff avoid unrelated files, reformatting and speculative abstractions?
4. Are APIs, data, errors, side effects and ordering preserved as required?
5. Did every relevant check run and pass, or is the limitation stated plainly?
6. Are remaining smells documented rather than hidden or half-refactored?
