---
name: protonpass
description: >-
  Obtiene secretos desde Proton Pass vía pass-cli sin pedirlos al usuario ni
  hardcodearlos. Usar cuando haga falta token, password o API key almacenado en
  Proton Pass. No usar para correo (→ email-proton).
license: MIT
metadata:
  author: Soluciones-Alexendros
  version: "1.0.0"
  dominio: integraciones
  idioma: es

---

# Proton Pass — Thin-skill: criterio de enrutado a protonsuite-tools

## Propósito

**Thin-skill**: criterio de enrutado para secretos Proton Pass. La operativa completa (pass-cli, bóvedas, campos) vive en **protonsuite-tools**.

**Cuándo usar esta skill**: para decidir si la petición va a protonsuite-tools (Pass).

## Cuándo usarme / Triggering

Derivar a **protonsuite-tools (Pass)** cuando el usuario pida:
- Leer/buscar/listar secretos (tokens, passwords, API keys) en Proton Pass
- Operar con `pass-cli` (v2.2.0+): list, search, get, insert, edit, generate, login, sync
- Acceder a bóvedas: Personal, Estatal, Finanzas, Infraestructura, Archivo
- Sintaxis URI: `pass://<Bóveda>/<Item>/<campo>`

**NO derivar aquí**: correo Proton Mail (→ `email-proton`), secretos de CI/GitHub (settings remoto).

## Referencias → protonsuite-tools

| Qué necesitas | Enlace a protonsuite-tools (tag v1.4.0) |
|---|---|
| CLI Reference (pass-cli commands) | `docs/mcp-tools/pass.md` |
| Security notes (sesión, env, clipboard) | `docs/bridge-core/security-notes.md` |
| Agent quickstart / deployment | `docs/agent-quickstart.md`, `docs/deployment.md` |

**URL base pinneada**: https://github.com/Soluciones-Alexendros/protonsuite-tools/tree/v1.4.0

> Licencia: protonsuite-tools es AGPL-3.0; este repo es MIT. Solo enlazar, no vendorizar código.

## Uso

Thin-skill: criterio de enrutado a protonsuite-tools (Pass). Ver `description` del frontmatter y tabla de referencias arriba.

## Estructura

- `SKILL.md` — criterio de enrutado y enlaces a protonsuite-tools (canon operativo).
- `references/cli-reference.md`, `references/security-notes.md` — detalle local heredado; el canon vive en protonsuite-tools.

## Referencias

Ver tabla **Referencias → protonsuite-tools** arriba.
