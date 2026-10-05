---
name: operate-lifecycle
description: "Orchestrates the work lifecycle: init-work (start of plan, repo starting), verify-hooks (Husky) or operate-release (close, publication and close of work post-plan). Use when the operator asks where to start, starts plan mode, or mixes audit, hooks, release or repo close. Do not use for executing audits, hooks or publications (→ verify-repo, verify-hooks, operate-release)."
license: MIT
metadata:
  author: Soluciones-Alexendros (adapted)
  version: 3.0.0
  domain: operate
  type: atomic
  language: en
  keywords: operate-lifecycle
compatibility: opencode, codex, cursor, copilot
allowed-tools: Read, Grep, Glob, Bash, Write
---

# Operate Lifecycle

## Overview

Routes the repository lifecycle: derives to verify-repo (diagnostics, health check and
plan start / repo starting), verify-hooks (Husky) or operate-release (close, publication
and close of work post-plan). Use when the operator asks where to start, opens plan mode,
or mixes audit, hooks, release or repo ending. Not for executing audits,
hooks or publications (→ verify-repo, verify-hooks, operate-release).

## When to Use

- When the operator asks where to start
- To open plan mode
- To mix audit, hooks, release or repo ending

## Not for:

- Executing audits (→ verify-repo)
- Executing hooks (→ verify-hooks)
- Publications (→ operate-release)

## Workflow

```text
Start work
       │
       ▼
Verify repo / hooks / release
       │
       ▼
Post-plan work closure
```
