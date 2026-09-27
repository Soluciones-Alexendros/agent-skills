# Modo Box (ES)

> Modo interno de la skill `upstash` (no es skill separada). Router: `upstash` → este modo
> ante container, sandbox, agente IA, browser headless, snapshot o workspace remoto.

## Cubre

Contenedores sandbox remotos para agentes IA: shell, filesystem, git, cron, snapshots,
navegador headless y agentes integrados. SDK JS/TS (`@upstash/box`), Python
(`upstash-box`, snake_case) y CLI (`box`).

## Referencias propias

Guía principal (ES): `references/box.md`.

| Fichero | Contenido |
|---|---|
| `references/box.md` | guía principal ES (JS/Python/CLI) |
| `references/box-js-overview.md` | SDK `@upstash/box` (referencia JS) |
| `references/box-py-overview.md` | SDK `upstash-box` (referencia Python, espejo snake_case) |
| `references/box-cli-overview.md` | CLI `box` (contenedor remoto, no local) |

## Ejemplos

Ver `ejemplos.md` (crear box, ejecutar shell, snapshot).

## Dependencias

Ninguna. `box` opera sobre un contenedor remoto: las herramientas locales de ficheros y
shell no actúan dentro del box (ver `references/box-cli-overview.md`).
Configuración y errores comunes: `../../core/config.md`, `../../core/errores.md`.
