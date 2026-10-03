---
name: disenar-interfaz
description: >-
  Dirección visual e interacción para UI: estética, tipografía, paleta, motion y
  microinteracciones. Usar cuando el operador pida diseñar o rediseñar interfaces,
  identidad visual o polish de interacción. No usar para design system o tokens
  formales (→ disenar-design-system) ni auditoría a11y/SEO (→ verificar-compliance).
license: MIT
metadata:
  author: Soluciones-Alexendros
  version: "1.1.1"
  dominio: disenar
  tipo: atomic
  idioma: es
---

# disenar-interfaz — Diseño visual intencional

## Propósito

Guiar el diseño visual para interfaces con identidad propia: dirección estética, sistema tipográfico, paleta, layout, motion y signature element. Cada decisión es deliberada respecto al brief.

## Cuándo usar

Nueva UI, rediseño, definición de paleta/tipografía o polish de interacción.

## Formato de salida

Plantilla:

```markdown
# [Plan de Diseño Visual]

## Brief & Sujeto concreto

## Token system (Color, Type, Layout, Signature)

## Wireframes ASCII / Layout concept

## Decisiones justificadas (por qué no defaults)

## Próximos pasos para implementación
```

Stack de motion: motion-one, framer-motion v11, Scroll-driven Animations, View Transitions API, Anchor Positioning. Todo motion respeta `prefers-reduced-motion`.

## Referencias

- `references/design-process.md` — proceso en 2 pasadas.
- `references/typography.md` — sistema tipográfico.
- `references/color-palette.md` — paleta, contraste y color moderno.
- `references/layout-motion.md` — layout, motion y signature element.
- `references/writing-in-design.md` — copy como material de diseño.
- `references/frontend-design-source.md`, `references/interaction-design-source.md` — fuentes absorbidas.
- Design system formal → `disenar-design-system`. Auditoría a11y/SEO → `verificar-compliance`.
