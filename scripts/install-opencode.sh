#!/bin/bash
# Populate project-local OpenCode/agent skill links. Always operates on --target repo root.
set -euo pipefail
SCRIPT_ROOT=$(cd "$(dirname "$0")/.." && pwd)
TARGET=""
DRY_RUN=0

while [ $# -gt 0 ]; do
  case "$1" in
    --target) TARGET="${2:-}"; shift 2 ;;
    --dry-run) DRY_RUN=1; shift ;;
    --help|-h)
      echo "Usage: bash scripts/install-opencode.sh --target REPO_ROOT [--dry-run]"
      exit 0
      ;;
    *) echo "ERROR: unknown arg $1" >&2; exit 2 ;;
  esac
done

if [ -z "$TARGET" ]; then
  TARGET="$SCRIPT_ROOT"
fi
TARGET=$(cd "$TARGET" && pwd)
ROOT="$TARGET"
SRC="$ROOT/skills"

if [ ! -d "$SRC" ]; then
  echo "ERROR: $SRC missing — target is not an autoworkspace checkout" >&2
  exit 1
fi

echo "OpenCode setup — project-local (target=$TARGET dry_run=$DRY_RUN)"

for dest_rel in .opencode/skills .agents/skills; do
  dest="$TARGET/$dest_rel"
  if [ "$DRY_RUN" = 1 ]; then
    echo "[dry-run] mkdir -p $dest"
  else
    mkdir -p "$dest"
  fi
  # Only remove symlinks we own (pointing at $SRC/*)
  if [ -d "$dest" ]; then
    for link in "$dest"/*; do
      [ -L "$link" ] || continue
      tgt=$(readlink -f "$link" 2>/dev/null || true)
      case "$tgt" in
        "$SRC"/*)
          if [ "$DRY_RUN" = 1 ]; then
            echo "[dry-run] rm owned link $link"
          else
            rm -f "$link"
          fi
          ;;
        *)
          echo "keep foreign/broken link: $link → ${tgt:-broken}"
          ;;
      esac
    done
  fi
  for s in "$SRC"/*; do
    [ -d "$s" ] || continue
    [ -f "$s/SKILL.md" ] || continue
    name=$(basename "$s")
    # Relative link from .opencode/skills or .agents/skills → ../../skills/name
    if [ "$DRY_RUN" = 1 ]; then
      echo "[dry-run] ln -sfn ../../skills/$name $dest/$name"
    else
      ln -sfn "../../skills/$name" "$dest/$name"
    fi
  done
done

if [ -f "$TARGET/opencode.json" ]; then
  echo "Check $TARGET/opencode.json skillDirectories"
  if [ "$DRY_RUN" = 0 ]; then
    cat "$TARGET/opencode.json"
  fi
else
  echo "WARN: opencode.json missing in target"
fi
echo "✓ done"
