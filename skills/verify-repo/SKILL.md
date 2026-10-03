---
name: verify-repo
description: >-
  Integral repository audit and canonical plan start: syncs the clone, status/roadmap/failures
  board, contrasts with repo-standard (P0/P1/P2, CI quality→test→smoke, Renovate) and corrects
  thereafter. Use when the operator requests to scan, health check, repo starting, plan start or
  plan mode. Not for release close or publication (→ operate-release).
license: MIT
metadata:
  author: "Soluciones-Alexendros (adapted)"
  version: "2.3.0"
  domain: verify
  type: atomic
  language: en
---
# Verify Repo

## Overview

Integral repository audit and canonical plan start (repo starting): syncs the clone,
status/roadmap/failures board, contrasts with repo-standard (P0/P1/P2, CI quality→test→smoke,
Renovate) and corrects thereafter. Use when the operator requests to scan, health check, repo starting,
plan start or plan mode. Not for release close or publication (→ operate-release).

## When to Use

- When asked to scan or audit a repository
- For repository health check
- For plan start (repo starting)
- For plan mode

## Not for:

- Release close (→ operate-release)
- Version publication

## Procedure

1. Sync clone with remote
2. Verify status board and roadmap
3. Contrast with repo-standard
   - P0/P1/P2 prioritization
   - CI quality → test → smoke
   - Automatic Renovate
4. Apply necessary corrections
5. Evolution plan identified
