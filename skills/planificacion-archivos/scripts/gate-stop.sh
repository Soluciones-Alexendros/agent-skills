#!/usr/bin/env bash
# planning-with-files: Stop-hook dispatcher for the v3 completion gate.
#
# Thin wrapper: discover check-complete.sh (sibling first, then the known
# install paths) and run it with --gate, passing the Stop hook's stdin JSON
# through so check-complete can read stop_hook_active and apply the gate
# decision table. check-complete in --gate mode is the host-aware termination
# oracle (W1A); without --gate it keeps the legacy advisory echo behavior.
#
# Always exits with check-complete's exit code. In legacy mode (no .mode file)
# check-complete --gate never blocks, so the Stop event proceeds exactly as v2.

set -euo pipefail
trap 'rc=$?; printf "%s: error at line %s (exit %s)\n" "${0##*/}" "${LINENO:-?}" "$rc" >&2' ERR

usage() {
    printf "Usage: %s [-h|--help]\n" "${0##*/}" >&2
    printf "  Dispatches to check-complete.sh --gate (Stop hook).\n" >&2
}

for _arg in "$@"; do
    case "${_arg}" in
        -h|--help) usage; exit 0 ;;
        *) printf "%s: unknown option: %s\n" "${0##*/}" "${_arg}" >&2; usage; exit 2 ;;
    esac
done

# issue #195: per-invocation opt-out (PLANNING_DISABLED=1) for one-shot/CI
# sessions that share a cwd with a plan but never opted into it.
[ "${PLANNING_DISABLED:-}" = "1" ] && exit 0

need_cmd() {
    command -v "$1" >/dev/null 2>&1 || {
        printf "%s: missing required command: %s\n" "${0##*/}" "$1" >&2
        exit 1
    }
}
need_cmd head

SCRIPT_DIR="$(cd "$(dirname -- "$0")" && pwd 2>/dev/null)" || SCRIPT_DIR="."

TARGET="${SCRIPT_DIR}/check-complete.sh"
if [ ! -f "${TARGET}" ] && [ -n "${HOME:-}" ]; then
    # ${HOME:-} keeps set -u from aborting the substitution in CI/Docker images
    # where HOME is unset; without the guard the shell exits before the gate runs.
    TARGET=$(ls "${HOME}/.claude/skills/planning-with-files/scripts/check-complete.sh" \
                "${HOME}/.claude/plugins/marketplaces/planning-with-files/scripts/check-complete.sh" \
                2>/dev/null | head -1 || true)
fi

[ -n "${TARGET:-}" ] && [ -f "${TARGET}" ] || exit 0

bash -- "${TARGET}" --gate
