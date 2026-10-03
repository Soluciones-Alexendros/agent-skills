---
name: disenar-design-system
description: >-
  Construye design systems con tokens (Style Dictionary, Figma Tokens/Tokens Studio),
  Tailwind v4 y componentes reutilizables (DESIGN.md, librería de UI). Usar cuando
  el operador pida crear un design system, tokens o librería de componentes. No
  usar para dirección estética puntual de una pantalla (→ disenar-interfaz) ni
  auditoría a11y (→ verificar-compliance).
license: MIT
metadata:
  author: Soluciones-Alexendros
  version: "1.1.1"
  dominio: disenar
  tipo: atomic
  idioma: es
---

# Web Design System (tokens + Tailwind + componentes)

## Propósito

Construir o evolucionar un design system reutilizable: `DESIGN.md` como schema, tokens DTCG, configuración Tailwind v4 y librería de componentes.

## Cuándo usar

Crear design system, librería de componentes o tokens; unificar Tailwind v4 con tipografía, color y spacing; sincronizar tokens Figma ↔ código (Tokens Studio, Style Dictionary).

## Procedimiento

1. Clarificar marca, audiencia y superficies (web/app).
2. Escribir o actualizar `DESIGN.md` (tokens semánticos, tipografía, spacing, motion, dark mode).
3. Definir tokens DTCG (`tokens.json`) y pipeline Style Dictionary → `tokens.css` / `tokens.ts`.
4. Mapear tokens a Tailwind v4 (`@theme` / CSS variables, `@tailwindcss/vite`, Oxc).
5. Definir componentes base (Button, Input, Card, Dialog…) con variantes y estados.
6. Documentar uso y anti-patrones. Verificar contraste WCAG AA en tokens de color.

Leer solo la referencia de la fase en curso.

## Referencias

- `references/builder-source.md` — generación de árbol/design system.
- `references/tailwind-source.md` — patrones Tailwind v4 y escalado.
- `references/tokens.md` — Style Dictionary, Figma Tokens/Tokens Studio, design-tokens CLI, formato DTCG.
- `references/modern-css.md` — Tailwind v4 + Oxc + `@tailwindcss/vite`, Container Queries, CSS Layers, Anchor Positioning.
- Dirección estética puntual → `disenar-interfaz`. Auditoría a11y/SEO → `verificar-compliance`.
