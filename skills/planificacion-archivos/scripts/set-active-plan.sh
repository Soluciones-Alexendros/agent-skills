#!/usr/bin/env bash
# planning-with-files: set or display the active plan pointer.
#
# Usage:
#   set-active-plan.sh <plan_id>   — pin .planning/.active_plan to plan_id
#   set-active-plan.sh             — print the current active plan (if any)
#
# The active plan is stored in .planning/.active_plan and is read by
# resolve-plan-dir.sh when no $PLAN_ID env var is set.
#
# Exit codes: 0 ok (including "no active plan"), 1 controlled error
# (unknown plan dir), 2 invalid CLI usage.

set -euo pipefail
trap 'rc=$?; printf "%s: error at line %s (exit %s)\n" "${0##*/}" "${LINENO:-?}" "$rc" >&2' ERR

usage() {
    printf "Usage: %s [<plan_id>] [-h|--help]\n" "${0##*/}" >&2
}

need_cmd() {
    command -v "$1" >/dev/null 2>&1 || {
        printf "%s: missing required command: %s\n" "${0##*/}" "$1" >&2
        exit 1
    }
}
need_cmd tr
need_cmd mkdir

for _a in "$@"; do
    case "${_a}" in
        -h|--help) usage; exit 0 ;;
        --*) printf "%s: unknown option: %s\n" "${0##*/}" "${_a}" >&2; usage; exit 2 ;;
    esac
done
if [ "$#" -gt 1 ]; then
    printf "%s: too many arguments\n" "${0##*/}" >&2
    usage
    exit 2
fi

PLAN_ROOT="${PWD}/.planning"
ACTIVE_FILE="${PLAN_ROOT}/.active_plan"

# No args → show current active plan
if [ "${1:-}" = "" ]; then
    if [ -f "${ACTIVE_FILE}" ]; then
        plan_id="$(tr -d '\r\n' < "${ACTIVE_FILE}" 2>/dev/null || true)" || plan_id=""
        if [ -n "${plan_id}" ] && [ -d "${PLAN_ROOT}/${plan_id}" ]; then
            echo "Active plan: ${plan_id}"
            echo "Path: ${PLAN_ROOT}/${plan_id}"
        elif [ -n "${plan_id}" ]; then
            echo "Active plan pointer: ${plan_id} (directory not found — stale pointer)"
        else
            echo "No active plan set."
        fi
    else
        echo "No active plan set."
    fi
    exit 0
fi

PLAN_ID="$1"
case "${PLAN_ID}" in
    -*) printf "%s: unknown option: %s\n" "${0##*/}" "${PLAN_ID}" >&2; usage; exit 2 ;;
esac
# Guard: plan ids are safe identifiers (parity with resolve-plan-dir.sh).
# Prevents path traversal via `../` in the pointer write below.
case "${PLAN_ID}" in
    [A-Za-z0-9_]*|"" ) : ;;
    *) printf "%s: invalid plan id: %s\n" "${0##*/}" "${PLAN_ID}" >&2; exit 2 ;;
esac
case "${PLAN_ID}" in
    *[!A-Za-z0-9._-]*) printf "%s: invalid plan id: %s\n" "${0##*/}" "${PLAN_ID}" >&2; exit 2 ;;
esac
PLAN_DIR="${PLAN_ROOT}/${PLAN_ID}"

if [ ! -d "${PLAN_DIR}" ]; then
    echo "Error: plan directory not found: ${PLAN_DIR}" >&2
    echo "Run: init-session.sh \"${PLAN_ID}\" to create it, or check .planning/ for available plans." >&2
    exit 1
fi

mkdir -p -- "${PLAN_ROOT}"
[ -n "${ACTIVE_FILE:-}" ] || { printf "%s: refusing to write with empty path\n" "${0##*/}" >&2; exit 1; }
printf "%s\n" "${PLAN_ID}" > "${ACTIVE_FILE}"

echo "Active plan set to: ${PLAN_ID}"
echo "Path: ${PLAN_DIR}"
echo ""
echo "To pin this terminal session only:"
echo "  export PLAN_ID=${PLAN_ID}"
