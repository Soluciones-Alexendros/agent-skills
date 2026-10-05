---
name: build-automation
description: Automation of build, test, and deployment pipelines. Use when setting up CI/CD, automating repetitive tasks, or configuring pipeline as code. Use when the operator requests pipeline creation, automation of release processes, or configuration of build workflows across multiple environments. Not for visual design (→ build-interface) nor security review (→ verify-owasp).
license: MIT
metadata:
  author: Soluciones-Alexendros (adapted)
  version: 3.0.0
  domain: build
  type: atomic
  language: en
  keywords: build-automation
compatibility: opencode, codex, cursor, copilot
allowed-tools: Read, Grep, Glob, Bash, Write
---

# Build Automation

## Overview

Automation of build, test, and deployment pipelines. Use when setting up CI/CD,
automating repetitive tasks, or configuring pipeline as code. Use when the operator
requests pipeline creation, automation of release processes, or configuration of
build workflows across multiple environments.

## When to Use

- When setting up CI/CD pipelines
- To automate repetitive tasks
- To configure pipeline as code
- For release process automation
- To configure build flows across multiple environments

## Not for

- Single manual deployment
- One-time environment configuration

## Pipeline Types

| Pipeline Type | Description                                         |
| ------------- | --------------------------------------------------- |
| CI            | Continuous integration: build, test on every commit |
| CD            | Continuous deployment: deploy to staging/production |
| Multi-stage   | Pipelines with multiple stages and environments     |
| Monorepo      | Pipelines for monorepos with affected               |

## Key Components

- Stages and jobs definition
- Multi-OS configuration matrix
- Dependencies caching
- Artifacts management
