---
name: operar-seguridad
description: >-
  Seguridad defensiva de hosts Linux: postura, forense ligero de registros, CVEs, hardening
  sysctl/SSH, AppArmor/SELinux, auditd y fail2ban. Usar cuando el operador pida auditoría
  de seguridad del sistema, hardening del host o revisión de logs de auth. No usar para
  vulnerabilidades de código de aplicación (→ verificar-owasp) ni limpieza de disco (→
  operar-mantenimiento).
license: MIT
metadata:
  author: Soluciones-Alexendros
  version: "2.2.0"
  dominio: operar
  tipo: atomic
  idioma: es
---

# Linux Seguridad — Seguridad defensiva de hosts Linux

## Propósito

Evaluar y mejorar la postura defensiva del host sin alarmismo ni escrituras no aprobadas: forense ligero, CVEs, hardening escalonado, escaneos con validación cruzada y ciclo AppArmor.

## Cuándo usar

Auditoría de seguridad, forense de logs, escaneos malware/rootkit, CVEs, hardening CIS o ciclo de vida de perfiles AppArmor.

## Alcance

La parte defensiva es de esta skill; la de higiene es de `operar-mantenimiento`. Read-only por defecto. Evidencia antes que intuición. Validar un hallazgo por segunda vía antes de remediar. Escala R0–R3 de `operar-mantenimiento`. Identidad constitucional si el operador la pide: `disenar-constitucion`.

## Procedimiento

| Modo       | Qué hace                                      | Permisos     |
| ---------- | --------------------------------------------- | ------------ |
| `postura`  | Inventario de defensas                        | R0           |
| `logs`     | Forense ligero                                | R0           |
| `scan`     | Escaneos con validación cruzada               | R0/R1        |
| `vulns`    | CVEs y parches pendientes                     | R0           |
| `harden`   | Plan CIS; ejecución con aprobación            | R0 plan / R2 |
| `apparmor` | genprof → complain → soak → logprof → enforce | R0 diag / R2 |

1. Fingerprint: `./scripts/postura_seguridad.sh`.
2. Modo pedido. Leer la referencia del modo antes de actuar (`apparmor-playbook.md` antes de tocar un perfil).
3. Informe: Security Posture Score 0–100 (MAC 30%, detección 25%, superficie 25%, parches 20%) y hallazgos P0–P4 con evidencia.

Ningún modo escribe sin petición explícita. `harden` y AppArmor enforce muestran el plan exacto antes.

## Formato de salida

Posture Score, cronología (modo logs), hallazgos validados vs descartados (modo scan), plan P1–P4 con rollback (modo harden).

## Herramientas

| Script                  | Propósito                            | Modo     |
| ----------------------- | ------------------------------------ | -------- |
| `postura_seguridad.sh`  | Fingerprint read-only (`--json`)     | postura  |
| `scan_orchestrator.py`  | ClamAV/rkhunter/AIDE/debsums/Lynis   | scan     |
| `vulns_check.py`        | apt + snap/flatpak                   | vulns    |
| `harden_plan.py`        | Plan P1–P4 + diff + rollback         | harden   |
| `apparmor_lifecycle.py` | Ciclo AppArmor (dry-run por defecto) | apparmor |
| `forense_collector.py`  | Cronología JSON                      | logs     |

## Casos límite

Forense ligero: no sustituye respuesta a incidentes. Sin red no consulta CVE en vivo. Perfiles AppArmor de navegadores/Electron exigen soak de días.

## Referencias

- `references/postura-defensiva.md`, `references/forense-logs.md`, `references/escaneos.md`
- `references/apparmor-playbook.md`, `references/hardening-baseline.md`, `references/linux-security-source.md`
- Higiene → `operar-mantenimiento`. Código de aplicación → `verificar-owasp`.
