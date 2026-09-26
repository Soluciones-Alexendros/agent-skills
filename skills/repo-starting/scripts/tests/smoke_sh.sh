#!/usr/bin/env bash
# Smoke para check-product-structure.sh: bash -n + --help (+ casos exit 2/1).
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SH="$SCRIPT_DIR/check-product-structure.sh"

fail=0
ok() { echo "OK: $1"; }
bad() { echo "FALLO: $1" >&2; fail=1; }

if bash -n "$SH"; then ok "bash -n"; else bad "bash -n"; fi

if bash "$SH" --help >/tmp/smoke_cps_help.txt 2>&1; then
  grep -q "Uso:" /tmp/smoke_cps_help.txt && ok "--help exit 0" || bad "--help sin Uso:"
else
  bad "--help exit $?"
fi

if bash "$SH" --opcion-inexistente >/dev/null 2>&1; then
  bad "args inválidos deberían dar exit 2"
else
  rc=$?
  if [[ $rc -eq 2 ]]; then ok "args inválidos exit 2"; else bad "args inválidos exit $rc (esperado 2)"; fi
fi

TMP="$(mktemp -d)"
if bash "$SH" "$TMP" >/dev/null 2>&1; then
  bad "repo vacío debería dar exit 1"
else
  rc=$?
  if [[ $rc -eq 1 ]]; then ok "repo vacío exit 1"; else bad "repo vacío exit $rc (esperado 1)"; fi
fi
rm -rf "$TMP"

if [[ $fail -eq 0 ]]; then echo "smoke check-product-structure: VERDE"; else echo "smoke check-product-structure: ROJO" >&2; fi
exit "$fail"
