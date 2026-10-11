#!/usr/bin/env bash
# Valida el árbol P0/P1 de un *repo de producto* según Soluciones-Alexendros/repo-standard.
# Uso: check-product-structure.sh [ruta_repo] [--profile P0|P1|P2]
# No exige ADRs ni stacks/ del meta-canon.

set -euo pipefail

trap 'rc=$?; echo "check-product-structure.sh: error en línea $LINENO (exit $rc)" >&2' ERR

SCRIPT_NAME="$(basename "$0")"

usage() {
  cat <<EOF
Uso: $SCRIPT_NAME [ruta_repo] [--profile P0|P1|P2]
     $SCRIPT_NAME -h|--help

Valida la estructura de un repo de producto (perfiles P0, P1, P2).

Opciones:
  --profile P0|P1|P2   Perfil de validación (por defecto: P1).
  -h, --help           Muestra esta ayuda y sale con 0.

Códigos de salida:
  0  OK (estructura válida)
  1  FALLO controlado (faltantes o errores de contenido)
  2  Error de uso (ruta inválida, perfil desconocido, argumentos inválidos)
EOF
}

for dep in grep; do
  if ! command -v "$dep" >/dev/null 2>&1; then
    echo "$SCRIPT_NAME: falta dependencia requerida: $dep" >&2
    exit 1
  fi
done

root="."
profile="P1"
positional_set=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    -h|--help)
      usage
      exit 0
      ;;
    --profile)
      if [[ $# -lt 2 ]]; then
        echo "$SCRIPT_NAME: --profile requiere un valor (P0|P1|P2)" >&2
        usage >&2
        exit 2
      fi
      profile="$2"
      shift 2
      ;;
    --profile=*)
      profile="${1#--profile=}"
      shift
      ;;
    --*)
      echo "$SCRIPT_NAME: opción desconocida: $1" >&2
      usage >&2
      exit 2
      ;;
    -*)
      echo "$SCRIPT_NAME: opción desconocida: $1" >&2
      usage >&2
      exit 2
      ;;
    *)
      if [[ "$positional_set" -eq 1 ]]; then
        echo "$SCRIPT_NAME: demasiados argumentos posicionales: $1" >&2
        usage >&2
        exit 2
      fi
      root="$1"
      positional_set=1
      shift
      ;;
  esac
done

case "$profile" in
  P0|P1|P2) ;;
  *)
    echo "$SCRIPT_NAME: perfil inválido: $profile (esperado P0|P1|P2)" >&2
    usage >&2
    exit 2
    ;;
esac

if [[ ! -d "$root" ]]; then
  echo "No es un directorio: $root" >&2
  exit 2
fi
cd "$root" || { echo "$SCRIPT_NAME: no se puede acceder a: $root" >&2; exit 1; }

missing=0
errors=0
warns=0

require_file() {
  local path="$1"
  if [[ ! -f "$path" ]]; then
    echo "FALTA archivo: $path"
    missing=$((missing + 1))
  fi
}

require_dir() {
  local path="$1"
  if [[ ! -d "$path" ]]; then
    echo "FALTA directorio: $path"
    missing=$((missing + 1))
  fi
}

warn_missing() {
  local path="$1"
  if [[ ! -f "$path" ]]; then
    echo "AVISO (recomendado): falta $path"
    warns=$((warns + 1))
  fi
}

echo "check-product-structure: perfil=$profile root=$root"

# --- P0 ---
require_file "README.md"
require_file "LICENSE"
require_file "CHANGELOG.md"
require_file "SECURITY.md"
require_file "CONTRIBUTING.md"
require_file ".github/workflows/ci.yml"
require_file ".github/CODEOWNERS"

ci=".github/workflows/ci.yml"
if [[ -f "$ci" ]]; then
  for job in quality test; do
    if ! grep -Eq "^[[:space:]]*${job}:" "$ci"; then
      echo "FALTA job '${job}' en $ci"
      errors=$((errors + 1))
    fi
  done
fi

# Renovate único
if [[ -f ".github/dependabot.yml" ]] || [[ -f "dependabot.yml" ]]; then
  echo "PROHIBIDO: dependabot.yml de version-updates. El bot de la flota es Renovate."
  errors=$((errors + 1))
fi

if [[ "$profile" == "P0" ]]; then
  if [[ $missing -gt 0 || $errors -gt 0 ]]; then
    echo "check-product-structure: FALLO P0 (faltantes=${missing} errores=${errors})"
    exit 1
  fi
  echo "check-product-structure: OK P0 (avisos=${warns})"
  exit 0
fi

# --- P1 ---
require_file "AGENTS.md"
require_file "ARCHITECTURE.md"
require_file "Makefile"
require_file ".env.example"
require_dir "docs"
require_dir "docs/architecture"
require_dir "docs/guides"
require_dir "docs/runbooks"
require_file "docs/README.md"
require_file ".github/renovate.json"
require_file ".github/PULL_REQUEST_TEMPLATE.md"
warn_missing ".github/ISSUE_TEMPLATE/bug.yml"
warn_missing ".github/ISSUE_TEMPLATE/feature.yml"

if [[ -f "$ci" ]] && ! grep -Eq "^[[:space:]]*smoke:" "$ci"; then
  echo "FALTA job 'smoke' en $ci (P1)"
  errors=$((errors + 1))
fi

if [[ ! -s ".github/renovate.json" ]] && [[ -f ".github/renovate.json" ]]; then
  echo "FALTA o vacío: .github/renovate.json"
  errors=$((errors + 1))
fi

purpose_heading="### Propósito de este documento"
purpose_files=(README.md AGENTS.md ARCHITECTURE.md SECURITY.md CONTRIBUTING.md docs/README.md)
for path in "${purpose_files[@]}"; do
  if [[ -f "$path" ]] && ! grep -Fq "$purpose_heading" "$path"; then
    echo "FALTA meta-sección '${purpose_heading}' en $path"
    errors=$((errors + 1))
  fi
done

if [[ "$profile" == "P2" ]]; then
  require_file "CODE_OF_CONDUCT.md"
  warn_missing "SUPPORT.md"
  warn_missing ".github/workflows/security.yml"
fi

if [[ $missing -gt 0 || $errors -gt 0 ]]; then
  echo "check-product-structure: FALLO ${profile} (faltantes=${missing} errores=${errors} avisos=${warns})"
  exit 1
fi

echo "check-product-structure: OK ${profile} (avisos=${warns})"
exit 0
