---
name: verificar-compliance
description: >-
  Auditoría de compliance web: accesibilidad (WCAG 2.2 AA / EN 301 549), legal
  (RGPD, Consent Mode v2, aviso legal, cookies), SEO on-page/off-page/SEM/analítica.
  Matriz de checks PASS/FAIL/N/A, scoring ponderado, dictamen POSITIVO/NEGATIVO/PARCIAL
  y plan de remediación RICE. Usar cuando el operador pida auditoría de cumplimiento,
  dictamen de compliance web o plan de remediación SEO/accesibilidad/legal. No usar
  para Core Web Vitals (→ verificar-performance) ni auditoría holística sin foco (→
  verificar-fullaudit).
license: MIT
metadata:
  author: Soluciones-Alexendros
  version: "2.1.1"
  dominio: verificar
  tipo: atomic
  idioma: es
---

# verificar-compliance — Auditoría de cumplimiento web

## Propósito

Auditar un website con evidencia medible, matriz de compliance y dictamen. Flujo one-shot FASE 0→8.

## Cuándo usar

Auditar un sitio web, revisar SEO/SEM, verificar WCAG/EN 301 549/EAA, comprobar cumplimiento legal web (cookies, consentimiento, aviso legal) o generar informe de cierre con plan de remediación.

## Procedimiento

Reglas: todo PASS exige evidencia; cada hallazgo lleva ID de `configs/checks.json`; lo no verificable queda PENDING; POSITIVO solo si 0 FAIL críticos, ≥90% PASS en Accesibilidad, ≥85% en SEO técnico y Consent Mode v2 conforme si hay analítica. Un FAIL crítico fuerza NEGATIVO.

1. **FASE 0 — Alcance.** Dominio, idiomas, entorno, accesos (GSC, GA4, GTM, GAds) y SEM activo. WCAG 2.2 AA siempre; EN 301 549/EAA si B2C en UE.
2. **FASE 1 — Inventario.** `scripts/audit_page.py` sobre home y plantillas. `robots.txt` y `sitemap.xml`.
3. **FASES 2–7 — Pilares.** Registry `configs/checks.json` (51 checks). Accesibilidad → `references/wcag22.md` (contraste con `scripts/contrast.py`). SEO → `references/playbook.md`. SEM → `references/sem.md`. Legal → `references/playbook.md` §Fase LEG.
4. **FASE 8 — Scoring.** `scripts/score.py` con `configs/thresholds.json`.
5. **Informe.** `scripts/report.py` y roadmap RICE (`references/remediation.md`).
6. Tras cambiar scripts o configs: `python3 scripts/selftest.py`.

Si el objetivo es `alexendros.dev`, re-verificar el baseline de `references/caso-alexendros.md`; no usarlo como evidencia vigente.

## Herramientas

| Script                                           | Uso                                              | Salida         |
| ------------------------------------------------ | ------------------------------------------------ | -------------- |
| `scripts/audit_page.py <url> [--json out.json]`  | Audita una URL                                   | JSON de checks |
| `scripts/contrast.py <fg> <bg> [--large]`        | Ratio WCAG; exit 0 AA+, 1 FAIL, 2 input inválido | JSON           |
| `scripts/score.py <results.json>`                | % por pilar, dictamen                            | JSON           |
| `scripts/report.py <results.json> [--md out.md]` | Informe de cierre                                | Markdown       |
| `scripts/selftest.py`                            | Suite integrada                                  | exit 0/1       |

Scripts en stdlib de Python.

## Formato de salida

Informe de cierre (matriz y dictamen), roadmap RICE 90 días y JSON de resultados.

## Referencias

- `references/playbook.md`, `references/checklist.md`, `references/wcag22.md`, `references/sem.md`.
- `references/seo-source.md`, `references/a11y-source.md`, `references/remediation.md`.
- `references/glossary.md`, `references/troubleshooting.md`, `references/caso-alexendros.md`.
- Rendimiento → `verificar-performance`. Holística → `verificar-fullaudit`.
