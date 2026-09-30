---
name: operar-mantenimiento
description: >
  Mantenimiento de sistemas Linux: higiene, actualizaciones, limpieza de
  cachés/logs/paquetes huérfanos, optimización de arranque, plan de acción P1–P4,
  ejecución de limpieza aprobada (snapshot + risk_gate). Incluye cribado de basura
  en disco (node_modules huérfanos, __pycache__, builds stale). Usar ante
  mantenimiento del SO, limpieza de espacio, rutina Arch/Debian/RHEL, optimización
  o 'cribar el filesystem'. No usar para health-check/auditoría (→ operar-salud-sistema)
  ni hardening/forense (→ operar-seguridad).
license: MIT
metadata:
  author: Soluciones-Alexendros
  version: "2.1.0"
  dominio: operar
  tipo: atomic
  idioma: es
---

# Linux Mantenimiento — Ejecución de mantenimiento y optimización de sistemas Linux

Skill para ejecución de mantenimiento, optimización y limpieza de sistemas Linux operada por un agente IA con seguridad estructural. Parte del sistema **ALIGNUX** — identidad constitucional en mayúsculas, coherencia sobre consistencia.

## Qué hace / Propósito

Mantener el sistema sano, ordenado y actualizado con riesgo controlado: higiene de paquetes/cachés/logs, actualizaciones, optimización de arranque y recursos, plan de acción priorizado (P1–P4), y limpieza reversible aprobada por el operador. Requiere auditoría previa de `operar-salud-sistema`.

## Cuándo usarme / Triggering

- **Mantenimiento rutinario**: "Ejecuta mantenimiento semanal", "Actualizaciones, limpieza cachés, huérfanos", "Verifica .pacnew"
- **Optimización**: "Optimiza mi sistema", "Plan de optimización P1-P4", "Boot time, espacio, superficie de ataque" (requiere auditoría previa)
- **Limpieza aprobada**: "Ejecuta limpieza", "Limpia cachés y logs", "Requiere snapshot + aprobación"
- **Verificar comando**: "Clasifica este comando", "¿Qué riesgo tiene `pacman -Syu`?", "risk_gate"
- **NO usar cuando**: Health-check/auditoría (→ `operar-salud-sistema`), auditoría de seguridad pura (→ `operar-seguridad`), forense profunda, hardening execution, AppArmor lifecycle

## Principios Rectores (Alineados con Constitución ALIGNUX)

1. **Read-only por defecto** — Todo diagnóstico se realiza sin modificar el sistema. La escritura requiere escalado explícito.
2. **Ejecución reversible** — Toda acción destructiva va precedida de captura de estado (snapshot de paquetes, backup de configs, lista de archivos afectados) que permita rollback.
3. **Seguridad en capas** — Deny-list estructural → Validador determinista (`risk_gate.py`) → Reversibilidad → Confirmación humana graduada → Instrucciones del skill.
4. **Salida estructurada y comparable** — Planes de optimización con puntuación P1–P4, y diff contra la ejecución anterior.
5. **Idempotencia y repetibilidad** — Los scripts de rutina pueden ejecutarse N veces con el mismo resultado.
6. **Registro forense completo** — Cada comando propuesto, validado, ejecutado y su salida quedan en un log inmutable por sesión.

## Frontera con operar-seguridad

| **operar-mantenimiento**                    | **operar-seguridad**                             |
| ------------------------------------------- | ------------------------------------------------ |
| Actualizaciones paquetes, cachés, huérfanos | Firewall, AppArmor, auditd, integridad (AIDE)    |
| Optimización arranque/recursos, plan P1-P4  | Forense: journald, auth.log, denials.log         |
| Higiene de paquetes, .pacnew, tamaño caché  | CVEs, vulnerabilidades, escaneos malware/rootkit |
| Limpieza logs (rotación, vacuum)            | Hardening CIS, SSH, sysctl seguridad             |
| Snapshots y mantenimiento rutinario         | Ciclo vida perfiles AppArmor (genprof→enforce)   |

**Regla:** Cuando una petición toca ambos mundos, la parte de higiene/mantenimiento es de esta skill y la defensiva de `operar-seguridad`.

## Frontera con operar-salud-sistema

| **operar-mantenimiento**            | **operar-salud-sistema**             |
| ----------------------------------- | ------------------------------------ |
| Ejecución: routine, optimize, clean | Diagnóstico: audit-quick, audit-full |
| Requiere auditoría previa           | Genera auditoría + health score      |
| Escritura R1/R2 con snapshot        | Solo lectura R0                      |

**Regla:** `operar-mantenimiento` consume la auditoría de `operar-salud-sistema` para generar planes de optimización y ejecutar limpieza.

## Modos de Operación

| Modo       | Descripción                                                       | Permisos                      | Uso típico                                    |
| ---------- | ----------------------------------------------------------------- | ----------------------------- | --------------------------------------------- |
| `routine`  | Mantenimiento periódico: actualizaciones, cachés, logs, huérfanos | R0 + R1 con snapshot          | Cron semanal, mantenimiento planificado       |
| `optimize` | Informe con plan de acción priorizado (P1–P4), sin ejecución      | Solo lectura (R0)             | Planificación, revisión de arquitectura       |
| `clean`    | Ejecución de acciones correctivas aprobadas                       | R1 + R2 con aprobación humana | Remediación tras auditoría, limpieza profunda |

**Regla:** El agente **nunca** ejecuta acciones de escritura sin que el usuario solicite explícitamente el modo `clean` o `routine` y apruebe el plan mostrado en dry-run.

## Flujo de Trabajo Estándar

### 1. Prerrequisito: Auditoría Previa

```bash
# La skill requiere una auditoría de operar-salud-sistema
./scripts/clean_routine.py --dry-run --audit audit-full-<timestamp>.json
```

### 2. Ejecución del Modo Solicitado

- **routine**: `./scripts/clean_routine.py --dry-run --audit <audit-file>` → muestra plan → si aprueba: `--execute` con snapshot previo
- **optimize**: analiza auditoría previa + `./scripts/report_render.py --mode optimize` → `optimization-plan-<timestamp>.md`
- **clean**: ejecuta plan de optimización aprobado con `./scripts/clean_routine.py --execute --audit <audit-file>` (requiere snapshot previo verificado)

### 3. Registro de Sesión

Todos los comandos, clasificaciones de riesgo, decisiones y salidas se anexan a `session-<timestamp>.log` (append-only).

## Política de Seguridad (Resumen)

Ver `references/safety-policy.md` para detalle completo.

| Nivel  | Descripción                                      | Ejemplos                                                                              | Requisito                                          |
| ------ | ------------------------------------------------ | ------------------------------------------------------------------------------------- | -------------------------------------------------- |
| **R0** | Solo lectura, sin efectos colaterales            | `ls`, `cat`, `systemctl status`, `pacman -Q`, `df`                                    | Libre                                              |
| **R1** | Escritura reversible, bajo riesgo                | `paccache -r`, `journalctl --vacuum-time`, `pacman -Rns (huérfanos confirmados)`      | Snapshot previo obligatorio                        |
| **R2** | Escritura con riesgo, requiere aprobación humana | Cambios SSH, firewall, kernel, bootloader, particiones, `pacman -Syu`                 | Aprobación explícita + plan documentado + snapshot |
| **R3** | Prohibido (bloqueo determinista)                 | `rm -rf /`, `mkfs.*`, `dd of=/dev/...`, `pacman -Rdd`, `curl \| sh`, `chmod -R 777 /` | Bloqueado siempre, sin bypass                      |

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
snapshot_tool: "timeshift" # o "snapper", "tar", "none"
```

## Herramientas

| Script              | Propósito                                                                                                                | Modo           |
| ------------------- | ------------------------------------------------------------------------------------------------------------------------ | -------------- |
| `risk_gate.py`      | Validador determinista pre-ejecución, anti-evasión sudo/env/subshells (hook)                                             | clean, routine |
| `snapshot_state.py` | Captura pre-cambio + `--list` y `--rollback` (dry-run; `--execute` restaura /etc)                                        | routine, clean |
| `clean_routine.py`  | Limpieza aprobada: paccache, journal vacuum, huérfanos, needrestart, caches userspace, fwupdmgr opt-in `--firmware` (R2) | routine, clean |
| `report_render.py`  | Genera informe MD/HTML con plan P1-P4, hallazgos, diff temporal `--prev`                                                 | optimize       |
| `session_logger.py` | Registro forense append-only por sesión                                                                                  | Todos (fuente) |
| `check_deps.py`     | Verifica dependencias requeridas y opcionales                                                                            | Pre-flight     |
| `common.py`         | Utilidades compartidas + scoring/sshd                                                                                    | Interno        |

> Los scripts canónicos son **Python nativo** (sin subproceso a bash ni dependencia de `jq`).

## Dependencias

### Requeridas

- `python3` (≥ 3.10) — intérprete de los scripts portados
- `timeout` (coreutils) — timeouts de comandos
- `systemctl` (systemd) — gestión de servicios
- `ss` (iproute2) — sockets/red
- `df`, `find`, `grep`, `awk` — utilidades estándar

### Opcionales (mejoran cobertura)

- `lynis` — auditoría CIS extendida (se integra en auditoría previa)
- `smartmontools` — health de disco
- `fwupd` — actualizaciones de firmware
- `paccache` (pacman-contrib) — limpieza caché Arch
- `deborphan`, `needrestart` — huérfanos/servicios Debian
- `rpmconf`, `ucf` — gestión configs RPM/Debian

Verificar con: `./scripts/check_deps.py --verbose --install-hint`

## Interacción Guiada (Guided Interaction)

Al invocar `operar-mantenimiento`, el agente inicia un flujo conversacional de 4 fases: (1) Diagnóstico de contexto verificando auditoría previa de `operar-salud-sistema` y preguntas sobre objetivo/restricciones, (2) Selección de modo y profundidad según respuesta, (3) Ejecución con confirmación graduada (dry-run → snapshot → risk_gate → verificación), (4) Informe y próximos pasos adaptados al objetivo.

> Ver [references/guided-interaction.md](references/guided-interaction.md) para el detalle completo con tablas de modos, preguntas exactas y flujos de confirmación.

---

## Quickstart Interactivo (Copia y pega)

```bash
# 1. Prerrequisito: auditoría de operar-salud-sistema
../operar-salud-sistema/scripts/audit_full.py

# 2. Inicio guiado (ejecuta check_deps + hace preguntas)
./scripts/check_deps.py --verbose

# 3. El agente te guiará según tus respuestas...
# Ejemplo flujo típico:
# → "Quiero mantenimiento semanal" → ./scripts/clean_routine.py --dry-run --audit ../operar-salud-sistema/audit-full-*.json
# → "Quiero optimizar" → ./scripts/report_render.py --mode optimize --input ../operar-salud-sistema/audit-full-*.json
# → "Quiero limpiar" → ./scripts/clean_routine.py --execute --audit ../operar-salud-sistema/audit-full-*.json
```

---

## Plantillas de Prompt por Objetivo

### 🧹 Mantenimiento Rutinario

> "Ejecuta mantenimiento semanal: actualizaciones, limpieza cachés/logs, huérfanos, verifica .pacnew. Muestra plan en dry-run antes de ejecutar."

### ⚡ Optimización

> "Analiza mi sistema y dame un plan de optimización priorizado (P1-P4): espacio, boot time, superficie de ataque, deuda técnica. Sin ejecutar, solo plan. Usa la auditoría previa de operar-salud-sistema."

### 🔧 Verificar Comando Específico

> "Clasifica este comando: `pacman -Syu`. ¿Qué riesgo tiene? ¿Qué snapshot necesito? ¿Es R1/R2/R3?"

---

## Contexto Adaptativo (El agente ajusta según...)

| Factor                | Ajuste automático                                                                   |
| --------------------- | ----------------------------------------------------------------------------------- |
| **Distro**            | Arch → pacman/AUR/pacdiff; Debian → apt/ucf; RHEL → dnf/rpmconf/SELinux             |
| **Entorno prod**      | Más conservador: dry-run obligatorio, snapshots obligatorios, verificación estricta |
| **Entorno dev**       | Más ágil: dry-run opcional, snapshots opcionales, verificación básica               |
| **Compliance CIS**    | Activa controles extendidos, genera evidencia, mapea hallazgos a controles CIS      |
| **Ventana corta**     | Prioriza P0/P1, salta P3/P4, dry-run rápido                                         |
| **Sin snapshot tool** | Degrada a solo-informe para R1+, requiere confirmación manual extra                 |

---

## Ejemplos de Invocación Natural

| Usuario dice...            | Agente interpreta → Ejecuta                                   |
| -------------------------- | ------------------------------------------------------------- |
| "Limpia el sistema"        | `routine` dry-run → confirmar → execute                       |
| "Optimiza el arranque"     | `optimize` → plan P1-P4 boot time (requiere auditoría previa) |
| "¿Puedo borrar esto?"      | `risk_gate.py "comando"` → clasificación                      |
| "Genera plan optimización" | `report_render.py --mode optimize` con auditoría previa       |

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
- Requiere auditoría previa de `operar-salud-sistema` para modos `optimize` y `clean`

---

## Trazabilidad ALIGNUX

Esta skill implementa los principios de `disenar-constitucion`:

- **Identidad**: Prefijo `ALIGNUX.` en mayúsculas (identidad constitucional)
- **Coherencia**: Frontera clara con `operar-seguridad` y `operar-salud-sistema`, nomenclatura `familia.subdominio`
- **Estructura habilita**: Tags `sistema.ALINKUX.*`, progressive disclosure, validador automatizado
- **Documentación viva**: Validador `tools/validate/skill_spec.py` como verdad ejecutable
- **Aprendizaje = despliegue**: Síntesis de ~4 décadas experiencia Linux en skill operativa
- **No límites coyunturales**: Diseño para siguiente paradigma (agentes, IA, edge)
- **Herramientas amplifican**: `risk_gate.py` valida, humano decide

## Cribado de disco (absorbido)

Modo de higiene de filesystem: ejecutar scripts en `scripts/cribado-extra/` si contienen ejecutables, o `references/cribado-source.md`. Solo proponer borrados; nunca `rm` sin confirmación explícita del operador.

## Uso

Mantenimiento del SO y del filesystem: invocar ante mantenimiento rutinario, optimización, limpieza aprobada, o ante «cribar el filesystem». Requiere auditoría previa de `operar-salud-sistema`. No usar para health-check/auditoría (→ `operar-salud-sistema`) ni hardening/forense (→ `operar-seguridad`).

## Estructura

- `SKILL.md` — modos, flujo, política R0–R3, scoring y plantillas de prompt.
- `references/` — safety-policy, pitfalls, audit-checklist, arch-maintenance, debian-rhel-adapters, hardening-baseline (legado), metrics-scoring, cribado-source (fuente absorbida) y guided-interaction.
- `scripts/` — scripts canónicos `.py` + `tests/` y `cribado-extra/`.

## Referencias

- Internas: ver «Referencias Internas» más arriba; el baseline de hardening activo vive en `../operar-seguridad/references/hardening-baseline.md` (existe).
- Herramientas: ver «Herramientas» más arriba (tabla script→propósito y modo).
- Auditoría previa: `operar-salud-sistema` (audit-quick, audit-full, report_render).
