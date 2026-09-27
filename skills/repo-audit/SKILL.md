---
name: repo-audit
description: >-
  Auditoría integral de repositorios de estado desconocido: sincroniza el clon
  con GitHub, diagnostica, contrasta con el canon repo-standard
  (estructura P0/P1/P2, docs, CI quality→test→smoke, Renovate), planifica y
  corrige tras confirmación. Usar al pedir escanear/auditar un repo, alinear
  con el estándar, "pon al día este proyecto", "repo audit" o health check.
  No usar para cierre de release ni publicación (→ repo-release).
license: MIT
metadata:
  author: Soluciones-Alexendros
  version: "1.0.0"
  dominio: repo
  idioma: es

---

# repo-audit — Auditoría integral de repositorios

## Propósito

Tomar un repositorio en estado desconocido y devolverlo: (a) alineado con el remoto cuando proceda, (b) contrastado con el canon [repo-standard](../../docs/repo-standard/structure.md), (c) saneado tras confirmación, (d) validado con tests, (e) con plan de evolución. El health check vive en esta skill; `repo-release` no lo duplica.

## Reglas duras (innegociables)

1. **No destruir**: nunca borrar código, historial ni datos sin confirmación. Rama `audit/AAAAMMDD` en fase 5, no en el reconocimiento. Un PR de alineación por repo; sin force-push.
2. **Seguridad primero**: secreto detectado → P0; rotación y purga de historial solo con autorización.
3. **Verde antes y después**: registrar si la suite pasa antes de tocar nada.
4. **Cambios pequeños**: Conventional Commits; commit solo si el operador lo pide.
5. **Separar lo disruptivo**: reescrituras grandes solo en el informe.
6. **No inventar**: anclar en docs del repo o en `references/`. Verificar ADRs en el remoto si hace falta.
7. **Preservar el propósito**: entender el producto antes de alinear estructura.
8. **Convención local gana** en estilo de código; el **contrato de flota** (nombres de jobs CI, Renovate, árbol docs P0/P1) gana sobre desviaciones injustificadas.
9. **Sincronización segura**: solo `git pull --ff-only` con árbol limpio y clon solo detrás del upstream.
10. **No tocar settings de org** ni protección de `main` desde el agente: informar y dejar al humano.

## Workflow por fases

Fases 0–4: diagnóstico. Fases 5–6: intervención tras sí. Fase 7: entrega.

Raíz de la skill = directorio que contiene este `SKILL.md`.

### Fase 0a — Sincronizar con GitHub

Antes del escáner:

1. Sin `.git`, sin `origin`, o `origin` no es `github.com` → anotar y seguir en local.
2. `git fetch --prune origin`. Si falla → **parar** (clon posiblemente viejo).
3. `git status --porcelain` y `git rev-list --left-right --count HEAD...@{upstream}`.
4. Solo detrás + árbol limpio → `git pull --ff-only`. Delante/divergente/sucio → preguntar. Alineado → seguir.

### Fase 0 — Reconocimiento

1. `bash <skill_root>/scripts/audit-repo.sh <ruta> --profile <P0|P1|P2> --out <fuera>` (entrada única: ejecuta el escáner y el chequeo de estructura; ver `Herramientas`).
2. Detectar **perfil** P0 / P1 / P2 (`references/canon.md` y [structure.md](../../docs/repo-standard/structure.md)).
3. `git log --oneline -20`, README, manifiestos, CI.
4. Mapa del proyecto y puntos calientes.

### Fase 1 — Detección de fallos

Estática / dinámica / semántica. Severidades P0–P4.

### Fase 2 — Contraste con canon

Leer en este orden (solo lo necesario):

1. [structure.md](../../docs/repo-standard/structure.md) — perfiles, árbol, nombrado y commits (canon vigente).
2. `references/canon.md` — resumen operativo de perfiles y decisiones cerradas.
3. `references/reutilizacion.md` — checklist §8 y copiar vs adaptar.
4. `references/higiene-community.md` — community standards residuales.
5. `references/convenciones-y-canon.md` — estilo por lenguaje (la convención local del repo gana aquí).

Hallazgos típicos de flota: jobs CI sin nombres canónicos, Dependabot version-updates, falta de Renovate, docs sin meta-sección, ausencia de AGENTS/ARCHITECTURE en P1, smoke ausente.

### Fase 3 — Formato y contenidos

Escáner + meta-sección «Propósito de este documento» en markdown contractuales (excepto CHANGELOG).

### Fase 4 — Plan

Presentar plan de alineación al operador (orden de `reutilizacion.md`). No implementar hasta el sí. Settings de `main` y org van como pasos manuales.

### Fase 5 — Implementación

Tras sí: rama `audit/AAAAMMDD` o `chore/repo-standard-*`. Aplicar checklist del perfil. Snippets CI desde el repo remoto `stacks/`, no inventar. `make validate` / `make test` / `make smoke` cuando existan.

### Fase 6 — Pulido frontend (si hay UI)

`references/frontend-ui-ux.md` tras confirmación.

### Fase 7 — Entrega

`references/plantilla-informe.md`. Incluir: resultado Fase 0a, perfil, salida de `check-product-structure`, gap vs §8, cambios aplicados, pasos humanos pendientes (protección `main`, App Renovate).

### Fase 8 — Handoff a repo-release (solo si el operador pide cierre)

Esta fase no publica nada: prepara el traspaso a `repo-release`.

1. Verificar que no quedan P0 abiertos ni suite en rojo; si los hay, volver a Fase 5, no derivar.
2. Entregar a `repo-release`: perfil, informe de Fase 7, checklist §8 marcado y pasos humanos pendientes.
3. `repo-release` asume desde su Arranque (remoto `github.com`, `gh auth`, modo auditoría/remediación/cierre). El health check no se repite allí: queda en esta skill.

## Recursos

| Archivo | Cuándo |
|---------|--------|
| `scripts/audit-repo.sh` | Fase 0 (entrada única) |
| `scripts/scan_repo.py` | Fase 0 (invocado por `audit-repo.sh`) |
| `scripts/check-product-structure.sh` | Fase 0–2 (invocado por `audit-repo.sh`) |
| `references/canon.md` | Fase 2 (resumen operativo) |
| `references/reutilizacion.md` | Fase 2–4 |
| `references/*` _(glob: detalle flota)_ | Detalle flota |
| `references/higiene-community.md` | Fases 2–3 |
| `references/convenciones-y-canon.md` | Estilo por lenguaje |
| `references/verificacion-y-tests.md` | Fases 4–5 |
| `references/frontend-ui-ux.md` | Fase 6 |
| `references/plantilla-informe.md` | Fase 7 |

Upstream vivo: https://github.com/Iniciativas-Alexendros/repo-standard. Canon local: [docs/repo-standard](../../docs/repo-standard/structure.md) (`structure.md`, `ci-cd.md`, `release.md`, `security.md`, `templates/`).

## TL;DR

```bash
git -C <repo> fetch --prune origin
# si solo detrás + limpio: git -C <repo> pull --ff-only
OUT=$(mktemp -d)
bash "$SKILL_ROOT/scripts/audit-repo.sh" <repo> --profile P1 --out "$OUT"
# leer docs/repo-standard/structure.md + references/reutilizacion.md
# plan → sí → rama audit/… → alinear → informe → Fase 8 si hay cierre
```

## Uso

Usar al pedir escanear/auditar un repo, alinear con el estándar de flota o health check. No usar para cierre de release ni publicación (→ `repo-release`).

## Estructura

- `SKILL.md` — fases 0–8 y TL;DR.
- `scripts/` — entrada `audit-repo.sh`, escáner y chequeo de estructura.
- `references/` — canon de flota (`canon.md`, `reutilizacion.md` y detalle).
- `references/convenciones-y-canon.md`, `references/higiene-community.md`, `references/verificacion-y-tests.md`, `references/frontend-ui-ux.md`, `references/plantilla-informe.md` — apoyo por fase.

## Herramientas

| Script | Propósito |
|---|---|
| `scripts/audit-repo.sh` | Entrada única Fase 0 (escáner + estructura) |
| `scripts/scan_repo.py` | Reconocimiento (Fase 0) |
| `scripts/check-product-structure.sh` | Chequeo de estructura por perfil P0/P1/P2 (Fases 0–2) |
| `scripts/test_scan_repo.py` _(tests, no tocar)_ | Tests del escáner |
| `scripts/tests/smoke_sh.sh` _(tests, no tocar)_ | Smoke de scripts shell |

## Referencias

- [structure.md](../../docs/repo-standard/structure.md) — canon vigente: perfiles, árbol, nombrado, commits.
- `references/canon.md` — resumen operativo del canon (primero en local).
- `references/reutilizacion.md` — checklist §8 y copiar vs adaptar (verificar case exacto `reutilizacion.md`).
- `references/*` _(glob: detalle flota)_ — `overview.md`, `architecture-resumen.md`, `adrs-indice.md`, `coding-standards.md`, `testing.md`.
- `references/higiene-community.md`, `references/convenciones-y-canon.md`, `references/verificacion-y-tests.md`, `references/frontend-ui-ux.md`, `references/plantilla-informe.md`.
- Rutas del canon externo `docs/architecture/`, `docs/architecture/decisions/` (ADR-0001…0011 y `template.md`) y `stacks/` — código plano, viven en el repo remoto `https://github.com/Iniciativas-Alexendros/repo-standard`, no incluidas en esta skill.
- Para hooks locales → `repo-hooks`. Para cierre o publicación → `repo-release` (Fase 8).
- Para auditoría de dependencias → `web-seguridad`.
