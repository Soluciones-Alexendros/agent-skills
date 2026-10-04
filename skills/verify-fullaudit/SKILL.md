---
name: verify-fullaudit
description: >-
  Holistic web audit router: derives to verify-compliance (web compliance SEO/a11y/legal),
  verify-performance (CWV/rendering), verify-repo (health check repo) or build-interface
  (visual direction). Use when the operator requests a complete audit, holistic audit, 'review
  everything' or full audit without focus. Not for executing the specialized audits themselves; it only routes to them.
license: MIT
metadata:
  author: "Soluciones-Alexendros (adapted)"
  version: "2.3.0"
  domain: verify
  type: atomic
  language: en
---

# Verify Fullaudit

## Overview

Holistic web audit router: derives to verify-compliance (compliance SEO/a11y/legal),
verify-performance (CWV/rendering), verify-repo (health check repo) or build-interface
(visual direction). Use when the operator requests a complete audit, holistic audit, 'review
everything' or full audit without focus.

## When to Use

- When complete audit is requested
- For holistic audit without focus
- For 'review everything' or full audit

## Not for:

- Executing audits (→ verify-compliance, verify-performance, verify-repo)
- Only routes (does not execute audits themselves)

## Audit Flow

```text
Full audit request
       │
       ▼
verify-fullaudit → routes to:
  │               │
  ▼               ▼
verify-compliance  verify-performance
     │                   │
     ▼                   ▼
verify-repo        build-interface
```

## Limitations

- Does not execute own audits
- Routes to appropriate audit based on requested focus
