"""Tests clean_routine.py: --help, inválidos, sin pkg-mgr -> 1, doradas parser."""
import subprocess
import sys

import clean_routine

SCRIPT = "clean_routine.py"


def _run(*args):
    return subprocess.run(
        [sys.executable, SCRIPT, *args], capture_output=True, text=True, cwd=".",
    )


def test_help_exit0():
    r = _run("--help")
    assert r.returncode == 0


def test_invalid_args_exit2():
    r = _run("--opcion-invalida-xyz")
    assert r.returncode == 2
    r2 = _run("--keep-versions", "no-entero")
    assert r2.returncode == 2


def test_error_sin_pkgmgr_exit1(monkeypatch):
    monkeypatch.setattr(clean_routine, "which", lambda cmd: None)
    assert clean_routine.main(["--dry-run"]) == 1


def test_parser_dry_run_golden():
    ns = clean_routine.build_parser().parse_args(["--dry-run"])
    clean_routine.apply_args(ns)
    assert clean_routine.DRY_RUN is True and clean_routine.EXECUTE is False


def test_parser_execute_snapshot_golden():
    ns = clean_routine.build_parser().parse_args(
        ["--execute", "--snapshot-id", "snap-1", "--keep-versions", "5"]
    )
    clean_routine.apply_args(ns)
    assert clean_routine.EXECUTE is True
    assert clean_routine.SNAPSHOT_ID == "snap-1"
    assert clean_routine.KEEP_VERSIONS == 5
    # restaurar default para no contaminar otros tests
    clean_routine.apply_args(clean_routine.build_parser().parse_args([]))


def test_run_safe_dryrun_golden(monkeypatch):
    monkeypatch.setattr(clean_routine, "DRY_RUN", True)
    assert clean_routine.run_safe("rm -rf /tmpx", "R1", "desc") == 0
