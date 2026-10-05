#!/usr/bin/env bash
# gate-husky.sh — Modo gate de verify-hooks para operate-release G.
# Si falta .husky/pre-commit lo instala (husky+lint-staged+prettier) y luego
# ejecuta el gate: lint-staged, typecheck (si existe), test (si existe).
# Uso: bash gate-husky.sh <repo_path>
# Exit: 0 verde, 1 gate en rojo o error de entorno.

set -euo pipefail

REPO_PATH="${1:-.}"
[[ -d "$REPO_PATH" ]] || { echo "[gate-husky] ERROR: ruta invalida: $REPO_PATH" >&2; exit 1; }
cd "$REPO_PATH"

log() { echo "[gate-husky] $*"; }

# Detectar gestor de paquetes
if [[ -f "pnpm-lock.yaml" ]]; then PM="pnpm"; RUN="pnpm exec"
elif [[ -f "yarn.lock" ]]; then PM="yarn"; RUN="yarn"
elif [[ -f "bun.lockb" ]]; then PM="bun"; RUN="bunx"
else PM="npm"; RUN="npx"; fi
log "Gestor: $PM"

# Instalar hooks si faltan (pasos 1-7 de SKILL.md)
if [[ ! -f ".husky/pre-commit" ]]; then
  log "Sin .husky/pre-commit; instalando husky+lint-staged+prettier..."
  $PM add -D husky lint-staged prettier 2>/dev/null || $PM install -D husky lint-staged prettier 2>/dev/null || npm install -D husky lint-staged prettier
  if ! ($RUN husky init 2>/dev/null || npx husky init 2>/dev/null); then
    log "husky init fallo (p. ej. FS noexec); configuracion manual de .husky/..."
    mkdir -p .husky
  fi
  {
    echo "$RUN lint-staged"
    echo "$PM run typecheck"
    echo "$PM run test"
  } > .husky/pre-commit
  chmod +x .husky/pre-commit
  [[ -f ".lintstagedrc" ]] || echo '{ "*": "prettier --ignore-unknown --write" }' > .lintstagedrc
  if [[ ! -f ".prettierrc" && ! -f ".prettierrc.json" && ! -f "prettier.config.js" ]]; then
    echo '{ "useTabs": false, "tabWidth": 2, "printWidth": 80, "singleQuote": false, "trailingComma": "es5", "semi": true, "arrowParens": "always" }' > .prettierrc
  fi
  if ! grep -q '"prepare"' package.json 2>/dev/null; then
    if ! python3 -c "
import json
p = 'package.json'
d = json.load(open(p))
d.setdefault('scripts', {})['prepare'] = 'husky'
json.dump(d, open(p, 'w'), indent=2, ensure_ascii=False)
open(p, 'a').write('\n')
" 2>/dev/null; then
      log "AVISO: anade manualmente \"prepare\": \"husky\" a scripts de package.json."
    fi
  fi
  log "Hooks instalados."
fi

# Gate: ejecutar sobre el head actual
log "Ejecutando lint-staged..."
$RUN lint-staged || { echo "[gate-husky] FAIL: lint-staged en rojo." >&2; exit 1; }

if [[ -f "package.json" ]] && grep -q '"typecheck"' package.json; then
  log "Ejecutando typecheck..."
  $PM run typecheck || { echo "[gate-husky] FAIL: typecheck en rojo." >&2; exit 1; }
else
  log "typecheck no declarado; se omite (anotado)."
fi

if [[ -f "package.json" ]] && grep -q '"test"' package.json; then
  log "Ejecutando tests unitarios..."
  $PM run test || { echo "[gate-husky] FAIL: tests en rojo." >&2; exit 1; }
else
  log "test no declarado; se omite (anotado)."
fi

log "OK: gate Husky en verde."
exit 0
