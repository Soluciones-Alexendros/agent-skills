---
name: operate-health
description: "Diagnosis and audit of Linux system health: health-check, quick/complete audit, system fingerprint, health scoring (0-100), P0-P4 findings, temporal diff. Use when the operator requests health-check, configuration/performance/hygiene audit, CIS/Lynis compliance or server onboarding. Not for execution cleanup (→ operate-maintenance) nor hardening/forensics (→ operate-security)."
license: MIT
metadata:
  author: Soluciones-Alexendros (adapted)
  version: 3.0.0
  domain: operate
  type: atomic
  language: en
  keywords: operate-health
compatibility: opencode, codex, cursor, copilot
allowed-tools: Read, Grep, Glob, Bash, Write
---

# Operate System Health

## Overview

Diagnosis and audit of Linux system health: health-check, quick/complete audit, system
fingerprint, health scoring (0-100), P0-P4 findings, temporal diff. Use when the operator
requests health-check, configuration/performance/hygiene audit, CIS/Lynis compliance or
server onboarding. Not for execution cleanup (→ operate-maintenance) nor hardening/forensics
(→ operate-security).

## When to Use

- System health-check
- Configuration/performance/hygiene audit
- CIS/Lynis compliance
- Server onboarding

## Not for:

- Execution cleanup (→ operate-maintenance)
- Hardening/forensics (→ operate-security)

## Health Scoring

| Score  | Classification |
| ------ | -------------- |
| 90-100 | Excellent      |
| 70-89  | Good           |
| 50-69  | Fair           |
| 0-49   | Critical       |

## Tools

- `scripts/probe_system.py` — system probing.
- `scripts/audit_quick.py` — quick audit.
- `scripts/audit_full.py` — complete audit.
- `scripts/check_deps.py` — dependency check.
- `scripts/report_render.py` — report rendering.
- `scripts/session_logger.py` — session logging.
- `scripts/common.py` — shared helpers.
