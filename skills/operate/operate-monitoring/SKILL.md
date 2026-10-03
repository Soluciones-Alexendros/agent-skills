---
name: operate-monitoring
description: >
  System and application monitoring orchestration. Use when setting up monitoring,
  alerting, and observability for infrastructure and applications. Use when the
  operator requests monitoring configuration, alert setup, or observability tooling.
license: MIT
metadata:
  author: "Soluciones-Alexendros (adapted)"
  version: "1.0.0"
  domain: operate
  type: atomic
  language: en
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

- Debugging ongoing incidents (use operate-seguridad)
- System cleanup (use operate-mantenimiento)

## Monitoring Tools

| Category | Tools                   |
| -------- | ----------------------- |
| Metrics  | Prometheus, Grafana     |
| Tracing  | OpenTelemetry, Jaeger   |
| Logs     | ELK Stack, Loki         |
| Alerting | Alertmanager, PagerDuty |
