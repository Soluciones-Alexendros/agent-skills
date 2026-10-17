# Core Clean Code Principles

Operational synthesis of the foundational chapters of Robert C. Martin's
*Clean Code*. Use these as judgment aids, not mechanical quotas. Existing
project conventions, language semantics and verified behavior take precedence.

## Meaningful names

A name should answer what the value represents, why it exists and how it is used.

- Reveal intention and domain meaning; avoid names requiring a comment to decode.
- Avoid disinformation: misleading types, near-identical names and ambiguous
  abbreviations are worse than longer explicit names.
- Make distinctions meaningful. `data`, `info`, `item`, `value` and numeric
  suffixes rarely distinguish responsibilities by themselves.
- Prefer pronounceable, searchable names and a consistent term for each concept.
- Avoid type encodings, Hungarian notation and decorative prefixes when the type
  system and project conventions already express that information.
- Use nouns or noun phrases for values/types and verbs or verb phrases for actions
  when that matches the language's conventions.
- Do not be cute, clever or culturally obscure at the reader's expense.
- When renaming, update declarations, references, tests, serialization mappings,
  dependency-injection keys and documentation as applicable. A textual rename is
  not always behavior-preserving at external boundaries.

## Functions and methods

Small means one coherent responsibility at one level of abstraction, not an
arbitrary maximum number of lines.

- Keep the main flow readable; move lower-level details behind intention-revealing
  operations when that removes cognitive switching.
- Prefer zero to two parameters where practical. Group parameters only when they
  form a real domain concept, not an anonymous bag used to reduce the count.
- Avoid boolean flags that select two different behaviors; separate the operations
  when callers and tests become clearer.
- Make side effects explicit. A query should not unexpectedly mutate state and a
  command should not hide a meaningful result.
- Extract repeated decisions or algorithms, not merely repeated text. Similar code
  with different reasons to change may be safer apart.
- Use guard clauses for exceptional paths when they reduce nesting; do not flatten
  code at the cost of losing important structure.
- Prefer structured control flow and language-idiomatic constructs. Do not extract
  so aggressively that the reader must reconstruct trivial logic across many calls.
- Preserve evaluation order, laziness, short-circuiting, numeric precision and
  error behavior when extracting or reordering expressions.

## Comments

The best cleanup is often to make a comment unnecessary through clearer code.

- Keep comments that explain intent, rationale, trade-offs, external constraints,
  warnings or consequences not expressible in the code.
- Remove comments that repeat the code, restate obvious syntax, record history,
  mark positions decoratively or have become stale.
- Remove commented-out code when version control preserves it and its intent is
  no longer needed; do not delete examples or disabled configuration with a
  documented operational purpose without confirmation.
- Do not use a comment to excuse a confusing name or a function with mixed
  responsibilities when a safe code improvement is available.
- Update comments affected by every refactor. An accurate comment is useful; an
  outdated explanation is active disinformation.

## Formatting

Formatting supports comprehension and review; it is not a separate aesthetic
rewrite.

- Follow the project's formatter, line width, import ordering and file conventions.
- Keep related concepts vertically close and use whitespace to separate distinct
  thoughts where the formatter permits.
- Preserve the team's established declaration and dependency ordering.
- Avoid manual alignment or large formatting-only diffs that obscure a behavioral
  review. Use the existing automated formatter rather than imposing a new style.

## Objects and data structures

Choose deliberately between encapsulating behavior and exposing data.

- Objects expose intention through operations while hiding representation;
  data structures expose data with little or no behavior.
- Avoid hybrids that expose mutable internals while also pretending to enforce
  invariants through methods.
- Tell an object what to do when it owns the invariant; avoid chains that reach
  through several collaborators merely to inspect their data.
- Apply the Law of Demeter as a coupling warning, not a ban on fluent APIs or
  composed value access. Distinguish navigation from trains of implementation detail.
- Use DTOs at process, network, persistence or serialization boundaries when the
  project needs explicit transport shapes; do not add them to every internal call.
- Preserve equality, hashing, mutability and serialization semantics when changing
  representation or encapsulation.

## Error handling

Error paths are part of the public behavior and deserve the same clarity as the
happy path.

- Never silently swallow failures. Handle, translate or propagate them with enough
  context for the intended caller to act.
- Use exceptions, result types, optionals or explicit error values according to
  the language and existing project contracts; do not impose Java idioms elsewhere.
- Separate normal flow from failure handling when it improves comprehension, but
  preserve which errors are recoverable and which must escape.
- Avoid fragile sentinel returns when the language offers a clear native alternative.
  Do not change a public null/error contract as a cleanup without explicit approval.
- Do not pass or return null merely to avoid defining an empty result. Prefer an
  empty collection or explicit absence only when that is already the contract.
- Include operation and contextual identifiers in errors, never secrets or sensitive
  payloads. Preserve error causes and diagnostic context when translating failures.

## Boundaries and third-party code

Keep external decisions from leaking unintentionally through the codebase.

- Learn and test the external API at the boundary rather than scattering assumptions
  through domain logic.
- Use an existing adapter when one exists. Add a narrow wrapper only when it protects
  a project-owned concept, centralizes error translation or reduces repeated coupling.
- Avoid returning third-party types broadly when a small project-owned abstraction
  already makes the boundary clearer.
- Distinguish real interfaces from hypothetical future providers. Do not create
  layers solely because a dependency might someday change.
- Keep input validation and external error translation at the trust boundary while
  preserving the contract expected by callers.

## Unit tests

Tests are executable examples and a safety net for refactoring, not an afterthought.

- Aim for Fast, Independent, Repeatable, Self-validating and Timely tests.
- Keep tests readable: arrange, act and assert around one observable behavior.
- Assert meaningful outcomes rather than implementation details whenever possible.
- Do not weaken, delete or rewrite a failing assertion merely to make cleanup pass.
- For test authoring, red-green-refactor and bug reproduction, use → plan-validation.
  For whole-suite strategy and quality assessment, use → project-testing.

## Classes and cohesive modules

A class or module should have a focused reason to change and collaborators that
support the same abstraction.

- Prefer high cohesion: related state and behavior belong together.
- Split responsibilities when independent reasons to change are visible, not just
  because a file exceeds a preferred size.
- Keep dependencies directed and understandable. Introduce abstractions where they
  clarify a real variation or boundary, not for speculative reuse.
- Depend on stable project-owned concepts at meaningful boundaries when the existing
  architecture supports it; avoid blanket dependency-inversion rewrites.
- Preserve encapsulation, initialization order and lifecycle semantics when moving
  responsibilities between classes or modules.
- Prefer the smallest design that passes the tests, removes meaningful duplication
  and expresses intent clearly.
