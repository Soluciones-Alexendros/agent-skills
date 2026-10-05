# Routing Avanzado — Determinista + LLM

## Objetivo

Fluidez en invocación automatizada por agentes de código sin depender solo del LLM.

## Componentes

1. `skill-index.json` — índice machine-readable con keywords, triggers, routes
2. `tools/skill-router/intent-map.yaml` — patrones ES/EN
3. `tools/skill-router/route.py` — scoring TF + trigger boost (0 dependencias)
4. `.opencode/agents/skill-router.md` — agente OpenCode que invoca route.py antes de decidir

## Flujo

```
User Prompt
  → route.py (determinista, <50ms)
    → top 3 skills con score
  → AGENTS.md rule: MUST use skill tool if score > threshold
  → skill tool loads SKILL.md
  → agent follows SKILL.md
```

## Ejemplo

Prompt: "audita y publica este repo"

- route.py:
  9.5 verify-repo -> skills/verify-repo/SKILL.md
  8.8 operate-release -> skills/operate-release/SKILL.md
  7.1 operate-lifecycle -> skills/operate-lifecycle/SKILL.md
- Agente OpenCode ejecuta verify-repo Fase 1..8, Fase 8 hace handoff a operate-release

## Añadir triggers

Edita `intent-map.yaml` y `metadata.keywords` en SKILL.md, luego rebuild:

```bash
python tools/skill-router/build_index.py
```

## Validación

```bash
python tools/skill-router/route.py --interactive
prompt> por donde empiezo con este repo
8.90 operate-lifecycle -> skills/operate-lifecycle/SKILL.md
```

## Vendor-neutral

Este router no usa APIs externas, funciona offline y sin dependencias de un único vendor.
