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

- `familia-subdominio` — todas las skills por fase SDLC (disenar-arquitectura, construir-upstash, verificar-owasp, operar-seguridad).
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
  dominio: <disenar|construir|verificar|operar>
  idioma: es
---
```

## Tags

Taxonomía jerárquica obligatoria: `familia.subdominio.etiqueta` (mínimo 3, máximo 10). Prefijos: disenar, construir, verificar, operar.

## Validador

`tools/validate/skill_spec.py` — exit 0 si todo válido, 1 con lista de errores. Sin dependencias externas.

## Deuda aceptada

- Licencia es global MIT (no `LICENSE.txt` por skill).
- `references/` es plano (sin subdirectorios).
- No `infrastructure/`, `languages/`, `agents/` como subdirs.

## Gobernanza

- Skills con `version` semver; bumps en `metadata.version`.
- CI: `.github/workflows/quality.yml` ejecuta validador + lint de enlaces.
