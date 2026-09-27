# Contribuir

## Añadir o modificar una skill

1. La carpeta debe llamarse igual que el `name` del frontmatter (kebab-case).
2. El frontmatter debe declarar `metadata.idioma: es` — toda skill se escribe en español.
3. Cumplir [STANDARD.md](STANDARD.md): frontmatter completo, cuerpo < 500 líneas, taxonomía en [TAXONOMY.md](TAXONOMY.md).
4. Sin trailing whitespace — la CI lo rechaza.
5. Registrar cambios en [CHANGELOG.md](../CHANGELOG.md).
6. Pasar la validación local en verde antes de la PR:

```bash
bash run-validation.sh
```

## Niveles de severidad (bump de `metadata.version`)

| Tipo | Cuándo usar | Ejemplo |
|------|-------------|---------|
| `major` | Cambio incompatible: reestructura, elimina secciones o cambia comportamiento | Fusionar dos skills, cambiar formato de frontmatter |
| `minor` | Nueva funcionalidad compatible: añade secciones, referencias o scripts | Añadir `references/nueva-guia.md` |
| `patch` | Fix compatible: typo, enlace roto, ajuste menor | Corregir URL, formatear tabla |

En español: `--type ruptura` (major), `--type desarrollo` (minor), `--type parche` (patch).

## Smoke tests

Cada skill con scripts debe incluir un `smoke_sh.sh` en su raíz. Este script ejecuta sus herramientas con datos sintéticos y verifica que producen salida esperada. La CI lo ejecuta automáticamente.

```bash
bash skills/<skill>/smoke_sh.sh
```

## PRs

- Describir qué skill cambia y por qué; bump de `metadata.version` si cambian instrucciones (autoversionado: `python3 tools/version/bump.py --auto --type <major|minor|patch>`; la CI lo exige en `version.yml`).
- La CI ejecuta `validate.yml` (spec + enlaces + tests), `version.yml` (bump exigido) y `quality.yml` (higiene). Todos deben estar en verde.
- No commitear residuos (`__pycache__/`, `.pytest_cache/`, `.log`, `.tmp`): están en `.gitignore` y la CI los rechaza.
- Usar la plantilla de PR: [`.github/pull_request_template.md`](../.github/pull_request_template.md).

## Issues

Usar las plantillas de `.github/ISSUE_TEMPLATE/` (bug o propuesta de skill/mejora).

## Planificación de tareas

Para proyectos multi-paso o tareas de investigación, mantener `task_plan.md`, `findings.md` y `progress.md` en disco.
