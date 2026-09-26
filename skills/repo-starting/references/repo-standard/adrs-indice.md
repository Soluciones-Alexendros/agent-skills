# Decisiones de arquitectura (ADR)

### Propósito de este documento

- **Objetivos:** Índice del registro de ADRs del canon (y, en un producto, de las decisiones de *ese* sistema).
- **Estructura:** Esta meta-sección → estados del ciclo → tabla ID/título/estado/prioridad → cómo añadir una.
- **Contenido a integrar según contexto:** En producto, vacía la tabla y lista solo ADRs del producto. Enlaza los ADRs del canon que adoptes (`repo-standard ≥x.y`). No copies el contenido de ADR-0001…0011: son del meta-estándar.

Registro de decisiones del canon. Estados: **Proposed** → **Accepted** → **Superseded** / **Deprecated**.

Prioridad: **P0** (hacer pronto) · **P1** (después de P0). Un ADR puede estar Accepted (política cerrada) con checklist de implementación aún abierto.

## Índice

> Nota: los ADR-0001…0011 y `template.md` viven en `docs/architecture/decisions/` del repo canon; esta skill solo incluye el índice.

| ID | Título | Estado | Prioridad |
|----|--------|--------|-----------|
| ADR-0001 | Este repo es el canon de flota | Accepted | — |
| ADR-0002 | Protección y metadatos como código | Accepted | P0 |
| ADR-0003 | Cuándo el job `build` es required | Accepted | P0 |
| ADR-0004 | Renovate org y política Dependabot | Accepted | P0 |
| ADR-0005 | Secret scanning / push protection org | Accepted | P0 |
| ADR-0006 | Reviews por perfil y label `automerge` | Proposed | P1 |
| ADR-0007 | Coverage ≥70% como gate opcional | Proposed | P1 |
| ADR-0008 | Snippets Astro y Python skills | Proposed | P1 |
| ADR-0009 | Scorecard P0 rojo/ámbar/verde | Proposed | P1 |
| ADR-0010 | SemVer del contrato del estándar | Proposed | P1 |
| ADR-0011 | Bootstrap al usar la plantilla | Proposed | P1 |

## Cómo añadir una

1. Copia `template.md` (en `docs/architecture/decisions/` del repo canon) a `ADR-NNNN-titulo-kebab.md`.
2. Incluye la meta-sección «Propósito de este documento», **Prioridad** (P0/P1) y **Checklist de implementación**.
3. Enlázala en esta tabla.
4. Si sustituye a otra, marca la antigua como Superseded y apunta aquí.
5. Resume el impacto en `CHANGELOG.md` `[Unreleased]` si cambia el contrato de flota.
