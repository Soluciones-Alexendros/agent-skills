# metrics-scoring.md

Definición de KPIs, fórmula de Health Score, y métricas de evaluación para la skill mantenimiento-linux.

---

## Health Score (0–100)

Puntuación compuesta ponderada que resume el estado de salud del sistema. Se calcula en cada auditoría y se compara con ejecuciones anteriores (tendencia).

### Fórmula

```
Health Score = (Security × 0.40) + (Updates × 0.25) + (Hygiene × 0.20) + (Resources × 0.15)
```

Cada componente se normaliza a 0–100.

---

## 1. Security (40%)

Evaluación de postura de seguridad según hardening-baseline.md y audit-checklist.md.

### Sub-componentes (peso interno)

| Sub-componente | Peso | Controles clave | Puntuación |
|----------------|------|-----------------|------------|
| **SSH Hardening** | 25% | SSH-01 a SSH-20 | 100 si todos P0/P1 PASS, -10 por cada FAIL P0, -5 por FAIL P1 |
| **Firewall** | 20% | FW-01 a FW-07 | 100 si FW-01/FW-02/FW-03 PASS, -20 si FW-01 FAIL, -10 si FW-02/03 FAIL |
| **Kernel Hardening** | 15% | KR-01 a KR-30 | % de controles PASS (P0/P1 peso 2x, P2 peso 1x, P3 peso 0.5x) |
| **Audit/Logging** | 15% | AU-01 a AU-15 | 100 si auditd activo + reglas críticas, -15 por cada regla crítica faltante |
| **Filesystem Permissions** | 10% | FS-01 a FS-13 | 100 si sin world-writable, SUID/SGID baseline, -5 por hallazgo P1, -2 por P2 |
| **User/Auth** | 10% | UA-01 a UA-15 | 100 si UID 0 solo root, sin passwd vacías, pam_pwquality/faillock, -10 por P0, -5 por P1 |
| **Crypto** | 5% | CR-01 a CR-05 | 100 si claves SSH modernas, TLS 1.2+, LUKS Argon2, -10 por cada FAIL |

### Cálculo Security Score
```
Security = Σ (sub_score_i × weight_i)  →  redondeado a entero 0–100
```

### Penalizaciones automáticas (aplicadas tras cálculo)
- **P0 hallazgos abiertos**: -20 por cada uno (mínimo 0)
- **P1 hallazgos abiertos > 5**: -10
- **Firewall inactivo**: Security = 0 (override)
- **SSH root login + password auth**: Security = 0 (override)
- **SELinux/AppArmor deshabilitado en distro que lo usa por defecto**: -15

---

## 2. Updates (25%)

Estado de actualizaciones del sistema, firmware, y noticias leídas.

### Sub-componentes

| Sub-componente | Peso | Verificación | Puntuación |
|----------------|------|--------------|------------|
| **Paquetes al día** | 50% | `checkupdates` / `apt list --upgradable` / `dnf check-update` | 100 si 0 pendientes, -2 por cada actualización normal, -10 por cada seguridad |
| **Kernel running = installed** | 20% | `uname -r` vs paquete kernel instalado | 100 si coincide, 0 si reboot pendiente |
| **Firmware actualizado** | 15% | `fwupdmgr get-updates` | 100 si 0 pendientes, -5 por cada actualización |
| **Noticias leídas (Arch)** | 10% | Verificar marca de noticias leídas | 100 si leídas, 0 si no (solo Arch) |
| **Rebuild-detector limpio** | 5% | `rebuild-detector` (Arch) | 100 si 0 paquetes rotos, -10 por cada uno |

### Cálculo Updates Score
```
Updates = Σ (sub_score_i × weight_i)  →  redondeado a entero 0–100
```

### Notas
- En rolling release (Arch), "paquetes al día" es crítico: más de 50 actualizaciones pendientes = score bajo
- En point release (Debian/RHEL), solo actualizaciones de seguridad cuentan para penalización fuerte
- Kernel reboot pendiente no es "roto", pero indica mantenimiento diferido

---

## 3. Hygiene (20%)

Higiene de paquetes, cachés, configs, y limpieza general.

### Sub-componentes

| Sub-componente | Peso | Verificación | Puntuación |
|----------------|------|--------------|------------|
| **Huérfanos** | 25% | `pacman -Qtdq` / `apt autoremove --dry-run` / `dnf repoquery --unneeded` | 100 si 0, -2 por cada huérfano (máx -50) |
| **Paquetes foráneos (AUR/third-party)** | 20% | `pacman -Qmq` / `apt list --manual-installed` / `dnf list extras` | 100 si ≤ 10, -1 por cada extra (máx -50) |
| **Archivos .pacnew/.pacsave/.rpmnew/.dpkg-new** | 20% | `find /etc -name "*.pacnew" ...` | 100 si 0, -5 por cada pendiente (máx -50) |
| **Tamaño caché paquetes** | 15% | `du -sh /var/cache/pacman/pkg` / `/var/cache/apt` / `/var/cache/dnf` | 100 si < 1GB, -5 por cada GB extra (máx -50) |
| **Journal size** | 10% | `journalctl --disk-usage` | 100 si < 500MB, -5 por cada 100MB extra (máx -50) |
| **Symlinks rotos en /etc, /usr, /boot** | 10% | `find /etc /usr /boot -xtype l` | 100 si 0, -2 por cada uno (máx -30) |

### Cálculo Hygiene Score
```
Hygiene = Σ (sub_score_i × weight_i)  →  redondeado a entero 0–100
```

---

## 4. Resources (15%)

Uso de recursos: disco, memoria, arranque, servicios.

### Sub-componentes

| Sub-componente | Peso | Verificación | Puntuación |
|----------------|------|--------------|------------|
| **Disco raíz (/)** | 30% | `df -h /` | 100 si < 70%, 80 si 70-80%, 50 si 80-90%, 0 si > 90% |
| **Disco /boot** | 15% | `df -h /boot` | 100 si < 50%, 50 si 50-80%, 0 si > 80% |
| **Disco /var** | 10% | `df -h /var` | 100 si < 70%, 70 si 70-85%, 30 si 85-95%, 0 si > 95% |
| **Inodos** | 10% | `df -i / /boot /var /home` | 100 si < 70%, degradación similar a disco |
| **RAM/Swap pressure** | 15% | `free -h`, `swapon -s` | 100 si swap used < 10%, 70 si 10-50%, 30 si 50-90%, 0 si > 90% |
| **Boot time** | 10% | `systemd-analyze` | 100 si < 15s, 80 si 15-30s, 50 si 30-60s, 30 si > 60s |
| **Servicios fallidos** | 10% | `systemctl --failed` | 100 si 0, -20 por cada servicio fallido |

### Cálculo Resources Score
```
Resources = Σ (sub_score_i × weight_i)  →  redondeado a entero 0–100
```

---

## Hallazgos: Clasificación P0–P4

Cada hallazgo de auditoría se clasifica:

| Nivel | Definición | Ejemplos | Impacto en Health Score |
|-------|------------|----------|------------------------|
| **P0** | Crítico: compromiso activo/inminente, superficie crítica expuesta | SSH root+password, firewall off, UID 0 extra, passwd vacía, kernel exploit conocido sin parche | -20 c/u en Security (override) |
| **P1** | Alto: vulnerabilidad conocida, config insegura, parche crítico faltante | SSH config débil, puerto expuesto innecesario, actualización seguridad pendiente, auditd inactivo | -10 c/u en Security, -10 en Updates si parche seguridad |
| **P2** | Medio: desviación baseline, deuda técnica, hardening incompleto | Sysctl no óptimo, world-writable files, .pacnew pendientes, huérfanos | -5 c/u en componente relevante |
| **P3** | Bajo: optimización, limpieza, mejoras higiene | Caché grande, journal grande, symlinks rotos, boot lento | -2 c/u en componente relevante |
| **P4** | Informativo: observación, tendencia, sin acción inmediata | Paquete AUR viejo, firmware opcional, timer no crítico | 0 (solo reporte) |

---

## Tendencia y Diff Temporal

La skill mantiene historial en `~/.local/share/mantenimiento-linux/history/` (o `$XDG_DATA_HOME`).

### Estructura de historial
```
history/
├── 2026-08-01_10-00-00_audit-quick.json
├── 2026-08-01_10-00-00_audit-quick.md
├── 2026-08-03_10-00-00_audit-full.json
├── 2026-08-03_10-00-00_audit-full.md
├── 2026-08-05_10-00-00_routine.json
├── 2026-08-05_10-00-00_routine.md
└── index.json  # índice con timestamps, modos, health scores
```

### index.json
```json
{
  "runs": [
    {
      "timestamp": "2026-08-01T10:00:00Z",
      "mode": "audit-quick",
      "health_score": 78,
      "security": 72,
      "updates": 85,
      "hygiene": 80,
      "resources": 75,
      "findings": {"P0": 0, "P1": 2, "P2": 5, "P3": 8, "P4": 12},
      "report": "2026-08-01_10-00-00_audit-quick.md"
    },
    {
      "timestamp": "2026-08-05T10:00:00Z",
      "mode": "routine",
      "health_score": 88,
      "security": 85,
      "updates": 95,
      "hygiene": 90,
      "resources": 80,
      "findings": {"P0": 0, "P1": 0, "P2": 2, "P3": 3, "P4": 5},
      "report": "2026-08-05_10-00-00_routine.md"
    }
  ]
}
```

### Cálculo de tendencia
```python
# En report_render.py
def calculate_trend(current, previous):
    if not previous:
        return "first_run"
    delta = current - previous
    if delta > 5:
        return "improving"
    elif delta < -5:
        return "degrading"
    else:
        return "stable"
```

### Diff de hallazgos
- **Nuevos**: hallazgos en actual que no estaban en anterior
- **Resueltos**: hallazgos en anterior que no están en actual
- **Persistentes**: hallazgos en ambos (indica deuda no atendida)
- **Regresados**: hallazgos resueltos que reaparecen

---

## KPIs Operativos (para dashboards/alertas)

| KPI | Definición | Meta | Alerta si |
|-----|------------|------|-----------|
| **Health Score** | Puntuación global 0–100 | ≥ 85 | < 70 |
| **P0 abiertos** | Conteo hallazgos P0 | 0 | > 0 |
| **P1 abiertos** | Conteo hallazgos P1 | ≤ 2 | > 5 |
| **Tiempo audit-quick** | Duración en segundos | < 300s | > 600s |
| **Cobertura quick** | % controles P0+P1 ejecutados | ≥ 90% | < 80% |
| **Cobertura full** | % todos controles ejecutados | ≥ 95% | < 90% |
| **Espacio recuperado** | MB liberados en rutina | Reportado | N/A |
| **Reversibilidad** | % acciones R1+ con snapshot verificado | 100% | < 100% |
| **Falsos positivos risk_gate** | Comandos R0/R1 bloqueados indebidamente | < 2% | > 5% |
| **Incidentes** | Acciones fuera de perímetro o roturas | 0 | > 0 |

---

## Salida JSON estandarizada (para scripts/integración)

### audit_quick.py / audit_full.py output
```json
{
  "metadata": {
    "timestamp": "2026-08-05T10:00:00Z",
    "mode": "audit-full",
    "hostname": "server01",
    "distro": "endeavouros",
    "family": "arch",
    "kernel": "6.9.5-arch1-1",
    "duration_seconds": 142,
    "skill_version": "1.0.0"
  },
  "system_profile": {
    "package_manager": "pacman",
    "aur_helper": "yay",
    "critical_services": ["NetworkManager", "sshd", "systemd-resolved"],
    "snapshot_tool": "timeshift"
  },
  "health_score": {
    "overall": 82,
    "security": 78,
    "updates": 90,
    "hygiene": 85,
    "resources": 75
  },
  "findings": [
    {
      "id": "SSH-02",
      "category": "security",
      "severity": "P0",
      "title": "SSH PasswordAuthentication enabled",
      "description": "SSH allows password authentication, should be key-only",
      "control": "SSH-02",
      "status": "FAIL",
      "evidence": "sshd -T | grep passwordauthentication -> yes",
      "remediation": "Set PasswordAuthentication no in /etc/ssh/sshd_config and reload sshd",
      "risk_level": "R2"
    },
    {
      "id": "PKG-01",
      "category": "updates",
      "severity": "P1",
      "title": "12 security updates pending",
      "description": "Packages with security updates available",
      "control": "PKG-01",
      "status": "FAIL",
      "evidence": "checkupdates | grep -i security | wc -l -> 12",
      "remediation": "Run pacman -Syu after reading Arch news",
      "risk_level": "R2"
    }
  ],
  "summary": {
    "total_checks": 156,
    "passed": 138,
    "failed": 12,
    "warned": 6,
    "skipped": 0,
    "errors": 0,
    "by_severity": {"P0": 1, "P1": 3, "P2": 4, "P3": 4, "P4": 0}
  }
}
```

### clean_routine.py output (ejecución)
```json
{
  "metadata": {
    "timestamp": "2026-08-05T11:30:00Z",
    "mode": "routine",
    "hostname": "server01",
    "dry_run": false,
    "snapshot_id": "timeshift-2026-08-05_11-29-45",
    "duration_seconds": 45,
    "skill_version": "1.0.0"
  },
  "actions": [
    {
      "action": "journal_vacuum",
      "command": "journalctl --vacuum-time=7d",
      "risk_level": "R1",
      "dry_run_output": "Vacuuming... freed 234.5M",
      "execution_output": "Vacuuming... freed 234.5M",
      "verification": "journalctl --disk-usage -> 412.3M",
      "status": "SUCCESS",
      "space_freed_mb": 234
    },
    {
      "action": "paccache_clean",
      "command": "paccache -r -k 3",
      "risk_level": "R1",
      "dry_run_output": "would remove 45 packages (1.2G)",
      "execution_output": "removed 45 packages (1.2G)",
      "verification": "du -sh /var/cache/pacman/pkg -> 856M",
      "status": "SUCCESS",
      "space_freed_mb": 1200
    },
    {
      "action": "remove_orphans",
      "command": "pacman -Rns $(pacman -Qtdq)",
      "risk_level": "R1",
      "dry_run_output": "would remove: pkg1 pkg2 pkg3 (45M)",
      "execution_output": "removed: pkg1 pkg2 pkg3 (45M)",
      "verification": "pacman -Qtdq -> (empty)",
      "status": "SUCCESS",
      "space_freed_mb": 45
    }
  ],
  "summary": {
    "total_actions": 3,
    "successful": 3,
    "failed": 0,
    "skipped": 0,
    "total_space_freed_mb": 1479,
    "snapshot_verified": true
  }
}
```

---

## Umbrales de alerta (para integración con monitoring)

```yaml
# alerting-rules.yaml (ejemplo para Prometheus/Alertmanager)
groups:
  - name: linux-sys-care
    rules:
      - alert: HealthScoreCritical
        expr: linux_sys_care_health_score < 70
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "Health score below 70 on {{ $labels.hostname }}"
          
      - alert: P0FindingsOpen
        expr: linux_sys_care_findings_p0 > 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "{{ $value }} P0 findings open on {{ $labels.hostname }}"
          
      - alert: SecurityUpdatesPending
        expr: linux_sys_care_security_updates_pending > 0
        for: 1h
        labels:
          severity: warning
        annotations:
          summary: "{{ $value }} security updates pending on {{ $labels.hostname }}"
          
      - alert: DiskSpaceCritical
        expr: (linux_sys_care_disk_usage_root / linux_sys_care_disk_size_root) > 0.90
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "Root disk > 90% on {{ $labels.hostname }}"
          
      - alert: KernelRebootPending
        expr: linux_sys_care_kernel_reboot_pending == 1
        for: 24h
        labels:
          severity: warning
        annotations:
          summary: "Kernel reboot pending > 24h on {{ $labels.hostname }}"
```

---

## Métricas de calidad de la skill (meta-evaluación)

| Métrica | Definición | Meta |
|---------|------------|------|
| **Precisión risk_gate** | % comandos clasificados correctamente (R0–R3) | ≥ 98% |
| **Falsos positivos R3** | Comandos legítimos bloqueados como R3 | 0 |
| **Falsos negativos R3** | Comandos peligrosos clasificados < R3 | 0 |
| **Cobertura checklist** | % controles audit-checklist implementados | 100% |
| **Tiempo audit-quick** | P95 duración | < 5 min |
| **Tiempo audit-full** | P95 duración | < 30 min |
| **Overhead skill** | Tokens/tiempo extra vs baseline sin skill | < 20% |
| **Satisfacción usuario** | Feedback cualitativo (viewer) | ≥ 4/5 |

---

## Versionado de métricas

La fórmula de Health Score y umbrales pueden evolucionar. Versionado semántico en `metrics-scoring.md`:

```
v1.0.0 - Fórmula inicial (2026-08-05)
v1.1.0 - Ajuste pesos Security 40%→35%, Updates 25%→30% (basado en datos reales)
v1.2.0 - Nuevo sub-componente: Supply Chain (AUR/third-party verification)
```

La skill reporta `metrics_version` en cada salida JSON para trazabilidad.