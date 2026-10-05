#!/bin/bash
set -e
# Rename ES folders to EN canonical v3.0 — vendor-neutral
declare -A MAP=(
  ["operar-mantenimiento"]="operate-maintenance"
  ["operar-seguridad"]="operate-security"
  ["operar-salud-sistema"]="operate-health"
  ["operar-release"]="operate-release"
  ["operar-lifecycle"]="operate-lifecycle"
  ["construir-upstash"]="build-upstash"
  ["disenar-arquitectura"]="design-architecture"
  ["disenar-constitucion"]="design-constitution"
  ["verificar-dependencias"]="verify-dependencies"
  ["verificar-performance"]="verify-performance"
  ["verificar-compliance"]="verify-compliance"
  ["verificar-fullaudit"]="verify-full-audit"
  ["verificar-repo"]="verify-repo"
  ["verificar-hooks"]="verify-hooks"
  ["verificar-owasp"]="verify-owasp"
  ["verificar-testing"]="verify-testing"
  ["operar-monitoring"]="operate-monitoring"
)

for old in "${!MAP[@]}"; do
  new=${MAP[$old]}
  if [ -d "skills/$old" ]; then
    echo "Renaming skills/$old -> skills/$new"
    mv "skills/$old" "skills/$new"
  fi
done

echo "Done. Now run: python scripts/migrate-frontmatter.py"
