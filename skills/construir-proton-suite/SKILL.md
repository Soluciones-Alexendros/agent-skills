---
name: construir-proton-suite
description: >-
  Correo Proton Mail (Proton Mail Bridge IMAP/SMTP local, MCP Mail) y secretos Proton Pass
  (pass-cli v2.3+ con salida JSON estable, MCP Pass). Usar para leer, buscar, enviar o
  clasificar correo Proton, o para obtener tokens, passwords y API keys almacenados en
  Proton Pass sin pedirlos al usuario ni hardcodearlos. No usar para otros proveedores de
  correo ni para secretos de CI/GitHub.
license: MIT
metadata:
  author: Soluciones-Alexendros
  version: "1.0.0"
  dominio: construir
  idioma: es

---
# construir-proton-suite — Correo Proton Mail y secretos Proton Pass

## Qué hace / Propósito

**Thin-skill** de enrutado para el ecosistema Proton: decide si la petición es de **correo**
(Proton Mail) o de **secretos** (Proton Pass) y qué vía usar. La operativa completa (MCP
tools, clasificación, bóvedas, deployment) vive en **protonsuite-tools** (canon operativo);
esta skill aporta el criterio de enrutado y el detalle local **legacy** si el canon no es accesible.

## Enrutado rápido

| Petición del operador | Ir a | Vía preferente |
|---|---|---|
| Leer, buscar, enviar o clasificar correo Proton | [Correo Proton Mail](#correo-proton-mail) | MCP Mail → CLI protonsuite-tools → `scripts/proton_bridge.py` |
| Obtener tokens, passwords o API keys de Proton Pass | [Secretos Proton Pass](#secretos-proton-pass) | MCP Pass → `pass-cli` v2.3+ (JSON) |
| Instalación/configuración de Bridge o sesión Pass | `references/setup.md` (Mail) y protonsuite-tools | docs del tag pineado |
| Otro proveedor de correo; secretos de CI/GitHub | fuera de esta skill | — |

## Correo Proton Mail

Derivar aquí cuando el usuario pida:
- Leer/buscar/listar correos Proton Mail
- Enviar emails desde Proton
- Clasificar correos por caso/organismo (juzgado, registro, TGSS, notaría, SMAC)
- Marcar leído/no leído, obtener cabeceras completas; operar vía Bridge (ver `references/setup.md`)

**Contrato Bridge 3.x**: IMAP `127.0.0.1:1143` y SMTP `127.0.0.1:1025` con STARTTLS; la
credencial es la **contraseña generada por Bridge** (no la de la cuenta; requiere plan de
pago). En modo «split», `PROTON_USER` debe ser la dirección concreta a revisar; si Bridge
se cierra, todo da `Connection refused`. Puesta en marcha y acceso remoto (túnel SSH):
`references/setup.md`.

### MCP tools de Mail

Vía preferente frente a IMAP manual (detalle: `docs/mcp-tools/mail.md` del tag pineado);
los 14 tools cubren listar, buscar, fetch, envío, marcado y carpetas:

| Tool MCP | Equivale a | Uso típico |
|---|---|---|
| `mail_list` | `unread` / listado INBOX | Listar no leídos con límite |
| `mail_search` | `search` | Búsqueda por remitente/asunto/texto/fecha |
| `mail_fetch` | `fetch` | Cuerpo + cabeceras de un UID |
| `mail_send` | `send` | Enviar texto plano UTF-8 |
| `mail_mark` | `mark` | Marcar leído/no leído |
| `mail_folders` | `folders` | Listar buzones/etiquetas |

Sin MCP: fallback al CLI de protonsuite-tools y, en última instancia, al script legacy
`scripts/proton_bridge.py` (IMAP/SMTP básico; subcomandos en `references/api_reference.md`).

## Secretos Proton Pass

Derivar aquí cuando el usuario pida:
- Leer/buscar/listar secretos (tokens, passwords, API keys) en Proton Pass
- Operar con `pass-cli` (v2.3+): list, search, show, insert, edit, generate, login, sync
- Acceder a bóvedas: Personal, Estatal, Finanzas, Infraestructura, Archivo
- Sintaxis URI: `pass://<Bóveda>/<Item>/<campo>`

### MCP tools de Pass

Vía preferente frente a `pass-cli` manual (detalle: `docs/mcp-tools/pass.md` del tag pineado):

| Tool MCP | Equivale a | Uso típico |
|---|---|---|
| `pass_list` | `pass-cli list` | Localizar el item en su bóveda |
| `pass_show` | `pass-cli show --field` | Obtener un campo sin volcar el resto |
| `pass_search` | búsqueda de items | Buscar por nombre across-bóvedas |
| `pass_generate` | `pass-cli generate` | Generar contraseña aleatoria |

### pass-cli v2.3+: salida JSON

Desde v2.3 `pass-cli` emite JSON estructurado (`--json` / `--output json` según subcomando;
flag exacta en `docs/mcp-tools/pass.md` del tag pineado). Preferir JSON y parsear con `jq`
— **nunca con `grep`**: el texto plano es fallback frágil ante cambios de formato.

```bash
pass-cli login                                   # flujo web, idempotente
pass-cli sync                                    # datos frescos
pass-cli list --vault Personal --json | jq -r '.[].name'
PASS_JSON=$(pass-cli show 'Personal/app.com' --field password)  # un campo, sin volcar
```

Reglas: pedir siempre **un campo** concreto (nunca volcar el item entero), no dejar secretos
en logs ni en código, e inyectarlos por variable de entorno en el proceso destino. Sesión,
portapapeles y temporales: `references/security-notes.md`; comandos: `references/cli-reference.md`.

## MCP protonsuite-tools (canon operativo)

Vía preferente en **ambas** secciones: el servidor MCP de protonsuite-tools expone correo y
secretos como tools, y su documentación es el canon.

**URL base pinneada**: https://github.com/Soluciones-Alexendros/protonsuite-tools/tree/v1.5.0

| Qué necesitas | Enlace a protonsuite-tools (tag v1.5.0) |
|---|---|
| Instalación/configuración Bridge | `docs/bridge-core/setup.md` |
| API Reference (subcomandos CLI Mail) | `docs/bridge-core/api-reference.md` |
| Mail: 14 tools (list, search, fetch, send, mark, folders) | `docs/mcp-tools/mail.md` |
| Pass: CLI y tools (pass-cli, bóvedas, campos) | `docs/mcp-tools/pass.md` |
| Security notes (sesión, env, clipboard) | `docs/bridge-core/security-notes.md` |
| Agent quickstart / deployment | `docs/agent-quickstart.md`, `docs/deployment.md` |

> Licencia: protonsuite-tools es AGPL-3.0; este repo es MIT. Solo enlazar, no vendorizar código.

## Novedades 2024-26

- Mail: `references/protonsuite-mail-2024-2026.md` — Bridge 3.x, `proton-python-sdk` (evaluación
  frente a Bridge IMAP), matriz MCP → CLI → script legacy.
- Pass: `references/protonsuite-pass-2024-2026.md` — pass-cli v2.3+ (JSON estable), MCP Pass,
  matriz MCP → CLI → manual.

## Uso

Skill de enrutado: identificar correo vs. secretos («Enrutado rápido»), preferir siempre los
MCP tools de protonsuite-tools, y bajar a CLI o script legacy solo si el MCP no está disponible.

## Estructura

- `SKILL.md` — criterio de enrutado (Mail vs. Pass) y enlaces a protonsuite-tools.
- `references/setup.md` — instalación/configuración de Proton Mail Bridge (legacy local; canon en protonsuite-tools).
- `references/api_reference.md` — subcomandos del script `proton_bridge.py` (legacy).
- `references/cli-reference.md` — `pass-cli` v2.2.0+ (legacy; JSON v2.3+ en `protonsuite-pass-2024-2026.md`).
- `references/security-notes.md` — sesión, inyección por entorno, portapapeles y temporales (Pass).
- `references/protonsuite-mail-2024-2026.md`, `references/protonsuite-pass-2024-2026.md` — novedades 2024-26.
- `scripts/proton_bridge.py` — CLI IMAP/SMTP **legacy: funcional pero deprecado**; se mantiene con tests en verde; no añadir features.
- `scripts/test_proton_bridge.py`, `scripts/tests/smoke_sh.sh` — tests del script legacy.

## Herramientas y referencias

- `scripts/proton_bridge.py` — IMAP/SMTP local contra Bridge (legacy, sin features nuevas);
  tests en `scripts/test_proton_bridge.py` (hardening sin red) y smoke en `scripts/tests/smoke_sh.sh`.
- Canon: tabla **MCP protonsuite-tools** arriba (tag v1.5.0 pineado; AGPL-3.0: solo enlazar).
- Detalle local legacy: `references/setup.md`, `references/api_reference.md`, `references/cli-reference.md`, `references/security-notes.md`.
