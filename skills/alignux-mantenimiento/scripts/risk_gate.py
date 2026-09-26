#!/usr/bin/env python3
"""risk_gate.py - Validador determinista pre-ejecución.

Port Python de risk_gate.sh. Clasifica comandos en R0/R1/R2/R3 antes de
permitir su ejecución.

Uso:
  risk_gate.py "<comando>" [snapshot_id] [approved]
  cat comandos.txt | risk_gate.py
"""

from __future__ import annotations

import argparse
import logging
import re
import sys

from common import GREEN, RED, YELLOW, color

logger = logging.getLogger("mantenimiento.risk_gate")


def _setup_logging(verbose: bool = False) -> None:
    level = logging.DEBUG if verbose else logging.WARNING
    if not logging.getLogger().handlers:
        logging.basicConfig(level=level, format="%(levelname)s: %(message)s", stream=sys.stderr)
    else:
        logging.getLogger().setLevel(level)

PROTECTED_PATHS = (
    "/boot", "/efi", "/etc/fstab", "/etc/passwd", "/etc/shadow",
    "/etc/group", "/etc/gshadow", "/etc/sudoers", "/etc/ssh/sshd_config",
    "/etc/ssh/ssh_host_", "/etc/systemd", "/etc/pacman.conf",
    "/etc/pacman.d", "/usr/lib/modules", "/var/lib/pacman/local",
    "/var/lib/dpkg", "/var/lib/rpm",
)

R3_PATTERNS = (
    r"^rm\s+(-rf?\s+)?/",
    r"^rm\s+(-rf?\s+)?\*",
    r"^rm\s+(-rf?\s+)?~",
    r"^mkfs\.",
    r"^dd\s+.*of=/dev/(sd|hd|vd|nvme|mmcblk)",
    r"^wipefs",
    r"^sgdisk\s+.*-Z",
    r"^parted\s+.*mklabel",
    r":\(\)\s*\{\s*:\|\:&\s*\};:",
    r"^chmod\s+(-R\s+)?777\s+/",
    r"^chown\s+(-R\s+)?root:root\s+/",
    r"^pacman\s+(-Rdd|--remove\s+--nodeps)",
    r"^apt\s+(purge|remove)\s+.*--force",
    r"^dnf\s+remove\s+.*--nodeps",
    r"curl\s+.*\|\s*sh",
    r"wget\s+.*\|\s*sh",
    r"bash\s+<\s*\(curl",
    r"bash\s+<\s*\(wget",
    r"git\s+push\s+(--force|-f)",
    r">\s*/dev/(sd|hd|vd|nvme|mmcblk)",
)

R2_PATTERNS = (
    r"^pacman\s+-Syu",
    r"^apt\s+(update|full-upgrade|dist-upgrade)",
    r"^dnf\s+(upgrade|update)",
    r"^vim\s+/etc/",
    r"^nano\s+/etc/",
    r"^systemctl\s+(enable|disable|mask|unmask)",
    r"^grub-mkconfig",
    r"^update-grub",
    r"^mkinitcpio",
    r"^bootctl",
    r"^iptables",
    r"^nft\s+",
    r"^ufw\s+",
    r"^firewall-cmd",
    r"^parted",
    r"^fdisk",
    r"^gdisk",
    r"^cryptsetup",
    r"^mkfs",
    r"^mkswap",
    r"^mount\s+/",
    r"^umount\s+/",
    r"^useradd",
    r"^usermod",
    r"^userdel",
    r"^groupadd",
    r"^groupmod",
    r"^groupdel",
    r"^chmod\s+.*\s+/etc",
    r"^chmod\s+.*\s+/boot",
    r"^chmod\s+.*\s+/usr",
    r"^chown\s+.*\s+/etc",
    r"^chown\s+.*\s+/boot",
    r"^chown\s+.*\s+/usr",
    r"^makepkg",
    r"^fwupdmgr\s+update",
)

R1_PATTERNS = (
    r"^paccache",
    r"^journalctl\s+--vacuum",
    r"^apt\s+(clean|autoclean|autoremove)",
    r"^dnf\s+(clean|autoremove)",
    r"^pacman\s+-Sc",
    r"^pacman\s+-Rns",
    r"^rm\s+.*\s+/tmp/",
    r"^rm\s+.*\s+/var/tmp/",
    r"^mv\s+.*\.pacnew",
    r"^mv\s+.*\.pacsave",
    r"^mv\s+.*\.rpmnew",
    r"^mv\s+.*\.rpmsave",
    r"^mv\s+.*\.dpkg-new",
    r"^mv\s+.*\.dpkg-old",
)


def matches_pattern(cmd: str, patterns: tuple) -> bool:
    for pattern in patterns:
        try:
            if re.search(pattern, cmd):
                return True
        except re.error as exc:
            logger.warning("patrón regex inválido %r: %s", pattern, exc)
            continue
    return False


def touches_protected_path(cmd: str) -> bool:
    """Verifica si un comando implica escritura en rutas protegidas.
    
    Solo considera escrita la línea de comandos si contiene redirecciones
    de salida (>, >>, | tee), o si es explícitamente un editor/escritor.
    Comandos de solo lectura como cat, grep, head, ls no se clasifican.
    """
    # Whitelist de comandos de solo lectura que no deberían clasificar como R2
    read_only_cmds = ("cat", "grep", "head", "tail", "ls", "find", "df", "du", 
                       "systemctl status", "journalctl", "ps", "top", "htop",
                       "ss", "ip", "uname", "uptime", "whoami", "id", 
                       "mount", "blkid", "lscpu", "free", "vmstat", "nproc")
    cmd_lower = cmd.lower()
    
    for ro_cmd in read_only_cmds:
        if cmd_lower.startswith(ro_cmd + " ") or cmd_lower == ro_cmd:
            return False
    
    # Detectar operaciones de escritura: redirecciones o herramientas de edición
    write_indicators = (" >", " >>", "| tee", "| sudo tee", "<(/dev/", "> /dev/")
    has_write_op = any(ind in cmd for ind in write_indicators)
    
    if not has_write_op:
        return False
    
    # Si hay operación de escritura, verificar si toca ruta protegida
    return any(path in cmd for path in PROTECTED_PATHS)


def classify_command(cmd: str) -> str:
    if matches_pattern(cmd, R3_PATTERNS):
        return "R3"
    if matches_pattern(cmd, R2_PATTERNS):
        return "R2"
    if touches_protected_path(cmd):
        return "R2"
    if matches_pattern(cmd, R1_PATTERNS):
        return "R1"
    return "R0"


def validate(cmd: str, snapshot_id: str = "", approved: bool = False) -> int:
    risk_level = classify_command(cmd)

    if risk_level == "R0":
        print(color(f"[R0] ALLOW: {cmd}", GREEN))
        return 0
    if risk_level == "R1":
        if not snapshot_id:
            logger.warning("R1 DENY sin snapshot: %s", cmd)
            print(color(f"[R1] DENY: {cmd} (requiere snapshot previo)", YELLOW))
            return 1
        print(color(f"[R1] ALLOW (con snapshot {snapshot_id}): {cmd}", YELLOW))
        return 0
    if risk_level == "R2":
        if not approved:
            logger.warning("R2 DENY sin aprobación: %s", cmd)
            print(color(f"[R2] DENY: {cmd} (requiere aprobación humana explícita)", YELLOW))
            return 1
        if not snapshot_id:
            logger.warning("R2 DENY sin snapshot: %s", cmd)
            print(color(f"[R2] DENY: {cmd} (requiere snapshot previo)", YELLOW))
            return 1
        print(color(f"[R2] ALLOW (con snapshot {snapshot_id} y aprobación): {cmd}", YELLOW))
        return 0
    # R3
    logger.error("R3 BLOCKED: %s", cmd)
    print(color(f"[R3] BLOCKED: {cmd} (prohibido por deny-list)", RED))
    return 2


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validador determinista pre-ejecución (clasifica R0/R1/R2/R3)."
    )
    parser.add_argument("command", nargs="?", default=None, help='Comando a validar entre comillas')
    parser.add_argument("snapshot_id", nargs="?", default="", help="ID de snapshot previo")
    parser.add_argument(
        "approved", nargs="?", default="false", help='"true" si hay aprobación humana explícita'
    )
    parser.add_argument("--verbose", action="store_true", help="Logging verboso a stderr")
    args = parser.parse_args(argv)
    _setup_logging(args.verbose)
    if args.command is not None:
        try:
            approved = str(args.approved).lower() == "true"
        except (ValueError, AttributeError) as exc:
            logger.error("approved inválido %r: %s", args.approved, exc)
            return 2
        return validate(args.command, args.snapshot_id or "", approved)

    # Sin comando posicional: leer de stdin (no bloquear si es TTY sin pipe).
    try:
        if sys.stdin.isatty():
            parser.print_usage(sys.stderr)
            logger.error("se requiere <comando> o comandos por stdin (pipe)")
            return 2
    except (OSError, ValueError) as exc:
        logger.error("no se pudo inspeccionar stdin: %s", exc)
        return 1
    try:
        rc = 0
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue
            r = validate(line)
            if r != 0 and rc == 0:
                rc = r
        return rc
    except OSError as exc:
        logger.error("error leyendo stdin: %s", exc)
        return 1


if __name__ == "__main__":
    sys.exit(main())
