#!/usr/bin/env bash
# postura_seguridad.sh — fingerprint read-only de defensas activas (R0)
# Salida por defecto: líneas "CLAVE: valor" pensadas para lectura por un agente.
# Con --json: objeto JSON {"CLAVE": "valor", ...}.
#
# El directorio del canon CLI observado se configura con CANON_TERMINAL_DIR
# (y la clave auditd con CANON_AUDIT_KEY, defecto "terminal_canon").
# Sin CANON_TERMINAL_DIR se informa "no-configurado" (sin hardcodeos de rutas).
set -euo pipefail

trap 'rc=$?; echo "postura_seguridad.sh: error en línea $LINENO (exit $rc)" >&2' ERR

SCRIPT_NAME="$(basename "$0")"
JSON_MODE=0

usage() {
  cat <<EOF
Uso: $SCRIPT_NAME [-h|--help] [--json]

Fingerprint read-only de defensas activas (solo lectura, no modifica el sistema).
Salida por defecto: líneas "CLAVE: valor" para lectura por un agente.
Con --json: objeto JSON con las mismas claves.

Variables de entorno:
  CANON_TERMINAL_DIR  Directorio del canon CLI a observar (sin defecto).
  CANON_AUDIT_KEY     Clave auditd del canon (defecto: terminal_canon).

Opciones:
  -h, --help   Muestra esta ayuda y sale con 0.
  --json       Emite JSON en lugar de líneas "CLAVE: valor".

Códigos de salida:
  0  OK (fingerprint emitido)
  1  Error controlado de lectura
  2  Error de uso (argumentos inválidos)
EOF
}

while [[ $# -gt 0 ]]; do
  case "${1:-}" in
    -h|--help)
      usage
      exit 0
      ;;
    --json)
      JSON_MODE=1
      shift
      ;;
    *)
      echo "$SCRIPT_NAME: argumento inválido: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

for dep in echo cat; do
  if ! command -v "$dep" >/dev/null 2>&1; then
    echo "$SCRIPT_NAME: falta dependencia requerida: $dep" >&2
    exit 1
  fi
done

OUT_LINES="$(mktemp)"
trap 'rc=$?; rm -f "$OUT_LINES"; [ $rc -ne 0 ] && echo "postura_seguridad.sh: error (exit $rc)" >&2' EXIT

say() { echo "$1: $2" >>"$OUT_LINES"; }

# is-active imprime el estado por stdout AUNQUE falle (exit != 0),
# lo que generaría líneas sueltas sin "CLAVE: ". Capturar estado o fallback.
svc() { # [--user] unit fallback
  local args=()
  if [[ "${1:-}" == "--user" ]]; then args+=(--user); shift; fi
  local st
  if st=$(systemctl "${args[@]}" is-active "$1" 2>/dev/null); then printf '%s' "$st"; else printf '%s' "$2"; fi
}

say "apparmor_kernel" "$(cat /sys/module/apparmor/parameters/enabled 2>/dev/null || echo '?')"
say "apparmor_userns_restrict" "$(sysctl -n kernel.apparmor_restrict_unprivileged_userns 2>/dev/null || echo '?')"
if command -v systemctl >/dev/null 2>&1; then
  say "apparmor_service" "$(svc apparmor '?')"
else
  say "apparmor_service" "?"
fi
if command -v aa-status >/dev/null 2>&1; then
  AA_OUT="$(aa-status 2>/dev/null | grep -E 'profiles are (loaded|in)' || true)"
  if [[ -n "$AA_OUT" ]]; then
    while IFS= read -r l; do
      l="$(echo "$l" | sed 's/^ *//')"
      [[ -n "$l" ]] && say "aa_status" "$l"
    done <<<"$AA_OUT"
  else
    say "aa_status" "sin perfiles (aa-status vacio)"
  fi
else
  say "aa_status" "aa-status no disponible (sin sudo o sin apparmor-utils)"
fi
if command -v systemctl >/dev/null 2>&1; then
  say "auditd" "$(svc auditd '?')"
else
  say "auditd" "?"
fi
if command -v sudo >/dev/null 2>&1 && command -v auditctl >/dev/null 2>&1; then
  say "audit_reglas" "$(sudo -n auditctl -l 2>/dev/null | wc -l) (0 si falla sudo -n)"
else
  say "audit_reglas" "0 (0 si falla sudo -n)"
fi
if command -v sudo >/dev/null 2>&1 && command -v auditctl >/dev/null 2>&1; then
  if command -v awk >/dev/null 2>&1; then
    say "audit_inmutable" "$(sudo -n auditctl -s 2>/dev/null | awk '/^enabled/{print $2}')"
  else
    say "audit_inmutable" ""
  fi
else
  say "audit_inmutable" ""
fi
say "journald_persistente" "$([ -d /var/log/journal ] && echo si || echo no)"
if command -v systemctl >/dev/null 2>&1; then
  if command -v grep >/dev/null 2>&1; then
    say "aide_timer" "$(systemctl list-timers --all --no-pager 2>/dev/null | grep -c aide || true)"
  else
    say "aide_timer" "?"
  fi
else
  say "aide_timer" "?"
fi
if command -v systemctl >/dev/null 2>&1; then
  say "clamav_daemon" "$(svc clamav-daemon no-instalado)"
  say "freshclam" "$(svc clamav-freshclam no-instalado)"
else
  say "clamav_daemon" "no-instalado"
  say "freshclam" "no-instalado"
fi
if command -v sudo >/dev/null 2>&1 && command -v ufw >/dev/null 2>&1; then
  if command -v head >/dev/null 2>&1; then
    say "ufw" "$(sudo -n ufw status 2>/dev/null | head -1 || echo 'sin sudo')"
  else
    say "ufw" "$(sudo -n ufw status 2>/dev/null || echo 'sin sudo')"
  fi
else
  say "ufw" "sin sudo"
fi
if command -v systemctl >/dev/null 2>&1; then
  say "sshd" "$(svc ssh inactivo)"
else
  say "sshd" "inactivo"
fi
if command -v systemctl >/dev/null 2>&1; then
  say "apparmor_notify_user" "$(svc --user apparmor-notify no)"
else
  say "apparmor_notify_user" "no"
fi
say "denials_log" "$([ -f /var/log/apparmor/denials.log ] && echo presente || echo ausente)"
if command -v systemctl >/dev/null 2>&1; then
  if command -v wc >/dev/null 2>&1; then
    say "failed_units" "$(systemctl --failed --no-legend 2>/dev/null | wc -l)"
  else
    say "failed_units" "?"
  fi
else
  say "failed_units" "?"
fi

# --- Endurecimiento de kernel / arranque (solo lectura) ---
say "lockdown" "$(cat /sys/kernel/security/lockdown 2>/dev/null | tr -d '[]' || echo '?')"
if [[ -f /sys/kernel/security/ima/ascii_runtime_measurements ]]; then
  if command -v wc >/dev/null 2>&1; then
    say "ima" "$(wc -l < /sys/kernel/security/ima/ascii_runtime_measurements 2>/dev/null || echo '?') mediciones en runtime"
  else
    say "ima" "activo (ascii_runtime_measurements presente)"
  fi
elif [[ -f /sys/kernel/security/ima/policy ]]; then
  say "ima" "politica presente, sin mediciones accesibles"
else
  say "ima" "no disponible"
fi
KREL="$(uname -r 2>/dev/null || echo unknown)"
if [[ -r "/boot/config-${KREL}" ]]; then
  if grep -q "^CONFIG_SECURITY_LANDLOCK=y" "/boot/config-${KREL}" 2>/dev/null; then
    say "landlock" "compilado en kernel (CONFIG_SECURITY_LANDLOCK=y)"
  else
    say "landlock" "no compilado (CONFIG_SECURITY_LANDLOCK ausente)"
  fi
else
  say "landlock" "? (sin /boot/config-${KREL} legible)"
fi
if [[ -e /dev/tpm0 || -e /dev/tpmrm0 ]]; then
  if command -v tpm2_pcrread >/dev/null 2>&1; then
    say "tpm2" "$(tpm2_pcrread 1 >/dev/null 2>&1 && echo presente-operativo || echo presente-sin-acceso)"
  else
    say "tpm2" "presente (tpm2-tools no instalado)"
  fi
else
  say "tpm2" "ausente"
fi
if command -v syft >/dev/null 2>&1; then
  say "syft" "$(syft version 2>/dev/null | head -1 || echo instalado)"
else
  say "syft" "no instalado (SBOM no disponible)"
fi

# --- Canon CLI observado (configurable, sin hardcodeos) ---
CANON_DIR="${CANON_TERMINAL_DIR:-}"
CANON_KEY="${CANON_AUDIT_KEY:-terminal_canon}"
if [[ -z "$CANON_DIR" ]]; then
  say "canon_terminal" "no-configurado (define CANON_TERMINAL_DIR)"
else
  if command -v awk >/dev/null 2>&1; then
    say "canon_terminal" "$([ -d "$CANON_DIR" ] && ls -ld "$CANON_DIR" | awk '{print $1, $3":"$4}' || echo ausente)"
  else
    say "canon_terminal" "$([ -d "$CANON_DIR" ] && echo presente || echo ausente)"
  fi
fi
if command -v sudo >/dev/null 2>&1 && command -v auditctl >/dev/null 2>&1; then
  if command -v grep >/dev/null 2>&1; then
    say "terminal_canon_audit" "$(sudo -n auditctl -l 2>/dev/null | grep -c "$CANON_KEY" || true) (regla cargada en kernel)"
  else
    say "terminal_canon_audit" "? (regla cargada en kernel)"
  fi
else
  say "terminal_canon_audit" "0 (regla cargada en kernel)"
fi

if [[ "$JSON_MODE" -eq 1 ]]; then
  if command -v python3 >/dev/null 2>&1; then
    python3 -c 'import json,sys; print(json.dumps({k.strip(): v.strip() for l in sys.stdin if ": " in l for k, v in [l.split(": ", 1)]}, indent=2, ensure_ascii=False))' <"$OUT_LINES"
  else
    cat "$OUT_LINES"
  fi
else
  cat "$OUT_LINES"
fi
