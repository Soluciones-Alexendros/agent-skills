# agent-skills

21 skills para agentes de codificación, mantenidas por Soluciones-Alexendros bajo licencia MIT.

## Quick start

```bash
git clone https://github.com/Soluciones-Alexendros/agent-skills.git
cp -r agent-skills/skills/<nombre> ~/.claude/skills/
```
## Skills por dominio

| Dominio | Skill | Qué hace |
|---|---|---|
| `alignux` | alignux-constitucion | Constitución y memoria del agente |
| | alignux-mantenimiento | Higiene y salud del sistema |
| | alignux-seguridad | Seguridad defensiva de Linux |
| `codigo` | codigo-arquitectura | Análisis y refactor de código |
| | codigo-seguridad | Revisión de vulnerabilidades |
| | dependency-audit | Auditoría de dependencias |
| | typescript-avanzado | Tipos avanzados de TypeScript |
| `datos` | datos-postgres | Buenas prácticas Postgres |
| | upstash | Ecosistema serverless Upstash |
| `integraciones` | email-proton | Correo Proton Mail |
| | protonpass | Gestor de contraseñas |
| `proceso` | planificacion-archivos | Planificación persistente por archivos |
| `repo` | git-hooks | Hooks pre-commit con Husky |
| | repo-ending | Finalización de repositorio |
| | repo-starting | Arranque de repositorio |
| `web` | auditoria-360-web | Auditoría web integral |
| | design-system | Sistema de diseño |
| | playwright-e2e-audit | Auditoría E2E con Playwright |
| | web-audit | Auditoría de sitios web |
| | web-diseno | Diseño visual de interfaces |
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
