# Interacción Guiada

Flujo conversacional estructurado de 4 fases para entender objetivo, contexto y restricciones antes de ejecutar acciones de mantenimiento.

---

Al invocar `operate-maintenance`, el agente inicia un flujo conversacional estructurado para entender objetivo, contexto y restricciones antes de ejecutar. El flujo tiene 4 fases:

### Fase 1: Diagnóstico de Contexto (Auto-detección + Preguntas)

El agente ejecuta `probe_system.py` automáticamente y pregunta:

```
🔍 Contexto detectado:
  • Distro: Ubuntu 24.04 (debian family)
  • Kernel: 7.0.0-29-generic
  • Paquetes: 2523 (apt)
  • Firewall: ufw activo
  • Disco /: 8% usado (937G/824G libre)
  • Servicios fallidos: 0

🎯 ¿Cuál es tu objetivo principal?
  1. Health-check rápido (audit-quick, ~3 min, solo lectura)
  2. Auditoría completa + hardening (audit-full, ~15 min, solo lectura)
  3. Mantenimiento rutinario (routine: updates, limpieza, huérfanos)
  4. Plan de optimización priorizado (optimize: plan P1-P4 sin ejecutar)
  5. Ejecutar limpieza aprobada (clean: requiere snapshot + aprobación)
  6. Verificar comando específico (risk_gate: clasificar riesgo R0-R3)
  7. Ver dependencias / diagnóstico (check_deps / probe_system)
  8. Generar informe de auditoría previa (report_render)

📋 ¿Hay restricciones o contexto adicional?
  • Entorno: [producción / staging / desarrollo / personal]
  • Ventana de mantenimiento: [inmediata / programada / sin ventana]
  • Nivel de riesgo tolerado: [conservador / estándar / agresivo]
  • Requiere compliance: [CIS / PCI-DSS / HIPAA / ninguno]
  • Snapshot tool disponible: [timeshift / snapper / btrfs / tar / none]
```

### Fase 2: Selección de Modo y Profundidad

Según respuesta, el agente propone plan concreto:

| Objetivo | Modo | Profundidad | Tiempo | Output |
|----------|------|-------------|--------|--------|
| Health-check | `audit-quick` | P0+P1 críticos | ~3 min | JSON + Health Score |
| Auditoría completa | `audit-full` | P0-P4 + lynis | ~15 min | JSON + Health Score + diff |
| Mantenimiento | `routine` | dry-run → execute | variable | Plan + JSON + verificación |
| Optimización | `optimize` | P1-P4 plan | ~5 min | Markdown plan P1-P4 |
| Limpieza | `clean` | execute + verify | variable | JSON + verificación post |
| Verificar comando | `risk_gate` | clasificación R0-R3 | <1s | Clasificación + requisitos |

### Fase 3: Ejecución con Confirmación Graduada

Para cada acción de escritura (R1+), el agente:

1. **Muestra plan en dry-run** con comandos exactos, riesgo, espacio a liberar
2. **Solicita confirmación explícita** (sí/no/modificar)
3. **Crea snapshot** (`snapshot_state.py`) si R1+
4. **Ejecuta con `risk_gate.py`** validando cada comando
5. **Verifica post-acción** (re-ejecuta checks afectados)
6. **Registra en log forense** (`session_logger.py`)

### Fase 4: Informe y Próximos Pasos

Genera informe adaptado al objetivo:

- **Health-check**: Resumen ejecutivo + Health Score + top 5 hallazgos
- **Auditoría completa**: Informe técnico + diff temporal + compliance gaps
- **Mantenimiento/Limpieza**: Resumen acciones + espacio liberado + verificación
- **Optimización**: Plan P1-P4 con impacto/riesgo/esfuerzo + comandos listos
- **Siempre**: Próximos pasos recomendados + comandos listos para copiar
