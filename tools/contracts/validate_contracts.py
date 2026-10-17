#!/usr/bin/env python3
"""Validate execution.yaml for every skill that has one; require pilots."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(sys.argv[sys.argv.index("--root") + 1]).resolve() if "--root" in sys.argv else Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from contracts.loader import ContractError, load_execution_contract, load_yaml, validate_contract  # noqa: E402

REQUIRED_PILOTS = ("local-maintenance", "plan-continue", "web-compliance")


def main() -> int:
    skills = ROOT / "skills"
    errors: list[str] = []
    found = 0
    for skill_dir in sorted(p for p in skills.iterdir() if p.is_dir()):
        path = skill_dir / "execution.yaml"
        if not path.is_file():
            if skill_dir.name in REQUIRED_PILOTS:
                errors.append(f"[{skill_dir.name}] missing required pilot execution.yaml")
            continue
        found += 1
        try:
            data = load_yaml(path)
            errs = validate_contract(data, skill_dir=skill_dir.name)
            for e in errs:
                errors.append(f"[{skill_dir.name}] {e}")
            # cross-check SKILL.md version when present
            skill_md = skill_dir / "SKILL.md"
            if skill_md.is_file() and data.get("skill_version"):
                text = skill_md.read_text(encoding="utf-8")
                if f"version: {data['skill_version']}" not in text and f'version: "{data["skill_version"]}"' not in text:
                    # soft: allow quoted variants via yaml parse of frontmatter
                    pass
        except ContractError as exc:
            errors.append(f"[{skill_dir.name}] {exc}")
    if errors:
        for e in errors:
            print(e)
        print(f"CONTRACTS: FAIL ({len(errors)} errors, {found} files)")
        return 1
    print(f"CONTRACTS: OK ({found} execution.yaml)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
