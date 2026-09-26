"""--help exit 0 for every .sh + session-catchup.py (subprocess, timeout)."""
import subprocess
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1]
SH_SCRIPTS = [
    "attest-plan.sh",
    "check-complete.sh",
    "gate-stop.sh",
    "init-session.sh",
    "inject-plan.sh",
    "ledger-append.sh",
    "ledger-summary.sh",
    "phase-status.sh",
    "plan-doctor.sh",
    "resolve-plan-dir.sh",
    "set-active-plan.sh",
]


def _env_isolated(tmp_path):
    env = dict(__import__("os").environ)
    for k in ("PLAN_ID", "PWF_PLAN_ROOT", "PWF_SESSION_ID", "PWF_INJECT", "PLANNING_DISABLED"):
        env.pop(k, None)
    env["HOME"] = str(tmp_path)
    env["XDG_CACHE_HOME"] = str(tmp_path / ".cache")
    return env


def test_sh_help_exit_0(tmp_path):
    for name in SH_SCRIPTS:
        script = SCRIPTS / name
        assert script.exists(), f"missing {name}"
        for flag in ("--help", "-h"):
            r = subprocess.run(
                ["bash", str(script), flag],
                capture_output=True, text=True, timeout=15,
                cwd=str(tmp_path), env=_env_isolated(tmp_path),
            )
            assert r.returncode == 0, f"{name} {flag} -> {r.returncode}: {r.stderr[:300]}"


def test_py_help_exit_0(tmp_path):
    r = subprocess.run(
        [sys.executable, str(SCRIPTS / "session-catchup.py"), "--help"],
        capture_output=True, text=True, timeout=15,
        cwd=str(tmp_path), env=_env_isolated(tmp_path),
    )
    assert r.returncode == 0
    assert "project" in r.stdout.lower()


def test_py_main_help_func():
    import importlib.util
    import pytest
    spec = importlib.util.spec_from_file_location(
        "session_catchup", str(SCRIPTS / "session-catchup.py")
    )
    assert spec is not None and spec.loader is not None
    sc = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(sc)
    with pytest.raises(SystemExit) as ei:
        sc.main(["--help"])
    assert ei.value.code == 0
