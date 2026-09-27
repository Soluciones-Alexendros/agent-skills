---
name: email-proton
description: >-
  Gestiona correo Proton Mail vía Proton Mail Bridge (IMAP/SMTP local). Usar cuando el
  operador pida leer, enviar o organizar correo Proton. No usar para secretos de Proton Pass
  (→ protonpass).
license: MIT
metadata:
  author: Soluciones-Alexendros
  version: "2.0.0"
  dominio: integraciones
  idioma: es

---
# Email Proton — Thin-skill: criterio de enrutado a protonsuite-tools

## Qué hace / Propósito

**Thin-skill**: criterio de enrutado para correo Proton Mail. La operativa completa (IMAP/SMTP via Bridge, scripts, clasificación) vive en **protonsuite-tools**.

**Cuándo usar esta skill**: para decidir si la petición va a protonsuite-tools (Mail).

## Cuándo usarme / Triggering

Derivar a **protonsuite-tools (Mail)** cuando el usuario pida:
- Leer/buscar/listar correos Proton Mail
- Enviar emails desde Proton
- Clasificar correos por caso/organismo (juzgado, registro, TGSS, notaría, SMAC)
- Marcar leído/no leído, obtener cabeceras completas
- Operar vía Proton Mail Bridge (IMAP 1143 / SMTP 1025 local)

**NO derivar aquí**: secretos/credenciales (→ `protonpass`), otro proveedor de correo.

## Referencias → protonsuite-tools

| Qué necesitas | Enlace a protonsuite-tools (tag v1.5.0) |
|---|---|
| Instalación/configuración Bridge | `docs/bridge-core/setup.md` |
| API Reference (subcomandos CLI) | `docs/bridge-core/api-reference.md` |
| Mail: 14 tools (list, search, fetch, send, mark, folders) | `docs/mcp-tools/mail.md` |
| Agent quickstart / deployment | `docs/agent-quickstart.md`, `docs/deployment.md` |

**URL base pinneada**: https://github.com/Soluciones-Alexendros/protonsuite-tools/tree/v1.5.0

> Licencia: protonsuite-tools es AGPL-3.0; este repo es MIT. Solo enlazar, no vendorizar código.

## MCP tools directos (Mail)

Vía preferente frente a IMAP manual: el servidor MCP de protonsuite-tools expone las operaciones de correo como tools (ver `docs/mcp-tools/mail.md` en el tag pineado). Resumen operativo:

| Tool MCP | Equivale a | Uso típico |
|---|---|---|
| `mail_list` | `unread` / listado INBOX | Listar no leídos con límite |
| `mail_search` | `search` | Búsqueda por remitente/asunto/texto/fecha |
| `mail_fetch` | `fetch` | Cuerpo + cabeceras de un UID |
| `mail_send` | `send` | Enviar texto plano UTF-8 |
| `mail_mark` | `mark` | Marcar leído/no leído |
| `mail_folders` | `folders` | Listar buzones/etiquetas |

Si el entorno no tiene servidor MCP disponible, el fallback es el CLI de protonsuite-tools y, en última instancia, el script legacy `scripts/proton_bridge.py`.

## Novedades 2024-26

Ver `references/protonsuite-2024-2026.md`: Bridge 3.x (qué cambia), `proton-python-sdk` (evaluación: cuándo preferirlo al Bridge IMAP), y matriz de decisión MCP → CLI → script legacy.

## Uso

Thin-skill: criterio de enrutado a protonsuite-tools (Mail). Ver `description` del frontmatter y tabla de referencias arriba.

## Estructura

- `SKILL.md` — criterio de enrutado y enlaces a protonsuite-tools (canon operativo).
- `references/setup.md`, `references/api_reference.md` — detalle local **legacy**; el canon vive en protonsuite-tools.
- `references/protonsuite-2024-2026.md` — Bridge 3.x, `proton-python-sdk`, MCP tools, tooling 2024-26.
- `scripts/proton_bridge.py` — CLI IMAP/SMTP **legacy: funcional pero deprecado**; el canon vive en protonsuite-tools. Se mantiene con tests en verde; no añadir features.

## Referencias

Ver tabla **Referencias → protonsuite-tools** arriba y `references/protonsuite-2024-2026.md`.
