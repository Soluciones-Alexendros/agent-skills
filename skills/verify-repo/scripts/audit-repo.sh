#!/usr/bin/env bash
# Entrada única de Fase 0 (verify-repo): ejecuta el escáner y el chequeo de estructura.
# Uso: audit-repo.sh <ruta_repo> [--profile P0|P1|P2] [--out DIR]
# No modifica el repositorio auditado; escribe scan.json/scan.md fuera de él.

set -euo pipefail

trap 'rc=$?; echo "audit-repo.sh: error en línea $LINENO (exit $rc)" >&2' ERR

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCRIPT_NAME="$(basename "$0")"

usage() {
  cat <<EOF
Uso: $SCRIPT_NAME <ruta_repo> [--profile P0|P1|P2] [--out DIR]
     $SCRIPT_NAME -h|--help

Ejecuta scan_repo.py y check-product-structure.sh sobre el repo indicado.

Opciones:
  --profile P0|P1|P2   Perfil de validación (por defecto: P1).
  --out DIR            Directorio de salida para scan.json/scan.md (por defecto: temporal).
  -h, --help           Muestra esta ayuda y sale con 0.
EOF
}

repo=""
profile="P1"
out=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    -h|--help)
      usage
      exit 0
      ;;
    --profile)
      [[ $# -lt 2 ]] && { echo "$SCRIPT_NAME: --profile requiere un valor" >&2; exit 2; }
      profile="$2"
      shift 2
      ;;
    --profile=*)
      profile="${1#--profile=}"
      shift
      ;;
    --out)
      [[ $# -lt 2 ]] && { echo "$SCRIPT_NAME: --out requiere un directorio" >&2; exit 2; }
      out="$2"
      shift 2
      ;;
    --out=*)
      out="${1#--out=}"
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
      [[ -n "$repo" ]] && { echo "$SCRIPT_NAME: demasiados argumentos posicionales: $1" >&2; exit 2; }
      repo="$1"
      shift
      ;;
  esac
done

[[ -z "$repo" ]] && { echo "$SCRIPT_NAME: falta <ruta_repo>" >&2; usage >&2; exit 2; }
[[ -d "$repo" ]] || { echo "$SCRIPT_NAME: no es un directorio: $repo" >&2; exit 2; }

case "$profile" in
  P0|P1|P2) ;;
  *) echo "$SCRIPT_NAME: perfil inválido: $profile (esperado P0|P1|P2)" >&2; exit 2 ;;
esac

if [[ -z "$out" ]]; then
  out="$(mktemp -d)"
  echo "$SCRIPT_NAME: salida en $out"
else
  mkdir -p "$out"
fi

python3 "$SCRIPT_DIR/scan_repo.py" "$repo" --json "$out/scan.json" --md "$out/scan.md"
bash "$SCRIPT_DIR/check-product-structure.sh" "$repo" --profile "$profile"

echo "audit-repo.sh: OK (scan.json/scan.md en $out)"
