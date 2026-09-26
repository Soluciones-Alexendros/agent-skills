# Changelog

## [Unreleased]

- `repo-starting` 0.2.0 -> 0.2.1 (patch)

  identidad P3 sobre aplanado

- `repo-starting` 0.1.0 -> 0.2.0 (minor)

  aplanar references/repo-standard (regla references planas)


Formato: entradas por release del repo. Las skills versionan además su `metadata.version` en cada `SKILL.md`.

## [Unreleased]

- `alignux-constitucion` 0.1.0 -> 0.2.0 (minor)
- `alignux-mantenimiento` 0.1.0 -> 0.2.0 (minor)
- `alignux-seguridad` 0.1.0 -> 0.2.0 (minor)
- `auditoria-360-web` 0.1.0 -> 0.2.0 (minor)
- `codigo-arquitectura` 0.1.0 -> 0.2.0 (minor)
- `codigo-seguridad` 0.1.0 -> 0.2.0 (minor)
- `datos-postgres` 0.1.0 -> 0.2.0 (minor)
- `dependency-audit` 0.1.0 -> 0.2.0 (minor)
- `email-proton` 0.1.0 -> 0.2.0 (minor)
- `planificacion-archivos` 0.1.0 -> 0.2.0 (minor)
- `playwright-e2e-audit` 0.1.0 -> 0.2.0 (minor)
- `protonpass` 0.1.0 -> 0.2.0 (minor)
- `repo-ending` 0.1.0 -> 0.2.0 (minor)
- `repo-starting` 0.1.0 -> 0.2.0 (minor)
- `typescript-avanzado` 0.1.0 -> 0.2.0 (minor)
- `upstash` 0.1.0 -> 0.2.0 (minor)
- `web-audit` 0.1.0 -> 0.2.0 (minor)
- `web-diseno` 0.1.0 -> 0.2.0 (minor)
- `webapp-testing` 0.1.0 -> 0.2.0 (minor)

  Revisión P0-P4: enlaces, validators, CI, smoke tests, expansión de skills thin, extracción de cuerpos, identidad de grupo, documentación

- Autoversionado semver por magnitud: `tools/version/bump.py` (`major` = actualización incompatible, `minor` = desarrollo menor compatible, `patch` = parcheado/fix; con alias en ES), tests propios, cobertura en `run-validation.sh` y CI `version.yml` que exige el bump en PRs con skills cambiadas.

## [v0.1.0] — 2026-09-26

Primera publicación pública del repo `Soluciones-Alexendros/agent-skills` (21 skills, licencia MIT).

- Estructura `skills/<nombre>/` con frontmatter normalizado (`license: MIT`, `metadata` con autor, versión, dominio e idioma).
- Taxonomía por dominios (`alignux`, `codigo`, `datos`, `integraciones`, `proceso`, `repo`, `web`).
- Limpieza: eliminados `__pycache__/`, `.pytest_cache/`, archivados legacy, licencias por skill y subdirectorios no canónicos (aplanados a `references/`).
- `planificacion-archivos`: cuerpo reducido bajo 500 líneas (extraído `references/claude-code-integration.md`).
- `codigo-seguridad`: creado `references/security-checklist.md` (estaba citado pero ausente).
- Validadores `tools/validate/` (spec + enlaces), CI en `.github/workflows/` y `run-validation.sh` agregado.

[Unreleased]: https://github.com/Soluciones-Alexendros/agent-skills/compare/v0.1.0...HEAD
[v0.1.0]: https://github.com/Soluciones-Alexendros/agent-skills/releases/tag/v0.1.0
