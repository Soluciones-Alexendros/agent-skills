---
name: codigo-arquitectura
description: >-
  Análisis de arquitectura de codebase: capas, acoplamiento, puntos de profundización y
  oportunidades de modularización. Usar ante 'revisa la arquitectura', 'dónde acopla esto' o
  mapa de módulos. No usar para auditoría de seguridad ni higiene git.
license: MIT
metadata:
  author: Soluciones-Alexendros
  version: "0.3.0"
  dominio: codigo
  idioma: es

---
# Mejorar la Arquitectura del Código

Detecta fricción arquitectónica y propone **oportunidades de profundización** (deepening): refactors que convierten módulos someros en módulos profundos. El objetivo es la testabilidad y la navegabilidad por IA.

Esta skill se apoya en el modelo de dominio del proyecto y en un vocabulario de diseño compartido:

- La skill `/codebase-design` aporta el vocabulario de arquitectura (**módulo**, **interfaz**, **profundidad**, **seam**, **adapter**, **leverage**, **locality**) y sus principios (el test de borrado, «la interfaz es la superficie de test», «un adapter = seam hipotético, dos = real»). Usa estos términos exactos en cada sugerencia; no derives a «componente», «servicio», «API» o «frontera».
- El lenguaje de dominio de `CONTEXT.md` da nombre a buenos seams; los ADR de `docs/adr/` registran decisiones que esta skill no debe re-litigar.

## Qué hace / Propósito

Analiza un codebase para detectar fricción arquitectónica y proponer oportunidades de profundización (**deepening**): refactors que convierten módulos someros en módulos profundos para ganar testabilidad y navegabilidad por IA. Presenta los candidatos en un informe visual HTML autónomo y guía la refactorización elegida hasta dejar el dominio y las decisiones registradas en `CONTEXT.md` y ADRs.

## Cuándo usarme / Triggering

- Cuando se pida analizar la arquitectura de un codebase o revisarlo en busca de oportunidades de refactor.
- Cuando se sospechen módulos someros, acoplamiento excesivo, interfaces más complejas que su implementación o código difícil de testear.
- Frases como "improve architecture", "deepening opportunities", "revisa la arquitectura de este proyecto" o "¿qué refactorizo primero?".
- Cuando se quiera un informe visual HTML con candidatos antes/después y una recomendación priorizada.
- Para mapear dependencias con dependency-cruiser/madge, modelar con C4/Structurizr o registrar decisiones con la plantilla ADR (ver `references/`).
- **NO usar cuando**: el trabajo sea revisión de seguridad del código (usar `web-seguridad`) o hardening y mantenimiento de un sistema Linux (usar `linux-seguridad`); esta skill es análisis y refactor de codebase.

## Referencias internas

- `references/html-report.md` — léelo antes de generar el informe: contiene el scaffold HTML completo, los patrones de diagramas (Mermaid, CSS y SVG) y la guía de estilos.
- `references/analisis-dependencias.md` — dependency-cruiser y madge: mapas de dependencias, reglas de acoplamiento y detección de ciclos.
- `references/c4-structurizr.md` — modelado C4 con Structurizr (Contexto, Contenedores, Componentes, Código).
- `references/plantilla-adr.md` — plantilla de Architecture Decision Record para registrar decisiones.
- `references/monolito-modular.md` — patrones de monolito modular: módulos con fronteras explícitas sin microservicios.

## Proceso

### 1. Explorar

Lee primero el glosario de dominio del proyecto (`CONTEXT.md`) y los ADR de la zona que vayas a tocar.

Después usa la herramienta Agent con `subagent_type=Explore` para recorrer el codebase. No sigas heurísticas rígidas: explora de forma orgánica y anota dónde sientes fricción:

- ¿Dónde exige entender un concepto saltar entre muchos módulos pequeños?
- ¿Dónde hay módulos **someros** (shallow): interfaz casi tan compleja como la implementación?
- ¿Dónde se han extraído funciones puras solo por testabilidad, pero los bugs reales esconden en cómo se las llama (sin **locality**)?
- ¿Dónde hay módulos fuertemente acoplados con fugas a través de sus seams?
- ¿Qué partes del codebase no tienen tests o son difíciles de testear con su interfaz actual?

Aplica el **test de borrado** a todo lo que sospeches somero: ¿borrarlo concentraría la complejidad o solo la movería? Un «sí, la concentra» es la señal buscada.

Para un mapa objetivo de dependencias, apoya la exploración con `references/analisis-dependencias.md` (dependency-cruiser/madge) antes de redactar candidatos.

### 2. Presentar candidatos como informe HTML

Escribe un HTML autónomo en el directorio temporal del SO para no ensuciar el repo. Resuelve el temp desde `$TMPDIR`, con fallback a `/tmp` (o `%TEMP%` en Windows), y escribe en `<tmpdir>/architecture-review-<timestamp>.html` para que cada ejecución tenga fichero fresco. Ábrelo para el usuario (`xdg-open <ruta>` en Linux, `open <ruta>` en macOS, `start <ruta>` en Windows) e indícale la ruta absoluta.

El informe usa **Tailwind por CDN** para maquetación y estilo, y **Mermaid por CDN** para diagramas donde un grafo/flujo/secuencia comunique bien la estructura. Mezcla Mermaid con visuales CSS/SVG hechos a mano: Mermaid cuando las relaciones tienen forma de grafo (call graphs, dependencias, secuencias), divs/SVG a mano cuando quieras algo más editorial (diagramas de masa, cortes transversales, animaciones de colapso). Cada candidato lleva visualización **antes/después**. Sé visual.

Cada candidato se renderiza como tarjeta con:

- **Ficheros** — qué ficheros/módulos están implicados
- **Problema** — por qué la arquitectura actual causa fricción
- **Solución** — descripción en lenguaje llano de qué cambiaría
- **Beneficios** — explicados en términos de locality y leverage, y cómo mejorarían los tests
- **Diagrama antes/después** — lado a lado, dibujado a medida, ilustrando la shallowness y el deepening
- **Fuerza de recomendación** — una de `Strong`, `Worth exploring`, `Speculative`, renderizada como badge

Cierra el informe con una sección **Recomendación principal**: qué candidato atacarías primero y por qué.

**Usa el vocabulario de `CONTEXT.md` para el dominio y el de `/codebase-design` para la arquitectura.** Si `CONTEXT.md` define «Order», habla del «módulo de intake de Order», no del «FooBarHandler» ni del «servicio Order».

**Conflictos con ADR**: si un candidato contradice un ADR existente, solo aflóralo cuando la fricción sea real y merezca reabrir el ADR. Márcalo claramente en la tarjeta (p. ej. callout de aviso: _«contradice ADR-0007, pero merece reabrirse porque…»_). No listes cada refactor teórico que un ADR prohíbe.

Ver [references/html-report.md](references/html-report.md) para el scaffold HTML completo, patrones de diagramas y guía de estilo.

NO propongas interfaces todavía. Tras escribir el fichero, pregunta al usuario: «¿Cuál de estos quieres explorar?».

### 3. Bucle de grilling

Cuando el usuario elija un candidato, ejecuta la skill `/grilling` para recorrer el árbol de diseño con él: constraints, dependencias, forma del módulo profundizado, qué queda tras el seam, qué tests sobreviven.

Los efectos laterales ocurren inline a medida que las decisiones cristalizan; ejecuta la skill `/domain-modeling` para mantener el modelo de dominio al día:

- **¿Nombras un módulo profundizado con un concepto que no está en `CONTEXT.md`?** Añade el término a `CONTEXT.md`. Crea el fichero de forma perezosa si no existe.
- **¿Afinas un término difuso durante la conversación?** Actualiza `CONTEXT.md` ahí mismo.
- **¿El usuario rechaza el candidato con una razón de peso?** Ofrece un ADR con: _«¿Quieres que lo registre como ADR para que futuras revisiones no lo vuelvan a sugerir?»_ Solo cuando la razón la necesitaría un futuro explorador para no re-sugerir lo mismo; omite razones efímeras («ahora no compensa») y autoevidentes.
- **¿Quieres explorar interfaces alternativas para el módulo profundizado?** Ejecuta `/codebase-design` con su patrón de subagentes paralelos «design-it-twice».

Registra la decisión final con [references/plantilla-adr.md](references/plantilla-adr.md).

## Uso

Análisis y refactor de arquitectura: invocar ante «revisa la arquitectura», sospecha de módulos someros o necesidad de mapa de módulos con informe HTML. No usar para auditoría de seguridad ni higiene git (ver «Cuándo usarme / Triggering»).

## Estructura

- `SKILL.md` — proceso Explorar → informe HTML → bucle de grilling.
- `references/html-report.md` — scaffold HTML, patrones de diagramas y guía de estilo (leer antes de generar el informe).
- `references/analisis-dependencias.md` — dependency-cruiser y madge.
- `references/c4-structurizr.md` — modelado C4 con Structurizr.
- `references/plantilla-adr.md` — plantilla ADR.
- `references/monolito-modular.md` — patrones de monolito modular.
- Sin `scripts/`: skill puramente analítica.

## Herramientas

Sin `scripts/` propios. Las herramientas externas viven documentadas en `references/`:

| Recurso | Propósito |
|---|---|
| `references/analisis-dependencias.md` | dependency-cruiser, madge (mapas y reglas) |
| `references/c4-structurizr.md` | C4 + Structurizr (modelado) |
| `references/plantilla-adr.md` | Plantilla ADR |
| `references/monolito-modular.md` | Patrones de monolito modular |

## Referencias

- Internas: `references/html-report.md` (scaffold del informe), `references/analisis-dependencias.md`, `references/c4-structurizr.md`, `references/plantilla-adr.md`, `references/monolito-modular.md`.
- Canon externo (no incluido en este repo): skills `/codebase-design`, `/grilling`, `/domain-modeling`.
- `CONTEXT.md` y `docs/adr/` _(ejemplo)_: rutas del proyecto objetivo, no de esta skill.
- Para tipado avanzado → `codigo-typescript`.
