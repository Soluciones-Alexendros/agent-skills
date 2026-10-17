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

try:
    import risk_gate
except ImportError:  # pragma: no cover
    risk_gate = None  # type: ignore

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
WITH_FIRMWARE = False
ACTION_RESULTS: list[dict[str, object]] = []

# Host mutations stay blocked unless the typed executor / explicit allow is set.
_HOST_MUTATION_ENV = "AUTOWORKSPACE_ALLOW_HOST_MUTATION"

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
    parser.add_argument("--firmware", action="store_true", default=False, help="Incluir fwupdmgr update (R2, solo con --execute)")
    parser.add_argument("--verbose", action="store_true", help="Logging verboso a stderr")
    return parser


def apply_args(args: argparse.Namespace) -> None:
    global DRY_RUN, EXECUTE, SNAPSHOT_ID, OUTPUT_FILE, JSON_OUTPUT
    global KEEP_VERSIONS, JOURNAL_VACUUM_TIME, JOURNAL_VACUUM_SIZE, JSON_MODE
    global WITH_FIRMWARE
    if args.execute:
        DRY_RUN, EXECUTE = False, True
    else:
        DRY_RUN, EXECUTE = True, False
    SNAPSHOT_ID = args.snapshot_id or ""
    OUTPUT_FILE = args.output or ""
    KEEP_VERSIONS = args.keep_versions
    JOURNAL_VACUUM_TIME = args.journal_time
    JOURNAL_VACUUM_SIZE = args.journal_size
    WITH_FIRMWARE = bool(args.firmware)
    if args.json is not None:
        JSON_MODE = True
        JSON_OUTPUT = args.json or ""
    else:
        JSON_MODE = False
        JSON_OUTPUT = ""


def _record(action: str, status: str, rc: int = 0, detail: str = "") -> None:
    ACTION_RESULTS.append(
        {"action": action, "status": status, "rc": rc, "detail": detail}
    )


def _snapshot_dir() -> str:
    return os.environ.get(
        "SNAPSHOT_DIR",
        os.path.expanduser("~/.local/share/mantenimiento-linux/snapshots"),
    )


def validate_snapshot(snapshot_id: str) -> tuple[bool, str]:
    """Validate snapshot id, directory, and recovery metadata before mutation."""
    if not snapshot_id or "/" in snapshot_id or snapshot_id in (".", ".."):
        return False, "invalid snapshot_id"
    path = os.path.join(_snapshot_dir(), snapshot_id)
    if not os.path.isdir(path):
        return False, f"snapshot directory missing: {path}"
    meta_path = os.path.join(path, "metadata.json")
    if not os.path.isfile(meta_path):
        return False, "metadata.json missing"
    try:
        with open(meta_path, encoding="utf-8") as fh:
            meta = json.load(fh)
    except (OSError, json.JSONDecodeError) as exc:
        return False, f"metadata unreadable: {exc}"
    if meta.get("backend_status") == "failed":
        return False, "snapshot backend_status=failed"
    if meta.get("recovery_scope") == "none" and meta.get("backend_required"):
        return False, "recovery_scope=none with required backend"
    return True, path


def host_mutations_allowed() -> bool:
    return os.environ.get(_HOST_MUTATION_ENV, "") == "1"


def run_safe(cmd: str, risk_level: str, description: str) -> int:
    action = description
    if DRY_RUN:
        log_info(f"[DRY-RUN] {description}")
        log_info(f"  Comando: {cmd}")
        log_info(f"  Riesgo: {risk_level}")
        _record(action, "simulated", 0, cmd)
        return 0

    if not host_mutations_allowed():
        log_error(
            f"Mutación bloqueada ({description}): set {_HOST_MUTATION_ENV}=1 "
            "only after typed executor approval (T10)."
        )
        _record(action, "blocked", 3, "host mutations disabled")
        return 3

    if risk_gate is not None:
        gate_rc = risk_gate.validate(cmd, snapshot_id=SNAPSHOT_ID, approved=False)
        if gate_rc != 0:
            log_error(f"risk_gate DENY: {description}")
            _record(action, "blocked", gate_rc, "risk_gate")
            return gate_rc

    log_info(f"Ejecutando: {description}")
    log_info(f"  Comando: {cmd}")
    rc, _ = run_capture(cmd, timeout=600)
    if rc == 0:
        log_success(f"  OK: {description}")
        _record(action, "succeeded", 0, cmd)
        return 0
    log_error(f"  FALLÓ: {description}")
    _record(action, "failed", rc, cmd)
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


def clean_needrestart() -> None:
    """needrestart: lista servicios que piden reinicio (R1); reinicia solo en --execute."""
    log_info("=== Servicios que piden reinicio (needrestart) ===")
    if which("needrestart") is None:
        log_info("needrestart no instalado (instalar para detectar reinicios pendientes)")
        return
    pending = run("needrestart -r l 2>/dev/null | head -20", timeout=120).strip()
    if DRY_RUN:
        log_info("needrestart -r l (solo lista):")
        for line in pending.splitlines()[:20]:
            if line.strip():
                log_info(f"  {line.strip()}")
        run_safe("needrestart -r a", "R1", "Reiniciar servicios obsoletos tras actualizacion")
    else:
        rc, _ = run_capture("needrestart -r a 2>/dev/null", timeout=600)
        if rc != 0:
            log_warn("needrestart -r a fallo o requirio intervencion")


def update_firmware() -> None:
    """fwupdmgr update (R2): solo con --firmware + --execute + snapshot previo."""
    log_info("=== Firmware (fwupdmgr, R2) ===")
    if which("fwupdmgr") is None:
        log_info("fwupd no instalado")
        return
    if DRY_RUN:
        pending = run("fwupdmgr get-updates 2>/dev/null | grep '^Device:' | head -10", timeout=120).strip()
        if pending:
            log_info("Dispositivos con updates:")
            for line in pending.splitlines():
                log_info(f"  {line.strip()}")
        run_safe("fwupdmgr update", "R2", "Actualizar firmware de dispositivos")
        return
    if not WITH_FIRMWARE:
        log_info("Omitido: requiere --firmware explicito (R2)")
        return
    rc, _ = run_capture("fwupdmgr update 2>/dev/null", timeout=900)
    if rc != 0:
        log_warn("fwupdmgr update fallo")


def clean_userspace_caches() -> None:
    """Caches userspace seguras: thumbnails + ficheros >30 dias (excluye navegadores)."""
    import os as _os
    log_info("=== Caches userspace ===")
    home = _os.path.expanduser("~")
    cache_dir = _os.path.join(home, ".cache")
    size = run(f"du -sh {cache_dir} 2>/dev/null | cut -f1", timeout=60).strip()
    log_info(f"Tamano ~/.cache: {size or '?'}")
    thumb = _os.path.join(cache_dir, "thumbnails")
    if DRY_RUN:
        run_safe(f"rm -rf {thumb}/* + find {cache_dir} -type f -atime +30 "
                 "(excluye *mozilla* *chromium* *Proton*)", "R1", "Limpiar caches userspace")
    else:
        run(f"rm -rf {thumb}/* 2>/dev/null", timeout=120)
        run(f"find {cache_dir} -type f -atime +30 ! -path '*mozilla*' ! -path '*chromium*' "
            "! -path '*Chromium*' ! -path '*Proton*' -delete 2>/dev/null", timeout=300)
        log_success("Caches userspace limpiadas")


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
    actions = list(ACTION_RESULTS)
    if not actions:
        # Ensure dry-run always emits explicit simulated rows, never fake completed.
        defaults = [
            "clean_package_cache",
            "clean_journal",
            "clean_orphans",
            "clean_temp",
            "clean_needrestart",
            "update_firmware",
            "clean_userspace_caches",
        ]
        for name in defaults:
            if name == "update_firmware" and not WITH_FIRMWARE:
                actions.append({"action": name, "status": "skipped", "rc": 0, "detail": ""})
            elif DRY_RUN:
                actions.append({"action": name, "status": "simulated", "rc": 0, "detail": ""})
            else:
                actions.append({"action": name, "status": "failed", "rc": 1, "detail": "no result recorded"})
    completed = sum(1 for a in actions if a.get("status") == "succeeded")
    failed = sum(1 for a in actions if a.get("status") in ("failed", "blocked"))
    simulated = sum(1 for a in actions if a.get("status") == "simulated")
    skipped = sum(1 for a in actions if a.get("status") == "skipped")
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
        "actions": actions,
        "summary": {
            "total_actions": len(actions),
            "completed": completed,
            "failed": failed,
            "simulated": simulated,
            "skipped": skipped,
        },
    }
    try:
        with open(json_file, "w", encoding="utf-8") as fh:
            json.dump(result, fh, indent=2)
    except (OSError, TypeError, ValueError) as exc:
        logger.error("no se pudo escribir JSON %r: %s", json_file, exc)
        raise
    log_info(f"JSON output: {json_file}")


def _ensure_snapshot_for_execute() -> int:
    """Create or validate snapshot before any host effect. Returns process rc."""
    global SNAPSHOT_ID
    if not SNAPSHOT_ID:
        log_warn("No se especificó --snapshot-id. Creando snapshot...")
        SNAPSHOT_ID = f"snap-{utcnow_iso().replace('-', '').replace(':', '').replace('T', '-').replace('Z', '')}"
        script_dir = os.path.dirname(os.path.abspath(__file__))
        script = os.path.join(script_dir, "snapshot_state.py")
        rc, out = run_capture(f"{sys.executable} '{script}' '{SNAPSHOT_ID}'", timeout=600)
        if rc != 0:
            log_error(f"Creación de snapshot falló (rc={rc})")
            _record("create_snapshot", "failed", rc, out[:200] if out else "")
            return 1
        log_info(f"Snapshot ID: {SNAPSHOT_ID}")
    ok, detail = validate_snapshot(SNAPSHOT_ID)
    if not ok:
        log_error(f"Snapshot inválido: {detail}")
        _record("validate_snapshot", "failed", 1, detail)
        return 1
    _record("validate_snapshot", "succeeded", 0, detail)
    return 0


def main(argv: list[str] | None = None) -> int:
    global SNAPSHOT_ID, PKG_MGR
    ACTION_RESULTS.clear()
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

    if EXECUTE:
        snap_rc = _ensure_snapshot_for_execute()
        if snap_rc != 0:
            if JSON_MODE:
                try:
                    generate_json_output()
                except (OSError, TypeError, ValueError):
                    pass
            return snap_rc
        if not host_mutations_allowed():
            log_error(
                f"Ejecución real bloqueada: {_HOST_MUTATION_ENV}=1 requerido "
                "tras aprobación del ejecutor tipado."
            )
            _record("host_mutation_gate", "blocked", 3, _HOST_MUTATION_ENV)
            if JSON_MODE:
                try:
                    generate_json_output()
                except (OSError, TypeError, ValueError):
                    pass
            return 3

    # Route cleanup through run_safe so dry-run records simulated and execute is gated.
    run_safe(f"clean_package_cache:{PKG_MGR}", "R1", "clean_package_cache")
    run_safe("clean_journal", "R1", "clean_journal")
    run_safe(f"clean_orphans:{PKG_MGR}", "R1", "clean_orphans")
    run_safe("clean_temp", "R1", "clean_temp")
    run_safe("needrestart", "R1", "clean_needrestart")
    if WITH_FIRMWARE:
        run_safe("fwupdmgr update", "R2", "update_firmware")
    else:
        _record("update_firmware", "skipped", 0, "requires --firmware")
    run_safe("clean_userspace_caches", "R1", "clean_userspace_caches")

    if EXECUTE and host_mutations_allowed():
        # Legacy detailed cleaners only when host mutation explicitly allowed.
        clean_package_cache()
        clean_journal()
        clean_orphans()
        clean_temp()
        clean_needrestart()
        update_firmware()
        clean_userspace_caches()
        verify_clean()

    failed = sum(1 for a in ACTION_RESULTS if a.get("status") in ("failed", "blocked"))
    if failed:
        log_error(f"Rutina finalizada con {failed} acción(es) fallidas/bloqueadas")
    else:
        log_info("Rutina de limpieza completada")

    if JSON_MODE:
        try:
            generate_json_output()
        except (OSError, TypeError, ValueError) as exc:
            logger.error("no se pudo generar JSON: %s", exc)
            return 1
    if failed and EXECUTE:
        return 1
    if any(a.get("status") == "blocked" for a in ACTION_RESULTS) and EXECUTE:
        return 3
    return 0


if __name__ == "__main__":
    sys.exit(main())
