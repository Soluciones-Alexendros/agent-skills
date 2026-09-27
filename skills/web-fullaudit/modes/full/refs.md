# Refs modo full

## Orden de ejecución recomendado

1. `discovery` (mapa) → 2. `audit_page` por plantilla (estáticos) → 3. loop e2e
   por persona (funcional + medido + axe) → 4. Lighthouse/CWV → 5. evaluación
   visual LLM → 6. fusión → 7. scoring dual → 8. informe + RICE.

## Fusión (`merge_results.py`)

- Acepta N entradas (objeto con `checks` o array; `resultado` o `status`).
- FAIL/WARN nunca pisados por PASS posterior; se conserva la evidencia más completa.
- IDs distintos no colisionan (ACC/TEC/… vs RT/FN/…); 93 checks unificados.

## Criterios de cierre

- Dictamen POSITIVO **y** veredicto APTO → cierre con re-auditoría trimestral.
- Cualquier otro par → roadmap RICE; re-auditoría parcial tras Sprint 0/1.
- Todo PENDING documentado con owner y protocolo de verificación (ver `core/references/playbook.md`).
