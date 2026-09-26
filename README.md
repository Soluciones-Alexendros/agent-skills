# agent-skills

Colección de 21 **skills** para agentes de codificación (Claude Code, OpenAI Codex, agentes compatibles con [Agent Skills](https://agentskills.io/specification)), mantenida por **Soluciones-Alexendros** bajo licencia MIT.

Cada skill vive en `skills/<nombre>/` con un `SKILL.md` de arranque más `references/`, `scripts/` y recursos opcionales. Ver [docs/TAXONOMY.md](docs/TAXONOMY.md), [docs/STANDARD.md](docs/STANDARD.md) y [docs/USAGE.md](docs/USAGE.md).

## Skills por dominio

| Dominio | Skills |
|---|---|
| `alignux` | alignux-constitucion · alignux-mantenimiento · alignux-seguridad |
| `codigo` | codigo-arquitectura · codigo-seguridad · dependency-audit · typescript-avanzado |
| `datos` | datos-postgres · upstash |
| `integraciones` | email-proton · protonpass |
| `proceso` | planificacion-archivos |
| `repo` | git-hooks · repo-ending · repo-starting |
| `web` | auditoria-360-web · design-system · playwright-e2e-audit · web-audit · web-diseno · webapp-testing |

## Uso rápido

```bash
# Clonar
git clone https://github.com/Soluciones-Alexendros/agent-skills.git

# Claude Code: copiar o enlazar la skill deseada
cp -r agent-skills/skills/codigo-seguridad ~/.claude/skills/
```

Detalle en [docs/USAGE.md](docs/USAGE.md).

## Estructura

```text
agent-skills/
├── skills/<nombre>/SKILL.md   # arranque de cada skill (+ references/, scripts/, ...)
├── tools/validate/            # validadores de spec y enlaces
├── docs/                      # STANDARD, USAGE, TAXONOMY, CONTRIBUTING
├── .github/workflows/         # CI: validate, quality, release
└── run-validation.sh          # validación local agregada
```

## Validación

```bash
bash run-validation.sh        # todo: spec + enlaces + pytest + smoke + bash -n
bash run-validation.sh --spec-only
```

## Contribuir

Ver [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md). Toda skill debe pasar `run-validation.sh` en verde.

## Licencia

MIT — ver [LICENSE](LICENSE). Cada `SKILL.md` declara `license: MIT` en su frontmatter.
