# Hardening baseline — escritorio/workstation Ubuntu

Controles aplicables a una máquina personal de desarrollo (no servidor). Cada control lleva su nivel de riesgo de aplicación (R1 reversible / R2 requiere aprobación).

## 1. Kernel y MAC

| Control | Verificación | Nivel |
|---|---|---|
| AppArmor activo y servicio enabled | `/sys/module/apparmor/parameters/enabled` | — |
| userns no privilegiados restringidos | `sysctl kernel.apparmor_restrict_unprivileged_userns` = 1; NUNCA bajar a 0 como atajo — perfiles por herramienta | R2 |
| sysctl de red endurecidos | `net.ipv4.conf.all.rp_filter`, `accept_redirects=0`, `send_redirects=0`, `tcp_syncookies=1` | R1 |
| kptr_restrict, dmesg_restrict | `kernel.kptr_restrict=2`, `kernel.dmesg_restrict=1` | R1 |

## 2. Autenticación y acceso

| Control | Verificación | Nivel |
|---|---|---|
| SSH: PermitRootLogin no, MaxAuthTries ≤ 4 | `sshd -T` | R2 (toca acceso remoto: planificar) |
| sudo con timestamp, sin NOPASSWD amplio | `grep -r NOPASSWD /etc/sudoers*` | R1 |
| Drop-ins sudo temporales: siempre con fecha de caducidad mental y eliminación al terminar la tarea | `ls /etc/sudoers.d/` | — |
| Umask 027 en cuentas con secretos | `/etc/login.defs`, `~/.profile` | R1 |

## 3. Auditoría y detección

| Control | Verificación | Nivel |
|---|---|---|
| auditd activo con reglas de identidad | `auditctl -l` (-w passwd/shadow/sudoers) | R1 |
| journald persistente | `/var/log/journal` existe | R1 |
| AIDE programado (timer) + DB regenerada tras cambios voluntarios | `systemctl list-timers` | R1 |
| Recolector de denegaciones MAC persistente | `/var/log/apparmor/denials.log` | R1 |
| Canal de alertas en escritorio | unidad user `apparmor-notify` | R1 |

## 4. Superficie de ataque

| Control | Verificación | Nivel |
|---|---|---|
| Firewall deny incoming por defecto | `ufw status` | R2 |
| Solo servicios necesarios escuchando | `ss -tulpn` revisado | R2 |
| Binarios con secretos en tierra de root (canon root-owned) | `ls -la ~/Terminal` | R1 |
| Navegadores y agentes IA con perfil MAC propio | `aa-status` | R2 (ciclo de días) |

## 5. Lo que NO se endurece en un escritorio developer

- No confinar intérpretes globales (node, python3), shells interactivos, compiladores ni git: el coste rompe el trabajo diario y el beneficio es mínimo frente a confinar servicios y agentes.
- No desactivar servicios del escritorio por paranoia de checklist: cada desactivación necesita su razón de amenaza.
- No auditd forense exhaustivo (todas las syscalls): el ruido entierra la señal; reglas de vigilancia sobre rutas sensibles bastan.

## Procedimiento de aplicación

1. Presentar plan numerado con: control, estado actual, cambio exacto, nivel R, rollback.
2. Aplicar solo lo aprobado; después de cada cambio R2, verificación funcional inmediata (login, red, app afectada).
3. Registrar en log de sesión y dejar constancia de qué quedó fuera y por qué.
