"""Execution ops and approval boundary tests."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))

from execution.approval import DenyProvider, is_insufficient_token, plan_digest  # noqa: E402
from execution.ops import run_operation  # noqa: E402
from execution.preflight import check_binaries, resolve_workspace_root  # noqa: E402


def test_deny_provider_blocks_mutation():
    from execution.approval import ApprovalRequest

    d = DenyProvider().decide(
        ApprovalRequest("clean_routine", "/tmp", {}, ("mutate-host",), "abc")
    )
    assert d.allowed is False


def test_insufficient_tokens():
    assert is_insufficient_token("approved=true")
    assert is_insufficient_token("true")
    assert is_insufficient_token("1")


def test_shell_c_rejected():
    r = run_operation(
        operation_id="x",
        argv=["bash", "-c", "echo hi"],
        effect="read",
        target=".",
        require_approval=False,
    )
    assert r.outcome == "blocked"
    assert "shell" in r.detail


def test_mutate_blocked_without_approval(monkeypatch):
    monkeypatch.setenv("AUTOWORKSPACE_APPROVAL_PROVIDER", "deny")
    r = run_operation(
        operation_id="clean_journal",
        argv=["true"],
        effect="mutate-host",
        target="/",
        require_approval=True,
    )
    assert r.outcome == "blocked"


def test_preflight_missing_binary():
    r = check_binaries(["definitely-not-a-real-binary-xyz"])
    assert r.ok is False


def test_resolve_workspace():
    assert resolve_workspace_root(ROOT) == ROOT.resolve()


def test_digest_stable():
    a = plan_digest("op", "t", {"x": 1}, ["read"])
    b = plan_digest("op", "t", {"x": 1}, ["read"])
    assert a == b
