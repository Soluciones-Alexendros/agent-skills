---
name: verificar-dependencias
description: >
  Auditoría de dependencias (SCA/CVE): pipeline multi-lenguaje (npm/pip/cargo/go/maven/gradle/composer/gem)
  para detectar vulnerabilidades, malware, typosquatting, dependencias no usadas y outdated.
  Usar ante dependency audit, SCA, CVE scanning, supply chain security, SBOM generation.
  No usar para revisión de código OWASP (→ verificar-owasp) ni hardening de aplicación.
license: MIT
metadata:
  author: Soluciones-Alexendros
  version: "1.0.0"
  dominio: verificar
  tipo: atomic
  idioma: es
---

# verificar-dependencias — Auditoría de dependencias y supply chain (SCA/CVE)

## Qué hace / Propósito

Ejecuta pipeline multi-lenguaje para auditar dependencias de proyecto: detecta vulnerabilidades conocidas (CVE), malware, typosquatting, dependencias no usadas, outdated, y genera SBOM. Cubre ecosistemas npm, pip, cargo, go, maven, gradle, composer, gem.

## Cuándo usarme / Triggering

- Cuando se pida "dependency audit", "SCA", "CVE scanning", "supply chain security", "SBOM"
- Al analizar `package.json`, `requirements.txt`, `Cargo.toml`, `go.mod`, `pom.xml`, `build.gradle`, `composer.json`, `Gemfile`
- En CI/CD para gate de dependencias vulnerables
- **NO usar cuando**: Revisión de código OWASP (inyección, XSS, auth, crypto) → `verificar-owasp`; hardening de aplicación → `verificar-owasp`/`operar-seguridad`

## Pipeline de Auditoría (7 etapas)

| Etapa                        | Acción                                   | Herramientas por ecosistema                                                              |
| ---------------------------- | ---------------------------------------- | ---------------------------------------------------------------------------------------- |
| 1. **Inventario**            | Lockfile parsing + resolución transitiva | `npm ls --json`, `pip list --format=json`, `cargo metadata`, `go list -m -json`          |
| 2. **Vulnerabilidades**      | Match contra CVE/GHSA/OSV                | `npm audit`, `pip-audit`, `cargo audit`, `govulncheck`, `mvn org.owasp:dependency-check` |
| 3. **Malware/Typosquatting** | Heurísticos + base de datos conocidas    | `npm audit --omit=dev`, `pypi-changes`, `cargo-crev`, `gosec`                            |
| 4. **Unused/Outdated**       | Dead code + version lag                  | `depcheck`, `pip-autoremove`, `cargo-machete`, `go-mod-outdated`                         |
| 5. **Licencias**             | Compatibilidad + copyleft                | `license-checker`, `pip-licenses`, `cargo-license`, `go-licenses`                        |
| 6. **SBOM**                  | Generación CycloneDX/SPDX                | `cyclonedx-bom`, `syft`, `cargo-sbom`, `go-sbom`                                         |
| 7. **Política/Remediación**  | Aplicar reglas + PR automático           | `dependabot`, `renovate`, `renovate-config`                                              |

## Ecosistemas Soportados

| Ecosistema       | Lockfile                          | Herramientas clave                                            | Registros CVE                |
| ---------------- | --------------------------------- | ------------------------------------------------------------- | ---------------------------- |
| **npm**          | `package-lock.json`               | `npm audit`, `audit-ci`, `snyk`, `cyclonedx-npm`              | GitHub Advisories, npm audit |
| **pip**          | `requirements.txt`, `poetry.lock` | `pip-audit`, `safety`, `pipdeptree`, `cyclonedx-py`           | PyPI advisories, GHSA        |
| **cargo**        | `Cargo.lock`                      | `cargo audit`, `cargo-deny`, `cargo-outdated`, `cargo-sbom`   | RustSec, GHSA                |
| **go**           | `go.sum`                          | `govulncheck`, `gosec`, `go-mod-outdated`, `go-sbom`          | Go Vuln DB, GHSA             |
| **maven/gradle** | `pom.xml`, `build.gradle`         | `dependency-check`, `owasp-dep-check`, `cyclonedx-maven`      | NVD, GHSA                    |
| **composer**     | `composer.lock`                   | `composer audit`, `symfony/security-checker`, `cyclonedx-php` | Packagist advisories         |
| **gem**          | `Gemfile.lock`                    | `bundler-audit`, `gem-audit`, `cyclonedx-ruby`                | RubySec, GHSA                |

## Formato de Salida

```markdown
## Dependency Audit: [Project Name]

### Summary

- **Ecosystems**: npm, pip, cargo
- **Total deps**: 247 (123 direct, 124 transitive)
- **Vulnerabilities**: 3 Critical, 7 High, 12 Medium, 5 Low
- **Malware suspects**: 0
- **Unused**: 8
- **Outdated**: 23

### Findings

#### [DEP-001] CVE-2024-XXXX (Critical)

- **Package**: `lodash@4.17.20`
- **Ecosystem**: npm
- **Fixed in**: `4.17.21`
- **Impact**: Prototype pollution → RCE
- **Remediation**: `npm update lodash`

#### [DEP-002] Unused dependency

- **Package**: `moment@2.29.4`
- **Ecosystem**: npm
- **Reason**: Replaced by `date-fns`, no imports found
- **Remediation**: `npm uninstall moment`

### SBOM

- **Format**: CycloneDX 1.6 (JSON)
- **Location**: `sbom.cyclonedx.json`

### Policy Gate

- **Status**: FAIL (Critical > 0)
- **Action**: Block merge, create Dependabot PRs
```

## Referencias Internas

- `references/dependency-audit-pipeline.md` — 7 etapas detalladas con comandos y umbrales
- `references/dependency-audit-ecosystems.md` — Detección y comandos por ecosistema (npm/pip/cargo/go/maven/gradle/composer/gem)
- `references/supply-chain.md` — Seguridad del build, provenance, SLSA, sigstore
- `references/modern-threats.md` — Prototype pollution, typosquatting, dependency confusion

## Herramientas

| Script                  | Propósito                                                                            |
| ----------------------- | ------------------------------------------------------------------------------------ |
| `scripts/audit_deps.py` | Pipeline principal: inventario → vulns → malware → unused → licenses → SBOM → policy |
| `scripts/check_deps.py` | Verifica herramientas requeridas por ecosistema detectado                            |
| `scripts/sbom_gen.py`   | Genera SBOM CycloneDX/SPDX                                                           |

> Scripts en Python nativo, sin dependencias externas.

## Dependencias

### Requeridas (auto-detectadas por ecosistema)

- `python3` (≥ 3.10)
- `npm` / `pnpm` / `yarn` (para proyectos JS/TS)
- `pip` / `pipx` / `uv` (para proyectos Python)
- `cargo` (para proyectos Rust)
- `go` (para proyectos Go)
- `mvn` / `gradle` (para proyectos JVM)
- `composer` (para proyectos PHP)
- `bundler` (para proyectos Ruby)

### Opcionales (mejoran cobertura)

- `snyk` / `audit-ci` — SAAS para npm/pip/cargo
- `syft` — SBOM universal
- `grype` — Vulnerability scanner universal
- `cyclonedx-cli` — SBOM tooling
- `dependabot` / `renovate` — PR automáticos de actualización

Verificar con: `./scripts/check_deps.py --verbose --install-hint`

## Uso

Auditoría de dependencias y supply chain: invocar ante dependency audit, SCA, CVE scanning, malware detection, unused/outdated deps, SBOM generation, license compliance. Ver frontmatter `description` y pipeline de 7 etapas.

No usar para revisión de código OWASP (inyección, XSS, auth, crypto) → `verificar-owasp`.

## Estructura

- `SKILL.md` — pipeline, ecosistemas, formato de salida.
- `references/` — dependency-audit-pipeline, dependency-audit-ecosystems, supply-chain, modern-threats.
- `scripts/` — audit_deps.py, check_deps.py, sbom_gen.py + tests/.

## Referencias

- Internas: ver «Referencias Internas» más arriba.
- OWASP Dependency-Check: https://owasp.org/www-project-dependency-check/
- OSV (Open Source Vulnerabilities): https://osv.dev/
- GitHub Advisory Database: https://github.com/advisories
- CycloneDX: https://cyclonedx.org/
- SPDX: https://spdx.dev/
