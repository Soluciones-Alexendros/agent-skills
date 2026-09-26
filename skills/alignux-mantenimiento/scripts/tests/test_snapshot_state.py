"""Tests snapshot_state.py: --help, inválidos, error dir -> 1, doradas puras."""
import hashlib
import os
import subprocess
import sys

import snapshot_state

SCRIPT = "snapshot_state.py"


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


def test_invalid_snapshot_id_exit2(tmp_path):
    r = _run("con/barra", "--snapshot-dir", str(tmp_path))
    assert r.returncode == 2


def test_error_snapshot_dir_es_fichero_exit1(tmp_path):
    blocker = tmp_path / "blocker"
    blocker.write_text("x", encoding="utf-8")
    assert snapshot_state.main(["snap-1", "--snapshot-dir", str(blocker)]) == 1


def test_md5_file_golden(tmp_path):
    p = tmp_path / "a.txt"
    p.write_bytes(b"abc")
    assert snapshot_state.md5_file(str(p)) == hashlib.md5(b"abc").hexdigest()
    assert snapshot_state.md5_file(str(tmp_path / "noexiste")) == ""


def test_write_text_roundtrip_golden(tmp_path):
    p = tmp_path / "w.txt"
    snapshot_state.write_text(str(p), "hola")
    assert p.read_text(encoding="utf-8") == "hola"


def test_detect_pkg_mgr_golden():
    mgr = snapshot_state.detect_pkg_mgr()
    assert isinstance(mgr, str)
