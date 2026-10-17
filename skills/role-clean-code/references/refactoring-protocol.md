# Behavior-Preserving Refactoring Protocol

Refactoring changes structure without changing observable behavior. Read this
protocol before modifying existing code with `role-clean-code`.

## Choose the task type first

| Task | Primary rule | Handoff |
| --- | --- | --- |
| New code | Apply Clean Code as behavior is implemented | Use → plan-validators for the behavior loop |
| Pure refactor | Preserve APIs and observable behavior step by step | Stay in this protocol |
| Bug fix or feature plus cleanup | Separate behavioral and structural edits | Lead with → plan-validators, then refactor with tests green |
| Broad architectural redesign | Confirm scope and migration strategy | Use → project-architecture first |
| Security-sensitive change | Treat security behavior as an invariant | Use → web-owasp for the review |

If the operator asks for both cleanup and a behavior change, make the distinction
explicit. Do not hide a behavior change behind the word "refactor".

## Preconditions

1. Read project instructions and the target's surrounding call sites.
2. Identify public signatures, wire formats, schemas, logs consumed operationally,
   side effects, ordering, errors and performance constraints that can be observed.
3. Discover and run the narrowest meaningful baseline command, then the broader
   suite when practical. Record pre-existing failures rather than blaming them on
   the refactor or silently fixing them.
4. Check for generated, vendored or externally synchronized files and exclude them
   unless the project explicitly expects edits there.
5. Keep the requested files and risk level bounded. Expand only with authorization.

## When coverage is insufficient

Lack of coverage is a risk to manage, not proof that refactoring is safe.

- For important behavior with an existing test framework, add characterization
  tests through → plan-validators before structural edits. Characterization tests
  document current observable behavior; they do not declare every current behavior
  desirable.
- For generated or trivial presentational changes, use the project's established
  build, typecheck, snapshot or rendering checks where applicable.
- If no meaningful verification exists and the transformation can affect behavior,
  narrow to a safer edit or ask the operator before proceeding.
- If the operator accepts the risk, state exactly what remains unverified. Never
  print "behavior preserved" without supporting evidence.

Do not create a new test framework solely for a small cleanup. Follow the project's
existing toolchain and conventions.

## Transformation loop

For each improvement:

1. **Name the obstacle.** Example: the function mixes validation with persistence,
   or two names suggest different concepts for the same value.
2. **Choose one transformation.** Prefer the smallest step that addresses it.
3. **Predict invariants.** Note which API, output, ordering and side effects must
   remain unchanged, including subtle language semantics.
4. **Edit narrowly.** Avoid combining the step with unrelated formatting or features.
5. **Run the focused check.** Inspect any failure before continuing; do not adjust
   tests to match an accidental change.
6. **Review the diff.** Confirm the code is clearer and the next step is still safe.
7. **Stop at sufficient.** Further polish is optional only while it adds clear value
   within scope.

## Useful transformations and their cautions

### Rename for intent

Update every reference and check reflection, dependency injection, templates,
serialization and external integrations. Public renames may require a migration
or compatibility alias rather than a simple replacement.

### Extract a responsibility

Extract when the new unit has a coherent name and hides lower-level detail. Keep
arguments and captured state explicit. Preserve closure scope, `this`/receiver
binding, laziness, exception timing and resource lifetime.

### Inline obscuring indirection

Remove a wrapper when it adds no abstraction, protection or useful vocabulary.
Check dynamic dispatch, overrides, instrumentation and public callers first.

### Introduce guard clauses

Useful for invalid or exceptional paths when nesting falls. Preserve the exact
condition evaluation order and side effects; do not reorder checks that can throw
or consume resources.

### Consolidate duplication

Unify duplicated decisions, not just similar lines. Confirm both copies have the
same reason to change and identical semantics for every input, including errors,
empty values and boundary conditions.

### Introduce a parameter object or value object

Do so only when the values form a meaningful concept with coherent validation or
behavior. Preserve construction, equality and serialization contracts.

### Replace conditional complexity

Use polymorphism, strategy objects, lookup tables or pattern matching only when
they fit the existing design and make a real variation clearer. A class hierarchy
is not automatically cleaner than a short conditional.

### Isolate an external boundary

Centralize repeated third-party error translation or data mapping when the project
benefits from its own vocabulary. Avoid wrappers that merely forward every method.

### Remove dead code and stale comments

Confirm reachability across dynamic entry points, configuration, scripts and
external callers. Version control preserves deleted history. Do not remove feature
flags, migrations or compatibility code whose lifecycle is still active.

## Behavior-preservation checklist

Review at least the dimensions relevant to the target:

- **Contracts:** signatures, types, defaults, public names, return shapes and errors.
- **Data:** serialization, persistence, migrations, equality, hashing and precision.
- **Order:** evaluation, initialization, iteration, cleanup and asynchronous completion.
- **Side effects:** I/O, logging, metrics, mutations, transactions and external calls.
- **Resources:** ownership, closing, flushing, cancellation, timeouts and retries.
- **Dynamics:** reflection, dependency injection, templates, plugins and feature flags.
- **Runtime:** concurrency, memory, complexity and performance-sensitive paths.

## Final verification and report

Run the focused checks again, then the full relevant suite, formatter/linter and
build/typecheck supplied by the project. Compare the final diff against the original
invariants and update stale documentation.

Report:

```markdown
## Clean Code changes
- <file>: <transformation and reader benefit>

## Verification
- `<command>` — PASS / FAIL / NOT RUN

## Contracts
- <explicit changes, or "None intended" plus the checks supporting preservation>

## Remaining
- <out-of-scope smells or unverified risk>
```

A failed or unrun check must remain visible in the report. Do not describe the task
as fully verified until every required gate is green.
