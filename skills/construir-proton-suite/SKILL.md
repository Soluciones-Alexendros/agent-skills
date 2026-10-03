---
name: construir-proton-suite
description: >-
  Correo Proton Mail (Proton Mail Bridge IMAP/SMTP local, MCP Mail) y secretos Proton Pass
  (pass-cli v2.3+ con salida JSON estable, MCP Pass). Usar cuando el operador pida leer,
  buscar, enviar o clasificar correo Proton, o obtener tokens, passwords y API keys
  almacenados en Proton Pass. No usar para otros proveedores de correo ni para secretos
  de CI/GitHub.
license: MIT
metadata:
  author: Soluciones-Alexendros
  version: "1.1.1"
  dominio: construir
  tipo: router
  idioma: es
---

# construir-proton-suite — Correo Proton Mail y secretos Proton Pass

## Propósito

Thin-skill de enrutado para el ecosistema Proton: decide si la petición es de correo (Proton Mail) o de secretos (Proton Pass) y qué vía usar. La operativa completa vive en protonsuite-tools (canon operativo, tag v1.5.0); esta skill aporta el criterio de enrutado y el detalle local legacy si el canon no es accesible.

## Cuándo usar

Leer, buscar, enviar o clasificar correo Proton; obtener tokens, passwords o API keys de Proton Pass sin pedirlos al operador ni hardcodearlos.

## Enrutado

| Petición del operador                               | Ir a                                      | Vía preferente                                                |
| --------------------------------------------------- | ----------------------------------------- | ------------------------------------------------------------- |
| Leer, buscar, enviar o clasificar correo Proton     | Correo Proton Mail                        | MCP Mail → CLI protonsuite-tools → `scripts/proton_bridge.py` |
| Obtener tokens, passwords o API keys de Proton Pass | Secretos Proton Pass                      | MCP Pass → `pass-cli` v2.3+ (JSON)                            |
| Instalación/configuración de Bridge o sesión Pass   | `references/setup.md` y protonsuite-tools | docs del tag pineado                                          |
| Otro proveedor de correo; secretos de CI/GitHub     | fuera de esta skill                       | —                                                             |

## Procedimiento

**Correo.** Contrato Bridge 3.x: IMAP `127.0.0.1:1143` y SMTP `127.0.0.1:1025` con STARTTLS; la credencial es la contraseña generada por Bridge. En modo split, `PROTON_USER` es la dirección concreta. Setup: `references/setup.md`. Tools MCP: `mail_list`, `mail_search`, `mail_fetch`, `mail_send`, `mail_mark`, `mail_folders`. Sin MCP: CLI de protonsuite-tools y, en última instancia, `scripts/proton_bridge.py` (legacy).

**Pass.** Preferir JSON de `pass-cli` v2.3+ y parsear con `jq`. Pedir un campo concreto, no volcar el item. Tools MCP: `pass_list`, `pass_show`, `pass_search`, `pass_generate`. Sesión y portapapeles: `references/security-notes.md`.

**Canon pineado:** https://github.com/Soluciones-Alexendros/protonsuite-tools/tree/v1.5.0 (AGPL-3.0: solo enlazar, no vendorizar). Novedades 2024-26: `references/protonsuite-mail-2024-2026.md`, `references/protonsuite-pass-2024-2026.md`.

## Herramientas

| Recurso                         | Propósito                                                   |
| ------------------------------- | ----------------------------------------------------------- |
| `scripts/proton_bridge.py`      | IMAP/SMTP local contra Bridge (legacy, sin features nuevas) |
| `scripts/test_proton_bridge.py` | Tests del script legacy (hardening sin red)                 |
| `scripts/tests/smoke_sh.sh`     | Smoke del script legacy                                     |

## Referencias

- `references/setup.md`, `references/api_reference.md`, `references/cli-reference.md`, `references/security-notes.md`.
- `references/protonsuite-mail-2024-2026.md`, `references/protonsuite-pass-2024-2026.md`.
- Canon: protonsuite-tools tag v1.5.0 (`docs/mcp-tools/mail.md`, `docs/mcp-tools/pass.md`).
