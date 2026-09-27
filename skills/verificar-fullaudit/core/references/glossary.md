# Glosario Fullaudit

- **Check**: unidad auditable con ID permanente (`core/configs/checks.json`).
- **Dictamen**: veredicto compliance (POSITIVO/PARCIAL/NEGATIVO).
- **Veredicto e2e**: APTO / APTO CON OBSERVACIONES / NO APTO.
- **Dictamen dual**: pareja dictamen + veredicto del modo full.
- **Semáforo**: Verde ≥90 · Ámbar 70–89 · Rojo <70 (% PASS sobre evaluables).
- **PENDING**: no verificable aún; **N/A**: no aplicable (justificado). Ambos fuera del denominador.
- **RICE**: reach × impact × confidence / effort; ordena el backlog.
- **Sprint 0–3**: Crítico/48h · Alto/sem.1 · Medio/sem.2 · Bajo/sem.3.
- **CWV**: LCP (≤2.5s) · INP (≤200ms) · CLS (≤0.1). Lab = Lighthouse; field = CrUX/RUM (manda field).
- **Triple pasada**: formularios en vacío → inválido → válido.
- **Evidencia**: URL/dato/salida/captura (compliance); locator+screenshot+console (e2e).
- **Deuda (h)**: esfuerzo estimado de remediación por severidad.
- **Modo**: compliance | e2e | performance | local | full (`orchestrator.py --list-modes`).
