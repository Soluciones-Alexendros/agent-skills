#!/bin/bash
# Canonical validation gate — wraps tools/validate/* (no duplicated rules).
#
# Usage: bash run-validation.sh [--pytest-only] [--smoke-only] [--check-index]
#   default: full gate. --pytest-only: tests only. --smoke-only: router smoke.
#   --check-index: compare skill-index.json without rewriting it.
set -euo pipefail

ONLY_PYTEST=0
ONLY_SMOKE=0
CHECK_INDEX=0
for arg in "$@"; do
  case "$arg" in
    --pytest-only) ONLY_PYTEST=1 ;;
    --smoke-only) ONLY_SMOKE=1 ;;
    --check-index) CHECK_INDEX=1 ;;
    --help|-h)
      echo "Usage: bash run-validation.sh [--pytest-only] [--smoke-only] [--check-index]"
      exit 0
      ;;
    *)
      echo "ERROR: invalid flag: $arg" >&2
      exit 2
      ;;
  esac
done
FULL=1
if [ "$ONLY_PYTEST" = 1 ] || [ "$ONLY_SMOKE" = 1 ]; then FULL=0; fi

ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
cd "$ROOT"

echo "=== Autoworkspace validation (canonical) ==="

if [ "$FULL" = 1 ]; then
  echo "[1] skill_spec.py (catalog + frontmatter + domain)"
  python3 tools/validate/skill_spec.py --root "$ROOT"

  echo "[2] skill_links.py"
  python3 tools/validate/skill_links.py --root "$ROOT"

  echo "[3] release_coherence.py"
  python3 tools/validate/release_coherence.py --root "$ROOT"

  echo "[4] hygiene.py"
  python3 tools/validate/hygiene.py --root "$ROOT"

  echo "[4b] execution contracts (if present)"
  if [ -f tools/contracts/validate_contracts.py ]; then
    python3 tools/contracts/validate_contracts.py --root "$ROOT"
  fi

  echo "[5] skill-index.json check (read-only)"
  python3 - <<'PY'
import json, sys
from pathlib import Path
root = Path(".")
skills = sorted(p.name for p in (root / "skills").iterdir() if p.is_dir() and (p / "SKILL.md").is_file())
index_path = root / "skill-index.json"
if not index_path.is_file():
    print("FAIL: skill-index.json missing (run: python3 tools/skill-router/build_index.py)")
    sys.exit(1)
data = json.loads(index_path.read_text(encoding="utf-8"))
indexed = [s["name"] for s in data.get("skills", [])]
set_skills, set_idx = set(skills), set(indexed)
dupes = [n for n in indexed if indexed.count(n) > 1]
if dupes:
    print(f"FAIL: duplicate index names: {sorted(set(dupes))}"); sys.exit(1)
missing = sorted(set_skills - set_idx)
extra = sorted(set_idx - set_skills)
if missing or extra:
    print(f"FAIL: index mismatch missing={missing} extra={extra}")
    print("Hint: python3 tools/skill-router/build_index.py  # explicit rebuild, not part of check")
    sys.exit(1)
print(f"Index OK: {len(skills)} skills (identity match, not count-only)")
PY
fi

if [ "$CHECK_INDEX" = 1 ] && [ "$FULL" = 0 ]; then
  python3 tools/skill-router/build_index.py --check 2>/dev/null || {
    # fallback check without build_index --check support
    python3 - <<'PY'
import json, sys
from pathlib import Path
skills = sorted(p.name for p in Path("skills").iterdir() if p.is_dir() and (p / "SKILL.md").is_file())
data = json.loads(Path("skill-index.json").read_text(encoding="utf-8"))
indexed = [s["name"] for s in data.get("skills", [])]
sys.exit(0 if set(skills) == set(indexed) else 1)
PY
  }
fi

if [ "$FULL" = 1 ] || [ "$ONLY_SMOKE" = 1 ]; then
  echo "[6] Router smoke (selection only — not behavior proof)"
  python3 tools/skill-router/route.py "por donde empiezo con este repo" --top 2
  python3 tools/skill-router/route.py "limpia mi sistema" --top 2
  python3 tools/skill-router/route.py "refactoriza este código aplicando clean code" --top 2
fi

if [ "$FULL" = 1 ] || [ "$ONLY_PYTEST" = 1 ]; then
  echo "[7] Pytest tools/ + safe skills surfaces"
  # Manifest of safe test roots (effects inventoried; host mutators use doubles).
  python3 -m pytest tools/ \
    skills/local-maintenance/scripts/tests/ \
    skills/web-compliance/tests/ \
    skills/local-security/scripts/tests/ \
    skills/local-proton/scripts/ \
    -q --ignore=skills/local-proton/scripts/test_proton_bridge.py
fi

if [ "$FULL" = 1 ]; then
  echo "[8] Bash syntax (scripts/ + root wrappers)"
  while IFS= read -r -d '' f; do
    bash -n "$f"
  done < <(find scripts skills tools -name '*.sh' -print0 2>/dev/null; printf '%s\0' run-validation.sh)
fi

echo "=== All checks passed ==="
