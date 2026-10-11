# Harness Integration — OpenCode-first (multi-harness)

| Harness      | Skill Path                                                        | Auto-invoke                   | Instalación                        |
| ------------ | ----------------------------------------------------------------- | ----------------------------- | ---------------------------------- |
| **OpenCode** | `~/.config/opencode/skills/<name>/SKILL.md` + `.opencode/skills/` | Sí vía AGENTS.md + skill tool | `bash scripts/install-opencode.sh` |
| **Cursor**   | `~/.cursor/skills/<name>/SKILL.md` + `~/.cursor/AGENTS.md`        | Sí                            | `bash scripts/install.sh`          |
| **Grok CLI** | `~/.grok/skills/<name>/SKILL.md` + `~/.grok/AGENTS.md`            | Sí + `/skill-route`           | `bash scripts/install.sh`          |
| Codex CLI    | `~/.codex/skills/<name>/SKILL.md`                                 | Sí                            | `bash scripts/install.sh`          |
| Copilot      | `.github/skills/<name>/SKILL.md`                                  | Sí (preview)                  | copy                               |
| Generic      | `./skills/<name>/SKILL.md`                                        | vía AGENTS.md                 | git clone                          |

## Instalación global (Cursor + Grok + OpenCode + Codex)

Desde la raíz del repo:

```bash
bash scripts/install.sh
# opcional: archivar skills obsoletas que no sean del catálogo canónico
bash scripts/install.sh --prune
```

Enlaza las 18 skills canónicas a:

- `~/.cursor/skills/` y copia `~/.cursor/AGENTS.md` + docs de taxonomía/routing
- `~/.grok/skills/`, `~/.grok/AGENTS.md` y comando `/skill-route`
- `~/.agents/skills/`, `~/.codex/skills/`, `~/.config/opencode/skills/`

Grok ya puede apuntar al árbol con `[skills].paths` en `~/.grok/config.toml`. Verifica:

```bash
grok inspect | grep -E 'plan-|system-|project-|web-|role-'
python tools/skill-router/route.py "limpia mi sistema Arch" --top 3
```

En Grok CLI: `/skill-route limpia mi Arch` o invoca la skill por nombre (`/user:system-maintenance`).

## Instalación proyecto (OpenCode local)

```bash
bash scripts/install-opencode.sh
```

## OpenCode es el harness primario del repo

- No depende de plugin system, solo de `AGENTS.md` + `opencode.json`
- Descubrimiento: `skillDirectories` en opencode.json
- Invocación: agente evalúa cada request, mapea a skill por description+keywords
