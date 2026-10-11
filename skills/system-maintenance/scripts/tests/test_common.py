"""Tests common.py: --help, args inválidos, self-check, doradas puras."""
import json
import subprocess
import sys

import pytest

import common

SCRIPT = "common.py"


def _run(*args):
    return subprocess.run(
        [sys.executable, SCRIPT, *args],
        capture_output=True, text=True, cwd=".",
    )


def test_help_exit0():
    r = _run("--help")
    assert r.returncode == 0
    assert "usage" in (r.stdout + r.stderr).lower()


def test_invalid_args_exit2():
    r = _run("--opcion-invalida-xyz")
    assert r.returncode == 2


def test_self_check_exit0():
    r = _run("--self-check")
    assert r.returncode == 0
    assert "self-check OK" in r.stdout


def test_self_check_failure_exit1(monkeypatch):
    monkeypatch.setattr(common, "to_int", lambda *a, **k: 9999)
    assert common.main(["--self-check"]) == 1


def test_count_nonempty_golden():
    assert common.count_nonempty("a\n\nb\n  \nc\n") == 3
    assert common.count_nonempty("") == 0
    assert common.count_nonempty("\n\n") == 0


def test_to_int_golden():
    assert common.to_int("42") == 42
    assert common.to_int("  7  ") == 7
    assert common.to_int("x") == 0
    assert common.to_int("x", default=7) == 7
    assert common.to_int("") == 0
    assert common.to_int(None) == 0  # type: ignore[arg-type]


def test_finding_collector_health_score_golden():
    c = common.FindingCollector()
    c.add("S1", "security", "P0", "t", "d", "c", "PASS", "e", "", "R0")
    c.add("S2", "security", "P0", "t", "d", "c", "FAIL", "e", "", "R2")
    c.add("U1", "updates", "P1", "t", "d", "c", "PASS", "e", "", "R0")
    hs = c.health_score()
    assert hs["security"] == 50
    assert hs["updates"] == 100
    assert hs["hygiene"] == 100
    assert hs["resources"] == 100
    assert hs["overall"] == (50 * 40 + 100 * 25 + 100 * 20 + 100 * 15) // 100
    s = c.summary()
    assert s["total_checks"] == 3
    assert s["passed"] == 2
    assert s["failed"] == 1


def test_load_profile_family_tmp(tmp_path):
    prof = {
        "distro": {
            "family": "debian", "package_manager": "apt",
            "distro_id": "ubuntu", "version_id": "22.04", "version_codename": "jammy",
        }
    }
    p = tmp_path / "profile.json"
    p.write_text(json.dumps(prof), encoding="utf-8")
    fam, mgr, did, vid, cod = common.load_profile_family(str(p))
    assert (fam, mgr, did, vid, cod) == ("debian", "apt", "ubuntu", "22.04", "jammy")


def test_load_profile_family_corrupt_fallback(tmp_path):
    p = tmp_path / "bad.json"
    p.write_text("{no-json", encoding="utf-8")
    fam, mgr, did, vid, cod = common.load_profile_family(str(p))
    assert isinstance(fam, str) and isinstance(mgr, str)
