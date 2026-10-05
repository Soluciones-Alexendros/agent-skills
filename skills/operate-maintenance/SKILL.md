---
name: operate-maintenance
description: "Systematic Linux system maintenance by IA agent: hygiene, updates, ordering, optimization and suggestions. Graduated modes (quick/complete audit, routine, optimization, cleanup) with read-only execution by default, deterministic command validation by risk level, reversible snapshots and system health KPIs. Defensive security (hardening, records/forensics, vulns, scans, AppArmor) NOT this skill: handled by sister operate-security skill. Use when asked: auditing a Linux system, routine review, cleaning packages/caches/logs, orphan pacman/AUR, boot or resource optimization, OS health-check, or periodic maintenance of Arch/EndeavourOS/ CachyOS/Debian/RHEL. Includes guided interaction to select objective, mode and depth according to context. Not for defensive security hardening or forensics (→ operate-security)."
license: MIT
metadata:
  author: Soluciones-Alexendros (adapted)
  version: 3.0.0
  domain: operate
  type: atomic
  language: en
  keywords: operate-maintenance
compatibility: opencode, codex, cursor, copilot
allowed-tools: Read, Grep, Glob, Bash, Write
---

# Operate Maintenance

## Overview

Systematic Linux system maintenance by an IA agent: hygiene, updates, ordering, optimization and
suggestions. Graduated modes (quick/complete audit, routine, optimization, cleanup) with
read-only execution by default, deterministic command validation by risk level, reversible
snapshots and system health KPIs. Defensive security (hardening, records/forensics, vulnerabilities,
scans, AppArmor) is NOT this skill: handled by sister ALIGNUX.security skill. Use when asked:
auditing a Linux system, routine review, cleaning packages/caches/logs, orphan pacman/AUR,
boot or resource optimization, OS health-check, or periodic maintenance of Arch/EndeavourOS/
CachyOS/Debian/RHEL. Includes guided interaction to select objective, mode and depth according
to context.

## When to Use

- When asked to audit a Linux system
- For routine review
- For cleaning packages/caches/logs
- For pacman/AUR orphans
- For boot or resource optimization
- For OS health-check
- Periodic maintenance of Arch/EndeavourOS/CachyOS/Debian/RHEL

## Not for:

- Health-check (→ operate-health)
- Hardening/forensics (→ operate-security)

## Graduated Modes

| Mode           | Description                            |
| -------------- | -------------------------------------- |
| Quick audit    | Quick system health check              |
| Complete audit | Full health check with all checks      |
| Routine        | Scheduled routine maintenance          |
| Optimization   | Resource and boot optimization         |
| Cleanup        | Clean caches, logs and orphan packages |

## Tools

- `scripts/check_deps.py` — dependency check.
- `scripts/snapshot_state.py` — reversible state snapshot.
- `scripts/risk_gate.py` — deterministic risk validation.
- `scripts/clean_routine.py` — cleanup routine.
- `scripts/report_render.py` — report rendering.
- `scripts/session_logger.py` — session logging.
- `scripts/common.py` — shared helpers.
