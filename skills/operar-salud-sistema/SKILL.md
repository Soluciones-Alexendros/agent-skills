---
name: operar-salud-sistema
description: >-
  Diagnóstico y auditoría de salud de sistemas Linux: health-check, auditoría rápida/completa,
  fingerprint de sistema, scoring de salud (0–100), hallazgos P0–P4, diff temporal. Usar cuando
  el operador pida health-check, auditoría de configuración/rendimiento/higiene, compliance
  CIS/Lynis u onboarding de servidores. No usar para ejecución de limpieza (→
  operar-mantenimiento) ni hardening/forense (→ operar-seguridad).
license: MIT
metadata:
  author: Soluciones-Alexendros
  version: "1.1.0"
  dominio: operar
  tipo: atomic
  idioma: es
---

# Linux Salud — Diagnóstico y auditoría de sistemas Linux

## Propósito

Diagnosticar el estado de salud del sistema: fingerprint, scoring 0–100, hallazgos P0–P4 y diff temporal. Solo lectura (R0).

## Cuándo usar

Health-check, auditoría rápida (`audit-quick`), auditoría completa (`audit-full`), fingerprint o informe HTML/MD de una auditoría previa.

## Procedimiento

| Modo          | Descripción                         | Permisos |
| ------------- | ----------------------------------- | -------- |
| `audit-quick` | Health-check 5–10 min               | R0       |
| `audit-full`  | Higiene, rendimiento, configuración | R0       |

1. `./scripts/probe_system.py` → `system-profile.json`.
2. `./scripts/audit_quick.py` o `./scripts/audit_full.py`.
3. `./scripts/report_render.py --input <audit-file> --output <report.md> --history <history-dir>`.
4. Log append-only `session-<timestamp>.log`.

Health Score: Seguridad 40% (postura de `operar-seguridad` en informes combinados), Actualización 25%, Higiene 20%, Recursos 15%. Fórmula: `references/metrics-scoring.md`. P0 bloqueo / P1 <24h / P2 <7d / P3 ventana / P4 informativo.

Nunca escribe. Identidad constitucional si el operador la pide: `disenar-constitucion`. Flujo conversacional: `references/guided-interaction.md`.

## Herramientas

| Script              | Propósito                    | Modo        |
| ------------------- | ---------------------------- | ----------- |
| `probe_system.py`   | Fingerprint JSON             | todos       |
| `audit_quick.py`    | Health-check P0+P1           | audit-quick |
| `audit_full.py`     | Extiende audit-quick a P0–P4 | audit-full  |
| `report_render.py`  | Informe MD/HTML + diff       | todos       |
| `session_logger.py` | Log forense                  | todos       |
| `check_deps.py`     | Pre-flight                   | todos       |
| `common.py`         | Checks compartidos           | interno     |

Python nativo. Requiere `python3` ≥ 3.10, `timeout`, `systemctl`, `ss`. Opcionales: lynis, smartmontools, fwupd.

## Casos límite

Sin `smartmontools`/`nvme-cli` no hay health de disco. Cron desatendido solo para R0.

## Referencias

- `references/safety-policy.md`, `references/pitfalls.md`, `references/audit-checklist.md`
- `references/arch-maintenance.md`, `references/debian-rhel-adapters.md`
- `references/metrics-scoring.md`, `references/guided-interaction.md`
- Baseline de hardening activo: `../operar-seguridad/references/hardening-baseline.md`
- Ejecución → `operar-mantenimiento`. Forense → `operar-seguridad`.
