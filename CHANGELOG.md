# Changelog

## [Unreleased]

- `repo-starting` 0.2.0 -> 0.2.1 (patch)

  cambios P2 sobre aplanado

- `repo-starting` 0.1.0 -> 0.2.0 (minor)

  aplanar references/repo-standard (regla references planas)


Formato: entradas por release del repo. Las skills versionan además su `metadata.version` en cada `SKILL.md`.

## [v0.1.0] — 2026-09-26

Primera publicación pública del repo `Soluciones-Alexendros/agent-skills` (21 skills, licencia MIT).

- Estructura `skills/<nombre>/` con frontmatter normalizado (`license: MIT`, `metadata` con autor, versión, dominio e idioma).
- Taxonomía por dominios (`alignux`, `codigo`, `datos`, `integraciones`, `proceso`, `repo`, `web`).
- Limpieza: eliminados `__pycache__/`, `.pytest_cache/`, archivados legacy, licencias por skill y subdirectorios no canónicos (aplanados a `references/`).
- `planificacion-archivos`: cuerpo reducido bajo 500 líneas (extraído `references/claude-code-integration.md`).
- `codigo-seguridad`: creado `references/security-checklist.md` (estaba citado pero ausente).
- Validadores `tools/validate/` (spec + enlaces), CI en `.github/workflows/` y `run-validation.sh` agregado.
