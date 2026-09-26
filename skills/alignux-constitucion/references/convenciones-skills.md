# Convenciones de Skills ALIGNUX

## Estructura obligatoria

Cada skill es un directorio bajo `skills/` con:

```
skills/<nombre-skill>/
├── SKILL.md          (obligatorio)
├── references/       (guías flat, solo .md)
└── scripts/          (opcional)
```

## Nomenclatura

- `ALIGNUX.*` — skills del sistema (mantenimiento, seguridad, constitución).
- `dominio.subdominio.accion` — skills genéricas (web.nextjs, datos.redis, codigo.arquitectura).
- Formato: `^[a-z0-9]+(-[a-z0-9]+)*$`.

## Frontmatter

```yaml
---
name: <nombre-directorio>
description: <1-1024 chars, cuándo usar y cuándo NO>
license: MIT
metadata:
  author: Soluciones-Alexendros
  version: X.Y.Z
  dominio: <alignux|codigo|datos|integraciones|proceso|repo|web>
  idioma: es
---
```

## Tags

Taxonomía jerárquica obligatoria: `dominio.subdominio.etiqueta` (mínimo 3, máximo 10). Prefijos: sistema, web, datos, entorno, cli, lenguaje, planificacion, git, codigo, meta, comunicacion.

## Validador

`tools/validate/skill_spec.py` — exit 0 si todo válido, 1 con lista de errores. Sin dependencias externas.

## Deuda aceptada

- Licencia es global MIT (no `LICENSE.txt` por skill).
- `references/` es plano (sin subdirectorios).
- No `infrastructure/`, `languages/`, `agents/` como subdirs.

## Gobernanza

- Skills con `version` semver; bumps en `metadata.version`.
- CI: `.github/workflows/quality.yml` ejecuta validador + lint de enlaces.
