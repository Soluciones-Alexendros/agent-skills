#!/usr/bin/env bash
# postura_seguridad.sh — fingerprint read-only de defensas activas (R0)
# Salida: líneas "CLAVE: valor" pensadas para lectura por un agente.
set -euo pipefail

trap 'rc=$?; echo "postura_seguridad.sh: error en línea $LINENO (exit $rc)" >&2' ERR

SCRIPT_NAME="$(basename "$0")"

usage() {
  cat <<EOF
Uso: $SCRIPT_NAME [-h|--help]

Fingerprint read-only de defensas activas (solo lectura, no modifica el sistema).
Salida: líneas "CLAVE: valor" para lectura por un agente.

Opciones:
  -h, --help   Muestra esta ayuda y sale con 0.

Códigos de salida:
  0  OK (fingerprint emitido)
  1  Error controlado de lectura
  2  Error de uso (argumentos inválidos)
EOF
}

if [[ $# -gt 0 ]]; then
  case "${1:-}" in
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "$SCRIPT_NAME: argumento inválido: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
fi

for dep in echo cat; do
  if ! command -v "$dep" >/dev/null 2>&1; then
    echo "$SCRIPT_NAME: falta dependencia requerida: $dep" >&2
    exit 1
  fi
done

say() { echo "$1: $2"; }

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
  aa-status 2>/dev/null | grep -E 'profiles are (loaded|in)' | sed 's/^ *//' | while read -r l; do say "aa_status" "$l"; done || true
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
# Canon ALIGNUX: la raíz del canon CLI vive en ~/Aplicaciones/Terminal (estrato ··Terminal)
if command -v awk >/dev/null 2>&1; then
  say "canon_terminal" "$([ -d "$HOME/Aplicaciones/Terminal" ] && ls -ld "$HOME/Aplicaciones/Terminal" | awk '{print $1, $3":"$4}' || echo ausente)"
else
  say "canon_terminal" "$([ -d "$HOME/Aplicaciones/Terminal" ] && echo presente || echo ausente)"
fi
if command -v sudo >/dev/null 2>&1 && command -v auditctl >/dev/null 2>&1; then
  if command -v grep >/dev/null 2>&1; then
    say "terminal_canon_audit" "$(sudo -n auditctl -l 2>/dev/null | grep -c terminal_canon || true) (regla cargada en kernel)"
  else
    say "terminal_canon_audit" "? (regla cargada en kernel)"
  fi
else
  say "terminal_canon_audit" "0 (regla cargada en kernel)"
fi
