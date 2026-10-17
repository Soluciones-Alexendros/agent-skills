"""Typed operation runner: argv only, shell=False, approval + timeout."""
from __future__ import annotations

import os
import signal
import subprocess
import time
from dataclasses import dataclass
from typing import Any

from execution.approval import (
    ApprovalRequest,
    DenyProvider,
    is_insufficient_token,
    plan_digest,
    provider_from_env,
)


@dataclass
class OpResult:
    operation_id: str
    outcome: str
    returncode: int | None
    duration_ms: int
    detail: str
    effect: str


SHELL_ESCAPES = {"bash", "sh", "dash", "zsh"}


def _reject_shell_escape(argv: list[str]) -> str | None:
    if not argv:
        return "empty argv"
    base = os.path.basename(argv[0])
    if base in SHELL_ESCAPES and len(argv) >= 2 and argv[1] in {"-c", "-lc"}:
        return "shell -c escape rejected"
    return None


def run_operation(
    *,
    operation_id: str,
    argv: list[str],
    effect: str,
    target: str,
    params: dict[str, Any] | None = None,
    timeout: int = 60,
    cwd: str | None = None,
    require_approval: bool = True,
) -> OpResult:
    params = params or {}
    # Never accept approved=true style tokens
    if is_insufficient_token(str(params.get("approved", ""))):
        params = {k: v for k, v in params.items() if k != "approved"}

    digest = plan_digest(operation_id, target, params, [effect])
    if effect in {"mutate-host", "communicate-external", "access-secret"} and require_approval:
        provider = provider_from_env()
        decision = provider.decide(
            ApprovalRequest(operation_id, target, params, (effect,), digest)
        )
        if not decision.allowed or decision.covers_digest != digest:
            return OpResult(
                operation_id,
                "blocked",
                None,
                0,
                decision.reason,
                effect,
            )

    bad = _reject_shell_escape(argv)
    if bad:
        return OpResult(operation_id, "blocked", 2, 0, bad, effect)

    start = time.monotonic()
    try:
        proc = subprocess.Popen(
            argv,
            shell=False,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            start_new_session=True,
        )
        try:
            stdout, stderr = proc.communicate(timeout=timeout)
        except subprocess.TimeoutExpired:
            os.killpg(proc.pid, signal.SIGKILL)
            proc.wait(timeout=5)
            return OpResult(
                operation_id,
                "cancelled",
                124,
                int((time.monotonic() - start) * 1000),
                "timeout; process group killed; reconcile before retry if external effects possible",
                effect,
            )
        rc = proc.returncode
        outcome = "succeeded" if rc == 0 else "failed"
        detail = (stderr or stdout or "")[:500]
        return OpResult(
            operation_id,
            outcome,
            rc,
            int((time.monotonic() - start) * 1000),
            detail,
            effect,
        )
    except OSError as exc:
        return OpResult(
            operation_id,
            "failed",
            127,
            int((time.monotonic() - start) * 1000),
            str(exc),
            effect,
        )


# Silence unused import lint for DenyProvider re-export convenience
_ = DenyProvider
