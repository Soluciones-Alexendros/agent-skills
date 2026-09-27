# agent-skills

18 skills para agentes de codificación, mantenidas por Soluciones-Alexendros bajo licencia MIT.

## Quick start

```bash
git clone https://github.com/Soluciones-Alexendros/agent-skills.git
cp -r agent-skills/skills/<nombre> ~/.claude/skills/
```

## Skills por dominio

| Dominio | Skill | Qué hace |
|---|---|---|
| `alignux` | alignux-constitucion | Constitución y memoria del agente |
| `codigo` | codigo-arquitectura | Análisis y refactor de código |
| | typescript-avanzado | Tipos avanzados de TypeScript |
| `datos` | upstash | Ecosistema serverless Upstash |
| `integraciones` | email-proton | Correo Proton Mail (thin-skill → protonsuite-tools) |
| | protonpass | Secretos Proton Pass (thin-skill → protonsuite-tools) |
| `linux` | linux-mantenimiento | Higiene y salud del sistema Linux |
| | linux-seguridad | Seguridad defensiva de Linux |
| `repo` | repo-ending | Finalización de repositorio |
| | repo-precommit | Hooks pre-commit con Husky |
| | repo-starting | Arranque de repositorio |
| `web` | design-system | Sistema de diseño |
| | web-compliance | Auditoría compliance web (A11y, legal, SEO/SEM) |
| | web-diseno | Diseño visual de interfaces |
| | web-playwright | Auditoría E2E con Playwright |
| | web-rendimiento | Auditoría performance y calidad técnica web |
| | web-seguridad | Revisión seguridad código y dependencias (OWASP) |
| | webapp-testing | Pruebas de aplicaciones web |

## Estructura del repo

```text
agent-skills/
├── skills/<nombre>/SKILL.md   # arranque + references/, scripts/
├── tools/validate/            # validadores de spec y enlaces
├── tools/version/             # bump.py — versionado semver
├── docs/                      # STANDARD, USAGE, TAXONOMY, CONTRIBUTING
├── .github/workflows/         # CI: validate, quality, release
└── run-validation.sh          # validación local agregada
```

## Validación

```bash
bash run-validation.sh        # spec + enlaces + pytest + smoke + bash -n
```

En CI se ejecutan los flujos `validate`, `quality`, `version` y `release`.

## Versionado

`tools/version/bump.py` incrementa la versión según la magnitud: `major` (rompe compatibilidad), `minor` (nueva skill o funcionalidad) y `patch` (correcciones). Alias en español: `mayor`, `menor`, `parche`. CI ejecuta `bump.py --check` para verificar que la versión esté actualizada.

## Contribuir

Ver [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md).
- Nombres en kebab-case, descriptivos y sin guiones bajos.
- Toda skill cumple `docs/STANDARD.md` (frontmatter, estructura, tests).
- Bump de versión obligatorio antes de mergear.

## Licencia

MIT — ver [LICENSE](LICENSE).