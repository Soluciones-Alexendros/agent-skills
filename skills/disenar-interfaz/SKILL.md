---
name: disenar-interfaz
description: >-
  Dirección visual e interacción para UI: estética, tipografía, paleta, motion y
  microinteracciones. Usar al diseñar o rediseñar interfaces, identidad visual o polish de
  interacción. No usar para design system/tokens formales (→ disenar-design-system) ni auditoría
  a11y/SEO (→ verificar-compliance).
license: MIT
metadata:
  author: Soluciones-Alexendros
  version: "1.0.0"
  dominio: disenar
  idioma: es

---

# disenar-interfaz — Diseño Visual Intencional (Frontend Design)

## Qué hace / Propósito
Guía el proceso de diseño visual para crear interfaces con **identidad propia**, no templadas. Cubre: dirección estética, sistema tipográfico, paleta de colores, layout, motion, y signature element. El objetivo: que cada decisión de diseño sea deliberada y específica al brief, no un default genérico.

## Cuándo usarme / Triggering
- **Nueva UI desde cero**: "Diseña la interfaz para...", "Crea visual identity para..."
- **Rediseño existente**: "Rediseña mi dashboard", "Moderniza mi UI", "Elimina look templado"
- **Dirección estética**: "Define paleta y tipografía", "Crea design system base", "Signature element"
- **NO usar cuando**: auditoría accesibilidad/UX (→ `verificar-compliance`), design system formal (→ `disenar-design-system`)

## Referencias internas
- `references/design-process.md` — Proceso en 2 pasadas: brainstorm plan → review contra brief → build
- `references/typography.md` — Sistema tipográfico: display/body/utility faces, type scale, weights, spacing
- `references/color-palette.md` — Paleta 4-6 hex nombrados, semantic color, contrast ratios, dark mode; color moderno OKLCH/`color-mix`/color relativo
- `references/layout-motion.md` — Layout concept (ASCII wireframes), motion orquestado, signature element; stack moderno (motion-one, framer-motion v11, Scroll-driven Animations, View Transitions API, Anchor Positioning)
- `references/writing-in-design.md` — Copy como material de diseño: active voice, user-side naming, error/empty states

## Stack moderno de motion e interacción
- **motion-one**: microinteracciones y reveals con API mínima (`animate`, `scroll`, `inView`).
- **framer-motion v11**: layouts animados, gestos y transiciones en React.
- **Scroll-driven Animations** (CSS): `animation-timeline: scroll() | view()` para parallax y progress sin JS.
- **View Transitions API**: transiciones de vista SPA/MPA con `document.startViewTransition()`.
- **Anchor Positioning**: tooltips y popovers anclados en CSS puro.
- Todo motion respeta `prefers-reduced-motion`; ver detalle en `references/layout-motion.md`.

## Estructura de salida
ALWAYS use this exact template:
# [Plan de Diseño Visual]
## Brief & Sujeto concreto
## Token system (Color, Type, Layout, Signature)
## Wireframes ASCII / Layout concept
## Decisiones justificadas (por qué no defaults)
## Próximos pasos para implementación

## Fuentes fusionadas

- `references/frontend-design-source.md` — guía de identidad visual distintiva (absorbida).
- `references/interaction-design-source.md` — microinteracciones y motion (absorbida).

Leer la referencia de la fase en curso. Design system formal → skill `disenar-design-system`.

## Uso

Usar al diseñar o rediseñar interfaces, definir paleta/tipografía o pulir interacción. No usar para design system/tokens formales (→ `disenar-design-system`) ni auditoría a11y/SEO (→ `verificar-compliance`).

## Estructura

- `SKILL.md` — propósito, triggering y plantilla de salida.
- `references/design-process.md` — proceso en 2 pasadas.
- `references/typography.md` — sistema tipográfico.
- `references/color-palette.md` — paleta, contraste y color moderno.
- `references/layout-motion.md` — layout, motion moderno y signature element.
- `references/writing-in-design.md` — copy como material de diseño.
- `references/frontend-design-source.md`, `references/interaction-design-source.md` — fuentes absorbidas.

## Herramientas

Sin scripts en esta skill. El trabajo es de dirección visual y se apoya en las referencias anteriores.

## Referencias

- `references/design-process.md`, `references/typography.md`, `references/color-palette.md`, `references/layout-motion.md`, `references/writing-in-design.md`.
- `references/frontend-design-source.md`, `references/interaction-design-source.md`.
- Skills relacionadas: `disenar-design-system`, `verificar-compliance`.
