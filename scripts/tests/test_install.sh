#!/bin/bash
# I01–I03 style install tests with temp HOME/target
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/../.." && pwd)
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT
TARGET="$TMP/skills-dest"
mkdir -p "$TARGET"

# dry-run: no changes
bash "$ROOT/scripts/install.sh" --target "$TARGET" --dry-run
test ! -e "$TARGET/.autoworkspace-install-manifest.json"

# real install
bash "$ROOT/scripts/install.sh" --target "$TARGET"
test -L "$TARGET/local-maintenance"
test -f "$TARGET/.autoworkspace-install-manifest.json"

# foreign dir preserved
mkdir -p "$TARGET/foreign-skill"
echo keep > "$TARGET/foreign-skill/x"
# second install idempotent
bash "$ROOT/scripts/install.sh" --target "$TARGET"
test "$(cat "$TARGET/foreign-skill/x")" = "keep"

# prune rejected
if bash "$ROOT/scripts/install.sh" --target "$TARGET" --prune 2>/dev/null; then
  echo "FAIL: prune should exit non-zero"; exit 1
fi

# uninstall only manifest resources
bash "$ROOT/scripts/install.sh" --target "$TARGET" --uninstall
test ! -e "$TARGET/local-maintenance"
test -d "$TARGET/foreign-skill"

# opencode install with explicit target
bash "$ROOT/scripts/install-opencode.sh" --target "$ROOT" --dry-run

echo "install tests OK"
