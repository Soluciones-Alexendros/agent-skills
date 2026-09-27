# Changelog

## [Unreleased]

- Reestructuración de skills 2026-09-27 (21 → 18):
  - `auditoria-360-web` → `web-compliance` 1.0.0 (major): conserva accesibilidad, legal, SEO/SEM; absorbe SEO/a11y de `web-audit`
  - Nueva `web-rendimiento` 1.0.0: CWV, carga, caché, SEO técnico (split web + resto de `web-audit`)
  - Suprimidas: `web-audit` (absorbida), `datos-postgres`, `planificacion-archivos`, `dependency-audit` (absorbida en `web-seguridad`)
  - `codigo-seguridad` → `web-seguridad` 1.0.0 (major, absorbe dependencias)
  - `playwright-e2e-audit` → `web-playwright` 1.0.0 (major)
  - `git-hooks` → `repo-precommit` 1.0.0 (major)
  - `alignux-seguridad` → `linux-seguridad` 1.0.0, `alignux-mantenimiento` → `linux-mantenimiento` 1.0.0 (major, nuevo dominio `linux`)
  - `email-proton` / `protonpass` 1.0.0 (major): thin-skills con enlaces pineados a protonsuite-tools v1.4.0
  - `upstash` 0.3.0 (minor: pierde referencia a `datos-postgres`); retoques de enlaces 0.2.x: `web-diseno`, `webapp-testing`, `design-system`, `repo-starting`, `repo-ending`, `codigo-arquitectura`, `alignux-constitucion` 0.2.1

- `repo-starting` 0.2.0 -> 0.2.1 (patch)

  cambios P2 sobre aplanado
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
