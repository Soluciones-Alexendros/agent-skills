---
name: disenar-constitucion
description: >-
  Constitución ALIGNUX: marco pasivo de identidad, coherencia operativa y límites
  del agente en sistemas Linux. Usar solo cuando el operador pida la constitución
  ALIGNUX, principios ALIGNUX, alinear una respuesta con la identidad del sistema o
  validar una decisión o estructura contra el marco constitucional. No invocar de
  forma proactiva. No usar para mantenimiento ni seguridad concreta.
license: MIT
metadata:
  author: Soluciones-Alexendros
  version: "1.0.0"
  dominio: disenar
  idioma: es
---
# Constitución ALIGNUX

## Qué hace / Propósito
Canaliza los conocimientos y estándares de estructuras e identidades del sistema ALIGNUX. Documenta y da forma coherente, documentada e ilustrada al despliegue de aprendizajes sobre: el camino recorrido, la historia de la computación e informática vivida en ~4 décadas, el empuje necesario desde el estancamiento en programas y lógicas de hace décadas construidas en base a limitaciones físicas de recursos y equipos disponibles, así como conocimiento parcial en comparación a lo que hoy en día hemos documentado y somos capaces de teorizar y desarrollar en consecuencia gracias a los avances tecnológicos y científicos.

## Cuándo usarme / Triggering
- Cuando se necesite definir o consultar estándares de nomenclatura, arquitectura, identidad del sistema ALIGNUX
- Al diseñar nuevas skills, estructuras de datos, convenciones que deban alinearse con ALIGNUX
- Para documentar decisiones arquitectónicas con trazabilidad a principios constitucionales
- Al resolver conflictos entre convicciones técnicas y restricciones heredadas
- **NO usar cuando**: se trate de tareas operativas puras (ej: comandos Linux, debugging, código específico)

## Referencias internas
- `references/identidad.md` — Principios de identidad ALIGNUX (mayúsculas, nomenclatura, coherencia)
- `references/historia-computacional.md` — Línea temporal ~4 décadas: limitaciones → superación → estado actual
- `references/estandares-estructura.md` — Estándares de estructura: directorios, nombres, tags, validación
- `references/principios-fundamentales.md` — Principios revisados, fundamentos adaptados, perspectivas mejoradas
- `references/despliegue-aprendizajes.md` — Metodología para cohesionar aprendizajes en habilidades operativas
- `references/DirectoriosEsenciales.md` — Directorios esenciales del home y notación de referencia ALIGNUX (`·`): `·Aplicaciones` (raíz única: `··Ventana`/`··Terminal` producto + `··Fuentes` + `··Websites` + `··dotfiles`), `·Audiovisual` (medios); invariantes del canon CLI (`Scripts/`, `Shell/`, `Agentes/`) y mapa XDG (incl. `Documentos/Formatos` sin certificar). Leer antes de crear/mover directorios del home o instalar productos
- `references/registro-estructura-home.md` — Registro constitucional del estándar del home (plantilla de salida: contexto histórico, principio, especificación, trazabilidad, validación), con la evolución a `·Aplicaciones`. Leer para entender *por qué* del canon del home
- `references/convenciones-skills.md` — canon de convenciones de skills: nomenclatura, estructura, frontmatter, tags, validador, deuda aceptada, gobernanza. Leer antes de crear o modificar cualquier skill

## Estructura de salida
ALWAYS use this exact template:
# [Decisión/Estándar ALIGNUX]
## Contexto histórico (qué limitación supera)
## Principio constitucional aplicado
## Especificación técnica
## Trazabilidad a ~4 décadas de experiencia
## Validación de coherencia

---

## Identidad ALIGNUX (Inmutable)

**ALIGNUX se escribe SIEMPRE en MAYÚSCULAS** — es identidad constitucional, no excepción técnica. Cualquier mención en minúsculas o capitalizada incorrectamente es error de forma y fondo. El sistema opencode acepta `ALIGNUX.*` en frontmatter `name` porque **no valida el patrón en runtime** (skill.ts:58-75 lee `frontmatter.name` directamente sin regex). La convención documentada `^[a-z0-9]+(-[a-z0-9]+)*$` es guía, no enforzamiento.

## Línea Temporal Computacional (~4 Décadas)

| Era | Limitaciones | Superación | Estado Actual |
|-----|--------------|------------|---------------|
| Años 80-90 | RAM KB, CPU MHz, disco MB, sin red | Optimización extrema, código a mano | Fundamentos: eficiencia, minimalismo |
| Años 2000 | RAM MB, CPU GHz, disco GB, red lenta | Abstracciones, frameworks, patrones | Capas: productividad vs control |
| Años 2010 | RAM GB, multi-core, SSD, cloud | Contenedores, microservicios, DevOps | Escalabilidad horizontal |
| Años 2020+ | RAM TB, GPU/TPU, edge, IA generativa | Agentes autónomos, síntesis código, razonamiento | **ALIGNUX: coherencia constitutiva** |

**Lección central**: Cada era creyó haber llegado al límite. La historia demuestra que los límites eran de *imaginación y herramienta*, no de posibilidad. ALIGNUX codifica esta lección: **no codifiques limitaciones actuales como principios permanentes**.

## Principios Fundamentales Revisados

1. **Identidad sobre convención** — ALIGNUX en mayúsculas no es capricho, es ancla semántica
2. **Coherencia sobre consistencia** — Consistencia = mismo patrón; Coherencia = mismo propósito
3. **Estructura que habilita, no que constriñe** — Directorios, nombres, tags al servicio del descubrimiento
4. **Documentación viva** — Lo que no se actualiza, miente. Validador automatizado = verdad ejecutable
5. **Aprendizaje como despliegue** — Cada skill nueva es síntesis de historia, no adición aislada

## Estándares de Estructura (Normativos)

### Nomenclatura Skills
```
ALIGNUX                # Identidad constitucional del sistema (marco, no prefijo de skill; ver «Identidad ALIGNUX»)
familia-subdominio     # Nomenclatura de skills (17 skills: disenar.*, construir.*, verificar.*, operar.*)
```

### Tags (Taxonomía Jerárquica Obligatoria)
```
familia.subdominio.etiqueta  # ej: disenar.interfaz, construir.typescript, verificar.owasp, operar.seguridad
Mínimo 3, máximo 10 por skill
Prefijos válidos: disenar, construir, verificar, operar
```

### Validación Automatizada
- tools/validate/skill_spec.py (validador del repo): identidad ALIGNUX + convención opencode + tags + estructura
- Modo estricto: errores = bloqueo, warnings = revisión
- CI-ready: exit code 0 = todo válido, 1 = hay errores

## Despliegue de Aprendizajes (Metodología)

1. **Extraer** — De la experiencia (~4 décadas): patrón recurrente, limitación superada, insight
2. **Sintetizar** — Conectar con principios constitucionales, no con moda técnica actual
3. **Estructurar** — En skill: nombre, descripción, tags, referencias, plantilla salida
4. **Validar** — Pasar validador → coherencia garantizada
5. **Integrar** — Enlazar en catálogo, actualizar dependencias cruzadas
6. **Iterar** — Feedback real → refinamiento → nueva versión

---

*Esta constitución es documento vivo. Cada migración, cada skill nueva, cada decisión arquitectónica refuerza o refina estos principios. La coherencia no es estado final, es práctica continua.*

## Uso

Consulta de identidad y estándares ALIGNUX: invocar solo cuando el operador pida la constitución, principios ALIGNUX o alinear una respuesta con la identidad del sistema. No usar para mantenimiento ni seguridad concreta (ver `description` del frontmatter).

## Estructura

- `SKILL.md` — constitución, triggering, estándares y metodología.
- `../../docs/archives/reflexiones-constitucion.md` — extra: registro de razonamientos del autor (no normativo, archivado).
- `references/` — identidad, historia computacional, estándares de estructura, principios, despliegue de aprendizajes, directorios esenciales y registro del home.
- Sin `scripts/`: skill puramente documental.

## Referencias

- Internas: ver «Referencias internas» más arriba.
- Canon del repo: docs/STANDARD.md y validador tools/validate/skill_spec.py.
