# Directorios Esenciales (FHS ALIGNUX)

## TOC
- [Propósito](#propósito)
- [Principio rector](#principio-rector)
- [Notación de referencia ALIGNUX](#notación-de-referencia-alignux)
- [Árbol canónico](#árbol-canónico)
- [Directorios y propósito](#directorios-y-propósito)
- [Invariantes de ownership y seguridad](#invariantes-de-ownership-y-seguridad)
- [Invariantes de `·Aplicaciones/Terminal`](#invariantes-de-aplicacionesterminal)
- [Mapa XDG](#mapa-xdg)
- [Frontera fuente / producto (interna)](#frontera-fuente--producto-interna)
- [Operaciones habituales](#operaciones-habituales)
- [Anti-patrones (directorios no certificables)](#anti-patrones-directorios-no-certificables)
- [Trazabilidad](#trazabilidad)

## Propósito
Definir los **directorios esenciales** del home del operador ALIGNUX: qué directorio sirve a qué propósito, con qué ownership e invariantes, y cuáles están **certificados** por ALIGNUX. Extiende al home completo el canon que ya regía para `··Terminal/` (ver `../../alignux-seguridad/references/postura-defensiva.md`).

## Principio rector
**Una raíz por dominio; un propósito por directorio dentro de ella** (Principio 2 — Coherencia sobre consistencia):

- **Aplicaciones** (producto + **código fuente** + webs + dotfiles versionables) → `·Aplicaciones`
- **Medios personales** → `·Audiovisual`
- **FHS/XDG del usuario** (documentos, descargas, escritorio, público) → intactos, sin marca

`·Aplicaciones` es el «Program Files» de ALIGNUX **ampliado**: la raíz de las aplicaciones del operador. La frontera **fuente/producto** no se separa en dos raíces, sino **dentro** de ella (`··Fuentes` vs `··Ventana`/`··Terminal`).

## Notación de referencia ALIGNUX
`·` es una **marca de estándar (certificación ALIGNUX)**: identifica los directorios **propuestos, validados e integrados** por la lógica ALIGNUX a partir del FHS original. **El origen es indiferente** — vale igual si ALIGNUX los **creó** (`·Audiovisual`) que si los **adoptó** (`·Aplicaciones`).

- **Nº de `·` = estrato respecto al origen `~`.** `·` = hijo directo de `~`; `··` = nieto (anidado genérico dentro de un directorio certificado); `···` = bisnieto.
- El signo es **notación de referencia, NO forma parte del nombre real en disco.** Los comandos y las rutas de fichero siguen usando `~/Aplicaciones`, `~/Audiovisual` (y así lo exigen XDG, auditd, AIDE y el `PATH`).
- **Solo se certifica lo que ALIGNUX integra en su estándar.** Los directorios del FHS/XDG que ALIGNUX **deja intactos** (`Documentos`, `Descargas`, `Escritorio`, `Público`) van **sin marca** — y también lo que se **integra dentro** de ellos: `Documentos/Formatos/` sirve a `XDG_TEMPLATES_DIR` pero **no se certifica** (su raíz, `Documentos`, es XDG intacto).
- La marca **no distingue fuente de producto**: eso lo decide la subcarpeta (`··Fuentes` = fuente; `··Ventana`/`··Terminal` = producto).

Certificados vigentes:
- **Estrato 1:** `·Aplicaciones/`, `·Audiovisual/`.
- **Estrato 2:** de `·Aplicaciones/`: `··Ventana/`, `··Terminal/`, `··Fuentes/`, `··Websites/`, `··dotfiles/`; de `·Audiovisual/`: `··Audio/`, `··Imágenes/`, `··Vídeos/`.
- **Estrato 3:** `···Scripts/`, `···Shell/`, `···Agentes/` (de `··Terminal/`).

## Árbol canónico
```text
~/
├── ·Aplicaciones/         # RAÍZ DE APLICACIONES (producto + fuente + webs)
│   ├── ··Ventana/         #   producto GUI (AppImages, suites)
│   ├── ··Terminal/        #   producto CLI + canon de terminal (root:root)
│   │   ├── Scripts/       #     conjuntos de comandos propios (shell/python) — en PATH
│   │   ├── Shell/         #     dotfiles de shell (fuente canónica; symlink en ~)
│   │   └── Agentes/       #     dotdirectories de CLIs de agentes LLM-IA (symlink en ~)
│   ├── ··Fuentes/         #   CÓDIGO FUENTE que el operador edita/desarrolla (repos git)
│   ├── ··Websites/        #   proyectos web (HTTP/deploy)
│   └── ··dotfiles/        #   dotfiles versionables (p. ej. ssh-config)
├── ·Audiovisual/          # MEDIOS PERSONALES (XDG)
│   ├── ··Audio/           #   XDG_MUSIC_DIR
│   ├── ··Imágenes/        #   XDG_PICTURES_DIR
│   └── ··Vídeos/          #   XDG_VIDEOS_DIR
├── Documentos/            # FHS/XDG intactos (sin marca)
│   ├── Formatos/          #   XDG_TEMPLATES_DIR (plantillas; NO certificado)
│   └── MantenimientoLocal/  # repo de trazabilidad del sistema
├── Descargas/  Escritorio/  Público/
└── .local/  .config/  .agents/  .ssh/ …   # dotfiles, toolchains y estado
```

## Directorios y propósito
| Ruta (referencia ALIGNUX) | Propósito | Invariante |
| --- | --- | --- |
| `·Aplicaciones` | Raíz de **aplicaciones** (producto + fuente + webs + dotfiles) | usuario |
| `··Ventana` | Producto **GUI** (instalar y operar) | usuario |
| `··Terminal` | Producto **CLI** + canon de terminal | ver invariantes específicos |
| `··Fuentes` | **Código fuente** que el operador edita/desarrolla | usuario; cada subcarpeta = repo git |
| `··Websites` | Proyectos web | usuario |
| `··dotfiles` | Dotfiles versionables (p. ej. `ssh-config`) | usuario |
| `···Scripts` | Conjuntos de comandos propios ejecutados por terminal | `root:root`; en `PATH` |
| `···Shell` | Dotfiles de shell (fuente canónica) | usuario; symlink ancla en `~` |
| `···Agentes` | Dotdirectories de CLIs de agentes LLM-IA (config, sesiones, estado) | usuario; symlink ancla en `~` |
| `··Audio` | Música y audio de trabajo | usuario; `XDG_MUSIC_DIR` |
| `··Imágenes` | Fotos, capturas, fondos | usuario; `XDG_PICTURES_DIR` |
| `··Vídeos` | Vídeo | usuario; `XDG_VIDEOS_DIR` |
| `Documentos` | Documentos del usuario + repos de trazabilidad | usuario; FHS intacto, sin marca |
| `Documentos/Formatos` | Plantillas | usuario; `XDG_TEMPLATES_DIR`, **sin certificar** |

## Invariantes de ownership y seguridad
1. El **código fuente** (`··Fuentes`) es propiedad del usuario y **no se ejecuta desde ahí**: se **construye** y su producto se instala en `··Ventana` (GUI) o `··Terminal` (CLI).
2. Los directorios versionados (`·Aplicaciones/··Fuentes/*`, `Documentos/MantenimientoLocal`) son repos git; las reorganizaciones se hacen con `mv` dentro del mismo filesystem (rename atómico y reversible).
3. La marca `·` es solo de referencia: **nunca** aparece en nombres reales, rutas de configuración ni reglas de auditoría.

## Invariantes de `·Aplicaciones/Terminal`
`··Terminal` **no es homogéneo**: separa canon inmutable de estado mutable.

| Subárbol | Contenido | Ownership | `chattr +i` | auditd/AIDE |
| --- | --- | --- | --- | --- |
| raíz + binarios + `Scripts/` | **canon inmutable** (productos CLI) | `root:root` 0755 | **Sí** | **Sí** — clave `terminal_canon` |
| `Shell/` | dotfiles de shell (fuente canónica) | usuario | No | No (excluido) |
| `Agentes/` | dotdirectories de las CLIs de agentes LLM-IA | usuario | No | No (excluido) |

- La regla auditd `-w /home/alexendros/Aplicaciones/Terminal -p wa -k terminal_canon` **no es recursiva**: vigila altas/bajas/renombrados en la raíz del canon; `Shell/` y `Agentes/` quedan fuera.
- AIDE aplica `TerminalCanon` al canon y **excluye** el estado mutable con reglas negativas no recursivas (`-…/Shell`, `-…/Agentes`; AIDE ≥ 0.19).
- **Anclaje:** las CLIs y el shell resuelven rutas **literales** (`~/.opencode`, `~/.bashrc`). La fuente canónica vive en `…/Terminal/{Shell,Agentes}/` y en `~` queda un **symlink** → canonical. `mv` es rename atómico: no rompe fds abiertos; **si se renombra la raíz o alguna de esas carpetas hay que recrear los symlinks y repuntar los shims**.
- **`.agents/`** (skills ALIGNUX) **no** es estado de una CLI: vive en `~` como infraestructura del canon de skills.

## Mapa XDG
`~/.config/user-dirs.dirs` define los directorios de usuario. **Aquí se usan rutas literales (sin marca)**, porque son valores de configuración:

| XDG | Ruta literal |
| --- | --- |
| `XDG_MUSIC_DIR` | `$HOME/Audiovisual/Audio` |
| `XDG_PICTURES_DIR` | `$HOME/Audiovisual/Imágenes` |
| `XDG_VIDEOS_DIR` | `$HOME/Audiovisual/Vídeos` |
| `XDG_TEMPLATES_DIR` | `$HOME/Documentos/Formatos` |
| `XDG_DESKTOP_DIR` / `XDG_DOWNLOAD_DIR` / `XDG_DOCUMENTS_DIR` / `XDG_PUBLICSHARE_DIR` | sin cambios (`Escritorio`, `Descargas`, `Documentos`, `Público`) |

**Reparto:** los directorios **certificados** (`·Aplicaciones`, `·Audiovisual`) sirven a roles XDG (`MUSIC`, `PICTURES`, `VIDEOS`), pero la marca `·` **nunca** entra en los valores de configuración. Los XDG que ALIGNUX no toca quedan **sin marca**; un directorio integrado dentro de ellos (`Documentos/Formatos`) tampoco se certifica.

Tras editar el mapa: ejecutar `xdg-user-dirs-update`; publicar las mismas rutas en `~/.config/environment.d/40-xdg.conf` (sesión systemd/GUI) y `··Shell/shared-env.sh` (shells); actualizar `~/.config/gtk-{3,4}.0/bookmarks` (barra lateral de Nautilus). Las bases XDG (`CONFIG`/`CACHE`/`DATA`/`STATE_HOME`) se declaran explícitas a `~/.config`, `~/.cache`, `~/.local/{share,state}` — no se relocan.

## Frontera fuente / producto (interna)
- **Fuente** → `··Fuentes` (repos git: CLIs, agentes, daemons, playbooks). Es el material que Devs/Maint/Progs **modifican, corrigen o mejoran**.
- **Producto** → `··Ventana` (GUI) y `··Terminal` (CLI). Es lo que el usuario **instala y opera** sin tocar código.

**Criterio (qué decide el destino):** no es "¿es un repo git?", sino **el uso**. Si el operador **lo edita/desarrolla** → `··Fuentes`. Si **se descarga/instala para usarlo** —aunque venga de GitHub y traiga `.git`, `src/` o `kits/`— → **producto** (`··Ventana`/`··Terminal`). Ejemplo: `tldraw` (suite descargada de GitHub por compatibilidad, para usar sus apps) es **producto GUI** (`··Ventana`), no fuente.

Ninguna subcarpeta debe mezclar fuente y producto.

## Operaciones habituales
- **snap:** **proscrito**. snapd exige `~/snap` en la raíz y no admite ocultarlo ni reubicarlo (symlink rechazado; bind-mount deja la entrada visible; el flag `experimental.hidden-snap-folder` no aplica). Se eliminaron los snaps y se purgó `snapd` (2026-09-14). Navegadores y apps viven como **deb** (Vivaldi, Brave).
- **Añadir un repo nuevo:** clonar en `·Aplicaciones/··Fuentes` (código que edito) o `··Websites` (proyectos web).
- **Instalar el producto de un repo:** construir y dejar el artefacto en `··Ventana` (GUI) o `··Terminal` (CLI); documentar su `.desktop` o symlink.
- **Añadir medios:** siempre bajo `·Audiovisual/<tipo>`. **Plantillas:** en `Documentos/Formatos`.
- **Añadir un comando propio:** script shell/python → `··Terminal/Scripts/` (en `PATH`).
- **Toolchains y cachés fuera de la raíz de `~`:** `cargo`/`rustup`/`bun`/`pyenv` → `~/.local/share/{cargo,rustup,bun,pyenv}`; `npm`/`nv`/`triton` → `~/.cache/{npm,nv,triton}`; GnuPG/`pass` → `~/.local/share/{gnupg,password-store}`. Conexión por variables en `··Shell/shared-env.sh` y `~/.config/environment.d/50-alignux-home.conf`. **No** recrear `~/.cargo`, `~/.gnupg`, etc.
- **Renombrar una carpeta anclada:** recrear los symlinks de `~` (`Shell/`, `Agentes/`), repuntar los shims de `··Terminal/` y actualizar auditd/AIDE/`PATH` si cambia la raíz.

## Anti-patrones (directorios no certificables)
- **`~/bin/`** — carpeta artificial, sin fundamento. Un script pertenece a un **`tmp/`** (uso puntual), a **`·Aplicaciones/··Terminal/Scripts/`** (comandos propios) o a una **plantilla/script reutilizable** (`plantillas/scripts/`). La única ubicación estándar de binarios de usuario es `~/.local/bin` (XDG). En este home, `~/bin` fue **eliminado** (2026-09-14).
- **`··Ventana/apps/`** — capa **redundante**: repite el propósito del propio directorio contenedor. El contenido va **directamente** en `··Ventana/` (un subdirectorio por app: `cursor/`, `grok-bot/`, `wezterm/`, `freebuff/`).
- **Raíces separadas para fuente y producto** — superado (2026-09-14): la frontera vive **dentro** de `·Aplicaciones` (`··Fuentes` vs `··Ventana`/`··Terminal`), no en dos raíces del home.
- **Certificar lo integrado en un árbol XDG** — `Documentos/Formatos` sirve a `XDG_TEMPLATES_DIR` pero **no lleva marca**: `Documentos` es FHS/XDG intacto.
- **Estado mutable bajo el canon inmutable** — `Shell/` y `Agentes/` **no** deben ser `root:root` ni `chattr +i` (romperían la escritura de las CLIs).
- **Repo git/husky en `~`** — el home **no** es un repositorio.

## Trazabilidad
| Época | Estructura | Lección |
| --- | --- | --- |
| Antes | `~/repositorios/<owner>/…` | agrupar por owner no dice nada del contenido |
| 2026-09 | `~/Github` + `~/Websites` + `~/Programas` | separa por tipo de repo, pero **mezcla fuente y producto** |
| 2026-09-14 (a) | `·Codexdev` (fuente) + `·Aplicaciones`/`·Terminal` (producto) + `·Audiovisual` | **agrupar por propósito** + certificación de estándar `·` |
| 2026-09-14 (b) | `·Programas` (producto) + `··Fuentes` + canon CLI completo | **producto como «Program Files»**; canon CLI absorbe shell y estado |
| 2026-09-14 (c) | `·Aplicaciones` (raíz única: producto + `··Fuentes` + `··Websites` + `··dotfiles`) + `·Audiovisual` | **una raíz por dominio**; frontera fuente/producto **interna** |
| 2026-09-14 (d) | `Formatos` → `Documentos/Formatos` (XDG, sin certificar); `Estado/` → `··Agentes/` | lo integrado en un árbol XDG **no se certifica**; nombrar por **contenido**, no por abstracción |

*Aplicado según la metodología de `despliegue-aprendizajes.md`: patrón histórico → principio constitucional (2, 3 y 6) → estructura → validación.*
