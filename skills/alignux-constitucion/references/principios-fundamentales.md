# Principios Fundamentales ALIGNUX

## 1. Identidad sobre Convención

**Principio**: La identidad constitutiva (ALIGNUX en mayúsculas) prevalece sobre convenciones técnicas documentadas pero no enforzadas.

**Aplicación**:
- opencode documenta `^[a-z0-9]+(-[a-z0-9]+)*$` como convención
- Runtime no la valida → `ALIGNUX.*` funciona nativamente
- **Decisión**: Afirmar identidad, no pedir permiso a herramienta

**Por qué**: Una convención sin enforcement es sugerencia. Una identidad sin concesión es constitución.

---

## 2. Coherencia sobre Consistencia

**Principio**: Consistencia = mismo patrón repetido. Coherencia = mismo propósito servido.

**Aplicación**:
- Nombres consistentes: `upstash-redis-js`, `upstash-vector-js`, `upstash-qstash-js` (patrón repetido)
- Nombres coherentes: `datos-redis`, `datos-vectorial`, `upstash` (propósito: dominio claro, descubrimiento)
- **Decisión**: Refactorizar a coherencia aunque rompa consistencia superficial

**Por qué**: La consistencia sin coherencia es cargo cult. La coherencia permite evolución.

---

## 3. Estructura que Habilita, No que Constriñe

**Principio**: Directorios, nombres, tags, validación existen para *descubrimiento y uso*, no para satisfacer linter.

**Aplicación**:
- Tags jerárquicos → búsqueda `tag:datos.*` encuentra todo ecosistema datos
- Nombres `dominio.subdominio.accion` → autocompletado semántico
- Validador → verdad ejecutable, no docs que mienten
- **Decisión**: Cada regla estructural debe tener propósito de uso demostrable

**Por qué**: Estructura sin propósito es burocracia. Estructura con propósito es arquitectura.

---

## 4. Documentación Viva

**Principio**: Lo que no se actualiza automáticamente, miente. La única documentación verdadera es la que se valida en CI.

**Aplicación**:
- plantillas/scripts/Validador_AgentSkills.py = especificación ejecutable (canon externo, no incluido en este repo)
- Frontmatter tags = catálogo consultable
- Referencias con límite de líneas → mantenimiento forzoso
- **Decisión**: Automatizar veracidad, no confiar en disciplina humana

**Por qué**: La documentación manual se desincroniza en días. La automatizada, en commits.

---

## 5. Aprendizaje como Despliegue

**Principio**: Cada skill nueva no es "adición al catálogo" — es **síntesis de historia** desplegada como capacidad operativa.

**Aplicación**:
- `ALIGNUX.constitucion` sintetiza ~4 décadas → estándares operativos
- `datos-redis` sintetiza historia cache/sessions/KV → skill unificada
- `web-diseno` sintetiza historia tipografía/identidad → skill coherente
- **Decisión**: Crear skill = extraer patrón histórico, estructurar, validar, integrar

**Por qué**: Catálogo de skills sin síntesis histórica = acumulación. Con síntesis = sistema vivo.

---

## 6. No Codifiques Limitaciones Actuales como Principios Permanentes

**Principio** (de `historia-computacional.md`): Cada era creyó haber llegado al límite. La historia demuestra que los límites eran de imaginación/herramienta, no de posibilidad.

**Aplicación**:
- ❌ "Skills deben ser simples porque context window pequeño" → límite coyuntural
- ✅ "Skills estructuradas por progressive disclosure" → principio permanente
- ❌ "Un skill = un archivo" → restricción herramienta actual
- ✅ "Progressive disclosure: 3 niveles de carga" → arquitectura escalable
- **Decisión**: Diseñar para el siguiente paradigma, optimizar para el actual

**Por qué**: Optimizar para límite actual = deuda técnica futura. Diseñar para principio = activo permanente.

---

## 7. Herramientas que Amplifican Juicio, No Reemplazo

**Principio**: Agentes, LLMs, validadores, linters amplifican juicio humano; no lo sustituyen.

**Aplicación**:
- Validador detecta errores → humano decide corrección semántica
- Skill `skill-creator` guía creación → humano define propósito
- `ALIGNUX.constitucion` da marco → humano toma decisiones arquitectónicas
- **Decisión**: Automatizar verificación, no decisión

**Por qué**: Verificación sin juicio = burocracia algorítmica. Juicio sin verificación = intuición frágil.

---

## Resumen de Principios (Para Referencia Rápida)

| # | Principio | Decisión Operativa |
|---|-----------|-------------------|
| 1 | Identidad sobre convención | `ALIGNUX.*` mayúsculas, no exception |
| 2 | Coherencia sobre consistencia | Refactor nombres a propósito, no patrón |
| 3 | Estructura habilita | Tags, nombres, validador al servicio del uso |
| 4 | Documentación viva | Validador = verdad, CI = enforcement |
| 5 | Aprendizaje = despliegue | Cada skill = síntesis histórica operativa |
| 6 | No límites coyunturales | Diseño para siguiente paradigma |
| 7 | Herramientas amplifican | Verificación automática, decisión humana |