#!/bin/bash
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/.." && pwd)
echo "OpenCode setup — vendor-neutral (project-local)"
for dest in .opencode/skills .agents/skills; do
  mkdir -p "$dest"
  # purge stale links in dest
  find "$dest" -maxdepth 1 -type l -delete 2>/dev/null || true
  for s in "$ROOT"/skills/*; do
    [ -d "$s" ] || continue
    [ -f "$s/SKILL.md" ] || continue
    name=$(basename "$s")
    ln -sfn "../../skills/$name" "$dest/$name"
  done
done
echo "✓ .opencode/skills and .agents/skills populated ($(ls .agents/skills | wc -l))"
echo "Check opencode.json skillDirectories"
cat opencode.json
