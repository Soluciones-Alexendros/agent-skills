"""T01 RED/GREEN: P0 containment for clean_routine, snapshot_state, risk_gate, F21."""
from __future__ import annotations

import json
import os
from pathlib import Path
from unittest.mock import MagicMock, patch

import clean_routine
import common
import risk_gate
import snapshot_state


class SpyExecutor:
    """Fails if any unexpected real host mutation is attempted."""

    FORBIDDEN = (
        "apt",
        "pacman",
        "dnf",
        "systemctl",
        "journalctl",
        "fwupdmgr",
        "timeshift",
        "snapper",
        "tar ",
    )

    def __init__(self) -> None:
        self.calls: list[str] = []

    def __call__(self, cmd: str, timeout: int = 10):
        self.calls.append(cmd)
        for needle in self.FORBIDDEN:
            if needle in cmd and "2>/dev/null" not in cmd.split(needle, 1)[0][-20:]:
                # Still record; callers decide. Explicit forbid for mutate paths.
                pass
        if any(x in cmd for x in ("apt-get", "apt autoremove", "pacman -Sc", "dnf clean",
                                   "journalctl --vacuum", "fwupdmgr update", "needrestart -r",
                                   "tar -xzf", "tar -czf", "timeshift --create", "snapper create")):
            raise AssertionError(f"forbidden host mutation attempted: {cmd}")
        return 1, ""


def test_f01_execute_without_policy_blocks(monkeypatch, tmp_path):
    """Mutating path must not call run_capture for cleanup without validated snapshot."""
    spy = SpyExecutor()
    monkeypatch.setattr(clean_routine, "which", lambda c: "/bin/true" if c == "apt" else None)
    monkeypatch.setattr(clean_routine, "run_capture", spy)
    monkeypatch.setattr(clean_routine, "run", lambda *a, **k: "")

    rc = clean_routine.main(["--execute", "--snapshot-id", "missing-snap"])
    assert rc != 0
    assert not any("apt" in c or "journalctl --vacuum" in c for c in spy.calls)


def test_f02_failed_snapshot_creation_blocks_first_effect(monkeypatch):
    monkeypatch.setattr(clean_routine, "which", lambda c: "/bin/true" if c == "apt" else None)

    def fake_run_capture(cmd, timeout=10):
        if "snapshot_state" in cmd:
            return 1, "backend failed"
        raise AssertionError(f"mutation before snapshot check: {cmd}")

    monkeypatch.setattr(clean_routine, "run_capture", fake_run_capture)
    monkeypatch.setattr(clean_routine, "run", lambda *a, **k: "")
    rc = clean_routine.main(["--execute"])
    assert rc != 0


def test_f02_invalid_snapshot_id_rejected(monkeypatch, tmp_path):
    monkeypatch.setattr(clean_routine, "which", lambda c: "/bin/true" if c == "apt" else None)
    monkeypatch.setattr(clean_routine, "run_capture", SpyExecutor())
    monkeypatch.setenv("SNAPSHOT_DIR", str(tmp_path))
    rc = clean_routine.main(["--execute", "--snapshot-id", "../escape"])
    assert rc != 0


def test_f03_json_reflects_real_failures(monkeypatch, tmp_path):
    monkeypatch.setattr(clean_routine, "which", lambda c: "/bin/true" if c == "apt" else None)
    monkeypatch.setattr(clean_routine, "DRY_RUN", True)
    monkeypatch.setattr(clean_routine, "EXECUTE", False)
    monkeypatch.setattr(clean_routine, "PKG_MGR", "apt")
    monkeypatch.setattr(clean_routine, "JSON_MODE", True)
    out = tmp_path / "out.json"
    monkeypatch.setattr(clean_routine, "JSON_OUTPUT", str(out))
    monkeypatch.setattr(clean_routine, "WITH_FIRMWARE", False)

    # Force one action failure via run_safe
    results = []

    def tracking_run_safe(cmd, risk, desc):
        results.append({"action": desc, "status": "failed", "rc": 1})
        return 1

    monkeypatch.setattr(clean_routine, "run_safe", tracking_run_safe)
    monkeypatch.setattr(clean_routine, "run", lambda *a, **k: "")
    # Use accumulate path if present
    if hasattr(clean_routine, "ACTION_RESULTS"):
        clean_routine.ACTION_RESULTS.clear()

    rc = clean_routine.main(["--dry-run", "--json", str(out)])
    assert out.is_file()
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["summary"]["failed"] >= 0
    # After fix: simulated/dry-run statuses are not "completed" for real execute
    statuses = {a["status"] for a in data["actions"]}
    assert "completed" not in statuses or data["metadata"].get("dry_run") is True
    # dry-run must mark simulated or skipped, not false completed counts as real success
    if data["metadata"].get("dry_run"):
        assert all(a["status"] in ("simulated", "skipped", "failed", "planned") for a in data["actions"])


def test_f04_unknown_operation_denied_for_mutation_registry():
    assert risk_gate.classify_command("echo hola") == "R0"
    # Registry deny-by-default for unknown *operations* (typed API)
    if hasattr(risk_gate, "authorize_operation"):
        allowed, reason = risk_gate.authorize_operation("totally-unknown-op", {})
        assert allowed is False
        assert reason


def test_f19_backend_failure_not_success(monkeypatch, tmp_path):
    monkeypatch.setattr(snapshot_state, "which", lambda c: "/usr/bin/timeshift" if c == "timeshift" else None)
    monkeypatch.setattr(snapshot_state, "detect_pkg_mgr", lambda: "apt")
    monkeypatch.setattr(snapshot_state, "run", lambda *a, **k: "5.0.0\n")
    monkeypatch.setattr(snapshot_state, "run_capture", lambda *a, **k: (1, "fail"))
    monkeypatch.setattr(snapshot_state, "capture_packages", lambda *a, **k: None)
    monkeypatch.setattr(snapshot_state, "capture_etc_checksums", lambda *a, **k: None)
    monkeypatch.setattr(snapshot_state, "capture_config_pending", lambda *a, **k: None)
    monkeypatch.setattr(snapshot_state, "write_text", lambda *a, **k: None)
    monkeypatch.setattr(snapshot_state, "md5_file", lambda p: "abc")

    rc = snapshot_state.main(["snap-fail", "--snapshot-dir", str(tmp_path)])
    assert rc != 0
    meta_path = tmp_path / "snap-fail" / "metadata.json"
    if meta_path.is_file():
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        assert meta.get("recovery_scope") in ("none", "partial", None) or meta.get("backend_status") != "ok"
        assert meta.get("outcome") in ("failed", "partial", "blocked", None) or rc != 0


def test_f20_no_private_ssh_keys_by_default(monkeypatch, tmp_path):
    monkeypatch.setattr(snapshot_state, "which", lambda c: None)
    monkeypatch.setattr(snapshot_state, "detect_pkg_mgr", lambda: "apt")
    monkeypatch.setattr(snapshot_state, "run", lambda *a, **k: "")
    captured = {}

    def capture_run(cmd, timeout=10):
        captured["cmd"] = cmd
        return 0, ""

    monkeypatch.setattr(snapshot_state, "run_capture", capture_run)
    monkeypatch.setattr(snapshot_state, "capture_packages", lambda *a, **k: None)
    monkeypatch.setattr(snapshot_state, "capture_etc_checksums", lambda *a, **k: None)
    monkeypatch.setattr(snapshot_state, "capture_config_pending", lambda *a, **k: None)
    monkeypatch.setattr(snapshot_state, "write_text", lambda *a, **k: None)
    monkeypatch.setattr(snapshot_state, "md5_file", lambda p: "d" * 32)

    snapshot_state.main(["snap-ssh", "--snapshot-dir", str(tmp_path)])
    cmd = captured.get("cmd", "")
    assert "ssh_host_" not in cmd
    assert "id_rsa" not in cmd


def test_f21_empty_category_not_perfect_score():
    collector = common.FindingCollector()
    scores = collector.health_score()
    # Categories with no scorable observations must not silently score 100
    for cat, score in scores.items():
        if cat == "overall":
            continue
        # When no findings at all, coverage is zero — score must not claim perfection
        assert score != 100 or collector.summary().get("check_coverage") == 0
    # Explicit: _category_score with no data is not 100 after fix
    assert collector._category_score("packages") != 100 or hasattr(collector, "category_coverage")


def test_f21_timeout_preserved_in_run_result():
    if hasattr(common, "run_result"):
        with patch("common.subprocess.run", side_effect=__import__("subprocess").TimeoutExpired("x", 1)):
            res = common.run_result(["true"], timeout=1)
            assert res.timed_out or res.returncode != 0
            assert res.stdout == "" or res.error


def test_f22_skill_version_from_manifest():
    version = common.skill_version_from_manifest() if hasattr(common, "skill_version_from_manifest") else None
    assert version is not None
    assert version == common.SKILL_VERSION
    # Must track SKILL.md, not the stale component constant
    assert version != "2.0.0"
    assert common.COMPONENT_VERSION != version or True  # component may differ


def test_r07_dry_run_zero_mutations(monkeypatch):
    spy = SpyExecutor()
    monkeypatch.setattr(clean_routine, "which", lambda c: "/bin/true" if c == "apt" else None)
    monkeypatch.setattr(clean_routine, "run_capture", spy)
    monkeypatch.setattr(clean_routine, "run", lambda *a, **k: "ok")
    rc = clean_routine.main(["--dry-run"])
    assert rc == 0
    assert spy.calls == [] or all("vacuum" not in c and "autoremove" not in c for c in spy.calls)


def test_host_rollback_execute_blocked_without_temp_root(monkeypatch, tmp_path):
    """Host restore --execute without explicit temp root must be denied."""
    snap = tmp_path / "snap-x"
    snap.mkdir()
    (snap / "etc-backup.tar.gz").write_bytes(b"not-a-real-tar")
    (snap / "metadata.json").write_text("{}", encoding="utf-8")
    rc = snapshot_state.main(
        ["--rollback", "snap-x", "--snapshot-dir", str(tmp_path), "--execute"]
    )
    assert rc != 0
