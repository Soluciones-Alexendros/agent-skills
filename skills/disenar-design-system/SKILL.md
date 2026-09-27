---
name: disenar-design-system
description: >-
  Construye design systems con tokens (Style Dictionary, Figma Tokens/Tokens Studio),
  Tailwind v4 y componentes reutilizables (DESIGN.md, librería de UI). Usar al crear
  design system, tokens o librería de componentes. No usar para dirección estética
  puntual de una pantalla (→ disenar-interfaz) ni auditoría a11y (→ verificar-compliance).
license: MIT
metadata:
  author: Soluciones-Alexendros
  version: "1.0.0"
  dominio: disenar
  idioma: es

---

# Web Design System (tokens + Tailwind + componentes)

## Propósito

Construir o evolucionar un design system reutilizable: `DESIGN.md` _(ejemplo: artefacto generado)_ como schema, tokens DTCG, configuración Tailwind v4 y librería de componentes. Distinto de la dirección estética de una pantalla (`disenar-interfaz`).

## Cuándo usar

- Crear design system, librería de componentes o tokens.
- Unificar Tailwind v4 + tipografía/color/spacing.
- Generar árbol de archivos y convenciones de componentes (estilo shadcn).
- Sincronizar tokens Figma ↔ código (Tokens Studio, Style Dictionary).

No usar para rediseño visual puntual (→ `disenar-interfaz`) ni auditoría a11y/SEO (→ `verificar-compliance`).

## Workflow

1. Clarificar marca, audiencia y superficies (web/app).
2. Escribir o actualizar `DESIGN.md` _(ejemplo: artefacto generado)_ (tokens semánticos, tipografía, spacing, motion, dark mode).
3. Definir tokens DTCG (`tokens.json`) y pipeline Style Dictionary → `tokens.css` / `tokens.ts`.
4. Mapear tokens a Tailwind v4 (`@theme` / CSS variables, `@tailwindcss/vite`, Oxc).
5. Definir componentes base (Button, Input, Card, Dialog…) con variantes y estados.
6. Documentar uso y anti-patrones. Verificar contraste WCAG AA en tokens de color.

## Recursos

- `references/builder-source.md` — guía de generación de árbol/design system.
- `references/tailwind-source.md` — patrones Tailwind v4 y escalado.
- `references/tokens.md` — Style Dictionary, Figma Tokens/Tokens Studio, design-tokens CLI, formato DTCG.
- `references/modern-css.md` — Tailwind v4 + Oxc + `@tailwindcss/vite`, Container Queries, CSS Layers, Anchor Positioning.

Leer solo la referencia relevante a la fase en curso. Preferir progressive disclosure: no cargar todo de golpe si basta una.

## Uso

Crear design system, librería de componentes o tokens; unificar Tailwind v4 + tipografía/color/spacing. No usar para rediseño puntual (ver `disenar-interfaz`) ni auditoría a11y/SEO (ver `verificar-compliance`). Ver frontmatter `description`.

## Estructura

- `SKILL.md` — workflow y criterios.
- `references/builder-source.md` — guía de generación de árbol/design system.
- `references/tailwind-source.md` — patrones Tailwind v4.
- `references/tokens.md` — tokens DTCG, Style Dictionary, Figma/Tokens Studio.
- `references/modern-css.md` — Tailwind v4 + Oxc, Container Queries, Layers, Anchor Positioning.
- Sin `scripts/` ni `configs/` propios; artefactos `DESIGN.md` / `tokens.css` / `tokens.json` son generados _(ejemplos)_, no fuentes versionadas.

## Herramientas

Sin `scripts/` propios. Referencias versionadas:

| Recurso | Propósito |
|---|---|
| `references/builder-source.md` | Generación de árbol, tokens y componentes |
| `references/tailwind-source.md` | Patrones Tailwind v4 y escalado |
| `references/tokens.md` | Pipeline de tokens DTCG ↔ Figma ↔ código |
| `references/modern-css.md` | CSS moderno (layers, queries, anchor) |

## Referencias

- Flujo en este `SKILL.md` (Workflow 1–6).
- Productos distintos: `disenar-interfaz` (dirección estética puntual), `verificar-compliance` (auditoría a11y/SEO).
