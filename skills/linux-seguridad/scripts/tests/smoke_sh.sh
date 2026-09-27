#!/usr/bin/env bash
# Smoke para postura_seguridad.sh: bash -n + --help (+ casos exit 2/0).
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SH="$SCRIPT_DIR/postura_seguridad.sh"

fail=0
ok() { echo "OK: $1"; }
bad() { echo "FALLO: $1" >&2; fail=1; }

if bash -n "$SH"; then ok "bash -n"; else bad "bash -n"; fi

if bash "$SH" --help >/tmp/smoke_postura_help.txt 2>&1; then
  grep -q "Uso:" /tmp/smoke_postura_help.txt && ok "--help exit 0" || bad "--help sin Uso:"
else
  bad "--help exit $?"
fi

if bash "$SH" --opcion-inexistente >/dev/null 2>&1; then
  bad "args inválidos deberían dar exit 2"
else
  rc=$?
  if [[ $rc -eq 2 ]]; then ok "args inválidos exit 2"; else bad "args inválidos exit $rc (esperado 2)"; fi
fi

if bash "$SH" >/tmp/smoke_postura_run.txt 2>&1; then
  grep -q ": " /tmp/smoke_postura_run.txt && ok "run exit 0 formato CLAVE: valor" || bad "run sin formato CLAVE: valor"
else
  bad "run exit $?"
fi

if [[ $fail -eq 0 ]]; then echo "smoke postura_seguridad: VERDE"; else echo "smoke postura_seguridad: ROJO" >&2; fi
exit "$fail"
