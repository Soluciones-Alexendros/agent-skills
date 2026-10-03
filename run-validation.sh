#!/usr/bin/env bash
# Validación agregada del repo agent-skills.
# Uso: bash run-validation.sh [--spec-only|--links-only|--version-only|--pytest-only|--smoke-only|--coherence-only|--hygiene-only]
# Exit: 0 todo verde, 1 algún fallo.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MODE="${1:-all}"
FAIL=0

step() {
    local label="$1"; shift
    echo "### $label"
    if "$@"; then echo "PASS: $label"; else echo "FAIL: $label"; FAIL=1; fi
}

if [[ "$MODE" == "all" || "$MODE" == "--spec-only" ]]; then
    step "spec" python3 "$ROOT/tools/validate/skill_spec.py" --root "$ROOT"
fi

if [[ "$MODE" == "all" || "$MODE" == "--links-only" ]]; then
    step "links" python3 "$ROOT/tools/validate/skill_links.py" --root "$ROOT"
fi

if [[ "$MODE" == "all" || "$MODE" == "--coherence-only" ]]; then
    step "release-coherence" python3 "$ROOT/tools/validate/release_coherence.py" --root "$ROOT"
fi

if [[ "$MODE" == "all" || "$MODE" == "--hygiene-only" ]]; then
    step "hygiene" python3 "$ROOT/tools/validate/hygiene.py" --root "$ROOT"
fi

if [[ "$MODE" == "all" || "$MODE" == "--version-only" ]]; then
    step "version-bump" python3 "$ROOT/tools/version/bump.py" --check --auto --base origin/main
fi

if [[ "$MODE" == "all" || "$MODE" == "--pytest-only" ]]; then
    declare -A SEEN=()
    while IFS= read -r t; do
        td="$(dirname "$t")"
        if [[ "$(basename "$td")" == "tests" && "$(basename "$(dirname "$td")")" == "scripts" ]]; then
            cwd="$(dirname "$td")"; arg="tests"
        else
            cwd="$(dirname "$td")"; arg="$(basename "$td")"
        fi
        key="$cwd"
        if [[ -z "${SEEN[$key]:-}" ]]; then
            SEEN[$key]=1
            step "pytest $cwd" bash -c "cd \"\$0\" && PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q -p no:cacheprovider \"\$1\"" "$ROOT/$cwd" "$arg"
        fi
    done < <(cd "$ROOT" && find skills tools -name "test_*.py" -not -path "*__pycache__*" | sort)
fi

if [[ "$MODE" == "all" || "$MODE" == "--smoke-only" ]]; then
    while IFS= read -r s; do
        step "smoke $s" bash "$ROOT/$s"
    done < <(cd "$ROOT" && find skills -path "*/scripts/tests/smoke_sh.sh" | sort)
    echo "### bash -n global (*.sh)"
    while IFS= read -r f; do
        bash -n "$ROOT/$f" || { echo "SYNTAX FAIL: $f"; FAIL=1; }
    done < <(cd "$ROOT" && find skills tools -name "*.sh" | sort)
    [[ $FAIL -eq 0 ]] && echo "bash -n global: OK" || echo "bash -n global: CON-FALLOS"
fi

if [[ $FAIL -eq 0 ]]; then echo "VALIDATION: ALL GREEN"; else echo "VALIDATION: FAILURES"; fi
exit $FAIL
