# agent-skills

25 skills de ingeniería para agentes de programación, mantenidas por Soluciones-Alexendros bajo licencia MIT. Los nombres, dominios y contenido de las skills están en inglés; las conversaciones y los resultados permanecen en español.

## Inicio rápido

```bash
git clone https://github.com/Soluciones-Alexendros/agent-skills.git
cp -r agent-skills/skills/<nombre-de-la-skill> ~/.agents/skills/
```

## Configuración en OpenCode (harness principal)

OpenCode es el harness principal: no necesita sistema de plugins, solo `AGENTS.md` + `opencode.json` (`skillDirectories`). El agente evalúa cada petición y la asigna a una skill según su descripción y palabras clave.

```bash
git clone https://github.com/Soluciones-Alexendros/agent-skills.git
cd agent-skills
bash scripts/install.sh            # global: ~/.config/opencode/skills, ~/.agents/skills, ~/.codex/skills, ~/.cursor/skills
bash scripts/install-opencode.sh   # local al proyecto: .opencode/skills + .agents/skills
```

Comprueba el enrutado con:

```bash
python tools/skill-router/route.py "limpia mi sistema Arch" --top 3
```

Consulta `docs/harness-integration.md` (tabla multi-harness), `docs/opencode-setup.md` y `docs/routing.md`.

## Skills por dominio

25 skills repartidas en 4 dominios activos (`build`, `operate`, `planning`, `verify`). El dominio `design` está reservado para futuras skills de arquitectura y actualmente está vacío.

### planning (4) — Planificación y desglose de tareas

| Skill                                | Descripción                                                                                                                                                                                                                                          |
| ------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `planning-source-driven-development` | Desarrollo guiado por fuentes: verifica cada decisión de implementación contra la documentación oficial del framework antes de programar. Úsala al empezar trabajo desconocido. No para ediciones rutinarias en código ya conocido.                  |
| `planning-test-driven-development`   | Ciclo TDD rojo-verde-refactor: primero el test que falla, hazlo pasar, refactoriza. Para bugs, reproduce con un test primero. Úsala al corregir bugs o añadir comportamiento. No para prototipos exploratorios.                                      |
| `planning-spec-driven-development`   | Especificación estructurada antes del código: objetivo, comandos, estructura, estilo, pruebas y límites. Flujo con puertas: Spec → Plan → Tareas → Implementación. Úsala al acotar trabajo de varios pasos. No para arreglos triviales de una línea. |
| `planning-task-breakdown`            | Divide el trabajo en tareas pequeñas y verificables con criterios de aceptación explícitos. Troceado vertical ordenado por dependencias, puntos de control cada 2-3 tareas. Úsala al planificar una implementación. No para ejecutar el trabajo.     |

### build (6) — Construcción, automatización y ecosistemas

| Skill                 | Descripción                                                                                                                                                                                                                                                              |
| --------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `build-automation`    | Automatización de pipelines CI/CD: build, test, deploy. Matriz de SO, caché de dependencias, artefactos, etapas y jobs. Úsala al montar pipelines. No para publicar releases (ver `operate-release`).                                                                    |
| `build-design-system` | Construcción de sistemas de diseño: tokens DTCG (Style Dictionary, Figma Tokens), Tailwind v4, librería de componentes reutilizables. Úsala al crear tokens o kits de UI. No para la dirección visual de una pantalla (ver `build-interface`).                           |
| `build-interface`     | Dirección visual intencional de una UI: sistema tipográfico, paleta, maquetación, movimiento, elemento de firma. El resultado es un plan de diseño visual justificado. Úsala al diseñar o rediseñar interfaces. No para pipelines de tokens (ver `build-design-system`). |
| `build-proton-suite`  | Proton Mail (Bridge IMAP/SMTP local, MCP Mail) y Proton Pass (pass-cli JSON, MCP Pass). Lee, busca y clasifica correo; obtén secretos; envía email. Úsala al trabajar con Proton. No para otros proveedores de correo.                                                   |
| `build-typescript`    | Tipado avanzado de TypeScript: genéricos, tipos condicionales, infer, tipos con marca, patrones de API tipada. Úsala para lógica de tipos compleja. No para revisión de seguridad (ver `verify-owasp`) ni mapeo de arquitectura (ver `verify-architecture`).             |
| `build-upstash`       | Enrutador del ecosistema Upstash (7 modos): Redis (caché, sesiones, KV), Vector (embeddings, RAG), Search (texto completo), QStash (colas, cron, workflows), Ratelimit, Blob, Box. Úsala al integrar servicios Upstash. No para bases de datos relacionales.             |

### verify (9) — Auditoría de código, calidad y seguridad

| Skill                 | Descripción                                                                                                                                                                                                                                                                                                             |
| --------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `verify-architecture` | Verificación de arquitectura de código: análisis de estructura, mapeo de dependencias, detección de desviaciones, oportunidades de refactor. Úsala al revisar arquitectura. No para revisión de seguridad (ver `verify-owasp`).                                                                                         |
| `verify-compliance`   | Auditoría de cumplimiento web: accesibilidad (WCAG 2.2 AA), legal (RGPD, consentimiento, cookies), SEO on-page y off-page. Matriz PASS/FAIL, puntuación ponderada, plan de remediación RICE. Úsala al auditar cumplimiento. No para rendimiento (ver `verify-performance`).                                             |
| `verify-dependencies` | Auditoría de dependencias (SCA/CVE): pipeline multi-lenguaje (npm, pip, cargo, go, maven, gradle, composer, gem) para vulnerabilidades, malware, typosquatting y dependencias sin usar o desactualizadas. Genera SBOM. Úsala al escanear la cadena de suministro. No para fallos de código propio (ver `verify-owasp`). |
| `verify-fullaudit`    | Enrutador de auditoría web holística: deriva a `verify-compliance`, `verify-performance`, `verify-repo` o `build-interface`. Úsala cuando pidan una revisión completa sin foco concreto. No ejecuta las auditorías por sí misma.                                                                                        |
| `verify-hooks`        | Hooks locales de git: Husky, lint-staged, Prettier, typecheck y tests en el commit; e2e en el push si existen. Úsala al poner puertas de calidad locales. No para CI remota (ver `operate-release`).                                                                                                                    |
| `verify-owasp`        | Revisión de seguridad de código (OWASP): inyección, XSS, autenticación/autorización, criptografía, SSRF, secretos y mala configuración. Úsala al buscar vulnerabilidades en el código. No para hardening del host (ver `operate-security`).                                                                             |
| `verify-performance`  | Auditoría de rendimiento web: Core Web Vitals, Lighthouse, TTFB/FCP, modos de renderizado, caché HTTP y CDN, optimización de carga. Úsala al diagnosticar lentitud. No para cumplimiento (ver `verify-compliance`).                                                                                                     |
| `verify-repo`         | Auditoría integral del repo y arranque canónico del plan (repo starting): sincroniza el clon, tablero de estado y hoja de ruta, contraste con el estándar del repo, corrección hacia adelante. Úsala al abrir un plan. No para cerrar releases (ver `operate-release`).                                                 |
| `verify-testing`      | Verificación de pruebas y QA: estrategia de tests, revisión de su calidad, análisis de cobertura y métricas. Úsala al evaluar una suite. No para escribir los tests en sí.                                                                                                                                              |

### operate (6) — Operación, mantenimiento y seguridad en Linux

| Skill                 | Descripción                                                                                                                                                                                                                                                                              |
| --------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `operate-lifecycle`   | Enrutador del ciclo de vida del trabajo: inicio de plan, puerta de hooks vía `verify-hooks` o cierre de release vía `operate-release`. Úsala al enrutar entre fases. No para ejecutar auditorías, hooks o releases.                                                                      |
| `operate-maintenance` | Mantenimiento sistematizado de Linux: higiene, actualizaciones, limpieza y optimización. Modos graduados, solo lectura por defecto, ejecución con puertas de riesgo y snapshots reversibles. Úsala al limpiar o ajustar un equipo. No para seguridad defensiva (ver `operate-security`). |
| `operate-monitoring`  | Configuración de monitorización y observabilidad: métricas, trazabilidad, logs y alertas. Úsala al montar paneles y alertas. No para forense de incidentes (ver `operate-security`).                                                                                                     |
| `operate-release`     | Cierre de repo en GitHub: publicación de versiones, auditoría CI/CD y cierre post-plan. Versionado semántico, changelog y cadena de suministro de Actions. Úsala al publicar. No para el inicio de plan (ver `verify-repo`).                                                             |
| `operate-health`      | Diagnóstico de salud de Linux: health checks, auditorías rápida y completa, huella del sistema, puntuación de salud 0–100. Úsala al evaluar una máquina. No para ejecutar limpieza (ver `operate-maintenance`) ni hardening (ver `operate-security`).                                    |
| `operate-security`    | Seguridad defensiva del host Linux: postura, forense ligero de logs, CVEs, hardening de sysctl y SSH, AppArmor/SELinux, auditd y fail2ban. Úsala al auditar o endurecer un host. No para fallos de código de aplicación (ver `verify-owasp`).                                            |

## Nomenclatura y frontmatter

- Estructura plana: `skills/<nombre-de-la-skill>/SKILL.md`.
- El campo `name` es idéntico al nombre del directorio: `<dominio>-<slug>` en kebab-case. El prefijo es el dominio (normativo, no orientativo).
- El frontmatter lleva exactamente 6 claves: `name`, `description` (alcance y límites), `license: MIT`, `compatibility: "opencode, codex, cursor, copilot"`, `allowed-tools` y `metadata` con `author`, `version` (semver), `domain`, `type`, `keywords` y `language: en`.
- Conjunto cerrado de tipos: `atomic` (una sola capacidad) · `orchestrator` (flujo de varios pasos) · `router` (deriva a otras skills) · `audit` (evaluación de solo lectura con informe).

## Añadir una nueva skill

Crea un directorio de primer nivel (estructura plana, sin anidamiento):

```bash
mkdir -p skills/<nombre-de-la-skill>
```

Incluye `SKILL.md` con el frontmatter estándar:

```yaml
---
name: <nombre-de-la-skill>
description: >-
  Qué hace. Úsala cuando el operador la pida. No para otras familias.
license: MIT
compatibility: "opencode, codex, cursor, copilot"
allowed-tools: "Read, Grep, Glob, Bash, Write"
metadata:
  author: Soluciones-Alexendros
  version: 3.0.0
  domain: build
  type: atomic
  language: en
  keywords: <nombre-de-la-skill>
---
```

El cuerpo debe incluir `## Overview` y `## When to Use`. Las skills que empaquetan scripts ejecutables también incluyen `## Tools` y `scripts/tests/smoke_sh.sh`.

## Referencias cruzadas

Las flechas (`→ otra-skill`) de las descripciones deben apuntar a una skill existente en este catálogo.

## Validación

```bash
bash run-validation.sh
```

Comprueba: esquema del frontmatter, cláusulas de alcance de las descripciones, canon de encabezados, paridad del catálogo entre carpetas, README y TAXONOMY, resolución de referencias y smoke tests.
