---
name: protonpass
description: >-
  Obtiene secretos desde Proton Pass vía pass-cli sin pedirlos al usuario ni
  hardcodearlos. Usar cuando haga falta token, password o API key almacenado en
  Proton Pass. No usar para correo (→ email-proton).
license: MIT
metadata:
  author: Soluciones-Alexendros
  version: "2.0.0"
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
- Operar con `pass-cli` (v2.3+): list, search, get, insert, edit, generate, login, sync
- Acceder a bóvedas: Personal, Estatal, Finanzas, Infraestructura, Archivo
- Sintaxis URI: `pass://<Bóveda>/<Item>/<campo>`

**NO derivar aquí**: correo Proton Mail (→ `email-proton`), secretos de CI/GitHub (settings remoto).

## Referencias → protonsuite-tools

| Qué necesitas | Enlace a protonsuite-tools (tag v1.5.0) |
|---|---|
| CLI Reference (pass-cli commands) | `docs/mcp-tools/pass.md` |
| Security notes (sesión, env, clipboard) | `docs/bridge-core/security-notes.md` |
| Agent quickstart / deployment | `docs/agent-quickstart.md`, `docs/deployment.md` |

**URL base pinneada**: https://github.com/Soluciones-Alexendros/protonsuite-tools/tree/v1.5.0

> Licencia: protonsuite-tools es AGPL-3.0; este repo es MIT. Solo enlazar, no vendorizar código.

## MCP tools directos (Pass)

Vía preferente frente a `pass-cli` manual: el servidor MCP de protonsuite-tools expone los secretos como tools (ver `docs/mcp-tools/pass.md` en el tag pineado). Resumen operativo:

| Tool MCP | Equivale a | Uso típico |
|---|---|---|
| `pass_list` | `pass-cli list` | Localizar el item en su bóveda |
| `pass_show` | `pass-cli show --field` | Obtener un campo sin volcar el resto |
| `pass_search` | búsqueda de items | Buscar por nombre across-bóvedas |
| `pass_generate` | `pass-cli generate` | Generar contraseña aleatoria |

Reglas: pedir siempre el campo concreto (nunca volcar el item entero), no dejar secretos en logs ni en código, e inyectarlos por variable de entorno en el proceso destino.

## pass-cli v2.3+: salida JSON

Desde v2.3 `pass-cli` emite JSON estructurado (`--json` / `--output json` según subcomando; ver `docs/mcp-tools/pass.md` del tag pineado para la flag exacta). El agente debe preferir JSON sobre parseo de texto:

```bash
pass-cli login                                   # flujo web, idempotente
pass-cli sync                                    # datos frescos
pass-cli list --vault Personal                   # localizar item
PASS_JSON=$(pass-cli show 'Personal/app.com' --field password)  # un campo, sin volcar
```

Ver `references/cli-reference.md` (legacy local) y `references/protonsuite-2024-2026.md` (novedades 2024-26).

## Uso

Thin-skill: criterio de enrutado a protonsuite-tools (Pass). Ver `description` del frontmatter y tabla de referencias arriba.

## Estructura

- `SKILL.md` — criterio de enrutado y enlaces a protonsuite-tools (canon operativo).
- `references/cli-reference.md`, `references/security-notes.md` — detalle local **legacy**; el canon vive en protonsuite-tools.
- `references/protonsuite-2024-2026.md` — pass-cli v2.3+ (JSON), MCP tools de Pass, tooling 2024-26.

## Referencias

Ver tabla **Referencias → protonsuite-tools** arriba y `references/protonsuite-2024-2026.md`.
