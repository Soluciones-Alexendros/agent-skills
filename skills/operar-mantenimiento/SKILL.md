---
name: operar-mantenimiento
description: >-
  Mantenimiento de sistemas Linux: higiene, actualizaciones, limpieza de
  cachés/logs/paquetes huérfanos, optimización de arranque, plan de acción P1–P4,
  ejecución de limpieza aprobada (snapshot + risk_gate). Incluye cribado de basura
  en disco. Usar cuando el operador pida mantenimiento del SO, limpieza de espacio,
  rutina Arch/Debian/RHEL, optimización o cribar el filesystem. No usar para
  health-check (→ operar-salud-sistema) ni hardening/forense (→ operar-seguridad).
license: MIT
metadata:
  author: Soluciones-Alexendros
  version: "2.2.0"
  dominio: operar
  tipo: atomic
  idioma: es
---

# Linux Mantenimiento — Ejecución de mantenimiento y optimización

## Propósito

Mantener el sistema sano y actualizado con riesgo controlado: higiene de paquetes/cachés/logs, actualizaciones, optimización de arranque, plan P1–P4 y limpieza reversible aprobada. Requiere auditoría previa de `operar-salud-sistema`.

## Cuándo usar

Mantenimiento rutinario, plan de optimización P1–P4, limpieza aprobada o clasificación de un comando con `risk_gate`.

## Alcance

| Esta skill                         | `operar-seguridad`               | `operar-salud-sistema`                     |
| ---------------------------------- | -------------------------------- | ------------------------------------------ |
| Actualizaciones, cachés, huérfanos | Firewall, AppArmor, auditd, AIDE | Diagnóstico audit-quick/full               |
| Optimización arranque, plan P1–P4  | Forense de logs, CVEs            | Health score, solo lectura R0              |
| Limpieza de logs, snapshots        | Hardening CIS, SSH, sysctl       | Genera la auditoría que esta skill consume |

Read-only por defecto. Escritura reversible con snapshot. Deny-list estructural → `risk_gate.py` → confirmación humana. Nunca ejecutar escritura sin modo `clean` o `routine` y plan en dry-run aprobado.

## Procedimiento

| Modo       | Descripción                              | Permisos               |
| ---------- | ---------------------------------------- | ---------------------- |
| `routine`  | Actualizaciones, cachés, logs, huérfanos | R0 + R1 con snapshot   |
| `optimize` | Plan P1–P4, sin ejecución                | R0                     |
| `clean`    | Acciones correctivas aprobadas           | R1 + R2 con aprobación |

1. Prerrequisito: auditoría de `operar-salud-sistema`.
2. `./scripts/clean_routine.py --dry-run --audit <audit-file>` o `./scripts/report_render.py --mode optimize`.
3. Si el operador aprueba: snapshot y `--execute`.
4. Registro append-only en `session-<timestamp>.log`.

Niveles R0 (lectura) / R1 (reversible, snapshot) / R2 (aprobación + snapshot) / R3 (bloqueo, sin bypass: `rm -rf /`, `mkfs`, `dd of=/dev/...`, `curl | sh`). Rutas protegidas: `/boot`, `/etc/fstab`, `/etc/passwd`, `/etc/shadow`, `/etc/sudoers`, `/etc/ssh/sshd_config`, `/usr`, `/lib/modules`. Detalle: `references/safety-policy.md`. Flujo conversacional: `references/guided-interaction.md`. Cribado de disco: `references/cribado-source.md`; nunca `rm` sin confirmación.

El agente se adapta al perfil (`system-profile.yaml`): distro, entorno prod/dev, ventana corta, ausencia de snapshot tool. No asume un host concreto.

## Herramientas

| Script              | Propósito                | Modo           |
| ------------------- | ------------------------ | -------------- |
| `risk_gate.py`      | Validador pre-ejecución  | clean, routine |
| `snapshot_state.py` | Captura, list y rollback | routine, clean |
| `clean_routine.py`  | Limpieza aprobada        | routine, clean |
| `report_render.py`  | Informe MD/HTML P1–P4    | optimize       |
| `session_logger.py` | Log forense              | todos          |
| `check_deps.py`     | Pre-flight               | todos          |

Python nativo, sin `jq`. `python3` ≥ 3.10, `timeout`, `systemctl`, `ss`. Opcionales: lynis, smartmontools, fwupd, paccache, deborphan, needrestart.

## Casos límite

Sin `smartmontools` no hay health de disco. Modo `clean`/`routine` con R1+ sin `risk_gate.py` degrada a solo-informe. Cron desatendido solo para R0.

## Referencias

- `references/safety-policy.md`, `references/pitfalls.md`, `references/audit-checklist.md`
- `references/arch-maintenance.md`, `references/debian-rhel-adapters.md`
- `references/metrics-scoring.md`, `references/guided-interaction.md`, `references/cribado-source.md`
- Auditoría previa → `operar-salud-sistema`. Hardening → `operar-seguridad`.
- Perfil de un equipo concreto (fuera de esta skill): `../../docs/archives/perfil-equipo-local.md`.
