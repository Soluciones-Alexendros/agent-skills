#!/usr/bin/env python3
"""Autoworkspace router: phase → skill handoff using project.yaml variables."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from project_load import (  # noqa: E402
    PHASES,
    ProjectConfigError,
    filter_skills,
    handoff_for_phase,
    load_project,
)
from status_bump import advance_status, load_status  # noqa: E402


def load_catalog() -> list[str]:
    index = ROOT / "skill-index.json"
    if not index.is_file():
        skills_dir = ROOT / "skills"
        return sorted(p.name for p in skills_dir.iterdir() if p.is_dir() and (p / "SKILL.md").is_file())
    data = json.loads(index.read_text(encoding="utf-8"))
    return [s["name"] for s in data.get("skills", [])]


def ensure_scaffold(repo: Path) -> None:
    aw = repo / ".autoworkspace"
    aw.mkdir(parents=True, exist_ok=True)
    (aw / "schemas").mkdir(exist_ok=True)
    tmpl = ROOT / "templates" / "autoworkspace"
    for name in ("project.yaml", "status.yaml"):
        dest = aw / name
        if not dest.is_file():
            dest.write_text((tmpl / name).read_text(encoding="utf-8"), encoding="utf-8")


def route(repo: Path, phase: str, *, bump: bool, note: str) -> dict:
    ensure_scaffold(repo)
    try:
        project = load_project(repo)
    except ProjectConfigError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(2)
    catalog = load_catalog()
    allowed = filter_skills(catalog, project)
    skill = handoff_for_phase(project, phase)
    if skill and skill not in allowed and allowed:
        # fall back to first allowed with same domain prefix if filtered out
        prefix = skill.split("-", 1)[0]
        alt = next((s for s in allowed if s.startswith(prefix + "-")), None)
        skill = alt or skill
    result = {
        "repo": str(repo),
        "phase": phase,
        "skill": skill,
        "allowed_skills": allowed,
        "profile": project.get("profile"),
        "handoffs": project.get("handoffs") or {},
    }
    if bump:
        status = advance_status(repo, phase=phase, skill=skill or "", note=note)
        result["status"] = {
            "version": status["version"],
            "advance": status["advance"],
            "phase": status["phase"],
        }
    else:
        result["status"] = {
            "version": load_status(repo).get("version"),
            "advance": load_status(repo).get("advance"),
            "phase": load_status(repo).get("phase"),
        }
    return result


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Autoworkspace phase router")
    ap.add_argument("--repo", default=".", help="Target repository path")
    ap.add_argument(
        "--phase",
        required=True,
        choices=PHASES,
        help="Pipeline phase",
    )
    ap.add_argument(
        "--bump",
        action="store_true",
        help="Advance status.yaml after routing",
    )
    ap.add_argument("--note", default="", help="Optional status history note")
    ap.add_argument("--json", action="store_true", help="JSON output")
    args = ap.parse_args(argv)
    repo = Path(args.repo).resolve()
    if not repo.is_dir():
        print(f"ERROR: not a directory: {repo}", file=sys.stderr)
        return 2
    out = route(repo, args.phase, bump=args.bump, note=args.note)
    if args.json:
        print(json.dumps(out, ensure_ascii=False, indent=2))
    else:
        print(f"phase={out['phase']} skill={out['skill']} profile={out['profile']}")
        print(f"status version={out['status'].get('version')} advance={out['status'].get('advance')}")
        print(f"allowed={len(out['allowed_skills'])} skills")
        print(f"→ invoke skill tool / read skills/{out['skill']}/SKILL.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
