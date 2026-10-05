---
name: operate-monitoring
description:
  "System and application monitoring orchestration. Use when setting up monitoring, alerting, and observability for infrastructure and applications. Use when the operator requests monitoring configuration, alert setup, or observability tooling. Not for debugging incidents (→ operate-security) nor system cleanup (→ operate-maintenance).

  "
license: MIT
metadata:
  author: Soluciones-Alexendros (adapted)
  version: 3.0.0
  domain: operate
  type: atomic
  language: en
  keywords: operate-monitoring
compatibility: opencode, codex, cursor, copilot
allowed-tools: Read, Grep, Glob, Bash, Write
---

# Operate Monitoring

## Overview

System and application monitoring orchestration. Use when setting up monitoring,
alerting, and observability for infrastructure and applications. Use when the
operator requests monitoring configuration, alert setup, or observability tooling.

## When to Use

- When infrastructure monitoring is configured
- For alert setup and notifications
- For observability tool configuration
- When system health visibility is requested

## Not for

- Debugging ongoing incidents (use operate-security)
- System cleanup (use operate-maintenance)

## Monitoring Tools

| Category | Tools                   |
| -------- | ----------------------- |
| Metrics  | Prometheus, Grafana     |
| Tracing  | OpenTelemetry, Jaeger   |
| Logs     | ELK Stack, Loki         |
| Alerting | Alertmanager, PagerDuty |
