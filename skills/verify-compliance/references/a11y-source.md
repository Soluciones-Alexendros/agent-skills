---
name: web-accesibilidad
title: "web.accesibilidad"
description: "Auditoría de código UI para cumplimiento de Web Interface Guidelines (WCAG, UX/UI). Usar cuando se pida 'review my UI', 'check accessibility', 'audit design', 'review UX', o 'check my site against best practices'. Auditoría WCAG, UX/UI, guidelines."
license: MIT
metadata:
  author: alexendros
  tags:
    - web.accesibilidad
    - web.wcag
    - web.ux
    - web.auditoria
  version: "2.0.0"
---

# Auditoría de Accesibilidad y UX (Web Interface Guidelines)

## Qué hace / Propósito
Revisa código UI (HTML, CSS, JSX, TSX, Vue, Svelte) para cumplimiento de **Web Interface Guidelines** — estándares de accesibilidad (WCAG 2.1/2.2), usabilidad, consistencia visual y mejores prácticas de interacción. Genera hallazgos accionables con severidad, ubicación y recomendación de corrección.

## Cuándo usarme / Triggering
- **Auditoría de accesibilidad**: "Revisa mi UI por accesibilidad", "Check WCAG compliance", "Audita contraste, focus, ARIA"
- **Revisión UX/UI**: "Audita mi diseño", "Revisa usabilidad", "Check consistencia visual"
- **Cumplimiento guidelines**: "Verifica contra Web Interface Guidelines", "Revisa best practices"
- **NO usar cuando**: Diseño visual desde cero (→ `build-interface`), implementación Next.js (fuera de alcance)

## Referencias internas
- `references/wcag-checklist.md` — Checklist WCAG 2.1/2.2 AA: perceivable, operable, understandable, robust
- `references/ux-principles.md` — Principios de usabilidad: consistencia, feedback, prevención errores, flexibilidad
- `references/interaction-patterns.md` — Patrones de interacción: focus management, keyboard nav, live regions, modals
- `references/visual-design.md` — Consistencia visual: tipografía, espaciado, color, motion, responsive

## Estructura de salida
ALWAYS use this exact template:
# [Reporte de Auditoría Web]
## Resumen ejecutivo
## Hallazgos por severidad (Crítico/Alto/Medio/Bajo)
## Recomendaciones priorizadas
## Referencias WCAG/Guidelines aplicadas