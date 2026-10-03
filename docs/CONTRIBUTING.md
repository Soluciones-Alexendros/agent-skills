# Contribuir

## Añadir o modificar una skill

1. La carpeta debe llamarse igual que el `name` del frontmatter (kebab-case).
2. El frontmatter debe declarar `metadata.idioma: es` y `metadata.tipo: atomic|router|tecnologia` — toda skill se escribe en español.
3. Cumplir [STANDARD.md](STANDARD.md): frontmatter completo (incluye `tipo`), cuerpo ≤ 500 líneas y ≤ 5000 tokens, taxonomía en [TAXONOMY.md](TAXONOMY.md), encabezados canónicos.
4. Sin trailing whitespace — la CI lo rechaza.
5. Registrar cambios en [CHANGELOG.md](../CHANGELOG.md).
6. Pasar la validación local en verde antes de la PR:

```bash
pip install -r requirements-dev.txt
bash run-validation.sh
```

## Niveles de severidad (bump de `metadata.version`)

| Tipo    | Cuándo usar                                                                  | Ejemplo                                             |
| ------- | ---------------------------------------------------------------------------- | --------------------------------------------------- |
| `major` | Cambio incompatible: reestructura, elimina secciones o cambia comportamiento | Fusionar dos skills, cambiar formato de frontmatter |
| `minor` | Nueva funcionalidad compatible: añade secciones, referencias o scripts       | Añadir `references/nueva-guia.md`                   |
| `patch` | Fix compatible: typo, enlace roto, ajuste menor                              | Corregir URL, formatear tabla                       |

En español: `--type ruptura` (major), `--type desarrollo` (minor), `--type parche` (patch).

La versión del **repo** (`package.json`) se sube al publicar. Un cambio en `CHANGELOG.md` de sección publicada, en `.github/workflows/release.yml` o en `tools/version/cut_tag.py` exige que `package.json` quede por delante del último tag.

## Smoke tests

Cada skill con ejecutables `.py` o `.sh` fuera de `tests/` incluye `scripts/tests/smoke_sh.sh`. Ese script ejecuta las herramientas con datos sintéticos y comprueba la salida. La CI lo lanza sola.

```bash
bash skills/<skill>/scripts/tests/smoke_sh.sh
```

## PRs

- Describir qué skill cambia y por qué; bump de `metadata.version` si cambian instrucciones (`python3 tools/version/bump.py --auto --type <major|minor|patch>`; la CI lo exige en `version.yml`).
- La CI ejecuta `validate.yml` (spec, enlaces, coherencia, tests), `version.yml` (bump exigido) y `quality.yml` (higiene). Todos deben estar en verde.
- No commitear residuos (`__pycache__/`, `.pytest_cache/`, `.log`, `.tmp`): están en `.gitignore` y la CI los rechaza si git los rastrea.
- Usar la plantilla de PR: [`.github/pull_request_template.md`](../.github/pull_request_template.md).

## Issues

Usar las plantillas de `.github/ISSUE_TEMPLATE/` (bug o propuesta de skill/mejora).

## Planificación de tareas

Para proyectos multi-paso o tareas de investigación, mantener `task_plan.md`, `findings.md` y `progress.md` en disco.
