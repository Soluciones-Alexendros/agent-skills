---
name: operar-lifecycle
description: >-
  Enruta el ciclo de vida del repositorio: deriva a verificar-repo (diagnóstico y
  health check), verificar-hooks (hooks locales Husky/lint-staged) o operar-release
  (cierre y publicación). Usar ante "¿por dónde empiezo con este repo?" o
  peticiones que mezclan auditar, hooks y release. No ejecuta auditorías,
  hooks ni releases: solo decide y deriva.
license: MIT
metadata:
  author: Soluciones-Alexendros
  version: "1.0.0"
  dominio: operar
  idioma: es

---

# operar-lifecycle — Enrutador del ciclo de vida del repo

## Propósito

Thin-router opcional: ante una petición ambigua del ciclo de vida, decidir qué skill la atiende y derivar. No diagnostica, no configura hooks, no publica: delega.

Canon vigente: [docs/repo-standard](../../docs/repo-standard/structure.md) (`structure.md`, `ci-cd.md`, `release.md`, `security.md`, `templates/`).

## Reglas

1. **Una petición, una skill**: si la petición mezcla fases, ordenarlas (auditar → hooks → release) y ejecutarlas en secuencia, una cada vez.
2. **No duplicar el health check**: vive en `verificar-repo`. `operar-release` lo consume vía Fase 8, no lo repite.
3. **No absorber lógica**: el procedimiento vive en la skill destino; aquí solo el criterio de enrutado.
4. **Derivar con contexto**: al derivar a `operar-release`, pasar perfil, informe y checklist §8 (formato de la Fase 8 de `verificar-repo`).

## Enrutado

| Petición | Destino |
|---|---|
| Escanear, auditar, alinear con el estándar, «pon al día este proyecto», health check | `verificar-repo` |
| Pre-commit hooks, Husky, lint-staged, Prettier local | `verificar-hooks` |
| Cerrar el repo, preparar release, publicar versión, auditoría de CI/CD, labels, changelog, seguridad de workflows | `operar-release` |
| Mezcla («audítalo y publícalo») | `verificar-repo` primero; su Fase 8 deriva a `operar-release` |

## Uso

Usar ante «¿por dónde empiezo con este repo?» o peticiones que mezclan auditar, hooks y release. No usar para ejecutar directamente una auditoría, unos hooks o un cierre (ir a la skill destino).

## Estructura

- `SKILL.md` — criterio de enrutado (este fichero). Sin `references/`, `scripts/` ni `assets/` propios.

## Herramientas

Sin scripts ni herramientas propias. Delega en `verificar-repo`, `verificar-hooks` y `operar-release`.

## Referencias

- `verificar-repo` — diagnóstico, health check y Fase 8 de handoff.
- `verificar-hooks` — hooks locales.
- `operar-release` — cierre y publicación.
- Canon: [structure.md](../../docs/repo-standard/structure.md), [ci-cd.md](../../docs/repo-standard/ci-cd.md), [release.md](../../docs/repo-standard/release.md), [security.md](../../docs/repo-standard/security.md).
