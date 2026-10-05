---
name: operate-security
description: "Defensive Linux host security: posture, light forensic record management, CVEs, sysctl/SSH hardening, AppArmor/SELinux, auditd and fail2ban. Use when the operator requests system security audit, host hardening or auth log review. Not for application code vulnerabilities (→ verify-owasp) nor disk cleanup (→ operate-maintenance)."
license: MIT
metadata:
  author: Soluciones-Alexendros (adapted)
  version: 3.0.0
  domain: operate
  type: atomic
  language: en
  keywords: operate-security
compatibility: opencode, codex, cursor, copilot
allowed-tools: Read, Grep, Glob, Bash, Write
---

# Operate Security

## Overview

Defensive Linux host security: posture, light forensic record management, CVEs, sysctl/SSH
hardening, AppArmor/SELinux, auditd and fail2ban. Use when the operator requests system
security audit, host hardening or auth log review. Not for application code vulnerabilities
(→ verify-owasp) nor disk cleanup (→ operate-maintenance).

## When to Use

- System security audit
- Host hardening
- Auth log review

## Not for:

- Application code vulnerabilities (→ verify-owasp)
- Disk cleanup (→ operate-maintenance)

## Components

| Component        | Description                 |
| ---------------- | --------------------------- |
| Posture          | Security posture assessment |
| CVEs             | Vulnerability tracking      |
| sysctl           | System parameter hardening  |
| SSH              | SSH server hardening        |
| AppArmor/SELinux | Mandatory access control    |
| auditd           | Audit daemon configuration  |
| fail2ban         | Brute force protection      |

## Tools

- `scripts/postura_seguridad.sh` — defensive posture snapshot.
- `scripts/forense_collector.py` — log forensics collection.
- `scripts/vulns_check.py` — vulnerability check.
- `scripts/harden_plan.py` — hardening plan.
- `scripts/scan_orchestrator.py` — malware/rootkit scan orchestration.
- `scripts/apparmor_lifecycle.py` — AppArmor profile lifecycle.
