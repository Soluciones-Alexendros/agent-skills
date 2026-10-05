# OpenCode Setup — agent-skills v3.0 (vendor-neutral)

Esta guía explica cómo usar Agent Skills con OpenCode de forma agent-driven (sin slash commands).

## Overview

OpenCode no tiene plugin system nativo. Logramos paridad con:

- System prompt fuerte (`AGENTS.md`)
- Built-in `skill` tool
- Descubrimiento consistente desde `/skills` + `skill-index.json`

## Instalación

1. Clone:

```bash
git clone https://github.com/Soluciones-Alexendros/agent-skills.git
```

2. Abre proyecto en OpenCode
3. Asegura que existen:

- `AGENTS.md` (root)
- `opencode.json`
- `skills/` directorio
- `.opencode/agents/skill-router.md`

No requiere instalación adicional.

## Cómo funciona

### 1. Skill Discovery

Todas las skills viven en:

```
skills/<skill-name>/SKILL.md
```

OpenCode agents son instruidos vía AGENTS.md a:

- Detectar cuándo aplica una skill
- Invocar `skill` tool
- Seguir la skill exactamente

### 2. Automatic Skill Invocation

El agente evalúa cada request y mapea a skill apropiada.
Ejemplos:

- "limpia mi Arch" → `operate-maintenance` + `operate-health`
- "revisa la arquitectura" → `verify-architecture`
- "prepara release" → `operate-release`
- "audita compliance" → `verify-compliance`

El usuario NO necesita pedir skills explícitamente.

### 3. Lifecycle Mapping

- DEFINE → planning-spec-driven-development
- PLAN → planning-task-breakdown
- BUILD → build-* + planning-test-driven-development
- VERIFY → verify-*
- OPERATE → operate-*
- DESIGN → design-*

### Agent Expectations (Critical)

- Always check if a skill applies before acting
- If a skill applies, it MUST be used
- Never skip required workflows
- Do not jump directly to implementation

Estas reglas son forzadas vía AGENTS.md y `tools/skill-router/route.py`.

## Recommended Workflow

Usa lenguaje natural:

- "Diseña feature X"
- "Planifica este cambio"
- "Limpia mi sistema"
- "Audita y publica"

El agente seleccionará automáticamente la skill correcta.

## Vendor-neutral

Este setup es OpenCode-first, solo usa OpenCode + estándares abiertos, sin dependencias de un único vendor.
