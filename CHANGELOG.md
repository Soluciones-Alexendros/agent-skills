# Changelog

Todas las versiones notables de este repositorio se documentan aquí. Formato: [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/). Versionado: [SemVer 2.0.0](https://semver.org/spec/v2.0.0.html).

La versión `2.1.0` de `package.json` no se publicó (no hubo tag ni sección de changelog). Su contenido queda absorbido en 2.2.0.

## [Unreleased]

### Added

- `operar-release` 2.2.0: modo G cierre de trabajo al finalizar un plan (`references/cierre-trabajo.md`): gate Husky, e2e Playwright, revisión contra el plan, PRs a `main`, merge-watch squash y limpieza.
- `verificar-repo` 2.2.0: modo I inicio de plan / repo starting (`references/inicio-plan.md`) y script `inicio_plan.py` (tablero `ESTADO.md` + `ESTADO.html`: git, camino del producto, fallos).

### Changed

- `operar-lifecycle` 1.3.0: enruta repo starting / modo plan a `verificar-repo` I y repo ending a `operar-release` G.
- `verificar-hooks` 3.2.0: modo gate y `pre-push` e2e cuando el repo ya tiene script Playwright.
- `verificar-repo` Fase 8 distingue publicación (B/F) y cierre de trabajo (G).
- `operar-release` merge-watch: `/pr-babysit --ship`, Vercel Hobby no requerido, `--delete-branch`.

## [2.2.0] - 2026-09-30

### Added

- Skills `verificar-dependencias` 1.0.1 y `operar-salud-sistema` 1.1.0 al catálogo (19 skills).
- Validadores `tools/validate/release_coherence.py` y `tools/validate/hygiene.py`.
- Corte de tag y GitHub Release: `tools/version/cut_tag.py` y workflow `release.yml` (notas desde el changelog, SHA pinning, provenance).
- `SECURITY.md`, `.github/CODEOWNERS`, `.github/dependabot.yml`, `requirements-dev.txt`.
- Archivo de operador `docs/archives/perfil-equipo-local.md` (fuera del paquete de la skill).

### Changed

- Canon de formulación en español (`docs/STANDARD.md`): descripción `Usar cuando` / `No usar para`, encabezados Propósito / Cuándo usar / Referencias.
- Puntos de entrada de las 19 skills alineados al canon. Minor: `operar-mantenimiento` 2.2.0, `disenar-constitucion` 1.2.0, `operar-salud-sistema` 1.1.0, `operar-seguridad` 2.2.0, `verificar-owasp` 2.2.0. Patch en el resto.
- Encabezados históricos del changelog a `## [X.Y.Z] - AAAA-MM-DD`.
- `contrast.py`: exit 1 cuando el par no cumple AA.

### Fixed

- Catálogo README (decía 17) alineado a 19 carpetas y a TAXONOMY.
- `verificar-owasp`: valla del formato de informe y sección Estructura que citaba `languages/`, `infrastructure/` y LICENSE inexistentes.
- `verificar-dependencias`: dejaba de documentar scripts que no existen.
- `release.yml` instalaba PyYAML, extraía notas del changelog y dejaba de usar `generate_release_notes`.

## [2.0.0] - 2026-09-27

- `construir-typescript` 2.0.0 -> 2.0.1 (patch)
- `construir-upstash` 1.0.0 -> 1.0.1 (patch)
- `verificar-compliance` 2.0.0 -> 2.0.1 (patch)

  Limpieza de referencias aspiracionales a skills inexistentes (web-nextjs, datos-*, cli-upstash, entorno-aislado); linaje absorbido (web-playwright, webapp-testing, web-rendimiento) conservado

- `construir-typescript` 1.0.0 -> 2.0.0 (major)
- `construir-upstash` 0.4.0 -> 1.0.0 (major)
- `disenar-arquitectura` 0.3.0 -> 1.0.0 (major)
- `disenar-constitucion` 0.2.1 -> 1.0.0 (major)
- `disenar-design-system` 0.2.0 -> 1.0.0 (major)
- `disenar-interfaz` 0.3.0 -> 1.0.0 (major)
- `operar-lifecycle` 0.1.0 -> 1.0.0 (major)
- `operar-mantenimiento` 1.0.0 -> 2.0.0 (major)
- `operar-release` 1.0.0 -> 2.0.0 (major)
- `operar-seguridad` 1.0.0 -> 2.0.0 (major)
- `verificar-compliance` 1.0.0 -> 2.0.0 (major)
- `verificar-fullaudit` 1.0.0 -> 2.0.0 (major)
- `verificar-hooks` 2.0.0 -> 3.0.0 (major)
- `verificar-owasp` 1.0.0 -> 2.0.0 (major)
- `verificar-performance` 2.0.0 -> 3.0.0 (major)
- `verificar-repo` 1.0.0 -> 2.0.0 (major)

  Reestructuración a 4 familias por fase SDLC (disenar/construir/verificar/operar); fusión email-proton+protonpass → construir-proton-suite v1.0.0; dominios alignux, datos, integraciones suprimidos

## [1.0.0] - 2026-09-27

- Consolidación FASE-4 (18 skills, 7 dominios): `docs/TAXONOMY.md`, `README.md` y `tools/validate/skill_spec.py` alineados a los nombres reales; `web-seguridad` con cuerpo íntegramente en ES (tecnicismos en inglés preservados).
- Tabla de renombros/fusiones:
  | Antes                 | Ahora               | Tipo                                  |
  | --------------------- | ------------------- | ------------------------------------- |
  | `web-rendimiento`     | `web-performance`   | renombro                              |
  | `design-system`       | `web-design-system` | renombro                              |
  | `typescript-avanzado` | `codigo-typescript` | renombro                              |
  | `repo-starting`       | `repo-audit`        | renombro                              |
  | `repo-precommit`      | `repo-hooks`        | renombro                              |
  | `repo-ending`         | `repo-release`      | renombro                              |
  | —                     | `repo-lifecycle`    | nueva (enrutador audit/hooks/release) |
  | —                     | `web-fullaudit`     | nueva (orquestador de auditoría web)  |
  | `web-playwright`      | —                   | suprimida                             |
  | `webapp-testing`      | —                   | suprimida                             |
- Canon `docs/repo-standard/` (solo lectura): `structure.md`, `ci-cd.md`, `release.md`, `security.md`, `templates/` (PR, issues, commitlint)
- Autoversionado semver por magnitud: `tools/version/bump.py`.

## [0.1.0] - 2026-09-26

Primera publicación pública del repo `Soluciones-Alexendros/agent-skills` (21 skills, licencia MIT).

- Estructura `skills/<nombre>/` con frontmatter normalizado (`license: MIT`, `metadata` con autor, versión, dominio e idioma).
- Validadores `tools/validate/` (spec + enlaces), CI en `.github/workflows/` y `run-validation.sh` agregado.

[Unreleased]: https://github.com/Soluciones-Alexendros/agent-skills/compare/v2.2.0...HEAD
[2.2.0]: https://github.com/Soluciones-Alexendros/agent-skills/compare/v2.0.0...v2.2.0
[2.0.0]: https://github.com/Soluciones-Alexendros/agent-skills/compare/v1.0.0...v2.0.0
[1.0.0]: https://github.com/Soluciones-Alexendros/agent-skills/compare/v0.1.0...v1.0.0
[0.1.0]: https://github.com/Soluciones-Alexendros/agent-skills/releases/tag/v0.1.0
