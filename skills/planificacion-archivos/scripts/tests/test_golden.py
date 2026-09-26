"""Golden tests: pure fns of session-catchup.py + route logic (tmp_path only)."""
import importlib.util
import os
import subprocess
import time
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1]


def load_py():
    spec = importlib.util.spec_from_file_location(
        "session_catchup", str(SCRIPTS / "session-catchup.py")
    )
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _env(tmp_path, extra=None):
    env = dict(os.environ)
    for k in ("PLAN_ID", "PWF_PLAN_ROOT", "PWF_SESSION_ID", "PWF_INJECT", "PLANNING_DISABLED"):
        env.pop(k, None)
    env["HOME"] = str(tmp_path)
    env["XDG_CACHE_HOME"] = str(tmp_path / ".cache")
    if extra:
        env.update(extra)
    return env


# ---- session-catchup pure functions ----

def test_normalize_path_gitbash():
    sc = load_py()
    assert sc.normalize_path("/c/Users/x/proj") == "C:/Users/x/proj"
    assert sc.normalize_path("/d/data") == "D:/data"


def test_claude_sanitize_basic_and_astral():
    sc = load_py()
    assert sc._claude_sanitize("a b/c") == "a-b-c"
    assert sc._claude_sanitize("a_b-c") == "a_b-c"
    emoji = "\U0001f600"  # ord > 0xFFFF
    assert sc._claude_sanitize(emoji, 2) == "--"
    assert sc._claude_sanitize(emoji, 1) == "-"


def test_planning_file_from_path():
    sc = load_py()
    assert sc.planning_file_from_path("/x/task_plan.md") == "task_plan.md"
    assert sc.planning_file_from_path("C:\\w\\progress.md") == "progress.md"
    assert sc.planning_file_from_path("/x/findings.md") == "findings.md"
    assert sc.planning_file_from_path("/x/other.md") is None
    assert sc.planning_file_from_path(None) is None
    assert sc.planning_file_from_path(123) is None


def test_planning_file_from_paths_priority():
    sc = load_py()
    assert sc.planning_file_from_paths(["/a/progress.md", "/a/task_plan.md"]) == "task_plan.md"
    assert sc.planning_file_from_paths(["/a/notes.md"]) is None


def test_result_excerpt_and_annotation():
    sc = load_py()
    assert sc.result_excerpt("  hello\nworld") == "hello"
    assert sc.result_excerpt("") == ""
    assert sc.result_excerpt(None) == ""
    long_line = "x" * 300
    assert len(sc.result_excerpt(long_line)) <= 80
    assert sc.result_annotation(False, "anything") == " -> ok"
    assert sc.result_annotation(True, "boom line\nsecond") == " -> FAILED (boom line)"
    assert sc.result_annotation(True, "") == " -> FAILED"


def test_text_content_shapes():
    sc = load_py()
    assert sc.text_content("hi") == "hi"
    assert sc.text_content([{"text": "a"}, {"text": "b"}]) == "a\nb"
    assert sc.text_content([{"nope": 1}]) == ""
    assert sc.text_content(None) == ""
    assert sc.text_content(123) == ""


def test_same_project_path_self():
    sc = load_py()
    assert sc.same_project_path("/tmp/a", "/tmp/a") is True
    assert sc.same_project_path("/tmp/a", "/tmp/b") is False


def test_find_last_planning_update_golden():
    sc = load_py()
    msgs = [
        {"_line_num": 0, "type": "assistant",
         "message": {"content": [{"type": "tool_use", "name": "Write",
                                  "input": {"file_path": "/p/task_plan.md"}}]}},
        {"_line_num": 1, "type": "assistant",
         "message": {"content": [{"type": "tool_use", "name": "Bash",
                                  "input": {"command": "ls"}}]}},
        {"_line_num": 2, "type": "assistant",
         "message": {"content": [{"type": "tool_use", "name": "Edit",
                                  "input": {"file_path": "/p/progress.md"}}]}},
        {"_line_num": 3, "type": "user", "message": {"content": "hi"}},
    ]
    line, fname = sc.find_last_planning_update(msgs)
    assert (line, fname) == (2, "progress.md")
    line, fname = sc.find_last_planning_update([{"_line_num": 0, "type": "user"}])
    assert (line, fname) == (-1, None)


def test_main_returns_int_and_empty_ok(tmp_path):
    sc = load_py()
    empty = tmp_path / "proj"
    empty.mkdir()
    assert sc.main([str(empty)]) == 0
    assert sc.main([str(tmp_path / "missing")]) == 1


# ---- resolve-plan-dir route logic (tmp_path) ----

def _mk_plan(root: Path, slug: str):
    d = root / ".planning" / slug
    d.mkdir(parents=True)
    (d / "task_plan.md").write_text("# t\n", encoding="utf-8")
    return d


def _run_resolver(tmp_path, extra=None, args=()):
    return subprocess.run(
        ["bash", str(SCRIPTS / "resolve-plan-dir.sh")] + list(args),
        capture_output=True, text=True, timeout=15,
        cwd=str(tmp_path), env=_env(tmp_path, extra),
    )


def test_resolve_plan_id_env_wins(tmp_path):
    _mk_plan(tmp_path, "aaa")
    b = _mk_plan(tmp_path, "bbb")
    (tmp_path / ".planning" / ".active_plan").write_text("aaa\n", encoding="utf-8")
    r = _run_resolver(tmp_path, {"PLAN_ID": "bbb"})
    assert r.returncode == 0
    assert r.stdout.strip() == str(b)


def test_resolve_active_file_and_newest(tmp_path):
    a = _mk_plan(tmp_path, "aaa")
    time.sleep(0.05)
    b = _mk_plan(tmp_path, "bbb")
    os.utime(b, (time.time() + 5, time.time() + 5))
    (tmp_path / ".planning" / ".active_plan").write_text("aaa\n", encoding="utf-8")
    r = _run_resolver(tmp_path)
    assert r.stdout.strip() == str(a)
    (tmp_path / ".planning" / ".active_plan").unlink()
    r = _run_resolver(tmp_path)
    assert r.stdout.strip() == str(b)


def test_resolve_rejects_traversal_and_garbage(tmp_path):
    _mk_plan(tmp_path, "good")
    for bad in ("../escape", "..", "", "  ", "a/b"):
        r = _run_resolver(tmp_path, {"PLAN_ID": bad})
        assert r.stdout.strip() != str(tmp_path / ".planning" / bad)
        assert ".." not in r.stdout
    (tmp_path / ".planning" / ".active_plan").write_text("   \n", encoding="utf-8")
    r = _run_resolver(tmp_path)
    # garbage pointer falls through to newest valid dir
    assert r.stdout.strip() == str(tmp_path / ".planning" / "good")


def test_resolve_pwf_plan_root_pin(tmp_path):
    outer = tmp_path / "outer"
    inner = tmp_path / "outer" / "inner"
    inner.mkdir(parents=True)
    _mk_plan(inner, "pinned")
    _mk_plan(outer, "parentplan")
    r = subprocess.run(
        ["bash", str(SCRIPTS / "resolve-plan-dir.sh")],
        capture_output=True, text=True, timeout=15, cwd=str(outer),
        env=_env(tmp_path, {"PWF_PLAN_ROOT": str(inner)}),
    )
    assert r.returncode == 0
    assert r.stdout.strip() == str(inner / ".planning" / "pinned")


# ---- init-session route logic (tmp_path) ----

def test_init_session_slug_and_legacy(tmp_path):
    work = tmp_path / "work"
    work.mkdir()
    r = subprocess.run(
        ["bash", str(SCRIPTS / "init-session.sh"), "Hello World!"],
        capture_output=True, text=True, timeout=20,
        cwd=str(work), env=_env(work),
    )
    assert r.returncode == 0
    plans = list((work / ".planning").glob("*-hello-world"))
    assert len(plans) == 1
    assert (plans[0] / "task_plan.md").exists()
    assert (plans[0] / "findings.md").exists()
    assert (plans[0] / "progress.md").exists()
    active = (work / ".planning" / ".active_plan").read_text(encoding="utf-8").strip()
    assert active == plans[0].name
    # resolver sees it
    r2 = subprocess.run(
        ["bash", str(SCRIPTS / "resolve-plan-dir.sh")],
        capture_output=True, text=True, timeout=15,
        cwd=str(work), env=_env(work),
    )
    assert r2.stdout.strip() == str(plans[0])

    legacy = tmp_path / "legacy"
    legacy.mkdir()
    r = subprocess.run(
        ["bash", str(SCRIPTS / "init-session.sh")],
        capture_output=True, text=True, timeout=20,
        cwd=str(legacy), env=_env(legacy),
    )
    assert r.returncode == 0
    assert (legacy / "task_plan.md").exists()


def test_init_session_autonomous_sidecars(tmp_path):
    work = tmp_path / "auto"
    work.mkdir()
    r = subprocess.run(
        ["bash", str(SCRIPTS / "init-session.sh"), "--autonomous", "Auto Run"],
        capture_output=True, text=True, timeout=20,
        cwd=str(work), env=_env(work),
    )
    assert r.returncode == 0
    plans = list((work / ".planning").glob("*-auto-run"))
    assert len(plans) == 1
    assert (plans[0] / ".mode").read_text(encoding="utf-8").strip() == "autonomous"
    assert (plans[0] / ".nonce").exists()
    assert (plans[0] / ".attestation").exists()


# ---- attest / phase-status / ledger roundtrip (tmp_path) ----

def test_attest_and_phase_status_roundtrip(tmp_path):
    work = tmp_path / "rt"
    work.mkdir()
    subprocess.run(["bash", str(SCRIPTS / "init-session.sh")],
                   cwd=str(work), env=_env(work), timeout=20, check=True)
    r = subprocess.run(["bash", str(SCRIPTS / "attest-plan.sh")],
                       capture_output=True, text=True, timeout=15,
                       cwd=str(work), env=_env(work))
    assert r.returncode == 0
    assert (work / ".plan-attestation").exists()
    r = subprocess.run(["bash", str(SCRIPTS / "attest-plan.sh"), "--show"],
                       capture_output=True, text=True, timeout=15,
                       cwd=str(work), env=_env(work))
    assert r.returncode == 0 and "SHA-256" in r.stdout
    r = subprocess.run(["bash", str(SCRIPTS / "phase-status.sh"), "1", "complete"],
                       capture_output=True, text=True, timeout=15,
                       cwd=str(work), env=_env(work))
    assert r.returncode == 0
    content = (work / "task_plan.md").read_text(encoding="utf-8")
    assert "**Status:** complete" in content
    r = subprocess.run(["bash", str(SCRIPTS / "ledger-append.sh"),
                        "progress", "golden summary", "--agent", "main"],
                       capture_output=True, text=True, timeout=15,
                       cwd=str(work), env=_env(work))
    assert r.returncode == 0
    assert (work / "ledger-main.jsonl").exists()
    r = subprocess.run(["bash", str(SCRIPTS / "ledger-summary.sh")],
                       capture_output=True, text=True, timeout=15,
                       cwd=str(work), env=_env(work))
    assert r.returncode == 0 and "=== RUN LEDGER ===" in r.stdout
    r = subprocess.run(["bash", str(SCRIPTS / "check-complete.sh")],
                       capture_output=True, text=True, timeout=15,
                       cwd=str(work), env=_env(work))
    assert r.returncode == 0
