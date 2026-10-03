# agent-skills

27 skills de ingeniería para agentes de código, mantenidas por Soluciones-Alexendros bajo licencia MIT.

## Inicio rápido

```bash
git clone https://github.com/Soluciones-Alexendros/agent-skills.git
cp -r agent-skills/skills/<dominio>-<nombre> ~/.claude/skills/
```

## Habilidades por dominio

Las 27 skills están organizadas en 5 dominios:

### planning (4) — Planificación y descomposición de trabajo

| Skill                                  | Descripción                                                                                                                                                                 |
| -------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `planning-source-driven-development`   | Desarrollo guiado por fuentes oficiales: cada decisión de implementación se verifica contra la documentación oficial del framework antes de codificar.                      |
| `planning-test-driven-development`     | Ciclo TDD red-green-refactor: escribe test fallido, hazlo pasar, refactoriza. Para bugs, reproduce primero con test (Patrón Demuéstralo).                                   |
| `planning-spec-driven-development`     | Especificación estructurada antes de codificar: objetivo, comandos, estructura, estilo, testing y límites (Siempre/Pregunta/Nunca). Gated: Spec → Plan → Tasks → Implement. |
| `planning-planning-and-task-breakdown` | Descompone trabajo en tareas pequeñas y verificables con criterios de aceptación explícitos. Slicing vertical, orden por dependencias, checkpoints cada 2-3 tareas.         |

### build (6) — Construcción, automatización y ecosistemas

| Skill                 | Descripción                                                                                                                                                                                   |
| --------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `build-automation`    | Automatización de pipelines CI/CD: build, test, deploy. Matriz de SO, cache de dependencias, artifacts, stages y jobs.                                                                        |
| `build-design-system` | Construye design systems: tokens DTCG (Style Dictionary, Figma Tokens), Tailwind v4 (`@theme`), componente library (Button, Input, Card, Dialog).                                             |
| `build-interface`     | Dirección visual intencional para UI: sistema tipográfico, paleta, layout, motion, signature element. Output: plan de diseño visual con decisiones justificadas.                              |
| `build-proton-suite`  | Proton Mail (Bridge IMAP/SMTP local, MCP Mail) y Proton Pass (pass-cli v2.3+ JSON, MCP Pass). Leer/buscar/clasificar correo, obtener secrets, enviar emails.                                  |
| `build-typescript`    | Tipado avanzado TypeScript: generics, conditional types, infer, branded types, patrones de API tipada. No para security review ni arquitectura general.                                       |
| `build-upstash`       | Router ecosistema Upstash (7 modos): Redis (cache/sessions/KV), Vector (embeddings/RAG), Search (full-text), QStash (colas/cron/workflows), Ratelimit, Blob (S3), Box (sandboxed containers). |

### verify (9) — Auditoría, calidad y seguridad de código

| Skill                 | Descripción                                                                                                                                                                                                                                                      |
| --------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `verify-compliance`   | Auditoría compliance web: accesibilidad (WCAG 2.2 AA / EN 301 549), legal (RGPD, Consent Mode v2, aviso legal, cookies), SEO on-page/off-page/SEM/analítica. Matriz PASS/FAIL/N/A, scoring ponderado, dictamen POSITIVO/PARCIAL/NEGATIVO, plan remediación RICE. |
| `verify-dependencias` | Auditoría dependencias (SCA/CVE): pipeline multi-lenguaje (npm/pip/cargo/go/maven/gradle/composer/gem) detecta vulnerabilidades, malware, typosquatting, dependencias no usadas y outdated. Genera SBOM.                                                         |
| `verify-fullaudit`    | Router auditoría web holística: deriva a verify-compliance (compliance SEO/a11y/legal), verify-performance (CWV/rendering), verify-repo (health check repo) o build-interface (dirección visual). Para auditoría completa sin foco.                              |
| `verify-hooks`        | Configura y ejecuta hooks git locales: Husky, lint-staged, Prettier, typecheck, tests en pre-commit; e2e en pre-push si existe. Gate local de cierre de trabajo.                                                                                                 |
| `verify-owasp`        | Revisión seguridad código (OWASP): inyección, XSS, authn/authz, criptografía, SSRF, secretos, misconfiguración. Security review, busca vulnerabilidades en código.                                                                                               |
| `verify-performance`  | Auditoría performance web: Core Web Vitals (LCP, INP, CLS), Lighthouse 12, TTFB/FCP, rendering (SSR/SSG/ISR/islands), caching HTTP/CDN, optimización carga, diagnóstico técnico frontend.                                                                        |
| `verify-repo`         | Auditoría integral repositorio e inicio canónico de plan (repo starting): sincroniza clon, tablero estado/roadmap/fallos, contrasta con repo-standard (P0/P1/P2, CI quality→test→smoke, Renovate), corrige tras sí.                                              |
| `verify-architecture` | Verificación arquitectura código: análisis estructura, dependencias, drift arquitectónico, oportunidades refactor. Mapeo dependencias (madge), métricas cuantitativas, detección cambios no intencionados.                                                       |
| `verify-testing`      | Verificación testing y quality assurance: planificación estrategia test, review calidad tests, análisis cobertura, definición métricas testing. Test pyramid, shift-left/shift-right, mantenimiento suite.                                                       |

### operate (6) — Operación, mantenimiento y seguridad de sistemas Linux

| Skill                   | Descripción                                                                                                                                                                                                                                                                                                                  |
| ----------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `operate-lifecycle`     | Orquesta ciclo de vida del trabajo: init-work (inicio plan, repo starting), verify-hooks (Husky) u operate-release (cierre, publicación, post-plan). Enruta: no ejecuta auditorías/hooks/publicaciones.                                                                                                                      |
| `operate-mantenimiento` | Mantenimiento sistematizado Linux: higiene, actualizaciones, ordenado, optimización, sugerencias. Modos graduados (auditoría rápida/completa, rutina, optimización, limpieza) read-only por defecto, validación determinista por riesgo, snapshots reversibles, KPIs salud. Seguridad defensiva NO (→ operate-seguridad).    |
| `operate-release`       | Cierre repositorio GitHub: publicación versión, auditoría CI/CD, cierre trabajo fin de plan (repo ending, merge, ship). Semantic versioning, Keep a Changelog, supply-chain Actions, Husky+e2e+PR+merge-watch post-plan.                                                                                                     |
| `operate-salud-sistema` | Diagnóstico y auditoría salud Linux: health-check, auditoría rápida/completa, fingerprint sistema, scoring salud (0–100), hallazgos P0–P4, diff temporal. CIS/Lynis compliance, onboarding servidores. No ejecución limpieza (→ operate-mantenimiento) ni hardening/forense (→ operate-seguridad).                           |
| `operate-seguridad`     | Seguridad defensiva hosts Linux: postura, forense ligero registros (journald/auditd/auth.log), CVEs, hardening sysctl/SSH, AppArmor/SELinux, auditd, fail2ban. Auditoría seguridad sistema, hardening host, revisión logs auth. No vulnerabilidades código app (→ verify-owasp) ni limpieza disco (→ operate-mantenimiento). |
| `operate-monitoring`    | Orquestación monitoring y observabilidad: configuración métricas (Prometheus/Grafana), tracing (OpenTelemetry/Jaeger), logs (ELK/Loki), alerting (Alertmanager/PagerDuty). Setup alertas, visión salud sistema.                                                                                                              |

### design (2) — Arquitectura y constitución del sistema

| Skill                 | Descripción                                                                                                                                                                                                                          |
| --------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `design-architecture` | Análisis arquitectura codebase: capas, acoplamiento, puntos de profundidad, oportunidades modularización. Mapa módulos, detección dónde acopla código. No security audit (→ verify-owasp) ni diseño general (→ build-design-system). |
| `design-constitution` | Constitución ALIGNUX: marco pasivo identidad, coherencia operativa, límites agente en sistemas Linux. Principios ALIGNUX, alinear respuesta con identidad sistema, validar decisión contra marco constitucional.                     |

## Alias de migración

Nombres antiguos → Nuevos nombres (compatibilidad hacia atrás):

```text
construir-typescript       → build-typescript
construir-upstash          → build-upstash
construir-proton-suite     → build-proton-suite
disenar-arquitectura       → design-architecture
disenar-constitucion       → design-constitution
disenar-design-system      → build-design-system
disenar-interfaz           → build-interface
verificar-*                → verify-* (7 skills)
operar-*                   → operate-* (5 skills)
```

## Skills reclasificadas

Estas skills cambiaron de dominio durante la reorganización:

| Nombre antiguo          | Nombre nuevo          | Nuevo dominio |
| ----------------------- | --------------------- | ------------- |
| `disenar-design-system` | `build-design-system` | build         |
| `disenar-interfaz`      | `build-interface`     | build         |
| `disenar-arquitectura`  | `design-architecture` | design        |
| `disenar-constitucion`  | `design-constitution` | design        |

## Esquema de versiones

- **2.0.0**: Skills reclasificadas (cambio de dominio)
- **1.0.0**: Skills nuevas (addyosmani adaptado)
- **2.3.0**: Skills existentes traducidas (español → inglés, bump versión)

## Añadir nuevas skills

Para añadir una skill, crea directorio bajo el dominio correspondiente:

```bash
mkdir -p skills/<dominio>/<dominio>-<nombre-skill>
```

Incluye `SKILL.md` con frontmatter estándar:

```yaml
---
name: <dominio>-<nombre-skill>
description: >
  Descripción en inglés.
license: MIT
metadata:
  author: "addyosmani (adapted)"
  version: "1.0.0"
  domain: <dominio>
  type: atomic
  language: en
---
```

## Cross-references

Todas las rutas `../../references/` deben resolver. Cada skill tiene directorio `references/` con documentación específica.

## Validación

```bash
node scripts/validate-skills.js
```

Verifica: frontmatter schema, resolución referencias, corrección router, esquema versiones, language="en", domain correcto.
