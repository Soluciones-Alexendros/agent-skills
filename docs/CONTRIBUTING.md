# Contribuir

## Añadir o modificar una skill

1. La carpeta debe llamarse igual que el `name` del frontmatter (kebab-case).
2. Cumplir [STANDARD.md](STANDARD.md): frontmatter completo, cuerpo < 500 líneas, taxonomía en [TAXONOMY.md](TAXONOMY.md).
3. Registrar cambios en [CHANGELOG.md](../CHANGELOG.md).
4. Pasar la validación local en verde antes de la PR:

```bash
bash run-validation.sh
```

## PRs

- Describir qué skill cambia y por qué; bump de `metadata.version` si cambian instrucciones.
- La CI ejecuta `validate.yml` (spec + enlaces + tests) y `quality.yml` (higiene). Ambos deben estar en verde.
- No commitear residuos (`__pycache__/`, `.pytest_cache/`, `.log`, `.tmp`): están en `.gitignore` y la CI los rechaza.

## Issues

Usar las plantillas de `.github/ISSUE_TEMPLATE/` (bug o propuesta de skill/mejora).
