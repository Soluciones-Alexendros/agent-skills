---
name: web-seguridad
description: >-
  Revisión de seguridad de código (OWASP): inyección, XSS, authn/authz, criptografía, SSRF,
  secretos y misconfiguración. Usar ante security review, OWASP o 'busca vulnerabilidades en
  este código'. No usar para hardening del SO (→ linux-seguridad) ni cierre de release (→
  repo-release).
license: MIT
metadata:
  author: Soluciones-Alexendros
  version: "1.0.0"
  dominio: web
  idioma: es

---
<!--
Reference material based on OWASP Cheat Sheet Series (CC BY-SA 4.0)
https://cheatsheetseries.owasp.org/
-->

# Web Seguridad — Revisión de seguridad de código y dependencias (OWASP)

Identify exploitable security vulnerabilities in code. Report only **HIGH CONFIDENCE** findings—clear vulnerable patterns with attacker-controlled input.

## Qué hace / Propósito

Revisa código en busca de vulnerabilidades explotables y reporta únicamente hallazgos de alta confianza: patrones vulnerables con entrada controlada por el atacante tras investigar todo el codebase. Aporta un proceso sistemático, niveles de confianza, clasificación de severidad y un formato de informe reproducible.

## Cuándo usarme / Triggering

- Cuando se pida "security review", "find vulnerabilities", "audit security", "check for security issues" u "OWASP review".
- Al revisar código por inyección, XSS, autenticación, autorización, criptografía, CSRF, SSRF, deserialización o exposición de secretos.
- Al analizar un diff, endpoint, plantilla, configuración, dependencia o pipeline antes de desplegar.
- **NO usar cuando**: el objetivo sea hardening, forense de logs, CVEs del sistema o AppArmor de una máquina Linux (usar `linux-seguridad`); esta skill revisa código, no sistemas operativos.

## Referencias internas

Carga solo las referencias que correspondan al tipo de código revisado (ver "Detect Context" más abajo):

- `references/injection.md` — inyección SQL, NoSQL, de comandos OS, LDAP y de plantillas.
- `references/xss.md` — XSS reflejado, almacenado y basado en DOM.
- `references/authorization.md` — control de acceso, IDOR y escalada de privilegios.
- `references/authentication.md` — sesiones, credenciales y almacenamiento de contraseñas.
- `references/cryptography.md` — algoritmos, gestión de claves y aleatoriedad.
- `references/deserialization.md` — deserialización insegura (pickle, YAML, Java, PHP).
- `references/file-security.md` — path traversal, subida de ficheros y XXE.
- `references/ssrf.md` — server-side request forgery.
- `references/csrf.md` — cross-site request forgery.
- `references/data-protection.md` — exposición de secretos, PII y logging.
- `references/api-security.md` — REST, GraphQL y mass assignment.
- `references/business-logic.md` — race conditions y bypass de flujos de negocio.
- `references/modern-threats.md` — prototype pollution, inyección en LLM y WebSocket.
- `references/misconfiguration.md` — cabeceras, CORS, modo debug y valores por defecto.
- `references/error-handling.md` — fail-open y divulgación de información.
- `references/supply-chain.md` — dependencias y seguridad del build.
- `references/logging.md` — fallos de auditoría e inyección de logs.
- `references/languages-python.md` — patrones de Django, Flask y FastAPI.
- `references/languages-javascript.md` — patrones de Node, Express, React, Vue y Next.js.
- `references/infrastructure-docker.md` — seguridad de contenedores y Dockerfile.

## Alcance: investigación vs. informe

**DISTINCIÓN CRÍTICA:**

- **Informa sobre**: solo el fichero, diff o código concreto que entrega el usuario
- **Investiga en**: TODO el codebase para ganar confianza antes de informar

Antes de marcar cualquier hallazgo, DEBES investigar el codebase para entender:
- ¿De dónde viene realmente esta entrada? (traza el flujo de datos)
- ¿Hay validación/sanitización en otro punto?
- ¿Cómo está configurado? (revisa settings, ficheros de configuración, middleware)
- ¿Qué protecciones aporta el framework?

**NO informes de hallazgos basándote solo en coincidencia de patrones.** Investiga primero e informa solo de lo que estés seguro de que es explotable.

## Niveles de confianza

| Nivel | Criterio | Acción |
|-------|----------|--------|
| **HIGH** | Patrón vulnerable + entrada controlada por el atacante confirmada | **Informar** con severidad |
| **MEDIUM** | Patrón vulnerable, origen de la entrada sin aclarar | **Anotar** como «Needs verification» |
| **LOW** | Teórico, buena práctica, defensa en profundidad | **No informar** |

## No marcar

### Reglas generales
- Ficheros de tests (salvo que se revise explícitamente la seguridad de los tests)
- Código muerto, código comentado, docstrings
- Patrones que usan **constantes** o **configuración controlada por el servidor**
- Rutas de código que exigen autenticación previa para alcanzarse (anota el requisito de auth en su lugar)

### Valores controlados por el servidor (NO controlados por el atacante)

Los configuran los operadores, no los controlan los atacantes:

| Origen | Ejemplo | Por qué es seguro |
|--------|---------|-------------------|
| Django settings | `settings.API_URL`, `settings.ALLOWED_HOSTS` | Se fijan vía config/env en el despliegue |
| Variables de entorno | `os.environ.get('DATABASE_URL')` | Configuración de despliegue |
| Ficheros de configuración | `config.yaml`, `app.config['KEY']` | Ficheros del lado servidor |
| Constantes del framework | `django.conf.settings.*` | No modificables por el usuario |
| Valores hardcodeados | `BASE_URL = "https://api.internal"` | Constantes en tiempo de compilación |

**Ejemplo SSRF: NO es vulnerabilidad:**
```python
# SAFE: URL comes from Django settings (server-controlled)
response = requests.get(f"{settings.SEER_AUTOFIX_URL}{path}")
```

**Ejemplo SSRF: SÍ es vulnerabilidad:**
```python
# VULNERABLE: URL comes from request (attacker-controlled)
response = requests.get(request.GET.get('url'))
```

### Patrones mitigados por el framework
Consulta las guías de lenguaje antes de marcar. Falsos positivos habituales:

| Patrón | Por qué suele ser seguro |
|---------|----------------------|
| Django `{{ variable }}` | Auto-escaped por defecto |
| React `{variable}` | Auto-escaped por defecto |
| Vue `{{ variable }}` | Auto-escaped por defecto |
| `User.objects.filter(id=input)` | El ORM parametriza las queries |
| `cursor.execute("...%s", (input,))` | Query parametrizada |
| `innerHTML = "<b>Loading...</b>"` | String constante, sin entrada de usuario |

**Marca estos solo cuando:**
- Django: `{{ var|safe }}`, `{% autoescape off %}`, `mark_safe(user_input)`
- React: `dangerouslySetInnerHTML={{__html: userInput}}`
- Vue: `v-html="userInput"`
- ORM: `.raw()`, `.extra()`, `RawSQL()` con interpolación de strings

## Proceso de revisión

### 1. Detectar el contexto

¿Qué tipo de código estoy revisando?

| Tipo de código | References a cargar |
|-----------|----------------------|
| Endpoints API, rutas | `authorization.md`, `authentication.md`, `injection.md` |
| Frontend, plantillas | `xss.md`, `csrf.md` |
| Manejo de ficheros, subidas | `file-security.md` |
| Cripto, secretos, tokens | `cryptography.md`, `data-protection.md` |
| Serialización de datos | `deserialization.md` |
| Peticiones externas | `ssrf.md` |
| Flujos de negocio | `business-logic.md` |
| Diseño GraphQL, REST | `api-security.md` |
| Config, cabeceras, CORS | `misconfiguration.md` |
| CI/CD, dependencias | `supply-chain.md` |
| Manejo de errores | `error-handling.md` |
| Auditoría, logging | `logging.md` |

### 2. Cargar la guía de lenguaje

Según la extensión del fichero o los imports:

| Indicadores | Guía |
|------------|-------|
| `.py`, `django`, `flask`, `fastapi` | `references/languages-python.md` |
| `.js`, `.ts`, `express`, `react`, `vue`, `next` | `references/languages-javascript.md` |
| `.go`, `.rs`, `.java`, `go.mod`, `Cargo.toml`, Spring | Sin guía propia en esta distribución: aplicar los references por vulnerabilidad |

### 3. Cargar la guía de infraestructura (si aplica)

| Tipo de fichero | Guía |
|-----------|-------|
| `Dockerfile`, `.dockerignore` | `references/infrastructure-docker.md` |
| K8s, Terraform, GitHub Actions, `.gitlab-ci.yml`, cloud/IAM | Sin guía propia en esta distribución: aplicar `references/supply-chain.md` y `references/misconfiguration.md` |

### 4. Investigar antes de marcar

**Ante cada posible hallazgo, investiga el codebase para ganar confianza:**

- ¿De dónde viene realmente este valor? Traza el flujo de datos.
- ¿Se configura en el despliegue (settings, env vars) o viene de la entrada del usuario?
- ¿Hay validación, sanitización o allowlisting en otro punto?
- ¿Qué protecciones del framework aplican?

Informa solo de hallazgos con confianza HIGH tras entender el contexto general.

### 5. Verificar la explotabilidad

Para cada posible hallazgo, confirma:

**¿La entrada está controlada por el atacante?**

| Controlada por el atacante (investigar) | Controlada por el servidor (suele ser segura) |
|-----------------------------------|----------------------------------|
| `request.GET`, `request.POST`, `request.args` | `settings.X`, `app.config['X']` |
| `request.json`, `request.data`, `request.body` | `os.environ.get('X')` |
| `request.headers` (la mayoría de cabeceras) | Constantes hardcodeadas |
| `request.cookies` (sin firmar) | URLs de servicios internos desde config |
| Segmentos de la URL: `/users/<id>/` | Contenido de BD creado por admin/sistema |
| Subidas de ficheros (contenido y nombres) | Datos de sesión firmados |
| Contenido de BD creado por otros usuarios | Settings del framework |
| Mensajes WebSocket | |

**¿Lo mitiga el framework?**
- Consulta la guía de lenguaje: auto-escaping, parametrización
- Busca middleware/decoradores que saniticen

**¿Hay validación aguas arriba?**
- Validación de la entrada antes de este código
- Librerías de sanitización (DOMPurify, bleach, etc.)

### 6. Informar solo con confianza HIGH

Omite los hallazgos teóricos. Informa solo de lo que hayas confirmado como explotable tras investigar.

---

## Clasificación de severidad

| Severidad | Impacto | Ejemplos |
|----------|--------|----------|
| **Critical** | Explotación directa, impacto grave, sin auth requerida | RCE, inyección SQL a datos, bypass de auth, secretos hardcodeados |
| **High** | Explotable con condiciones, impacto significativo | XSS almacenado, SSRF a metadatos, IDOR a datos sensibles |
| **Medium** | Requiere condiciones específicas, impacto moderado | XSS reflejado, CSRF en acciones con estado, path traversal |
| **Low** | Defensa en profundidad, impacto directo mínimo | Cabeceras ausentes, errores verbosos, algoritmos débiles en contexto no crítico |

---

## Quick Patterns Reference

Patrones de código que deben marcarse inmediatamente durante la revisión. Se organizan en: **Always Flag (Critical)** — `eval`/`exec`/`pickle`/`yaml.load`/`unserialize`/`shell=True`; **Always Flag (High)** — DOM XSS, SQL injection, command injection; **Always Flag (Secrets)** — hardcoded passwords, API keys, private keys; **Check Context First** — SSRF, path traversal, open redirect y weak crypto (depende de si la entrada es del usuario o de configuración).

> Ver [references/quick-patterns.md](references/quick-patterns.md) para la lista completa de patrones con ejemplos de código y criterios FLAG/SAFE/CHECK.

---

## Formato de salida

```markdown
## Security Review: [File/Component Name]

### Summary
- **Findings**: X (Y Critical, Z High, ...)
- **Risk Level**: Critical/High/Medium/Low
- **Confidence**: High/Mixed

### Findings

#### [VULN-001] [Vulnerability Type] (Severity)
- **Location**: `file.py:123`
- **Confidence**: High
- **Issue**: [Qué vulnerabilidad es]
- **Impact**: [Qué podría hacer un atacante]
- **Evidence**:
  ```python
  [Vulnerable code snippet]
  ```
- **Fix**: [Cómo remediarlo]

### Needs Verification

#### [VERIFY-001] [Potential Issue]
- **Location**: `file.py:456`
- **Question**: [Qué hay que verificar]
```

Si no se encuentran vulnerabilidades, indica: «No high-confidence vulnerabilities identified.» (sin hallazgos de alta confianza).

---

## Ficheros de referencia

### Vulnerabilidades principales (`references/`)
| Fichero | Cubre |
|------|--------|
| `injection.md` | Inyección SQL, NoSQL, de comandos OS, LDAP y de plantillas |
| `xss.md` | XSS reflejado, almacenado y basado en DOM |
| `authorization.md` | Autorización, IDOR, escalada de privilegios |
| `authentication.md` | Sesiones, credenciales, almacenamiento de contraseñas |
| `cryptography.md` | Algoritmos, gestión de claves, aleatoriedad |
| `deserialization.md` | Deserialización Pickle, YAML, Java, PHP |
| `file-security.md` | Path traversal, subidas, XXE |
| `ssrf.md` | Server-side request forgery |
| `csrf.md` | Cross-site request forgery |
| `data-protection.md` | Exposición de secretos, PII, logging |
| `api-security.md` | REST, GraphQL, mass assignment |
| `business-logic.md` | Race conditions, bypass de flujos de negocio |
| `modern-threats.md` | Prototype pollution, inyección en LLM, WebSocket |
| `misconfiguration.md` | Cabeceras, CORS, modo debug, valores por defecto |
| `error-handling.md` | Fail-open, divulgación de información |
| `supply-chain.md` | Dependencias, seguridad del build |
| `logging.md` | Fallos de auditoría, inyección de logs |

### Guías de lenguaje (`languages/`)
- `python.md` — patrones Django, Flask, FastAPI
- `javascript.md` — patrones Node, Express, React, Vue, Next.js
- Go, Rust y Java: sin guía específica incluida en esta distribución

### Infraestructura (`infrastructure/`)
- `docker.md` — seguridad de contenedores
- Kubernetes, Terraform, CI/CD y cloud: sin guía específica incluida en esta distribución

## Auditoría de dependencias (absorbida de dependency-audit)

Pipeline multi-lenguaje (npm/pip/cargo) para detectar vulnerabilidades, malware, typosquatting, dependencias no usadas y outdated. Ver `references/dependency-audit-pipeline.md` (7 etapas) y `references/dependency-audit-ecosystems.md` (detección npm/pip/cargo/go/maven/gradle/composer/gem).

## Hardening de aplicación (absorbido)

Patrones de endurecimiento de código: `references/hardening-source.md`. Combinar con las refs OWASP de esta skill según el tipo de hallazgo.

## Uso

Revisión de seguridad de código: invocar ante security review, OWASP o «busca vulnerabilidades en este código». Investigar todo el codebase pero reportar solo el código entregado, únicamente hallazgos de alta confianza.

## Estructura

- `SKILL.md` — proceso, niveles de confianza, severidad y formato de informe.
- `LICENSE` — extra top-level.
- `references/` — 19 guías OWASP por vulnerabilidad + `hardening-source.md` y `dependency-audit-*.md` (fuentes absorbidas).
- `languages/` — python, javascript (Go/Rust/Java sin guía propia: aplicar references por vulnerabilidad).
- `infrastructure/` — docker (K8s/Terraform/CI sin guía propia: aplicar supply-chain + misconfiguration).
- Sin `scripts/`: skill puramente de revisión.

## Referencias

- Internas: ver «Referencias internas» y «Reference Files» más arriba.
- `references/security-checklist.md`: checklist operativo creado en v0.1.0 (lo cita `references/hardening-source.md`).
