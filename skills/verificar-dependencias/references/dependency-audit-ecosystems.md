# Ecosistemas — heurísticas de detección

Cómo detectar el ecosistema de un proyecto por sus ficheros característicos, y qué
herramientas de auditoría corresponden a cada uno.

## Tabla de detección

| Ecosistema     | Fichero clave _(ejemplo)_                        | Lockfile _(ejemplo)_                               | Herramienta de auditoría                                      |
| -------------- | ------------------------------------------------ | -------------------------------------------------- | ------------------------------------------------------------- |
| npm / Node.js  | `package.json`                                   | `package-lock.json`, `pnpm-lock.yaml`, `yarn.lock` | `npm audit --json`, Socket.dev, Depcheck                      |
| pip / Python   | `pyproject.toml`, `requirements.txt`, `setup.py` | `uv.lock`, `poetry.lock`, `pip-compile`            | `pip-audit`, `safety check`, `deptry`                         |
| Cargo / Rust   | `Cargo.toml`                                     | `Cargo.lock`                                       | `cargo audit`, `cargo outdated`, `cargo udeps`                |
| Go             | `go.mod`                                         | `go.sum`                                           | `govulncheck`, `go list -m -u all`                            |
| Maven / JVM    | `pom.xml`                                        | _(implícito: `mvn dependency:tree`)_               | `dependency-check`, `mvn versions:display-dependency-updates` |
| Gradle / JVM   | `build.gradle`, `build.gradle.kts`               | `gradle.lockfile`                                  | `dependency-check`, `gradle dependencyInsight`                |
| Composer / PHP | `composer.json`                                  | `composer.lock`                                    | `composer audit`, `security-checker`                          |
| Gem / Ruby     | `Gemfile`                                        | `Gemfile.lock`                                     | `bundle audit`, `bundle outdated`                             |

## Heurísticas por ecosistema

### npm / Node.js

- `package.json` presente → proyecto npm. Verificar `package-lock.json` para builds reproducibles.
- Monorepo: buscar `package.json` en subcarpetas y `pnpm-workspace.yaml` / `lerna.json`.
- Árbol transitivo: `npm ls --all`.

### pip / Python

- `pyproject.toml` con `[project]` → proyecto moderno (PEP 621); `dependencies` = directas.
- `requirements.txt` con `==` → versiones fijadas; con `>=` o sin fijar → riesgo de deriva.
- Entorno gestionado por `uv` (`uv.lock`) o Poetry (`poetry.lock`) → usar su lockfile como fuente de verdad.

### Cargo / Rust

- `Cargo.toml` con `[dependencies]` / `[dev-dependencies]` → directas por categoría.
- Workspace: `Cargo.toml` con `[workspace]` y miembros en subcarpetas → auditar cada miembro.
- `cargo tree` para el árbol transitivo.

### Go

- `go.mod` presente → módulos Go. `require` = directas, `// indirect` = transitivas.
- Sin lockfile的传统: `go.sum` solo registra checksums; versiones en `go.mod`.
- Auditar con `govulncheck ./...` (base de datos de vulnerabilidades Go).

### Maven / JVM

- `pom.xml` presente → proyecto Maven. `<dependencies>` = directas, `<dependencyManagement>` = versiones controladas.
- multi-módulo: `<modules>` con `pom.xml` por módulo → auditar cada módulo.
- Plugin OWASP `dependency-check` cubre CVEs; `mvn dependency:tree` para transitivas.

### Gradle / JVM

- `build.gradle` o `build.gradle.kts` presente → proyecto Gradle. Bloque `dependencies { ... }` = directas.
- `gradle.lockfile` → versiones fijadas; ausente → deriva posible.
- `gradle dependencies` para el árbol; `dependency-check` para CVEs.

### Composer / PHP

- `composer.json` presente → proyecto Composer. `require` = directas, `require-dev` = desarrollo.
- `composer.lock` → versiones fijadas; ausente → `composer install` puede resolver versiones distintas.
- `composer audit` contra la base de seguridad de Packagist.

### Gem / Ruby

- `Gemfile` presente → proyecto Ruby con Bundler. `Gemfile.lock` = versiones fijadas.
- `gem 'x', '~> 1.2'` → rango semver; sin constraint → riesgo de deriva.
- `bundle audit` para CVEs; `bundle outdated` para actualizaciones.

## Reglas transversales

1. Múltiples ecosistemas en un monorepo → detectar cada uno y auditar por separado.
2. Lockfile ausente en npm/Python/PHP/Ruby → señalar como riesgo antes de auditar versiones.
3. Lockfile presente pero no commiteado → recomendar añadirlo al repo (regla de oro: lockfile sagrado).
4. Nunca instalar o actualizar ciegamente: verificar cada cambio con la herramienta de comportamiento (Socket.dev) antes de aplicar.
