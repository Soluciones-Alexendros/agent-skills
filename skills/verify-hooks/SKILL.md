---
name: verify-hooks
description: Configure and run local git hooks (Husky, lint-staged, Prettier, typecheck, tests in pre-commit; e2e in pre-push if they exist). Use when the operator wants pre-commit hooks, husky, lint-staged or the local gate of a work close. Not for CI pipelines (→ operate-release) nor e2e test authorship.
license: MIT
metadata:
  author: Soluciones-Alexendros (adapted)
  version: 3.0.0
  domain: verify
  type: atomic
  language: en
  keywords: verify-hooks
compatibility: opencode, codex, cursor, copilot
allowed-tools: Read, Grep, Glob, Bash, Write
---

# Verify Hooks

## Overview

Configure and run local git hooks (Husky, lint-staged, Prettier, typecheck, tests in pre-commit;
e2e in pre-push if they exist). Use when the operator wants pre-commit hooks, husky, lint-staged
or the local gate of a work close.

## When to Use

- When pre-commit hooks are wanted
- To configure Husky
- To configure lint-staged
- To add formatting/typechecking/testing in commit

## Not for:

- GitHub CI (→ operate-release)

## Workflow

```text
Development phase
       │
       ▼
Pre-commit hooks
       │
       ▼
Pre-push hooks (optional)
       │
       ▼
Work closure
```

## Husky + lint-staged

- Pre-commit: `husky add` to add hooks
- lint-staged: Formats and validates only staged files
- Typecheck: Integration with TypeScript/Flow

## Pre-push e2e

- If e2e config exists in pre-push, it runs
- Useful for critical validations before merge

## Tools

- `scripts/gate-husky.sh` — local pre-commit/pre-push gate (Husky + lint-staged).
