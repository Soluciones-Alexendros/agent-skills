# debian-rhel-adapters.md

Adaptadores para Debian/Ubuntu y RHEL/Fedora/CentOS/AlmaLinux/Rocky. La skill detecta la distro automáticamente y usa el adaptador correspondiente. Cada adaptador mapea las operaciones canónicas de Arch a sus equivalentes.

---

## Detección automática de distro

```bash
# En probe_system.py
if [[ -f /etc/os-release ]]; then
    source /etc/os-release
    DISTRO_ID="$ID"
    DISTRO_LIKE="${ID_LIKE:-}"
else
    DISTRO_ID="unknown"
fi

# Mapeo a familia
case "$DISTRO_ID" in
    arch|endeavouros|cachyos|manjaro|garuda)
        FAMILY="arch"
        PKG_MGR="pacman"
        ;;
    artix)
        # Artix usa OpenRC/Runit en lugar de systemd: los comandos
        # systemctl, journalctl, mkinitcpio y timers systemd no aplican.
        # Adaptadores systemd-dependent deben omitirse o traducirse a
        # rc-service / sv según init en uso.
        FAMILY="artix"
        PKG_MGR="pacman"
        ;;
    debian|ubuntu|linuxmint|pop|elementary|kali|parrot|zorin)
        FAMILY="debian"
        PKG_MGR="apt"
        ;;
    fedora|rhel|centos|almalinux|rocky|ol|scientific)
        FAMILY="rhel"
        PKG_MGR="dnf"
        ;;
    opensuse*|sles)
        FAMILY="suse"
        PKG_MGR="zypper"
        ;;
    *)
        FAMILY="unknown"
        PKG_MGR="unknown"
        ;;
esac
```

---

## Adaptador Debian / Ubuntu / derivados

### Gestión de paquetes (apt)

| Operación Arch | Equivalente Debian/Ubuntu | Notas |
|----------------|---------------------------|-------|
| `pacman -Sy` | `apt update` | Sincroniza BD |
| `pacman -Syu` | `apt full-upgrade` | Actualización completa (maneja dependencias cambiantes) |
| `pacman -S pkg` | `apt install pkg` | Instalación |
| `pacman -Rns pkg` | `apt purge --auto-remove pkg` | Elimina + dependencias huérfanas + configs |
| `pacman -Q` | `dpkg -l` / `apt list --installed` | Lista instalados |
| `pacman -Qtdq` | `apt autoremove --dry-run` / `deborphan` | Huérfanos |
| `pacman -Qm` | `apt list --manual-installed` | Paquetes instalados manualmente |
| `pacman -Qk` | `debsums -c` | Verificación integridad (requiere debsums) |
| `pacman -Qo /path` | `dpkg -S /path` | Dueño de archivo |
| `paccache -r -k 3` | `apt autoclean` / `apt clean` | Limpieza caché (apt no tiene retención por versiones) |
| `checkupdates` | `apt list --upgradable 2>/dev/null` | Actualizaciones disponibles |
| `pacdiff` | `ucf` / `dpkg --configure -a` / manual | Gestión conffiles (.dpkg-new/.dpkg-old) |

### Caché de paquetes
```bash
# Ver tamaño
du -sh /var/cache/apt/archives

# Limpiar paquetes .deb descargados (conserva lock file)
apt autoclean  # elimina versiones antiguas, conserva la última

# Limpiar TODO (incluye lock)
apt clean

# Configurar retención automática en /etc/apt/apt.conf.d/99clean-cache:
# APT::Clean-Installed "false";
# APT::Archives::MaxAge "30";
# APT::Archives::MinAge "7";
# APT::Archives::MaxSize "500";
```

### Huérfanos y limpieza
```bash
# Listar paquetes instalados automáticamente y ya no necesarios
apt autoremove --dry-run

# Ejecutar (requiere confirmación)
apt autoremove --purge

# deborphan: encuentra paquetes bibliotecas sin dependientes
apt install deborphan
deborphan  # lista
deborphan | xargs apt purge -y  # eliminar (cuidado)
```

### Archivos de configuración modificados (.dpkg-new, .dpkg-old, .ucf-new, .ucf-old)
```bash
# Buscar
find /etc -name "*.dpkg-*" -o -name "*.ucf-*" 2>/dev/null

# ucf (Update Configuration Files) - herramienta estándar Debian
ucf --purge /etc/archivo.conf  # elimina gestión ucf para este archivo
ucf -h  # ayuda

# dpkg-reconfigure para reconfigurar paquetes
dpkg-reconfigure -plow <paquete>
```

### Actualizaciones de seguridad
```bash
# Solo actualizaciones de seguridad
apt list --upgradable 2>/dev/null | grep -i security

# unattended-upgrades (automático)
apt install unattended-upgrades
dpkg-reconfigure -plow unattended-upgrades
# Config en /etc/apt/apt.conf.d/50unattended-upgrades
```

### Kernel y bootloader
```bash
# Kernels instalados
dpkg -l 'linux-image-*'

# Kernel running
uname -r

# Actualizar GRUB
update-grub
# o
grub-mkconfig -o /boot/grub/grub.cfg

# initramfs
update-initramfs -u -k all
```

### Firmware
```bash
# fwupd funciona igual (independiente de distro)
fwupdmgr get-devices
fwupdmgr get-updates
fwupdmgr update

# Paquetes firmware en Debian/Ubuntu
apt install linux-firmware
# O específicos: amd64-microcode, intel-microcode
```

### Servicios y systemd
```bash
# Igual que Arch (systemd es estándar)
systemctl status <servicio>
systemctl enable --now <servicio>
systemctl --failed
systemd-analyze blame
```

### Journal y logs
```bash
# Igual que Arch (systemd-journald)
journalctl --vacuum-time=7d
journalctl --vacuum-size=500M
journalctl -p 0..3 --since "24 hours ago"
```

### Verificación de integridad
```bash
# debsums (instalar si no está)
apt install debsums
debsums -c  # solo archivos modificados
debsums -a  # todos

# apt-get check: dependencias rotas
apt-get check
```

### needrestart (servicios que requieren reinicio)
```bash
apt install needrestart
needrestart -r l  # lista
needrestart -r a  # reinicia automáticamente (cuidado)
```

### Mirrorlist / repositorios
```bash
# /etc/apt/sources.list y /etc/apt/sources.list.d/
# No hay reflector equivalente estándar.
# Herramientas: apt-mirror, apt-spy2, netselect-apt
# Para Ubuntu: software-properties-gtk / software-properties-kde

# Verificar accesibilidad
apt update  # falla si mirrors no responden
```

---

## Adaptador RHEL / Fedora / CentOS / AlmaLinux / Rocky

### Gestión de paquetes (dnf / yum)

| Operación Arch | Equivalente RHEL/Fedora | Notas |
|----------------|-------------------------|-------|
| `pacman -Sy` | `dnf check-update` / `dnf makecache` | Sincroniza BD |
| `pacman -Syu` | `dnf upgrade --refresh` | Actualización completa |
| `pacman -S pkg` | `dnf install pkg` | Instalación |
| `pacman -Rns pkg` | `dnf remove pkg` + `dnf autoremove` | Elimina + limpieza |
| `pacman -Q` | `rpm -qa` / `dnf list installed` | Lista instalados |
| `pacman -Qtdq` | `dnf repoquery --unneeded` / `dnf autoremove --dry-run` | Huérfanos |
| `pacman -Qm` | `dnf list installed | grep -v @System` / `rpm -qa --qf '%{NAME} %{VENDOR}\n' | grep -v 'Red Hat\\|Fedora\\|CentOS'` | Third-party |
| `pacman -Qk` | `rpm -Va` | Verificación integridad |
| `pacman -Qo /path` | `rpm -qf /path` | Dueño de archivo |
| `paccache -r -k 3` | `dnf clean all` / `dnf clean packages` | Limpieza caché |
| `checkupdates` | `dnf check-update` / `dnf list upgrades` | Actualizaciones disponibles |

### Caché de paquetes
```bash
# Ver tamaño
du -sh /var/cache/dnf

# Limpiar
dnf clean packages      # solo paquetes .rpm
dnf clean metadata      # solo metadatos
dnf clean all           # todo

# Configurar retención en /etc/dnf/dnf.conf:
# clean_requirements_on_remove=True
# installonly_limit=3  # kernels a conservar
# max_parallel_downloads=10
```

### Huérfanos y limpieza
```bash
# Listar paquetes no necesarios (instalados como dependencias)
dnf repoquery --unneeded

# Eliminar (autorremove limpia dependencias huérfanas)
dnf autoremove

# dnf remove + autoremove en uno
dnf remove <pkg> --autoremove
```

### Archivos de configuración modificados (.rpmnew, .rpmsave)
```bash
# Buscar
find /etc -name "*.rpmnew" -o -name "*.rpmsave" 2>/dev/null

# rpmconf: herramienta para gestionar (similar a pacdiff/ucf)
dnf install rpmconf
rpmconf -a  # interactivo
```

### Actualizaciones de seguridad
```bash
# Solo seguridad
dnf check-update --security
dnf upgrade --security

# dnf-automatic (equivalente a unattended-upgrades)
dnf install dnf-automatic
systemctl enable --now dnf-automatic-install.timer
# Config en /etc/dnf/automatic.conf
```

### Kernel y bootloader
```bash
# Kernels instalados
rpm -qa kernel-core kernel

# Kernel running
uname -r

# GRUB2 (BIOS)
grub2-mkconfig -o /boot/grub2/grub.cfg

# GRUB2 (UEFI)
grub2-mkconfig -o /boot/efi/EFI/<distro>/grub.cfg

# Kernel install hooks (dnf instala kernels y actualiza GRUB automáticamente)
# Ver /etc/kernel/install.d/
```

### Firmware
```bash
# fwupd igual
fwupdmgr get-devices
fwupdmgr get-updates
fwupdmgr update

# Microcode
dnf install microcode_ctl  # Intel/AMD
# Se aplica automáticamente en initramfs via dracut
```

### SELinux (crítico en RHEL/Fedora)
```bash
# Estado
getenforce  # Enforcing / Permissive / Disabled
sestatus

# Booleans
semanage boolean -l
getsebool -a

# Políticas
semodule -l

# Auditoría SELinux
ausearch -m avc -ts recent
sealert -a /var/log/audit/audit.log
```

### Verificación de integridad
```bash
# rpm -Va: verifica todos los archivos de paquetes RPM
# Salida: S=size, M=mode, 5=MD5, D=device, L=link, U=user, G=group, T=time, c=config
rpm -Va 2>/dev/null | grep -v "^.......  c /"  # ignora configs modificadas legítimamente

# dnf verify (wrapper)
dnf verify <paquete>
```

### needrestart / needs-restarting
```bash
# needs-restarting (paquete dnf-utils)
dnf install dnf-utils
needs-restarting -r  # reboot requerido (kernel, systemd, glibc)
needs-restarting     # servicios que requieren reinicio
```

### Mirrorlist / repositorios
```bash
# /etc/yum.repos.d/ /etc/dnf/repos.d/
# dnf config-manager para habilitar/deshabilitar
dnf config-manager --set-enabled <repo>
dnf config-manager --set-disabled <repo>

# fastestmirror plugin (dnf-plugins-core)
dnf install dnf-plugins-core
# Config en /etc/dnf/dnf.conf: fastestmirror=true

# Verificar mirrors
dnf repolist
```

---

## Adaptador openSUSE / SLES (zypper)

### Gestión de paquetes (zypper)

| Operación Arch | Equivalente openSUSE |
|----------------|----------------------|
| `pacman -Sy` | `zypper refresh` |
| `pacman -Syu` | `zypper dup` (Tumbleweed) / `zypper up` (Leap) |
| `pacman -S pkg` | `zypper in pkg` |
| `pacman -Rns pkg` | `zypper rm -u pkg` |
| `pacman -Q` | `zypper se -i` / `rpm -qa` |
| `pacman -Qtdq` | `zypper packages --orphaned` |
| `paccache -r -k 3` | `zypper clean -a` |
| `checkupdates` | `zypper list-updates` |

### Snapper (snapshots BTRFS) - nativo en openSUSE
```bash
# Listar snapshots
snapper list

# Crear snapshot pre/post
snapper create --description "Pre-update" --cleanup-algorithm number
# zypper llama automáticamente a snapper si está configurado

# Rollback
snapper undochange <pre>..<post>
```

---

## Tabla resumen de comandos por familia

| Acción | Arch (pacman) | Debian/Ubuntu (apt) | RHEL/Fedora (dnf) | openSUSE (zypper) |
|--------|---------------|---------------------|-------------------|-------------------|
| Sync DB | `pacman -Sy` | `apt update` | `dnf makecache` | `zypper refresh` |
| Full upgrade | `pacman -Syu` | `apt full-upgrade` | `dnf upgrade --refresh` | `zypper dup` / `zypper up` |
| Install | `pacman -S` | `apt install` | `dnf install` | `zypper in` |
| Remove + deps | `pacman -Rns` | `apt purge --auto-remove` | `dnf remove --autoremove` | `zypper rm -u` |
| List installed | `pacman -Q` | `apt list --installed` | `dnf list installed` | `zypper se -i` |
| Orphans | `pacman -Qtdq` | `apt autoremove --dry-run` | `dnf repoquery --unneeded` | `zypper packages --orphaned` |
| Foreign pkgs | `pacman -Qm` | `apt list --manual-installed` | `dnf list extras` | `zypper se -i -t package --unneeded` |
| Verify integrity | `pacman -Qk` | `debsums -c` | `rpm -Va` | `rpm -Va` |
| Owner of file | `pacman -Qo` | `dpkg -S` | `rpm -qf` | `rpm -qf` |
| Clean cache | `paccache -r -k3` | `apt autoclean` | `dnf clean packages` | `zypper clean -a` |
| Check updates | `checkupdates` | `apt list --upgradable` | `dnf check-update` | `zypper list-updates` |
| Config files | `pacdiff` | `ucf` / `dpkg-reconfigure` | `rpmconf` | `rpmconf` |
| Kernel rebuild | `mkinitcpio -P` | `update-initramfs -u -k all` | `dracut -f` / auto | `dracut -f` / auto |
| Bootloader update | `bootctl update` / `grub-mkconfig` | `update-grub` | `grub2-mkconfig` | `grub2-mkconfig` |
| Firmware | `fwupdmgr` | `fwupdmgr` | `fwupdmgr` | `fwupdmgr` |
| Services restart | `needrestart` | `needrestart` | `needs-restarting` | `zypper ps` / `systemctl` |

---

## Perfil de sistema por familia (ejemplos)

### Debian/Ubuntu
```yaml
distro: "ubuntu"
version: "24.04"
package_manager: "apt"
aur_helper: null
kernel: "linux-generic"
critical_services:
  - "systemd-resolved"
  - "ssh"
  - "apparmor"
protected_paths:
  - "/boot"
  - "/etc/fstab"
  - "/etc/ssh/sshd_config"
  - "/etc/apparmor/"
exceptions:
  - package: "nvidia-driver-*"
    reason: "Drivers propietarios, actualización manual"
  - path: "/var/lib/docker"
    reason: "Docker storage"
snapshot_tool: "timeshift"  # o snapper si BTRFS
```

### RHEL/Fedora
```yaml
distro: "fedora"
version: "40"
package_manager: "dnf"
aur_helper: null
kernel: "kernel"
critical_services:
  - "NetworkManager"
  - "sshd"
  - "firewalld"
  - "selinux-autorelabel"
protected_paths:
  - "/boot"
  - "/etc/fstab"
  - "/etc/ssh/sshd_config"
  - "/etc/selinux/"
  - "/boot/efi/"
exceptions:
  - package: "kernel"
    reason: "Múltiples kernels conservados (installonly_limit=3)"
  - path: "/var/lib/containers"
    reason: "Podman storage"
snapshot_tool: "snapper"  # BTRFS por defecto en Fedora Workstation
```

---

## Notas de implementación para la skill

1. **probe_system.py** detecta `FAMILY` y `PKG_MGR` y exporta variables de entorno para los scripts
2. **audit_quick.py** y **audit_full.py** usan funciones wrapper que despachan al adaptador correcto
3. **clean_routine.py** usa la misma lógica de despacho
4. **risk_gate.py** conoce las rutas protegidas por familia (ver safety-policy.md)
5. **report_render.py** incluye el nombre de la distro/familia en el informe
6. Los checklists en `audit-checklist.md` tienen columnas "Modo" que indican quick/full; los scripts filtran por familia