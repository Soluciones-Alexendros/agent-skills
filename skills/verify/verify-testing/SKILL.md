---
name: verify-testing
description: >
  Testing verification and quality assurance. Use when planning, implementing, or verifying
  test strategies, test quality metrics, and test coverage goals. Use when the operator
  requests test planning, test quality review, or test coverage analysis.
license: MIT
metadata:
  author: "Soluciones-Alexendros (adapted)"
  version: "1.0.0"
  domain: verify
  type: atomic
  language: en
---

# Verify Testing

## Overview

Testing verification and quality assurance. Use when planning, implementing, or verifying
test strategies, test quality metrics, and test coverage goals. Use when the operator
requests test planning, test quality review, or test coverage analysis.

## When to Use

- When test strategy is planned
- For test quality review
- For test coverage analysis
- When testing quality metrics are defined

## Not for

- Specific test case writing (use planning-test-driven-development)
- Debug errors in production (use operate-salud-sistema)

## Testing Strategies

| Strategy            | Description                          |
| ------------------- | ------------------------------------ |
| Test pyramid        | Distribution: unit, integration, e2E |
| Testing shift-left  | Tests early in the cycle             |
| Testing shift-right | Tests in production                  |
| Test maintenance    | Test suite maintenance               |
