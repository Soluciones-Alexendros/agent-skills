# Modo compliance — matriz SEO/A11y/SEM/legal

Fusión del flujo `web-compliance` (FASE 0→8, 51 checks ACC/TEC/ONP/OFF/SEM/ANA/LEG).

## Flujo

1. **Alcance**: dominio, idiomas, accesos (GSC/GA4/GTM/GAds), normativa (WCAG 2.2 AA
   siempre; EN 301 549/EAA si B2C UE; ADA/508 si EE. UU.).
2. **Inventario**: `core/utils/audit_page.py` por plantilla + `robots.txt`/`sitemap.xml`.
3. **Evaluación**: registry `core/configs/checks.json` (prefijos ACC/TEC/ONP/OFF/SEM/ANA/LEG);
   50% script + 50% manual obligatorio (teclado, zoom 200%, contraste con `contrast.py`).
4. **Scoring**: `run.py --checks resultados.json --outdir output/` → dictamen
   POSITIVO/PARCIAL/NEGATIVO (0 FAIL Críticos + ACC ≥90% + TEC ≥85%).
5. **Informe y RICE**: `REPORT.md` + roadmap 4 sprints.

## Entrada/salida

- Entrada: `{"target":…, "checks": [{"id":…, "resultado": "PASS|FAIL|WARN|NA|PENDING", …}]}`.
- Salida en `--outdir`: `score.json`, `REPORT.md`, `REPORT.html`, `issues.csv`.

## Refs específicas

Ver `refs.md` (WCAG 2.2, protocolos manuales, Consent Mode v2, benchmarks SEM).
