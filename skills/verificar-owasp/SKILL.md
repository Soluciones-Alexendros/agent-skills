---
name: verificar-owasp
description: >-
  Revisión de seguridad de código (OWASP): inyección, XSS, authn/authz, criptografía, SSRF,
  secretos y misconfiguración. Usar cuando el operador pida security review, OWASP o
  buscar vulnerabilidades en este código. No usar para hardening del SO (→
  operar-seguridad) ni cierre de release (→ operar-release) ni auditoría de
  dependencias/SCA (→ verificar-dependencias).
license: MIT
metadata:
  author: Soluciones-Alexendros
  version: "2.2.0"
  dominio: verificar
  tipo: atomic
  idioma: es
---

<!--
Reference material based on OWASP Cheat Sheet Series (CC BY-SA 4.0)
https://cheatsheetseries.owasp.org/
-->

# verificar-owasp — Revisión de seguridad de código (OWASP)

## Propósito

Identificar vulnerabilidades explotables en código. Informar solo hallazgos de **alta confianza**: patrón vulnerable con entrada controlada por el atacante, tras investigar el codebase.

## Cuándo usar

Security review, OWASP, buscar vulnerabilidades, o revisar un diff/endpoint/plantilla/configuración antes de desplegar.

## Alcance

Informar sobre el fichero, diff o código que entrega el operador. Investigar en todo el codebase para ganar confianza. No informar por coincidencia de patrón.

| Nivel  | Criterio                                            | Acción                      |
| ------ | --------------------------------------------------- | --------------------------- |
| HIGH   | Patrón vulnerable + entrada del atacante confirmada | Informar                    |
| MEDIUM | Patrón vulnerable, origen sin aclarar               | Anotar «Needs verification» |
| LOW    | Teórico o defensa en profundidad                    | No informar                 |

No marcar: tests (salvo petición), código muerto, constantes o config de servidor, rutas que exigen auth previa (anotar el requisito). No marcar `settings.X`, `os.environ`, ficheros de config ni URLs internas de despliegue como SSRF. Frameworks que auto-escapan (Django `{{ var }}`, React `{var}`) solo se marcan con `|safe`, `dangerouslySetInnerHTML` o equivalentes. ORM parametrizado no es inyección; `.raw()` interpolado sí.

## Procedimiento

1. Detectar contexto (API, plantillas, ficheros, cripto, serialización, SSRF, negocio, GraphQL/REST, config, errores, logs) y cargar solo las referencias de esa fila.
2. Cargar guía de lenguaje: `references/languages-python.md` o `references/languages-javascript.md`. Go/Rust/Java: aplicar references por vulnerabilidad.
3. Infraestructura: `references/infrastructure-docker.md` para Dockerfile; resto → `references/misconfiguration.md`.
4. Trazar el flujo de datos. Confirmar explotabilidad. Informar solo HIGH.
5. Patrones inmediatos: `references/quick-patterns.md`. Hardening de aplicación: `references/hardening-source.md`.

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
- **Issue**: ...
- **Impact**: ...
- **Evidence**: (snippet)
- **Fix**: ...

### Needs Verification

#### [VERIFY-001] [Potential Issue]

- **Location**: `file.py:456`
- **Question**: ...
```

Si no hay hallazgos HIGH: «No high-confidence vulnerabilities identified.»

Severidad: Critical (RCE, SQLi a datos, bypass de auth, secretos hardcodeados) / High / Medium / Low.

## Referencias

| Fichero                               | Cubre                               |
| ------------------------------------- | ----------------------------------- |
| `references/injection.md`             | SQL, NoSQL, OS, LDAP, plantillas    |
| `references/xss.md`                   | Reflejado, almacenado, DOM          |
| `references/authorization.md`         | IDOR, escalada                      |
| `references/authentication.md`        | Sesiones, credenciales              |
| `references/cryptography.md`          | Algoritmos, claves                  |
| `references/deserialization.md`       | Pickle, YAML, Java, PHP             |
| `references/file-security.md`         | Path traversal, subidas, XXE        |
| `references/ssrf.md`                  | SSRF                                |
| `references/csrf.md`                  | CSRF                                |
| `references/data-protection.md`       | Secretos, PII, logging              |
| `references/api-security.md`          | REST, GraphQL, mass assignment      |
| `references/business-logic.md`        | Race, bypass de flujo               |
| `references/modern-threats.md`        | Prototype pollution, LLM, WebSocket |
| `references/misconfiguration.md`      | Cabeceras, CORS, debug              |
| `references/error-handling.md`        | Fail-open, info leak                |
| `references/logging.md`               | Auditoría, inyección de logs        |
| `references/languages-python.md`      | Django, Flask, FastAPI              |
| `references/languages-javascript.md`  | Node, Express, React, Vue, Next     |
| `references/infrastructure-docker.md` | Contenedores                        |
| `references/quick-patterns.md`        | FLAG/SAFE/CHECK                     |
| `references/hardening-source.md`      | Endurecimiento de código            |
| `references/security-checklist.md`    | Checklist operativo                 |
