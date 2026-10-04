---
name: operate-release
description: >-
  Closes a GitHub repository: version publication, CI/CD audit, or close of work at the end of
  a plan (repo ending, merge the plan, ship). Use when the topic is semantic versioning, Keep a
  Changelog, supply-chain of Actions, Husky+e2e+PR+merge-watch post-plan. Not for implementing
  product features or forges distinct from github.com.
license: MIT
metadata:
  author: "Soluciones-Alexendros (adapted)"
  version: "2.0.0"
  domain: operate
  type: atomic
  language: en
---

# Operate Release

## Overview

Closes a GitHub repository: version publication, CI/CD audit, or close of work
at the end of a plan (repo ending, merge the plan, ship). Use when the topic is semantic
versioning, Keep a Changelog, supply-chain of Actions, Husky+e2e+PR+merge-watch post-plan.

## When to Use

- Semantic versioning
- Keep a Changelog
- Supply-chain of Actions
- Husky+e2e+PR+merge-watch post-plan

## Not for:

- Implementing product features
- Forges distinct from github.com

## Closure Flow

```text
End of plan
       │
       ▼
Version publication
       │
       ▼
CI/CD audit
       │
       ▼
Husky+e2e+PR+merge-watch
```

## Tools

- `scripts/review-vs-plan.py` — contrast plan vs execution when closing work.
