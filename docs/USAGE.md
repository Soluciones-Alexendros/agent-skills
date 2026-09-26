# Uso de las skills

## Claude Code

Copiar o enlazar la carpeta de la skill al directorio de skills del usuario o del proyecto:

```bash
# global
cp -r skills/codigo-seguridad ~/.claude/skills/
# o por proyecto
cp -r skills/codigo-seguridad /ruta/proyecto/.claude/skills/
```

Claude Code descubre el `SKILL.md` por su frontmatter (`name` + `description`).

## OpenAI Codex / agentes compatibles

Copiar la carpeta a la ubicación que el agente use para skills (consultar su documentación; el formato `SKILL.md` + frontmatter es el estándar abierto de [agentskills.io](https://agentskills.io)).

## Uso manual

Cada `SKILL.md` es autocontenido y legible: sus `references/` amplían por niveles y sus `scripts/` automatizan lo repetible (ver sección de herramientas de cada skill).

## Elegir skill

- Por dominio: ver tabla en [README](../README.md) y [TAXONOMY.md](TAXONOMY.md).
- Los `description` declaran límites explícitos (`No usar para X → otra-skill`); ante solape, seguir esa indicación.
