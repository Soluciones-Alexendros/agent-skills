# Convenciones, estándares y canon por ecosistema

Contraste del repositorio contra las normas reconocidas de cada stack. Si el repo declara su propia convención (config de linter, CONTRIBUTING), esa convención local tiene prioridad sobre el canon general — pero la inconsistencia interna es siempre un hallazgo. Si el lenguaje no está en la tabla, no improvisar: verificar en documentación oficial (regla 6 de la skill).

**Contrato de flota (estructura, CI, docs, Renovate):** ver `references/repo-standard/canon.md` antes de aplicar solo este fichero. Este documento cubre estilo y tooling por lenguaje; el esqueleto del repo lo fija [repo-standard](https://github.com/Iniciativas-Alexendros/repo-standard).

## Contenido

- [Canon de proyecto sano (transversal)](#canon-de-proyecto-sano)
- [Canon por lenguaje](#canon-por-lenguaje)
- [Estructuras de directorios canónicas](#estructuras-de-directorios-canonicas)
- [Gestión de dependencias](#gestion-de-dependencias)
- [Historial y versionado](#historial-y-versionado)
- [Documentación mínima](#documentacion-minima)

## Canon de proyecto sano

Todo repositorio, independientemente del stack:

- `README.md` con: qué es, requisitos, instalación, uso básico, cómo ejecutar tests, estado del proyecto.
- `LICENSE` (sin licencia = "todos los derechos reservados"; un repo público sin licencia es un P2 legal).
- `.gitignore` adecuado al stack (referencia: colección github/gitignore). Sin artefactos versionados: binarios compilados, `node_modules`, `__pycache__`, `.env` reales, credenciales, ficheros de IDE personales.
- `.editorconfig` para normalizar indentación, charset y finales de línea entre editores.
- CI mínima: lint + tests + build en cada push/PR (GitHub Actions, GitLab CI, etc.).
- Lockfile comprometido en aplicaciones (reproducibilidad); en librerías, seguir la convención del ecosistema.
- Secretos solo en variables de entorno o gestores de secretos; nunca en el árbol ni en el historial.
- Codificación UTF-8 sin BOM, finales LF, sin espacios finales (salvo formatos que lo requieran).
- Nombres de fichero portables: sin espacios ni caracteres no ASCII en código fuente. Preferir minúsculas donde el ecosistema lo hace; **no** marcar como defecto PascalCase en React/Vue, Java, Kotlin, C# o Swift (componentes/clases).

## Canon por lenguaje

En fase de diagnóstico, ejecutar formatters y linters en **modo solo lectura** (`--check`, sin autofix). No usar comandos que reescriben ficheros (`rubocop -A`, `black` sin `--check`, etc.) hasta la fase de implementación confirmada.

| Lenguaje | Guía canónica | Formateador | Linter / análisis estático | Type-check | Tests |
|---|---|---|---|---|---|
| Python | PEP 8 + PEP 257 (docstrings Google/NumPy) | black / ruff format | ruff, pylint, bandit (seguridad) | mypy / pyright | pytest, hypothesis (PBT), coverage.py, mutmut/cosmic-ray |
| JavaScript/TypeScript | Airbnb o Standard (JS), TS handbook; TS estricto (`strict: true`) | prettier | eslint (+ plugins de seguridad), tsc | tsc | vitest/jest, fast-check (PBT), stryker (mutation), playwright (E2E) |
| Go | Effective Go, Go Code Review Comments | gofmt / goimports | golangci-lint, go vet, staticcheck | (integrado) | go test, testing/quick, go test -fuzz, go test -race/-cover |
| Rust | Rust API Guidelines, Clippy lints | rustfmt | clippy, cargo audit (CVEs) | (integrado) | cargo test, proptest/quickcheck, cargo-mutants, cargo-tarpaulin |
| Java | Google Java Style | google-java-format / spotless | checkstyle, spotbugs, error-prone | (integrado) | JUnit 5, jqwik (PBT), pitest (mutation), JaCoCo |
| C/C++ | CERT C/C++, Google C++ Style; MISRA si es crítico | clang-format | clang-tidy, cppcheck, sanitizers (ASan/UBSan) | (integrado) | GoogleTest/Catch2, libFuzzer/AFL++, sanitizers en CI |
| C# | Microsoft C# Coding Conventions | dotnet format | Roslyn analyzers, SonarAnalyzer | (integrado) | xUnit/NUnit, FsCheck (PBT), Stryker.NET, coverlet |
| Ruby | Ruby Style Guide (RuboCop) | rubocop (solo lectura en diagnóstico) | rubocop, brakeman (seguridad Rails) | sorbet/rbs | RSpec/minitest, rantly, mutant |
| PHP | PSR-1/PSR-12 | php-cs-fixer / pint | PHPStan/Psalm | PHPStan niveles | PHPUnit, infection (mutation) |
| Swift | Swift API Design Guidelines | swift-format | SwiftLint | (integrado) | XCTest, SwiftCheck |
| Kotlin | Kotlin Coding Conventions | ktlint | detekt | (integrado) | JUnit 5, kotest-property |
| Shell | Google Shell Style Guide | shfmt | shellcheck | — | bats |
| SQL | Estilo consistente; migraciones versionadas | sqlfluff fix | sqlfluff | — | tSQLt / pgTAP según motor |

Notas transversales:

- **Sanitizado de entradas**: validar en el borde (límites, tipos, formatos); parametrizar SQL; escapar salidas HTML; normalizar rutas frente a path traversal. Referencia: OWASP Top 10 y OWASP ASVS.
- **Gestión de errores**: nunca tragar excepciones; errores con contexto; fail-fast en invariantes violados.
- **Logging**: niveles coherentes, sin datos sensibles, sin logs de debug en producción.

## Estructuras de directorios canónicas

- **Librería Python**: `src/<paquete>/`, `tests/`, `docs/`, `pyproject.toml`. Evitar paquetes planos con tests mezclados.
- **App Node/TS**: `src/` (o `app/`), `tests/` o `__tests__` colocalizados, `public/`, config en raíz. Monorepos: `apps/`, `packages/` (pnpm workspaces/turborepo).
- **Go**: módulos en raíz, `cmd/<binario>/`, `internal/`, `pkg/` solo si es API pública real.
- **Rust**: `src/lib.rs` + `src/main.rs`, `tests/` (integración), `benches/`, `examples/`.
- **Java/Kotlin**: `src/main/java|kotlin/`, `src/test/...` (Maven/Gradle estándar).
- **Web frontend**: separación por dominio/feature sobre separación por tipo técnico cuando el proyecto crece; assets en `public/` o `assets/`, estilos con sistema de tokens.

Criterio general: la estructura debe hacer evidente dónde vive cada cosa; profundidad excesiva (>4 niveles sin justificación) o ficheros huérfanos en raíz son señal de deuda estructural.

## Gestión de dependencias

- Versiones fijadas (exactas o rangos conservadores `^`/`~`/`>=` acotados según ecosistema); nunca `*`/`latest` en producción.
- Auditoría de CVEs: `npm audit`, `pip-audit`, `cargo audit`, `govulncheck`, `bundle audit`, OWASP Dependency-Check.
- Dependencias muertas: eliminar las no importadas/usadas (`depcheck`, `pipreqs` vs requirements, `cargo machete`).
- Actualización escalonada: primero parches de seguridad, luego minor, majors solo con plan (si rompen API → propuesta disruptiva).

## Historial y versionado

- Conventional Commits: `tipo(ámbito): descripción` — tipos: feat, fix, refactor, test, docs, style, perf, build, ci, chore, revert.
- Versionado semántico 2.0: MAJOR.MINOR.PATCH; pre-1.0, cualquier cosa puede romper.
- Tags y CHANGELOG.md sincronizados con releases (formato Keep a Changelog).
- Ramas: troncal corta o trunk-based; ramas abandonadas antiguas se listan en el informe.

## Documentación mínima

- README actualizado (si describe comandos que ya no funcionan → P2).
- Docstrings/comentarios explican el *porqué*, no el *qué*; código autoexplicativo sobre comentarios redundantes.
- Decisiones de arquitectura relevantes: ADRs en `docs/adr/` si el proyecto las usa.
