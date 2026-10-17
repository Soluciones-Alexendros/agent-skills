# autoworkspace

Workspace agéntico de Soluciones-Alexendros (MIT): no es una vitrina de skills, sino un pipeline preprogramado con variables por proyecto — especificación → esquemas/tests → código → validación → integración → status declarativo versionado.

19 skills en 5 dominios (`plan`, `system`, `project`, `web`, `role`). Nombres y contenido de skills en inglés; conversaciones en español.

**Deps:** version-updates vía [Renovate](.github/renovate.json) (Dependabot Alerts de seguridad pueden quedar ON). App Renovate en la org es prerrequisito humano.

## Inicio rápido

```bash
git clone https://github.com/Soluciones-Alexendros/autoworkspace.git
cp -r autoworkspace/skills/<nombre-de-la-skill> ~/.agents/skills/
```

## Configuración en OpenCode (harness principal)

OpenCode es el harness principal: no necesita sistema de plugins, solo `AGENTS.md` + `opencode.json` (`skillDirectories`). El agente evalúa cada petición y la asigna a una skill según su descripción y palabras clave.

```bash
git clone https://github.com/Soluciones-Alexendros/autoworkspace.git
cd autoworkspace
bash scripts/install.sh            # global: ~/.config/opencode/skills, ~/.agents/skills, ~/.codex/skills, ~/.cursor/skills
bash scripts/install-opencode.sh   # local al proyecto: .opencode/skills + .agents/skills
```

Comprueba el enrutado con:

```bash
python tools/skill-router/route.py "limpia mi sistema Arch" --top 3
python tools/workspace-router/run.py --phase DEFINE --repo . --json
```

Plantillas de proyecto: `templates/autoworkspace/` → copiar a `<repo>/.autoworkspace/`.

Consulta `docs/harness-integration.md` (tabla multi-harness), `docs/opencode-setup.md` y `docs/routing.md`.

## Skills por dominio

19 skills repartidas en 5 dominios (`plan`, `system`, `project`, `web`, `role`).

### plan (3) — Cómo se decide el trabajo

| Skill                | Descripción                                                                                                                                                                                                                                                |
| -------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `plan-specification` | Especificación estructurada antes del código y desglose en tareas verificables con criterios de aceptación. Flujo Spec → Plan → Tareas → Implementación. Úsala al acotar trabajo de varios pasos. No para arreglos triviales de una línea.                 |
| `plan-continue`      | Continúa según el roadmap previsto; si no hay, analiza el estado del repo (repo starting) y razona los próximos pasos. Cita documentación oficial cuando el stack importa. Úsala al preguntar por dónde empezar. No para publicar (ver `project-publish`). |
| `plan-validation`    | Ciclo TDD rojo-verde-refactor: primero el test que falla, hazlo pasar, refactoriza. Para bugs, reproduce con un test primero. Úsala al corregir bugs o añadir comportamiento. No para prototipos exploratorios.                                            |

### system (4) — Entorno y SO local

| Skill                | Descripción                                                                                                                                                                                                                                                                             |
| -------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `system-health`      | Diagnóstico de salud de Linux: health checks, auditorías rápida y completa, huella del sistema, puntuación de salud 0–100. Úsala al evaluar una máquina. No para ejecutar limpieza (ver `system-maintenance`) ni hardening (ver `system-security`).                                     |
| `system-maintenance` | Mantenimiento sistematizado de Linux: higiene, actualizaciones, limpieza y optimización. Modos graduados, solo lectura por defecto, ejecución con puertas de riesgo y snapshots reversibles. Úsala al limpiar o ajustar un equipo. No para seguridad defensiva (ver `system-security`). |
| `system-security`    | Seguridad defensiva del host Linux: postura, forense ligero de logs, CVEs, hardening de sysctl y SSH, AppArmor/SELinux, auditd y fail2ban. Úsala al auditar o endurecer un host. No para fallos de código de aplicación (ver `web-owasp`).                                              |
| `system-proton`      | Proton Mail (Bridge IMAP/SMTP local, MCP Mail) y Proton Pass (pass-cli JSON, MCP Pass). Lee, busca y clasifica correo; obtén secretos; envía email. Úsala al trabajar con Proton. No para otros proveedores de correo.                                                                  |

### project (5) — Repo estático: docs, config, versionado, calidad local

| Skill                  | Descripción                                                                                                                                                                                                                                                                                                          |
| ---------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `project-architecture` | Verificación de arquitectura de código: análisis de estructura, mapeo de dependencias, detección de desviaciones, oportunidades de refactor. Úsala al revisar arquitectura. No para revisión de seguridad (ver `web-owasp`).                                                                                         |
| `project-hooks`        | Hooks locales de git: Husky, lint-staged, Prettier, typecheck y tests en el commit; e2e en el push si existen. Úsala al poner puertas de calidad locales. No para CI remota (ver `project-publish`).                                                                                                                 |
| `project-libraries`    | Auditoría de dependencias (SCA/CVE): pipeline multi-lenguaje (npm, pip, cargo, go, maven, gradle, composer, gem) para vulnerabilidades, malware, typosquatting y dependencias sin usar o desactualizadas. Genera SBOM. Úsala al escanear la cadena de suministro. No para fallos de código propio (ver `web-owasp`). |
| `project-publish`      | Cierre de repo en GitHub: publicación de versiones, auditoría CI/CD y cierre post-plan. Versionado semántico, changelog y cadena de suministro de Actions. Úsala al publicar. No para el inicio de plan (ver `plan-continue`).                                                                                       |
| `project-testing`      | Verificación de pruebas y QA: estrategia de tests, revisión de su calidad, análisis de cobertura y métricas. Úsala al evaluar una suite. No para escribir los tests en sí (ver `plan-validation`).                                                                                                                   |

### web (3) — Comportamiento del proyecto desplegado

| Skill             | Descripción                                                                                                                                                                                                                                                              |
| ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `web-compliance`  | Auditoría de cumplimiento web: accesibilidad (WCAG 2.2 AA), legal (RGPD, consentimiento, cookies), SEO on-page y off-page. Matriz PASS/FAIL, puntuación ponderada, plan de remediación RICE. Úsala al auditar cumplimiento. No para rendimiento (ver `web-performance`). |
| `web-owasp`       | Revisión de seguridad de código (OWASP): inyección, XSS, autenticación/autorización, criptografía, SSRF, secretos y mala configuración. Úsala al buscar vulnerabilidades en el código. No para hardening del host (ver `system-security`).                               |
| `web-performance` | Auditoría de rendimiento web: Core Web Vitals, Lighthouse, TTFB/FCP, modos de renderizado, caché HTTP y CDN, optimización de carga. Úsala al diagnosticar lentitud. No para cumplimiento (ver `web-compliance`).                                                         |

### role (4) — Agentes especialistas de implementación

| Skill             | Descripción                                                                                                                                                                                                                                                                                                                                  |
| ----------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `role-front`      | Especialista frontend: estabilidad, compatibilidad, coherencia de estado y contratos de comunicación cliente-servidor. Úsala al implementar o corregir UI y flujos. No para dirección visual (ver `role-design`) ni auditorías (ver `web-*`).                                                                                                |
| `role-back`       | Especialista backend: datos en reposo y en movimiento, rutas, despliegue, robustez y seguridad de aplicación. Patrones de caché/KV, colas, rate limit, blobs y búsqueda (Upstash u otros proveedores). Úsala al implementar APIs y persistencia.                                                                                             |
| `role-clean-code` | Especialista Clean Code: escritura legible y refactor seguro en cualquier lenguaje, con nombres expresivos, funciones cohesionadas, menos duplicación y pasos pequeños verificados. Úsala al aplicar código limpio o refactorizar. No para auditoría arquitectónica (ver `project-architecture`) ni revisión de seguridad (ver `web-owasp`). |
| `role-design`     | Especialista UI/UX: dirección visual, tipografía, paleta, motion, CSS limpio, tokens DTCG y Tailwind v4. Úsala al diseñar interfaces o un design system. No para lógica de aplicación (ver `role-front`) ni a11y/SEO (ver `web-compliance`).                                                                                                 |

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
  Qué hace. Use when the operator requests it. Not for other families.
license: MIT
compatibility: "opencode, codex, cursor, copilot"
allowed-tools: "Read, Grep, Glob, Bash, Write"
metadata:
  author: Soluciones-Alexendros
  version: 1.0.0
  domain: plan
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
