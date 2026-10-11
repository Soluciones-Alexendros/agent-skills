---
name: plan-continue
description: "Continue work according to the existing roadmap; when none exists, audit repository state against repo-standard and reason the next logical steps. Cite official documentation when framework-specific decisions matter. Use when asking where to start, plan mode, repo starting, or bringing a project up to date. Not for release close or version publication (→ project-publish)."
license: MIT
metadata:
  author: Soluciones-Alexendros (adapted)
  version: 4.0.0
  domain: plan
  type: orchestrator
  language: en
  keywords: plan-continue
compatibility: opencode, codex, cursor, copilot
allowed-tools: Read, Grep, Glob, Bash, Write
---

# Plan Continue

## Overview

Continue according to the planned roadmap. When there is no roadmap, analyze
repository state (sync, status board, failures, contrast with repo-standard)
and reason the next logical steps. Framework-specific decisions cite official
documentation — training data goes stale.

## When to Use

- Operator asks where to start or opens plan mode
- Repo starting / bring a project up to date
- An existing `tasks/`, roadmap or status board should drive the next work
- Mix of audit then continue implementation

**When NOT to use:** Release close or version publication (→ project-publish);
writing a fresh multi-module spec from scratch (→ plan-specification).

## Process

### 1. Detect existing plan

Look for `tasks/plan.md`, `tasks/todo.md`, `ESTADO.md`, roadmap docs, open
milestones or an active branch with a clear work package.

- **Roadmap present** → pick the next unfinished task with unmet dependencies;
  verify acceptance criteria still match the codebase; proceed.
- **No roadmap** → run the repository analysis below, then propose the next
  steps (and optionally hand off to → plan-specification).

### 2. Repository analysis (when no roadmap)

1. Sync clone with remote
2. Verify status board and roadmap / failures
3. Contrast with repo-standard: P0/P1/P2, CI quality → test → smoke, Renovate
4. Apply necessary corrections that unblock progress
5. Identify the evolution plan and write it down

Detail for plan start: [inicio-plan.md](references/inicio-plan.md).
Canon contrast: [canon.md](references/canon.md), [convenciones-y-canon.md](references/convenciones-y-canon.md).

### 3. Source-backed decisions

When the next step depends on a framework or library version:

1. Detect stack and versions from dependency files
2. Fetch the specific official docs page (not the homepage)
3. Implement following documented patterns; surface conflicts with existing code
4. Cite sources (formats in [citation-guide.md](references/citation-guide.md))

Authority hierarchy and safety: [source-guide.md](references/source-guide.md).
Verification checklist: [verification-guide.md](references/verification-guide.md).

### 4. Handoff

- Implementation work → → role-front / → role-back / → role-design plus
  → plan-validation
- Publish or close work → → project-publish
- Mixed «audítalo y publícalo» → finish analysis here, then hand off to
  → project-publish

## Tools

- `scripts/scan_repo.py` — repository scan
- `scripts/audit-repo.sh` — repo audit
- `scripts/check-product-structure.sh` — product structure check
- `scripts/inicio_plan.py` — plan initialization / status board

## References

- [inicio-plan.md](references/inicio-plan.md) — plan start / repo starting mode
- [plantilla-informe.md](references/plantilla-informe.md) — report template
- [source-guide.md](references/source-guide.md) — authority hierarchy, fetch safety
- [citation-guide.md](references/citation-guide.md) — citation formats
- [verification-guide.md](references/verification-guide.md) — checklist
