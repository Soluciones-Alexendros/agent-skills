---
name: build-interface
description: >
  Direct visual design for interfaces with own identity: aesthetic direction,
  typographic system, palette, layout, motion and signature element. Each
  decision is deliberate with respect to the brief.
license: MIT
metadata:
  author: "Soluciones-Alexendros (adapted)"
  version: "2.0.0"
  domain: build
  type: atomic
  language: en
---
# build-interface — Intentional Visual Design

## Purpose

Guide visual design for interfaces with own identity: aesthetic direction, typographic system, palette, layout, motion and signature element. Each decision is deliberate with respect to the brief.

## When to Use

New UI, redesign, palette/typography definition or interaction polish.

## Output Format

Template:

```markdown
# [Visual Design Plan]

## Brief & Concrete Subject

## Token System (Color, Type, Layout, Signature)

## ASCII Wireframes / Layout Concept

## Justified Decisions (why not defaults)

## Next Steps for Implementation
```

Motion stack: motion-one, framer-motion v11, Scroll-driven Animations, View Transitions API, Anchor Positioning. All motion respects `prefers-reduced-motion`.

## References

- `references/design-process.md` — 2-pass process.
- `references/typography.md` — typographic system.
- `references/color-palette.md` — palette, contrast and modern color.
- `references/layout-motion.md` — layout, motion and signature element.
- `references/writing-in-design.md` — copy as design material.
- `references/frontend-design-source.md`, `references/interaction-design-source.md` — absorbed sources.
- Formal design system → `build-design-system`. a11y/SEO audit → `verify-compliance`.
