---
name: verificar-repo
description: >-
  Auditoría integral de repositorios e inicio canónico de plan (repo starting):
  sincroniza el clon, tablero de estado/roadmap/fallos, contrasta con
  repo-standard (P0/P1/P2, CI quality→test→smoke, Renovate) y corrige tras sí.
  Usar cuando el operador pida escanear, health check, repo starting, inicio de
  plan o modo plan. No usar para cierre de release ni publicación
  (→ operar-release).
license: MIT
metadata:
  author: Soluciones-Alexendros
  version: "2.2.0"
  dominio: verificar
  tipo: atomic
  idioma: es
---

# verificar-repo — Auditoría integral de repositorios

## Propósito

Tomar un repositorio en estado desconocido y devolverlo alineado con el remoto cuando proceda, contrastado con el canon [repo-standard](../../docs/repo-standard/structure.md), saneado tras confirmación y con plan de evolución. El health check vive aquí; `operar-release` no lo duplica.

## Cuándo usar

Escanear o auditar un repo, alinear con el estándar de flota, health check, repo starting, inicio de plan o arranque de modo plan.

## Procedimiento

Reglas: no destruir sin confirmación; secreto → P0; registrar si la suite pasa antes de tocar; Conventional Commits; no inventar; `git pull --ff-only` solo con árbol limpio y clon detrás; no tocar settings de org.

Fase I inicio de plan. Fases 0–4 diagnóstico. Fases 5–6 intervención tras sí. Fase 7 entrega. Fase 8 handoff.

- **I.** Antes de `/design` o `enter_plan_mode`: `references/inicio-plan.md`. `python3 <skill_root>/scripts/inicio_plan.py <ruta> --profile <P0|P1|P2> --out <fuera>`. Tablero `ESTADO.md` + `ESTADO.html`. P0 de secreto detiene el diseño.
- **0a.** `git fetch --prune origin`. Árbol sucio o divergente → preguntar. Solo detrás y limpio → `git pull --ff-only`.
- **0.** `bash <skill_root>/scripts/audit-repo.sh <ruta> --profile <P0|P1|P2> --out <fuera>`.
- **1–3.** Fallos P0–P4, contraste con [structure.md](../../docs/repo-standard/structure.md) y `references/canon.md`, formato.
- **4.** Plan; no implementar hasta el sí.
- **5–6.** Rama `audit/AAAAMMDD`. Frontend solo si hay UI (`references/frontend-ui-ux.md`).
- **7.** Informe `references/plantilla-informe.md`.
- **8.** Si el operador pide cierre o finalizar un plan: sin P0 ni suite en rojo; entregar perfil, informe y checklist §8 a `operar-release` (publicación = B/F; cierre de trabajo = G).

```bash
OUT=$(mktemp -d)
python3 "$SKILL_ROOT/scripts/inicio_plan.py" <repo> --profile P1 --out "$OUT"
bash "$SKILL_ROOT/scripts/audit-repo.sh" <repo> --profile P1 --out "$OUT"
```

## Herramientas

| Script                               | Propósito                                   |
| ------------------------------------ | ------------------------------------------- |
| `scripts/inicio_plan.py`             | Tablero de partida (estado, camino, fallos) |
| `scripts/audit-repo.sh`              | Entrada única Fase 0 (escáner + estructura) |
| `scripts/scan_repo.py`               | Reconocimiento                              |
| `scripts/check-product-structure.sh` | Chequeo de estructura P0/P1/P2              |

## Referencias

- [structure.md](../../docs/repo-standard/structure.md)
- `references/canon.md`, `references/reutilizacion.md`
- `references/higiene-community.md`, `references/convenciones-y-canon.md`
- `references/verificacion-y-tests.md`, `references/frontend-ui-ux.md`, `references/plantilla-informe.md`
- `references/inicio-plan.md` — repo starting / modo plan.
- Hooks locales → `verificar-hooks`. Cierre → `operar-release`. Dependencias → `verificar-dependencias`.
