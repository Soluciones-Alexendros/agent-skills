# Despliegue de Aprendizajes: Metodología ALIGNUX

## Definición
**Despliegue de aprendizajes** = Transformar experiencia histórica (~4 décadas), patrones recurrentes, limitaciones superadas e insights en **skills operativas validadas**, no en documentación pasiva.

---

## Ciclo de 6 Fases

### Fase 1: EXTRAER — Identificar Patrón Histórico

**Entrada**: Experiencia vivida, código legacy, decisiones pasadas, post-mortems, frustraciones recurrentes.

**Preguntas guía**:
- ¿Qué problema resolví 3+ veces con variaciones menores?
- ¿Qué límite creí inquebrantable y luego superé?
- ¿Qué convención adopté por moda y luego lamenté?
- ¿Qué estructura me obligó a workarounds constantes?

**Salida**: `Patrón Histórico` documentado con:
- Contexto original (era, limitaciones)
- Solución aplicada entonces
- Por qué funcionó / falló
- Lección extraíble

**Ejemplo ALIGNUX**: "Nombres skills con sufijos -js/-py/-cli" → patrón histórico de fragmentación por SDK → lección: namespace + submódulos.

---

### Fase 2: SINTETIZAR — Conectar con Principios Constitucionales

**Entrada**: Patrón Histórico + `principios-fundamentales.md` (mismo `references/`)

**Proceso**:
1. Mapear patrón a principios (1-7)
2. Identificar tensiones: ¿El patrón viola algún principio?
3. Derivar **especificación normativa** del principio aplicado

**Salida**: `Especificación Constitutiva`:
- Principio(s) invocado(s)
- Regla normativa derivada
- Excepciones justificadas (con trazabilidad)

**Ejemplo ALIGNUX**: Principio 2 (Coherencia) + Principio 3 (Estructura habilita) → Regla: `dominio.subdominio.accion` + tags jerárquicos + validador.

---

### Fase 3: ESTRUCTURAR — Materializar en Skill

**Entrada**: Especificación Constitutiva

**Plantilla obligatoria** (ver plantillas/SKILL_TEMPLATE.md — canon externo, no incluido en este repo):
```
skill-name/
├── SKILL.md (frontmatter + body <500 líneas)
├── references/ (≤300 líneas c/u, TOC si >100)
├── scripts/ (ejecutables, opcional)
└── assets/ (plantillas, opcional)
```

**Checks obligatorios**:
- Frontmatter: name, description, tags (3-10), license, version
- Name = Directorio
- Tags: taxonomía `dominio.subdominio.etiqueta`
- Body: secciones propósito, triggering, referencias
- Referencias internas declaradas con triggering contextual

---

### Fase 4: VALIDAR — Verificación Automatizada

**Herramienta**: plantillas/scripts/Validador_AgentSkills.py --strict (canon externo, no incluido en este repo)

**Criterios de paso**:
- 0 ERRORS (frontmatter, estructura, tags, identidad ALIGNUX)
- Warnings revisados y justificados o corregidos
- Exit code 0

**Si falla**: Regresar a Fase 3. No hay "excepciones temporales" — o pasa validador o no es skill ALIGNUX.

---

### Fase 5: INTEGRAR — Enlazar en Ecosistema

**Acciones obligatorias**:
1. Actualizar `CATALOGO_SKILLS.md` con nueva fila
2. Añadir referencias cruzadas en skills relacionadas
3. Verificar tags: `tag:dominio.*` encuentra la nueva skill
4. Probar triggering: `skill({ name: "nueva.skill" })` carga correctamente
5. Registrar en `MIGRACION_LOG.md`: fecha, skill, cambios, decisiones

**Verificación de cohesión**:
- ¿`tag:sistema.ALIGNUX` agrupa las 3 skills ALIGNUX?
- ¿`tag:datos.*` agrupa todo ecosistema datos?
- ¿No hay skills huérfanas (sin tags, sin referencias cruzadas)?

---

### Fase 6: ITERAR — Feedback Real → Refinamiento

**Fuentes de feedback**:
- Uso real: triggering incorrecto, description ambigua
- Validador: warnings recurrentes → mejorar plantilla
- Usuario: "falta X", "confuso Y" → refinar sections
- Evolución técnica: nuevo SDK, deprecación → actualizar referencias

**Ciclo**: Cada iteración = nueva versión en `version` frontmatter + entrada en `MIGRACION_LOG.md`.

**Principio**: La coherencia no es estado final, es práctica continua (Principio 4).

---

## Métricas de Calidad de Despliegue

| Métrica | Objetivo | Medición |
|---------|----------|----------|
| **Tiempo extracción→skill** | <2 horas | Timestamp git |
| **Validador first-pass** | 100% | CI logs |
| **Cobertura tags** | 100% skills ≥3 tags | Validador |
| **Referencias cruzadas** | 0 skills huérfanas | Script verificación |
| **Triggering accuracy** | >90% | Logs uso real |

---

## Anti-Patrones (Qué NO Hacer)

| Anti-Patrón | Por Qué Falla | Corrección ALIGNUX |
|-------------|---------------|-------------------|
| **Documentar sin validar** | Docs mienten en días | Validador = verdad ejecutable |
| **Crear skill por feature request** | Acumulación sin síntesis | Extraer patrón histórico primero |
| **Nombres por convención herramienta** | Cargo cult, no coherencia | Principio 1+2: identidad + coherencia |
| **Tags planos o inventados** | Búsqueda rota | Taxonomía jerárquica obligatoria |
| **Referencias >300 líneas sin TOC** | Mantenimiento imposible | Límite + TOC obligatorio |
| **Sin referencias cruzadas** | Skills huérfanas, descubrimiento roto | Fase 5 obligatoria |

---

## Checklist de Despliegue (Para Cada Nueva Skill)

- [ ] Fase 1: Patrón histórico documentado con contexto y lección
- [ ] Fase 2: Principios constitucionales invocados, regla normativa derivada
- [ ] Fase 3: Estructura completa (SKILL.md, references/, tags, version)
- [ ] Fase 4: `Validador_AgentSkills.py --strict` → exit 0
- [ ] Fase 5: Catálogo actualizado, referencias cruzadas, triggering probado, log registrado
- [ ] Fase 6: Feedback loop definido, versión incrementada

---

*Esta metodología asegura que cada skill ALIGNUX no sea "otro archivo en el directorio" sino **síntesis histórica validada y desplegada como capacidad operativa coherente**.*