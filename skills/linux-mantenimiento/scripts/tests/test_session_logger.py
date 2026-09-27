"""Tests session_logger.py: --help, inválidos, error I/O -> 1, dorada log_event."""
import os
import subprocess
import sys

import session_logger

SCRIPT = "session_logger.py"


def _run(*args, env=None):
    import os as _os
    e = dict(_os.environ)
    if env:
        e.update(env)
    return subprocess.run(
        [sys.executable, SCRIPT, *args], capture_output=True, text=True, cwd=".", env=e,
    )


def test_help_exit0():
    r = _run("--help")
    assert r.returncode == 0


def test_invalid_args_exit2():
    r = _run("--opcion-invalida-xyz")
    assert r.returncode == 2


def test_main_crea_log_en_tmp(tmp_path):
    logdir = str(tmp_path / "logs")
    r = _run("--log-dir", logdir, "--session-id", "test-sess-1")
    assert r.returncode == 0
    logf = os.path.join(logdir, "test-sess-1.log")
    assert os.path.isfile(logf)
    content = open(logf, encoding="utf-8").read()
    assert "mantenimiento-linux session log" in content
    assert "SESSION_ID: test-sess-1" in content


def test_error_io_exit1(monkeypatch):
    def _boom(*a, **k):
        raise OSError("disco simulado")
    monkeypatch.setattr(session_logger.os, "makedirs", _boom)
    assert session_logger.main(["--log-dir", "/tmp/irrelevante-xyz", "--session-id", "s"]) == 1


def test_log_event_golden(tmp_path, monkeypatch):
    logdir = str(tmp_path / "logs2")
    monkeypatch.setattr(session_logger, "LOG_DIR", logdir)
    monkeypatch.setattr(session_logger, "SESSION_ID", "gold-1")
    monkeypatch.setattr(session_logger, "LOG_FILE", os.path.join(logdir, "gold-1.log"))
    session_logger.log_event("GATE", "R0", "echo hola", "ALLOW", "detalle-x")
    content = open(os.path.join(logdir, "gold-1.log"), encoding="utf-8").read()
    assert "[GATE]" in content and "echo hola" in content and "detalle-x" in content
    assert session_logger.get_log_file().endswith("gold-1.log")
    assert session_logger.get_session_id() == "gold-1"
