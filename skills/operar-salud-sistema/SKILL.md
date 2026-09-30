---
name: operar-salud-sistema
description: >
  Diagnóstico y auditoría de salud de sistemas Linux: health-check, auditoría rápida/completa,
  fingerprint de sistema, scoring de salud (0–100), hallazgos P0–P4, diff temporal. Usar ante
  health-check, auditoría de configuración/rendimiento/higiene, compliance CIS/Lynis, onboarding
  de servidores. No usar para ejecución de limpieza ni optimización (→ operar-mantenimiento)
  ni hardening/forense (→ operar-seguridad).
license: MIT
metadata:
  author: Soluciones-Alexendros
  version: "1.0.0"
  dominio: operar
  tipo: atomic
  idioma: es
---

# Linux Salud — Diagnóstico y auditoría de sistemas Linux

Skill para diagnóstico y auditoría de salud de sistemas Linux operada por un agente IA con seguridad estructural. Parte del sistema **ALIGNUX** — identidad constitucional en mayúsculas, coherencia sobre consistencia.

## Qué hace / Propósito

Diagnosticar y auditar el estado de salud del sistema: health-check continuo, auditoría de configuración/rendimiento/higiene, fingerprint de sistema, scoring de salud (0–100), hallazgos clasificados (P0–P4), y diff temporal contra ejecuciones previas. Solo lectura (R0) por defecto.

## Cuándo usarme / Triggering

- **Health-check / Monitoring**: "Haz un health-check de mi servidor", "¿Cómo está mi sistema?", "Health Score y hallazgos críticos"
- **Auditoría rápida**: "Auditoría rápida de mi Linux", "Revisa configuración básica", "audit-quick"
- **Auditoría completa**: "Auditoría completa de mi Linux", "Revisa configuración, rendimiento, higiene", "Compliance CIS/Lynis", "audit-full"
- **Fingerprint / Perfil**: "Perfila mi sistema", "Detecta distro, kernel, servicios", "probe_system"
- **Generar informe**: "Genera informe HTML/MD de salud", "Diff temporal vs auditoría anterior"
- **NO usar cuando**: Ejecución de limpieza/optimización (→ `operar-mantenimiento`), hardening/forense (→ `operar-seguridad`)

## Principios Rectores (Alineados con Constitución ALIGNUX)

1. **Read-only por defecto** — Todo diagnóstico se realiza sin modificar el sistema.
2. **Salida estructurada y comparable** — Informes con puntuación de salud (0–100), hallazgos clasificados (P0–P4), y diff contra la ejecución anterior.
3. **Idempotencia y repetibilidad** — Los scripts de auditoría pueden ejecutarse N veces con el mismo resultado.
4. **Registro forense completo** — Cada comando propuesto, validado, ejecutado y su salida quedan en un log inmutable por sesión.

## Modos de Operación

| Modo          | Descripción                                             | Permisos          | Uso típico                                   |
| ------------- | ------------------------------------------------------- | ----------------- | -------------------------------------------- |
| `audit-quick` | Health-check read-only (5–10 min)                       | Solo lectura (R0) | Diagnóstico rápido, CI/CD, alertas           |
| `audit-full`  | Auditoría completa: higiene, rendimiento, configuración | Solo lectura (R0) | Auditoría programada, compliance, onboarding |

**Regla:** El agente **nunca** ejecuta acciones de escritura. Esta skill es puramente de diagnóstico.

## Flujo de Trabajo Estándar

### 1. Detección de Perfil y Fingerprint

```bash
./scripts/probe_system.py
```

Genera `system-profile.json` con: distro, gestor de paquetes, kernel, CPU/RAM/disco, servicios críticos, rutas protegidas, excepciones de usuario.

### 2. Ejecución del Modo Solicitado

- **audit-quick**: `./scripts/audit_quick.py` → `audit-quick-<timestamp>.json`
- **audit-full**: `./scripts/audit_full.py` → `audit-full-<timestamp>.json`

### 3. Generación de Informe

```bash
./scripts/report_render.py --input <audit-file> --output <report.md> --history <history-dir>
```

Producción: Markdown + HTML con Health Score, hallazgos P0–P4, diff temporal, KPIs.

### 4. Registro de Sesión

Todos los comandos, clasificaciones de riesgo, decisiones y salidas se anexan a `session-<timestamp>.log` (append-only).

## Formato de Salida: Health Score y Hallazgos

### Health Score (0–100)

Fórmula ponderada (ver `references/metrics-scoring.md`):

- **Seguridad (40%)**: evaluada por la skill hermana `operar-seguridad` (hardening, SSH, firewall, permisos, auditd). En informes combinados, tomar su Posture Score.
- **Actualización (25%)**: paquetes al día, noticias leídas, firmware, rebuild-detector
- **Higiene de paquetes (20%)**: huérfanos, foráneos, .pacnew, tamaño caché, AUR
- **Recursos (15%)**: disco, RAM, swap, boot time, servicios innecesarios

### Clasificación de Hallazgos

| Nivel  | Significado                                           | Acción                            |
| ------ | ----------------------------------------------------- | --------------------------------- |
| **P0** | Crítico: compromiso activo o inminente                | Bloqueo inmediato, requiere R2+   |
| **P1** | Alto: vulnerabilidad conocida, configuración insegura | Plan de remediación < 24h         |
| **P2** | Medio: desviación de baseline, deuda técnica          | Plan de remediación < 7 días      |
| **P3** | Bajo: optimización, limpieza, mejoras                 | Próxima ventana de mantenimiento  |
| **P4** | Informativo: observación, tendencia                   | Seguimiento, sin acción inmediata |

## Referencias Internas

- `references/safety-policy.md` — Lista blanca/negra de comandos, rutas protegidas, niveles de riesgo
- `references/pitfalls.md` — Falsos positivos y bugs conocidos de los checks (leer SIEMPRE antes de remediar un hallazgo)
- `references/audit-checklist.md` — Controles mapeados a CIS/Lynis con criticidad
- `references/arch-maintenance.md` — Rutinas pacman/AUR: huérfanos, .pacnew, caché, mirrorlist, rebuild-detector
- `references/debian-rhel-adapters.md` — Equivalencias apt/dnf
- `references/hardening-baseline.md` — (legado; el baseline de hardening activo vive en `../operar-seguridad/references/hardening-baseline.md`)
- `references/metrics-scoring.md` — Definición de KPIs y fórmula de puntuación
- `references/guided-interaction.md` — Flujo conversacional de 4 fases

## Herramientas

| Script              | Propósito                                                       | Modo           |
| ------------------- | --------------------------------------------------------------- | -------------- |
| `probe_system.py`   | Fingerprint del sistema + stack moderno, salida JSON            | Todos          |
| `audit_quick.py`    | Health-check higiene/updates P0+P1, salida JSON                 | audit-quick    |
| `audit_full.py`     | Higiene/updates P0-P4: reutiliza audit_quick + fase extendida   | audit-full     |
| `report_render.py`  | Genera informe MD/HTML con puntuación, hallazgos, diff temporal | Todos          |
| `session_logger.py` | Registro forense append-only por sesión                         | Todos (fuente) |
| `check_deps.py`     | Verifica dependencias requeridas y opcionales                   | Pre-flight     |
| `common.py`         | Checks compartidos + scoring/sshd                               | Interno        |

> Los scripts canónicos son **Python nativo** (sin subproceso a bash ni dependencia de `jq`).

## Dependencias

### Requeridas

- `python3` (≥ 3.10) — intérprete de los scripts
- `timeout` (coreutils) — timeouts de comandos
- `systemctl` (systemd) — gestión de servicios
- `ss` (iproute2) — sockets/red
- `df`, `find`, `grep`, `awk` — utilidades estándar

### Opcionales (mejoran cobertura)

- `lynis` — auditoría CIS extendida (se integra en `audit-full`)
- `smartmontools` — health de disco
- `fwupd` — actualizaciones de firmware
- `paccache` (pacman-contrib) — limpieza caché Arch
- `deborphan`, `needrestart` — huérfanos/servicios Debian
- `rpmconf`, `ucf` — gestión configs RPM/Debian

Verificar con: `./scripts/check_deps.py --verbose --install-hint`

## Interacción Guiada (Guided Interaction)

Al invocar `operar-salud-sistema`, el agente inicia un flujo conversacional de 4 fases: (1) Diagnóstico de contexto con `probe_system.py` y preguntas sobre objetivo/restricciones, (2) Selección de modo y profundidad según respuesta, (3) Ejecución read-only con confirmación, (4) Informe y próximos pasos adaptados al objetivo.

> Ver `references/guided-interaction.md` para el detalle completo con tablas de modos, preguntas exactas y flujos de confirmación.

## Plantillas de Prompt por Objetivo

### 🏥 Health-check / Monitoring

> "Haz un health-check rápido de mi servidor. Quiero saber Health Score y si hay algo crítico (P0/P1)."

### 🔒 Auditoría de Configuración / Compliance

> "Auditoría completa de mi Linux: configuración, rendimiento, higiene, compliance CIS/Lynis. Solo diagnóstico, sin ejecutar."

### 📊 Informe de Auditoría Previa

> "Genera informe HTML de la auditoría `audit-full-20260805-103000.json` con diff temporal vs anterior."

## Contexto Adaptativo (El agente ajusta según...)

| Factor             | Ajuste automático                                                                   |
| ------------------ | ----------------------------------------------------------------------------------- |
| **Distro**         | Arch → pacman/AUR/pacdiff; Debian → apt/ucf; RHEL → dnf/rpmconf/SELinux             |
| **Entorno prod**   | Más conservador: dry-run obligatorio, snapshots obligatorios, verificación estricta |
| **Entorno dev**    | Más ágil: dry-run opcional, snapshots opcionales, verificación básica               |
| **Compliance CIS** | Activa controles extendidos, genera evidencia, mapea hallazgos a controles CIS      |
| **Ventana corta**  | Prioriza P0/P1, salta P3/P4, dry-run rápido                                         |

## Ejemplos de Invocación Natural

| Usuario dice...                | Agente interpreta → Ejecuta                          |
| ------------------------------ | ---------------------------------------------------- |
| "¿Cómo está mi servidor?"      | `audit-quick` + informe ejecutivo                    |
| "Revisa configuración a fondo" | `audit-full` + hardening gaps (→ `operar-seguridad`) |
| "Perfila mi sistema"           | `probe_system.py` → `system-profile.json`            |
| "Genera informe HTML"          | `report_render.py --format html`                     |
| "Verifica dependencias"        | `check_deps.py --verbose --install-hint`             |

## Limitaciones Declaradas

- No puede verificar hardware sin `smartmontools`/`nvme-cli` instalados
- No audita servicios que no exponen métricas (binarios cerrados)
- No gestiona secretos/credenciales (fuera de alcance)
- Ejecución desatendida (cron) solo para R0

## Trazabilidad ALIGNUX

Esta skill implementa los principios de `disenar-constitucion`:

- **Identidad**: Prefijo `ALIGNUX.` en mayúsculas (identidad constitucional)
- **Coherencia**: Frontera clara con `operar-mantenimiento` y `operar-seguridad`, nomenclatura `familia.subdominio`
- **Estructura habilita**: Progressive disclosure, validador automatizado
- **Documentación viva**: Validador `tools/validate/skill_spec.py` como verdad ejecutable
- **Aprendizaje = despliegue**: Síntesis de ~4 décadas experiencia Linux en skill operativa
- **Herramientas amplifican**: Scripts nativos Python, humano decide

## Uso

Diagnóstico y auditoría de salud del SO: invocar ante health-check, auditoría rápida/completa, fingerprint, scoring de salud, hallazgos P0–P4, diff temporal. No usar para ejecución de limpieza/optimización (→ `operar-mantenimiento`) ni hardening/forense (→ `operar-seguridad`).

## Estructura

- `SKILL.md` — modos, flujo, scoring y plantillas de prompt.
- `references/` — safety-policy, pitfalls, audit-checklist, arch-maintenance, debian-rhel-adapters, hardening-baseline (legado), metrics-scoring, guided-interaction.
- `scripts/` — scripts canónicos `.py` + `tests/`.

## Referencias

- Internas: ver «Referencias Internas» más arriba.
- Herramientas: ver «Herramientas» más arriba (tabla script→propósito y modo).
