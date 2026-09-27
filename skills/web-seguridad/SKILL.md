---
name: web-seguridad
description: >-
  Revisión de seguridad de código (OWASP): inyección, XSS, authn/authz, criptografía, SSRF,
  secretos y misconfiguración. Usar ante security review, OWASP o 'busca vulnerabilidades en
  este código'. No usar para hardening del SO (→ linux-seguridad) ni cierre de release (→
  repo-ending).
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

## Scope: Research vs. Reporting

**CRITICAL DISTINCTION:**

- **Report on**: Only the specific file, diff, or code provided by the user
- **Research**: The ENTIRE codebase to build confidence before reporting

Before flagging any issue, you MUST research the codebase to understand:
- Where does this input actually come from? (Trace data flow)
- Is there validation/sanitization elsewhere?
- How is this configured? (Check settings, config files, middleware)
- What framework protections exist?

**Do NOT report issues based solely on pattern matching.** Investigate first, then report only what you're confident is exploitable.

## Confidence Levels

| Level | Criteria | Action |
|-------|----------|--------|
| **HIGH** | Vulnerable pattern + attacker-controlled input confirmed | **Report** with severity |
| **MEDIUM** | Vulnerable pattern, input source unclear | **Note** as "Needs verification" |
| **LOW** | Theoretical, best practice, defense-in-depth | **Do not report** |

## Do Not Flag

### General Rules
- Test files (unless explicitly reviewing test security)
- Dead code, commented code, documentation strings
- Patterns using **constants** or **server-controlled configuration**
- Code paths that require prior authentication to reach (note the auth requirement instead)

### Server-Controlled Values (NOT Attacker-Controlled)

These are configured by operators, not controlled by attackers:

| Source | Example | Why It's Safe |
|--------|---------|---------------|
| Django settings | `settings.API_URL`, `settings.ALLOWED_HOSTS` | Set via config/env at deployment |
| Environment variables | `os.environ.get('DATABASE_URL')` | Deployment configuration |
| Config files | `config.yaml`, `app.config['KEY']` | Server-side files |
| Framework constants | `django.conf.settings.*` | Not user-modifiable |
| Hardcoded values | `BASE_URL = "https://api.internal"` | Compile-time constants |

**SSRF Example - NOT a vulnerability:**
```python
# SAFE: URL comes from Django settings (server-controlled)
response = requests.get(f"{settings.SEER_AUTOFIX_URL}{path}")
```

**SSRF Example - IS a vulnerability:**
```python
# VULNERABLE: URL comes from request (attacker-controlled)
response = requests.get(request.GET.get('url'))
```

### Framework-Mitigated Patterns
Check language guides before flagging. Common false positives:

| Pattern | Why It's Usually Safe |
|---------|----------------------|
| Django `{{ variable }}` | Auto-escaped by default |
| React `{variable}` | Auto-escaped by default |
| Vue `{{ variable }}` | Auto-escaped by default |
| `User.objects.filter(id=input)` | ORM parameterizes queries |
| `cursor.execute("...%s", (input,))` | Parameterized query |
| `innerHTML = "<b>Loading...</b>"` | Constant string, no user input |

**Only flag these when:**
- Django: `{{ var|safe }}`, `{% autoescape off %}`, `mark_safe(user_input)`
- React: `dangerouslySetInnerHTML={{__html: userInput}}`
- Vue: `v-html="userInput"`
- ORM: `.raw()`, `.extra()`, `RawSQL()` with string interpolation

## Review Process

### 1. Detect Context

What type of code am I reviewing?

| Code Type | Load These References |
|-----------|----------------------|
| API endpoints, routes | `authorization.md`, `authentication.md`, `injection.md` |
| Frontend, templates | `xss.md`, `csrf.md` |
| File handling, uploads | `file-security.md` |
| Crypto, secrets, tokens | `cryptography.md`, `data-protection.md` |
| Data serialization | `deserialization.md` |
| External requests | `ssrf.md` |
| Business workflows | `business-logic.md` |
| GraphQL, REST design | `api-security.md` |
| Config, headers, CORS | `misconfiguration.md` |
| CI/CD, dependencies | `supply-chain.md` |
| Error handling | `error-handling.md` |
| Audit, logging | `logging.md` |

### 2. Load Language Guide

Based on file extension or imports:

| Indicators | Guide |
|------------|-------|
| `.py`, `django`, `flask`, `fastapi` | `references/languages-python.md` |
| `.js`, `.ts`, `express`, `react`, `vue`, `next` | `references/languages-javascript.md` |
| `.go`, `.rs`, `.java`, `go.mod`, `Cargo.toml`, Spring | Sin guía propia en esta distribución: aplicar los references por vulnerabilidad |

### 3. Load Infrastructure Guide (if applicable)

| File Type | Guide |
|-----------|-------|
| `Dockerfile`, `.dockerignore` | `references/infrastructure-docker.md` |
| K8s, Terraform, GitHub Actions, `.gitlab-ci.yml`, cloud/IAM | Sin guía propia en esta distribución: aplicar `references/supply-chain.md` y `references/misconfiguration.md` |

### 4. Research Before Flagging

**For each potential issue, research the codebase to build confidence:**

- Where does this value actually come from? Trace the data flow.
- Is it configured at deployment (settings, env vars) or from user input?
- Is there validation, sanitization, or allowlisting elsewhere?
- What framework protections apply?

Only report issues where you have HIGH confidence after understanding the broader context.

### 5. Verify Exploitability

For each potential finding, confirm:

**Is the input attacker-controlled?**

| Attacker-Controlled (Investigate) | Server-Controlled (Usually Safe) |
|-----------------------------------|----------------------------------|
| `request.GET`, `request.POST`, `request.args` | `settings.X`, `app.config['X']` |
| `request.json`, `request.data`, `request.body` | `os.environ.get('X')` |
| `request.headers` (most headers) | Hardcoded constants |
| `request.cookies` (unsigned) | Internal service URLs from config |
| URL path segments: `/users/<id>/` | Database content from admin/system |
| File uploads (content and names) | Signed session data |
| Database content from other users | Framework settings |
| WebSocket messages | |

**Does the framework mitigate this?**
- Check language guide for auto-escaping, parameterization
- Check for middleware/decorators that sanitize

**Is there validation upstream?**
- Input validation before this code
- Sanitization libraries (DOMPurify, bleach, etc.)

### 6. Report HIGH Confidence Only

Skip theoretical issues. Report only what you've confirmed is exploitable after research.

---

## Severity Classification

| Severity | Impact | Examples |
|----------|--------|----------|
| **Critical** | Direct exploit, severe impact, no auth required | RCE, SQL injection to data, auth bypass, hardcoded secrets |
| **High** | Exploitable with conditions, significant impact | Stored XSS, SSRF to metadata, IDOR to sensitive data |
| **Medium** | Specific conditions required, moderate impact | Reflected XSS, CSRF on state-changing actions, path traversal |
| **Low** | Defense-in-depth, minimal direct impact | Missing headers, verbose errors, weak algorithms in non-critical context |

---

## Quick Patterns Reference

Patrones de código que deben marcarse inmediatamente durante la revisión. Se organizan en: **Always Flag (Critical)** — `eval`/`exec`/`pickle`/`yaml.load`/`unserialize`/`shell=True`; **Always Flag (High)** — DOM XSS, SQL injection, command injection; **Always Flag (Secrets)** — hardcoded passwords, API keys, private keys; **Check Context First** — SSRF, path traversal, open redirect y weak crypto (depende de si la entrada es del usuario o de configuración).

> Ver [references/quick-patterns.md](references/quick-patterns.md) para la lista completa de patrones con ejemplos de código y criterios FLAG/SAFE/CHECK.

---

## Output Format

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
- **Issue**: [What the vulnerability is]
- **Impact**: [What an attacker could do]
- **Evidence**:
  ```python
  [Vulnerable code snippet]
  ```
- **Fix**: [How to remediate]

### Needs Verification

#### [VERIFY-001] [Potential Issue]
- **Location**: `file.py:456`
- **Question**: [What needs to be verified]
```

If no vulnerabilities found, state: "No high-confidence vulnerabilities identified."

---

## Reference Files

### Core Vulnerabilities (`references/`)
| File | Covers |
|------|--------|
| `injection.md` | SQL, NoSQL, OS command, LDAP, template injection |
| `xss.md` | Reflected, stored, DOM-based XSS |
| `authorization.md` | Authorization, IDOR, privilege escalation |
| `authentication.md` | Sessions, credentials, password storage |
| `cryptography.md` | Algorithms, key management, randomness |
| `deserialization.md` | Pickle, YAML, Java, PHP deserialization |
| `file-security.md` | Path traversal, uploads, XXE |
| `ssrf.md` | Server-side request forgery |
| `csrf.md` | Cross-site request forgery |
| `data-protection.md` | Secrets exposure, PII, logging |
| `api-security.md` | REST, GraphQL, mass assignment |
| `business-logic.md` | Race conditions, workflow bypass |
| `modern-threats.md` | Prototype pollution, LLM injection, WebSocket |
| `misconfiguration.md` | Headers, CORS, debug mode, defaults |
| `error-handling.md` | Fail-open, information disclosure |
| `supply-chain.md` | Dependencies, build security |
| `logging.md` | Audit failures, log injection |

### Language Guides (`languages/`)
- `python.md` - Django, Flask, FastAPI patterns
- `javascript.md` - Node, Express, React, Vue, Next.js
- Go, Rust y Java: sin guía específica incluida en esta distribución

### Infrastructure (`infrastructure/`)
- `docker.md` - Container security
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
