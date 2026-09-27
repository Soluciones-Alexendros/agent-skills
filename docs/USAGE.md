# Uso de las skills

## Claude Code

Copiar o enlazar la carpeta de la skill al directorio de skills del usuario o del proyecto:

```bash
# global
cp -r skills/web-seguridad ~/.claude/skills/
# o por proyecto
cp -r skills/web-seguridad /ruta/proyecto/.claude/skills/
```

Claude Code descubre el `SKILL.md` por su frontmatter (`name` + `description`).

## OpenAI Codex / agentes compatibles

Copiar la carpeta a la ubicación que el agente use para skills (consultar su documentación; el formato `SKILL.md` + frontmatter es el estándar abierto de [agentskills.io](https://agentskills.io)).

## Uso manual

Cada `SKILL.md` es autocontenido y legible: sus `references/` amplían por niveles y sus `scripts/` automatizan lo repetible (ver sección de herramientas de cada skill).

## Elegir skill

- Por dominio: ver tabla en [README](../README.md) y [TAXONOMY.md](TAXONOMY.md).
- Los `description` declaran límites explícitos (`No usar para X → otra-skill`); ante solape, seguir esa indicación.

## Versionado automático

Cada skill declara `metadata.version` en su frontmatter. Al modificar instrucciones, bump según la magnitud:

```bash
python3 tools/version/bump.py --auto --type <major|minor|patch>
```

- `major`: actualización incompatible (breaking)
- `minor`: desarrollo menor, nueva funcionalidad compatible
- `patch`: parcheado, fix compatible

La CI (`version.yml`) exige el bump en PRs con skills cambiadas. Para verificar localmente:

```bash
python3 tools/version/bump.py --check --auto --base origin/main
```

## Estructura de references/ (carga progresiva)

Cada skill sigue el patrón de carga progresiva:

1. `SKILL.md` — arranque autocontenido con el 80% de los casos resueltos.
2. `references/` — guías detalladas por tema, se cargan solo cuando el caso lo requiere.
3. `scripts/` — utilidades automatizadas (no se cargan en contexto, se ejecutan).

Esto mantiene el contexto del agente ligero: solo se lee lo necesario para la tarea.

## Validación

Toda skill debe pasar la validación del repo en verde:

```bash
bash run-validation.sh
```

Ejecuta: spec (`skill_spec.py`), enlaces (`skill_links.py`), bump de versión, pytest, smoke tests y `bash -n` global. Ver [CONTRIBUTING.md](CONTRIBUTING.md) para el proceso de contribución.
