# Estándar de skills del repo

Basado en la [especificación Agent Skills](https://agentskills.io/specification). El validador `tools/validate/skill_spec.py` hace cumplir estas reglas.

## Frontmatter de `SKILL.md` (obligatorio)

```yaml
---
name: mi-skill            # = nombre de la carpeta; kebab-case, 1–64 chars, sin -- ni - extremos
description: >-           # 1–1024 chars; qué hace + cuándo usarla + qué NO cubre (→ otra skill)
  ...
license: MIT              # licencia global del repo
metadata:
  author: Soluciones-Alexendros
  version: "0.1.0"        # semver de la skill
  dominio: codigo         # uno de docs/TAXONOMY.md
  idioma: es
---
```

Campos opcionales de la spec (`compatibility`, `allowed-tools`) pueden añadirse cuando aporten valor.

## Cuerpo

- Límite recomendado: **< 500 líneas**. Si crece, extraer a `references/*.md` y dejar un resumen con enlace.
- Secciones sugeridas: propósito, uso, estructura, herramientas, referencias.
- Enlaces relativos solo a ficheros que existen (lo verifica `tools/validate/skill_links.py`).
- Referencias de un nivel: `references/` no debe contener subdirectorios con contenido enlazado (los `assets/` y `scripts/` son recursos, no lectura progresiva).

## Estructura de carpeta

```text
skills/<nombre>/
├── SKILL.md
├── references/   # lectura progresiva (md)
├── scripts/      # scripts ejecutables + tests/
├── assets/       # plantillas, esquemas, estáticos
└── configs/      # configuraciones de ejemplo
```

Prohibido en el repo: `__pycache__/`, `.pytest_cache/`, dirs `.archivado-*`, ficheros `LICENSE` por skill, `agents/`, `infrastructure/`, `languages/` sueltos (van aplanados en `references/`).

## Versiones

- `metadata.version` por skill (semver). Cambios incompatibles de instrucciones → bump minor/major y nota en [CHANGELOG.md](../CHANGELOG.md).
- Release del repo: tag `vX.Y.Z` + GitHub Release (workflow `release.yml`).
