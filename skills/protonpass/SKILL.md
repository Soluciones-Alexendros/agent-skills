---
name: protonpass
description: >-
  Obtiene secretos desde Proton Pass vía pass-cli sin pedirlos al usuario ni
  hardcodearlos. Usar cuando haga falta token, password o API key almacenado en
  Proton Pass. No usar para correo (→ email-proton).
license: MIT
metadata:
  author: Soluciones-Alexendros
  version: "0.2.0"
  dominio: integraciones
  idioma: es

---

# Proton Pass — operativa de secretos

## Propósito

Leer credenciales del almacén Proton Pass e inyectarlas en fichero o proceso. Nunca pegar el secreto en el chat ni en commits.

## Pre-flight

- `pass-cli` instalado: `which pass-cli && pass-cli --version` (v2.2.0+)
- Sesión activa en `~/.local/share/proton-pass-cli/.session/`
- Si falta pass-cli → instalar desde https://proton.me/pass _(externo)_
- Si sesión caducada → `pass-cli login` (flujo web, idempotente)

Almacén: **Proton Pass**, CLI oficial **`pass-cli`** (`~/.local/bin/pass-cli`, backend keyring).

Bóvedas habituales: **Personal · Estatal · Finanzas · Infraestructura · Archivo**.

Sintaxis URI: `pass://<Bóveda>/<Item>/<campo>`.

## Acceso

```bash
# Listar / buscar (sin volcar secretos al chat)
pass-cli list
pass-cli search "<término>"

# Leer un campo a variable de entorno en la misma shell
export TOKEN="$(pass-cli get 'pass://Infraestructura/<Item>/password')"
# Usar $TOKEN en el comando siguiente; no echo ni printf del valor
```

Si una lectura falla por sesión: `pass-cli login` y reintentar una vez.

## Reglas

1. No mostrar el valor del secreto en la respuesta al usuario.
2. No escribir secretos en ficheros versionados; preferir env o ficheros fuera del repo (`chmod 600`).
3. Tras usar, no dejar el valor en historial de shell si se puede evitar (`set +o history` en la sesión puntual).
4. Si el ítem no existe, preguntar la ruta URI; no inventar bóvedas.

## Frontera

- Correo Proton Mail → `email-proton`.
- Secretos de CI/GitHub → settings del remoto o `gh secret`, no esta skill.

## Uso

Obtener secretos desde Proton Pass vía pass-cli cuando haga falta token, password o API key almacenado, sin pedirlos ni hardcodearlos. No usar para correo (ver `email-proton`). Ver frontmatter `description`.

## Estructura

- `SKILL.md` — operativa de acceso y reglas.
- `references/cli-reference.md` — comandos de `pass-cli` (list, show, insert, edit, rm, mv, cp, generate, login, logout, sync, share).
- `references/security-notes.md` — manejo de sesión, inyección por variables de entorno y limpieza de portapapeles.
- URI _(ejemplos)_: `pass://<Bóveda>/<Item>/<campo>`; rutas locales _(ejemplos)_: `~/.local/share/proton-pass-cli/.session/`, `~/.local/bin/pass-cli`.

## Herramientas

Sin `scripts/` propios. Herramienta externa invocada (no versionada aquí):

| Herramienta | Propósito |
|---|---|
| `pass-cli` (v2.2.0+) | Listar/buscar/leer secretos de Proton Pass |

## Referencias

- Pre-flight, Acceso y Reglas en este `SKILL.md`.
- Producto distinto: `email-proton` (correo Proton Mail).
