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


"""Tests clean_routine.py: --help, inválidos, sin pkg-mgr -> 1, doradas parser."""
import subprocess
import sys
from unittest.mock import patch, MagicMock

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


# --- clean_routine unit tests for coverage ---

def test_clean_which_found():
    with patch("clean_routine.which", return_value="/usr/bin/apt"):
        assert clean_routine.which("apt") == "/usr/bin/apt"


def test_clean_which_not_found():
    with patch("clean_routine.which", return_value=None):
        assert clean_routine.which("nonexistent") is None


def test_clean_detect_pkgmgr_pacman(monkeypatch):
    monkeypatch.setattr(clean_routine, "which", lambda cmd: "/usr/bin/pacman" if cmd == "pacman" else None)
    mgr = clean_routine.detect_pkg_mgr()
    assert mgr == "pacman"


def test_clean_detect_pkgmgr_apt(monkeypatch):
    monkeypatch.setattr(clean_routine, "which", lambda cmd: "/usr/bin/apt" if cmd == "apt" else None)
    mgr = clean_routine.detect_pkg_mgr()
    assert mgr == "apt"


def test_clean_detect_pkgmgr_dnf(monkeypatch):
    monkeypatch.setattr(clean_routine, "which", lambda cmd: "/usr/bin/dnf" if cmd == "dnf" else None)
    mgr = clean_routine.detect_pkg_mgr()
    assert mgr == "dnf"


def test_clean_detect_pkgmgr_none(monkeypatch):
    monkeypatch.setattr(clean_routine, "which", lambda cmd: None)
    mgr = clean_routine.detect_pkg_mgr()
    assert mgr == ""


def test_clean_run_safe_execute(monkeypatch):
    monkeypatch.setattr(clean_routine, "DRY_RUN", False)
    with patch("clean_routine.run_capture", return_value=(0, "ok")):
        rc = clean_routine.run_safe("echo test", "R1", "desc")
        assert rc == 0


def test_clean_run_safe_execute_failure(monkeypatch):
    monkeypatch.setattr(clean_routine, "DRY_RUN", False)
    with patch("clean_routine.run_capture", return_value=(1, "error")):
        rc = clean_routine.run_safe("false", "R1", "desc")
        assert rc == 1


def test_clean_package_cache_pacman(monkeypatch):
    monkeypatch.setattr(clean_routine, "PKG_MGR", "pacman")
    monkeypatch.setattr(clean_routine, "DRY_RUN", True)
    with patch("clean_routine.run", return_value="100M"):
        with patch("clean_routine.run_safe", return_value=0):
            clean_routine.clean_package_cache()


def test_clean_package_cache_apt(monkeypatch):
    monkeypatch.setattr(clean_routine, "PKG_MGR", "apt")
    monkeypatch.setattr(clean_routine, "DRY_RUN", True)
    with patch("clean_routine.run", return_value="50M"):
        clean_routine.clean_package_cache()


def test_clean_package_cache_dnf(monkeypatch):
    monkeypatch.setattr(clean_routine, "PKG_MGR", "dnf")
    monkeypatch.setattr(clean_routine, "DRY_RUN", True)
    with patch("clean_routine.run", return_value="80M"):
        clean_routine.clean_package_cache()


def test_clean_journal(monkeypatch):
    monkeypatch.setattr(clean_routine, "DRY_RUN", True)
    with patch("clean_routine.run", return_value="200M"):
        clean_routine.clean_journal()


def test_clean_orphans_pacman_none(monkeypatch):
    monkeypatch.setattr(clean_routine, "PKG_MGR", "pacman")
    monkeypatch.setattr(clean_routine, "DRY_RUN", True)
    with patch("clean_routine.run", return_value=""):
        clean_routine.clean_orphans()


def test_clean_orphans_pacman_some(monkeypatch):
    monkeypatch.setattr(clean_routine, "PKG_MGR", "pacman")
    monkeypatch.setattr(clean_routine, "DRY_RUN", True)
    with patch("clean_routine.run", return_value="pkg1\npkg2"):
        clean_routine.clean_orphans()


def test_clean_orphans_apt(monkeypatch):
    monkeypatch.setattr(clean_routine, "PKG_MGR", "apt")
    monkeypatch.setattr(clean_routine, "DRY_RUN", True)
    with patch("clean_routine.run", return_value="pkg1\npkg2"):
        clean_routine.clean_orphans()
