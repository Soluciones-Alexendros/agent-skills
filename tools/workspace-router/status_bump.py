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
    bump_product_version: bool = False,
    evidence_ok: bool = False,
) -> dict[str, Any]:
    """Advance bookkeeping. Product SemVer is unchanged unless bump_product_version.

    Completing a real phase requires evidence_ok=True. Otherwise raises.
    """
    if phase not in PHASES:
        raise ValueError(f"unknown phase {phase!r}")
    if not evidence_ok:
        raise ValueError(
            "refusing status advance without evidence_ok=True "
            "(simulated/awaiting_agent/blocked must not complete a phase)"
        )
    root = Path(repo).resolve()
    data = load_status(root)
    product_version = str(data.get("version") or "0.1.0")
    if bump_product_version:
        kind = bump_kind_for_phase(phase)
        product_version = _bump_semver(product_version, kind)
    state_revision = int(data.get("state_revision") or 0) + 1
    advance = int(data.get("advance") or 0) + 1
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    entry = {
        "advance": advance,
        "version": product_version,
        "state_revision": state_revision,
        "phase": phase,
        "skill": skill,
        "at": now,
        "note": note,
        "evidence_ok": evidence_ok,
    }
    history = list(data.get("history") or [])
    history.append(entry)
    # Summarized history may trim; evidence_log retains checksums without dropping the only proof.
    evidence_log = list(data.get("evidence_log") or [])
    if checksum_spec:
        evidence_log.append(
            {"state_revision": state_revision, "checksum_spec": checksum_spec, "at": now, "phase": phase}
        )
    data.update(
        {
            "schema_version": 1,
            "version": product_version,
            "state_revision": state_revision,
            "phase": phase,
            "advance": advance,
            "last_skill": skill,
            "checksum_spec": checksum_spec or data.get("checksum_spec") or "",
            "updated_at": now,
            "history": history[-50:],
            "evidence_log": evidence_log,
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
