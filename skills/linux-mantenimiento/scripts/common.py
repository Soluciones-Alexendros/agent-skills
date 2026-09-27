#!/usr/bin/env python3
"""Utilidades compartidas para mantenimiento-linux (port Python nativo).

Reemplaza las funciones comunes de los scripts bash (run_cmd/run_check,
detección de distro/gestor de paquetes, logging con color, recolección de
hallazgos y cálculo del Health Score) sin depender de jq ni de subprocesos
bash. Todo el parsing se hace con la librería estándar.
"""

from __future__ import annotations

import json
import logging
import os
import shutil
import socket
import subprocess
import sys
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("mantenimiento.common")


def _setup_logging(verbose: bool = False) -> None:
    level = logging.DEBUG if verbose else logging.WARNING
    if not logging.getLogger().handlers:
        logging.basicConfig(level=level, format="%(levelname)s: %(message)s", stream=sys.stderr)
    else:
        logging.getLogger().setLevel(level)

SKILL_VERSION = "1.1.0"

# --- Colores ANSI (desactivados si no hay TTY o está NO_COLOR) ---
_USE_COLOR = sys.stdout.isatty() and not os.environ.get("NO_COLOR")

RED = "\033[0;31m"
GREEN = "\033[0;32m"
YELLOW = "\033[1;33m"
BLUE = "\033[0;34m"
NC = "\033[0m"

CATEGORIES = ("security", "updates", "hygiene", "resources")
SEVERITIES = ("P0", "P1", "P2", "P3", "P4")
STATUSES = ("PASS", "FAIL", "WARN", "SKIP", "ERROR")


def color(text: str, code: str) -> str:
    return f"{code}{text}{NC}" if _USE_COLOR else text


def log_info(msg: str) -> None:
    print(color(f"[INFO] {msg}", GREEN))


def log_pass(msg: str) -> None:
    print(color(f"[PASS] {msg}", GREEN))


def log_fail(msg: str) -> None:
    print(color(f"[FAIL] {msg}", RED))


def log_warn(msg: str) -> None:
    print(color(f"[WARN] {msg}", YELLOW))


def log_error(msg: str) -> None:
    logger.error("%s", msg)
    print(color(f"[ERROR] {msg}", RED))


def log_debug(msg: str) -> None:
    print(color(f"[DEBUG] {msg}", BLUE))


def utcnow_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def hostname() -> str:
    return socket.gethostname()


def which(cmd: str) -> str | None:
    return shutil.which(cmd)


def run(cmd: str, timeout: int = 10) -> str:
    """Ejecuta un comando shell y devuelve su stdout; '' ante fallo/timeout."""
    try:
        proc = subprocess.run(
            cmd,
            shell=True,
            executable="/bin/bash",
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            timeout=timeout,
            text=True,
            check=False,
        )
        return proc.stdout
    except (subprocess.TimeoutExpired, OSError):
        return ""


def run_capture(cmd: str, timeout: int = 10) -> tuple[int, str]:
    """Ejecuta un comando shell y devuelve (returncode, stdout)."""
    try:
        proc = subprocess.run(
            cmd,
            shell=True,
            executable="/bin/bash",
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            timeout=timeout,
            text=True,
            check=False,
        )
        return proc.returncode, proc.stdout
    except (subprocess.TimeoutExpired, OSError):
        return 1, ""


def count_nonempty(text: str) -> int:
    """Cuenta líneas no vacías (equivale a `grep -c .`, sin el bug de 0)."""
    return sum(1 for line in text.splitlines() if line.strip())


def to_int(value: str, default: int = 0) -> int:
    value = (value or "").strip()
    try:
        return int(value)
    except (ValueError, TypeError):
        return default


def sysctl_get(key: str) -> str:
    return run(f"sysctl -n {key} 2>/dev/null", timeout=5).strip()


def service_active(unit: str) -> bool:
    """Verifica si un servicio systemd está activo leyendo su estado real."""
    rc, out = run_capture(f"systemctl is-active {unit} 2>/dev/null", timeout=10)
    return out.strip() == "active"


def read_os_release() -> dict[str, str]:
    values: dict[str, str] = {}
    try:
        with open("/etc/os-release", encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line or "=" not in line:
                    continue
                key, _, val = line.partition("=")
                values[key] = val.strip().strip('"').strip("'")
    except OSError:
        pass
    return values


# --- Detección de distro y gestor de paquetes ---

_ARCH_IDS = {"arch", "endeavouros", "cachyos", "manjaro", "garuda", "artix"}
_DEBIAN_IDS = {
    "debian", "ubuntu", "linuxmint", "pop", "elementary",
    "kali", "parrot", "zorin",
}
_RHEL_IDS = {
    "fedora", "rhel", "centos", "almalinux", "rocky", "ol", "scientific",
}
_SUSE_IDS = {"opensuse", "opensuse-leap", "opensuse-tumbleweed", "sles"}


def detect_distro() -> dict[str, str]:
    release = read_os_release()
    distro_id = release.get("ID", "unknown")
    distro_like = release.get("ID_LIKE", "")
    version_id = release.get("VERSION_ID", "")
    version_codename = release.get("VERSION_CODENAME", "")

    family = "unknown"
    pkg_mgr = "unknown"
    aur_helper = ""

    if distro_id in _ARCH_IDS:
        family, pkg_mgr = "arch", "pacman"
        if which("yay"):
            aur_helper = "yay"
        if which("paru"):
            aur_helper = "paru"
    elif distro_id in _DEBIAN_IDS:
        family, pkg_mgr = "debian", "apt"
    elif distro_id in _RHEL_IDS:
        family, pkg_mgr = "rhel", "dnf"
    elif any(distro_id.startswith(prefix) for prefix in ("opensuse",)) or distro_id == "sles":
        family, pkg_mgr = "suse", "zypper"
    else:
        # Fallback por gestor de paquetes
        if which("pacman"):
            family, pkg_mgr = "arch", "pacman"
        elif which("apt"):
            family, pkg_mgr = "debian", "apt"
        elif which("dnf"):
            family, pkg_mgr = "rhel", "dnf"
        elif which("zypper"):
            family, pkg_mgr = "suse", "zypper"

    return {
        "distro_id": distro_id,
        "distro_like": distro_like,
        "version_id": version_id,
        "version_codename": version_codename,
        "family": family,
        "package_manager": pkg_mgr,
        "aur_helper": aur_helper,
    }


def detect_pkg_mgr() -> tuple[str, str]:
    """Devuelve (family, package_manager)."""
    distro = detect_distro()
    return distro["family"], distro["package_manager"]


def load_profile_family(profile_file: str) -> tuple[str, str, str, str, str]:
    """Carga family, package_manager, distro_id, version_id, version_codename de un system-profile.json si existe."""
    if os.path.isfile(profile_file):
        try:
            with open(profile_file, encoding="utf-8") as fh:
                profile = json.load(fh)
            family = profile.get("distro", {}).get("family", "unknown")
            pkg_mgr = profile.get("distro", {}).get("package_manager", "unknown")
            distro_id = profile.get("distro", {}).get("distro_id", "unknown")
            version_id = profile.get("distro", {}).get("version_id", "")
            version_codename = profile.get("distro", {}).get("version_codename", "")
            if family and pkg_mgr:
                return family, pkg_mgr, distro_id, version_id, version_codename
        except (OSError, json.JSONDecodeError):
            pass
    distro = detect_distro()
    return distro["family"], distro["package_manager"], distro["distro_id"], distro["version_id"], distro["version_codename"]


# --- Recolección de hallazgos y Health Score (compartido audit_quick/full) ---


class FindingCollector:
    """Recolecta hallazgos y calcula el Health Score con la fórmula del skill."""

    def __init__(self) -> None:
        self.findings: list[dict[str, str]] = []
        self._counters: dict[str, int] = {status: 0 for status in STATUSES}

    def add(
        self,
        id: str,
        category: str,
        severity: str,
        title: str,
        description: str,
        control: str,
        status: str,
        evidence: str,
        remediation: str,
        risk_level: str,
    ) -> None:
        self.findings.append(
            {
                "id": id,
                "category": category,
                "severity": severity,
                "title": title,
                "description": description,
                "control": control,
                "status": status,
                "evidence": evidence,
                "remediation": remediation,
                "risk_level": risk_level,
            }
        )
        self._counters[status] = self._counters.get(status, 0) + 1

    @property
    def total(self) -> int:
        return len(self.findings)

    @property
    def passed(self) -> int:
        return self._counters.get("PASS", 0)

    @property
    def failed(self) -> int:
        return self._counters.get("FAIL", 0)

    @property
    def warned(self) -> int:
        return self._counters.get("WARN", 0)

    @property
    def skipped(self) -> int:
        return self._counters.get("SKIP", 0)

    @property
    def errors(self) -> int:
        return self._counters.get("ERROR", 0)

    def _category_score(self, category: str) -> int:
        total = sum(1 for f in self.findings if f["category"] == category)
        if total == 0:
            return 100
        passed = sum(
            1 for f in self.findings
            if f["category"] == category and f["status"] == "PASS"
        )
        return passed * 100 // total

    def health_score(self) -> dict[str, int]:
        security = self._category_score("security")
        updates = self._category_score("updates")
        hygiene = self._category_score("hygiene")
        resources = self._category_score("resources")
        overall = (security * 40 + updates * 25 + hygiene * 20 + resources * 15) // 100
        return {
            "overall": overall,
            "security": security,
            "updates": updates,
            "hygiene": hygiene,
            "resources": resources,
        }

    def summary(self) -> dict[str, object]:
        by_severity = {
            sev: sum(1 for f in self.findings if f["severity"] == sev)
            for sev in SEVERITIES
        }
        return {
            "total_checks": self.total,
            "passed": self.passed,
            "failed": self.failed,
            "warned": self.warned,
            "skipped": self.skipped,
            "errors": self.errors,
            "by_severity": by_severity,
        }

    def build_output(
        self,
        mode: str,
        distro: str,
        family: str,
        kernel: str,
        duration_seconds: int,
        version_id: str = "",
        version_codename: str = "",
        skill_version: str = SKILL_VERSION,
    ) -> dict[str, Any]:
        return {
            "metadata": {
                "timestamp": utcnow_iso(),
                "mode": mode,
                "hostname": hostname(),
                "distro": distro,
                "family": family,
                "version_id": version_id,
                "version_codename": version_codename,
                "kernel": kernel,
                "duration_seconds": duration_seconds,
                "skill_version": skill_version,
            },
            "health_score": self.health_score(),
            "findings": self.findings,
            "summary": self.summary(),
        }


# --- Utilidades de sshd (audit_full) ---

_SSHD_KEYS = (
    "permitrootlogin",
    "passwordauthentication",
    "permitemptypasswords",
    "maxauthtries",
    "clientaliveinterval",
    "clientalivecountmax",
    "allowusers",
    "allowgroups",
)


def sshd_effective() -> str:
    """Devuelve la config efectiva de sshd como líneas 'clave valor' (minúsculas).

    Intenta `sshd -T` (requiere root); si devuelve vacío, parsea los ficheros
    de configuración. Corrige la recursión infinita del bash original.
    """
    output = run("sshd -T 2>/dev/null", timeout=10)
    if output.strip():
        return output

    files = ["/etc/ssh/sshd_config"]
    files += sorted(
        f
        for f in glob_sorted("/etc/ssh/sshd_config.d/*.conf")
    )
    lines: list[str] = []
    for path in files:
        try:
            with open(path, encoding="utf-8", errors="replace") as fh:
                for line in fh:
                    stripped = line.strip().lower()
                    if not stripped or stripped.startswith("#"):
                        continue
                    for key in _SSHD_KEYS:
                        if stripped.startswith(key + " "):
                            parts = stripped.split()
                            if len(parts) >= 2:
                                lines.append(f"{parts[0]} {parts[1]}")
                            break
        except OSError:
            continue
    return "\n".join(lines) + ("\n" if lines else "")


def glob_sorted(pattern: str) -> list[str]:
    import glob

    return sorted(glob.glob(pattern))


def _sshd_get(key: str) -> str:
    for line in sshd_effective().splitlines():
        parts = line.split()
        if parts and parts[0].lower() == key and len(parts) >= 2:
            return parts[1]
    return ""


def main(argv: list[str] | None = None) -> int:
    """Entry point librería común (no ejecuta auditoría; solo --help/self-check)."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Utilidades compartidas mantenimiento-linux (librería, sin acción por defecto)."
    )
    parser.add_argument("--verbose", action="store_true", help="Logging verboso a stderr")
    parser.add_argument(
        "--self-check",
        action="store_true",
        help="Verifica imports y funciones puras básicas (no toca el sistema)",
    )
    args = parser.parse_args(argv)
    _setup_logging(args.verbose)
    if args.self_check:
        try:
            assert count_nonempty("a\n\nb\n") == 2
            assert to_int("42") == 42 and to_int("x", default=7) == 7
            c = FindingCollector()
            c.add("T-01", "security", "P0", "t", "d", "c", "PASS", "e", "", "R0")
            assert c.passed == 1 and c.total == 1
        except AssertionError as exc:
            logger.error("self-check fallido: %s", exc)
            return 1
        print("common self-check OK")
        return 0
    parser.print_usage(sys.stdout)
    print("common.py es una librería; impórtala desde los demás scripts.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
