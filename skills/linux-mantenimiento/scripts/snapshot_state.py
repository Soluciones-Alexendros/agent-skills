#!/usr/bin/env python3
"""snapshot_state.py - Captura pre-cambio (paquetes, configs, espacio, servicios).

Port Python de snapshot_state.sh. Crea un snapshot reversible antes de
acciones R1+. Uso: snapshot_state.py [snapshot-id]
"""

from __future__ import annotations

import argparse
import getpass
import hashlib
import json
import logging
import os
import sys

from common import (
    SKILL_VERSION,
    hostname,
    log_info,
    log_warn,
    run,
    run_capture,
    utcnow_iso,
    which,
)

SNAPSHOT_DIR = os.environ.get("SNAPSHOT_DIR", os.path.expanduser("~/.local/share/mantenimiento-linux/snapshots"))

logger = logging.getLogger("mantenimiento.snapshot")


def _setup_logging(verbose: bool = False) -> None:
    level = logging.DEBUG if verbose else logging.WARNING
    if not logging.getLogger().handlers:
        logging.basicConfig(level=level, format="%(levelname)s: %(message)s", stream=sys.stderr)
    else:
        logging.getLogger().setLevel(level)


def _current_user() -> str:
    try:
        return getpass.getuser()
    except (OSError, KeyError) as exc:
        logger.warning("getpass.getuser() falló: %s", exc)
        return os.environ.get("USER", "unknown")


def md5_file(path: str) -> str:
    digest = hashlib.md5()
    try:
        with open(path, "rb") as fh:
            for chunk in iter(lambda: fh.read(65536), b""):
                digest.update(chunk)
    except OSError:
        return ""
    return digest.hexdigest()


def detect_pkg_mgr() -> str:
    if which("pacman"):
        return "pacman"
    if which("apt"):
        return "apt"
    if which("dnf"):
        return "dnf"
    return ""


def write_text(path: str, content: str) -> None:
    try:
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(content)
    except OSError as exc:
        logger.error("no se pudo escribir %r: %s", path, exc)
        raise


def capture_packages(pkg_mgr: str, snapshot_path: str) -> None:
    if pkg_mgr == "pacman":
        write_text(f"{snapshot_path}/packages-installed.txt", run("pacman -Q 2>/dev/null", timeout=30))
        write_text(f"{snapshot_path}/packages-explicit.txt", run("pacman -Qe 2>/dev/null", timeout=30))
        write_text(f"{snapshot_path}/packages-orphans.txt", run("pacman -Qtdq 2>/dev/null", timeout=30))
        write_text(f"{snapshot_path}/packages-foreign.txt", run("pacman -Qmq 2>/dev/null", timeout=30))
    elif pkg_mgr == "apt":
        write_text(f"{snapshot_path}/packages-installed.txt", run("dpkg --get-selections 2>/dev/null", timeout=30))
        write_text(
            f"{snapshot_path}/packages-explicit.txt",
            run("apt list --manual-installed 2>/dev/null | tail -n +2", timeout=60),
        )
    elif pkg_mgr == "dnf":
        write_text(f"{snapshot_path}/packages-installed.txt", run("rpm -qa 2>/dev/null", timeout=30))
        write_text(
            f"{snapshot_path}/packages-explicit.txt",
            run("dnf list installed 2>/dev/null | tail -n +2", timeout=60),
        )


def capture_etc_checksums(snapshot_path: str) -> None:
    lines: list = []
    for root, _dirs, files in os.walk("/etc"):
        for name in files:
            full = os.path.join(root, name)
            digest = md5_file(full)
            if digest:
                lines.append(f"{digest}  {full}\n")
    write_text(f"{snapshot_path}/etc-checksums.txt", "".join(lines))


def capture_config_pending(pkg_mgr: str, snapshot_path: str) -> None:
    if pkg_mgr == "pacman":
        out = run("find /etc -name '*.pacnew' -o -name '*.pacsave' 2>/dev/null", timeout=30)
    elif pkg_mgr == "apt":
        out = run("find /etc -name '*.dpkg-*' -o -name '*.ucf-*' 2>/dev/null", timeout=30)
    else:
        out = run("find /etc -name '*.rpmnew' -o -name '*.rpmsave' 2>/dev/null", timeout=30)
    write_text(f"{snapshot_path}/config-pending.txt", out)


def list_snapshots(base_dir: str) -> int:
    """Lista snapshots con metadata (solo lectura)."""
    try:
        entries = sorted(os.listdir(base_dir))
    except OSError as exc:
        logger.error("no se pudo listar %r: %s", base_dir, exc)
        return 1
    found = 0
    for name in entries:
        meta_path = os.path.join(base_dir, name, "metadata.json")
        if not os.path.isfile(meta_path):
            continue
        try:
            with open(meta_path, encoding="utf-8") as fh:
                meta = json.load(fh)
            print(f"{name}  {meta.get('timestamp', '?')}  {meta.get('package_manager', '?')}")
        except (OSError, ValueError):
            print(f"{name}  (metadata ilegible)")
        found += 1
    if not found:
        print("(sin snapshots)")
    return 0


def diff_snapshot(base_dir: str, snapshot_id: str) -> tuple[list, list, int]:
    """Compara etc-checksums del snapshot contra el /etc actual.

    Devuelve (changed, missing, total). Solo /etc, solo lectura.
    """
    snap_file = os.path.join(base_dir, snapshot_id, "etc-checksums.txt")
    changed: list = []
    missing: list = []
    total = 0
    try:
        with open(snap_file, encoding="utf-8") as fh:
            lines = fh.read().splitlines()
    except OSError as exc:
        logger.error("no se pudo leer %r: %s", snap_file, exc)
        return [], [], 0
    for line in lines:
        parts = line.split()
        if len(parts) < 2:
            continue
        digest, path = parts[0], parts[-1]
        if not path.startswith("/etc/"):
            continue
        total += 1
        current = md5_file(path)
        if not current:
            missing.append(path)
        elif current != digest:
            changed.append(path)
    return changed, missing, total


def rollback_snapshot(base_dir: str, snapshot_id: str, execute: bool = False) -> int:
    """Rollback de /etc contra un snapshot.

    Por defecto dry-run: diff + plan de restauracion. Con --execute restaura
    desde etc-backup.tar.gz (si existe) con backup previo; snapper/timeshift
    se indican como comandos manuales (no se auto-restauran).
    """
    if "/" in snapshot_id or snapshot_id in ("", ".", ".."):
        logger.error("snapshot_id inválido: %r", snapshot_id)
        print(f"snapshot_id inválido: {snapshot_id}", file=sys.stderr)
        return 2
    snapshot_path = os.path.join(base_dir, snapshot_id)
    if not os.path.isdir(snapshot_path):
        logger.error("snapshot inexistente: %r", snapshot_path)
        print(f"snapshot inexistente: {snapshot_id}", file=sys.stderr)
        return 1
    changed, missing, total = diff_snapshot(base_dir, snapshot_id)
    print(f"rollback {snapshot_id}: {total} ficheros vigilados, "
          f"{len(changed)} cambiados, {len(missing)} eliminados")
    for path in (changed + missing)[:20]:
        print(f"  ~ {path}")
    tarball = os.path.join(snapshot_path, "etc-backup.tar.gz")
    if not execute:
        print("[dry-run] Sin cambios. Plan de restauracion:")
        if os.path.isfile(tarball):
            print(f"  tar -tzf {tarball}  # verificar contenido")
            print(f"  snapshot_state.py --rollback {snapshot_id} --execute  # restaura /etc desde tarball")
        if which("snapper") is not None:
            print("  snapper undochange <pre>..<post>  # alternativa btrfs (manual)")
        if which("timeshift") is not None:
            print("  timeshift --restore  # alternativa (interactivo, ventana acordada)")
        return 0
    if not os.path.isfile(tarball):
        log_warn("sin etc-backup.tar.gz: restauracion manual con los comandos de arriba")
        return 1
    backup_dir = os.path.join(snapshot_path, f"pre-rollback-{utcnow_iso().replace('-', '').replace(':', '').replace('T', '-').replace('Z', '')}")
    try:
        os.makedirs(backup_dir, exist_ok=True)
    except OSError as exc:
        logger.error("no se pudo crear %r: %s", backup_dir, exc)
        return 1
    restored, failed = 0, 0
    for path in changed + missing:
        rel = path.lstrip("/")
        try:
            if os.path.isfile(path):
                with open(path, "rb") as src, open(os.path.join(backup_dir, rel.replace("/", "_")), "wb") as dst:
                    dst.write(src.read())
        except OSError as exc:
            logger.warning("no se pudo respaldar %r: %s", path, exc)
        rc, _ = run_capture(f"tar -xzf '{tarball}' -C / '{rel}' 2>/dev/null", timeout=120)
        if rc == 0:
            restored += 1
        else:
            failed += 1
            log_warn(f"no se pudo restaurar {path}")
    log_info(f"Rollback {snapshot_id}: {restored} restaurados, {failed} fallidos (backup en {backup_dir})")
    return 0 if failed == 0 else 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Captura pre-cambio (snapshot reversible antes de R1+).")
    parser.add_argument("snapshot_id", nargs="?", default=None, help="ID del snapshot")
    parser.add_argument("--snapshot-dir", default=None, help="Override directorio base de snapshots")
    parser.add_argument("--list", action="store_true", help="Listar snapshots existentes")
    parser.add_argument("--rollback", default="", help="ID del snapshot contra el que comparar/restaurar /etc")
    parser.add_argument("--execute", action="store_true", help="Ejecutar rollback (por defecto dry-run)")
    parser.add_argument("--verbose", action="store_true", help="Logging verboso a stderr")
    args = parser.parse_args(argv)
    _setup_logging(args.verbose)

    base_dir = args.snapshot_dir or os.environ.get("SNAPSHOT_DIR", SNAPSHOT_DIR)
    if not base_dir:
        logger.error("directorio base de snapshots vacío")
        return 1
    if args.list:
        return list_snapshots(base_dir)
    if args.rollback:
        return rollback_snapshot(base_dir, args.rollback, execute=args.execute)
    snapshot_id = args.snapshot_id or f"snap-{utcnow_iso().replace('-', '').replace(':', '').replace('T', '-').replace('Z', '')}"
    if "/" in snapshot_id or snapshot_id in ("", ".", ".."):
        logger.error("snapshot_id inválido: %r", snapshot_id)
        print(f"snapshot_id inválido: {snapshot_id}", file=sys.stderr)
        return 2
    snapshot_path = os.path.join(base_dir, snapshot_id)

    pkg_mgr = detect_pkg_mgr()

    try:
        os.makedirs(snapshot_path, exist_ok=True)
    except OSError as exc:
        logger.error("no se pudo crear %r: %s", snapshot_path, exc)
        return 1

    log_info(f"Creando snapshot: {snapshot_id}")
    log_info(f"Destino: {snapshot_path}")

    metadata = {
        "snapshot_id": snapshot_id,
        "timestamp": utcnow_iso(),
        "hostname": hostname(),
        "user": _current_user(),
        "package_manager": pkg_mgr,
        "kernel": run("uname -r", timeout=5).strip(),
        "skill_version": SKILL_VERSION,
    }
    try:
        with open(f"{snapshot_path}/metadata.json", "w", encoding="utf-8") as fh:
            json.dump(metadata, fh, indent=2)
    except (OSError, TypeError, ValueError) as exc:
        logger.error("no se pudo escribir metadata.json: %s", exc)
        return 1

    try:
        log_info("Capturando lista de paquetes...")
        capture_packages(pkg_mgr, snapshot_path)

        log_info("Capturando checksums de /etc...")
        capture_etc_checksums(snapshot_path)

        log_info("Capturando archivos de configuración pendientes...")
        capture_config_pending(pkg_mgr, snapshot_path)

        log_info("Capturando estado de servicios...")
        write_text(
            f"{snapshot_path}/services-enabled.txt",
            run("systemctl list-unit-files --type=service --state=enabled --no-pager 2>/dev/null", timeout=15),
        )
        write_text(
            f"{snapshot_path}/services-running.txt",
            run("systemctl list-units --type=service --state=running --no-pager 2>/dev/null", timeout=15),
        )

        log_info("Capturando uso de espacio...")
        write_text(f"{snapshot_path}/disk-usage.txt", run("df -h 2>/dev/null", timeout=15))
        write_text(
            f"{snapshot_path}/cache-sizes.txt",
            run("du -sh /var/cache/pacman/pkg /var/cache/apt/archives /var/cache/dnf 2>/dev/null", timeout=30),
        )

        write_text(f"{snapshot_path}/journal-size.txt", run("journalctl --disk-usage 2>/dev/null", timeout=15))
    except OSError:
        return 1

    if which("timeshift"):
        log_info("Creando snapshot timeshift...")
        rc, _ = run_capture(f"timeshift --create --comments 'mantenimiento-linux: {snapshot_id}' --tags D 2>/dev/null", timeout=300)
        if rc != 0:
            log_warn("No se pudo crear snapshot timeshift")
    elif which("snapper"):
        log_info("Creando snapshot snapper...")
        rc, _ = run_capture(
            f"snapper create --description 'mantenimiento-linux: {snapshot_id}' --cleanup-algorithm number 2>/dev/null",
            timeout=300,
        )
        if rc != 0:
            log_warn("No se pudo crear snapshot snapper")
    else:
        log_warn("No hay snapshot tool (timeshift/snapper). Creando backup tar de configs críticas...")
        family = detect_pkg_mgr()
        etc_files = ["/etc/ssh/sshd_config", "/etc/ssh/ssh_host_*", "/etc/fstab"]
        if family == "pacman":
            etc_files.extend(["/etc/pacman.conf", "/etc/pacman.d"])
        elif family == "apt":
            etc_files.extend(["/etc/apt/sources.list", "/etc/apt/preferences"])
        elif family == "dnf":
            etc_files.extend(["/etc/yum.repos.d/", "/etc/dnf/dnf.conf"])
        etc_str = " ".join(etc_files)
        rc, _ = run_capture(f"tar -czf '{snapshot_path}/etc-backup.tar.gz' {etc_str} 2>/dev/null", timeout=120)
        if rc != 0:
            log_warn("Backup parcial de configs")

    log_info("Calculando hash del snapshot...")
    hash_lines = []
    try:
        for root, _dirs, files in os.walk(snapshot_path):
            for name in files:
                full = os.path.join(root, name)
                digest = md5_file(full)
                if digest:
                    hash_lines.append((full, digest))
        hash_lines.sort(key=lambda item: item[0])
        with open(f"{snapshot_path}/SNAPSHOT-HASHES.txt", "w", encoding="utf-8") as fh:
            for full, digest in hash_lines:
                fh.write(f"{digest}  {full}\n")

        hashes_digest = hashlib.md5()
        with open(f"{snapshot_path}/SNAPSHOT-HASHES.txt", "rb") as fh:
            for chunk in iter(lambda: fh.read(65536), b""):
                hashes_digest.update(chunk)
        snapshot_hash = hashes_digest.hexdigest()
        write_text(f"{snapshot_path}/SNAPSHOT-HASH.txt", snapshot_hash + "\n")
    except OSError as exc:
        logger.error("no se pudo calcular hash del snapshot: %s", exc)
        return 1

    log_info(f"Snapshot creado exitosamente: {snapshot_id}")
    log_info(f"Hash: {snapshot_hash}")
    log_info(f"Ubicación: {snapshot_path}")

    if os.environ.get("OUTPUT_JSON", "false") == "true":
        try:
            files_captured = sum(len(files) for _, _, files in os.walk(snapshot_path))
        except OSError as exc:
            logger.error("no se pudo contar ficheros del snapshot: %s", exc)
            return 1
        result = {
            "snapshot_id": snapshot_id,
            "snapshot_path": snapshot_path,
            "snapshot_hash": snapshot_hash,
            "timestamp": utcnow_iso(),
            "package_manager": pkg_mgr,
            "files_captured": files_captured,
        }
        try:
            print(json.dumps(result, indent=2))
        except (TypeError, ValueError) as exc:
            logger.error("no se pudo serializar JSON de salida: %s", exc)
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
