---
name: verificar-fullaudit
description: >
  Router de auditoría web holística: deriva a verificar-compliance (compliance SEO/a11y/legal),
  verificar-performance (CWV/rendering), verificar-repo (health check repo) o disenar-interfaz
  (dirección visual). Usar cuando el usuario pida "auditoría completa", "auditoría holística",
  "revisa todo" o "full audit" sin especificar foco. No ejecuta auditorías: solo enruta.
license: MIT
metadata:
  author: Soluciones-Alexendros
  version: "2.1.0"
  dominio: verificar
  tipo: router
  idioma: es
---

# verificar-fullaudit — Router de auditoría web holística

## Propósito

Thin-router: ante una petición de auditoría web completa/holística sin foco específico,
decide qué skill(es) atienden y deriva. No ejecuta auditorías ni scoring: delega.

## Enrutado

| Petición del usuario                                                     | Destino(s)                                                                  |
| ------------------------------------------------------------------------ | --------------------------------------------------------------------------- |
| "Auditoría completa", "auditoría holística", "revisa todo", "full audit" | verificar-compliance → verificar-performance → (si hay repo) verificar-repo |
| "Compliance SEO/a11y/legal"                                              | verificar-compliance                                                        |
| "Performance CWV/rendering"                                              | verificar-performance                                                       |
| "QA E2E/Playwright", "tests funcionales"                                 | verificar-compliance (modo e2e si existe) o skill dedicada                  |
| "Health check repo", "audita este repo"                                  | verificar-repo                                                              |
| "Dirección visual", "rediseña interfaz"                                  | disenar-interfaz / disenar-design-system                                    |

## Reglas

1. **Una petición, una skill destino principal**: si la petición mezcla facetas, ordenar y ejecutar en secuencia.
2. **No duplicar lógica**: el procedimiento vive en la skill destino; aquí solo el criterio de enrutado.
3. **Derivar con contexto**: pasar objetivo, alcance y restricciones conocidas a la skill destino.
4. **No absorber scoring ni reporting**: viven en `verificar-compliance` y `verificar-performance`.

## Uso

Usar cuando el usuario pida "auditoría completa", "auditoría holística", "revisa todo", "full audit"
sin especificar foco (compliance, performance, e2e, repo). Ver frontmatter `description`.

## Estructura

- `SKILL.md` — criterio de enrutado (este fichero). Sin `core/`, `modes/`, `tests/` propios.

## Referencias

- `verificar-compliance` — compliance SEO/a11y/legal, scoring, dictamen, RICE.
- `verificar-performance` — CWV, rendering, caching, Lighthouse.
- `verificar-repo` — health check repo, canon repo-standard.
- `disenar-interfaz` — dirección visual, identidad visual.
- `disenar-design-system` — tokens, Tailwind, componentes.
