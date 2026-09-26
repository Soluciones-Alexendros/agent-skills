---
name: codigo-arquitectura
description: >-
  Análisis de arquitectura de codebase: capas, acoplamiento, puntos de profundización y
  oportunidades de modularización. Usar ante 'revisa la arquitectura', 'dónde acopla esto' o
  mapa de módulos. No usar para auditoría de seguridad ni higiene git.
license: MIT
metadata:
  author: Soluciones-Alexendros
  version: "0.2.0"
  dominio: codigo
  idioma: es

---
# Mejorar la Arquitectura del Código

Surface architectural friction and propose **deepening opportunities** — refactors that turn shallow modules into deep ones. The aim is testability and AI-navigability.

This command is _informed_ by the project's domain model and built on a shared design vocabulary:

- Run the `/codebase-design` skill for the architecture vocabulary (**module**, **interface**, **depth**, **seam**, **adapter**, **leverage**, **locality**) and its principles (the deletion test, "the interface is the test surface", "one adapter = hypothetical seam, two = real"). Use these terms exactly in every suggestion — don't drift into "component," "service," "API," or "boundary."
- The domain language in `CONTEXT.md` gives names to good seams; ADRs in `docs/adr/` record decisions this command should not re-litigate.

## Qué hace / Propósito

Analiza un codebase para detectar fricción arquitectónica y proponer oportunidades de profundización (**deepening**): refactors que convierten módulos someros en módulos profundos para ganar testabilidad y navegabilidad por IA. Presenta los candidatos en un informe visual HTML autónomo y guía la refactorización elegida hasta dejar el dominio y las decisiones registradas en `CONTEXT.md` y ADRs.

## Cuándo usarme / Triggering

- Cuando se pida analizar la arquitectura de un codebase o revisarlo en busca de oportunidades de refactor.
- Cuando se sospechen módulos someros, acoplamiento excesivo, interfaces más complejas que su implementación o código difícil de testear.
- Frases como "improve architecture", "deepening opportunities", "revisa la arquitectura de este proyecto" o "¿qué refactorizo primero?".
- Cuando se quiera un informe visual HTML con candidatos antes/después y una recomendación priorizada.
- **NO usar cuando**: el trabajo sea revisión de seguridad del código (usar `codigo-seguridad`) o hardening y mantenimiento de un sistema Linux (usar `alignux-seguridad`); esta skill es análisis y refactor de codebase.

## Referencias internas

- `HTML-REPORT.md` — léelo antes de generar el informe: contiene el scaffold HTML completo, los patrones de diagramas (Mermaid, CSS y SVG) y la guía de estilos.

## Process

### 1. Explore

Read the project's domain glossary (`CONTEXT.md`) and any ADRs in the area you're touching first.

Then use the Agent tool with `subagent_type=Explore` to walk the codebase. Don't follow rigid heuristics — explore organically and note where you experience friction:

- Where does understanding one concept require bouncing between many small modules?
- Where are modules **shallow** — interface nearly as complex as the implementation?
- Where have pure functions been extracted just for testability, but the real bugs hide in how they're called (no **locality**)?
- Where do tightly-coupled modules leak across their seams?
- Which parts of the codebase are untested, or hard to test through their current interface?

Apply the **deletion test** to anything you suspect is shallow: would deleting it concentrate complexity, or just move it? A "yes, concentrates" is the signal you want.

### 2. Present candidates as an HTML report

Write a self-contained HTML file to the OS temp directory so nothing lands in the repo. Resolve the temp dir from `$TMPDIR`, falling back to `/tmp` (or `%TEMP%` on Windows), and write to `<tmpdir>/architecture-review-<timestamp>.html` so each run gets a fresh file. Open it for the user — `xdg-open <path>` on Linux, `open <path>` on macOS, `start <path>` on Windows — and tell them the absolute path.

The report uses **Tailwind via CDN** for layout and styling, and **Mermaid via CDN** for diagrams where a graph/flow/sequence reliably communicates the structure. Mix Mermaid with hand-crafted CSS/SVG visuals — use Mermaid when relationships are graph-shaped (call graphs, dependencies, sequences), and hand-built divs/SVG when you want something more editorial (mass diagrams, cross-sections, collapse animations). Each candidate gets a **before/after visualisation**. Be visual.

For each candidate, render a card with:

- **Files** — which files/modules are involved
- **Problem** — why the current architecture is causing friction
- **Solution** — plain English description of what would change
- **Benefits** — explained in terms of locality and leverage, and how tests would improve
- **Before / After diagram** — side-by-side, custom-drawn, illustrating the shallowness and the deepening
- **Recommendation strength** — one of `Strong`, `Worth exploring`, `Speculative`, rendered as a badge

End the report with a **Top recommendation** section: which candidate you'd tackle first and why.

**Use CONTEXT.md vocabulary for the domain, and the `/codebase-design` vocabulary for the architecture.** If `CONTEXT.md` defines "Order," talk about "the Order intake module" — not "the FooBarHandler," and not "the Order service."

**ADR conflicts**: if a candidate contradicts an existing ADR, only surface it when the friction is real enough to warrant revisiting the ADR. Mark it clearly in the card (e.g. a warning callout: _"contradicts ADR-0007 — but worth reopening because…"_). Don't list every theoretical refactor an ADR forbids.

See [HTML-REPORT.md](references/html-report.md) for the full HTML scaffold, diagram patterns, and styling guidance.

Do NOT propose interfaces yet. After the file is written, ask the user: "Which of these would you like to explore?"

### 3. Grilling loop

Once the user picks a candidate, run the `/grilling` skill to walk the design tree with them — constraints, dependencies, the shape of the deepened module, what sits behind the seam, what tests survive.

Side effects happen inline as decisions crystallize — run the `/domain-modeling` skill to keep the domain model current as you go:

- **Naming a deepened module after a concept not in `CONTEXT.md`?** Add the term to `CONTEXT.md`. Create the file lazily if it doesn't exist.
- **Sharpening a fuzzy term during the conversation?** Update `CONTEXT.md` right there.
- **User rejects the candidate with a load-bearing reason?** Offer an ADR, framed as: _"Want me to record this as an ADR so future architecture reviews don't re-suggest it?"_ Only offer when the reason would actually be needed by a future explorer to avoid re-suggesting the same thing — skip ephemeral reasons ("not worth it right now") and self-evident ones.
- **Want to explore alternative interfaces for the deepened module?** Run the `/codebase-design` skill and use its design-it-twice parallel sub-agent pattern.

## Uso

Análisis y refactor de arquitectura: invocar ante «revisa la arquitectura», sospecha de módulos someros o necesidad de mapa de módulos con informe HTML. No usar para auditoría de seguridad ni higiene git (ver «Cuándo usarme / Triggering»).

## Estructura

- `SKILL.md` — proceso Explore → informe HTML → grilling loop.
- `HTML-REPORT.md` — extra top-level: scaffold HTML, patrones de diagramas y guía de estilo (leer antes de generar el informe).
- Sin `scripts/`: skill puramente analítica.

## Referencias

- Internas: `HTML-REPORT.md` (existe).
- Canon externo (no incluido en este repo): skills `/codebase-design`, `/grilling`, `/domain-modeling`.
- `CONTEXT.md` y `docs/adr/` _(ejemplo)_: rutas del proyecto objetivo, no de esta skill.

## Referencias

- [references/html-report.md](references/html-report.md): informe HTML de ejemplo generado por la skill.
- Para tipado avanzado → `typescript-avanzado`.
