#!/bin/bash
set -e
echo "OpenCode setup — vendor-neutral"
mkdir -p .opencode/skills .agents/skills
for s in skills/*; do
  [ -d "$s" ] || continue
  ln -sf "../../$s" ".opencode/skills/$(basename "$s")"
  ln -sf "../../$s" ".agents/skills/$(basename "$s")"
done
echo "✓ .opencode/skills and .agents/skills populated"
echo "Check opencode.json skillDirectories"
cat opencode.json
