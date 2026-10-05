#!/usr/bin/env python3
"""Build skill-index.json from skills/*/SKILL.md frontmatter.

Triggers are sourced from tools/skill-router/intent-map.yaml so the
deterministic router (route.py) can boost on Spanish/English intent
patterns. Output is sorted by skill name for stable diffs.
"""
import pathlib, yaml, json
root = pathlib.Path("skills")

# skill name -> list of trigger patterns from intent-map.yaml
triggers_by_skill: dict[str, list[str]] = {}
intent_map = pathlib.Path("tools/skill-router/intent-map.yaml")
if intent_map.exists():
    intents = (yaml.safe_load(intent_map.read_text(encoding="utf-8")) or {}).get("intents", {})
    for intent in intents.values():
        for skill in intent.get("skills", []):
            triggers_by_skill.setdefault(skill, []).extend(intent.get("patterns", []))

skills = []
for md in sorted(root.glob("*/SKILL.md")):
    text = md.read_text(encoding="utf-8")
    try:
        fm = yaml.safe_load(text.split("---")[1])
    except Exception as e:
        print(f"skip {md}: {e}")
        continue
    if not isinstance(fm, dict):
        print(f"skip {md}: frontmatter is not a mapping")
        continue
    meta = fm.get("metadata",{})
    skills.append({
        "name": fm.get("name", md.parent.name),
        "description": fm.get("description","")[:1000],
        "domain": meta.get("domain",""),
        "type": meta.get("type","atomic"),
        "language": meta.get("language","es"),
        "keywords": [k.strip() for k in meta.get("keywords","").split(",") if k.strip()],
        "triggers": sorted(set(triggers_by_skill.get(fm.get("name", md.parent.name), []))),
        "entry": f"skills/{md.parent.name}/SKILL.md",
        "compatibility": fm.get("compatibility","opencode, codex, cursor")
    })
out = {"version":"3.0.0","skills": skills}
pathlib.Path("skill-index.json").write_text(
    json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
)
print(f"Built index with {len(skills)} skills")
