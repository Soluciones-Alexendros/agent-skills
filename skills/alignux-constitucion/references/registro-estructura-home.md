# Estándar: Estructura del home y notación de referencia ALIGNUX (`·`)

> Registro constitucional conforme a la plantilla de salida de `ALIGNUX.constitucion`.
> Norma completa: `references/DirectoriosEsenciales.md`. Fecha: 2026-09-14. Registro: **2.5.1** (skill `ALIGNUX.constitucion` 2.8.1).

## Contexto histórico (qué limitación supera)
La organización del home derivó sin canon y por **contenedor**, no por propósito:

| Época | Estructura | Limitación que revelaba |
| --- | --- | --- |
| Anterior | `~/repositorios/<owner>/…` | agrupar por owner — no dice nada del contenido |
| 2026-09 | `~/Github` + `~/Websites` + `~/Programas` | agrupar por tipo de repo — **mezcla código fuente y productos** |
| 2026-09-14 (a) | `·Codexdev` (fuente) + `·Aplicaciones`/`·Terminal` (producto) | el **producto** quedaba disperso en varias raíces |
| 2026-09-14 (b) | `·Programas` (producto) + `·Codexdev` (fuente) | **dos raíces** del home para lo mismo: «programas» |
| 2026-09-14 (c) | `·Aplicaciones` (raíz única: producto + fuente + webs + dotfiles) + `·Audiovisual` | **una raíz por dominio**; frontera fuente/producto **interna** |
| 2026-09-14 (d) | `Formatos` → `Documentos/Formatos` (XDG, sin certificar); `Estado/` → `··Agentes/` | lo integrado en un árbol XDG **no se certifica**; nombrar por **contenido**, no por abstracción |

Segunda limitación: sin una marca, los directorios **certificados** por el canon eran **indistinguibles** de los estándar/XDG. El signo `·` los hace referenciables de un vistazo.

## Principio constitucional aplicado
- **P2 — Coherencia sobre consistencia:** mismo *propósito* servido. Deriva en **una raíz por dominio** (`·Aplicaciones`, `·Audiovisual`) y, dentro de ella, **un propósito por directorio** (producto ≠ fuente).
- **P3 — Estructura que habilita, no que constriñe:** la marca `·` y los estratos existen para *descubrimiento y uso*, no para satisfacer un linter — y **no se aplican** a lo que vive en árboles XDG intactos.
- **P4 — Documentación viva:** la norma se fija en `DirectoriosEsenciales.md` y se registra en catálogo y log.
- **P5 — Aprendizaje como despliegue:** síntesis de ~4 épocas de estructura del home, no una adición aislada.
- **P6 — No codificar límites coyunturales:** `Terminal` no es monolíticamente inmutable (canon vs estado); la separación fuente/producto **no exige dos raíces**; y el **nombre** de un directorio debe describir su **contenido** (`Agentes`, no «Estado»).

## Especificación técnica
- **Árbol canónico:** `·Aplicaciones/{··Ventana,··Terminal,··Fuentes,··Websites,··dotfiles}` + `·Audiovisual/{··Audio,··Imágenes,··Vídeos}` + FHS/XDG intacto (`Documentos` —con `Formatos/` = `XDG_TEMPLATES_DIR`, **sin certificar**—, `Descargas`, `Escritorio`, `Público`).
- **Canon CLI (`··Terminal`):** `Scripts/` (comandos propios, shell/python; en `PATH`), `Shell/` (dotfiles de shell, fuente canónica), `Agentes/` (dotdirectories de CLIs de agentes LLM-IA: `.commandcode`, `.kimi-code`, `.opencode`, `.cursor`, `.grokbot`). `Shell/` y `Agentes/` se **anclan** con symlink en `~`.
- **Invariantes:** canon inmutable de `··Terminal` (raíz + binarios + `Scripts/`) = `root:root`, 0755, `chattr +i`, auditd `terminal_canon`, AIDE. Estado mutable (`Shell/`, `Agentes/`) = usuario, sin `+i`, **excluido** de auditd/AIDE (reglas negativas no recursivas `-…/Shell`, `-…/Agentes`). La fuente (`··Fuentes`) nunca se ejecuta *in situ*.
- **Notación `·`** (U+00B7): nº de `·` = estrato respecto a `~` (`·` hijo; `··` nieto; `···` bisnieto). **No forma parte del nombre real** — XDG, auditd, AIDE, `PATH` y comandos usan rutas literales.
- **Estratos certificados:** 1 = `·Aplicaciones`, `·Audiovisual`; 2 = `··Ventana`, `··Terminal`, `··Fuentes`, `··Websites`, `··dotfiles`, `··Audio`, `··Imágenes`, `··Vídeos`; 3 = `···Scripts`, `···Shell`, `···Agentes`.
- **XDG:** `XDG_TEMPLATES_DIR` → `$HOME/Documentos/Formatos` (**sin certificar**: su raíz, `Documentos`, es XDG intacto); `MUSIC`/`PICTURES`/`VIDEOS` → `·Audiovisual/*`. La marca `·` **nunca** entra en valores de configuración.
- **Frontera fuente/producto:** **interna** a `·Aplicaciones` — `··Fuentes` (lo que edito/desarrollo) vs `··Ventana`/`··Terminal` (producto). Criterio: **el uso**.
- **Referencia normativa:** `references/DirectoriosEsenciales.md`.

## Trazabilidad a ~4 décadas de experiencia
| Era | Cómo se estructuraba | Lección heredada |
| --- | --- | --- |
| 1980s (64 KB) | por **necesidad absoluta**: cada byte cuenta | rigidez cuando el recurso manda |
| 1990s–2000s | jerarquías rígidas, "big iron" | la jerarquía por contenedor envejece |
| 2010s (cloud) | convenciones heredadas de proveedor | importar convenciones ≠ coherencia |
| 2020s+ (agentes/IA) | **por propósito e intención de uso** | nombrar por *para qué*, no por *dónde estaba* |

## Validación de coherencia
- [x] `DirectoriosEsenciales.md`: secciones requeridas, ≤300 líneas, TOC.
- [x] `SKILL.md`: referencias actualizadas; versión 2.8.1.
- [x] Referencia cruzada desde `../../linux-seguridad/references/postura-defensiva.md` (canon `··Terminal` y exclusiones `Shell/`/`Agentes/`).
- [x] Registro en `MIGRACION_LOG.md`; `~/Documentos/MantenimientoLocal` actualizado y commiteado.
- [x] Invariantes verificados: `lsattr -d ~/Aplicaciones/Terminal` = `+i`; `aide --config-check` OK; shims `kimi`/`opencode` → `Agentes/`; regla auditd reescrita (aplicación tras reinicio por `-e 2`).
- [x] XDG: `xdg-user-dir TEMPLATES` → `~/Documentos/Formatos`; sin `~/Plantillas` recreado.
- [x] `plantillas/scripts/Validador_AgentSkills.py --strict` — 18/18 skills válidas, 0 errores, exit 0.

---

# Registro anterior — 2026-09-14 (b/c) · 2.4.0 → 2.5.0 (superado)

> `·Programas` → `·Aplicaciones` como **raíz única** (producto: `··Ventana`/`··Terminal`; más `··Fuentes`, `··Websites`, `··Formatos`, `··dotfiles`), absorbiendo `·Codexdev`. Canon CLI completo (`Scripts/`, `Shell/`, `Estado/`). Estrato 1: `·Audiovisual`, `·Aplicaciones`; estrato 2: `··Audio/Imágenes/Vídeos`, `··Fuentes/Websites/Formatos/dotfiles`, `··Ventana/··Terminal`; estrato 3: `···Scripts/Shell/Estado`. XDG: `XDG_TEMPLATES_DIR` → `··Formatos`.

---

# Registro anterior — 2026-09-14 (b) · 2.4.0 (superado)

> `·Programas` (producto: `··Ventana`/`··Terminal`) + `··Fuentes` (en `·Codexdev`) + canon CLI completo. Estrato 1: `·Audiovisual`, `·Codexdev`, `·Programas`. Invariantes de `··Terminal` (canon inmutable vs estado mutable).

---

# Registro anterior — 2026-09-14 (a) · 2.3.0 (superado)

> `·Codexdev` (fuente) + `·Aplicaciones`/`·Terminal` (producto) + `·Audiovisual`, con la notación `·` de estratos. `Programas` era **fuente**; el producto se instalaba en `·Aplicaciones`/`·Terminal`. Invariantes: `·Terminal` = `root:root`, 0755, `chattr +i`, auditd `terminal_canon`, AIDE.
