# arch-maintenance.md

Rutinas canónicas de mantenimiento para Arch Linux y derivados (EndeavourOS, CachyOS, Manjaro, Garuda). Basado en ArchWiki "System maintenance" y mejores prácticas de la comunidad.

---

## Principios Arch

1. **Leer noticias antes de actualizar** — Regla de oro del rolling release
2. **El gestor de paquetes es la fuente de verdad** — Nada de instalaciones manuales fuera de pacman
3. **No borrado ciego** — Symlinks rotos, configs antiguas, homes se listan e inspeccionan antes de retirar
4. **AUR con sobriedad** — Revisión de PKGBUILD, límite cuantitativo configurable
5. **Backup antes de cambios** — Especialmente kernel, bootloader, glibc, systemd

---

## 1. Actualización del sistema

### Pre-actualización (obligatorio)

```bash
# 1. Leer noticias de Arch Linux
# Fuente: https://archlinux.org/news/ (RSS: https://archlinux.org/feeds/news/)
# Herramienta: `pacman -Sy` (solo sincroniza BD, no instala) + leer noticias
# O usar: `yay -Ps` (muestra noticias de AUR también)

# 2. Verificar espacio en /boot (mínimo 100MB libre para kernel + initramfs)
df -h /boot

# 3. Verificar paquetes que requieren intervención manual (pacnew, rebuild-detector)
pacdiff --output
rebuild-detector

# 4. Snapshot del estado actual (si timeshift/snapper/btrfs)
timeshift --create --comments "Pre-update $(date)" --tags D
# o
snapper create --description "Pre-update $(date)" --cleanup-algorithm number
```

### Actualización

```bash
# Actualización completa (nunca parcial: pacman -Syu, no pacman -Sy)
pacman -Syu

# Si hay paquetes AUR:
yay -Syu  # o paru, o makepkg -si manual tras revisar PKGBUILD
```

### Post-actualización

```bash
# 1. Verificar .pacnew/.pacsave
pacdiff -s  # solo muestra, no interactúa

# 2. Reconstruir módulos de kernel si cambió linux/linux-lts/linux-zen
# (mkinitcpio se ejecuta automáticamente via hook, pero verificar)
mkinitcpio -P

# 3. Verificar servicios que requieren reinicio
needrestart -r l  # o: systemctl list-units --state=running | grep -E 'service.*running' | while read u; do systemctl try-reload-or-restart "$u"; done

# 4. Limpiar caché conservando 3 versiones
paccache -r -k 3

# 5. Verificar integridad de paquetes
pacman -Qk 2>&1 | grep -v "0 altered files"
```

---

## 2. Limpieza de paquetes y cachés

### Caché de pacman (conservar N=3 versiones por defecto)

```bash
# Dry-run: muestra qué se borraría
paccache -r -k 3 -d

# Ejecución real
paccache -r -k 3

# Eliminar TODAS las versiones de paquetes desinstalados
paccache -ruk0
```

### Paquetes huérfanos (sin dependientes)

```bash
# Listar huérfanos
pacman -Qtdq

# Eliminar huérfanos (con confirmación, dry-run primero)
pacman -Rns $(pacman -Qtdq)  # SOLO si la lista no está vacía y usuario confirma

# Nota: nunca eliminar ciegamente. Algunos "huérfanos" son dependencias opcionales
# que el usuario quiere mantener. Revisar lista antes.
```

### Paquetes foráneos (AUR, manuales, third-party)

```bash
# Listar
pacman -Qmq

# Verificar actualizaciones AUR
yay -Qu  # o paru -Qu

# Revisar PKGBUILD antes de actualizar AUR
yay -G <paquete>  # descarga PKGBUILD a directorio actual
# Editar/revisar PKGBUILD
makepkg -si  # compila e instala
```

### Archivos .pacnew / .pacsave

```bash
# Buscar
find /etc -name "*.pacnew" -o -name "*.pacsave"

# Gestionar con pacdiff (interactivo, muestra diff)
pacdiff

# O manual: comparar y fusionar
# vimdiff /etc/archivo.conf /etc/archivo.conf.pacnew
# mv /etc/archivo.conf.pacnew /etc/archivo.conf  # tras fusión
```

---

## 3. Mirrorlist y repositorios

### Actualizar mirrorlist con reflector

```bash
# Dry-run: muestra nuevos mirrors
reflector --latest 20 --protocol https --sort rate --dry-run

# Ejecución real (requiere root)
reflector --latest 20 --protocol https --sort rate --save /etc/pacman.d/mirrorlist

# Verificar que mirrors responden
pacman -Sy  # sincroniza con nueva lista
```

### Repositorios oficiales vs AUR

```bash
# Verificar /etc/pacman.conf: repos habilitados, orden de prioridad
# [core], [extra], [community], [multilib] - orden estándar
# AUR NO va en pacman.conf (se gestiona con yay/paru/makepkg)
```

---

## 4. Journal y logs

### Vacuum de journal (systemd-journald)

```bash
# Por tiempo: conservar 7 días
journalctl --vacuum-time=7d

# Por tamaño: máximo 500MB
journalctl --vacuum-size=500M

# Ver uso actual
journalctl --disk-usage

# Configuración persistente en /etc/systemd/journald.conf:
# SystemMaxUse=500M
# SystemKeepFree=1G
# RuntimeMaxUse=100M
```

### Logs de pacman

```bash
# Ver historial de actualizaciones
grep "pacman -Syu" /var/log/pacman.log

# Ver instalaciones/eliminaciones recientes
grep -E "installed|removed" /var/log/pacman.log | tail -20
```

---

## 5. Kernel y bootloader

### Múltiples kernels (recomendado: linux + linux-lts)

```bash
# Instalar kernel LTS como respaldo
pacman -S linux-lts linux-lts-headers

# Regenerar initramfs para todos los kernels
mkinitcpio -P

# Verificar entries de bootloader
# systemd-boot:
bootctl list
# GRUB:
grub-editenv list
ls /boot/loader/entries/  # systemd-boot
```

### Parámetros de kernel (hardening)

```bash
# Editar /etc/default/grub o /boot/loader/entries/*.conf
# Parámetros recomendados:
# slab_nomerge init_on_alloc=1 init_on_free=1 page_poison=1
# vsyscall=none module.sig_enforce=1 lockdown=confidentiality
# kernel.unprivileged_bpf_disabled=1
# (ver references/hardening-baseline.md para lista completa)
```

---

## 6. Firmware (fwupd)

```bash
# Ver dispositivos compatibles
fwupdmgr get-devices

# Ver actualizaciones disponibles
fwupdmgr get-updates

# Actualizar (requiere reinicio para algunos dispositivos)
fwupdmgr update

# Nota: fwupd usa LVFS (Linux Vendor Firmware Service).
# Algunos fabricantes no publican ahí (ej. NVIDIA GPU firmware).
```

---

## 7. Rebuild-detector (paquetes rotos por actualización de librerías)

```bash
# Instalar
pacman -S rebuild-detector

# Ejecutar
rebuild-detector

# Salida: lista de paquetes que necesitan reconstrucción
# Acción: reconstruir desde AUR o reportar al mantenedor
```

---

## 8. Symlinks rotos

```bash
# Buscar (solo listar, NUNCA borrar ciegamente)
find /etc /usr /boot -xtype l 2>/dev/null

# Buscar en home del usuario (informativo)
find /home -xtype l 2>/dev/null | head -20

# Análisis: cada symlink roto debe investigarse:
# - ¿Apuntaba a archivo de paquete eliminado?
# - ¿Es residuo de configuración manual?
# - ¿Rompe funcionalidad?
# Solo eliminar si se confirma que es basura sin efecto colateral.
```

---

## 9. Cachés de usuario (~/.cache)

```bash
# Tamaño
du -sh ~/.cache

# Limpieza selectiva (ejemplos):
# - Navegadores: gestionan su propia caché
# - yay/paru: ~/.cache/yay, ~/.cache/paru (pkgs compilados)
# - pip: ~/.cache/pip
# - npm: ~/.npm
# - cargo: ~/.cargo/registry/cache

# Regla: listar > 100MB, mostrar al usuario, él decide.
```

---

## 10. Verificación de integridad post-mantenimiento

```bash
# 1. Paquetes alterados
pacman -Qk 2>&1 | grep -v "0 altered files"

# 2. Servicios fallidos
systemctl --failed

# 3. Espacio en disco
df -h / /boot /var /home

# 4. Journal errores recientes
journalctl -p 0..3 --since "1 hour ago" --no-pager

# 5. Kernel running vs installed
uname -r
pacman -Q linux linux-lts linux-zen  # según kernels instalados
```

---

## 11. Automatización (systemd timers)

### Timer para actualización semanal (solo sincronización + notificación)

```ini
# /etc/systemd/system/pacman-sync.timer
[Unit]
Description=Weekly pacman database sync

[Timer]
OnCalendar=weekly
Persistent=true
RandomizedDelaySec=4h

[Install]
WantedBy=timers.target
```

```ini
# /etc/systemd/system/pacman-sync.service
[Unit]
Description=Sync pacman databases
After=network-online.target
Wants=network-online.target

[Service]
Type=oneshot
ExecStart=/usr/bin/pacman -Sy
ExecStartPost=/usr/bin/bash -c 'checkupdates 2>/dev/null | wc -l | xargs -I{} notify-send "Updates available: {}"'
```

### Timer para limpieza de journal (diario)

```ini
# /etc/systemd/system/journal-vacuum.timer
[Unit]
Description=Daily journal vacuum

[Timer]
OnCalendar=daily
Persistent=true

[Install]
WantedBy=timers.target
```

```ini
# /etc/systemd/system/journal-vacuum.service
[Unit]
Description=Vacuum systemd journal

[Service]
Type=oneshot
ExecStart=/usr/bin/journalctl --vacuum-time=7d --vacuum-size=500M
```

### Timer para paccache (semanal)

```ini
# /etc/systemd/system/paccache.timer
[Unit]
Description=Weekly pacman cache cleanup

[Timer]
OnCalendar=weekly
Persistent=true

[Install]
WantedBy=timers.target
```

```ini
# /etc/systemd/system/paccache.service
[Unit]
Description=Clean pacman cache (keep 3 versions)

[Service]
Type=oneshot
ExecStart=/usr/bin/paccache -r -k 3
```

---

## Checklist de rutina semanal (modo `routine`)

| Acción                  | Comando                       | Requiere aprobación                   |
| ----------------------- | ----------------------------- | ------------------------------------- |
| Sincronizar BD pacman   | `pacman -Sy`                  | No (R0)                               |
| Leer noticias Arch      | Manual / RSS                  | No (R0)                               |
| Verificar espacio /boot | `df -h /boot`                 | No (R0)                               |
| Listar actualizaciones  | `checkupdates` / `yay -Qu`    | No (R0)                               |
| Listar huérfanos        | `pacman -Qtdq`                | No (R0)                               |
| Listar .pacnew          | `find /etc -name "*.pacnew"`  | No (R0)                               |
| Vacuum journal          | `journalctl --vacuum-time=7d` | Sí (R1, snapshot)                     |
| Limpiar caché pacman    | `paccache -r -k 3`            | Sí (R1, snapshot)                     |
| Eliminar huérfanos      | `pacman -Rns $(pacman -Qtdq)` | Sí (R1, snapshot + confirmación)      |
| Gestionar .pacnew       | `pacdiff`                     | Sí (R2, aprobación + backup)          |
| Actualizar sistema      | `pacman -Syu` (+ AUR)         | Sí (R2, aprobación + plan + snapshot) |
| Regenerar initramfs     | `mkinitcpio -P`               | Sí (R2, si kernel actualizado)        |
| Actualizar firmware     | `fwupdmgr update`             | Sí (R2, aprobación)                   |

---

## Excepciones comunes en perfil de usuario

```yaml
# system-profile.yaml
exceptions:
  - package: "nvidia"
    reason: "Drivers propietarios, actualización manual tras leer changelog"
    action: "hold" # no actualizar automáticamente
  - package: "linux-zen"
    reason: "Kernel personalizado, compilar módulos out-of-tree tras update"
    action: "rebuild-modules"
  - path: "/home/user/.cache/yay"
    reason: "Caché de compilación AUR, usuario gestiona tamaño"
    action: "ignore"
  - path: "/var/lib/docker"
    reason: "Docker gestiona su propio almacenamiento"
    action: "ignore"
```
