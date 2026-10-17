"""Load and semantically validate skills/*/execution.yaml (local extension)."""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    raise SystemExit("PyYAML required") from exc

DIALECT = "autoworkspace.execution"
SCHEMA_VERSION = 1
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
EFFECTS = {
    "read",
    "write-workspace",
    "mutate-host",
    "communicate-external",
    "access-secret",
}
KINDS = {"agent", "script", "orchestrator"}
DISTRIBUTIONS = {"standalone", "workspace-required"}
TRI = {"yes", "no", "unknown"}
CRITICAL_KEYS = {
    "schema_version",
    "skill",
    "execution_kind",
    "distribution",
    "operations",
}


class ContractError(ValueError):
    pass


def _reject_duplicate_keys(loader: yaml.SafeLoader, node: yaml.nodes.MappingNode):
    mapping = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=False)
        if key in mapping:
            raise ContractError(f"duplicate YAML key: {key!r}")
        mapping[key] = loader.construct_object(value_node, deep=True)
    return mapping


class StrictLoader(yaml.SafeLoader):
    pass


StrictLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    _reject_duplicate_keys,
)


def load_yaml(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    if len(text) > 200_000:
        raise ContractError(f"{path}: contract too large")
    data = yaml.load(text, Loader=StrictLoader)
    if not isinstance(data, dict):
        raise ContractError(f"{path}: root must be a mapping")
    return data


def validate_contract(data: dict[str, Any], *, skill_dir: str) -> list[str]:
    errors: list[str] = []
    for key in CRITICAL_KEYS:
        if key not in data:
            errors.append(f"missing critical key: {key}")
    unknown_critical = [
        k
        for k in data
        if k
        not in {
            "schema_version",
            "dialect",
            "skill",
            "skill_version",
            "execution_kind",
            "distribution",
            "shared_dependencies",
            "system_requirements",
            "operations",
            "handoffs",
            "normative_sources",
            "automation_limits",
        }
    ]
    if unknown_critical:
        errors.append(f"unknown fields (reject critical unknown): {unknown_critical}")
    if data.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"unsupported schema_version: {data.get('schema_version')}")
    if data.get("dialect", DIALECT) != DIALECT:
        errors.append(f"unsupported dialect: {data.get('dialect')}")
    skill = data.get("skill")
    if not isinstance(skill, str) or not NAME_RE.match(skill):
        errors.append("skill id invalid")
    elif skill != skill_dir:
        errors.append(f"skill {skill!r} != directory {skill_dir!r}")
    if data.get("execution_kind") not in KINDS:
        errors.append("execution_kind invalid")
    if data.get("distribution") not in DISTRIBUTIONS:
        errors.append("distribution invalid")
    ops = data.get("operations")
    if not isinstance(ops, list) or not ops:
        errors.append("operations must be a non-empty list")
    else:
        seen = set()
        for op in ops:
            if not isinstance(op, dict):
                errors.append("operation must be mapping")
                continue
            oid = op.get("id")
            if oid in seen:
                errors.append(f"duplicate operation id: {oid}")
            seen.add(oid)
            if op.get("effect") not in EFFECTS:
                errors.append(f"operation {oid}: bad effect")
            if op.get("dry_run") not in TRI:
                errors.append(f"operation {oid}: dry_run must be yes|no|unknown")
            if op.get("idempotency") not in TRI:
                errors.append(f"operation {oid}: idempotency must be yes|no|unknown")
    for h in data.get("handoffs") or []:
        if not isinstance(h, dict) or "skill" not in h:
            errors.append("handoff missing skill")
            continue
        if not NAME_RE.match(str(h["skill"])):
            errors.append(f"handoff skill invalid: {h['skill']}")
    return errors


def load_execution_contract(skill_path: Path) -> dict[str, Any]:
    path = skill_path / "execution.yaml"
    if not path.is_file():
        raise ContractError(f"missing {path}")
    data = load_yaml(path)
    errs = validate_contract(data, skill_dir=skill_path.name)
    if errs:
        raise ContractError("; ".join(errs))
    return data
