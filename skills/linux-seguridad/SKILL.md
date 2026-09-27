---
name: linux-seguridad
description: >-
  Seguridad defensiva de hosts Linux: postura, forense ligero de registros, CVEs, hardening
  sysctl/SSH, AppArmor/SELinux, auditd y fail2ban. Usar ante auditoría de seguridad del
  sistema, hardening del host o revisión de logs de auth. No usar para vulnerabilidades de
  código de aplicación (→ web-seguridad) ni limpieza de disco (→ linux-mantenimiento).
license: MIT
metadata:
  author: Soluciones-Alexendros
  version: "1.0.0"
  dominio: linux
  idioma: es

---
# Linux Seguridad — Seguridad defensiva de hosts Linux

Skill de seguridad defensiva para sistemas Linux, operada por un agente IA con seguridad estructural. Parte del dominio **linux** — seguridad defensiva de hosts Linux. Hermana de `linux-mantenimiento` (higiene, actualizaciones, ordenado, optimización). Cuando una petición toca ambos mundos, la parte defensiva es de esta skill y la de higiene de la otra.

## Qué hace / Propósito

Evaluar y mejorar la postura defensiva del sistema sin alarmismo ni escrituras no aprobadas: forense ligero de registros, vulnerabilidades/CVEs, hardening escalonado, escaneos con validación cruzada y ciclo de vida de perfiles AppArmor.

## Cuándo usarme / Triggering

- **Auditoría de seguridad**: "Auditoría de seguridad de mi servidor", "Revisa postura defensiva", "Security Posture Score"
- **Forense de logs**: "Analiza logs sospechosos", "Revisa auth.log, journald, auditd", "Actividad anómala"
- **Escaneos**: "Escanea malware/rootkits", "ClamAV, rkhunter, AIDE, Lynis", "Validación cruzada de hallazgos"
- **Vulnerabilidades/CVEs**: "Chequea CVEs", "Actualizaciones de seguridad pendientes", "Lista priorizada con severidad"
- **Hardening**: "Hardening CIS", "Endurece SSH, sysctl, firewall", "Plan P1-P4 con aprobación"
- **AppArmor**: "Ciclo vida perfiles AppArmor", "genprof, complain, soak, logprof, enforce", "Depuración denegaciones"
- **NO usar cuando**: Higiene/mantenimiento puro (→ `linux-mantenimiento`), actualizaciones paquetes, limpieza cachés, optimización recursos

## Frontera de Alcances

| **linux-seguridad** | **linux-mantenimiento** |
|----------------------|---------------------------|
| Postura defensiva (firewall, MAC, auditd, AV, integridad) | Actualizaciones de paquetes, cachés, huérfanos |
| Forense ligero: journald, auditd, auth.log, denials.log | Limpieza de logs (rotación, vacuum) |
| Vulnerabilidades y CVEs del software instalado | Aplicar las actualizaciones que los corrigen |
| Hardening (CIS, SSH, sysctl de seguridad, AppArmor) | Optimización de arranque y recursos |
| Escaneos: ClamAV, rkhunter, AIDE, debsums, Lynis | Health Score de higiene/recursos |
| Ciclo de vida de perfiles AppArmor | Snapshots y mantenimiento rutinario |

**Regla:** Cuando una petición toca ambos mundos, la parte defensiva es de esta skill y la de higiene de `linux-mantenimiento`.

## Principios Rectores (Alinenados con Constitución ALIGNUX)

1. **Read-only por defecto** — Toda evaluación se hace sin modificar el sistema. Hardening real requiere escalado explícito y aprobación.
2. **Evidencia antes que intuición** — Ningún hallazgo se reporta sin el comando y la salida que lo sustentan. Un "parece sospechoso" sin evidencia se investiga o se descarta, nunca se alarmea.
3. **Validar antes de remediar** — Los escáneres mienten con frecuencia (rkhunter y sus falsos positivos son el ejemplo clásico). Antes de proponer una acción, confirmar el hallazgo por una segunda vía.
4. **Defensa en capas, no en pánico** — MAC en vivo (AppArmor), integridad a posteriori (AIDE), auditoría de acciones (auditd), firmas (ClamAV/rkhunter). Ninguna capa sustituye a otra; el informe siempre dice qué capa cubre qué.
5. **Reversibilidad** — Toda acción de escritura documenta su vuelta atrás antes de ejecutarse.
6. **Riesgo graduado** — Se reutiliza la escala de `linux-mantenimiento`: R0 (solo lectura, libre), R1 (escritura reversible con snapshot), R2 (riesgo: SSH, firewall, kernel, AppArmor enforce; requiere aprobación), R3 (prohibido siempre).

## Modos de Operación

| Modo | Qué hace | Permisos | Salida |
|------|----------|----------|--------|
| `postura` | Inventario y salud de las defensas activas | R0 | Posture Score + hallazgos P0–P4 |
| `logs` | Forense ligero: autenticación, audit, denegaciones MAC, actividad sospechosa | R0 | Cronología + veredicto por evento |
| `scan` | Escaneos antimalware/rootkits/integridad con validación cruzada | R0/R1 | Hallazgos validados + descartados (con motivo) |
| `vulns` | CVEs y actualizaciones de seguridad pendientes | R0 | Lista priorizada con severidad y fix |
| `harden` | Plan de endurecimiento CIS priorizado; ejecución solo con aprobación | R0 plan / R2 ejecución | Plan P1–P4 + diff post-ejecución |
| `apparmor` | Ciclo de vida de perfiles: diagnóstico, genprof, complain, soak, logprof, enforce, depuración | R0 diag / R2 cambios | Estado de perfiles + acciones |

**Regla:** ningún modo escribe sin que el usuario lo pida explícitamente; `harden` y cambios en AppArmor (enforce, cargar perfiles) siempre muestran antes el plan exacto.

## Flujo Estándar

1. **Fingerprint defensivo**: `./scripts/postura_seguridad.sh` → inventario de firewall, AppArmor, auditd, AIDE, ClamAV, rkhunter, journald, SSH, sysctl críticos.
2. **Modo solicitado** según tabla; para forense seguir `references/forense-logs.md`, para escaneos `references/escaneos.md`, para AppArmor `references/apparmor-playbook.md`, para hardening `references/hardening-baseline.md`, para el inventario de defensas `references/postura-defensiva.md`.
3. **Informe**: Security Posture Score (0–100), hallazgos P0–P4 con evidencia, acciones propuestas con su nivel de riesgo y rollback.

## Formato de Salida

### Security Posture Score (0–100)
- **Control de acceso mandatorio (30%)**: AppArmor activo, perfiles en enforce, userns restringido, procesos sin confinar.
- **Detección y auditoría (25%)**: auditd con reglas, journald persistente, AIDE programado, denegaciones cosechadas.
- **Superficie de ataque (25%)**: firewall, SSH, servicios expuestos, binarios inesperados con privilegios.
- **Higiene de parches de seguridad (20%)**: CVEs críticos sin parchear, actualizaciones de seguridad pendientes.

### Clasificación de Hallazgos
Igual que en `linux-mantenimiento`: **P0** compromiso activo/inminente · **P1** vulnerabilidad o configuración insegura real · **P2** desviación de baseline · **P3** mejora de defensa · **P4** informativo.

## Referencias Internas

- `references/postura-defensiva.md` — Qué defensas inventariar y cómo leer su estado.
- `references/forense-logs.md` — Cookbook de journalctl, ausearch, auth.log y denials.log.
- `references/escaneos.md` — Uso correcto de ClamAV, rkhunter, AIDE, debsums y Lynis, con sus trampas.
- `references/apparmor-playbook.md` — Lecciones duras del trabajo real con AppArmor en Ubuntu 26.04. **Leer antes de tocar cualquier perfil.**
- `references/hardening-baseline.md` — Controles CIS aplicables a escritorio/workstation Ubuntu.

## Herramientas

| Script | Propósito | Modo |
|--------|-----------|------|
| `postura_seguridad.sh` | Fingerprint read-only de defensas activas (firewall, AppArmor, auditd, AIDE, AV, SSH, lockdown/IMA/landlock/TPM2/syft; `--json`) | postura (y pre-flight de todos) |
| `scan_orchestrator.py` | Orquesta ClamAV/rkhunter/AIDE/debsums/Lynis con validación cruzada (solo lectura) | scan |
| `vulns_check.py` | Chequeo apt + snap/flatpak, degradado sin red (solo lectura) | vulns |
| `harden_plan.py` | Plan P1–P4 + diff + rollback desde el baseline canónico (solo lectura) | harden |
| `apparmor_lifecycle.py` | Ciclo genprof→complain→soak→logprof→enforce (dry-run por defecto) | apparmor |
| `forense_collector.py` | Recetas de forense-logs.md a cronología JSON (solo lectura) | logs |

## Interacción

Al invocarse, el agente ejecuta el fingerprint, muestra el contexto detectado (defensas activas, denegaciones recientes, alertas pendientes) y pregunta el objetivo si no está claro. Para `logs` y `scan`, siempre ofrece primero el resumen ejecutivo y después el detalle forense.

## Limitaciones Declaradas

- Forense **ligero**: no sustituye a una respuesta a incidentes completa (memoria, timeline de disco, IOCs).
- Sin acceso a red no consulta bases CVE en vivo; degrada a análisis de paquetes pendientes locales.
- Los perfiles AppArmor de aplicaciones complejas (navegadores, Electron) exigen ciclo complain→soak→logprof→enforce de días; la skill lo planifica pero no lo falsea en una sesión.

---

## Trazabilidad ALIGNUX

Esta skill implementa los principios de `alignux-constitucion`:
- **Identidad**: Prefijo `ALIGNUX.` en mayúsculas (identidad constitucional)
- **Coherencia**: Frontera clara con `linux-mantenimiento`, nomenclatura `dominio.subdominio`
- **Estructura habilita**: Tags `sistema.ALIGNUX.*`, progressive disclosure, validador automatizado
- **Documentación viva**: validador como verdad ejecutable (tools/validate/skill_spec.py (validador del repo))
- **Aprendizaje = despliegue**: Síntesis de ~4 décadas experiencia Linux/seguridad en skill operativa
- **No límites coyunturales**: Diseño para siguiente paradigma (agentes, IA, edge)
- **Herramientas amplifican**: `postura_seguridad.sh` inventaria, humano decide

## Checks de host (absorbido de linux-security)

Ver `references/linux-security-source.md` para MAC (AppArmor/SELinux), sysctl, SSH, auditd y fail2ban. Solo lectura salvo que el operador pida remediación.

## Uso

Seguridad defensiva del host: invocar ante auditoría de seguridad, hardening, revisión de logs, escaneos, CVEs o ciclo AppArmor. No usar para higiene ni vulnerabilidades de código de aplicación (ver `description` del frontmatter).

## Estructura

- `SKILL.md` — modos, flujo, Posture Score y límites.
- `references/` — postura-defensiva, forense-logs, escaneos, apparmor-playbook, hardening-baseline (canónico) y linux-security-source (fuente absorbida).
- `scripts/` — `postura_seguridad.sh`, `scan_orchestrator.py`, `vulns_check.py`, `harden_plan.py`, `apparmor_lifecycle.py`, `forense_collector.py`, `test_postura.py` y `tests/`.

## Referencias

- Internas: ver «Referencias Internas» más arriba.
- Herramientas: ver «Herramientas» más arriba (tabla script→propósito y modo).
- Canon del repo: docs/STANDARD.md y validador tools/validate/skill_spec.py.
