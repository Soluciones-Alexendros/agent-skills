"""Tests de los scripts nuevos de linux-seguridad (esqueletos funcionales)."""
import json
import os
import subprocess
import sys

SCRIPTS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, SCRIPTS)

import apparmor_lifecycle
import forense_collector
import harden_plan
import scan_orchestrator
import vulns_check


def _run(script, *args):
    return subprocess.run(
        [sys.executable, os.path.join(SCRIPTS, script), *args],
        capture_output=True, text=True, timeout=60,
    )


def test_all_help_exit0():
    for s in ("scan_orchestrator.py", "vulns_check.py", "harden_plan.py",
              "apparmor_lifecycle.py", "forense_collector.py"):
        r = _run(s, "--help")
        assert r.returncode == 0, s


def test_all_invalid_args_exit2():
    for s in ("scan_orchestrator.py", "vulns_check.py", "harden_plan.py",
              "apparmor_lifecycle.py"):
        r = _run(s, "--opcion-inexistente-xyz")
        assert r.returncode == 2, s
    r = _run("forense_collector.py", "receta-inexistente-xyz")
    assert r.returncode == 2


def test_scan_check_exit0(tmp_path):
    out = tmp_path / "scan.json"
    r = _run("scan_orchestrator.py", "--json", str(out))
    assert r.returncode == 0
    data = json.loads(out.read_text(encoding="utf-8"))
    assert set(data) >= {"availability", "scans", "cross_validation"}


def test_cross_validate_golden():
    res = {"rkhunter": {"warnings": 2}, "debsums": {"mismatches": 1},
           "aide": {"changed_entries": True}}
    cv = scan_orchestrator.cross_validate(res)
    assert len(cv["indeterminados"]) == 3 and cv["validados"] == []
    cv2 = scan_orchestrator.cross_validate({"rkhunter": {}, "debsums": {}, "aide": {}})
    assert cv2["descartados"] != []


def test_vulns_exit0(tmp_path):
    out = tmp_path / "vulns.json"
    r = _run("vulns_check.py", "--json", str(out))
    assert r.returncode == 0
    data = json.loads(out.read_text(encoding="utf-8"))
    assert set(data["sources"]) == {"apt", "snap", "flatpak"}


def test_harden_plan_baseline_ids():
    base = os.path.join(SCRIPTS, "..", "references", "hardening-baseline.md")
    ids = harden_plan.parse_control_ids(base)
    assert "SSH-01" in ids and "KR-22" in ids and len(ids) > 50


def test_harden_plan_exit0(tmp_path):
    out = tmp_path / "plan.json"
    r = _run("harden_plan.py", "--level", "1", "--json", str(out))
    assert r.returncode == 0
    data = json.loads(out.read_text(encoding="utf-8"))
    assert "plan" in data and isinstance(data["plan"], list)


def test_harden_plan_baseline_ilegible():
    assert harden_plan.parse_control_ids("/no/existe/baseline.md") == []
    assert _run("harden_plan.py", "--baseline", "/no/existe.md").returncode == 1


def test_apparmor_status_y_soak(tmp_path):
    st = str(tmp_path / "aa.json")
    assert apparmor_lifecycle.main(["status", "--state", st]) == 0
    assert apparmor_lifecycle.main(
        ["soak", "--profile", "test-prof", "--days", "3", "--state", st]) == 0
    data = json.loads(open(st, encoding="utf-8").read())
    assert data["profiles"]["test-prof"]["stage"] == "soak"
    # enforce bloqueado si aa-logprof no parsea
    rc = apparmor_lifecycle.main(["enforce", "--profile", "test-prof", "--state", st])
    assert rc in (0, 1)


def test_apparmor_retroceso_bloqueado(tmp_path):
    st = str(tmp_path / "aa2.json")
    apparmor_lifecycle.main(["soak", "--profile", "p", "--days", "1", "--state", st])
    assert apparmor_lifecycle.main(["genprof", "--profile", "p", "--state", st]) == 1


def test_forense_sin_pid_requiere_pid():
    assert forense_collector.main(["pid"]) == 2


def test_forense_timeline_exit0(tmp_path):
    out = tmp_path / "for.json"
    r = _run("forense_collector.py", "timeline", "--json", str(out))
    assert r.returncode == 0
    data = json.loads(out.read_text(encoding="utf-8"))
    assert "events" in data and "system_clock" in data


def test_postura_json(tmp_path):
    sh = os.path.join(SCRIPTS, "postura_seguridad.sh")
    p = subprocess.run(["bash", sh, "--json"], capture_output=True, text=True, timeout=60)
    assert p.returncode == 0
    data = json.loads(p.stdout)
    assert "apparmor_kernel" in data and "lockdown" in data and "tpm2" in data
    assert "syft" in data and "canon_terminal" in data


def test_postura_sin_hardcodeo_visible():
    sh = os.path.join(SCRIPTS, "postura_seguridad.sh")
    text = open(sh, encoding="utf-8").read()
    assert "Aplicaciones/Terminal" not in text
