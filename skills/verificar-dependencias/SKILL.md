---
name: verificar-dependencias
description: >-
  Auditoría de dependencias (SCA/CVE): pipeline multi-lenguaje (npm/pip/cargo/go/maven/gradle/composer/gem)
  para detectar vulnerabilidades, malware, typosquatting, dependencias no usadas y outdated.
  Usar cuando el operador pida dependency audit, SCA, CVE scanning, supply chain security o
  generación de SBOM. No usar para revisión de código OWASP (→ verificar-owasp) ni
  hardening de host (→ operar-seguridad).
license: MIT
metadata:
  author: Soluciones-Alexendros
  version: "1.0.1"
  dominio: verificar
  tipo: atomic
  idioma: es
---

# verificar-dependencias — Auditoría de dependencias y supply chain (SCA/CVE)

## Propósito

Ejecutar un pipeline multi-lenguaje para auditar dependencias: CVE, malware, typosquatting, unused, outdated y SBOM. Cubre npm, pip, cargo, go, maven, gradle, composer y gem. Esta skill no empaqueta scripts propios: usa las CLIs del ecosistema detectado.

## Cuándo usar

Peticiones de dependency audit, SCA, CVE scanning, supply chain security o generación de SBOM; análisis de `package.json`, `requirements.txt`, `Cargo.toml`, `go.mod`, `pom.xml`, `build.gradle`, `composer.json` o `Gemfile`.

## Procedimiento

| Etapa                    | Acción                           | Herramientas por ecosistema                                                     |
| ------------------------ | -------------------------------- | ------------------------------------------------------------------------------- |
| 1. Inventario            | Lockfile + resolución transitiva | `npm ls --json`, `pip list --format=json`, `cargo metadata`, `go list -m -json` |
| 2. Vulnerabilidades      | Match CVE/GHSA/OSV               | `npm audit`, `pip-audit`, `cargo audit`, `govulncheck`, OWASP dependency-check  |
| 3. Malware/Typosquatting | Heurísticos                      | `npm audit --omit=dev`, `pypi-changes`, `cargo-crev`                            |
| 4. Unused/Outdated       | Dead code + version lag          | `depcheck`, `pip-autoremove`, `cargo-machete`, `go-mod-outdated`                |
| 5. Licencias             | Compatibilidad                   | `license-checker`, `pip-licenses`, `cargo-license`, `go-licenses`               |
| 6. SBOM                  | CycloneDX/SPDX                   | `cyclonedx-bom`, `syft`, `cargo-sbom`                                           |
| 7. Política              | Gate y PRs                       | Dependabot, Renovate                                                            |

Detalle de comandos: `references/dependency-audit-pipeline.md` y `references/dependency-audit-ecosystems.md`.

## Formato de salida

Informe Markdown con Summary (ecosistemas, total deps, vulns por severidad, unused, outdated), Findings `[DEP-NNN]`, ruta del SBOM y Policy Gate (FAIL si Critical > 0).

## Referencias

- `references/dependency-audit-pipeline.md`
- `references/dependency-audit-ecosystems.md`
- `references/supply-chain.md`
- `references/modern-threats.md`
- Revisión de código → `verificar-owasp`. Hardening de host → `operar-seguridad`.
