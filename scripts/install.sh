#!/bin/bash
# Install autoworkspace skills into an explicit target. Never touches HOME by default.
# Usage:
#   bash scripts/install.sh --target DIR [--dry-run] [--scope skills]
#   bash scripts/install.sh --uninstall --target DIR
#   bash scripts/install.sh --prune   # REJECTED: prune-by-catalog-absence removed
set -euo pipefail

ROOT=$(cd "$(dirname "$0")/.." && pwd)
SRC="$ROOT/skills"
TARGET=""
DRY_RUN=0
UNINSTALL=0
SCOPE="skills"
MANIFEST_NAME=".autoworkspace-install-manifest.json"

usage() {
  cat <<EOF
Usage: bash scripts/install.sh --target DIR [--dry-run] [--uninstall]
  --target DIR   Required. Destination skills directory (must resolve under a confined path).
  --dry-run      Print actions without changing the filesystem.
  --uninstall    Remove only resources listed in the manifest under --target.
Does not overwrite global AGENTS.md. Does not prune foreign skills.
EOF
}

while [ $# -gt 0 ]; do
  case "$1" in
    --target) TARGET="${2:-}"; shift 2 ;;
    --dry-run) DRY_RUN=1; shift ;;
    --uninstall) UNINSTALL=1; shift ;;
    --scope) SCOPE="${2:-}"; shift 2 ;;
    --prune)
      echo "ERROR: --prune removed; refusing to archive foreign skills by catalog absence" >&2
      exit 2
      ;;
    --help|-h) usage; exit 0 ;;
    *) echo "ERROR: unknown arg $1" >&2; usage; exit 2 ;;
  esac
done

if [ -z "$TARGET" ]; then
  echo "ERROR: --target is required (refusing implicit \$HOME installs)" >&2
  exit 2
fi

# Resolve and confine target (no path traversal via .. after resolve)
TARGET=$(mkdir -p "$TARGET" 2>/dev/null; cd "$TARGET" && pwd)
case "$TARGET" in
  /|/etc|/usr|/var|/bin|/sbin)
    echo "ERROR: target too privileged: $TARGET" >&2
    exit 3
    ;;
esac

MANIFEST="$TARGET/$MANIFEST_NAME"
run() {
  if [ "$DRY_RUN" = 1 ]; then
    echo "[dry-run] $*"
  else
    eval "$@"
  fi
}

validate_manifest_paths() {
  local mf="$1"
  [ -f "$mf" ] || return 0
  python3 - "$mf" "$TARGET" <<'PY'
import json, os, sys
from pathlib import Path
mf, target = Path(sys.argv[1]), Path(sys.argv[2]).resolve()
data = json.loads(mf.read_text(encoding="utf-8"))
for rel in data.get("resources", []):
    if ".." in Path(rel).parts or Path(rel).is_absolute():
        print(f"FAIL: traversal/absolute in manifest: {rel}", file=sys.stderr)
        sys.exit(1)
    # Do not follow symlinks when checking confinement (owned links point at SRC).
    joined = Path(os.path.normpath(str(target / rel)))
    try:
        joined.relative_to(target)
    except ValueError:
        print(f"FAIL: manifest path escapes target: {rel}", file=sys.stderr)
        sys.exit(1)
print("manifest paths OK")
PY
}

if [ "$UNINSTALL" = 1 ]; then
  validate_manifest_paths "$MANIFEST"
  if [ ! -f "$MANIFEST" ]; then
    echo "ERROR: no manifest at $MANIFEST; refusing blind uninstall" >&2
    exit 1
  fi
  python3 - "$MANIFEST" "$TARGET" "$DRY_RUN" <<'PY'
import json, os, sys
from pathlib import Path
mf, target, dry = Path(sys.argv[1]), Path(sys.argv[2]).resolve(), sys.argv[3] == "1"
data = json.loads(mf.read_text(encoding="utf-8"))
for rel in data.get("resources", []):
    if ".." in Path(rel).parts or Path(rel).is_absolute():
        print("escape", rel); sys.exit(1)
    p = Path(os.path.normpath(str(target / rel)))
    try:
        p.relative_to(target)
    except ValueError:
        print("escape", rel); sys.exit(1)
    if p.is_symlink() or p.exists():
        print(("dry-run " if dry else "") + f"remove {p}")
        if not dry:
            p.unlink()
if not dry:
    mf.unlink(missing_ok=True)
print("uninstall done")
PY
  exit 0
fi

echo "Installing from $SRC → $TARGET (scope=$SCOPE dry_run=$DRY_RUN)"
RESOURCES=()
for s in "$SRC"/*; do
  [ -d "$s" ] || continue
  [ -f "$s/SKILL.md" ] || continue
  name=$(basename "$s")
  dest="$TARGET/$name"
  if [ -e "$dest" ] && [ ! -L "$dest" ]; then
    echo "ERROR: conflict — real file/dir at $dest (foreign resource preserved)" >&2
    exit 1
  fi
  if [ -L "$dest" ]; then
    cur=$(readlink -f "$dest" 2>/dev/null || true)
    if [ -n "$cur" ] && [ "$cur" != "$(readlink -f "$s")" ]; then
      case "$cur" in
        "$SRC"/*) ;;
        *)
          echo "ERROR: conflict — symlink $dest → $cur not owned by this install" >&2
          exit 1
          ;;
      esac
    fi
  fi
  if [ "$DRY_RUN" = 1 ]; then
    echo "[dry-run] ln -sfn $s $dest"
  else
    ln -sfn "$s" "$dest"
  fi
  RESOURCES+=("$name")
done

if [ "$DRY_RUN" = 0 ]; then
  python3 - "$MANIFEST" "$ROOT" "${RESOURCES[@]}" <<'PY'
import json, sys
from pathlib import Path
mf = Path(sys.argv[1])
root = sys.argv[2]
resources = list(sys.argv[3:])
doc = {
    "schema_version": 1,
    "source_root": root,
    "resources": resources,
    "installer": "scripts/install.sh",
}
mf.write_text(json.dumps(doc, indent=2) + "\n", encoding="utf-8")
print(f"manifest → {mf}")
PY
  validate_manifest_paths "$MANIFEST"
fi

echo "Done. AGENTS.md was not copied to any global home."
echo "OpenCode project links: use scripts/install-opencode.sh --target <repo>"
