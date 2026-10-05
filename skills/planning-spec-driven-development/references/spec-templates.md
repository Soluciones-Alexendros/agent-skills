# Spec Templates and Worked Examples

Companion to `planning-spec-driven-development`. Full-size templates and examples kept out of the SKILL.md body.

## Capability Map (Phase 0)

```text
# Capability Map: [Initiative Name]

| Module id | Responsibility | Depends on |
|-----------|----------------|------------|
| identity  | Accounts, sessions, SSO | — |
| billing   | Plans, invoices, payments | identity |
| notifications | Email and webhook fan-out | identity |
| reporting  | Usage dashboards | billing, notifications |

Build order: identity → billing, notifications → reporting
```

Rules:

- **Stable module ids.** Kebab-case, chosen once, never renamed mid-initiative.
- **Dependency direction, no cycles.** Arrows point one way.
- **Interfaces live at the boundary.** The map records that `billing` depends on `identity`; the contract between them belongs in the provider module's spec.
- **The map is gated like every phase.** The human reviews module boundaries, dependency direction, and build order before any module spec is written.
- **Recurse per module.** Run Specify → Plan → Tasks → Implement for each module in dependency order. Save the approved map at the project root and each module's spec alongside it, named by module id (`SPEC-identity.md`, `SPEC-billing.md`).

## Assumptions Block (Phase 1)

```text
ASSUMPTIONS I'M MAKING:
1. This is a web application (not native mobile)
2. Authentication uses session-based cookies (not JWT)
3. The database is PostgreSQL (based on existing Prisma schema)
4. We're targeting modern browsers only (no IE11)
→ Correct me now or I'll proceed with these.
```

## Commands Snippet

```text
Build: npm run build
Test: npm test -- --coverage
Lint: npm run lint --fix
Dev: npm run dev
```

List full executable commands with flags, not just tool names.

## Project Structure Snippet

```text
src/           → Application source code
src/components → React components
src/lib        → Shared utilities
tests/         → Unit and integration tests
e2e/           → End-to-end tests
docs/          → Documentation
```

## Full Spec Template

```text
# Spec: [Project/Feature Name]

## Objective
[What we're building and why. User stories or acceptance criteria.]

## Tech Stack
[Framework, language, key dependencies with versions]

## Commands
[Build, test, lint, dev — full commands]

## Project Structure
[Directory layout with descriptions]

## Code Style
[Example snippet + key conventions]

## Testing Strategy
[Framework, test locations, coverage requirements, test levels]

## Boundaries
- Always: [...]
- Ask first: [...]
- Never: [...]

## Success Criteria
[How we'll know this is done — specific, testable conditions]

## Open Questions
[Anything unresolved that needs human input]
```

Boundary defaults: always run tests before commits, follow naming conventions, validate inputs; ask first for schema changes, new dependencies, CI config changes; never commit secrets, edit vendor directories, or remove failing tests without approval.

## Plan Output Convention

Save the plan to `tasks/plan.md` and record the task list in the task target defined by → planning-task-breakdown (default `tasks/todo.md`; projects may designate an external tracker instead). Create `tasks/` if it does not exist. The plan must be reviewable: the human reads it and says "yes, that's the right approach" or "no, change X."

## Task Template

```text
- [ ] Task: [Description]
  - Acceptance: [What must be true when done]
  - Verify: [How to confirm — test command, build, manual check]
  - Files: [Which files will be touched]
```
