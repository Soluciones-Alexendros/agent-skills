"""Cobertura de logica de negocio: checks comunes, diff temporal, rollback, evasion."""
import json

import audit_full
import audit_quick
import common
import report_render
import risk_gate
import snapshot_state


def _collector():
    return common.FindingCollector()


def _ids(collector):
    return [f["id"] for f in collector.findings]


# --- common.check_* ---

def test_check_pkg_01_apt_sin_updates():
    c = _collector()
    common.check_pkg_01(c, "apt", runner=lambda cmd, timeout=60: "")
    assert c.findings[-1]["status"] == "PASS"


def test_check_pkg_01_apt_con_updates():
    c = _collector()
    common.check_pkg_01(c, "apt", runner=lambda cmd, timeout=60: "foo/1.0\nbar/2.0\n")
    assert c.findings[-1]["status"] == "FAIL"
    assert "2" in c.findings[-1]["title"]


def test_check_pkg_01_gestor_desconocido_skip():
    c = _collector()
    common.check_pkg_01(c, "desconocido-xyz", runner=lambda cmd, timeout=60: "")
    assert c.findings[-1]["status"] == "SKIP"


def test_check_pkg_03_coincide():
    c = _collector()
    def fake(cmd, timeout=10):
        if cmd.startswith("uname"):
            return "6.8.0-1-generic\n"
        return "6.8.0-1-generic\n"
    kernel = common.check_pkg_03(c, "apt", runner=fake)
    assert kernel == "6.8.0-1-generic"
    assert c.findings[-1]["status"] == "PASS"


def test_check_pkg_03_mismatch_fail():
    c = _collector()
    def fake(cmd, timeout=10):
        return "6.8.0-2-generic\n" if cmd.startswith("uname") else "6.8.0-1-generic\n"
    common.check_pkg_03(c, "apt", runner=fake)
    assert c.findings[-1]["status"] == "FAIL"


def test_check_fs_10_disk_thresholds():
    c = _collector()
    df = "sda1 / 95%\nsda2 /home 85%\nsda3 /var 50%\n"
    common.check_fs_10_disk(c, runner=lambda cmd, timeout=15: df)
    by_status = {f["title"]: f["status"] for f in c.findings}
    assert by_status["Disco / al 95%"] == "FAIL"
    assert by_status["Disco /home al 85%"] == "WARN"
    assert by_status["Disco /var al 50%"] == "PASS"


def test_check_log_06_sin_errores():
    c = _collector()
    common.check_log_06(c, runner=lambda cmd, timeout=60: "")
    assert c.findings[-1]["status"] == "PASS"
    assert c.findings[-1]["id"] == "LOG-06"


def test_check_srv_02_fallidos():
    c = _collector()
    common.check_srv_02(c, runner=lambda cmd, timeout=15: "foo.service loaded failed\n")
    assert c.findings[-1]["status"] == "FAIL"
    c2 = _collector()
    common.check_srv_02(c2, runner=lambda cmd, timeout=15: "")
    assert c2.findings[-1]["status"] == "PASS"


def test_check_net_04_expuesto_y_no():
    c = _collector()
    common.check_net_04(c, runner=lambda cmd, timeout=10: "tcp 0 0 0.0.0.0:22 0.0.0.0:* LISTEN\n")
    assert c.findings[-1]["status"] == "WARN"
    c2 = _collector()
    common.check_net_04(c2, runner=lambda cmd, timeout=10: "")
    assert c2.findings[-1]["status"] == "PASS"


def test_check_pkg_07_pacnew_fail():
    c = _collector()
    common.check_pkg_07(c, "pacman", runner=lambda cmd, timeout=30: "/etc/x.pacnew\n")
    assert c.findings[-1]["status"] == "FAIL"
    assert "pacdiff" in c.findings[-1]["remediation"]


def test_check_fs_09_e_inodos():
    c = _collector()
    common.check_fs_09(c, runner=lambda cmd, timeout=120: "/etc/roto\n")
    assert c.findings[-1]["status"] == "WARN"
    c2 = _collector()
    common.check_fs_11_inodes(c2, runner=lambda cmd, timeout=15: "/dev/sda1 100 90 10 90% /\n")
    assert c2.findings and c2.findings[-1]["status"] == "FAIL"


# --- audit_quick / audit_full reuse ---

def test_run_quick_checks_ids():
    c = _collector()
    def fake(cmd, timeout=10):
        if "df -h" in cmd:
            return "sda1 / 50%\n"
        return ""
    kernel = audit_quick.run_quick_checks(c, "apt", runner=fake)
    assert isinstance(kernel, str)
    assert set(_ids(c)) == {"PKG-01", "PKG-03", "PKG-05", "PKG-07",
                            "NET-04", "FS-10", "LOG-06", "SRV-02"}


def test_run_extended_checks_ids():
    c = _collector()
    audit_full.run_extended_checks(c, "apt", runner=lambda cmd, timeout=10: "")
    ids = set(_ids(c))
    assert {"FS-09", "LOG-08", "PKG-06", "PKG-09", "PKG-04", "ARC-07", "DEB-04"} <= ids
    # Sin hardening puro
    assert not (ids & {"SSH-03", "KR-02", "AU-01", "UA-03", "CR-01", "FW-02"})


def test_health_score_vacio_es_100():
    hs = _collector().health_score()
    assert hs == {"overall": 100, "security": 100, "updates": 100,
                  "hygiene": 100, "resources": 100}


def test_health_score_todo_fail_es_0():
    c = _collector()
    c.add("S", "security", "P0", "t", "d", "c", "FAIL", "e", "", "R2")
    c.add("U", "updates", "P1", "t", "d", "c", "FAIL", "e", "", "R2")
    hs = c.health_score()
    assert hs["security"] == 0 and hs["hygiene"] == 100
    assert hs["overall"] == (0 * 40 + 0 * 25 + 100 * 20 + 100 * 15) // 100


# --- risk_gate evasion ---

def test_evasion_sudo_env_subshell():
    assert risk_gate.classify_command("sudo pacman -Syu") == "R2"
    assert risk_gate.classify_command("FOO=1 pacman -Syu") == "R2"
    assert risk_gate.classify_command("echo $(pacman -Syu)") == "R2"
    assert risk_gate.classify_command("echo `rm -rf /`") == "R3"
    assert risk_gate.classify_command("sudo rm -rf /") == "R3"
    assert risk_gate.classify_command("echo hola") == "R0"


def test_strip_wrappers_golden():
    assert risk_gate._strip_wrappers("sudo apt update") == "apt update"
    assert risk_gate._strip_wrappers("A=1 B=2 paccache -r") == "paccache -r"


# --- report diff temporal ---

def _finding(fid, status, title="T"):
    return {"id": fid, "category": "security", "severity": "P1", "title": title,
            "description": "d", "control": fid, "status": status,
            "evidence": "e", "remediation": "r", "risk_level": "R1"}


def test_diff_findings_categorias():
    prev = [_finding("A", "FAIL"), _finding("B", "FAIL"), _finding("C", "PASS")]
    curr = [_finding("A", "FAIL"), _finding("B", "PASS"), _finding("C", "FAIL"),
            _finding("D", "WARN")]
    diff = report_render.diff_findings(prev, curr)
    assert any("A" in x for x in diff["persistentes"])
    assert any("B" in x for x in diff["resueltos"])
    assert any("C" in x for x in diff["regresados"])
    assert any("D" in x for x in diff["nuevos"])


def test_diff_findings_vacio():
    assert report_render.diff_findings([], []) == {"nuevos": [], "resueltos": [],
                                                   "persistentes": [], "regresados": []}


def test_render_markdown_con_diff(tmp_path):
    prev = {"findings": [_finding("A", "FAIL", "Viejo")]}
    curr = {"metadata": {"timestamp": "t", "hostname": "h", "mode": "m",
                         "distro": "d", "family": "f", "kernel": "k",
                         "duration_seconds": 1},
            "health_score": {"overall": 50, "security": 50, "updates": 50,
                             "hygiene": 50, "resources": 50},
            "findings": [_finding("A", "PASS", "Viejo"), _finding("B", "FAIL", "Nuevo")],
            "summary": {"total_checks": 2, "passed": 1, "failed": 1, "warned": 0,
                        "skipped": 0, "errors": 0,
                        "by_severity": {"P0": 0, "P1": 2, "P2": 0, "P3": 0, "P4": 0}}}
    md = report_render.render_markdown(curr, prev_data=prev)
    assert "Diff temporal" in md and "Resueltos" in md and "Nuevos" in md


# --- snapshot rollback ---

def _fake_snapshot(tmp_path):
    base = tmp_path / "snaps"
    snap = base / "snap-1"
    snap.mkdir(parents=True)
    (snap / "metadata.json").write_text(json.dumps({"timestamp": "t"}), encoding="utf-8")
    (snap / "etc-checksums.txt").write_text("d41d8cfd4ccd0f2b  /etc/fake-test-xyz.conf\n",
                                            encoding="utf-8")
    return str(base)


def test_snapshot_list_y_rollback_dryrun(tmp_path):
    base = _fake_snapshot(tmp_path)
    assert snapshot_state.main(["--list", "--snapshot-dir", base]) == 0
    # /etc/fake-test-xyz.conf no existe -> missing, dry-run OK
    assert snapshot_state.main(["--rollback", "snap-1", "--snapshot-dir", base]) == 0


def test_snapshot_rollback_inexistente(tmp_path):
    base = _fake_snapshot(tmp_path)
    assert snapshot_state.main(["--rollback", "no-existe", "--snapshot-dir", base]) == 1
    assert snapshot_state.main(["--rollback", "con/barra", "--snapshot-dir", base]) == 2


def test_diff_snapshot_missing(tmp_path):
    base = _fake_snapshot(tmp_path)
    changed, missing, total = snapshot_state.diff_snapshot(base, "snap-1")
    assert total == 1 and changed == [] and missing == ["/etc/fake-test-xyz.conf"]
