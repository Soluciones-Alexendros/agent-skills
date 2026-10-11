---
name: project-architecture
description:
  "Code architecture verification and analysis. Use when analyzing code structure, dependencies, architectural drift, or refactoring opportunities. Use when the operator requests architectural analysis, dependency mapping, or code health assessment. Not for security code review (→ web-owasp) nor minor implementation changes (→ project-libraries).

  "
license: MIT
metadata:
  author: Soluciones-Alexendros (adapted)
  version: 4.0.0
  domain: project
  type: atomic
  language: en
  keywords: project-architecture
compatibility: opencode, codex, cursor, copilot
allowed-tools: Read, Grep, Glob, Bash, Write
---

# Project Architecture

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

- Security code review (use web-owasp)
- Minor implementation changes (use project-libraries)

## Architectural Analysis

| Aspect       | Tool                    | Objective                    |
| ------------ | ----------------------- | ---------------------------- |
| Dependencies | madge, dependency-crawl | Map module relationships     |
| Structure    | eslint, stylelint       | Check code style conventions |
| Metrics      | source-metrics, madric  | Quantitative analysis        |
| Drift        | custom scripts          | Detect unintended changes    |
