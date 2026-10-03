# Estándar de skills del repo

Basado en la [especificación Agent Skills](https://agentskills.io/specification). El validador `tools/validate/skill_spec.py` hace cumplir estas reglas.

## Frontmatter de `SKILL.md` (obligatorio)

```yaml
---
name: mi-skill # = nombre de la carpeta; kebab-case, 1–64 chars, sin -- ni - extremos
description: >- # 1–1024 chars; plantilla abajo
  ...
license: MIT # licencia global del repo
metadata:
  author: Soluciones-Alexendros
  version: "0.1.0" # semver de la skill
  dominio: construir # uno de docs/TAXONOMY.md: disenar | construir | verificar | operar
  tipo: atomic # atomic | router | tecnologia
  idioma: es
---
```

Campos opcionales de la spec (`compatibility`, `allowed-tools`) pueden añadirse cuando aporten valor.

## Descripción (plantilla)

Tercera persona, dentro de 1024 caracteres:

`[Capacidad]. Usar cuando [contextos]. No usar para [límite] (→ skill-vecina).`

Las frases `Usar cuando` y `No usar para` son literales (el validador las exige). La flecha `→ nombre` solo si `nombre` es una carpeta real en `skills/`.

## Cuerpo

- Límite obligatorio: **≤ 500 líneas** y **≤ 5000 tokens**. Si crece, extraer a `references/*.md` y dejar un resumen con enlace.
- Encabezados H2 canónicos en español. Obligatorios: **Propósito**, **Cuándo usar**, **Referencias**. Si hay ejecutables `.py` o `.sh` fuera de `tests/`: **Herramientas**.
- Opcionales con contenido real: Alcance, Procedimiento, Formato de salida, Casos límite, Validación, más las secciones de dominio que el procedimiento necesite (Enrutado, Fases, Modos).
- Prohibidos: `Qué hace / Propósito`, `Cuándo usarme / Triggering`, un `Uso` que repita la descripción, un `Estructura` de inventario, `Perfil de Este Equipo`, rutas `sudoers.d` y nombres de host en el arranque.
- Enlaces relativos solo a ficheros que existen (`tools/validate/skill_links.py`).
- `references/` es plano: sin subdirectorios. `assets/` y `scripts/` son recursos, no lectura progresiva.

## Estructura de carpeta

```text
skills/<nombre>/
├── SKILL.md
├── references/   # lectura progresiva (md plano)
├── scripts/      # ejecutables + tests/ (smoke en scripts/tests/smoke_sh.sh)
├── assets/       # plantillas, esquemas, estáticos
└── configs/      # configuraciones de ejemplo
```

Excepción: `construir-upstash` usa `core/` y `modes/<modo>/` como recursos internos del router. Cada `modes/<modo>/references/` sigue siendo plano. No son skills separadas.

Prohibido en el repo: `__pycache__/`, `.pytest_cache/`, dirs `.archivado-*`, ficheros `LICENSE` por skill, `agents/`, `infrastructure/`, `languages/` sueltos (van aplanados en `references/`). El validador solo falla si esos residuos están rastreados por git.

## Procedimientos (scripts y lógica)

Estructura: **Precondition → Action → Expected → Error → Recovery**.
Scripts: **INPUT → validate → execute → inspect → structured output → exit code**.
Salida estructurada: JSON para consumo máquina, Markdown para humano.
Códigos de salida: `0` OK, `1` error o veredicto negativo, `2` input inválido, `3` dependencia ausente, `4` permiso denegado.

Smoke: `skills/<nombre>/scripts/tests/smoke_sh.sh` es obligatorio si y solo si hay ejecutables `.py` o `.sh` fuera de `tests/` y de `test_*.py`.

## MCP Tools

Convención: `ServerName:tool_name` (ej. `firecrawl:firecrawl_search`, `github:github_search_code`).

## Versiones (dos ejes)

1. **Skill** — `metadata.version` en cada `SKILL.md`. La CI (`version.yml`) exige bump en PRs que toquen esa skill.
2. **Repo** — `package.json` `version` + tag anotado `vX.Y.Z` + sección del [CHANGELOG.md](../CHANGELOG.md). El workflow de release corta el tag y publica la GitHub Release cuando el manifiesto está por delante del último tag y el changelog tiene notas.

Autoversionado de skills con `tools/version/bump.py`:

| Magnitud | Alias ES                                 | Efecto              | Cuándo                      |
| -------- | ---------------------------------------- | ------------------- | --------------------------- |
| `major`  | actualización, breaking, incompatible    | `X.y.z` → `X+1.0.0` | instrucciones incompatibles |
| `minor`  | desarrollo menor, feature, funcionalidad | `x.Y.z` → `x.Y+1.0` | nueva capacidad compatible  |
| `patch`  | parche, parcheado, fix, corrección       | `x.y.Z` → `x.y.Z+1` | fix compatible, docs, typos |

```bash
python3 tools/version/bump.py --type minor --skills verificar-owasp
python3 tools/version/bump.py --type parche --all --dry-run
python3 tools/version/bump.py --check --auto --base origin/main
python3 tools/version/cut_tag.py --dry-run
```

Corte de tag del repo: `tools/version/cut_tag.py` (el workflow de `main` lo aplica; no etiquetar a mano en el árbol de trabajo).
