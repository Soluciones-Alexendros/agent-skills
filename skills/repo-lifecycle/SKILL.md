---
name: repo-lifecycle
description: >-
  Enruta el ciclo de vida del repositorio: deriva a repo-audit (diagnóstico y
  health check), repo-hooks (hooks locales Husky/lint-staged) o repo-release
  (cierre y publicación). Usar ante "¿por dónde empiezo con este repo?" o
  peticiones que mezclan auditar, hooks y release. No ejecuta auditorías,
  hooks ni releases: solo decide y deriva.
license: MIT
metadata:
  author: Soluciones-Alexendros
  version: "0.1.0"
  dominio: repo
  idioma: es

---

# repo-lifecycle — Enrutador del ciclo de vida del repo

## Propósito

Thin-router opcional: ante una petición ambigua del ciclo de vida, decidir qué skill `repo-*` la atiende y derivar. No diagnostica, no configura hooks, no publica: delega.

Canon vigente: [docs/repo-standard](../../docs/repo-standard/structure.md) (`structure.md`, `ci-cd.md`, `release.md`, `security.md`, `templates/`).

## Reglas

1. **Una petición, una skill**: si la petición mezcla fases, ordenarlas (auditar → hooks → release) y ejecutarlas en secuencia, una cada vez.
2. **No duplicar el health check**: vive en `repo-audit`. `repo-release` lo consume vía Fase 8, no lo repite.
3. **No absorber lógica**: el procedimiento vive en la skill destino; aquí solo el criterio de enrutado.
4. **Derivar con contexto**: al derivar a `repo-release`, pasar perfil, informe y checklist §8 (formato de la Fase 8 de `repo-audit`).

## Enrutado

| Petición | Destino |
|---|---|
| Escanear, auditar, alinear con el estándar, «pon al día este proyecto», health check | `repo-audit` |
| Pre-commit hooks, Husky, lint-staged, Prettier local | `repo-hooks` |
| Cerrar el repo, preparar release, publicar versión, auditoría de CI/CD, labels, changelog, seguridad de workflows | `repo-release` |
| Mezcla («audítalo y publícalo») | `repo-audit` primero; su Fase 8 deriva a `repo-release` |

## Uso

Usar ante «¿por dónde empiezo con este repo?» o peticiones que mezclan auditar, hooks y release. No usar para ejecutar directamente una auditoría, unos hooks o un cierre (ir a la skill destino).

## Estructura

- `SKILL.md` — criterio de enrutado (este fichero). Sin `references/`, `scripts/` ni `assets/` propios.

## Herramientas

Sin scripts ni herramientas propias. Delega en `repo-audit`, `repo-hooks` y `repo-release`.

## Referencias

- `repo-audit` — diagnóstico, health check y Fase 8 de handoff.
- `repo-hooks` — hooks locales.
- `repo-release` — cierre y publicación.
- Canon: [structure.md](../../docs/repo-standard/structure.md), [ci-cd.md](../../docs/repo-standard/ci-cd.md), [release.md](../../docs/repo-standard/release.md), [security.md](../../docs/repo-standard/security.md).
