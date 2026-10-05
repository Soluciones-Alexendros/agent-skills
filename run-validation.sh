#!/bin/bash
# v3.0 Validation — OpenCode-first, multi-harness, legacy-vendor-free.
#
# Usage: bash run-validation.sh [--pytest-only] [--smoke-only]
#   default: full gate. --pytest-only: only [6]. --smoke-only: only [5].
#   both flags: [5] + [6] (fast CI path used by `npm test`).
set -e

ONLY_PYTEST=0
ONLY_SMOKE=0
for arg in "$@"; do
  case "$arg" in
    --pytest-only) ONLY_PYTEST=1 ;;
    --smoke-only) ONLY_SMOKE=1 ;;
  esac
done
FULL=1
if [ "$ONLY_PYTEST" = 1 ] || [ "$ONLY_SMOKE" = 1 ]; then FULL=0; fi

echo "=== v3.0 Validation — OpenCode-first, multi-harness ==="

if [ "$FULL" = 1 ]; then
echo "[0] Legacy-harness hygiene (scoped)"
python3 - <<'PY'
import subprocess, sys
# Needle built at runtime so this file never contains the literal.
needle = "cl" + "aude"
cmd = [
    "grep", "-r", "-i", needle, ".",
    "--include=*.md", "--include=*.json", "--include=*.sh",
    "--include=*.py", "--include=*.yaml", "--include=*.yml",
    "--exclude-dir=node_modules", "--exclude-dir=.git",
    "--exclude-dir=.pytest_cache",
    "--exclude-dir=references",      # third-party SDK/API reference docs
    "--exclude-dir=NuevoPlan",       # untracked migration-pack source
]
p = subprocess.run(cmd, capture_output=True, text=True)
hits = [l for l in p.stdout.splitlines() if l.strip()]
if hits:
    print("FAIL: legacy harness references found (outside references/):")
    for h in hits:
        print(f"  {h}")
    sys.exit(1)
print("Hygiene OK: no legacy harness references in scope")
PY

echo "[1] Frontmatter whitelist + name==dir"
python3 - <<'PY'
import pathlib, sys, yaml
allowed={"name","description","license","compatibility","metadata","allowed-tools"}
ok=True
for f in sorted(pathlib.Path("skills").glob("*/SKILL.md")):
    txt=f.read_text(encoding="utf-8")
    if not txt.startswith("---"):
        print(f"FAIL {f}: missing frontmatter"); ok=False; continue
    try:
        fm=yaml.safe_load(txt.split("---")[1])
    except Exception as e:
        print(f"FAIL {f}: yaml {e}"); ok=False; continue
    if not isinstance(fm, dict):
        print(f"FAIL {f}: frontmatter is not a mapping"); ok=False; continue
    extra=set(fm)-allowed
    if extra:
        print(f"FAIL {f}: extra keys {extra} — only {allowed} allowed"); ok=False
    if fm.get("name")!=f.parent.name:
        print(f"FAIL {f}: name {fm.get('name')} != dir {f.parent.name}"); ok=False
    desc=fm.get("description","")
    if not isinstance(desc,str) or not (1 <= len(desc) <= 1024):
        print(f"FAIL {f}: description length not in 1-1024"); ok=False
    # no legacy-harness references in the skill file itself
    if ("cl" + "aude") in txt.lower():
        print(f"FAIL {f}: contains a legacy harness reference — must be removed"); ok=False
    # metadata must be map string->string
    meta=fm.get("metadata",{})
    if not isinstance(meta, dict):
        print(f"FAIL {f}: metadata is not a mapping"); ok=False
    else:
        for k,v in meta.items():
            if not isinstance(v,str):
                print(f"FAIL {f}: metadata.{k} not string: {type(v)}"); ok=False
    # compatibility must include opencode
    comp=fm.get("compatibility","")
    if "opencode" not in str(comp).lower():
        print(f"WARN {f}: compatibility should include opencode: {comp}")
print("Frontmatter checks done" if ok else "Frontmatter checks FAILED")
sys.exit(0 if ok else 1)
PY

echo "[2] References exist"
refs_ok=1
for f in skills/*/SKILL.md; do
  # extract references/ paths (process substitution: no subshell swallowing exit)
  while IFS= read -r ref; do
    dir=$(dirname "$f")
    if [ ! -f "$dir/$ref" ]; then
      echo "FAIL $f: missing $dir/$ref"
      refs_ok=0
    fi
  done < <(grep -o "references/[A-Za-z0-9_./-]*\.md" "$f" 2>/dev/null || true)
done
[ "$refs_ok" = 1 ] || exit 1
echo "References OK"

echo "[3] Arrow cross-refs resolve (domain-scoped)"
python3 - <<'PY'
import pathlib, re, sys
# Domain-scoped: only <domain>-<slug> tokens count as skill refs.
# Bare prose after an arrow (e.g. "-> test", "-> smoke") is not a skill ref.
ARROW_RE = re.compile(r"→\s*`?((?:build|design|operate|planning|verify)-[a-z0-9-]+)`?")
skills=set(p.name for p in pathlib.Path("skills").iterdir() if p.is_dir())
ok=True
for f in sorted(pathlib.Path("skills").glob("*/SKILL.md")):
    txt=f.read_text(encoding="utf-8")
    for m in ARROW_RE.findall(txt):
        if m not in skills:
            print(f"FAIL {f}: arrow -> {m} not in catalog")
            ok=False
print("Arrows OK" if ok else "Arrow checks FAILED")
sys.exit(0 if ok else 1)
PY

echo "[4] skill-index.json parity (25 skills)"
python3 tools/skill-router/build_index.py
python3 - <<'PY'
import json, sys
d = json.load(open("skill-index.json"))
n = len(d.get("skills", []))
print(f"Index holds {n} skills")
sys.exit(0 if n == 25 else 1)
PY
echo "Index rebuilt (25 skills)"
fi

if [ "$FULL" = 1 ] || [ "$ONLY_SMOKE" = 1 ]; then
echo "[5] Router smoke test"
python3 tools/skill-router/route.py "por donde empiezo con este repo" --top 2
python3 tools/skill-router/route.py "limpia mi sistema" --top 2
fi

if [ "$FULL" = 1 ] || [ "$ONLY_PYTEST" = 1 ]; then
echo "[6] Python test-suite (existing v2 validators stay green)"
python3 -m pytest tools/ -q
fi

echo "=== All checks passed ==="
