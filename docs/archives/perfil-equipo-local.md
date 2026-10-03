# Perfil local del operador

Archivo de operador, fuera del paquete que carga el agente. No forma parte de `operar-mantenimiento`.

Información específica del equipo local (Ubuntu 26.04, apt + snap, sin flatpak):

- CPU **Ryzen AI 7 350 + RTX 5060**; kernel `linux-image-generic-hwe-26.04`.
- WiFi Realtek **RTL8852CE** (`rtw89_8852ce`) con crashes de firmware conocidos (`[ERR]fw PC`, `SER catches error 0x999`); mitigación en `/etc/modprobe.d/rtw89-8852ce.conf` (ASPM y power-save off). Las desautenticaciones `locally_generated=1` no son culpa del router.
- Firewall ufw (deny incoming); SSH en 0.0.0.0:22 (excepción documentada: WiFi doméstica DHCP, no restringir ListenAddress).
- auditd con reglas base; journald persistente. Sin timeshift/snapper → snapshots manuales con `snapshot_state.py`.
- Servicios de usuario activos: `voicebox-backend.service`, `ydotoold.service`.

## Gestión de sudo en este equipo

`/etc/sudoers.d/90-mantenimiento` concede NOPASSWD acotado para: `apt`, `apt-get`, `dpkg`, `ufw`, `auditctl`, `augenrules`, `sysctl`, `fwupdmgr`, `snap`, `systemctl`, `update-initramfs`, `modprobe`. Protocolo:

1. Si el comando está cubierto, usar `sudo -n <comando>` directamente (nunca pedir contraseña).
2. Si hace falta un comando root no cubierto, agrupar todas las acciones root pendientes en un único `/tmp/fix-*.sh` y ejecutarlo una sola vez con askpass (un popup por sesión como máximo, avisando antes).
3. Si un comando root se repite, proponer añadirlo (con argumentos concretos) a `/etc/sudoers.d/90-mantenimiento` y validar con `visudo -cf`.
4. Nunca pedir contraseña en chat ni usar `echo pass | sudo -S`, ni NOPASSWD para `rm`/`find`/shells/`ALL`.
