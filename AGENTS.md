# Soluciones-Alexendros Agent Skills — Routing Contract

## Discovery

All skills live in `skills/<skill-name>/SKILL.md`. Flat layout, one folder per skill. Name == directory name.

## Mandatory Rule — OpenCode & Code Harness

Before ANY action, you MUST evaluate if a skill in `skills/` applies.

- Read each SKILL.md `name` and `description` (discovery phase)
- If user intent matches `description` or `metadata.keywords` or `triggers`, you MUST invoke the `skill` tool
- Follow SKILL.md exactly, including reading its `references/` when instructed
- Never skip required workflows

## Lifecycle Enforcement

DEFINE → plan-specification
CONTINUE → plan-continue
IMPLEMENT → role-* + plan-validation
PROJECT GATES → project-*
WEB AUDITS → web-*
SYSTEM (local OS) → system-*

Ambiguous "¿por dónde empiezo?" or "pon al día este proyecto" → plan-continue
Mix audit+release ("audítalo y publícalo") → plan-continue first, then hand off to project-publish

## OpenCode Specific

OpenCode searches in this order:

- .opencode/skills/<name>/SKILL.md
- ~/.config/opencode/skills/<name>/SKILL.md
- .agents/skills/<name>/SKILL.md
- ./skills/<name>/SKILL.md (project fallback)

The agent must load `opencode.json` for skillDirectories.

## Language

Content is Spanish, frontmatter description is bilingual (EN + ES triggers) for embedding quality.

## Progressive Disclosure

SKILL.md is <200 lines. Heavy docs live in references/. Read them only when SKILL.md says so.
