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
- Autoversionado por magnitud con `tools/version/bump.py` (sin dependencias):

| Magnitud | Alias ES | Efecto | Cuándo |
|---|---|---|---|
| `major` | actualización, breaking, incompatible | `X.y.z` → `X+1.0.0` | instrucciones incompatibles |
| `minor` | desarrollo menor, feature, funcionalidad | `x.Y.z` → `x.Y+1.0` | nueva capacidad compatible |
| `patch` | parche, parcheado, fix, corrección | `x.y.Z` → `x.y.Z+1` | fix compatible, docs, typos |

```bash
python3 tools/version/bump.py --type minor --skills web-seguridad
python3 tools/version/bump.py --type parche --all --dry-run
python3 tools/version/bump.py --type fix --auto --base origin/main
python3 tools/version/bump.py --check --auto --base origin/main  # lo que exige la CI
```

- El bumper actualiza `SKILL.md`, añade la entrada a `## [Unreleased]` del CHANGELOG y sugiere el tag de repo (`--tag` lo crea: `vX.Y.Z`).
- La CI (`version.yml`) falla en la PR si una skill cambiada no trae su bump.
- Release del repo: tag `vX.Y.Z` + GitHub Release (workflow `release.yml`).
