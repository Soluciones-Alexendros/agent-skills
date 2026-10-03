# agent-skills

19 skills para agentes de codificación, mantenidas por Soluciones-Alexendros bajo licencia MIT.

## Quick start

```bash
git clone https://github.com/Soluciones-Alexendros/agent-skills.git
cp -r agent-skills/skills/<nombre> ~/.claude/skills/
```

## Skills por familia

| Familia     | Skill                  | Qué hace                                          |
| ----------- | ---------------------- | ------------------------------------------------- |
| `disenar`   | disenar-arquitectura   | Análisis de arquitectura de codebase              |
|             | disenar-constitucion   | Constitución y memoria del agente                 |
|             | disenar-design-system  | Sistema de diseño                                 |
|             | disenar-interfaz       | Diseño visual de interfaces                       |
| `construir` | construir-typescript   | Tipos avanzados de TypeScript                     |
|             | construir-upstash      | Ecosistema serverless Upstash                     |
|             | construir-proton-suite | Correo Proton Mail y secretos Proton Pass         |
| `verificar` | verificar-compliance   | Auditoría compliance web (A11y, legal, SEO/SEM)   |
|             | verificar-performance  | Auditoría performance y calidad técnica web       |
|             | verificar-owasp        | Revisión de seguridad de código (OWASP)           |
|             | verificar-dependencias | Auditoría SCA/CVE de dependencias                 |
|             | verificar-fullaudit    | Orquestador de auditoría web completa             |
|             | verificar-repo         | Health check e inicio de plan (tablero de estado) |
|             | verificar-hooks        | Hooks pre-commit con Husky                        |
| `operar`    | operar-release         | Cierre, publicación y cierre de trabajo post-plan |
|             | operar-lifecycle       | Enrutador audit/hooks/release/cierre de trabajo   |
|             | operar-mantenimiento   | Higiene y mantenimiento del sistema Linux         |
|             | operar-salud-sistema   | Diagnóstico y health-check de sistemas Linux      |
|             | operar-seguridad       | Seguridad defensiva de Linux                      |

## Estructura del repo

```text
agent-skills/
├── skills/<nombre>/SKILL.md   # arranque + references/, scripts/
├── tools/validate/            # spec, enlaces, coherencia de release, higiene
├── tools/version/             # bump.py (skills) y cut_tag.py (repo)
├── docs/                      # STANDARD, USAGE, TAXONOMY, CONTRIBUTING
├── .github/workflows/         # CI: validate, quality, version, release
└── run-validation.sh          # validación local agregada
```

## Validación

```bash
pip install -r requirements-dev.txt
bash run-validation.sh        # spec + enlaces + coherencia + higiene + pytest + smoke + bash -n
```

En CI se ejecutan los flujos `validate`, `quality`, `version` y `release`.

## Versionado

Dos ejes:

- **Skill:** `metadata.version` en cada `SKILL.md`. `tools/version/bump.py` incrementa según magnitud: `major`, `minor`, `patch` (alias ES: `mayor`, `menor`, `parche`). CI ejecuta `bump.py --check` en las skills tocadas.
- **Repo:** `package.json` + tag anotado `vX.Y.Z` + sección del changelog. `tools/version/cut_tag.py` corta el tag cuando el manifiesto está por delante del último tag y hay notas. El workflow de `main` publica la GitHub Release con esas notas.

## Contribuir

Ver [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md).

- Nombres en kebab-case, descriptivos y sin guiones bajos.
- Toda skill cumple [docs/STANDARD.md](docs/STANDARD.md) (frontmatter, estructura, tests).
- Bump de `metadata.version` obligatorio antes de mergear un cambio de instrucciones.

## Licencia

MIT — ver [LICENSE](LICENSE).
