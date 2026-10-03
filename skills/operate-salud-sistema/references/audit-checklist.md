# audit-checklist.md

Checklist de auditoría mapeado a controles CIS Benchmarks / Lynis / DISA STIGs. Cada control tiene: ID, descripción, criticidad (P0–P4), comando de verificación, y modo de auditoría donde se ejecuta.

---

## Estructura de criticidad

| Nivel  | Etiqueta CIS/STIG | Significado                                                              | SLA remediación  |
| ------ | ----------------- | ------------------------------------------------------------------------ | ---------------- |
| **P0** | Cat I / Critical  | Compromiso activo o inminente, superficie de ataque crítica expuesta     | Inmediato (< 4h) |
| **P1** | Cat II / High     | Vulnerabilidad conocida, configuración insegura, parche faltante crítico | < 24h            |
| **P2** | Cat III / Medium  | Desviación de baseline, deuda técnica, hardening incompleto              | < 7 días         |
| **P3** | Info / Low        | Optimización, limpieza, mejoras de higiene                               | Próxima ventana  |
| **P4** | Info              | Observación, tendencia, informativo                                      | Seguimiento      |

---

## 1. Gestión de parches y actualizaciones (CIS 1.x, 3.x)

| ID     | Control                                                         | Criticidad | Verificación                                                                                   | Modo        |
| ------ | --------------------------------------------------------------- | ---------- | ---------------------------------------------------------------------------------------------- | ----------- |
| PKG-01 | Paquetes con actualizaciones de seguridad pendientes            | P1         | `checkupdates` / `apt list --upgradable` / `dnf check-update`                                  | quick, full |
| PKG-02 | Noticias de la distro leídas antes de actualizar (Arch)         | P2         | Verificar `~/.config/pacman/news-read` o equivalente                                           | full        |
| PKG-03 | Kernel running != kernel installed (reboot pendiente)           | P1         | `uname -r` vs `pacman -Q linux` / `dpkg -l linux-image-*`                                      | quick, full |
| PKG-04 | Firmware actualizable (fwupd)                                   | P2         | `fwupdmgr get-updates`                                                                         | full        |
| PKG-05 | Paquetes huérfanos (sin dependientes)                           | P3         | `pacman -Qtdq` / `apt autoremove --dry-run` / `dnf repoquery --unneeded`                       | quick, full |
| PKG-06 | Paquetes foráneos (AUR, manuales, third-party)                  | P3         | `pacman -Qmq` / `apt list --manual-installed` / `dnf list installed`                           | full        |
| PKG-07 | Archivos .pacnew/.pacsave/.rpmnew pendientes                    | P2         | `find /etc -name "*.pacnew" -o -name "*.pacsave" -o -name "*.rpmnew"`                          | quick, full |
| PKG-08 | Rebuild-detector: paquetes rotos por actualización de librerías | P1         | `rebuild-detector` (Arch) / `apt-get check` / `rpm -Va`                                        | full        |
| PKG-09 | Tamaño de caché de paquetes                                     | P4         | `du -sh /var/cache/pacman/pkg` / `/var/cache/apt` / `/var/cache/dnf`                           | quick, full |
| PKG-10 | Mirrorlist / repositorios actualizados y accesibles             | P3         | `reflector --latest 20 --protocol https --sort rate --save /etc/pacman.d/mirrorlist` (dry-run) | full        |

---

## 2. Configuración de acceso y autenticación (CIS 5.x, 6.x)

| ID     | Control                                                   | Criticidad | Verificación                                             | Modo                         |
| ------ | --------------------------------------------------------- | ---------- | -------------------------------------------------------- | ---------------------------- |
| ACC-01 | SSH: PermitRootLogin no                                   | P0         | `sshd -T                                                 | grep permitrootlogin`        | quick, full   |
| ACC-02 | SSH: PasswordAuthentication no (solo claves)              | P0         | `sshd -T                                                 | grep passwordauthentication` | quick, full   |
| ACC-03 | SSH: PermitEmptyPasswords no                              | P0         | `sshd -T                                                 | grep permitemptypasswords`   | full          |
| ACC-04 | SSH: MaxAuthTries ≤ 4                                     | P1         | `sshd -T                                                 | grep maxauthtries`           | full          |
| ACC-05 | SSH: ClientAliveInterval/CountMax configurados            | P2         | `sshd -T                                                 | grep clientalive`            | full          |
| ACC-06 | SSH: AllowUsers/AllowGroups restrictivo                   | P2         | `sshd -T                                                 | grep -E 'allowusers          | allowgroups'` | full                   |
| ACC-07 | SSH: Puerto no estándar (≠ 22)                            | P3         | `sshd -T                                                 | grep ^port`                  | full          |
| ACC-08 | Usuarios con UID 0 (solo root)                            | P0         | `awk -F: '$3==0' /etc/passwd`                            | quick, full                  |
| ACC-09 | Cuentas sin contraseña / contraseña vacía                 | P0         | `awk -F: '$2==""' /etc/shadow`                           | full                         |
| ACC-10 | Contraseñas con expiración / envejecimiento               | P2         | `chage -l <user>` para usuarios críticos                 | full                         |
| ACC-11 | Sudoers: sin NOPASSWD para usuarios no administrativos    | P1         | `grep -r NOPASSWD /etc/sudoers /etc/sudoers.d/`          | full                         |
| ACC-12 | Sudoers: lecture_file, log_input, log_output, use_pty     | P2         | `grep -E 'lecture                                        | log_input                    | log_output    | use_pty' /etc/sudoers` | full |
| ACC-13 | Polkit: reglas restrictivas para acciones administrativas | P2         | `ls /etc/polkit-1/rules.d/ /usr/share/polkit-1/rules.d/` | full                         |

---

## 3. Firewall y superficie de red (CIS 3.x, 4.x)

| ID     | Control                                             | Criticidad | Verificación                                                | Modo                                |
| ------ | --------------------------------------------------- | ---------- | ----------------------------------------------------------- | ----------------------------------- |
| NET-01 | Firewall activo (ufw/nftables/iptables/firewalld)   | P0         | `systemctl is-active ufw/nftables/iptables/firewalld`       | quick, full                         |
| NET-02 | Política por defecto: deny incoming, allow outgoing | P1         | `nft list ruleset` / `iptables-save` / `ufw status verbose` | full                                |
| NET-03 | Puertos abiertos solo los necesarios (lista blanca) | P1         | `ss -tuln` vs lista permitida en perfil                     | quick, full                         |
| NET-04 | SSH expuesto a Internet (interfaz pública)          | P0         | `ss -tuln                                                   | grep :22` + comprobación IP pública | quick, full |
| NET-05 | Servicios escuchando en 0.0.0.0 innecesarios        | P2         | `ss -tuln                                                   | grep 0.0.0.0` + análisis            | full        |
| NET-06 | IPv6 deshabilitado si no se usa                     | P3         | `sysctl net.ipv6.conf.all.disable_ipv6`                     | full                                |
| NET-07 | ICMP rate limiting / hardening                      | P3         | `sysctl net.ipv4.icmp_*`                                    | full                                |
| NET-08 | SYN cookies, TCP hardening                          | P2         | `sysctl net.ipv4.tcp_syncookies` etc.                       | full                                |

---

## 4. Sistema de archivos y permisos (CIS 1.x, 6.x)

| ID    | Control                                                | Criticidad | Verificación                                                                                       | Modo        |
| ----- | ------------------------------------------------------ | ---------- | -------------------------------------------------------------------------------------------------- | ----------- |
| FS-01 | Particiones separadas para /tmp, /var, /home, /var/log | P2         | `findmnt -T /tmp /var /home /var/log`                                                              | full        |
| FS-02 | /tmp con noexec, nosuid, nodev                         | P1         | `findmnt -T /tmp -o OPTIONS`                                                                       | full        |
| FS-03 | /var/tmp con noexec, nosuid, nodev                     | P2         | `findmnt -T /var/tmp -o OPTIONS`                                                                   | full        |
| FS-04 | /home con nosuid, nodev                                | P2         | `findmnt -T /home -o OPTIONS`                                                                      | full        |
| FS-05 | Archivos world-writable (excluyendo /tmp, /var/tmp)    | P1         | `find / -xdev -type f -perm -0002 ! -path "/tmp/*" ! -path "/var/tmp/*" 2>/dev/null`               | full        |
| FS-06 | Directorios world-writable sin sticky bit              | P1         | `find / -xdev -type d -perm -0002 ! -perm -1000 ! -path "/tmp/*" ! -path "/var/tmp/*" 2>/dev/null` | full        |
| FS-07 | Archivos sin dueño (no user/group)                     | P2         | `find / -xdev \( -nouser -o -nogroup \) ! -path "/proc/*" ! -path "/sys/*" 2>/dev/null`            | full        |
| FS-08 | Archivos SUID/SGID no documentados                     | P1         | `find / -xdev -type f \( -perm -4000 -o -perm -2000 \) 2>/dev/null` vs baseline                    | full        |
| FS-09 | Symlinks rotos en /etc, /usr, /boot                    | P3         | `find /etc /usr /boot -xtype l 2>/dev/null`                                                        | quick, full |
| FS-10 | Uso de disco > 80% en particiones críticas             | P1         | `df -h / /boot /var /home`                                                                         | quick, full |
| FS-11 | Inodos agotados > 80%                                  | P2         | `df -i / /boot /var /home`                                                                         | full        |

---

## 5. Logging y auditoría (CIS 4.x, NIST 800-92)

| ID     | Control                                                               | Criticidad | Verificación                                           | Modo              |
| ------ | --------------------------------------------------------------------- | ---------- | ------------------------------------------------------ | ----------------- |
| LOG-01 | systemd-journald: Storage=persistent                                  | P1         | `grep ^Storage /etc/systemd/journald.conf`             | full              |
| LOG-02 | systemd-journald: SystemMaxUse ≤ 10% disco /var                       | P2         | `grep SystemMaxUse /etc/systemd/journald.conf`         | full              |
| LOG-03 | auditd activo y configurado (CIS 4.1.x)                               | P1         | `systemctl is-active auditd` + `auditctl -l`           | full              |
| LOG-04 | Reglas auditd: cambios de identidad, sudo, acceso a archivos críticos | P2         | `auditctl -l                                           | grep -E 'identity | sudo | passwd | shadow | ssh | sudoers'` | full |
| LOG-05 | Logrotate configurado para logs críticos                              | P3         | `ls /etc/logrotate.d/` + verificación contenido        | full              |
| LOG-06 | Journal: errores de prioridad 0-3 en últimas 24h                      | P2         | `journalctl -p 0..3 --since "24 hours ago" --no-pager` | quick, full       |
| LOG-07 | Coredumps: systemd-coredump configurado / deshabilitado               | P2         | `sysctl kernel.core_pattern` + `coredumpctl list`      | full              |
| LOG-08 | Fallos de arranque (systemd)                                          | P2         | `systemctl --failed`                                   | quick, full       |

---

## 6. Hardening del kernel y runtime (CIS 1.x, 3.x)

| ID     | Control                                                                        | Criticidad | Verificación                              | Modo |
| ------ | ------------------------------------------------------------------------------ | ---------- | ----------------------------------------- | ---- |
| KER-01 | ASLR activado (kernel.randomize_va_space = 2)                                  | P1         | `sysctl kernel.randomize_va_space`        | full |
| KER-02 | Restricción dmesg (kernel.dmesg_restrict = 1)                                  | P2         | `sysctl kernel.dmesg_restrict`            | full |
| KER-03 | Restricción kptr (kernel.kptr_restrict = 2)                                    | P2         | `sysctl kernel.kptr_restrict`             | full |
| KER-04 | Perf events restrictivo (kernel.perf_event_paranoid = 3)                       | P2         | `sysctl kernel.perf_event_paranoid`       | full |
| KER-05 | SysRq deshabilitado (kernel.sysrq = 0)                                         | P3         | `sysctl kernel.sysrq`                     | full |
| KER-06 | Módulos kernel: carga restringida (modules_disabled=1 tras arranque)           | P2         | `sysctl kernel.modules_disabled`          | full |
| KER-07 | BPF hardening (kernel.unprivileged_bpf_disabled = 1)                           | P2         | `sysctl kernel.unprivileged_bpf_disabled` | full |
| KER-08 | User namespaces restrictivos (user.max_user_namespaces = 0 si no contenedores) | P3         | `sysctl user.max_user_namespaces`         | full |

---

## 7. Servicios y demonios (CIS 2.x)

| ID     | Control                                                                               | Criticidad | Verificación                                                                        | Modo        |
| ------ | ------------------------------------------------------------------------------------- | ---------- | ----------------------------------------------------------------------------------- | ----------- |
| SRV-01 | Servicios innecesarios deshabilitados (cups, avahi, bluetooth si no se usan)          | P2         | `systemctl list-unit-files --state=enabled` vs lista permitida                      | full        |
| SRV-02 | Servicios fallidos                                                                    | P1         | `systemctl --failed`                                                                | quick, full |
| SRV-03 | Timers systemd: limpieza, snapshots, actualizaciones programadas                      | P3         | `systemctl list-timers --all`                                                       | full        |
| SRV-04 | Servicios escuchando en puertos (ver NET-03/05)                                       | P1         | `ss -tulnp`                                                                         | quick, full |
| SRV-05 | systemd: ProtectSystem, ProtectHome, PrivateTmp, NoNewPrivileges en unidades críticas | P2         | `systemctl show <servicio> -p ProtectSystem,ProtectHome,PrivateTmp,NoNewPrivileges` | full        |

---

## 8. Criptografía y certificados (CIS 5.x)

| ID     | Control                                                           | Criticidad | Verificación                                       | Modo |
| ------ | ----------------------------------------------------------------- | ---------- | -------------------------------------------------- | ---- |
| CRY-01 | SSH host keys: algoritmos modernos (ed25519, rsa-sha2-512)        | P1         | `ssh-keygen -lf /etc/ssh/ssh_host_*_key.pub`       | full |
| CRY-02 | Certificados TLS: expiración < 30 días                            | P1         | `openssl x509 -in <cert> -noout -checkend 2592000` | full |
| CRY-03 | OpenSSL: no SSLv2/v3, TLS 1.0/1.1 deshabilitados                  | P1         | `openssl ciphers -v` + config de servicios         | full |
| CRY-04 | LUKS: particiones cifradas con PBKDF2/Argon2, key slots auditados | P2         | `cryptsetup luksDump /dev/...`                     | full |

---

## 9. Específico Arch / EndeavourOS / CachyOS

| ID     | Control                                                         | Criticidad | Verificación                                                      | Modo                                               |
| ------ | --------------------------------------------------------------- | ---------- | ----------------------------------------------------------------- | -------------------------------------------------- |
| ARC-01 | `pacman -Qk`: archivos modificados en paquetes instalados       | P2         | `pacman -Qk 2>&1                                                  | grep -v "0 altered files"`                         | full |
| ARC-02 | `pacman -Qm`: paquetes AUR/foráneos sin actualización > 90 días | P3         | `pacman -Qm --format "%n %v %l\n"                                 | awk '$3 < "'$(date -d "90 days ago" +%Y-%m-%d)'"'` | full |
| ARC-03 | `pacdiff` / `.pacnew` pendientes en /etc                        | P2         | `pacdiff --output`                                                | quick, full                                        |
| ARC-04 | Mirrorlist: reflectores actualizados, HTTPS, sin mirrors rotos  | P3         | `reflector --latest 20 --protocol https --sort rate --dry-run`    | full                                               |
| ARC-05 | `mkinitcpio`: hooks correctos, preset actualizado               | P2         | `mkinitcpio -P` (dry-run)                                         | full                                               |
| ARC-06 | Bootloader: systemd-boot / GRUB configurado, entries válidas    | P1         | `bootctl list` / `grub-editenv list`                              | full                                               |
| ARC-07 | `pacman -Sy` sin `-u` (actualización parcial) detectada         | P1         | Verificar log de pacman: `grep "pacman -Sy$" /var/log/pacman.log` | full                                               |

---

## 10. Específico Debian / Ubuntu

| ID     | Control                                                            | Criticidad | Verificación                                                                            | Modo              |
| ------ | ------------------------------------------------------------------ | ---------- | --------------------------------------------------------------------------------------- | ----------------- |
| DEB-01 | `apt list --upgradable` con actualizaciones de seguridad           | P1         | `apt list --upgradable 2>/dev/null                                                      | grep -i security` | quick, full |
| DEB-02 | `apt-get check`: dependencias rotas                                | P1         | `apt-get check`                                                                         | full              |
| DEB-03 | `debsums -c`: archivos modificados vs paquetes                     | P2         | `debsums -c 2>/dev/null`                                                                | full              |
| DEB-04 | Unattended-upgrades configurado y activo                           | P2         | `systemctl is-active unattended-upgrades` + `/etc/apt/apt.conf.d/50unattended-upgrades` | full              |
| DEB-05 | `needrestart`: servicios que requieren reinicio tras actualización | P2         | `needrestart -r l`                                                                      | full              |

---

## 11. Específico RHEL / Fedora / CentOS / AlmaLinux / Rocky

| ID      | Control                                                           | Criticidad | Verificación                                               | Modo                    |
| ------- | ----------------------------------------------------------------- | ---------- | ---------------------------------------------------------- | ----------------------- |
| RHEL-01 | `dnf check-update` con actualizaciones de seguridad               | P1         | `dnf check-update --security`                              | quick, full             |
| RHEL-02 | `rpm -Va`: verificación de integridad RPM                         | P2         | `rpm -Va 2>/dev/null                                       | grep -v "^....... c /"` | full |
| RHEL-03 | SELinux: Enforcing mode                                           | P0         | `getenforce`                                               | quick, full             |
| RHEL-04 | SELinux: booleans seguros, sin políticas personalizadas inseguras | P2         | `semanage boolean -l` + `semodule -l`                      | full                    |
| RHEL-05 | `dnf needs-restarting`: kernel/userspace reboot pendiente         | P1         | `needs-restarting -r` / `needs-restarting`                 | full                    |
| RHEL-06 | `firewalld` / `nftables` activo y zona correcta                   | P0         | `firewall-cmd --state` + `firewall-cmd --get-active-zones` | quick, full             |

---

## Métricas de cobertura

| Métrica              | Definición                                                 | Meta     |
| -------------------- | ---------------------------------------------------------- | -------- |
| **Cobertura quick**  | % de controles P0+P1 ejecutados en `audit-quick`           | ≥ 90%    |
| **Cobertura full**   | % de todos los controles ejecutados en `audit-full`        | ≥ 95%    |
| **Falsos positivos** | Controles que alertan sin hallazgo real tras investigación | < 5%     |
| **Tiempo quick**     | Duración total `audit-quick`                               | < 5 min  |
| **Tiempo full**      | Duración total `audit-full`                                | < 30 min |

---

## Uso en la skill

- `audit_quick.py` ejecuta controles marcados con modo `quick`
- `audit_full.py` ejecuta **todos** los controles
- Cada control produce: `PASS`, `FAIL`, `WARN`, `SKIP` (con razón), `ERROR` (falla de verificación)
- Salida JSON estructurada para `report_render.py`
