---
name: build-design-system
description:
  "Build design systems with tokens (Style Dictionary, Figma Tokens/Tokens Studio), Tailwind v4 and reusable UI components. Use when creating a design system, tokens or a UI component library. Not for pinpoint aesthetic direction of a screen (→ build-interface) or a11y/SEO audit (→ verify-compliance).

  "
license: MIT
metadata:
  author: Soluciones-Alexendros (adapted)
  version: 3.0.0
  domain: build
  type: atomic
  language: en
  keywords: build-design-system
compatibility: opencode, codex, cursor, copilot
allowed-tools: Read, Grep, Glob, Bash, Write
---

# Web Design System (tokens + Tailwind + components)

## Overview

Build or evolve a reusable design system: `DESIGN.md` as schema, DTCG tokens, Tailwind v4 configuration and component library.

## When to Use

Create design system, component library or tokens; unify Tailwind v4 with typography, color and spacing; sync Figma tokens ↔ code (Tokens Studio, Style Dictionary).

## Procedure

1. Clarify brand, audience and surfaces (web/app).
2. Write or update `DESIGN.md` (semantic tokens, typography, spacing, motion, dark mode).
3. Define DTCG tokens (`tokens.json`) and Style Dictionary pipeline → `tokens.css` / `tokens.ts`.
4. Map tokens to Tailwind v4 (`@theme` / CSS variables, `@tailwindcss/vite`, Oxc).
5. Define base components (Button, Input, Card, Dialog…) with variants and states.
6. Document usage and anti-patterns. Verify WCAG AA contrast in color tokens.

Read only the reference for the current phase.

## References

- `references/builder-source.md` — design system tree generation.
- `references/tailwind-source.md` — Tailwind v4 patterns and scaling.
- `references/tokens.md` — Style Dictionary, Figma Tokens/Tokens Studio, design-tokens CLI, DTCG format.
- `references/modern-css.md` — Tailwind v4 + Oxc + `@tailwindcss/vite`, Container Queries, CSS Layers, Anchor Positioning.
- Pinpoint aesthetic direction → `build-interface`. a11y/SEO audit → `verify-compliance`.
