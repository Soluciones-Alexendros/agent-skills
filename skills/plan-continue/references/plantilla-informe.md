# Plantilla del informe final de auditoría

Usar SIEMPRE esta estructura exacta en la Fase 7. Resumir el informe en la respuesta. Si se guarda como fichero Markdown, hacerlo **fuera** del árbol auditado salvo que el operador pida dejarlo dentro. Todo hallazgo cita fichero y línea. Nada de relleno: las secciones vacías se marcan "Sin hallazgos" y no se eliminan (excepción: sección 9 sin UI → "Sin interfaz de usuario").

---

# Informe de auditoría: [nombre del repositorio]

**Fecha**: [AAAA-MM-DD] | **Rama de trabajo**: `audit/[fecha]` o `n/d (solo diagnóstico)` | **Commit base**: [hash]

## 1. Resumen ejecutivo

[Un párrafo: qué es el proyecto, semáforo global, cuántos hallazgos por severidad, qué se corrigió ya y qué queda propuesto.]

**Semáforo**:

- 🔴 **Rojo**: hay P0 abiertos, o build/tests rotos al cierre.
- 🟡 **Amarillo**: sin P0, pero hay P1 o P2 abiertos.
- 🟢 **Verde**: sin P0 ni P1 abiertos.

## 2. Estado encontrado

- **Propósito inferido**: [qué hace el proyecto y para quién, según README/código/historial]
- **Stack**: [lenguajes, frameworks, versiones objetivo]
- **Actividad**: [último commit, frecuencia, ramas vivas/abandonadas]
- **Salud inicial**: [build: pasa/rompe · tests: N, verdes/rojos · cobertura inicial: X % o n/d]
- **Inventario**: [resumen de scan_repo.py: ficheros, lenguaje principal, alertas destacadas]

## 3. Hallazgos

Tabla por severidad. Cada fila: ID, severidad, localización, descripción, estado (Corregido / Planificado / Aceptado).

| ID | Sev | Localización | Hallazgo | Estado |
|---|---|---|---|---|
| H-01 | P0 | src/auth.py:42 | Secreto hardcodeado detectado; movido a `os.environ` | Corregido |
| H-02 | P2 | requirements.txt:3 | Dependencia con `*` / `latest` | Planificado |

Severidades: **P0** seguridad/pérdida de datos · **P1** funcionalidad rota · **P2** deuda que bloquea evolución · **P3** calidad/legibilidad · **P4** cosmético.

## 4. Desviaciones del canon

[Contrastes de la Fase 2: guía de estilo violada, estructura de directorios, ficheros estándar ausentes, inconsistencias internas. Indicar para cada una si se corrigió o se justifica mantener.]

## 5. Correcciones aplicadas

Si hubo commits en la rama de auditoría, listarlos en orden:

```
fix(auth): mover credencial SMTP a variable de entorno
refactor(core): extraer módulos profundos de procesar()
test(parser): property-based tests de round-trip
```

Si el operador no pidió commit: listar los cambios en el árbol de trabajo con los mensajes Conventional Commits **propuestos** (sin crear commits).

Cambios NOTA: [cualquier corrección que altere comportamiento observable, con justificación].

## 6. Garantías de verificación

- **Suite final**: [N tests, estado, cobertura por módulo o n/d]
- **Invariantes documentados**: [lista por módulo crítico, o "Sin hallazgos"]
- **Property-based / fuzzing añadidos**: [qué propiedades, sobre qué; o "No ejecutado: <motivo>"]
- **Mutation score** (módulos críticos): [X %, mutantes supervivientes relevantes; o "No ejecutado: <motivo>"]
- **Lo que NO queda garantizado**: [lista honesta: caminos sin tests, supuestos no verificables]

## 7. Optimización estructural

[Cambios de organización de ficheros aplicados (antes → después), renombrados, duplicados eliminados, dependencias actualizadas/retiradas. Si ninguno: "Sin hallazgos".]

## 8. Ampliaciones implementadas

[Mejoras naturales de bajo riesgo añadidas según el propósito del proyecto; cada una con su justificación de encaje. Si ninguna: "Sin hallazgos".]

## 9. Pulido frontend (si aplica)

[Errores de axe/Lighthouse corregidos, advertencias solo anotadas, estados cubiertos (incl. parcial/degradado), anchos comprobados (360/768/1280/1920), tokens, métricas antes/después si se midieron.]

Si no hay UI: **Sin interfaz de usuario**.

## 10. Plan pendiente

[Trabajo no disruptivo que queda por hacer, ordenado por prioridad, con estimación grosera (S/M/L). Si ninguno: "Sin hallazgos".]

## 11. Propuestas disruptivas (para otro hilo)

Cada propuesta con: descripción, motivación, coste estimado, riesgo, y evaluación **interés** × **urgencia** (Alto/Medio/Bajo cada uno, con una frase de porqué).

| # | Propuesta | Motivación | Coste | Riesgo | Interés | Urgencia |
|---|---|---|---|---|---|---|
| D-01 | Migrar de CRA a Vite | Builds 10× más rápidos, CRA abandonado | M | Bajo | Alto | Medio |
| D-02 | Reescribir parser en Rust/WASM | Rendimiento en ficheros grandes | L | Alto | Medio | Bajo |

Criterio: **interés** = valor estratégico si se hace; **urgencia** = coste de no hacerlo pronto. Alto interés + alta urgencia = candidato a planificar ya en un hilo dedicado.

Si no hay propuestas: "Sin hallazgos".

## 12. Anexos

- Ruta al JSON completo de `scan_repo.py` (fuera del repo si aplica).
- Comandos para reproducir: build, tests, lint.
