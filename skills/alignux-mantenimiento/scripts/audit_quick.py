#!/usr/bin/env python3
"""audit_quick.py - Health-check read-only (controles P0+P1).

Port Python de audit_quick.sh. Ejecuta controles P0+P1 críticos y genera
salida JSON con Health Score. Uso: audit_quick.py [output-file] [profile-file]
"""

from __future__ import annotations

import argparse
import json
import logging
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
    sysctl_get,
    to_int,
)

logger = logging.getLogger("mantenimiento.audit_quick")


def _setup_logging(verbose: bool = False) -> None:
    level = logging.DEBUG if verbose else logging.WARNING
    if not logging.getLogger().handlers:
        logging.basicConfig(level=level, format="%(levelname)s: %(message)s", stream=sys.stderr)
    else:
        logging.getLogger().setLevel(level)

log_tag = color("[AUDIT-QUICK]", BLUE)


def run_check(cmd: str, timeout: int = 10) -> str:
    return run(cmd, timeout=timeout)


def sshd_value(key: str) -> str:
    out = run(f"sshd -T 2>/dev/null | grep '^{key} ' | awk '{{print $2}}'", timeout=10)
    return out.strip()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Health-check read-only (controles P0+P1).")
    parser.add_argument("output_file", nargs="?", default=None, help="Fichero JSON de salida")
    parser.add_argument("profile_file", nargs="?", default="system-profile.json", help="Perfil del sistema")
    parser.add_argument("--verbose", action="store_true", help="Logging verboso a stderr")
    args = parser.parse_args(argv)
    _setup_logging(args.verbose)
    output_file = args.output_file or f"audit-quick-{time.strftime('%Y%m%d-%H%M%S')}.json"
    profile_file = args.profile_file

    try:
        distro_family, pkg_mgr, distro_id, version_id, version_codename = load_profile_family(profile_file)
    except (OSError, ValueError) as exc:
        logger.error("no se pudo cargar perfil %r: %s", profile_file, exc)
        return 1

    collector = FindingCollector()
    add = collector.add

    print(f"{log_tag} Iniciando auditoría rápida (controles P0+P1)...")
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
        evidence = f"News check -> {sec_updates}"
        if sec_updates > 0:
            add("PKG-01", "updates", "P1", f"{sec_updates} actualizaciones de seguridad pendientes", "Paquetes con actualizaciones de seguridad disponibles", "PKG-01", "FAIL", evidence, "Ejecutar pacman -Syu tras leer noticias Arch", "R2")
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
        sec_updates = to_int(run_check("dnf check-update --security 2>/dev/null | grep -v '^$' | wc -l", timeout=60))
        if sec_updates > 0:
            add("PKG-01", "updates", "P1", f"{sec_updates} actualizaciones de seguridad pendientes", "Paquetes con actualizaciones de seguridad disponibles", "PKG-01", "FAIL", f"dnf check-update --security -> {sec_updates}", "Ejecutar dnf upgrade --security", "R2")
        else:
            add("PKG-01", "updates", "P1", "Sin actualizaciones de seguridad pendientes", "Sistema actualizado en seguridad", "PKG-01", "PASS", "0 actualizaciones de seguridad", "", "R0")

    # --- PKG-03: Kernel running vs installed ---
    print(f"{log_tag} Verificando kernel running vs installed...")
    running_kernel = run("uname -r", timeout=5).strip()
    installed_kernel = ""
    if pkg_mgr == "pacman":
        installed_kernel = run_check("pacman -Q linux 2>/dev/null | awk '{print $2}'").strip()
        if running_kernel != f"{installed_kernel}-arch" and running_kernel != installed_kernel:
            add("PKG-03", "updates", "P1", f"Kernel running ({running_kernel}) != installed ({installed_kernel})", "Reinicio pendiente para cargar nuevo kernel", "PKG-03", "FAIL", f"uname -r: {running_kernel}, pacman -Q linux: {installed_kernel}", "Reiniciar sistema", "R2")
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
            add("PKG-07", "hygiene", "P2", f"{pending_count} archivos .pacnew/.pacsave pendientes", "Configuraciones nuevas de paquetes no fusionadas", "PKG-07", "FAIL", f"find /etc -name '*.pacnew' -o -name '*.pacsave' -> {pending_count}", "Ejecutar pacdiff y fusionar cambios", "R2")
        else:
            add("PKG-07", "hygiene", "P2", "Sin archivos .pacnew/.pacsave pendientes", "Configuraciones al día", "PKG-07", "PASS", "0 pendientes", "", "R0")
    elif pkg_mgr == "apt":
        pending = run_check("find /etc -name '*.dpkg-new' -o -name '*.dpkg-old' -o -name '*.ucf-new' -o -name '*.ucf-old' 2>/dev/null", timeout=30)
        pending_count = count_nonempty(pending)
        if pending_count > 0:
            add("PKG-07", "hygiene", "P2", f"{pending_count} archivos .dpkg-new/.dpkg-old/.ucf-* pendientes", "Configuraciones nuevas de paquetes no fusionadas", "PKG-07", "FAIL", f"find /etc -> {pending_count}", "Revisar con ucf o dpkg-reconfigure", "R2")
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
    ssh_root = sshd_value("permitrootlogin")
    if ssh_root == "yes":
        add("ACC-01", "security", "P0", "SSH PermitRootLogin yes", "Root puede loguearse por SSH (crítico)", "ACC-01", "FAIL", "sshd -T | grep permitrootlogin -> yes", "Establecer PermitRootLogin no en /etc/ssh/sshd_config y recargar sshd", "R2")
    else:
        add("ACC-01", "security", "P0", "SSH PermitRootLogin no", "Root login deshabilitado correctamente", "ACC-01", "PASS", f"sshd -T | grep permitrootlogin -> {ssh_root}", "", "R0")

    # --- ACC-02: SSH PasswordAuthentication ---
    print(f"{log_tag} Verificando SSH PasswordAuthentication...")
    ssh_pass = sshd_value("passwordauthentication")
    if ssh_pass == "yes":
        add("ACC-02", "security", "P0", "SSH PasswordAuthentication yes", "Autenticación por contraseña habilitada (crítico)", "ACC-02", "FAIL", "sshd -T | grep passwordauthentication -> yes", "Establecer PasswordAuthentication no en /etc/ssh/sshd_config y recargar sshd", "R2")
    else:
        add("ACC-02", "security", "P0", "SSH PasswordAuthentication no", "Solo autenticación por clave pública", "ACC-02", "PASS", f"sshd -T | grep passwordauthentication -> {ssh_pass}", "", "R0")

    # --- ACC-08: Usuarios con UID 0 ---
    print(f"{log_tag} Verificando usuarios con UID 0...")
    uid0_users = run_check("awk -F: '$3==0' /etc/passwd", timeout=10)
    uid0_count = count_nonempty(uid0_users)
    if uid0_count > 1:
        add("ACC-08", "security", "P0", f"{uid0_count} usuarios con UID 0 (solo root debería tenerlo)", "Cuentas adicionales con privilegios de root", "ACC-08", "FAIL", f"awk -F: '$3==0' /etc/passwd -> {uid0_count} usuarios", "Eliminar/cambiar UID de usuarios no-root", "R2")
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
            add("NET-04", "security", "P0", "SSH escuchando en todas las interfaces (0.0.0.0/::)", "SSH expuesto a Internet potencialmente", "NET-04", "WARN", f"ss -tuln | grep :22 -> {ssh_listening.strip()}", "Restringir SSH a interfaces internas o usar firewall", "R2")
        else:
            add("NET-04", "security", "P0", "SSH escuchando en interfaz específica", "No expuesto a todas las interfaces", "NET-04", "PASS", f"ss -tuln | grep :22 -> {ssh_listening.strip()}", "", "R0")
    else:
        add("NET-04", "security", "P0", "SSH no está escuchando en puerto 22", "Puerto SSH no estándar o servicio detenido", "NET-04", "PASS", "ss -tuln | grep :22 -> (none)", "", "R0")

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
        add("SRV-02", "resources", "P1", f"{failed_count} servicios systemd fallidos", "Servicios que no iniciaron correctamente — riesgo de disponibilidad", "SRV-02", "FAIL", f"systemctl --failed -> {failed_count}", "Investigar con systemctl status <servicio> y journalctl -u <servicio>", "R2")
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
        add("CR-01", "security", "P1", "Claves SSH host débiles detectadas", "Algoritmos obsoletos (DSA, ECDSA débil, RSA SHA1)", "CR-01", "FAIL", "ssh-keygen -lf /etc/ssh/ssh_host_*_key.pub -> claves débiles encontradas", 'Regenerar claves: ssh-keygen -t ed25519 -f /etc/ssh/ssh_host_ed25519_key -N ""', "R2")
    else:
        add("CR-01", "security", "P1", "Claves SSH host modernas (ED25519, RSA-SHA2)", "Algoritmos criptográficos actuales", "CR-01", "PASS", "Todas las claves son ED25519 o RSA-SHA2", "", "R0")

    duration = int(time.time() - start_time)

    try:
        output = collector.build_output("audit-quick", distro_id, distro_family, running_kernel, duration, version_id, version_codename)
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
    print(f"{log_tag} Auditoría rápida completada en {duration}s")
    print(f"{log_tag} Health Score: {hs['overall']} (Security: {hs['security']}, Updates: {hs['updates']}, Hygiene: {hs['hygiene']}, Resources: {hs['resources']})")
    print(f"{log_tag} Resultados: {collector.passed} passed, {collector.failed} failed, {collector.warned} warned, {collector.skipped} skipped, {collector.errors} errors")
    print(f"{log_tag} Guardado en: {output_file}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
