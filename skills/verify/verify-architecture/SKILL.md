---
name: verify-architecture
description: >
  Code architecture verification and analysis. Use when analyzing code structure,
  dependencies, architectural drift, or refactoring opportunities. Use when the
  operator requests architectural analysis, dependency mapping, or code health assessment.
license: MIT
metadata:
  author: "Soluciones-Alexendros (adapted)"
  version: "1.0.0"
  domain: verify
  type: atomic
  language: en
---

# Verify Architecture

## Overview

Code architecture verification and analysis. Use when analyzing code structure,
dependencies, architectural drift, or refactoring opportunities. Use when the
operator requests architectural analysis, dependency mapping, or code health assessment.

## When to Use

- When analyzing code structure
- For dependency mapping
- For architectural drift analysis
- When code health assessment is requested

## Not for

- Security code review (use verify-owasp)
- Minor implementation changes (use verify-dependencias)

## Architectural Analysis

| Aspect       | Tool                    | Objective                    |
| ------------ | ----------------------- | ---------------------------- |
| Dependencies | madge, dependency-crawl | Map module relationships     |
| Structure    | eslint, stylelint       | Check code style conventions |
| Metrics      | source-metrics, madric  | Quantitative analysis        |
| Drift        | custom scripts          | Detect unintended changes    |
