# Checklist de readiness — gate de cierre

Recorre cada ítem y registra `OK`, `WARN`, `BLOCK` o `N/A`.

- `BLOCK` impide el cierre.
- `WARN` no impide el cierre. Exige una justificación en el informe. En un repo crítico (público con consumidores, despliegue a producción, o criticidad declarada por el usuario) un `WARN` de la columna «crítico» pasa a `BLOCK`.
- `N/A` exige el motivo. No uses `N/A` para tapar un `BLOCK`.

| Ítem                                                                        | Severidad | Cuándo bloquea                                                                          |
| --------------------------------------------------------------------------- | --------- | --------------------------------------------------------------------------------------- |
| Secreto en árbol o historial señalado por el escaneo                        | BLOCK     | Siempre                                                                                 |
| `uses:` de terceros sin SHA completo verificado                             | BLOCK     | Siempre. En repo crítico, también `actions/*` y `github/*`                              |
| Workflow sin `permissions:` explícito                                       | BLOCK     | Siempre                                                                                 |
| Job sin `timeout-minutes`                                                   | BLOCK     | Siempre                                                                                 |
| Entrada no confiable interpolada en `run:` o `github-script`                | BLOCK     | Siempre                                                                                 |
| `pull_request_target` o `workflow_run` con checkout de código no confiable  | BLOCK     | Siempre                                                                                 |
| Tag, CHANGELOG y manifiesto de versión coherentes                           | BLOCK     | Solo si se publica                                                                      |
| Breaking sin marcar, o número yanked reutilizado                            | BLOCK     | Solo si se publica                                                                      |
| Labels en taxonomía por ejes, sin duplicados                                | WARN      | Repo crítico                                                                            |
| Issues y PRs abiertos mapeados; labels por defecto no listados se conservan | WARN      | Repo crítico                                                                            |
| Lockfile presente; actualizaciones agrupadas por riesgo                     | WARN      | Repo crítico, o `BLOCK` si el escaneo de dependencias está en rojo y el repo es crítico |
| Runtime fuera de soporte sin plan                                           | BLOCK     | Siempre, si el calendario oficial confirma EOL                                          |
| README con instalación reproducible, badges que responden y licencia        | WARN      | Repo crítico                                                                            |
| CONTRIBUTING, CODEOWNERS de `.github/workflows/`, SECURITY.md               | WARN      | Repo crítico. `SECURITY.md` pasa a `BLOCK` si el repo es público                        |
| actionlint verde                                                            | BLOCK     | Siempre que existan workflows                                                           |
| Última ejecución de cada workflow revisada, sin fallos tapados              | WARN      | Repo crítico                                                                            |
| Required checks de lint, tests y build en verde                             | BLOCK     | Siempre que el repo tenga CI                                                            |
| CodeQL, dependency review, rulesets                                         | WARN      | Repo crítico                                                                            |
| Estrategia de despliegue y rollback                                         | N/A       | `BLOCK` solo si el repo despliega y no hay rollback                                     |
| Attestations o SLSA                                                         | WARN      | Repo crítico, o si el usuario las pidió                                                 |
| PR de remediación mergeado con required checks verdes (Fase F)              | BLOCK     | Solo si hubo remediación: no cerrar con PR abierto o checks en rojo                     |

## Plantilla — Informe de readiness

```markdown
# Readiness report — <owner>/<repo> — <fecha>

**Veredicto:** READY FOR RELEASE vX.Y.Z | BLOCKED | AUDIT ONLY

**Modo:** auditoría | publicación
**Repo crítico:** sí | no — motivo

## Resumen de release

- Versión: vX.Y.Z (esquema, bump y justificación)
- Tag anotado: vX.Y.Z @ <sha corto> — o no creado
- Changelog: sección promovida desde [Unreleased], o sin cambios

## Estado por fase

| Fase                   | Estado | Notas |
| ---------------------- | ------ | ----- |
| A. Etiquetado          | OK     |       |
| B. Versionado          | OK     |       |
| C. Dependencias y docs | OK     |       |
| D. Pipeline            | OK     |       |
| E. Producción          | OK     |       |

## Bloqueos

1. **[SEV-1]** <bloqueo> — remediación: <acción concreta>

## Avisos

- WARN <aviso> — por qué no bloquea

## [PENDIENTE]

- <dato> — se pide al usuario
```
