---
name: alignux-mantenimiento
description: >-
  Mantenimiento de sistemas Linux: higiene, actualizaciones, limpieza de
  cachés/logs/paquetes huérfanos, optimización de arranque y health-check. Incluye cribado
  de basura en disco (node_modules huérfanos, __pycache__, builds stale). Usar ante
  mantenimiento del SO, limpieza de espacio, rutina Arch/Debian/RHEL o 'cribar el
  filesystem'. No usar para hardening ni forense (→ alignux-seguridad).
license: MIT
metadata:
  author: Soluciones-Alexendros
  version: "0.1.0"
  dominio: alignux
  idioma: es

---
# ALIGNUX.mantenimiento

Skill para diagnóstico, auditoría, mantenimiento y optimización de sistemas Linux operada por un agente IA con seguridad estructural. Parte del sistema **ALIGNUX** — identidad constitucional en mayúsculas, coherencia sobre consistencia.

## Qué hace / Propósito

Mantener el sistema sano, ordenado y actualizado con riesgo controlado: health-check continuo, higiene de paquetes/cachés/logs, actualizaciones, optimización de arranque y recursos, y limpieza reversible aprobada por el operador.

## Cuándo usarme / Triggering

- **Health-check / Monitoring**: "Haz un health-check de mi servidor", "¿Cómo está mi sistema?", "Health Score y hallazgos críticos"
- **Auditoría completa**: "Auditoría completa de mi Linux", "Revisa configuración, seguridad, rendimiento", "Compliance CIS/Lynis"
- **Mantenimiento rutinario**: "Ejecuta mantenimiento semanal", "Actualizaciones, limpieza cachés, huérfanos", "Verifica .pacnew"
- **Optimización**: "Optimiza mi sistema", "Plan de optimización P1-P4", "Boot time, espacio, superficie de ataque"
- **Limpieza aprobada**: "Ejecuta limpieza", "Limpia cachés y logs", "Requiere snapshot + aprobación"
- **Verificar comando**: "Clasifica este comando", "¿Qué riesgo tiene `pacman -Syu`?", "risk_gate"
- **Generar informe**: "Genera informe HTML/MD", "Diff temporal vs auditoría anterior"
- **NO usar cuando**: Auditoría de seguridad pura (→ `ALIGNUX.seguridad`), forense profunda, hardening execution, AppArmor lifecycle

## Principios Rectores (Alinenados con Constitución ALIGNUX)

1. **Read-only por defecto** — Todo diagnóstico se realiza sin modificar el sistema. La escritura requiere escalado explícito.
2. **Ejecución reversible** — Toda acción destructiva va precedida de captura de estado (snapshot de paquetes, backup de configs, lista de archivos afectados) que permita rollback.
3. **Seguridad en capas** — Deny-list estructural → Validador determinista (`risk_gate.py`) → Reversibilidad → Confirmación humana graduada → Instrucciones del skill.
4. **Salida estructurada y comparable** — Informes con puntuación de salud (0–100), hallazgos clasificados (P0–P4), y diff contra la ejecución anterior.
5. **Idempotencia y repetibilidad** — Los scripts de rutina pueden ejecutarse N veces con el mismo resultado.
6. **Registro forense completo** — Cada comando propuesto, validado, ejecutado y su salida quedan en un log inmutable por sesión.

## Frontera con ALIGNUX.seguridad

| **ALIGNUX.mantenimiento** | **ALIGNUX.seguridad** |
|---------------------------|----------------------|
| Actualizaciones paquetes, cachés, huérfanos | Firewall, AppArmor, auditd, integridad (AIDE) |
| Health score, optimización arranque/recursos | Forense: journald, auth.log, denials.log |
| Higiene de paquetes, .pacnew, tamaño caché | CVEs, vulnerabilidades, escaneos malware/rootkit |
| Limpieza logs (rotación, vacuum) | Hardening CIS, SSH, sysctl seguridad |
| Snapshots y mantenimiento rutinario | Ciclo vida perfiles AppArmor (genprof→enforce) |

**Regla:** Cuando una petición toca ambos mundos, la parte de higiene/mantenimiento es de esta skill y la defensiva de `ALIGNUX.seguridad`.

## Modos de Operación

| Modo | Descripción | Permisos | Uso típico |
|------|-------------|----------|------------|
| `audit-quick` | Health-check read-only (5–10 min) | Solo lectura (R0) | Diagnóstico rápido, CI/CD, alertas |
| `audit-full` | Auditoría completa: seguridad, rendimiento, higiene, configuración | Solo lectura (R0) | Auditoría programada, compliance, onboarding |
| `routine` | Mantenimiento periódico: actualizaciones, cachés, logs, huérfanos | R0 + R1 con snapshot | Cron semanal, mantenimiento planificado |
| `optimize` | Informe con plan de acción priorizado (P1–P4), sin ejecución | Solo lectura (R0) | Planificación, revisión de arquitectura |
| `clean` | Ejecución de acciones correctivas aprobadas | R1 + R2 con aprobación humana | Remediación tras auditoría, limpieza profunda |

**Regla:** El agente **nunca** ejecuta acciones de escritura sin que el usuario solicite explícitamente el modo `clean` o `routine` y apruebe el plan mostrado en dry-run.

## Flujo de Trabajo Estándar

### 1. Detección de Perfil y Fingerprint
```bash
./scripts/probe_system.py
```
Genera `system-profile.json` con: distro, gestor de paquetes, kernel, CPU/RAM/disco, servicios críticos, rutas protegidas, excepciones de usuario.

### 2. Ejecución del Modo Solicitado
- **audit-quick**: `./scripts/audit_quick.py` → `audit-quick-<timestamp>.json`
- **audit-full**: `./scripts/audit_full.py` → `audit-full-<timestamp>.json`
- **routine**: `./scripts/clean_routine.py --dry-run` → muestra plan → si aprueba: `--execute` con snapshot previo
- **optimize**: analiza auditoría previa + `./scripts/report_render.py --mode optimize` → `optimization-plan-<timestamp>.md`
- **clean**: ejecuta plan de optimización aprobado con `./scripts/clean_routine.py --execute` (requiere snapshot previo verificado)

### 3. Generación de Informe
```bash
./scripts/report_render.py --input <audit-file> --output <report.md> --history <history-dir>
```
Producción: Markdown + HTML con Health Score, hallazgos P0–P4, diff temporal, KPIs.

### 4. Registro de Sesión
Todos los comandos, clasificaciones de riesgo, decisiones y salidas se anexan a `session-<timestamp>.log` (append-only).

## Política de Seguridad (Resumen)

Ver `references/safety-policy.md` para detalle completo.

| Nivel | Descripción | Ejemplos | Requisito |
|-------|-------------|----------|-----------|
| **R0** | Solo lectura, sin efectos colaterales | `ls`, `cat`, `systemctl status`, `pacman -Q`, `df` | Libre |
| **R1** | Escritura reversible, bajo riesgo | `paccache -r`, `journalctl --vacuum-time`, `pacman -Rns (huérfanos confirmados)` | Snapshot previo obligatorio |
| **R2** | Escritura con riesgo, requiere aprobación humana | Cambios SSH, firewall, kernel, bootloader, particiones, `pacman -Syu` | Aprobación explícita + plan documentado + snapshot |
| **R3** | Prohibido (bloqueo determinista) | `rm -rf /`, `mkfs.*`, `dd of=/dev/...`, `pacman -Rdd`, `curl \| sh`, `chmod -R 777 /` | Bloqueado siempre, sin bypass |

**Rutas protegidas (nunca tocar sin R2+ y aprobación):**
`/boot`, `/etc/fstab`, `/etc/passwd`, `/etc/shadow`, `/etc/sudoers`, `/etc/ssh/sshd_config`, `/usr`, `/lib/modules`, particiones EFI, `/var/lib/pacman/local`

## Perfil de Sistema (system-profile.yaml)

La skill se adapta al perfil, no asume. Ejemplo mínimo:

```yaml
distro: "endeavouros"
package_manager: "pacman"
aur_helper: "yay"
kernel: "linux-cachyos"
critical_services:
  - "NetworkManager"
  - "systemd-resolved"
  - "sshd"
protected_paths:
  - "/boot"
  - "/etc/fstab"
  - "/etc/ssh/sshd_config"
exceptions:
  - path: "/home/user/.cache"
    reason: "Usuario gestiona su propia caché"
  - package: "nvidia"
    reason: "Drivers propietarios, actualización manual"
snapshot_tool: "timeshift"  # o "snapper", "tar", "none"
```

## Formato de Salida: Health Score y Hallazgos

### Health Score (0–100)
Fórmula ponderada (ver `references/metrics-scoring.md`):
- **Seguridad (40%)**: evaluada por la skill hermana `ALIGNUX.seguridad` (hardening, SSH, firewall, permisos, auditd). En informes combinados, tomar su Posture Score.
- **Actualización (25%)**: paquetes al día, noticias leídas, firmware, rebuild-detector
- **Higiene de paquetes (20%)**: huérfanos, foráneos, .pacnew, tamaño caché, AUR
- **Recursos (15%)**: disco, RAM, swap, boot time, servicios innecesarios

### Clasificación de Hallazgos
| Nivel | Significado | Acción |
|-------|-------------|--------|
| **P0** | Crítico: compromiso activo o inminente | Bloqueo inmediato, requiere R2+ |
| **P1** | Alto: vulnerabilidad conocida, configuración insegura | Plan de remediación < 24h |
| **P2** | Medio: desviación de baseline, deuda técnica | Plan de remediación < 7 días |
| **P3** | Bajo: optimización, limpieza, mejoras | Próxima ventana de mantenimiento |
| **P4** | Informativo: observación, tendencia | Seguimiento, sin acción inmediata |

## Referencias Internas

- `references/safety-policy.md` — Lista blanca/negra de comandos, rutas protegidas, niveles de riesgo
- `references/pitfalls.md` — Falsos positivos y bugs conocidos de los checks (leer SIEMPRE antes de remediar un hallazgo)
- `references/audit-checklist.md` — Controles mapeados a CIS/Lynis con criticidad
- `references/arch-maintenance.md` — Rutinas pacman/AUR: huérfanos, .pacnew, caché, mirrorlist, rebuild-detector
- `references/debian-rhel-adapters.md` — Equivalencias apt/dnf
- `references/hardening-baseline.md` — (legado; el baseline de hardening activo vive en `../alignux-seguridad/references/hardening-baseline.md`)
- `references/metrics-scoring.md` — Definición de KPIs y fórmula de puntuación

## Herramientas

| Script | Propósito | Modo |
|--------|-----------|------|
| `probe_system.py` | Fingerprint del sistema (solo lectura) | Todos |
| `audit_quick.py` | Health-check read-only, salida JSON | audit-quick |
| `audit_full.py` | Auditoría completa: 46+ controles P0-P4 + integración lynis | audit-full |
| `risk_gate.py` | Validador determinista pre-ejecución (hook) | clean, routine |
| `snapshot_state.py` | Captura pre-cambio: paquetes, configs, espacio, servicios | routine, clean |
| `clean_routine.py` | Limpieza aprobada: paccache, journal vacuum, huérfanos | routine, clean |
| `report_render.py` | Genera informe MD/HTML con puntuación, hallazgos, diff | Todos |
| `session_logger.py` | Registro forense append-only por sesión | Todos (fuente) |
| `check_deps.py` | Verifica dependencias requeridas y opcionales | Pre-flight |
| `common.py` | Helpers compartidos (subprocess, distro, scoring, sshd_effective) | Interno |

> Los scripts canónicos son **Python nativo** (sin subproceso a bash ni dependencia de `jq`). Las versiones `.sh` legado fueron eliminadas en v0.1.0; los scripts canónicos son Python nativo.

## Dependencias

### Requeridas
- `python3` (≥ 3.10) — intérprete de los scripts portados
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

Al invocar `ALIGNUX.mantenimiento`, el agente inicia un flujo conversacional estructurado para entender objetivo, contexto y restricciones antes de ejecutar. El flujo tiene 4 fases:

### Fase 1: Diagnóstico de Contexto (Auto-detección + Preguntas)

El agente ejecuta `probe_system.py` automáticamente y pregunta:

```
🔍 Contexto detectado:
  • Distro: Ubuntu 24.04 (debian family)
  • Kernel: 7.0.0-29-generic
  • Paquetes: 2523 (apt)
  • Firewall: ufw activo
  • Disco /: 8% usado (937G/824G libre)
  • Servicios fallidos: 0

🎯 ¿Cuál es tu objetivo principal?
  1. Health-check rápido (audit-quick, ~3 min, solo lectura)
  2. Auditoría completa + hardening (audit-full, ~15 min, solo lectura)
  3. Mantenimiento rutinario (routine: updates, limpieza, huérfanos)
  4. Plan de optimización priorizado (optimize: plan P1-P4 sin ejecutar)
  5. Ejecutar limpieza aprobada (clean: requiere snapshot + aprobación)
  6. Verificar comando específico (risk_gate: clasificar riesgo R0-R3)
  7. Ver dependencias / diagnóstico (check_deps / probe_system)
  8. Generar informe de auditoría previa (report_render)

📋 ¿Hay restricciones o contexto adicional?
  • Entorno: [producción / staging / desarrollo / personal]
  • Ventana de mantenimiento: [inmediata / programada / sin ventana]
  • Nivel de riesgo tolerado: [conservador / estándar / agresivo]
  • Requiere compliance: [CIS / PCI-DSS / HIPAA / ninguno]
  • Snapshot tool disponible: [timeshift / snapper / btrfs / tar / none]
```

### Fase 2: Selección de Modo y Profundidad

Según respuesta, el agente propone plan concreto:

| Objetivo | Modo | Profundidad | Tiempo | Output |
|----------|------|-------------|--------|--------|
| Health-check | `audit-quick` | P0+P1 críticos | ~3 min | JSON + Health Score |
| Auditoría completa | `audit-full` | P0-P4 + lynis | ~15 min | JSON + Health Score + diff |
| Mantenimiento | `routine` | dry-run → execute | variable | Plan + JSON + verificación |
| Optimización | `optimize` | P1-P4 plan | ~5 min | Markdown plan P1-P4 |
| Limpieza | `clean` | execute + verify | variable | JSON + verificación post |
| Verificar comando | `risk_gate` | clasificación R0-R3 | <1s | Clasificación + requisitos |

### Fase 3: Ejecución con Confirmación Graduada

Para cada acción de escritura (R1+), el agente:

1. **Muestra plan en dry-run** con comandos exactos, riesgo, espacio a liberar
2. **Solicita confirmación explícita** (sí/no/modificar)
3. **Crea snapshot** (`snapshot_state.py`) si R1+
4. **Ejecuta con `risk_gate.py`** validando cada comando
5. **Verifica post-acción** (re-ejecuta checks afectados)
6. **Registra en log forense** (`session_logger.py`)

### Fase 4: Informe y Próximos Pasos

Genera informe adaptado al objetivo:

- **Health-check**: Resumen ejecutivo + Health Score + top 5 hallazgos
- **Auditoría completa**: Informe técnico + diff temporal + compliance gaps
- **Mantenimiento/Limpieza**: Resumen acciones + espacio liberado + verificación
- **Optimización**: Plan P1-P4 con impacto/riesgo/esfuerzo + comandos listos
- **Siempre**: Próximos pasos recomendados + comandos listos para copiar

---

## Quickstart Interactivo (Copia y pega)

```bash
# 1. Inicio guiado (ejecuta probe + hace preguntas)
./scripts/check_deps.py --verbose && ./scripts/probe_system.py

# 2. El agente te guiará según tus respuestas...
# Ejemplo flujo típico:
# → "Quiero health-check rápido" → ./scripts/audit_quick.py
# → "Quiero auditoría completa" → ./scripts/audit_full.py
# → "Quiero limpiar" → ./scripts/clean_routine.py --dry-run → revisar → --execute

# 3. Generar informe final
./scripts/report_render.py --input audit-*.json --output report.md --format md
./scripts/report_render.py --input audit-*.json --output report.html --format html
```

---

## Plantillas de Prompt por Objetivo

### 🏥 Health-check / Monitoring
> "Haz un health-check rápido de mi servidor. Quiero saber Health Score y si hay algo crítico (P0/P1)."

### 🔒 Auditoría de Seguridad / Compliance
> Redirigir a la skill hermana **`ALIGNUX.seguridad`** (postura defensiva, forense, vulnerabilidades, hardening, escaneos). Esta skill solo aporta el contexto de higiene/actualizaciones cuando un informe es mixto.

### 🧹 Mantenimiento Rutinario
> "Ejecuta mantenimiento semanal: actualizaciones, limpieza cachés/logs, huérfanos, verifica .pacnew. Muestra plan en dry-run antes de ejecutar."

### ⚡ Optimización
> "Analiza mi sistema y dame un plan de optimización priorizado (P1-P4): espacio, boot time, superficie de ataque, deuda técnica. Sin ejecutar, solo plan."

### 🔧 Verificar Comando Específico
> "Clasifica este comando: `pacman -Syu`. ¿Qué riesgo tiene? ¿Qué snapshot necesito? ¿Es R1/R2/R3?"

### 📊 Informe de Auditoría Previa
> "Genera informe HTML de la auditoría `audit-full-20260805-103000.json` con diff temporal vs anterior."

---

## Contexto Adaptativo (El agente ajusta según...)

| Factor | Ajuste automático |
|--------|-------------------|
| **Distro** | Arch → pacman/AUR/pacdiff; Debian → apt/ucf; RHEL → dnf/rpmconf/SELinux |
| **Entorno prod** | Más conservador: dry-run obligatorio, snapshots obligatorios, verificación estricta |
| **Entorno dev** | Más ágil: dry-run opcional, snapshots opcionales, verificación básica |
| **Compliance CIS** | Activa controles extendidos, genera evidencia, mapea hallazgos a controles CIS |
| **Ventana corta** | Prioriza P0/P1, salta P3/P4, dry-run rápido |
| **Sin snapshot tool** | Degrada a solo-informe para R1+, requiere confirmación manual extra |

---

## Ejemplos de Invocación Natural

| Usuario dice... | Agente interpreta → Ejecuta |
|-----------------|----------------------------|
| "¿Cómo está mi servidor?" | `audit-quick` + informe ejecutivo |
| "Revisa seguridad a fondo" | `audit-full` + hardening gaps (→ `ALIGNUX.seguridad`) |
| "Limpia el sistema" | `routine` dry-run → confirmar → execute |
| "Optimiza el arranque" | `optimize` → plan P1-P4 boot time |
| "¿Puedo borrar esto?" | `risk_gate.py "comando"` → clasificación |
| "Genera informe HTML" | `report_render.py --format html` |
| "Verifica dependencias" | `check_deps.py --verbose --install-hint` |

---

## Perfil de Este Equipo (alexendros-aerox16)

Información específica del equipo local (Ubuntu 26.04, apt + snap, sin flatpak):

- CPU **Ryzen AI 7 350 + RTX 5060**; kernel `linux-image-generic-hwe-26.04`.
- WiFi Realtek **RTL8852CE** (`rtw89_8852ce`) con crashes de firmware conocidos (`[ERR]fw PC`, `SER catches error 0x999`); mitigación en `/etc/modprobe.d/rtw89-8852ce.conf` (ASPM y power-save off). Las desautenticaciones `locally_generated=1` **no son culpa del router**.
- Firewall ufw (deny incoming); SSH en 0.0.0.0:22 (excepción documentada: WiFi doméstica DHCP, no restringir ListenAddress).
- auditd con reglas base; journald persistente. Sin timeshift/snapper → snapshots manuales con `snapshot_state.py`.
- Servicios de usuario activos: `voicebox-backend.service`, `ydotoold.service`.

### Gestión de sudo en este equipo

`/etc/sudoers.d/90-mantenimiento` concede NOPASSWD acotado para: `apt`, `apt-get`, `dpkg`, `ufw`, `auditctl`, `augenrules`, `sysctl`, `fwupdmgr`, `snap`, `systemctl`, `update-initramfs`, `modprobe`. Protocolo:

1. Si el comando está cubierto, usar `sudo -n <comando>` directamente (nunca pedir contraseña).
2. Si hace falta un comando root **no cubierto**, agrupar todas las acciones root pendientes en un único `/tmp/fix-*.sh` y ejecutarlo una sola vez con askpass (un popup por sesión como máximo, avisando antes).
3. Si un comando root se repite, proponer añadirlo (con argumentos concretos) a `/etc/sudoers.d/90-mantenimiento` y validar con `visudo -cf`.
4. **Nunca** pedir contraseña en chat ni usar `echo pass | sudo -S`, ni NOPASSWD para `rm`/`find`/shells/`ALL`.

---

## Limitaciones Declaradas

- No puede verificar hardware sin `smartmontools`/`nvme-cli` instalados
- No audita servicios que no exponen métricas (binarios cerrados)
- No gestiona secretos/credenciales (fuera de alcance)
- Modo `clean`/`routine` con R1+ requiere entorno con hooks deterministas (`risk_gate.py`); sin ellos, degrada a solo-informe
- Ejecución desatendida (cron) solo para R0; R1+ en modo programado exige aprobación previa del plan

---

## Trazabilidad ALIGNUX

Esta skill implementa los principios de `ALIGNUX.constitucion`:
- **Identidad**: Prefijo `ALIGNUX.` en mayúsculas (identidad constitucional)
- **Coherencia**: Frontera clara con `ALIGNUX.seguridad`, nomenclatura `dominio.subdominio`
- **Estructura habilita**: Tags `sistema.ALINKUX.*`, progressive disclosure, validador automatizado
- **Documentación viva**: Validador `tools/validate/skill_spec.py` como verdad ejecutable
- **Aprendizaje = despliegue**: Síntesis de ~4 décadas experiencia Linux en skill operativa
- **No límites coyunturales**: Diseño para siguiente paradigma (agentes, IA, edge)
- **Herramientas amplifican**: `risk_gate.py` valida, humano decide

## Cribado de disco (absorbido)

Modo de higiene de filesystem: ejecutar scripts en `scripts/cribado-extra/` si contienen ejecutables, o `references/cribado-source.md`. Solo proponer borrados; nunca `rm` sin confirmación explícita del operador.

## Uso

Mantenimiento del SO y del filesystem: invocar ante health-check, auditoría, rutina, optimización o limpieza aprobada, o ante «cribar el filesystem». No usar para hardening ni forense (ver `description` del frontmatter).

## Estructura

- `SKILL.md` — modos, flujo, política R0–R3, scoring y plantillas de prompt.
- `references/` — safety-policy, pitfalls, audit-checklist, arch-maintenance, debian-rhel-adapters, hardening-baseline (legado), metrics-scoring y cribado-source (fuente absorbida).
- `scripts/` — scripts canónicos `.py` + legado `.sh` eliminado en v0.1.0, `tests/` y `cribado-extra/`.

## Referencias

- Internas: ver «Referencias Internas» más arriba; el baseline de hardening activo vive en `../alignux-seguridad/references/hardening-baseline.md` (existe).
- Herramientas: ver «Herramientas» más arriba (tabla script→propósito y modo).
