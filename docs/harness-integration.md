# Harness Integration — OpenCode-first (multi-harness)

| Harness      | Skill Path                                                        | Auto-invoke                   | Instalación                        |
| ------------ | ----------------------------------------------------------------- | ----------------------------- | ---------------------------------- |
| **OpenCode** | `~/.config/opencode/skills/<name>/SKILL.md` + `.opencode/skills/` | Sí vía AGENTS.md + skill tool | `bash scripts/install-opencode.sh` |
| Codex CLI    | `~/.codex/skills/<name>/SKILL.md`                                 | Sí                            | `bash scripts/install.sh`          |
| Cursor       | `~/.cursor/skills/<name>/SKILL.md`                                | Sí                            | `bash scripts/install.sh`          |
| Copilot      | `.github/skills/<name>/SKILL.md`                                  | Sí (preview)                  | copy                               |
| Generic      | `./skills/<name>/SKILL.md`                                        | vía AGENTS.md                 | git clone                          |

## OpenCode es el harness primario

- No depende de plugin system, solo de `AGENTS.md` + `opencode.json`
- Descubrimiento: `skillDirectories` en opencode.json
- Invocación: agente evalúa cada request, mapea a skill por description+keywords

## Instalación global OpenCode

```bash
git clone https://github.com/Soluciones-Alexendros/agent-skills.git
cd agent-skills
bash scripts/install.sh
```

## Instalación proyecto

```bash
bash scripts/install-opencode.sh
```

Verifica con:

```bash
python tools/skill-router/route.py "limpia mi sistema Arch" --top 3
```
