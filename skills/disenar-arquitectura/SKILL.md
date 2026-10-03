---
name: disenar-arquitectura
description: >-
  Análisis de arquitectura de codebase: capas, acoplamiento, puntos de profundización y
  oportunidades de modularización. Usar cuando el operador pida revisar la arquitectura,
  dónde acopla el código o un mapa de módulos. No usar para auditoría de seguridad (→
  verificar-owasp) ni higiene git (→ verificar-repo).
license: MIT
metadata:
  author: Soluciones-Alexendros
  version: "1.1.1"
  dominio: disenar
  tipo: atomic
  idioma: es
---

# Mejorar la arquitectura del código

## Propósito

Detectar fricción arquitectónica y proponer oportunidades de profundización (deepening): refactors que convierten módulos someros en módulos profundos para ganar testabilidad y navegabilidad por IA. Vocabulario: módulo, interfaz, profundidad, seam, adapter, leverage, locality.

## Cuándo usar

Análisis de arquitectura, sospecha de módulos someros, acoplamiento excesivo o necesidad de un informe HTML de candidatos.

## Procedimiento

1. **Explorar.** Leer `CONTEXT.md` y los ADR de la zona. Recorrer el codebase y anotar fricción: módulos someros, fugas de seam, falta de locality. Aplicar el test de borrado. Mapa de dependencias: `references/analisis-dependencias.md`.
2. **Informe HTML.** Escribir un HTML autónomo en `$TMPDIR/architecture-review-<timestamp>.html` (Tailwind y Mermaid por CDN). Cada candidato: ficheros, problema, solución, beneficios, diagrama antes/después, fuerza de recomendación. Cerrar con recomendación principal. Scaffold: `references/html-report.md`. Preguntar qué candidato explorar. No proponer interfaces todavía.
3. **Grill.** Cuando el operador elija, recorrer constraints y forma del módulo. Actualizar `CONTEXT.md` si nace un término. Registrar la decisión con `references/plantilla-adr.md`.

## Referencias

- `references/html-report.md` — leer antes de generar el informe.
- `references/analisis-dependencias.md` — dependency-cruiser y madge.
- `references/c4-structurizr.md` — modelado C4.
- `references/plantilla-adr.md` — plantilla ADR.
- `references/monolito-modular.md` — monolito modular.
- Tipado avanzado → `construir-typescript`. Seguridad → `verificar-owasp`.
