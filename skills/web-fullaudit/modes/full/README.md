# Modo full — auditoría completa (compliance + e2e)

Modo por defecto cuando se pide "auditoría completa/web 360". Fusiona matriz
compliance (51 checks) + QA e2e (42 checks) en un único dictamen dual.

## Flujo

1. **Alcance**: como en `compliance` + `e2e` (URL, accesos, auth, personas, viewports, normativa).
2. **Compliance**: `modes/compliance/run.py` → `compliance.json` parcial.
3. **E2E**: `modes/e2e/run.py` → `compliance.json` e2e (validado).
4. **Fusión y dictamen dual**:
   `run.py --checks compliance.json e2e.json --outdir output/`
   → `merge_results` (FAIL nunca pisado por PASS) → `score` dual →
   `REPORT.md` + `REPORT.html` + `issues.csv`.
5. **RICE 4 sprints**: Sprint 0 Crítico/48h → S1 Alto/sem.1 → S2 Medio/sem.2 → S3 Bajo/sem.3.

## Dictamen dual

- **Dictamen compliance**: POSITIVO (0 FAIL Críticos + ACC ≥90% + TEC ≥85% + global ≥85%) /
  PARCIAL (global ≥70%) / NEGATIVO.
- **Veredicto e2e**: APTO (0 FAIL Críticas + ≥90%) / APTO CON OBSERVACIONES (70–89%) / NO APTO.
- Semáforo por dominio: Verde ≥90 / Ámbar 70–89 / Rojo <70.
- CWV: LCP ≤2.5s · INP ≤200ms · CLS ≤0.1 · TTFB ≤800ms.

## Refs específicas

Ver `refs.md` (orden de ejecución, fusión, criterios de cierre).
