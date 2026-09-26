"""Invalid args -> 2, controlled errors -> 1. All in tmp_path, no real writes."""
import os
import subprocess
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1]


def _env(tmp_path, extra=None):
    env = dict(os.environ)
    for k in ("PLAN_ID", "PWF_PLAN_ROOT", "PWF_SESSION_ID", "PWF_INJECT", "PLANNING_DISABLED"):
        env.pop(k, None)
    env["HOME"] = str(tmp_path)
    env["XDG_CACHE_HOME"] = str(tmp_path / ".cache")
    if extra:
        env.update(extra)
    return env


def _run(name, args, tmp_path, extra=None):
    return subprocess.run(
        ["bash", str(SCRIPTS / name)] + args,
        capture_output=True, text=True, timeout=15,
        cwd=str(tmp_path), env=_env(tmp_path, extra),
    )


def test_invalid_args_exit_2(tmp_path):
    cases = [
        ("attest-plan.sh", ["--bogus"]),
        ("attest-plan.sh", ["--show", "--clear"]),
        ("check-complete.sh", ["--bogus"]),
        ("check-complete.sh", ["a.md", "b.md"]),
        ("gate-stop.sh", ["--bogus"]),
        ("gate-stop.sh", ["extra"]),
        ("init-session.sh", ["--bogus"]),
        ("init-session.sh", ["--template"]),
        ("inject-plan.sh", ["--bogus"]),
        ("inject-plan.sh", ["--context=bogus"]),
        ("inject-plan.sh", ["extra-positional"]),
        ("ledger-append.sh", []),
        ("ledger-append.sh", ["progress"]),
        ("ledger-append.sh", ["bad-event", "summary text"]),
        ("ledger-append.sh", ["progress", "s", "--bogus"]),
        ("ledger-summary.sh", ["--bogus"]),
        ("ledger-summary.sh", ["a", "b"]),
        ("phase-status.sh", []),
        ("phase-status.sh", ["1"]),
        ("phase-status.sh", ["1", "bogus"]),
        ("phase-status.sh", ["abc", "complete"]),
        ("phase-status.sh", ["1", "complete", "extra"]),
        ("plan-doctor.sh", ["--bogus"]),
        ("resolve-plan-dir.sh", ["--bogus"]),
        ("resolve-plan-dir.sh", ["a", "b"]),
        ("set-active-plan.sh", ["--bogus"]),
        ("set-active-plan.sh", ["a", "b"]),
        ("set-active-plan.sh", ["../escape"]),
    ]
    for name, args in cases:
        r = _run(name, args, tmp_path)
        assert r.returncode == 2, f"{name} {args} -> {r.returncode}: {r.stderr[:200]} {r.stdout[:200]}"


def test_py_invalid_args_exit_2(tmp_path):
    r = subprocess.run(
        [sys.executable, str(SCRIPTS / "session-catchup.py"), "--bogus-flag"],
        capture_output=True, text=True, timeout=15,
        cwd=str(tmp_path), env=_env(tmp_path),
    )
    assert r.returncode == 2


def test_controlled_errors_exit_1(tmp_path):
    # attest: no plan found
    r = _run("attest-plan.sh", [], tmp_path)
    assert r.returncode == 1
    # attest --show with no attestation (plan exists, no hash yet)
    (tmp_path / "task_plan.md").write_text("# plan\n", encoding="utf-8")
    r = _run("attest-plan.sh", ["--show"], tmp_path)
    assert r.returncode == 1
    # phase-status: no plan (fresh dir)
    fresh = tmp_path / "fresh"
    fresh.mkdir()
    r = subprocess.run(
        ["bash", str(SCRIPTS / "phase-status.sh"), "1", "complete"],
        capture_output=True, text=True, timeout=15,
        cwd=str(fresh), env=_env(fresh),
    )
    assert r.returncode == 1
    # phase-status: phase missing (plan exists, phase 99 absent)
    planed = tmp_path / "planed"
    planed.mkdir(exist_ok=True)
    (planed / "task_plan.md").write_text(
        "### Phase 1: A\n**Status:** pending\n", encoding="utf-8"
    )
    r = subprocess.run(
        ["bash", str(SCRIPTS / "phase-status.sh"), "99", "complete"],
        capture_output=True, text=True, timeout=15,
        cwd=str(planed), env=_env(planed),
    )
    assert r.returncode == 1
    # phase-status: corrupt plan (no **Status:** line for existing phase)
    corrupt = tmp_path / "corrupt"
    corrupt.mkdir(exist_ok=True)
    (corrupt / "task_plan.md").write_text(
        "### Phase 1: A\nno status line here\n", encoding="utf-8"
    )
    r = subprocess.run(
        ["bash", str(SCRIPTS / "phase-status.sh"), "1", "complete"],
        capture_output=True, text=True, timeout=15,
        cwd=str(corrupt), env=_env(corrupt),
    )
    assert r.returncode == 1
    # set-active-plan: dir inexistente
    r = _run("set-active-plan.sh", ["does-not-exist"], tmp_path)
    assert r.returncode == 1


def test_py_controlled_errors_exit_1(tmp_path):
    # dir inexistente
    r = subprocess.run(
        [sys.executable, str(SCRIPTS / "session-catchup.py"), str(tmp_path / "nope")],
        capture_output=True, text=True, timeout=15,
        cwd=str(tmp_path), env=_env(tmp_path),
    )
    assert r.returncode == 1
    # project_path is a file, not a dir
    f = tmp_path / "afile.txt"
    f.write_text("x", encoding="utf-8")
    r = subprocess.run(
        [sys.executable, str(SCRIPTS / "session-catchup.py"), str(f)],
        capture_output=True, text=True, timeout=15,
        cwd=str(tmp_path), env=_env(tmp_path),
    )
    assert r.returncode == 1
    # empty project (no planning files) -> 0, silent
    empty = tmp_path / "emptyproj"
    empty.mkdir(exist_ok=True)
    r = subprocess.run(
        [sys.executable, str(SCRIPTS / "session-catchup.py"), str(empty)],
        capture_output=True, text=True, timeout=15,
        cwd=str(tmp_path), env=_env(tmp_path),
    )
    assert r.returncode == 0


def test_graceful_zero_paths(tmp_path):
    # resolver with nothing -> 0 + empty stdout (never errors agent loop)
    r = _run("resolve-plan-dir.sh", [], tmp_path)
    assert r.returncode == 0
    assert r.stdout.strip() == ""
    # check-complete with no plan -> 0 advisory
    (tmp_path / "emptyproj").mkdir(exist_ok=True)
    r = subprocess.run(
        ["bash", str(SCRIPTS / "check-complete.sh")],
        capture_output=True, text=True, timeout=15,
        cwd=str(tmp_path / "emptyproj"), env=_env(tmp_path),
    )
    assert r.returncode == 0
    # inject-plan with no plan -> 0 silent
    r = subprocess.run(
        ["bash", str(SCRIPTS / "inject-plan.sh"), "--context=userprompt"],
        capture_output=True, text=True, timeout=15,
        cwd=str(tmp_path / "emptyproj"), env=_env(tmp_path),
    )
    assert r.returncode == 0
    assert r.stdout.strip() == ""
    # ledger-summary with missing resolver-less dir -> unavailable block, 0
    r = _run("ledger-summary.sh", [str(tmp_path / "nope")], tmp_path)
    assert r.returncode == 0
    assert "unavailable" in r.stdout
    # plan-doctor always 0
    r = _run("plan-doctor.sh", [], tmp_path)
    assert r.returncode == 0
    # gate-stop with no target plan -> 0 (legacy passthrough)
    r = subprocess.run(
        ["bash", str(SCRIPTS / "gate-stop.sh")],
        capture_output=True, text=True, timeout=15,
        cwd=str(tmp_path / "emptyproj"), env=_env(tmp_path),
    )
    assert r.returncode == 0
