# Estándares de Estructura ALIGNUX

## Convención de Nombres Skills

### Patrones Aprobados

| Tipo | Patrón | Ejemplos | Validación |
|------|--------|----------|------------|
| **Familias SDLC** | `familia-subdominio` | `disenar-interfaz`, `construir-upstash`, `verificar-owasp`, `operar-seguridad` | `OPENCODE_NAME_PATTERN` |

### Reglas Normativas

1. **Español por defecto** — `disenar-interfaz` no `web-design`
2. **Sustantivo, no verbo** — `planificacion-archivos` (histórica, suprimida 2026-09) no `planning-with-files`
3. **Sin sufijos redundantes** — `datos-postgres` (histórica, suprimida 2026-09) no `supabase-postgres-best-practices`
4. **SDK/CLI en submódulo** — `construir-upstash` + `references/redis.md` no `upstash-redis-js`
5. **Nombre = Directorio** — obligatorio, validador lo verifica

---

## Taxonomía de Tags (Jerárquica, Obligatoria)

### Estructura
```
familia.subdominio.etiqueta
```

### Familias Válidas (Prefijos Raíz)

| Familia | Subdominios Típicos | Skills Asociadas |
|---------|---------------------|------------------|
| `disenar` | `arquitectura`, `constitucion`, `design-system`, `interfaz` | disenar.* |
| `construir` | `typescript`, `upstash`, `proton-suite` | construir.* |
| `verificar` | `compliance`, `performance`, `owasp`, `fullaudit`, `repo`, `hooks` | verificar.* |
| `operar` | `release`, `lifecycle`, `mantenimiento`, `seguridad` | operar.* |

### Reglas de Tags
- **Mínimo 3, máximo 10** por skill
- **Formato**: `familia.subdominio.etiqueta` (minúsculas, puntos separadores)
- **Excepción ALIGNUX**: `sistema.ALIGNUX` (mayúsculas por identidad)
- **Validador**: Verifica prefijo raíz en `TAG_TAXONOMY_PREFIXES`

---

## Estructura de Directorios por Skill

```
skill-name/
├── SKILL.md                 # Frontmatter + body (<500 líneas)
├── references/              # Documentación técnica lazy-loaded
│   ├── archivo1.md          # ≤300 líneas, TOC si >100
│   └── archivo2.md
├── scripts/                 # Scripts ejecutables (opcional)
│   └── script.sh
└── assets/                  # Plantillas, iconos, fuentes (opcional)
    └── template.md
```

### Progressive Disclosure (3 Niveles)

| Nivel | Contenido | Carga | Límite |
|-------|-----------|-------|--------|
| 1 | Frontmatter (name, description, tags) | Siempre | ~100 palabras |
| 2 | SKILL.md body | Al invocar skill | <500 líneas |
| 3 | references/, scripts/, assets/ | Bajo demanda | Ilimitado |

---

## Librería Compartida (`plantillas/`)

Contenedor de lo **reutilizable** entre skills: plantillas canónicas y scripts compartidos. No es una skill (no tiene `SKILL.md`). Canon externo: `plantillas/` no existe en este repo.

```
plantillas/
├── README.md               # manifiesto + convención + registro
├── SKILL_TEMPLATE.md       # plantilla canónica de SKILL.md
└── scripts/                # librería de scripts reutilizables (.py/.sh)
```

**Frontera:** los `scripts/` **internos** de cada skill se quedan en su skill (se versionan con ella). En `plantillas/scripts/` solo vive lo **compartido/reutilizable** por varias skills.

**Requisitos de un script de la librería:**
1. Cabecera de metadatos (`name`, `version`, `tags`, `author`, `license`, `purpose`, `uso`).
2. Error handling explícito; sin fallos silenciosos.
3. Comentarios explicativos (el *por qué*).
4. Informes/logs con niveles y salida estructurada opcional.
5. CLI con `--help`/`--version`; códigos de salida `0` (OK) · `1` (hallazgos) · `2` (entorno/uso).
6. Read-only e idempotente salvo indicación contraria.
7. Validado (`py_compile` / `shellcheck`) antes de publicarse.

El validador excluye `plantillas/` y `scripts/` del cómputo de skills (directorios reservados), evitando falsos positivos.

---

## Validador Automatizado (plantillas/scripts/Validador_AgentSkills.py — canon externo, no incluido en este repo)

### Checks Implementados

| Categoría | Reglas | Severidad |
|-----------|--------|-----------|
| **Frontmatter** | Campos requeridos, name pattern, name=dir, description length | ERROR |
| **Estructura** | Body ≤500 líneas, secciones requeridas (propósito, triggering, referencias) | ERROR/WARNING |
| **Calidad** | Imperativos vs explicaciones, ejemplos, formatos salida | WARNING/INFO |
| **Referencias** | ≤300 líneas, TOC si >100 | WARNING/INFO |
| **Tags** | Mínimo 3, taxonomía, prefijos válidos | ERROR/WARNING |
| **Identidad ALIGNUX** | `ALIGNUX.*` mayúsculas, coherencia | ERROR |

### Modo Estricto
- `strict_mode=True` (default): warnings de estructura → ERROR
- Exit code: 0 = todo válido, 1 = hay errores
- CI-ready: integrable en pipelines

---

## Plantilla SKILL.md Canónica

Ver: plantillas/SKILL_TEMPLATE.md (canon externo, no incluido en este repo)

---

## Referencias Cruzadas Obligatorias

Toda skill debe declarar en `## Referencias internas`:
- Qué archivos en `references/` existen
- Cuándo leer cada uno (triggering contextual)
- Qué NO está en referencias (evita búsquedas infructuosas)