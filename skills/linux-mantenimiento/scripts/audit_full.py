#!/usr/bin/env python3
"""audit_full.py - Auditoría completa (seguridad, rendimiento, higiene, config).

Port Python de audit_full.sh. Ejecuta todos los controles del checklist
P0-P4 (extiende audit_quick) y genera salida JSON con Health Score.
Uso: audit_full.py [output-file] [profile-file]
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import re
import subprocess
import sys
import time

from common import (
    BLUE,
    FindingCollector,
    color,
    count_nonempty,
    load_profile_family,
    run,
    service_active,
    sshd_effective,
    sysctl_get,
    to_int,
    which,
)

log_tag = color("[AUDIT-FULL]", BLUE)

logger = logging.getLogger("mantenimiento.audit_full")


def _setup_logging(verbose: bool = False) -> None:
    level = logging.DEBUG if verbose else logging.WARNING
    if not logging.getLogger().handlers:
        logging.basicConfig(level=level, format="%(levelname)s: %(message)s", stream=sys.stderr)
    else:
        logging.getLogger().setLevel(level)


def run_check(cmd: str, timeout: int = 10) -> str:
    return run(cmd, timeout=timeout)


def sshd_eff_get(key: str) -> str:
    for line in sshd_effective().splitlines():
        parts = line.split()
        if parts and parts[0].lower() == key and len(parts) >= 2:
            return parts[1]
    return ""


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Auditoría completa (controles P0-P4).")
    parser.add_argument("output_file", nargs="?", default=None, help="Fichero JSON de salida")
    parser.add_argument("profile_file", nargs="?", default="system-profile.json", help="Perfil del sistema")
    parser.add_argument("--verbose", action="store_true", help="Logging verboso a stderr")
    args = parser.parse_args(argv)
    _setup_logging(args.verbose)
    output_file = args.output_file or f"audit-full-{time.strftime('%Y%m%d-%H%M%S')}.json"
    profile_file = args.profile_file

    try:
        distro_family, pkg_mgr, distro_id, version_id, version_codename = load_profile_family(profile_file)
    except (OSError, ValueError) as exc:
        logger.error("no se pudo cargar perfil %r: %s", profile_file, exc)
        return 1

    collector = FindingCollector()
    add = collector.add

    print(f"{log_tag} Fase 1: Controles críticos (P0+P1)...")
    start_time = time.time()

    # --- PKG-01: Actualizaciones de seguridad ---
    print(f"{log_tag} Verificando actualizaciones de seguridad...")
    if pkg_mgr == "pacman":
        try:
            news_out = run("curl -s https://news.archlinux.org/index.xml 2>/dev/null", timeout=30)
            sec_pkg_names = set()
            if "<title>" in news_out and "</title>" in news_out:
                for m in re.finditer(r'<title>(.*?)</title>', news_out):
                    title = m.group(1).lower()
                    if any(w in title for w in ["security", "security update", "actualización de seguridad"]):
                        sec_pkg_names.add(m.group(1))
            pkg_updates = run("checkupdates 2>/dev/null", timeout=60)
            sec_updates = 0
            for pkg_line in pkg_updates.splitlines():
                pkg_name = pkg_line.split()[0] if pkg_line.split() else ""
                if pkg_name in sec_pkg_names or any(sn.lower().split(":")[-1].strip().lower() == pkg_name.lower() for sn in sec_pkg_names):
                    sec_updates += 1
        except (OSError, ValueError, re.error, subprocess.SubprocessError) as exc:
            logger.warning("fallo verificando updates pacman (se asume 0): %s", exc)
            sec_updates = 0
        if sec_updates > 0:
            add("PKG-01", "updates", "P1", f"{sec_updates} actualizaciones de seguridad pendientes", "Paquetes con actualizaciones de seguridad disponibles", "PKG-01", "FAIL", f"News check -> {sec_updates}", "Ejecutar pacman -Syu tras leer noticias Arch", "R2")
        else:
            add("PKG-01", "updates", "P1", "Sin actualizaciones de seguridad pendientes", "Sistema actualizado en seguridad", "PKG-01", "PASS", "0 actualizaciones de seguridad", "", "R0")
    elif pkg_mgr == "apt":
        # apt list imprime 1 línea de cabecera (Listing.../Listando...) que debe excluirse
        pkg_updates = run("apt list --upgradable 2>/dev/null | grep -vE '^(Listing|Listando)' ", timeout=60)
        sec_updates = count_nonempty(pkg_updates)
        if sec_updates > 0:
            add("PKG-01", "updates", "P1", f"{sec_updates} actualizaciones pendientes", "Actualizaciones disponibles", "PKG-01", "FAIL", f"apt list --upgradable -> {sec_updates}", "Ejecutar apt full-upgrade", "R2")
        else:
            add("PKG-01", "updates", "P1", "Sin actualizaciones pendientes", "Sistema actualizado", "PKG-01", "PASS", "0 actualizaciones", "", "R0")
    elif pkg_mgr == "dnf":
        sec_updates = to_int(run_check("dnf check-update --security 2>/dev/null | grep -cv '^$'", timeout=60))
        if sec_updates > 0:
            add("PKG-01", "updates", "P1", f"{sec_updates} actualizaciones de seguridad pendientes", "Paquetes con actualizaciones de seguridad disponibles", "PKG-01", "FAIL", f"dnf check-update --security -> {sec_updates}", "Ejecutar dnf upgrade --security", "R2")
        else:
            add("PKG-01", "updates", "P1", "Sin actualizaciones de seguridad pendientes", "Sistema actualizado en seguridad", "PKG-01", "PASS", "0 actualizaciones de seguridad", "", "R0")

    # --- PKG-03: Kernel running vs installed ---
    print(f"{log_tag} Verificando kernel running vs installed...")
    running_kernel = run("uname -r", timeout=5).strip()
    installed_kernel = ""
    if pkg_mgr == "pacman":
        for kernel_pkg in ("linux", "linux-lts", "linux-zen", "linux-hardened"):
            kv = run_check(f"pacman -Q {kernel_pkg} 2>/dev/null | awk '{{print $2}}'").strip()
            if kv:
                installed_kernel = kv
                break
        if not installed_kernel:
            installed_kernel = "unknown"
        running_base = running_kernel.split("-")[0] if "-" in running_kernel else running_kernel
        installed_base = installed_kernel.split("-")[0] if "-" in installed_kernel else installed_kernel
        if running_base != installed_base:
            add("PKG-03", "updates", "P1", f"Kernel running ({running_kernel}) != installed ({installed_kernel})", "Reinicio pendiente para cargar nuevo kernel", "PKG-03", "FAIL", f"uname -r: {running_kernel}, pacman -Q linux variants: {installed_kernel}", "Reiniciar sistema", "R2")
        else:
            add("PKG-03", "updates", "P1", "Kernel running coincide con instalado", "No hay reinicio pendiente de kernel", "PKG-03", "PASS", f"running: {running_kernel}, installed: {installed_kernel}", "", "R0")
    elif pkg_mgr == "apt":
        installed_kernel = run_check(
            "dpkg -l 'linux-image-*' 2>/dev/null | grep '^ii' | awk '{print $2}' "
            "| grep -E '^linux-image-[0-9]' | sed 's/linux-image-//' | sort -Vr | head -1"
        ).strip()
        if installed_kernel and running_kernel != installed_kernel:
            add("PKG-03", "updates", "P1", f"Kernel running ({running_kernel}) != latest installed ({installed_kernel})", "Reinicio pendiente", "PKG-03", "FAIL", f"running: {running_kernel}, installed: {installed_kernel}", "Reiniciar sistema", "R2")
        else:
            add("PKG-03", "updates", "P1", "Kernel running coincide con instalado", "No hay reinicio pendiente", "PKG-03", "PASS", f"running: {running_kernel}", "", "R0")
    elif pkg_mgr == "dnf":
        installed_kernel = run_check("rpm -q kernel 2>/dev/null | tail -1 | sed 's/kernel-//'").strip()
        if installed_kernel and running_kernel != installed_kernel:
            add("PKG-03", "updates", "P1", f"Kernel running ({running_kernel}) != latest installed ({installed_kernel})", "Reinicio pendiente", "PKG-03", "FAIL", f"running: {running_kernel}, installed: {installed_kernel}", "Reiniciar sistema", "R2")
        else:
            add("PKG-03", "updates", "P1", "Kernel running coincide con instalado", "No hay reinicio pendiente", "PKG-03", "PASS", f"running: {running_kernel}", "", "R0")

    # --- PKG-05: Paquetes huérfanos ---
    print(f"{log_tag} Verificando paquetes huérfanos...")
    if pkg_mgr == "pacman":
        orphans = run_check("pacman -Qtdq 2>/dev/null", timeout=60)
        orphan_count = count_nonempty(orphans)
        if orphan_count > 0:
            add("PKG-05", "hygiene", "P3", f"{orphan_count} paquetes huérfanos detectados", "Paquetes sin dependientes que pueden limpiarse", "PKG-05", "WARN", f"pacman -Qtdq -> {orphan_count} paquetes", "Revisar y eliminar con pacman -Rns $(pacman -Qtdq)", "R1")
        else:
            add("PKG-05", "hygiene", "P3", "Sin paquetes huérfanos", "Limpio", "PKG-05", "PASS", "0 huérfanos", "", "R0")
    elif pkg_mgr == "apt":
        orphans = run_check("apt autoremove --dry-run 2>/dev/null | grep '^Remv'", timeout=120)
        orphan_count = count_nonempty(orphans)
        if orphan_count > 0:
            add("PKG-05", "hygiene", "P3", f"{orphan_count} paquetes huérfanos detectados", "Paquetes instalados como dependencias ya no necesarios", "PKG-05", "WARN", f"apt autoremove --dry-run -> {orphan_count}", "Ejecutar apt autoremove --purge", "R1")
        else:
            add("PKG-05", "hygiene", "P3", "Sin paquetes huérfanos", "Limpio", "PKG-05", "PASS", "0 huérfanos", "", "R0")
    elif pkg_mgr == "dnf":
        orphans = run_check("dnf repoquery --unneeded 2>/dev/null", timeout=60)
        orphan_count = count_nonempty(orphans)
        if orphan_count > 0:
            add("PKG-05", "hygiene", "P3", f"{orphan_count} paquetes huérfanos detectados", "Paquetes sin dependientes", "PKG-05", "WARN", f"dnf repoquery --unneeded -> {orphan_count}", "Ejecutar dnf autoremove", "R1")
        else:
            add("PKG-05", "hygiene", "P3", "Sin paquetes huérfanos", "Limpio", "PKG-05", "PASS", "0 huérfanos", "", "R0")

    # --- PKG-07: Archivos de configuración pendientes ---
    print(f"{log_tag} Verificando archivos de configuración pendientes...")
    if pkg_mgr == "pacman":
        pending = run_check("find /etc -name '*.pacnew' -o -name '*.pacsave' 2>/dev/null", timeout=30)
        pending_count = count_nonempty(pending)
        if pending_count > 0:
            add("PKG-07", "hygiene", "P2", f"{pending_count} archivos .pacnew/.pacsave pendientes", "Configuraciones nuevas de paquetes no fusionadas", "PKG-07", "FAIL", f"find /etc -> {pending_count}", "Ejecutar pacdiff y fusionar cambios", "R2")
        else:
            add("PKG-07", "hygiene", "P2", "Sin archivos .pacnew/.pacsave pendientes", "Configuraciones al día", "PKG-07", "PASS", "0 pendientes", "", "R0")
    elif pkg_mgr == "apt":
        pending = run_check("find /etc -name '*.dpkg-new' -o -name '*.dpkg-old' -o -name '*.ucf-new' -o -name '*.ucf-old' 2>/dev/null", timeout=30)
        pending_count = count_nonempty(pending)
        if pending_count > 0:
            add("PKG-07", "hygiene", "P2", f"{pending_count} archivos .dpkg-* pendientes", "Configuraciones nuevas de paquetes no fusionadas", "PKG-07", "FAIL", f"find /etc -> {pending_count}", "Revisar con ucf o dpkg-reconfigure", "R2")
        else:
            add("PKG-07", "hygiene", "P2", "Sin archivos de configuración pendientes", "Configuraciones al día", "PKG-07", "PASS", "0 pendientes", "", "R0")
    elif pkg_mgr == "dnf":
        pending = run_check("find /etc -name '*.rpmnew' -o -name '*.rpmsave' 2>/dev/null", timeout=30)
        pending_count = count_nonempty(pending)
        if pending_count > 0:
            add("PKG-07", "hygiene", "P2", f"{pending_count} archivos .rpmnew/.rpmsave pendientes", "Configuraciones nuevas de paquetes no fusionadas", "PKG-07", "FAIL", f"find /etc -> {pending_count}", "Revisar con rpmconf", "R2")
        else:
            add("PKG-07", "hygiene", "P2", "Sin archivos de configuración pendientes", "Configuraciones al día", "PKG-07", "PASS", "0 pendientes", "", "R0")

    # --- ACC-01: SSH PermitRootLogin ---
    print(f"{log_tag} Verificando SSH PermitRootLogin...")
    ssh_root = sshd_eff_get("permitrootlogin")
    if ssh_root == "yes":
        add("ACC-01", "security", "P0", "SSH PermitRootLogin yes", "Root puede loguearse por SSH (crítico)", "ACC-01", "FAIL", "sshd -T -> yes", "Establecer PermitRootLogin no en /etc/ssh/sshd_config y recargar sshd", "R2")
    else:
        add("ACC-01", "security", "P0", "SSH PermitRootLogin no", "Root login deshabilitado correctamente", "ACC-01", "PASS", f"sshd -T -> {ssh_root}", "", "R0")

    # --- ACC-02: SSH PasswordAuthentication ---
    print(f"{log_tag} Verificando SSH PasswordAuthentication...")
    ssh_pass = sshd_eff_get("passwordauthentication")
    if ssh_pass == "yes":
        add("ACC-02", "security", "P0", "SSH PasswordAuthentication yes", "Autenticación por contraseña habilitada (crítico)", "ACC-02", "FAIL", "sshd -T -> yes", "Establecer PasswordAuthentication no en /etc/ssh/sshd_config y recargar sshd", "R2")
    else:
        add("ACC-02", "security", "P0", "SSH PasswordAuthentication no", "Solo autenticación por clave pública", "ACC-02", "PASS", f"sshd -T -> {ssh_pass}", "", "R0")

    # --- ACC-08: Usuarios con UID 0 ---
    print(f"{log_tag} Verificando usuarios con UID 0...")
    uid0_users = run_check("awk -F: '$3==0' /etc/passwd", timeout=10)
    uid0_count = count_nonempty(uid0_users)
    if uid0_count > 1:
        add("ACC-08", "security", "P0", f"{uid0_count} usuarios con UID 0 (solo root debería tenerlo)", "Cuentas adicionales con privilegios de root", "ACC-08", "FAIL", f"awk -F: '$3==0' /etc/passwd -> {uid0_count}", "Eliminar/cambiar UID de usuarios no-root", "R2")
    else:
        add("ACC-08", "security", "P0", "Solo root tiene UID 0", "Correcto", "ACC-08", "PASS", "1 usuario (root)", "", "R0")

    # --- NET-01: Firewall activo ---
    print(f"{log_tag} Verificando firewall...")
    fw_active = False
    fw_type = ""
    for name in ("ufw", "nftables", "iptables", "firewalld"):
        if service_active(name):
            fw_active, fw_type = True, name
            break
    if fw_active:
        add("NET-01", "security", "P0", f"Firewall activo ({fw_type})", "Firewall funcionando", "NET-01", "PASS", f"systemctl is-active {fw_type} -> active", "", "R0")
    else:
        add("NET-01", "security", "P0", "Firewall INACTIVO", "Sin firewall de red activo (crítico)", "NET-01", "FAIL", "systemctl is-active ufw/nftables/iptables/firewalld -> inactive", "Activar firewall: systemctl enable --now ufw/nftables/firewalld", "R2")

    # --- NET-04: SSH expuesto a Internet ---
    print(f"{log_tag} Verificando exposición SSH...")
    ssh_listening = run_check("ss -tuln 2>/dev/null | grep ':22 '", timeout=10)
    if ssh_listening.strip():
        if "0.0.0.0:22" in ssh_listening or ":::22" in ssh_listening:
            add("NET-04", "security", "P0", "SSH escuchando en todas las interfaces (0.0.0.0/::)", "SSH expuesto a Internet potencialmente", "NET-04", "WARN", f"ss -tuln -> {ssh_listening.strip()}", "Restringir SSH a interfaces internas o usar firewall", "R2")
        else:
            add("NET-04", "security", "P0", "SSH escuchando en interfaz específica", "No expuesto a todas las interfaces", "NET-04", "PASS", f"ss -tuln -> {ssh_listening.strip()}", "", "R0")
    else:
        add("NET-04", "security", "P0", "SSH no está escuchando en puerto 22", "Puerto SSH no estándar o servicio detenido", "NET-04", "PASS", "ss -tuln -> (none)", "", "R0")

    # --- FS-10: Uso de disco crítico ---
    print(f"{log_tag} Verificando uso de disco...")
    df_out = run_check("df -h -x tmpfs -x devtmpfs -x squashfs --output=source,target,pcent 2>/dev/null | tail -n +2", timeout=15)
    seen = set()
    for line in df_out.splitlines():
        parts = line.split()
        if len(parts) < 3:
            continue
        source = parts[0]
        if source in seen:
            continue
        seen.add(source)
        mountpoint = parts[1]
        use_pcent = parts[2].rstrip("%")
        if not use_pcent.isdigit():
            continue
        use_pcent_i = int(use_pcent)
        if use_pcent_i >= 90:
            add("FS-10", "resources", "P1", f"Disco {mountpoint} al {use_pcent_i}%", "Espacio crítico, riesgo de fallo", "FS-10", "FAIL", f"df -h {mountpoint} -> {use_pcent_i}%", "Limpiar espacio o expandir partición", "R2")
        elif use_pcent_i >= 80:
            add("FS-10", "resources", "P2", f"Disco {mountpoint} al {use_pcent_i}%", "Espacio bajo, planificar limpieza", "FS-10", "WARN", f"df -h {mountpoint} -> {use_pcent_i}%", "Ejecutar rutina de limpieza", "R1")
        else:
            add("FS-10", "resources", "P4", f"Disco {mountpoint} al {use_pcent_i}%", "Espacio adecuado", "FS-10", "PASS", f"df -h {mountpoint} -> {use_pcent_i}%", "", "R0")

    # --- LOG-06: Errores en journal 24h ---
    print(f"{log_tag} Verificando errores en journal...")
    journal_errors_emerg = to_int(run_check("journalctl -p emerg --since '24 hours ago' --no-pager 2>/dev/null | grep -c .", timeout=60))
    journal_errors_alert = to_int(run_check("journalctl -p alert --since '24 hours ago' --no-pager 2>/dev/null | grep -c .", timeout=60))
    journal_errors_crit = to_int(run_check("journalctl -p crit --since '24 hours ago' --no-pager 2>/dev/null | grep -c .", timeout=60))
    journal_errors_err = to_int(run_check("journalctl -p err --since '24 hours ago' --no-pager 2>/dev/null | grep -c .", timeout=60))
    journal_errors = journal_errors_emerg + journal_errors_alert + journal_errors_crit + journal_errors_err
    if journal_errors > 50:
        add("LOG-06", "security", "P2", f"{journal_errors} errores (prioridad 0-3) en últimas 24h", "Alto volumen de errores en logs", "LOG-06", "WARN", f"journalctl -p 0..3 --since '24h' -> {journal_errors} líneas", "Investigar errores recurrentes", "R0")
    elif journal_errors > 0:
        add("LOG-06", "security", "P3", f"{journal_errors} errores (prioridad 0-3) en últimas 24h", "Algunos errores en logs", "LOG-06", "PASS", f"journalctl -p 0..3 --since '24h' -> {journal_errors} líneas", "Monitorear", "R0")
    else:
        add("LOG-06", "security", "P4", "Sin errores críticos en journal 24h", "Logs limpios", "LOG-06", "PASS", "0 errores", "", "R0")

    # --- SRV-02: Servicios fallidos ---
    print(f"{log_tag} Verificando servicios fallidos...")
    failed_svcs = run_check("systemctl --failed --no-legend --no-pager 2>/dev/null", timeout=15)
    failed_count = count_nonempty(failed_svcs)
    if failed_count > 0:
        add("SRV-02", "resources", "P1", f"{failed_count} servicios systemd fallidos", "Servicios que no iniciaron correctamente", "SRV-02", "FAIL", f"systemctl --failed -> {failed_count}", "Investigar con systemctl status <servicio> y journalctl -u <servicio>", "R2")
    else:
        add("SRV-02", "resources", "P1", "Sin servicios fallidos", "Todos los servicios activos", "SRV-02", "PASS", "0 fallidos", "", "R0")

    # --- KER-01: ASLR ---
    print(f"{log_tag} Verificando ASLR...")
    aslr = sysctl_get("kernel.randomize_va_space")
    if aslr == "2":
        add("KER-01", "security", "P1", "ASLR activado (nivel 2 - full)", "Protección completa contra exploits de memoria", "KER-01", "PASS", "kernel.randomize_va_space = 2", "", "R0")
    else:
        add("KER-01", "security", "P1", f"ASLR no está en nivel 2 (actual: {aslr})", "Protección incompleta", "KER-01", "FAIL", f"kernel.randomize_va_space = {aslr}", "Establecer kernel.randomize_va_space=2 en /etc/sysctl.d/99-hardening.conf", "R2")

    # --- UA-02: Cuentas sin contraseña ---
    print(f"{log_tag} Verificando cuentas sin contraseña...")
    empty_pass = run_check("awk -F: '$2==\"\"' /etc/shadow 2>/dev/null", timeout=10)
    empty_count = count_nonempty(empty_pass)
    if empty_count > 0:
        add("UA-02", "security", "P0", f"{empty_count} cuentas sin contraseña", "Cuentas vulnerables a login sin credenciales", "UA-02", "FAIL", f"awk -F: '$2==\"\"' /etc/shadow -> {empty_count}", "Bloquear cuentas: passwd -l <user> o asignar contraseña", "R2")
    else:
        add("UA-02", "security", "P0", "Sin cuentas sin contraseña", "Todas las cuentas tienen contraseña o están bloqueadas", "UA-02", "PASS", "0 cuentas vacías", "", "R0")

    # --- CR-01: SSH host keys modernos ---
    print(f"{log_tag} Verificando SSH host keys...")
    weak_keys = run_check(
        "for k in /etc/ssh/ssh_host_*_key.pub; do ssh-keygen -lf \"$k\" 2>/dev/null; done "
        "| grep -vE 'ED25519|\\(RSA\\)' | grep -v '^$'",
        timeout=30,
    )
    if weak_keys.strip():
        add("CR-01", "security", "P1", "Claves SSH host débiles detectadas", "Algoritmos obsoletos (DSA, ECDSA débil, RSA SHA1)", "CR-01", "FAIL", "ssh-keygen -lf -> claves débiles encontradas", 'Regenerar claves: ssh-keygen -t ed25519 -f /etc/ssh/ssh_host_ed25519_key -N ""', "R2")
    else:
        add("CR-01", "security", "P1", "Claves SSH host modernas (ED25519, RSA-SHA2)", "Algoritmos criptográficos actuales", "CR-01", "PASS", "Todas las claves son ED25519 o RSA-SHA2", "", "R0")

    print(f"{log_tag} Fase 2: Controles extendidos (P2-P4)...")

    # --- SSH-03: PermitEmptyPasswords ---
    print(f"{log_tag} Verificando SSH PermitEmptyPasswords...")
    ssh_empty = sshd_eff_get("permitemptypasswords")
    if ssh_empty == "yes":
        add("SSH-03", "security", "P0", "SSH PermitEmptyPasswords yes", "Permite login sin contraseña (crítico)", "SSH-03", "FAIL", "sshd -T -> yes", "Establecer PermitEmptyPasswords no en /etc/ssh/sshd_config", "R2")
    else:
        add("SSH-03", "security", "P0", "SSH PermitEmptyPasswords no", "Correcto", "SSH-03", "PASS", f"sshd -T -> {ssh_empty}", "", "R0")

    # --- SSH-04: MaxAuthTries ---
    print(f"{log_tag} Verificando SSH MaxAuthTries...")
    ssh_maxauth = sshd_eff_get("maxauthtries")
    if ssh_maxauth and to_int(ssh_maxauth) > 4:
        add("SSH-04", "security", "P1", f"SSH MaxAuthTries {ssh_maxauth} (recomendado ≤ 4)", "Demasiados intentos de autenticación permitidos", "SSH-04", "FAIL", f"sshd -T -> {ssh_maxauth}", "Establecer MaxAuthTries 4 en /etc/ssh/sshd_config", "R2")
    else:
        add("SSH-04", "security", "P1", f"SSH MaxAuthTries correcto ({ssh_maxauth})", "Valor dentro del rango seguro", "SSH-04", "PASS", f"sshd -T -> {ssh_maxauth}", "", "R0")

    # --- SSH-05: ClientAliveInterval/CountMax ---
    print(f"{log_tag} Verificando SSH ClientAlive...")
    ssh_alive = sshd_eff_get("clientaliveinterval")
    if not ssh_alive or to_int(ssh_alive) == 0:
        add("SSH-05", "security", "P2", "SSH ClientAliveInterval no configurado", "Sesiones SSH pueden quedar huérfanas", "SSH-05", "WARN", f"sshd -T -> {ssh_alive}", "Establecer ClientAliveInterval 300 y ClientAliveCountMax 2", "R2")
    else:
        add("SSH-05", "security", "P2", f"SSH ClientAliveInterval configurado ({ssh_alive})", "Sesiones SSH con timeout", "SSH-05", "PASS", f"sshd -T -> {ssh_alive}", "", "R0")

    # --- SSH-06: AllowUsers/AllowGroups ---
    print(f"{log_tag} Verificando SSH AllowUsers/AllowGroups...")
    ssh_allow = sshd_eff_get("allowusers") or sshd_eff_get("allowgroups")
    if not ssh_allow:
        add("SSH-06", "security", "P2", "SSH sin AllowUsers/AllowGroups restrictivo", "Cualquier usuario puede conectarse por SSH", "SSH-06", "WARN", "sshd -T -> (none)", "Configurar AllowUsers o AllowGroups en /etc/ssh/sshd_config", "R2")
    else:
        add("SSH-06", "security", "P2", "SSH con AllowUsers/AllowGroups restrictivo", "Solo usuarios/grupos específicos pueden conectarse", "SSH-06", "PASS", f"sshd -T -> {ssh_allow}", "", "R0")

    # --- FW-02: Política por defecto deny ---
    print(f"{log_tag} Verificando política por defecto del firewall...")
    if fw_type == "ufw":
        fw_policy = run_check("sudo -n ufw status verbose 2>/dev/null | grep -iE 'Default:|Predeterminado:' | head -1", timeout=15).strip()
        if "deny" in fw_policy.lower() and ("incoming" in fw_policy.lower() or "entrantes" in fw_policy.lower()):
            add("FW-02", "security", "P1", "Firewall: política deny incoming correcta", "Política por defecto segura", "FW-02", "PASS", "ufw status -> deny incoming", "", "R0")
        else:
            add("FW-02", "security", "P1", "Firewall: política incoming no es deny", "Política por defecto insegura", "FW-02", "FAIL", f"ufw status -> {fw_policy}", "Establecer: ufw default deny incoming", "R2")
    elif fw_type == "nftables":
        fw_policy = run_check("nft list ruleset 2>/dev/null | grep 'policy' | head -1", timeout=15).strip()
        if "drop" in fw_policy.lower():
            add("FW-02", "security", "P1", "nftables: política drop correcta", "Política por defecto segura", "FW-02", "PASS", "nft list ruleset -> drop", "", "R0")
        else:
            add("FW-02", "security", "P1", "nftables: política no es drop", "Política por defecto insegura", "FW-02", "WARN", f"nft list ruleset -> {fw_policy}", "Establecer policy drop en chain input", "R2")
    elif fw_type == "firewalld":
        fw_policy = run_check("firewall-cmd --get-default-zone 2>/dev/null", timeout=15).strip()
        add("FW-02", "security", "P1", f"firewalld: zona por defecto {fw_policy}", "Verificar que la zona tenga política restrictiva", "FW-02", "PASS", f"firewall-cmd --get-default-zone -> {fw_policy}", "", "R0")
    else:
        add("FW-02", "security", "P1", "No se pudo verificar política firewall", "Firewall no detectado o tipo desconocido", "FW-02", "SKIP", f"fw_type={fw_type}", "", "R0")

    # --- FW-03: Puertos abiertos solo los necesarios ---
    print(f"{log_tag} Verificando puertos abiertos...")
    open_ports = run_check("ss -tuln 2>/dev/null | tail -n +2 | awk '{print $5}' | cut -d: -f2 | sort -nu | grep -v '^$'", timeout=15)
    open_port_count = count_nonempty(open_ports)
    if open_port_count > 10:
        add("FW-03", "security", "P1", f"{open_port_count} puertos TCP/UDP abiertos", "Muchos puertos abiertos, posible superficie de ataque amplia", "FW-03", "WARN", f"ss -tuln -> {open_port_count} puertos", "Revisar y cerrar puertos innecesarios", "R2")
    else:
        add("FW-03", "security", "P1", f"{open_port_count} puertos TCP/UDP abiertos", "Puertos abiertos dentro de rango aceptable", "FW-03", "PASS", f"ss -tuln -> {open_port_count} puertos", "", "R0")

    # --- FS-05: Archivos world-writable ---
    print(f"{log_tag} Verificando archivos world-writable...")
    ww_files = run_check(
        "find /home /opt /usr/local -xdev -type f -perm -0002 ! -path '/proc/*' ! -path '/sys/*' ! -path '/tmp/*' "
        "! -path '/var/tmp/*' ! -path '*/node_modules/*' ! -path '*/.bun/*' ! -path '*/share/bun/*' "
        "! -path '*/share/containers/storage/*' ! -path '*/share/uv/*' ! -path '*/cache/uv/*' "
        "! -path '*/venv*/.lock' ! -path '*/papelera-xdg/*' "
        "! -path '/snap/*' ! -path '*/.config/Proton Mail/*' ! -path '*/config/Proton Mail/*' "
        "! -path '*/config/Proton Pass/*' 2>/dev/null | head -20",
        timeout=120,
    )
    ww_count = count_nonempty(ww_files)
    if ww_count > 0:
        add("FS-05", "security", "P1", f"{ww_count} archivos world-writable detectados", "Archivos modificables por cualquier usuario", "FS-05", "FAIL", f"find / -perm -0002 -> {ww_count} archivos", "Eliminar permiso world-writable: chmod o-w <archivo>", "R2")
    else:
        add("FS-05", "security", "P1", "Sin archivos world-writable", "Correcto", "FS-05", "PASS", "0 archivos world-writable", "", "R0")

    # --- FS-06: Directorios world-writable sin sticky bit ---
    print(f"{log_tag} Verificando directorios world-writable sin sticky...")
    ww_dirs = run_check(
        "find /home /opt /usr/local -xdev -type d -perm -0002 ! -perm -1000 ! -path '/proc/*' ! -path '/sys/*' "
        "! -path '/tmp/*' ! -path '/var/tmp/*' ! -path '*/node_modules/*' ! -path '*/.bun/*' "
        "! -path '*/share/bun/*' ! -path '*/share/containers/storage/*' "
        "! -path '/snap/*' ! -path '*/.config/Proton Mail/*' 2>/dev/null | head -20",
        timeout=120,
    )
    ww_dir_count = count_nonempty(ww_dirs)
    if ww_dir_count > 0:
        add("FS-06", "security", "P1", f"{ww_dir_count} directorios world-writable sin sticky bit", "Directorios modificables por cualquier usuario sin protección", "FS-06", "FAIL", f"find / -type d -perm -0002 ! -perm -1000 -> {ww_dir_count}", "Añadir sticky bit: chmod +t <dir>", "R2")
    else:
        add("FS-06", "security", "P1", "Sin directorios world-writable sin sticky bit", "Correcto", "FS-06", "PASS", "0 directorios problemáticos", "", "R0")

    # --- FS-07: Archivos sin dueño ---
    print(f"{log_tag} Verificando archivos sin dueño...")
    noowner_files = run_check("find /home /opt /usr/local -xdev \\( -nouser -o -nogroup \\) ! -path '/proc/*' ! -path '/sys/*' ! -path '*/share/containers/storage/*' 2>/dev/null | head -20", timeout=120)
    noowner_count = count_nonempty(noowner_files)
    if noowner_count > 0:
        add("FS-07", "security", "P2", f"{noowner_count} archivos sin dueño válido", "Archivos con usuario/grupo inexistente", "FS-07", "WARN", f"find / -nouser -o -nogroup -> {noowner_count}", "Asignar dueño o eliminar archivos huérfanos", "R2")
    else:
        add("FS-07", "security", "P2", "Sin archivos sin dueño", "Todos los archivos tienen dueño válido", "FS-07", "PASS", "0 archivos sin dueño", "", "R0")

    # --- FS-08: SUID/SGID no documentados ---
    print(f"{log_tag} Verificando archivos SUID/SGID...")
    suid_files = run_check("find /home /opt /usr/local -xdev -type f \\( -perm -4000 -o -perm -2000 \\) 2>/dev/null | head -30", timeout=120)
    suid_count = count_nonempty(suid_files)
    if suid_count > 20:
        add("FS-08", "security", "P1", f"{suid_count} archivos SUID/SGID detectados", "Muchos binarios con privilegios elevados", "FS-08", "WARN", f"find / -perm -4000 -o -perm -2000 -> {suid_count}", "Auditar y eliminar SUID/SGID innecesarios", "R2")
    else:
        add("FS-08", "security", "P1", f"{suid_count} archivos SUID/SGID detectados", "Cantidad dentro de rango normal", "FS-08", "PASS", f"find / -perm -4000 -o -perm -2000 -> {suid_count}", "", "R0")

    # --- FS-09: Symlinks rotos ---
    print(f"{log_tag} Verificando symlinks rotos...")
    broken_symlinks = run_check("find /etc /usr /boot -xtype l 2>/dev/null | head -20", timeout=120)
    symlink_count = count_nonempty(broken_symlinks)
    if symlink_count > 0:
        add("FS-09", "hygiene", "P3", f"{symlink_count} symlinks rotos en /etc, /usr, /boot", "Enlaces simbólicos que apuntan a archivos inexistentes", "FS-09", "WARN", f"find /etc /usr /boot -xtype l -> {symlink_count}", "Investigar y eliminar symlinks rotos (no borrar ciegamente)", "R1")
    else:
        add("FS-09", "hygiene", "P3", "Sin symlinks rotos", "Correcto", "FS-09", "PASS", "0 symlinks rotos", "", "R0")

    # --- AU-01: auditd activo ---
    print(f"{log_tag} Verificando auditd...")
    if service_active("auditd"):
        auditd_rules = to_int(run_check("sudo -n auditctl -l 2>/dev/null | grep -c .", timeout=15))
        if auditd_rules > 0:
            add("AU-01", "security", "P1", f"auditd activo con {auditd_rules} reglas", "Auditoría del sistema funcionando", "AU-01", "PASS", f"auditctl -l -> {auditd_rules} reglas", "", "R0")
        else:
            add("AU-01", "security", "P1", "auditd activo sin reglas", "auditd está activo pero sin reglas configuradas", "AU-01", "WARN", "auditctl -l -> 0 reglas", "Configurar reglas auditd en /etc/audit/rules.d/", "R2")
    else:
        add("AU-01", "security", "P1", "auditd INACTIVO", "Sin auditoría del sistema activa", "AU-01", "FAIL", "systemctl is-active auditd -> inactive", "Instalar y activar: pacman -S audit && systemctl enable --now auditd", "R2")

    # --- AU-11: systemd-journald persistent ---
    print(f"{log_tag} Verificando systemd-journald...")
    journal_storage = run_check("grep '^Storage=' /etc/systemd/journald.conf 2>/dev/null | cut -d= -f2", timeout=10).strip()
    if journal_storage == "persistent":
        add("AU-11", "security", "P1", "systemd-journald: Storage=persistent", "Logs persistentes entre reinicios", "AU-11", "PASS", "Storage=persistent", "", "R0")
    else:
        add("AU-11", "security", "P1", "systemd-journald: Storage no es persistent", "Logs se pierden entre reinicios", "AU-11", "FAIL", f"Storage={journal_storage}", "Establecer Storage=persistent en /etc/systemd/journald.conf", "R2")

    # --- KR-02: dmesg_restrict ---
    print(f"{log_tag} Verificando kernel.dmesg_restrict...")
    dmesg_restrict = sysctl_get("kernel.dmesg_restrict")
    if dmesg_restrict == "1":
        add("KR-02", "security", "P2", "kernel.dmesg_restrict=1", "Restricción de dmesg para no-root", "KR-02", "PASS", "kernel.dmesg_restrict = 1", "", "R0")
    else:
        add("KR-02", "security", "P2", f"kernel.dmesg_restrict={dmesg_restrict} (recomendado 1)", "Usuarios no-root pueden leer dmesg", "KR-02", "FAIL", f"kernel.dmesg_restrict = {dmesg_restrict}", "Establecer kernel.dmesg_restrict=1 en /etc/sysctl.d/99-hardening.conf", "R2")

    # --- KR-03: kptr_restrict ---
    print(f"{log_tag} Verificando kernel.kptr_restrict...")
    kptr = sysctl_get("kernel.kptr_restrict")
    if kptr == "2":
        add("KR-03", "security", "P2", "kernel.kptr_restrict=2", "Punteros kernel ocultos para no-root", "KR-03", "PASS", "kernel.kptr_restrict = 2", "", "R0")
    else:
        add("KR-03", "security", "P2", f"kernel.kptr_restrict={kptr} (recomendado 2)", "Punteros kernel visibles", "KR-03", "FAIL", f"kernel.kptr_restrict = {kptr}", "Establecer kernel.kptr_restrict=2 en /etc/sysctl.d/99-hardening.conf", "R2")

    # --- KR-22: TCP syncookies ---
    print(f"{log_tag} Verificando TCP syncookies...")
    syncookies = sysctl_get("net.ipv4.tcp_syncookies")
    if syncookies == "1":
        add("KR-22", "security", "P1", "net.ipv4.tcp_syncookies=1", "Protección contra SYN flood activa", "KR-22", "PASS", "net.ipv4.tcp_syncookies = 1", "", "R0")
    else:
        add("KR-22", "security", "P1", f"net.ipv4.tcp_syncookies={syncookies} (recomendado 1)", "Sin protección contra SYN flood", "KR-22", "FAIL", f"net.ipv4.tcp_syncookies = {syncookies}", "Establecer net.ipv4.tcp_syncookies=1 en /etc/sysctl.d/99-hardening.conf", "R2")

    # --- KR-27: suid_dumpable ---
    print(f"{log_tag} Verificando fs.suid_dumpable...")
    suid_dump = sysctl_get("fs.suid_dumpable")
    if suid_dump == "0":
        add("KR-27", "security", "P1", "fs.suid_dumpable=0", "Core dumps SUID deshabilitados", "KR-27", "PASS", "fs.suid_dumpable = 0", "", "R0")
    else:
        add("KR-27", "security", "P1", f"fs.suid_dumpable={suid_dump} (recomendado 0)", "Core dumps SUID habilitados", "KR-27", "FAIL", f"fs.suid_dumpable = {suid_dump}", "Establecer fs.suid_dumpable=0 en /etc/sysctl.d/99-hardening.conf", "R2")

    # --- KR-28: protected_hardlinks ---
    print(f"{log_tag} Verificando fs.protected_hardlinks...")
    prot_hard = sysctl_get("fs.protected_hardlinks")
    if prot_hard == "1":
        add("KR-28", "security", "P1", "fs.protected_hardlinks=1", "Protección de hardlinks activa", "KR-28", "PASS", "fs.protected_hardlinks = 1", "", "R0")
    else:
        add("KR-28", "security", "P1", f"fs.protected_hardlinks={prot_hard} (recomendado 1)", "Sin protección de hardlinks", "KR-28", "FAIL", f"fs.protected_hardlinks = {prot_hard}", "Establecer fs.protected_hardlinks=1 en /etc/sysctl.d/99-hardening.conf", "R2")

    # --- KR-29: protected_symlinks ---
    print(f"{log_tag} Verificando fs.protected_symlinks...")
    prot_sym = sysctl_get("fs.protected_symlinks")
    if prot_sym == "1":
        add("KR-29", "security", "P1", "fs.protected_symlinks=1", "Protección de symlinks activa", "KR-29", "PASS", "fs.protected_symlinks = 1", "", "R0")
    else:
        add("KR-29", "security", "P1", f"fs.protected_symlinks={prot_sym} (recomendado 1)", "Sin protección de symlinks", "KR-29", "FAIL", f"fs.protected_symlinks = {prot_sym}", "Establecer fs.protected_symlinks=1 en /etc/sysctl.d/99-hardening.conf", "R2")

    # --- UA-03: Contraseñas con expiración ---
    print(f"{log_tag} Verificando políticas de contraseña...")
    pw_maxage = run_check("grep '^PASS_MAX_DAYS' /etc/login.defs 2>/dev/null | awk '{print $2}'", timeout=10).strip()
    if pw_maxage and to_int(pw_maxage) <= 90:
        add("UA-03", "security", "P2", f"PASS_MAX_DAYS={pw_maxage} (≤ 90)", "Política de expiración de contraseña correcta", "UA-03", "PASS", f"PASS_MAX_DAYS = {pw_maxage}", "", "R0")
    else:
        add("UA-03", "security", "P2", f"PASS_MAX_DAYS={pw_maxage} (recomendado ≤ 90)", "Contraseñas no expiran o expiran muy tarde", "UA-03", "WARN", f"PASS_MAX_DAYS = {pw_maxage}", "Establecer PASS_MAX_DAYS 90 en /etc/login.defs", "R2")

    # --- UA-09: Umask por defecto ---
    print(f"{log_tag} Verificando umask por defecto...")
    umask_val = run_check("grep '^UMASK' /etc/login.defs 2>/dev/null | awk '{print $2}'", timeout=10).strip()
    if umask_val in ("027", "077"):
        add("UA-09", "security", "P2", f"UMASK={umask_val}", "Umask restrictivo configurado", "UA-09", "PASS", f"UMASK = {umask_val}", "", "R0")
    else:
        add("UA-09", "security", "P2", f"UMASK={umask_val} (recomendado 027 o 077)", "Umask permisivo", "UA-09", "WARN", f"UMASK = {umask_val}", "Establecer UMASK 027 en /etc/login.defs", "R2")

    # --- SRV-01: Servicios innecesarios ---
    print(f"{log_tag} Verificando servicios innecesarios...")
    unnecessary = [svc for svc in ("cups", "avahi-daemon", "bluetooth", "ModemManager") if service_active(svc)]
    if unnecessary:
        add("SRV-01", "resources", "P2", "Servicios potencialmente innecesarios activos: " + " ".join(unnecessary), "Servicios que pueden no ser necesarios", "SRV-01", "WARN", "systemctl is-active -> " + " ".join(unnecessary), "Evaluar y deshabilitar si no se necesitan: systemctl disable --now <servicio>", "R2")
    else:
        add("SRV-01", "resources", "P2", "Sin servicios innecesarios detectados", "Solo servicios esenciales activos", "SRV-01", "PASS", "0 servicios innecesarios", "", "R0")

    # --- PKG-06: Paquetes foráneos ---
    print(f"{log_tag} Verificando paquetes foráneos...")
    if pkg_mgr == "pacman":
        foreign = run_check("pacman -Qmq 2>/dev/null", timeout=60)
        foreign_count = count_nonempty(foreign)
        if foreign_count > 20:
            add("PKG-06", "hygiene", "P3", f"{foreign_count} paquetes foráneos (AUR/manuales)", "Muchos paquetes fuera de repositorios oficiales", "PKG-06", "WARN", f"pacman -Qmq -> {foreign_count}", "Revisar y limitar paquetes AUR/manuales", "R1")
        else:
            add("PKG-06", "hygiene", "P3", f"{foreign_count} paquetes foráneos (AUR/manuales)", "Cantidad dentro de rango aceptable", "PKG-06", "PASS", f"pacman -Qmq -> {foreign_count}", "", "R0")
    elif pkg_mgr == "apt":
        foreign = run_check("apt list --manual-installed 2>/dev/null | tail -n +2", timeout=60)
        foreign_count = count_nonempty(foreign)
        if foreign_count > 50:
            add("PKG-06", "hygiene", "P3", f"{foreign_count} paquetes instalados manualmente", "Muchos paquetes manuales", "PKG-06", "WARN", f"apt list --manual-installed -> {foreign_count}", "Revisar paquetes manuales innecesarios", "R1")
        else:
            add("PKG-06", "hygiene", "P3", f"{foreign_count} paquetes instalados manualmente", "Cantidad dentro de rango aceptable", "PKG-06", "PASS", f"apt list --manual-installed -> {foreign_count}", "", "R0")
    elif pkg_mgr == "dnf":
        foreign = run_check("dnf list extras 2>/dev/null | tail -n +2", timeout=60)
        foreign_count = count_nonempty(foreign)
        if foreign_count > 50:
            add("PKG-06", "hygiene", "P3", f"{foreign_count} paquetes extras", "Muchos paquetes fuera de grupos estándar", "PKG-06", "WARN", f"dnf list extras -> {foreign_count}", "Revisar paquetes extras innecesarios", "R1")
        else:
            add("PKG-06", "hygiene", "P3", f"{foreign_count} paquetes extras", "Cantidad dentro de rango aceptable", "PKG-06", "PASS", f"dnf list extras -> {foreign_count}", "", "R0")

    # --- PKG-09: Tamaño caché paquetes ---
    print(f"{log_tag} Verificando tamaño de caché...")
    if pkg_mgr == "pacman":
        cache_size = to_int(run_check("du -sm /var/cache/pacman/pkg 2>/dev/null | cut -f1", timeout=30))
        if cache_size > 2000:
            add("PKG-09", "hygiene", "P4", f"Caché pacman: {cache_size}MB (> 2GB)", "Caché de paquetes muy grande", "PKG-09", "WARN", f"du -sm /var/cache/pacman/pkg -> {cache_size}MB", "Limpiar caché: paccache -r -k 3", "R1")
        else:
            add("PKG-09", "hygiene", "P4", f"Caché pacman: {cache_size}MB", "Tamaño de caché aceptable", "PKG-09", "PASS", f"du -sm /var/cache/pacman/pkg -> {cache_size}MB", "", "R0")
    elif pkg_mgr == "apt":
        cache_size = to_int(run_check("du -sm /var/cache/apt/archives 2>/dev/null | cut -f1", timeout=30))
        if cache_size > 1000:
            add("PKG-09", "hygiene", "P4", f"Caché apt: {cache_size}MB (> 1GB)", "Caché de paquetes muy grande", "PKG-09", "WARN", f"du -sm /var/cache/apt/archives -> {cache_size}MB", "Limpiar caché: apt autoclean", "R1")
        else:
            add("PKG-09", "hygiene", "P4", f"Caché apt: {cache_size}MB", "Tamaño de caché aceptable", "PKG-09", "PASS", f"du -sm /var/cache/apt/archives -> {cache_size}MB", "", "R0")
    elif pkg_mgr == "dnf":
        cache_size = to_int(run_check("du -sm /var/cache/dnf 2>/dev/null | cut -f1", timeout=30))
        if cache_size > 1000:
            add("PKG-09", "hygiene", "P4", f"Caché dnf: {cache_size}MB (> 1GB)", "Caché de paquetes muy grande", "PKG-09", "WARN", f"du -sm /var/cache/dnf -> {cache_size}MB", "Limpiar caché: dnf clean packages", "R1")
        else:
            add("PKG-09", "hygiene", "P4", f"Caché dnf: {cache_size}MB", "Tamaño de caché aceptable", "PKG-09", "PASS", f"du -sm /var/cache/dnf -> {cache_size}MB", "", "R0")

    # --- LOG-08: Fallos de arranque ---
    print(f"{log_tag} Verificando fallos de arranque...")
    boot_failures_emerg = to_int(run_check("journalctl -b -p emerg --no-pager 2>/dev/null | grep -c .", timeout=60))
    boot_failures_alert = to_int(run_check("journalctl -b -p alert --no-pager 2>/dev/null | grep -c .", timeout=60))
    boot_failures_crit = to_int(run_check("journalctl -b -p crit --no-pager 2>/dev/null | grep -c .", timeout=60))
    boot_failures_err = to_int(run_check("journalctl -b -p err --no-pager 2>/dev/null | grep -c .", timeout=60))
    boot_failures = boot_failures_emerg + boot_failures_alert + boot_failures_crit + boot_failures_err
    if boot_failures > 20:
        add("LOG-08", "security", "P2", f"{boot_failures} errores en arranque actual", "Muchos errores durante el arranque", "LOG-08", "WARN", f"journalctl -b -p 0..3 -> {boot_failures} líneas", "Investigar errores de arranque con journalctl -b", "R0")
    elif boot_failures > 0:
        add("LOG-08", "security", "P3", f"{boot_failures} errores en arranque actual", "Algunos errores durante el arranque", "LOG-08", "PASS", f"journalctl -b -p 0..3 -> {boot_failures} líneas", "Monitorear", "R0")
    else:
        add("LOG-08", "security", "P4", "Sin errores en arranque actual", "Arranque limpio", "LOG-08", "PASS", "0 errores", "", "R0")

    # --- NET-05: Servicios escuchando en 0.0.0.0 ---
    print(f"{log_tag} Verificando servicios en 0.0.0.0...")
    listening_all = run_check("ss -tuln 2>/dev/null | grep '0.0.0.0:' | grep -v '0.0.0.0:22' | head -10", timeout=15)
    listening_all_count = count_nonempty(listening_all)
    if listening_all_count > 5:
        add("NET-05", "security", "P2", f"{listening_all_count} servicios escuchando en 0.0.0.0", "Muchos servicios expuestos a todas las interfaces", "NET-05", "WARN", f"ss -tuln | grep 0.0.0.0 -> {listening_all_count}", "Restringir servicios a interfaces específicas", "R2")
    else:
        add("NET-05", "security", "P2", f"{listening_all_count} servicios escuchando en 0.0.0.0", "Pocos servicios expuestos a todas las interfaces", "NET-05", "PASS", f"ss -tuln | grep 0.0.0.0 -> {listening_all_count}", "", "R0")

    # --- FS-11: Inodos ---
    print(f"{log_tag} Verificando uso de inodos...")
    inode_out = run_check("df -i / /boot /var /home 2>/dev/null | tail -n +2", timeout=15)
    for line in inode_out.splitlines():
        parts = line.split()
        if len(parts) < 6:
            continue
        mountpoint = parts[5]
        inode_pcent = parts[4].rstrip("%")
        if not inode_pcent.isdigit():
            continue
        inode_pcent_i = int(inode_pcent)
        if inode_pcent_i >= 90:
            add("FS-11", "resources", "P2", f"Inodos {mountpoint} al {inode_pcent_i}%", "Inodos casi agotados", "FS-11", "FAIL", f"df -i {mountpoint} -> {inode_pcent_i}%", "Eliminar archivos pequeños innecesarios", "R2")
        elif inode_pcent_i >= 80:
            add("FS-11", "resources", "P3", f"Inodos {mountpoint} al {inode_pcent_i}%", "Uso de inodos elevado", "FS-11", "WARN", f"df -i {mountpoint} -> {inode_pcent_i}%", "Monitorear uso de inodos", "R1")

    # --- PKG-04: Firmware actualizable ---
    print(f"{log_tag} Verificando firmware...")
    if which("fwupdmgr"):
        fw_updates = to_int(run_check("fwupdmgr get-updates 2>/dev/null | grep -c 'Device:'", timeout=60))
        if fw_updates > 0:
            add("PKG-04", "updates", "P2", f"{fw_updates} actualizaciones de firmware disponibles", "Dispositivos con firmware actualizable", "PKG-04", "WARN", f"fwupdmgr get-updates -> {fw_updates} dispositivos", "Ejecutar: fwupdmgr update", "R2")
        else:
            add("PKG-04", "updates", "P2", "Sin actualizaciones de firmware", "Firmware al día", "PKG-04", "PASS", "0 actualizaciones", "", "R0")
    else:
        add("PKG-04", "updates", "P2", "fwupd no instalado", "No se puede verificar firmware", "PKG-04", "SKIP", "fwupdmgr no encontrado", "Instalar fwupd para verificar firmware", "R0")

    # --- ARC-07 / DEB-02 / RHEL-05: Actualización parcial ---
    print(f"{log_tag} Verificando actualizaciones parciales...")
    if pkg_mgr == "pacman":
        partial_update = run_check("grep 'pacman -Sy$' /var/log/pacman.log 2>/dev/null | tail -5", timeout=30)
        partial_count = count_nonempty(partial_update)
        if partial_count > 0:
            add("ARC-07", "updates", "P1", "Actualizaciones parciales detectadas en log", "Se detectó 'pacman -Sy' sin '-u' (actualización parcial peligrosa)", "ARC-07", "WARN", f"grep 'pacman -Sy$' /var/log/pacman.log -> {partial_count}", "Usar siempre 'pacman -Syu' para actualizaciones completas", "R2")
        else:
            add("ARC-07", "updates", "P1", "Sin actualizaciones parciales detectadas", "Correcto", "ARC-07", "PASS", "0 actualizaciones parciales", "", "R0")
    else:
        add("ARC-07", "updates", "P4", "Verificación de actualizaciones parciales N/A", "Solo aplicable a Arch Linux", "ARC-07", "SKIP", f"PKG_MGR={pkg_mgr}", "", "R0")

    # --- DEB-04: unattended-upgrades ---
    if pkg_mgr == "apt":
        print(f"{log_tag} Verificando unattended-upgrades...")
        if service_active("unattended-upgrades"):
            add("DEB-04", "updates", "P2", "unattended-upgrades activo", "Actualizaciones automáticas de seguridad habilitadas", "DEB-04", "PASS", "systemctl is-active unattended-upgrades -> active", "", "R0")
        else:
            add("DEB-04", "updates", "P2", "unattended-upgrades INACTIVO", "Sin actualizaciones automáticas de seguridad", "DEB-04", "WARN", "systemctl is-active unattended-upgrades -> inactive", "Activar: systemctl enable --now unattended-upgrades", "R2")

    # --- RHEL-03: SELinux ---
    if pkg_mgr == "dnf":
        print(f"{log_tag} Verificando SELinux...")
        selinux_status = run_check("getenforce 2>/dev/null", timeout=10).strip()
        if selinux_status == "Enforcing":
            add("RHEL-03", "security", "P0", "SELinux Enforcing", "SELinux en modo enforcing", "RHEL-03", "PASS", "getenforce -> Enforcing", "", "R0")
        else:
            add("RHEL-03", "security", "P0", f"SELinux {selinux_status} (recomendado Enforcing)", "SELinux no está enforcing", "RHEL-03", "FAIL", f"getenforce -> {selinux_status}", "Establecer SELINUX=enforcing en /etc/selinux/config", "R2")

    # --- LYNIS-01: integración con Lynis ---
    if which("lynis"):
        print(f"{log_tag} Fase 3: Ejecutando Lynis...")
        base = output_file.removesuffix(".json")
        run(f"lynis audit system --quick --no-log --report-file {base}-lynis.dat 2>/dev/null", timeout=600)
        dat_file = f"{base}-lynis.dat"
        if os.path.isfile(dat_file):
            dat = run(f"cat {dat_file}", timeout=10)
            lynis_warnings = dat.count("warning=")
            lynis_suggestions = dat.count("suggestion=")
            add("LYNIS-01", "security", "P2", f"Lynis: {lynis_warnings} warnings, {lynis_suggestions} suggestions", "Auditoría Lynis completada", "LYNIS-01", "PASS", f"lynis audit system -> warnings={lynis_warnings}, suggestions={lynis_suggestions}", f"Revisar informe Lynis: {dat_file}", "R0")
    else:
        print(f"{log_tag} Fase 3: Lynis no disponible (instalar para auditoría adicional)")

    duration = int(time.time() - start_time)

    try:
        output = collector.build_output("audit-full", distro_id, distro_family, running_kernel, duration, version_id, version_codename)
    except (ValueError, TypeError, OSError) as exc:
        logger.error("no se pudo construir salida de auditoría: %s", exc)
        return 1
    try:
        with open(output_file, "w", encoding="utf-8") as fh:
            json.dump(output, fh, indent=2, ensure_ascii=False)
            fh.write("\n")
    except (OSError, TypeError, ValueError) as exc:
        logger.error("no se pudo escribir %r: %s", output_file, exc)
        print(f"Error: no se pudo escribir {output_file}: {exc}", file=sys.stderr)
        return 1

    hs = output["health_score"]
    print(f"{log_tag} Auditoría completada en {duration}s")
    print(f"{log_tag} Health Score: {hs['overall']} (Security: {hs['security']}, Updates: {hs['updates']}, Hygiene: {hs['hygiene']}, Resources: {hs['resources']})")
    print(f"{log_tag} Resultados: {collector.passed} passed, {collector.failed} failed, {collector.warned} warned, {collector.skipped} skipped, {collector.errors} errors")
    print(f"{log_tag} Guardado en: {output_file}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
