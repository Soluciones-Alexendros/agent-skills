---
name: design-system
description: >-
  Construye design systems con tokens, Tailwind v4 y componentes reutilizables (DESIGN.md,
  librería de UI). Usar al crear design system, tokens o librería de componentes. No usar
  para dirección estética puntual de una pantalla (→ web-diseno) ni auditoría a11y (→ web-compliance).
license: MIT
metadata:
  author: Soluciones-Alexendros
  version: "0.1.1"
  dominio: web
  idioma: es

---

# Design system (tokens + Tailwind + componentes)

## Propósito

Construir o evolucionar un design system reutilizable: `DESIGN.md` _(ejemplo: artefacto generado)_ como schema, tokens, configuración Tailwind v4 y librería de componentes. Distinto de la dirección estética de una pantalla (`web-diseno`).

## Cuándo usar

- Crear design system, librería de componentes o tokens.
- Unificar Tailwind v4 + tipografía/color/spacing.
- Generar árbol de archivos y convenciones de componentes (estilo shadcn).

No usar para rediseño visual puntual (→ `web-diseno`) ni auditoría a11y/SEO (→ `web-compliance`).

## Workflow

1. Clarificar marca, audiencia y superficies (web/app).
2. Escribir o actualizar `DESIGN.md` _(ejemplo: artefacto generado)_ (tokens semánticos, tipografía, spacing, motion, dark mode).
3. Mapear tokens a Tailwind v4 (`@theme` / CSS variables).
4. Definir componentes base (Button, Input, Card, Dialog…) con variantes y estados.
5. Documentar uso y anti-patrones. Verificar contraste WCAG AA en tokens de color.

## Recursos

- `references/builder-source.md` — guía de generación de árbol/design system.
- `references/tailwind-source.md` — patrones Tailwind v4 y escalado.

Leer solo la referencia relevante a la fase en curso. Preferir progressive disclosure: no cargar ambas de golpe si basta una.

## Uso

Crear design system, librería de componentes o tokens; unificar Tailwind v4 + tipografía/color/spacing. No usar para rediseño puntual (ver `web-diseno`) ni auditoría a11y/SEO (ver `web-compliance`). Ver frontmatter `description`.

## Estructura

- `SKILL.md` — workflow y criterios.
- `references/builder-source.md` — guía de generación de árbol/design system.
- `references/tailwind-source.md` — patrones Tailwind v4 (deduplicado 2026-09-26: 5 bloques en una copia canónica).
- Sin `scripts/` ni `configs/` propios; artefactos `DESIGN.md` / `tokens.css` son generados _(ejemplos)_, no fuentes versionadas.

## Herramientas

Sin `scripts/` propios. Referencias versionadas:

| Recurso | Propósito |
|---|---|
| `references/builder-source.md` | Generación de árbol, tokens y componentes |
| `references/tailwind-source.md` | Patrones Tailwind v4 y escalado |

## Referencias

- Flujo en este `SKILL.md` (Workflow 1–5).
- Productos distintos: `web-diseno` (dirección estética puntual), `web-compliance` (auditoría a11y/SEO).
