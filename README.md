# agent-skills

17 skills para agentes de codificación, mantenidas por Soluciones-Alexendros bajo licencia MIT.

## Quick start

```bash
git clone https://github.com/Soluciones-Alexendros/agent-skills.git
cp -r agent-skills/skills/<nombre> ~/.claude/skills/
```

## Skills por familia

| Familia | Skill | Qué hace |
|---|---|---|
| `disenar` | disenar-arquitectura | Análisis de arquitectura de codebase |
| | disenar-constitucion | Constitución y memoria del agente |
| | disenar-design-system | Sistema de diseño |
| | disenar-interfaz | Diseño visual de interfaces |
| `construir` | construir-typescript | Tipos avanzados de TypeScript |
| | construir-upstash | Ecosistema serverless Upstash |
| | construir-proton-suite | Correo Proton Mail y secretos Proton Pass (thin-skill → protonsuite-tools) |
| `verificar` | verificar-compliance | Auditoría compliance web (A11y, legal, SEO/SEM) |
| | verificar-performance | Auditoría performance y calidad técnica web |
| | verificar-owasp | Revisión seguridad código y dependencias (OWASP) |
| | verificar-fullaudit | Orquestador de auditoría web completa |
| | verificar-repo | Auditoría y health check de repositorio |
| | verificar-hooks | Hooks pre-commit con Husky |
| `operar` | operar-release | Cierre y publicación de repositorio |
| | operar-lifecycle | Enrutador audit/hooks/release |
| | operar-mantenimiento | Higiene y salud del sistema Linux |
| | operar-seguridad | Seguridad defensiva de Linux |

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