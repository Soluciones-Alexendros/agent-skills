"""Declarative status bump for .autoworkspace/status.yaml."""
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    raise SystemExit("PyYAML required: pip install -r requirements-dev.txt") from exc

PHASES = ("DEFINE", "SCHEMAS", "IMPLEMENT", "VALIDATE", "INTEGRATE", "STATUS")


def status_path(repo: Path) -> Path:
    return Path(repo).resolve() / ".autoworkspace" / "status.yaml"


def load_status(repo: Path | str) -> dict[str, Any]:
    path = status_path(Path(repo))
    if not path.is_file():
        return {
            "schema_version": 1,
            "version": "0.1.0",
            "phase": "DEFINE",
            "advance": 0,
            "last_skill": "",
            "checksum_spec": "",
            "updated_at": "",
            "history": [],
        }
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise ValueError("status.yaml must be a mapping")
    return data


def _bump_semver(version: str, kind: str) -> str:
    parts = version.strip().split(".")
    while len(parts) < 3:
        parts.append("0")
    major, minor, patch = (int(parts[0]), int(parts[1]), int(parts[2]))
    if kind == "major":
        return f"{major + 1}.0.0"
    if kind == "minor":
        return f"{major}.{minor + 1}.0"
    return f"{major}.{minor}.{patch + 1}"


def bump_kind_for_phase(phase: str) -> str:
    # Completing INTEGRATE → minor; STATUS bookkeeping → patch; earlier phases → patch
    if phase == "INTEGRATE":
        return "minor"
    return "patch"


def advance_status(
    repo: Path | str,
    *,
    phase: str,
    skill: str = "",
    checksum_spec: str = "",
    note: str = "",
    write: bool = True,
) -> dict[str, Any]:
    if phase not in PHASES:
        raise ValueError(f"unknown phase {phase!r}")
    root = Path(repo).resolve()
    data = load_status(root)
    kind = bump_kind_for_phase(phase)
    new_version = _bump_semver(str(data.get("version") or "0.1.0"), kind)
    advance = int(data.get("advance") or 0) + 1
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    entry = {
        "advance": advance,
        "version": new_version,
        "phase": phase,
        "skill": skill,
        "at": now,
        "note": note,
    }
    history = list(data.get("history") or [])
    history.append(entry)
    data.update(
        {
            "schema_version": 1,
            "version": new_version,
            "phase": phase,
            "advance": advance,
            "last_skill": skill,
            "checksum_spec": checksum_spec or data.get("checksum_spec") or "",
            "updated_at": now,
            "history": history[-50:],  # keep last 50
        }
    )
    if write:
        path = status_path(root)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            yaml.safe_dump(data, sort_keys=False, allow_unicode=True),
            encoding="utf-8",
        )
    return data
