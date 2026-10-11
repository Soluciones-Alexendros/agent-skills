#!/bin/bash
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/.." && pwd)
SRC="$ROOT/skills"
PRUNE=0
for arg in "$@"; do
  case "$arg" in
    --prune) PRUNE=1 ;;
  esac
done

CANON=$(find "$SRC" -mindepth 1 -maxdepth 1 -type d -printf '%f\n' | sort | tr '\n' ' ')

echo "Installing autoworkspace (canon v4) to global harnesses..."

install_to() {
  local dest="$1"
  mkdir -p "$dest"
  for link in "$dest"/*; do
    [ -e "$link" ] || [ -L "$link" ] || continue
    name=$(basename "$link")
    if [ -L "$link" ]; then
      target=$(readlink -f "$link" 2>/dev/null || true)
      case "$target" in
        "$SRC"/*|"") rm -f "$link" ;;
      esac
      [ -e "$link" ] || rm -f "$link"
    elif [ "$PRUNE" = 1 ] && [ -d "$link" ]; then
      case " $CANON " in
        *" $name "*) ;;
        *)
          archive="$HOME/.cursor/skills-archive-prune-$(date +%Y%m%d)"
          # only prune cursor/agents/codex/opencode/grok skill dirs, not arbitrary
          mkdir -p "$archive"
          mv "$link" "$archive/$name"
          echo "  pruned $dest/$name → $archive/"
          ;;
      esac
    fi
  done
  for s in "$SRC"/*; do
    [ -d "$s" ] || continue
    [ -f "$s/SKILL.md" ] || continue
    name=$(basename "$s")
    ln -sfn "$s" "$dest/$name"
  done
  echo "✓ $dest ($(find "$dest" -maxdepth 1 \( -type l -o -type d \) ! -path "$dest" | wc -l) entries)"
}

for dest in \
  "$HOME/.config/opencode/skills" \
  "$HOME/.agents/skills" \
  "$HOME/.codex/skills" \
  "$HOME/.cursor/skills" \
  "$HOME/.grok/skills"
do
  install_to "$dest"
done

mkdir -p "$HOME/.grok" "$HOME/.cursor" "$HOME/.cursor/autoworkspace-docs" "$HOME/.grok/commands"
cp -f "$ROOT/AGENTS.md" "$HOME/.grok/AGENTS.md"
cp -f "$ROOT/AGENTS.md" "$HOME/.cursor/AGENTS.md"
cp -f "$ROOT/docs/TAXONOMY.md" "$ROOT/docs/routing.md" "$HOME/.cursor/autoworkspace-docs/" 2>/dev/null || true
cat > "$HOME/.grok/commands/skill-route.md" <<CMD
---
description: Route a natural-language intent to the best autoworkspace skill (canon v4)
---

Run the deterministic router and follow the top skill:

\`\`\`bash
python3 $ROOT/tools/skill-router/route.py "\$ARGUMENTS" --top 3
\`\`\`

Then open \`~/.grok/skills/<name>/SKILL.md\` and follow it exactly.
CMD

echo "Done. Cursor: ~/.cursor/skills + ~/.cursor/AGENTS.md"
echo "Grok: ~/.grok/skills + ~/.grok/AGENTS.md + /skill-route"
