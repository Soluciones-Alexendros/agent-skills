"""Portable preflight: resolve skill root and check requirements without installing."""
from __future__ import annotations

import os
import shutil
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class PreflightResult:
    ok: bool
    blocked_reasons: list[str] = field(default_factory=list)
    optional_missing: list[str] = field(default_factory=list)
    skill_root: str | None = None
    workspace_root: str | None = None


def resolve_workspace_root(start: Path | None = None) -> Path | None:
    cur = (start or Path.cwd()).resolve()
    for p in [cur, *cur.parents]:
        if (p / ".git").exists() and (p / "skills").is_dir():
            return p
        if (p / "skills").is_dir() and (p / "tools" / "workspace-router").is_dir():
            return p
    return None


def resolve_skill_root(skill: str, workspace: Path | None = None) -> Path | None:
    ws = workspace or resolve_workspace_root()
    if ws is None:
        return None
    candidate = ws / "skills" / skill
    if (candidate / "SKILL.md").is_file():
        return candidate.resolve()
    return None


def check_binaries(required: list[str], optional: list[str] | None = None) -> PreflightResult:
    result = PreflightResult(ok=True)
    for b in required:
        if shutil.which(b) is None:
            result.ok = False
            result.blocked_reasons.append(f"missing required binary: {b}")
    for b in optional or []:
        if shutil.which(b) is None:
            result.optional_missing.append(b)
    return result


def preflight_contract(contract: dict[str, Any], *, cwd: Path | None = None) -> PreflightResult:
    dist = contract.get("distribution")
    skill = contract["skill"]
    result = PreflightResult(ok=True)
    ws = resolve_workspace_root(cwd)
    result.workspace_root = str(ws) if ws else None
    if dist == "workspace-required" and ws is None:
        result.ok = False
        result.blocked_reasons.append(
            "workspace-required skill: install full autoworkspace (skills/ + tools/); "
            "cwd is not an implicit installation"
        )
        return result
    skill_root = resolve_skill_root(skill, ws)
    if skill_root is None:
        # standalone copy: skill root is the directory containing execution.yaml next to SKILL.md
        result.ok = False
        result.blocked_reasons.append(f"skill root not found for {skill}")
        return result
    result.skill_root = str(skill_root)
    # Refuse reading outside skill/workspace for standalone verification
    if dist == "standalone":
        # Ensure we do not need ../../tools from original checkout
        tools_ref = skill_root / ".." / ".." / "tools"
        # informational only
        _ = tools_ref
    reqs = contract.get("system_requirements") or {}
    hard = list(reqs.get("binaries") or [])
    bin_check = check_binaries(hard)
    if not bin_check.ok:
        result.ok = False
        result.blocked_reasons.extend(bin_check.blocked_reasons)
    result.optional_missing.extend(bin_check.optional_missing)
    if reqs.get("network") and os.environ.get("AUTOWORKSPACE_ALLOW_NETWORK") != "1":
        # network required but not authorized → blocked for ops that need it; preflight warns
        result.optional_missing.append("network:not-authorized")
    return result
