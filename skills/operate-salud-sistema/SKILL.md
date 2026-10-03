---
name: operate-salud-sistema
description: >-
  Diagnosis and audit of Linux system health: health-check, quick/complete audit, system
  fingerprint, health scoring (0-100), P0-P4 findings, temporal diff. Use when the operator
  requests health-check, configuration/performance/hygiene audit, CIS/Lynis compliance or
  server onboarding. Not for execution cleanup (→ operate-mantenimiento) nor hardening/forensics
  (→ operate-seguridad).
license: MIT
metadata:
  author: "Soluciones-Alexendros (adapted)"
  version: "2.0.0"
  domain: operate
  type: atomic
  language: en
---
# Operate System Health

## Overview

Diagnosis and audit of Linux system health: health-check, quick/complete audit, system
fingerprint, health scoring (0-100), P0-P4 findings, temporal diff. Use when the operator
requests health-check, configuration/performance/hygiene audit, CIS/Lynis compliance or
server onboarding. Not for execution cleanup (→ operate-mantenimiento) nor hardening/forensics
(→ operate-seguridad).

## When to Use

- System health-check
- Configuration/performance/hygiene audit
- CIS/Lynis compliance
- Server onboarding

## Not for:

- Execution cleanup (→ operate-mantenimiento)
- Hardening/forensics (→ operate-seguridad)

## Health Scoring

| Score | Classification |
|-------|---------------|
| 90-100 | Excellent |
| 70-89 | Good |
| 50-69 | Fair |
| 0-49 | Critical |
