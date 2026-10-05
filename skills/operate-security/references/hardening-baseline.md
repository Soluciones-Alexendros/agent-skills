# hardening-baseline.md — BASELINE CANÓNICO (operate-security)

Baseline canónico de hardening según CIS Benchmarks, DISA STIGs y guías de
SUSE/Red Hat/Arch. Cubre **servidor completo** (§1–§10, importado del baseline
histórico de mantenimiento) más **controles de escritorio/workstation Ubuntu**
(§12). Cada control lleva: ID, descripción, criticidad, verificación y
remediación, más su **nivel de riesgo de aplicación R1/R2** y **rollback** (§11).

Niveles CIS: **Nivel 1** básico (servidores expuestos), **Nivel 2** estándar
(producción/compliance), **Nivel 3** alto (entornos regulados). Ver §10.

> Reparto entre skills: este fichero es el baseline activo. La skill hermana
> `operate-maintenance` solo conserva un stub que referencia aquí más su
> subconjunto de higiene (`skills/operate-maintenance/references/hardening-baseline.md`).
> `audit_full.py`/`audit_quick.py` de mantenimiento **NO** verifican SSH/KR/FS-05–08/AU/UA/CR
> (hardening puro: vive aquí); solo PKG-\*, FS-09/10/11, LOG-06/08, SRV-02, NET-04.

---

## 1. SSH Hardening (CIS 5.2, STIG V-20445x)

| ID | Control | Criticidad | Verificación | Remediación |
|----|---------|------------|--------------|-------------|
| SSH-01 | `PermitRootLogin no` | P0 | `sshd -T | grep permitrootlogin` | Editar `/etc/ssh/sshd_config`, `systemctl reload sshd` |
| SSH-02 | `PasswordAuthentication no` | P0 | `sshd -T | grep passwordauthentication` | Idem, solo claves públicas |
| SSH-03 | `PubkeyAuthentication yes` | P1 | `sshd -T | grep pubkeyauthentication` | Verificar habilitado |
| SSH-04 | `PermitEmptyPasswords no` | P0 | `sshd -T | grep permitemptypasswords` | Idem |
| SSH-05 | `MaxAuthTries 4` | P1 | `sshd -T | grep maxauthtries` | Valor ≤ 4 |
| SSH-06 | `MaxSessions 10` | P2 | `sshd -T | grep maxsessions` | Valor ≤ 10 |
| SSH-07 | `ClientAliveInterval 300` / `ClientAliveCountMax 2` | P2 | `sshd -T | grep clientalive` | Timeout 5 min, 2 intentos |
| SSH-08 | `LoginGraceTime 60` | P2 | `sshd -T | grep logingracetime` | ≤ 60 segundos |
| SSH-09 | `AllowUsers` / `AllowGroups` restrictivo | P2 | `sshd -T | grep -E 'allowusers|allowgroups'` | Lista blanca de usuarios/grupos |
| SSH-10 | `DenyUsers` / `DenyGroups` para cuentas de servicio | P3 | `sshd -T | grep -E 'denyusers|denygroups'` | Bloquear daemon, nobody, etc. |
| SSH-11 | `Protocol 2` (implícito en OpenSSH moderno) | P1 | `sshd -T | grep protocol` | Solo v2 |
| SSH-12 | `HostKey` solo algoritmos modernos | P1 | `ls /etc/ssh/ssh_host_*_key` | Ed25519, RSA-SHA2-512/256; eliminar DSA, ECDSA débiles |
| SSH-13 | `KexAlgorithms`, `Ciphers`, `MACs` restrictivos | P1 | `sshd -T | grep -E 'kexalgorithms|ciphers|macs'` | Ver `man sshd_config` para valores seguros |
| SSH-14 | `Banner /etc/issue.net` | P3 | `sshd -T | grep banner` | Banner legal/advertencia |
| SSH-15 | `LogLevel VERBOSE` | P2 | `sshd -T | grep loglevel` | VERBOSE o INFO |
| SSH-16 | `X11Forwarding no` (si no se usa) | P2 | `sshd -T | grep x11forwarding` | Deshabilitar |
| SSH-17 | `AllowTcpForwarding no` (si no se usa) | P2 | `sshd -T | grep allowtcpforwarding` | Deshabilitar |
| SSH-18 | `PermitTunnel no` | P3 | `sshd -T | grep permittunnel` | Deshabilitar |
| SSH-19 | `DebianBanner no` / `VersionAddendum none` | P4 | `sshd -T | grep -E 'debianbanner|versionaddendum'` | Ocultar versión |
| SSH-20 | `AuthenticationMethods publickey` (2FA opcional) | P1 | `sshd -T | grep authenticationmethods` | Requerir clave pública |

### Valores recomendados para algoritmos (OpenSSH 9.x+)
```ssh
# /etc/ssh/sshd_config
KexAlgorithms curve25519-sha256,curve25519-sha256@libssh.org,diffie-hellman-group16-sha512,diffie-hellman-group18-sha512
Ciphers chacha20-poly1305@openssh.com,aes256-gcm@openssh.com,aes128-gcm@openssh.com,aes256-ctr,aes192-ctr,aes128-ctr
MACs hmac-sha2-256-etm@openssh.com,hmac-sha2-512-etm@openssh.com,umac-128-etm@openssh.com
HostKeyAlgorithms ssh-ed25519,ssh-ed25519-cert-v01@openssh.com,rsa-sha2-512,rsa-sha2-512-cert-v01@openssh.com,rsa-sha2-256,rsa-sha2-256-cert-v01@openssh.com
PubkeyAcceptedAlgorithms ssh-ed25519,ssh-ed25519-cert-v01@openssh.com,rsa-sha2-512,rsa-sha2-512-cert-v01@openssh.com,rsa-sha2-256,rsa-sha2-256-cert-v01@openssh.com
```

---

## 2. Firewall (CIS 3.4, 3.5, STIG V-20446x)

| ID | Control | Criticidad | Verificación | Remediación |
|----|---------|------------|--------------|-------------|
| FW-01 | Firewall activo y habilitado en boot | P0 | `systemctl is-active ufw/nftables/iptables/firewalld` | `systemctl enable --now <firewall>` |
| FW-02 | Política por defecto: deny incoming | P1 | `nft list ruleset` / `iptables -L -n -v` / `ufw status verbose` | Default deny input, allow output |
| FW-03 | Reglas allow solo puertos/servicios documentados | P1 | `ss -tuln` vs lista permitida en perfil | Eliminar reglas innecesarias |
| FW-04 | SSH: rate limiting (max 3 conexiones/min/IP) | P1 | Ver reglas firewall para puerto SSH | `ufw limit ssh` / nftables rate limit |
| FW-05 | Logging de paquetes denegados | P2 | Ver reglas de log en firewall | `ufw logging on` / nftables log |
| FW-06 | IPv6: firewall configurado si IPv6 habilitado | P2 | `ip -6 route` + firewall IPv6 | `ip6tables` / `nft` familia inet6 |
| FW-07 | Establecer zona pública/restringida (firewalld) | P2 | `firewall-cmd --get-active-zones` | `firewall-cmd --set-default-zone=public` |

### Ejemplo nftables baseline (`/etc/nftables.conf`)
```nft
#!/usr/sbin/nft -f

flush ruleset

table inet filter {
    chain input {
        type filter hook input priority 0; policy drop;
        iif "lo" accept
        ct state established,related accept
        ct state invalid drop
        # ICMP esencial
        ip protocol icmp icmp type { destination-unreachable, router-advertisement, time-exceeded, parameter-problem } accept
        ip6 nexthdr icmpv6 icmpv6 type { destination-unreachable, packet-too-big, time-exceeded, parameter-problem, nd-router-advert, nd-neighbor-solicit, nd-neighbor-advert } accept
        # SSH con rate limiting
        tcp dport 22 ct state new limit rate 3/minute accept
        # Servicios permitidos (ejemplo)
        # tcp dport { 80, 443 } accept
        # Rechazar resto con tcp-reset/icmp-port-unreachable
        reject with icmp type port-unreachable
    }
    chain forward {
        type filter hook forward priority 0; policy drop;
    }
    chain output {
        type filter hook output priority 0; policy accept;
    }
}
```

---

## 3. Permisos y sistema de archivos (CIS 1.1, 6.1, 6.2)

| ID | Control | Criticidad | Verificación | Remediación |
|----|---------|------------|--------------|-------------|
| FS-01 | Particiones separadas: /tmp, /var, /home, /var/log, /var/tmp | P2 | `findmnt -T /tmp /var /home /var/log /var/tmp` | Requiere reinstalación o LVM/BTRFS |
| FS-02 | /tmp: noexec, nosuid, nodev | P1 | `findmnt -T /tmp -o OPTIONS` | Editar `/etc/fstab` o `systemd-tmpfiles` |
| FS-03 | /var/tmp: noexec, nosuid, nodev | P2 | `findmnt -T /var/tmp -o OPTIONS` | Idem |
| FS-04 | /home: nosuid, nodev | P2 | `findmnt -T /home -o OPTIONS` | Idem |
| FS-05 | /boot: noexec, nosuid, nodev (si partición separada) | P2 | `findmnt -T /boot -o OPTIONS` | Idem |
| FS-06 | No world-writable files (excl. /tmp, /var/tmp) | P1 | `find / -xdev -type f -perm -0002 ! -path "/tmp/*" ! -path "/var/tmp/*" 2>/dev/null` | `chmod o-w <archivo>` |
| FS-07 | No world-writable dirs sin sticky bit | P1 | `find / -xdev -type d -perm -0002 ! -perm -1000 ! -path "/tmp/*" ! -path "/var/tmp/*" 2>/dev/null` | `chmod +t <dir>` o `chmod o-w <dir>` |
| FS-08 | No archivos sin dueño (nouser/nogroup) | P2 | `find / -xdev \( -nouser -o -nogroup \) ! -path "/proc/*" ! -path "/sys/*" 2>/dev/null` | Asignar dueño o eliminar |
| FS-09 | SUID/SGID: solo binarios documentados | P1 | `find / -xdev -type f \( -perm -4000 -o -perm -2000 \) 2>/dev/null` vs baseline | `chmod u-s/g-s <binario>` si no necesario |
| FS-10 | Sticky bit en /tmp, /var/tmp | P1 | `stat -c '%A %n' /tmp /var/tmp` | `chmod +t /tmp /var/tmp` |
| FS-11 | /etc/fstab: noexec en particiones de datos | P2 | `grep noexec /etc/fstab` | Añadir `noexec` a /data, /home, etc. |
| FS-12 | /etc/fstab: nodev en particiones no root | P2 | `grep nodev /etc/fstab` | Añadir `nodev` |
| FS-13 | /etc/fstab: nosuid en particiones no root | P2 | `grep nosuid /etc/fstab` | Añadir `nosuid` |

---

## 4. Auditoría y logging (CIS 4.1, 4.2, 4.3, NIST 800-92)

| ID | Control | Criticidad | Verificación | Remediación |
|----|---------|------------|--------------|-------------|
| AU-01 | auditd instalado y activo | P1 | `systemctl is-active auditd` | `pacman -S audit && systemctl enable --now auditd` |
| AU-02 | Reglas auditd: cambios de identidad (user/group) | P2 | `auditctl -l | grep -E 'identity|passwd|group|shadow'` | Ver reglas abajo |
| AU-03 | Reglas auditd: uso de sudo | P2 | `auditctl -l | grep sudo` | Idem |
| AU-04 | Reglas auditd: acceso a archivos críticos (/etc/shadow, /etc/sudoers, SSH keys) | P2 | `auditctl -l | grep -E 'shadow|sudoers|ssh_host.*key'` | Idem |
| AU-05 | Reglas auditd: modificaciones de red/firewall | P2 | `auditctl -l | grep -E 'iptables|nft|firewall|network'` | Idem |
| AU-06 | Reglas auditd: carga/descarga módulos kernel | P2 | `auditctl -l | grep -E 'init_module|delete_module|finit_module'` | Idem |
| AU-07 | Reglas auditd: cambios de hora/sistema | P2 | `auditctl -l | grep -E 'adjtimex|settimeofday|clock_settime'` | Idem |
| AU-08 | auditd: max_log_file ≥ 100MB, num_logs ≥ 5 | P2 | `grep -E 'max_log_file|num_logs' /etc/audit/auditd.conf` | Editar `/etc/audit/auditd.conf` |
| AU-09 | auditd: space_left_action = email, action_mail_acct = root | P3 | `grep -E 'space_left|action_mail' /etc/audit/auditd.conf` | Idem |
| AU-10 | auditd: admin_space_left_action = halt (crítico) | P1 | `grep admin_space_left_action /etc/audit/auditd.conf` | `admin_space_left_action = halt` |
| AU-11 | systemd-journald: Storage=persistent | P1 | `grep ^Storage /etc/systemd/journald.conf` | `Storage=persistent` |
| AU-12 | systemd-journald: SystemMaxUse ≤ 10% disco /var | P2 | `grep SystemMaxUse /etc/systemd/journald.conf` | `SystemMaxUse=500M` (ajustar) |
| AU-13 | systemd-journald: ForwardToSyslog=no (si no se usa syslog) | P3 | `grep ForwardToSyslog /etc/systemd/journald.conf` | `ForwardToSyslog=no` |
| AU-14 | Logrotate: configurado para /var/log/* crítico | P3 | `ls /etc/logrotate.d/` | Crear configs en `/etc/logrotate.d/` |
| AU-15 | Coredumps: systemd-coredump configurado o deshabilitado | P2 | `sysctl kernel.core_pattern` + `coredumpctl list` | `kernel.core_pattern=|/usr/lib/systemd/systemd-coredump %P %u %g %s %t %c %e` o `kernel.core_pattern=/dev/null` |

### Reglas auditd recomendadas (`/etc/audit/rules.d/hardening.rules`)
```bash
# Eliminar reglas previas
-D

# Buffer size
-b 8192

# Fallo: panic (kernel panic) o halt
-f 1

# Cambios de identidad
-w /etc/passwd -p wa -k identity
-w /etc/group -p wa -k identity
-w /etc/shadow -p wa -k identity
-w /etc/gshadow -p wa -k identity
-w /etc/security/opasswd -p wa -k identity

# Sudo
-w /etc/sudoers -p wa -k sudo
-w /etc/sudoers.d/ -p wa -k sudo

# SSH
-w /etc/ssh/sshd_config -p wa -k sshd
-w /etc/ssh/ssh_host_*_key -p wa -k sshd

# Firewall/red
-w /etc/nftables.conf -p wa -k network
-w /etc/iptables/ -p wa -k network
-w /etc/firewalld/ -p wa -k network
-w /etc/NetworkManager/ -p wa -k network

# Módulos kernel
-a always,exit -F arch=b64 -S init_module,delete_module,finit_module -k modules
-a always,exit -F arch=b32 -S init_module,delete_module,finit_module -k modules

# Tiempo
-a always,exit -F arch=b64 -S adjtimex,settimeofday,clock_settime -k time
-a always,exit -F arch=b32 -S adjtimex,settimeofday,clock_settime -k time

# Permisos y atributos
-a always,exit -F arch=b64 -S chmod,fchmod,chown,fchown,lchown,fchownat -F auid>=1000 -F auid!=4294967295 -k perm_mod
-a always,exit -F arch=b32 -S chmod,fchmod,chown,fchown,lchown,fchownat -F auid>=1000 -F auid!=4294967295 -k perm_mod

# Extended attributes
-a always,exit -F arch=b64 -S setxattr,lsetxattr,fsetxattr,removexattr,lremovexattr,fremovexattr -F auid>=1000 -F auid!=4294967295 -k xattr
-a always,exit -F arch=b32 -S setxattr,lsetxattr,fsetxattr,removexattr,lremovexattr,fremovexattr -F auid>=1000 -F auid!=4294967295 -k xattr

# Montajes
-a always,exit -F arch=b64 -S mount,umount2 -F auid>=1000 -F auid!=4294967295 -k mounts
-a always,exit -F arch=b32 -S mount,umount2 -F auid>=1000 -F auid!=4294967295 -k mounts

# Hacer inmutable la configuración (requiere reboot para cambiar)
-e 2
```

---

## 5. Hardening del kernel (sysctl) (CIS 3.1, 3.2, 3.3)

| ID | Control | Criticidad | Verificación | Valor recomendado |
|----|---------|------------|--------------|-------------------|
| KR-01 | `kernel.randomize_va_space` | P1 | `sysctl kernel.randomize_va_space` | `2` (full ASLR) |
| KR-02 | `kernel.dmesg_restrict` | P2 | `sysctl kernel.dmesg_restrict` | `1` |
| KR-03 | `kernel.kptr_restrict` | P2 | `sysctl kernel.kptr_restrict` | `2` (ocultar punteros a no-root) |
| KR-04 | `kernel.perf_event_paranoid` | P2 | `sysctl kernel.perf_event_paranoid` | `3` (solo root) |
| KR-05 | `kernel.sysrq` | P3 | `sysctl kernel.sysrq` | `0` (deshabilitado) |
| KR-06 | `kernel.modules_disabled` | P3 (Nivel 3, servidores) | `sysctl kernel.modules_disabled` | Solo Nivel 3: `1` (rompe NVIDIA DKMS/desktop, ver nota) |
| KR-07 | `kernel.unprivileged_bpf_disabled` | P2 | `sysctl kernel.unprivileged_bpf_disabled` | `1` |
| KR-08 | `kernel.yama.ptrace_scope` | P2 | `sysctl kernel.yama.ptrace_scope` | `1` (solo parent) o `2` (solo root) |
| KR-09 | `net.ipv4.ip_forward` | P1 | `sysctl net.ipv4.ip_forward` | `0` (si no router) |
| KR-10 | `net.ipv4.conf.all.send_redirects` | P2 | `sysctl net.ipv4.conf.all.send_redirects` | `0` |
| KR-11 | `net.ipv4.conf.default.send_redirects` | P2 | `sysctl net.ipv4.conf.default.send_redirects` | `0` |
| KR-12 | `net.ipv4.conf.all.accept_redirects` | P1 | `sysctl net.ipv4.conf.all.accept_redirects` | `0` |
| KR-13 | `net.ipv4.conf.default.accept_redirects` | P1 | `sysctl net.ipv4.conf.default.accept_redirects` | `0` |
| KR-14 | `net.ipv4.conf.all.secure_redirects` | P2 | `sysctl net.ipv4.conf.all.secure_redirects` | `0` |
| KR-15 | `net.ipv4.conf.default.secure_redirects` | P2 | `sysctl net.ipv4.conf.default.secure_redirects` | `0` |
| KR-16 | `net.ipv4.conf.all.accept_source_route` | P1 | `sysctl net.ipv4.conf.all.accept_source_route` | `0` |
| KR-17 | `net.ipv4.conf.default.accept_source_route` | P1 | `sysctl net.ipv4.conf.default.accept_source_route` | `0` |
| KR-18 | `net.ipv4.conf.all.log_martians` | P2 | `sysctl net.ipv4.conf.all.log_martians` | `1` |
| KR-19 | `net.ipv4.conf.default.log_martians` | P2 | `sysctl net.ipv4.conf.default.log_martians` | `1` |
| KR-20 | `net.ipv4.icmp_echo_ignore_broadcasts` | P2 | `sysctl net.ipv4.icmp_echo_ignore_broadcasts` | `1` |
| KR-21 | `net.ipv4.icmp_ignore_bogus_error_responses` | P2 | `sysctl net.ipv4.icmp_ignore_bogus_error_responses` | `1` |
| KR-22 | `net.ipv4.tcp_syncookies` | P1 | `sysctl net.ipv4.tcp_syncookies` | `1` |
| KR-23 | `net.ipv4.tcp_max_syn_backlog` | P3 | `sysctl net.ipv4.tcp_max_syn_backlog` | `4096` o más |
| KR-24 | `net.ipv4.tcp_synack_retries` | P3 | `sysctl net.ipv4.tcp_synack_retries` | `2` |
| KR-25 | `net.ipv6.conf.all.disable_ipv6` | P3 | `sysctl net.ipv6.conf.all.disable_ipv6` | `1` (si no se usa IPv6) |
| KR-26 | `net.ipv6.conf.default.disable_ipv6` | P3 | `sysctl net.ipv6.conf.default.disable_ipv6` | `1` (si no se usa IPv6) |
| KR-27 | `fs.suid_dumpable` | P1 | `sysctl fs.suid_dumpable` | `0` (deshabilitar core dumps SUID) |
| KR-28 | `fs.protected_hardlinks` | P1 | `sysctl fs.protected_hardlinks` | `1` |
| KR-29 | `fs.protected_symlinks` | P1 | `sysctl fs.protected_symlinks` | `1` |
| KR-30 | `vm.mmap_min_addr` | P2 | `sysctl vm.mmap_min_addr` | `65536` |

### Archivo sysctl baseline (`/etc/sysctl.d/99-hardening.conf`)
```ini
# Kernel hardening
# NOTA KR-06: `kernel.modules_disabled=1` destruye NVIDIA DKMS, Docker/Podman con
# nvidia-container-runtime, VirtualBox/KVM y firmware-as-module en desktops.
# SOLO aplicar en servidores hardened Nivel 3 sin drivers propietarios.
# Precondición de verificación: solo verificar KR-06 si no hay nvidia-dkms ni docker.
kernel.randomize_va_space = 2
kernel.dmesg_restrict = 1
kernel.kptr_restrict = 2
kernel.perf_event_paranoid = 3
kernel.sysrq = 0
kernel.unprivileged_bpf_disabled = 1
kernel.yama.ptrace_scope = 1

# Network hardening (IPv4)
net.ipv4.ip_forward = 0
net.ipv4.conf.all.send_redirects = 0
net.ipv4.conf.default.send_redirects = 0
net.ipv4.conf.all.accept_redirects = 0
net.ipv4.conf.default.accept_redirects = 0
net.ipv4.conf.all.secure_redirects = 0
net.ipv4.conf.default.secure_redirects = 0
net.ipv4.conf.all.accept_source_route = 0
net.ipv4.conf.default.accept_source_route = 0
net.ipv4.conf.all.log_martians = 1
net.ipv4.conf.default.log_martians = 1
net.ipv4.icmp_echo_ignore_broadcasts = 1
net.ipv4.icmp_ignore_bogus_error_responses = 1
net.ipv4.tcp_syncookies = 1
net.ipv4.tcp_max_syn_backlog = 4096
net.ipv4.tcp_synack_retries = 2

# Network hardening (IPv6) - deshabilitar si no se usa
net.ipv6.conf.all.disable_ipv6 = 1
net.ipv6.conf.default.disable_ipv6 = 1

# Filesystem hardening
fs.suid_dumpable = 0
fs.protected_hardlinks = 1
fs.protected_symlinks = 1

# Memory hardening
vm.mmap_min_addr = 65536
```

### Aplicar en runtime (sin reboot)
```bash
sysctl --system  # recarga todos los .conf en /etc/sysctl.d/
# O individual:
sysctl -w kernel.randomize_va_space=2
```

---

## 6. Usuarios y autenticación (CIS 5.1, 5.3, 5.4, 5.5)

| ID | Control | Criticidad | Verificación | Remediación |
|----|---------|------------|--------------|-------------|
| UA-01 | Solo root con UID 0 | P0 | `awk -F: '$3==0' /etc/passwd` | Eliminar/fix otros UID 0 |
| UA-02 | No cuentas sin contraseña | P0 | `awk -F: '$2==""' /etc/shadow` | `passwd -l <user>` o asignar contraseña |
| UA-03 | Contraseñas: expiración máxima 90 días | P2 | `chage -l <user> | grep "Maximum"` | `chage -M 90 <user>` |
| UA-04 | Contraseñas: expiración mínima 7 días | P3 | `chage -l <user> | grep "Minimum"` | `chage -m 7 <user>` |
| UA-05 | Contraseñas: aviso 14 días antes | P3 | `chage -l <user> | grep "Warning"` | `chage -W 14 <user>` |
| UA-06 | Contraseñas: inactividad 30 días tras expiración | P3 | `chage -l <user> | grep "Inactive"` | `chage -I 30 <user>` |
| UA-07 | Política de complejidad (pam_pwquality) | P1 | `grep pam_pwquality /etc/pam.d/passwd` | Configurar `/etc/security/pwquality.conf` |
| UA-08 | Bloqueo tras 5 intentos fallidos (pam_faillock) | P1 | `grep pam_faillock /etc/pam.d/system-auth` | Configurar `/etc/security/faillock.conf` |
| UA-09 | Umask por defecto 027 (o 077) | P2 | `grep ^UMASK /etc/login.defs` | `UMASK 027` |
| UA-10 | Timeout de sesión inactiva (TMOUT) | P2 | `grep TMOUT /etc/profile /etc/bash.bashrc` | `TMOUT=900; readonly TMOUT; export TMOUT` |
| UA-11 | Sudo: requiretty (si aplica) | P3 | `grep requiretty /etc/sudoers` | `Defaults requiretty` |
| UA-12 | Sudo: log_input, log_output, use_pty | P2 | `grep -E 'log_input|log_output|use_pty' /etc/sudoers` | Añadir defaults |
| UA-13 | Sudo: timestamp_timeout ≤ 15 min | P2 | `grep timestamp_timeout /etc/sudoers` | `Defaults timestamp_timeout=15` |
| UA-14 | Cuentas de servicio: shell /usr/sbin/nologin | P2 | `awk -F: '$7!="/usr/sbin/nologin" && $7!="/bin/false" && $3<1000' /etc/passwd` | `usermod -s /usr/sbin/nologin <user>` |
| UA-15 | Root login solo en tty1 (securetty) | P3 | `cat /etc/securetty` | Solo `tty1` `console` `vc/1` |

### Configuración pam_pwquality (`/etc/security/pwquality.conf`)
```ini
minlen = 14
dcredit = -1
ucredit = -1
ocredit = -1
lcredit = -1
minclass = 4
maxrepeat = 3
maxsequence = 3
dictcheck = 1
usercheck = 1
enforce_for_root = 1
retry = 3
```

### Configuración pam_faillock (`/etc/security/faillock.conf`)
```ini
deny = 5
unlock_time = 900
fail_interval = 900
even_deny_root = 1
```

---

## 7. Servicios systemd (CIS 2.1, 2.2)

| ID | Control | Criticidad | Verificación | Remediación |
|----|---------|------------|--------------|-------------|
| SD-01 | Servicios innecesarios deshabilitados | P2 | `systemctl list-unit-files --state=enabled` vs lista permitida | `systemctl disable --now <servicio>` |
| SD-02 | Servicios fallidos = 0 | P1 | `systemctl --failed` | Investigar y fix/reiniciar |
| SD-03 | Unidades críticas: ProtectSystem=strict/full | P2 | `systemctl show <servicio> -p ProtectSystem` | Editar unit file o drop-in |
| SD-04 | Unidades críticas: ProtectHome=yes | P2 | `systemctl show <servicio> -p ProtectHome` | Idem |
| SD-05 | Unidades críticas: PrivateTmp=yes | P2 | `systemctl show <servicio> -p PrivateTmp` | Idem |
| SD-06 | Unidades críticas: NoNewPrivileges=yes | P2 | `systemctl show <servicio> -p NoNewPrivileges` | Idem |
| SD-07 | Unidades críticas: RestrictAddressFamilies=AF_UNIX AF_INET AF_INET6 | P3 | `systemctl show <servicio> -p RestrictAddressFamilies` | Idem |
| SD-08 | Unidades críticas: RestrictNamespaces=yes | P3 | `systemctl show <servicio> -p RestrictNamespaces` | Idem |
| SD-09 | Unidades críticas: LockPersonality=yes | P3 | `systemctl show <servicio> -p LockPersonality` | Idem |
| SD-10 | Unidades críticas: MemoryDenyWriteExecute=yes | P3 | `systemctl show <servicio> -p MemoryDenyWriteExecute` | Idem |
| SD-11 | Unidades críticas: SystemCallFilter=@system-service | P3 | `systemctl show <servicio> -p SystemCallFilter` | Idem |
| SD-12 | Timers: limpieza, snapshots, updates programados | P3 | `systemctl list-timers --all` | Verificar timers necesarios |

### Drop-in example para hardening de servicio (`/etc/systemd/system/sshd.service.d/hardening.conf`)
```ini
[Service]
ProtectSystem=strict
ProtectHome=yes
PrivateTmp=yes
NoNewPrivileges=yes
RestrictAddressFamilies=AF_UNIX AF_INET AF_INET6
RestrictNamespaces=yes
LockPersonality=yes
MemoryDenyWriteExecute=yes
SystemCallFilter=@system-service
ProtectKernelTunables=yes
ProtectKernelModules=yes
ProtectControlGroups=yes
RestrictRealtime=yes
RestrictSUIDSGID=yes
RemoveIPC=yes
PrivateDevices=yes
ProtectProc=invisible
ProcSubset=pid
```

---

## 8. Criptografía (CIS 5.6, 5.7)

| ID | Control | Criticidad | Verificación | Remediación |
|----|---------|------------|--------------|-------------|
| CR-01 | SSH host keys: solo ed25519, rsa-sha2-512/256 | P1 | `ssh-keygen -lf /etc/ssh/ssh_host_*_key.pub` | Regenerar: `ssh-keygen -t ed25519 -f /etc/ssh/ssh_host_ed25519_key -N ""` |
| CR-02 | TLS: certificados no expiran en < 30 días | P1 | `openssl x509 -in <cert> -noout -checkend 2592000` | Renovar certificado |
| CR-03 | TLS: no SSLv2, SSLv3, TLS 1.0, TLS 1.1 | P1 | `openssl ciphers -v` + config servicios | Configurar `MinProtocol = TLSv1.2` en openssl.cnf / servicios |
| CR-04 | LUKS: PBKDF2/Argon2, key slots auditados | P2 | `cryptsetup luksDump /dev/...` | `cryptsetup luksConvertKey --pbkdf argon2id /dev/...` |
| CR-05 | OpenSSL: config system-wide (openssl.cnf) | P2 | `cat /etc/ssl/openssl.cnf | grep -A5 MinProtocol` | `MinProtocol = TLSv1.2` `CipherSuites = HIGH:!aNULL:!kRSA:!PSK:!SRP:!MD5:!RC4` |

---

## 9. Parámetros de kernel en bootloader (GRUB / systemd-boot)

### GRUB (`/etc/default/grub`)
```ini
GRUB_CMDLINE_LINUX_DEFAULT="loglevel=3 quiet \
slab_nomerge init_on_alloc=1 init_on_free=1 page_poison=1 \
vsyscall=none module.sig_enforce=1 lockdown=confidentiality \
kernel.unprivileged_bpf_disabled=1 \
pti=on spectre_v2=on spec_store_bypass_disable=on \
mds=full,nosmt tsx=off tsx_async_abort=full,nosmt \
l1tf=full,force"
```
Luego: `grub-mkconfig -o /boot/grub/grub.cfg`

### systemd-boot (`/boot/loader/entries/*.conf`)
```ini
options root=PARTUUID=... rw loglevel=3 quiet \
slab_nomerge init_on_alloc=1 init_on_free=1 page_poison=1 \
vsyscall=none module.sig_enforce=1 lockdown=confidentiality \
kernel.unprivileged_bpf_disabled=1 \
pti=on spectre_v2=on spec_store_bypass_disable=on \
mds=full,nosmt tsx=off tsx_async_abort=full,nosmt \
l1tf=full,force
```

### Parámetros explicados
| Parámetro | Efecto |
|-----------|--------|
| `slab_nomerge` | Evita fusión de slabs (dificulta heap exploits) |
| `init_on_alloc=1 init_on_free=1` | Limpia memoria al asignar/liberar (previene info leaks) |
| `page_poison=1` | Envenena páginas libres (detecta use-after-free) |
| `vsyscall=none` | Deshabilita mapeo vsyscall legacy (superficie de ataque) |
| `module.sig_enforce=1` | Solo módulos firmados (requiere kernel con CONFIG_MODULE_SIG_FORCE) |
| `lockdown=confidentiality` | Modo lockdown: impide extracción de claves, módulos sin firmar, kexec, etc. |
| `kernel.unprivileged_bpf_disabled=1` | Deshabilita BPF no privilegiado |
| `pti=on` | Page Table Isolation (mitigación Meltdown) |
| `spectre_v2=on` | Mitigación Spectre v2 (retpoline/IBRS) |
| `spec_store_bypass_disable=on` | Mitigación Speculative Store Bypass (SSBD) |
| `mds=full,nosmt` | Mitigación MDS (Microarchitectural Data Sampling) + deshabilita SMT |
| `tsx=off tsx_async_abort=full,nosmt` | Deshabilita TSX (Transactional Synchronization Extensions) |
| `l1tf=full,force` | Mitigación L1TF (L1 Terminal Fault) |

---

## 10. Perfil de hardening por nivel (CIS Nivel 1/2/3)

### Nivel 1: Básico (servidores expuestos a Internet)
- SSH hardening completo (SSH-01 a SSH-15)
- Firewall activo con default deny (FW-01 a FW-04)
- auditd con reglas básicas (AU-01 a AU-07)
- Kernel sysctl network hardening (KR-09 a KR-24)
- Usuarios: UID 0 solo root, sin contraseñas vacías (UA-01, UA-02)
- Servicios: deshabilitar innecesarios (SD-01, SD-02)

### Nivel 2: Estándar (producción, compliance)
- Nivel 1 +
- FS hardening (FS-01 a FS-13)
- auditd completo (AU-08 a AU-15)
- Kernel sysctl completo (KR-01 a KR-30)
- pam_pwquality, pam_faillock (UA-07, UA-08)
- systemd service hardening (SD-03 a SD-11)
- Criptografía (CR-01 a CR-05)
- Bootloader params (si hardware soporta)

### Nivel 3: Alto (entornos regulados, datos sensibles)
- Nivel 2 +
- Particiones separadas con mount options (FS-01 a FS-05)
- SELinux/AppArmor enforcing (RHEL/Fedora: SELinux; Debian/Arch: AppArmor)
- AIDE/Tripwire para integridad de archivos
- Kernel lockdown mode + módulos firmados
- Hardware: TPM2, Secure Boot, measured boot
- Auditoría continua (auditd + log forwarding a SIEM)

---

## 11. Niveles de riesgo de aplicación (R1/R2) y rollback

Todo control de este baseline se aplica con nivel de riesgo y rollback
documentado antes de ejecutar. Regla transversal: **snapshot previo verificado**
(`snapshot_state.py` de mantenimiento o snapper/timeshift) + plan numerado con
control, estado actual, cambio exacto, nivel R y rollback.

| Nivel | Significado | Ejemplos | Requisitos |
|-------|-------------|----------|------------|
| R1 | Reversible, bajo riesgo | sysctl de red (`KR-09`–`KR-24`, salvo `ip_forward` en routers), `kptr_restrict`/`dmesg_restrict` (`KR-02/03`), `umask 027` (`UA-09`), journald persistente (`AU-11`), AIDE timer, `Banner`/`LogLevel` SSH (`SSH-14/15`) | Snapshot previo; verificación funcional tras aplicar |
| R2 | Requiere aprobación humana explícita | `PermitRootLogin`/`PasswordAuthentication` (`SSH-01/02`), firewall default-deny (`FW-02`), `AllowUsers` (`SSH-09`), `pam_pwquality`/`pam_faillock` (`UA-07/08`), bootloader params (§9), `lockdown=confidentiality`, `modules_disabled` (`KR-06`, solo Nivel 3), UFW deny incoming en escritorio | Aprobación explícita + snapshot previo verificado + verificación funcional inmediata (login, red, app afectada) |

### Rollback por familia de control
```bash
# SSH: restaurar backup y recargar (NO reiniciar sshd a ciegas con sesión única)
cp /root/hardening-bak/sshd_config.bak /etc/ssh/sshd_config
sshd -t && systemctl reload sshd

# sysctl: revertir clave y recargar
sysctl -w net.ipv4.ip_forward=1
rm /etc/sysctl.d/99-hardening.conf && sysctl --system

# firewall: volver a política previa documentada en el plan
ufw default allow incoming   # SOLO si el plan previo decía allow; si no, revisar plan
# nftables:
cp /root/hardening-bak/nftables.conf.bak /etc/nftables.conf && nft -f /etc/nftables.conf

# auditd: quitar reglas y recargar (inmutables con -e 2 requieren reboot)
rm /etc/audit/rules.d/hardening.rules && augenrules --load   # o reboot si -e 2

# bootloader: editar /etc/default/grub, regenerar y reboot en ventana
grub-mkconfig -o /boot/grub/grub.cfg

# snapshots del sistema (cuando existen)
snapper undochange <pre>..<post>        # btrfs/snapper
timeshift --restore                     # timeshift (interactivo; ventana acordada)
```

### Procedimiento de aplicación
1. Presentar plan numerado con: control, estado actual, cambio exacto, nivel R, rollback.
2. Aplicar solo lo aprobado; después de cada cambio R2, verificación funcional inmediata
   (login, red, app afectada).
3. Registrar en log de sesión y dejar constancia de qué quedó fuera y por qué.

---

## 12. Controles de escritorio/workstation Ubuntu (heredados)

Controles aplicables a una máquina personal de desarrollo (no servidor).
Complementan §1–§10; en caso de conflicto, en escritorio developer manda esta
sección (ver "Lo que NO se endurece" más abajo).

### 12.1 Kernel y MAC

| Control | Verificación | Nivel |
|---|---|---|
| AppArmor activo y servicio enabled | `/sys/module/apparmor/parameters/enabled` | — |
| userns no privilegiados restringidos | `sysctl kernel.apparmor_restrict_unprivileged_userns` = 1; NUNCA bajar a 0 como atajo — perfiles por herramienta | R2 |
| sysctl de red endurecidos | `net.ipv4.conf.all.rp_filter`, `accept_redirects=0`, `send_redirects=0`, `tcp_syncookies=1` | R1 |
| kptr_restrict, dmesg_restrict | `kernel.kptr_restrict=2`, `kernel.dmesg_restrict=1` | R1 |

### 12.2 Autenticación y acceso

| Control | Verificación | Nivel |
|---|---|---|
| SSH: PermitRootLogin no, MaxAuthTries ≤ 4 | `sshd -T` | R2 (toca acceso remoto: planificar) |
| sudo con timestamp, sin NOPASSWD amplio | `grep -r NOPASSWD /etc/sudoers*` | R1 |
| Drop-ins sudo temporales: siempre con fecha de caducidad mental y eliminación al terminar la tarea | `ls /etc/sudoers.d/` | — |
| Umask 027 en cuentas con secretos | `/etc/login.defs`, `~/.profile` | R1 |

### 12.3 Auditoría y detección

| Control | Verificación | Nivel |
|---|---|---|
| auditd activo con reglas de identidad | `auditctl -l` (-w passwd/shadow/sudoers) | R1 |
| journald persistente | `/var/log/journal` existe | R1 |
| AIDE programado (timer) + DB regenerada tras cambios voluntarios | `systemctl list-timers` | R1 |
| Recolector de denegaciones MAC persistente | `/var/log/apparmor/denials.log` | R1 |
| Canal de alertas en escritorio | unidad user `apparmor-notify` | R1 |

### 12.4 Superficie de ataque

| Control | Verificación | Nivel |
|---|---|---|
| Firewall deny incoming por defecto | `ufw status` | R2 |
| Solo servicios necesarios escuchando | `ss -tulpn` revisado | R2 |
| Binarios con secretos en tierra de root (canon root-owned) | `ls -la ~/Terminal` | R1 |
| Navegadores y agentes IA con perfil MAC propio | `aa-status` | R2 (ciclo de días) |

### 12.5 Lo que NO se endurece en un escritorio developer

- No confinar intérpretes globales (node, python3), shells interactivos, compiladores ni git: el coste rompe el trabajo diario y el beneficio es mínimo frente a confinar servicios y agentes.
- No desactivar servicios del escritorio por paranoia de checklist: cada desactivación necesita su razón de amenaza.
- No auditd forense exhaustivo (todas las syscalls): el ruido entierra la señal; reglas de vigilancia sobre rutas sensibles bastan.

---

## Uso en las skills

- `operate-security`: `harden_plan.py` lee este baseline canónico y genera plan
  P1–P4 + diff + rollback; `postura_seguridad.sh` inventaría defensas (R0);
  escaneos (`scan_orchestrator.py`) y AppArmor (`apparmor_lifecycle.py`) operan
  contra estos controles.
- `operate-maintenance`: `audit_quick.py`/`audit_full.py` verifican **solo** el
  subconjunto de higiene (PKG-\*, FS-09/10/11, LOG-06/08, SRV-02, NET-04). Todo
  lo SSH/KR/FS-05–08/AU/UA/CR es hardening puro y vive aquí.
- `report_render.py` (mantenimiento) muestra puntuación por categoría; el nivel
  de hardening alcanzado (Nivel 1/2/3) lo evalúa `operate-security`.
- Perfil de sistema (`system-profile.json`) declara `hardening_level: 1|2|3` y
  excepciones documentadas.
