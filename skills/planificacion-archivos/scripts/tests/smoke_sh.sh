#!/usr/bin/env bash
# Smoke: bash -n (syntax) + --help (exit 0) for every .sh. Also --help for .py.
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname -- "$0")" && pwd)" || exit 1
ROOT="$(dirname -- "${SCRIPT_DIR}")"
pass=0; fail=0
check() { # $1=label $2...=cmd
    label="$1"; shift
    if "$@" >/dev/null 2>&1; then
        printf 'PASS %s\n' "${label}"; pass=$((pass+1))
    else
        printf 'FAIL %s (exit %s)\n' "${label}" "$?" >&2; fail=$((fail+1))
    fi
}
for sh in "${ROOT}"/attest-plan.sh "${ROOT}"/check-complete.sh "${ROOT}"/gate-stop.sh \
          "${ROOT}"/init-session.sh "${ROOT}"/inject-plan.sh "${ROOT}"/ledger-append.sh \
          "${ROOT}"/ledger-summary.sh "${ROOT}"/phase-status.sh "${ROOT}"/plan-doctor.sh \
          "${ROOT}"/resolve-plan-dir.sh "${ROOT}"/set-active-plan.sh; do
    base="$(basename -- "${sh}")"
    check "syntax:${base}" bash -n -- "${sh}"
    check "help:${base}" bash -- "${sh}" --help
done
check "help:session-catchup.py" python3 -- "${ROOT}/session-catchup.py" --help
printf 'smoke: %s pass, %s fail\n' "${pass}" "${fail}"
[ "${fail}" -eq 0 ]
