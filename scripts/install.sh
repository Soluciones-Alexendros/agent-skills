#!/bin/bash
set -e
SRC=$(pwd)/skills
echo "Installing skills to OpenCode & other harnesses (multi-harness)..."
for dest in ~/.config/opencode/skills ~/.agents/skills ~/.codex/skills ~/.cursor/skills; do
  mkdir -p "$dest"
  for s in "$SRC"/*; do
    [ -d "$s" ] || continue
    ln -sf "$s" "$dest/$(basename "$s")"
  done
  echo "✓ linked to $dest"
done
echo "Done. Skills available for OpenCode."
