---
name: email-proton
description: >-
  Gestiona correo Proton Mail vía Proton Mail Bridge (IMAP/SMTP local). Usar cuando el
  operador pida leer, enviar o organizar correo Proton. No usar para secretos de Proton Pass
  (→ protonpass).
license: MIT
metadata:
  author: Soluciones-Alexendros
  version: "0.1.0"
  dominio: integraciones
  idioma: es

---
# Proton Mail Bridge — gestión de correo

## Qué hace / Propósito

Gestiona el correo de Proton Mail a través de Proton Mail Bridge, que expone IMAP y SMTP locales para descifrar el buzón. Sirve para listar, buscar, leer, clasificar y marcar correos, enviar mensajes y obtener cabeceras completas como prueba documental del expediente.

## Cuándo usarme / Triggering

- Cuando se mencione Proton Mail, Proton Mail Bridge o la cuenta de correo cifrado del usuario.
- Cuando haya que listar correos no leídos o buscar por remitente, asunto, texto o fecha.
- Al buscar comunicaciones de organismos concretos: juzgado, registro, TGSS, notaría o SMAC.
- Cuando se pida leer un correo completo (`fetch`), sus cabeceras (`--headers`) o marcar leído/no leído.
- Al clasificar por caso y registrar «Correo sin contestar» o «Correo mal contestado» en Notion.
- Cuando se solicite enviar un email o listar carpetas/etiquetas de la cuenta Proton.
- **NO usar cuando**: el correo no sea Proton vía Bridge (otro proveedor o protocolo externo a IMAP/SMTP locales); para la instalación inicial del Bridge, seguir `references/setup.md`.

## Referencias internas

- `references/setup.md` — Instalación y configuración inicial de Proton Mail Bridge; léelo si el Bridge no está instalado, no arranca o rechaza el login.
- `references/api_reference.md` — Detalle de subcomandos y opciones de `scripts/proton_bridge.py`; consúltalo cuando necesites la sintaxis exacta de `unread`, `search`, `fetch`, `folders`, `mark` o `send`.

## Cómo funciona

Proton Mail Bridge corre en la máquina del usuario y expone IMAP y SMTP locales
que descifran el buzón de Proton:

- **IMAP:** `127.0.0.1:1143` (STARTTLS, certificado autofirmado)
- **SMTP:** `127.0.0.1:1025` (STARTTLS)
- **Credenciales:** dirección Proton completa como usuario y la contraseña generada
  por Bridge (no la de la cuenta Proton). Se obtiene en la app Bridge → cuenta →
  «Mailbox details» / «Detalles del buzón».

## Limitación crítica de red

El Bridge escucha solo en `localhost` **de la máquina del usuario**. Un agente en
sandbox remoto NO puede alcanzarlo. Por tanto:

1. Si se ejecuta código en la máquina del usuario (CLI local, agente local):
   usar `scripts/proton_bridge.py` directamente.
2. Si el agente corre en remoto: entregar al usuario el comando exacto para que lo
   ejecute él, o pedirle que exponga el Bridge por red (no recomendado salvo túnel
   SSH: `ssh -L 1143:127.0.0.1:1143 user@host`).

Nunca pedir la contraseña de la cuenta Proton; solo la contraseña generada por
Bridge. Las credenciales se pasan por variables de entorno
(`PROTON_USER`, `PROTON_PASS`), nunca en la línea de comandos ni en archivos.

## Flujo de trabajo

1. Confirmar que Bridge está instalado y corriendo (ver
   `references/setup.md` si no lo está).
2. Pedir al usuario usuario (email Proton) y contraseña de Bridge, que los exporte
   como `PROTON_USER` y `PROTON_PASS`.
3. Ejecutar `scripts/proton_bridge.py` con el subcomando adecuado:

```bash
# Listar no leídos (bandeja de entrada, 50 más recientes)
python3 scripts/proton_bridge.py unread

# Buscar por remitente, asunto o texto (sintaxis IMAP SEARCH)
python3 scripts/proton_bridge.py search --from "juzgado" --since 01-Jan-2026
python3 scripts/proton_bridge.py search --subject "expediente"
python3 scripts/proton_bridge.py search --text "Registro de la Propiedad"

# Leer un correo completo por UID
python3 scripts/proton_bridge.py fetch --uid 12345

# Listar carpetas/etiquetas
python3 scripts/proton_bridge.py folders

# Marcar leído / no leído
python3 scripts/proton_bridge.py mark --uid 12345 --read
python3 scripts/proton_bridge.py mark --uid 12345 --unread

# Enviar (SMTP :1025)
python3 scripts/proton_bridge.py send --to "dest@ejemplo.com" --subject "Asunto" --body "Texto"
```

4. Clasificar resultados según la materia del usuario: al trabajar el expediente,
   cada correo relevante se registra en la lista de pendientes de Notion con tipo
   «Correo sin contestar» / «Correo mal contestado», fecha, remitente y detalle.

## Criterios de clasificación para el expediente

- **Correo sin contestar:** enviado por el usuario a un organismo sin respuesta en
  hilo posterior.
- **Correo mal contestado:** respuesta recibida que no contesta lo preguntado, es
  genérica o evasiva («parrafada infumable»).
- Para ambos: conservar fecha, remitente, asunto y Message-ID como prueba; el
  correo electrónico con cabeceras completas es documento acreditativo
  (`--headers` en `fetch`).

## Errores frecuentes

- `Connection refused`: Bridge no está corriendo o el puerto no es 1143/1025
  (comprobar en la app Bridge → «Switch to...» → puertos).
- Fallo de certificado TLS: el script ya desactiva la verificación del certificado
  autofirmado de Bridge; no «arreglarlo» instalando nada.
- Login rechazado: se está usando la contraseña de la cuenta Proton en vez de la
  contraseña de Bridge.
- Carpetas con nombres raros (`&AOk`): son IMAP UTF-7 modificado; el script las
  decodifica en `folders`.

Para instalación y configuración inicial de Bridge: leer `references/setup.md`. Para
detalles del script: `references/api_reference.md`.

## Uso

Usar cuando el operador pida leer, enviar o organizar correo Proton vía Bridge. No usar para secretos de Proton Pass (→ `protonpass`) ni para otro proveedor fuera de IMAP/SMTP locales.

## Estructura

- `SKILL.md` — flujo, clasificación y errores frecuentes.
- `references/setup.md` — instalación y variables de entorno.
- `references/api_reference.md` — subcomandos del script.
- `scripts/proton_bridge.py` — CLI IMAP/SMTP.

## Herramientas

| Script | Propósito |
|---|---|
| `scripts/proton_bridge.py` | `unread`, `search`, `fetch`, `folders`, `mark`, `send` vía Bridge |
| `scripts/test_proton_bridge.py` _(tests, no tocar)_ | Tests del script |

## Referencias

- `references/setup.md` — instalación y configuración.
- `references/api_reference.md` — sintaxis exacta de subcomandos.
