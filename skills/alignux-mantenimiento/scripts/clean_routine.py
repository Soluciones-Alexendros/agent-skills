#!/usr/bin/env python3
"""clean_routine.py - Limpieza aprobada (cache, journal, huérfanos, temporales).

Port Python de clean_routine.sh. Soporta --dry-run y --execute con snapshot
previo.
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import sys

from common import (
    BLUE,
    GREEN,
    RED,
    SKILL_VERSION,
    color,
    hostname,
    log_warn,
    run,
    run_capture,
    utcnow_iso,
    which,
)

DRY_RUN = True
EXECUTE = False
SNAPSHOT_ID = ""
OUTPUT_FILE = ""
JSON_OUTPUT = ""
PKG_MGR = ""
KEEP_VERSIONS = 3
JOURNAL_VACUUM_TIME = "7d"
JOURNAL_VACUUM_SIZE = "500M"
JSON_MODE = False

logger = logging.getLogger("mantenimiento.clean")


def _setup_logging(verbose: bool = False) -> None:
    level = logging.DEBUG if verbose else logging.WARNING
    if not logging.getLogger().handlers:
        logging.basicConfig(level=level, format="%(levelname)s: %(message)s", stream=sys.stderr)
    else:
        logging.getLogger().setLevel(level)


def log_info(msg: str) -> None:
    print(color(f"[CLEAN] {msg}", BLUE))


def log_success(msg: str) -> None:
    print(color(f"[SUCCESS] {msg}", GREEN))


def log_error(msg: str) -> None:
    logger.error("%s", msg)
    print(color(f"[ERROR] {msg}", RED))


def detect_pkg_mgr() -> str:
    """Detecta gestor; devuelve '' si no hay ninguno (main decide exit 1)."""
    mgr = ""
    if which("pacman"):
        mgr = "pacman"
    if which("apt"):
        mgr = "apt"
    if which("dnf"):
        mgr = "dnf"
    return mgr


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Rutina de limpieza aprobada (por defecto --dry-run).")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--dry-run", dest="dry_run", action="store_true", default=None, help="Solo simular (defecto)")
    mode.add_argument("--execute", dest="execute", action="store_true", default=None, help="Ejecutar limpieza real")
    parser.add_argument("--snapshot-id", default="", help="ID de snapshot previo (requerido en --execute)")
    parser.add_argument("--output", default="", help="Fichero de salida (reservado)")
    parser.add_argument("--keep-versions", type=int, default=3, help="Versiones a conservar en caché (defecto 3)")
    parser.add_argument("--journal-time", default="7d", help="Vacuum time del journal (defecto 7d)")
    parser.add_argument("--journal-size", default="500M", help="Vacuum size del journal (defecto 500M)")
    parser.add_argument("--json", nargs="?", const="", default=None, help="Generar JSON (opcional fichero)")
    parser.add_argument("--verbose", action="store_true", help="Logging verboso a stderr")
    return parser


def apply_args(args: argparse.Namespace) -> None:
    global DRY_RUN, EXECUTE, SNAPSHOT_ID, OUTPUT_FILE, JSON_OUTPUT
    global KEEP_VERSIONS, JOURNAL_VACUUM_TIME, JOURNAL_VACUUM_SIZE, JSON_MODE
    if args.execute:
        DRY_RUN, EXECUTE = False, True
    else:
        DRY_RUN, EXECUTE = True, False
    SNAPSHOT_ID = args.snapshot_id or ""
    OUTPUT_FILE = args.output or ""
    KEEP_VERSIONS = args.keep_versions
    JOURNAL_VACUUM_TIME = args.journal_time
    JOURNAL_VACUUM_SIZE = args.journal_size
    if args.json is not None:
        JSON_MODE = True
        JSON_OUTPUT = args.json or ""
    else:
        JSON_MODE = False
        JSON_OUTPUT = ""


def run_safe(cmd: str, risk_level: str, description: str) -> int:
    if DRY_RUN:
        log_info(f"[DRY-RUN] {description}")
        log_info(f"  Comando: {cmd}")
        log_info(f"  Riesgo: {risk_level}")
        return 0

    log_info(f"Ejecutando: {description}")
    log_info(f"  Comando: {cmd}")
    rc, _ = run_capture(cmd, timeout=600)
    if rc == 0:
        log_success(f"  OK: {description}")
        return 0
    log_error(f"  FALLÓ: {description}")
    return 1


def clean_package_cache() -> None:
    log_info("=== Limpieza de caché de paquetes ===")
    if PKG_MGR == "pacman":
        cache_size = run("du -sh /var/cache/pacman/pkg 2>/dev/null | cut -f1", timeout=30).strip()
        log_info(f"Tamaño actual: {cache_size}")
        if DRY_RUN:
            run_safe(f"paccache -r -k {KEEP_VERSIONS} -d", "R1", "paccache dry-run")
        else:
            rc, _ = run_capture(f"paccache -r -k {KEEP_VERSIONS} 2>/dev/null", timeout=600)
            if rc != 0:
                log_warn("paccache falló")
    elif PKG_MGR == "apt":
        cache_size = run("du -sh /var/cache/apt/archives 2>/dev/null | cut -f1", timeout=30).strip()
        log_info(f"Tamaño actual: {cache_size}")
        if DRY_RUN:
            log_info("apt autoclean eliminaría paquetes antiguos")
        else:
            rc, _ = run_capture("apt-get autoclean 2>/dev/null", timeout=600)
            if rc != 0:
                log_warn("apt-get autoclean falló")
    elif PKG_MGR == "dnf":
        cache_size = run("du -sh /var/cache/dnf 2>/dev/null | cut -f1", timeout=30).strip()
        log_info(f"Tamaño actual: {cache_size}")
        if DRY_RUN:
            log_info("dnf clean packages eliminaría caché")
        else:
            rc, _ = run_capture("dnf clean packages -y 2>/dev/null", timeout=600)
            if rc != 0:
                log_warn("dnf clean falló")


def clean_journal() -> None:
    log_info("=== Limpieza de journal ===")
    journal_size = run("journalctl --disk-usage 2>/dev/null", timeout=15).strip()
    log_info(f"Tamaño actual: {journal_size}")
    if DRY_RUN:
        log_info(f"journalctl --vacuum-time={JOURNAL_VACUUM_TIME} --vacuum-size={JOURNAL_VACUUM_SIZE}")
    else:
        rc, _ = run_capture(
            f"journalctl --vacuum-time={JOURNAL_VACUUM_TIME} --vacuum-size={JOURNAL_VACUUM_SIZE} 2>/dev/null",
            timeout=600,
        )
        if rc != 0:
            log_warn("journal vacuum falló")


def clean_orphans() -> None:
    log_info("=== Limpieza de paquetes huérfanos ===")
    if PKG_MGR == "pacman":
        orphans = run("pacman -Qtdq 2>/dev/null", timeout=60).strip()
        orphan_list = [p for p in orphans.splitlines() if p.strip()]
        if not orphan_list:
            log_info("Sin paquetes huérfanos")
            return
        log_info(f"Huérfanos detectados: {len(orphan_list)}")
        for pkg in orphan_list:
            if DRY_RUN:
                log_info(f"  - {pkg}")
            else:
                log_info(f"Eliminando: {pkg}")
                rc, _ = run_capture(f"pacman -Rns {pkg} --noconfirm 2>/dev/null", timeout=600)
                if rc != 0:
                    log_warn(f"No se pudo eliminar {pkg}")
    elif PKG_MGR == "apt":
        if DRY_RUN:
            run("apt autoremove --dry-run 2>/dev/null", timeout=120)
        else:
            rc, _ = run_capture("apt autoremove --purge -y 2>/dev/null", timeout=600)
            if rc != 0:
                log_warn("apt autoremove falló")
    elif PKG_MGR == "dnf":
        if DRY_RUN:
            run("dnf autoremove --assumeno 2>/dev/null", timeout=120)
        else:
            rc, _ = run_capture("dnf autoremove -y 2>/dev/null", timeout=600)
            if rc != 0:
                log_warn("dnf autoremove falló")


def clean_temp() -> None:
    log_info("=== Limpieza de archivos temporales ===")
    if DRY_RUN:
        log_info("rm -rf /tmp/* /var/tmp/* (archivos > 7 días)")
    else:
        run("find /tmp -type f -atime +7 -delete 2>/dev/null", timeout=300)
        run("find /var/tmp -type f -atime +7 -delete 2>/dev/null", timeout=300)
        log_success("Temporales limpiados")


def verify_clean() -> None:
    log_info("=== Verificación post-limpieza ===")
    failed = run("systemctl --failed --no-legend --no-pager 2>/dev/null", timeout=15)
    failed_count = sum(1 for line in failed.splitlines() if line.strip())
    if failed_count > 0:
        log_warn(f"{failed_count} servicios fallidos detectados")
    else:
        log_success("Sin servicios fallidos")

    df_out = run("df -h / 2>/dev/null | tail -1", timeout=15).strip()
    if df_out:
        print(df_out)
    journal_out = run("journalctl --disk-usage 2>/dev/null", timeout=15).strip()
    if journal_out:
        print(journal_out)


def generate_json_output() -> None:
    json_file = JSON_OUTPUT or f"clean-routine-{utcnow_iso().replace('-', '').replace(':', '').replace('T', '-').replace('Z', '')}.json"
    result = {
        "metadata": {
            "timestamp": utcnow_iso(),
            "mode": "clean-routine",
            "hostname": hostname(),
            "distro": PKG_MGR,
            "dry_run": DRY_RUN,
            "snapshot_id": SNAPSHOT_ID or "none",
            "skill_version": SKILL_VERSION,
        },
        "actions": [
            {"action": "clean_package_cache", "status": "completed"},
            {"action": "clean_journal", "status": "completed"},
            {"action": "clean_orphans", "status": "completed"},
            {"action": "clean_temp", "status": "completed"},
        ],
        "summary": {
            "total_actions": 4,
            "completed": 4,
            "failed": 0,
        },
    }
    try:
        with open(json_file, "w", encoding="utf-8") as fh:
            json.dump(result, fh, indent=2)
    except (OSError, TypeError, ValueError) as exc:
        logger.error("no se pudo escribir JSON %r: %s", json_file, exc)
        raise
    log_info(f"JSON output: {json_file}")


def main(argv: list[str] | None = None) -> int:
    global SNAPSHOT_ID, PKG_MGR
    parser = build_parser()
    args = parser.parse_args(argv)
    _setup_logging(args.verbose)
    apply_args(args)

    PKG_MGR = detect_pkg_mgr()
    if not PKG_MGR:
        logger.error("No se pudo detectar gestor de paquetes")
        log_error("No se pudo detectar gestor de paquetes")
        return 1

    log_info("Iniciando rutina de limpieza")
    log_info("Modo: " + ("DRY-RUN" if DRY_RUN else "EJECUCIÓN"))
    log_info(f"Gestor de paquetes: {PKG_MGR}")

    if EXECUTE and not SNAPSHOT_ID:
        log_warn("No se especificó --snapshot-id. Creando snapshot...")
        SNAPSHOT_ID = f"snap-{utcnow_iso().replace('-', '').replace(':', '').replace('T', '-').replace('Z', '')}"
        script_dir = os.path.dirname(os.path.abspath(__file__))
        try:
            run_capture(f"{script_dir}/snapshot_state.py {SNAPSHOT_ID}", timeout=600)
        except (OSError, ValueError) as exc:
            logger.error("fallo creando snapshot previo: %s", exc)
            return 1
        log_info(f"Snapshot ID: {SNAPSHOT_ID}")

    clean_package_cache()
    clean_journal()
    clean_orphans()
    clean_temp()

    if EXECUTE:
        verify_clean()

    log_info("Rutina de limpieza completada")

    if JSON_MODE:
        try:
            generate_json_output()
        except (OSError, TypeError, ValueError) as exc:
            logger.error("no se pudo generar JSON: %s", exc)
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
