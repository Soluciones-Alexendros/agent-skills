---
name: planning-test-driven-development
description:
  "Drive development with tests using the red-green-refactor loop. Use when implementing any logic, fixing any bug, or changing any behavior. Use when you need to prove that code works, when a bug report arrives, or when you're about to modify existing functionality. Not for pure configuration changes, documentation updates, or static content.

  "
license: MIT
metadata:
  author: addyosmani (adapted)
  version: 3.0.0
  domain: planning
  type: atomic
  language: en
  keywords: planning-test-driven-development
compatibility: opencode, codex, cursor, copilot
allowed-tools: Read, Grep, Glob, Bash, Write
---

# Test-Driven Development

## Overview

Write a failing test before writing the code that makes it pass.
For bug fixes, reproduce the bug with a test before attempting a fix.
Tests are proof — "seems right" is not done.

## When to Use

- Implementing any new logic or behavior
- Fixing any bug (the Prove-It pattern)
- Modifying existing functionality or adding edge case handling
- Any change that could break existing behavior

When NOT to use: pure configuration changes, documentation updates, or
static content changes.

## Process

### 1. Discover the stack

The TDD cycle is universal; the commands are not. Before the first test,
learn how this repository tests: the language and build file (`package.json`,
`pom.xml`/`build.gradle`, `pyproject.toml`, `go.mod`, `Cargo.toml`, `Gemfile`,
`Makefile`), checked-in wrappers (`./gradlew`, `./mvnw`, `make test`), the test
framework and its focused-test vs full-suite commands, test locations and
naming conventions, and documented commands in README, CONTRIBUTING, and CI
workflows. Never assume a default like `npm test`.

### 2. RED — write a failing test

Write the test first. It must fail. A test that passes immediately proves
nothing — run it and confirm the failure.

### 3. GREEN — make it pass

Write the minimum code to make the test pass. Do not over-engineer.

### 4. REFACTOR — clean up

With tests green, improve naming, extract shared logic, and remove duplication
without changing behavior. Run tests after every refactor step.

### 5. Prove-It pattern for bug fixes

Do not start by fixing. Write a reproduction test first, confirm it fails
(bug confirmed), implement the fix, confirm it passes, then run the full
suite to check for regressions.

## Tools

- Run the focused-test command during the loop; run the full-suite command
  before finishing.
- For code that runs in a browser, add runtime verification with Chrome
  DevTools MCP: DOM inspection, console logs, network requests, performance
  traces, and screenshots.
- For complex bugs, spawn a subagent to write the reproduction test without
  knowledge of the fix, then verify it fails before implementing the fix.

## References

- skills/planning-test-driven-development/references/test-pyramid-and-sizes.md — pyramid, test sizes, decision guide.
- skills/planning-test-driven-development/references/writing-good-tests.md — state-based tests, DAMP, doubles, AAA, naming, anti-patterns.
- skills/planning-test-driven-development/references/rationalizations-and-flags.md — rationalizations, red flags, verification checklist.
- For JavaScript/TypeScript patterns (Jest, React Testing Library, Supertest, Playwright), see references. The principles transfer; the syntax there is JS/TS-specific.

## Examples

TDD cycle:

```text
// RED: fails because createTask does not exist yet
const task = await taskService.createTask({ title: 'Buy groceries' });
expect(task.status).toBe('pending');

// GREEN: minimal implementation
export async function createTask(input) {
  const task = {
    id: generateId(),
    title: input.title,
    status: 'pending',
    createdAt: new Date(),
  };
  await db.tasks.insert(task);
  return task;
}
// REFACTOR: clean up with tests green; re-run after each step.
```

Bug fix (Prove-It):

```text
// 1. Reproduction test — must FAIL before the fix
it('sets completedAt when task is completed', async () => {
  const task = await taskService.createTask({ title: 'Test' });
  const completed = await taskService.completeTask(task.id);
  expect(completed.completedAt).toBeInstanceOf(Date);
});
// 2. Fix: set completedAt in completeTask. Test passes; run full suite.
```
