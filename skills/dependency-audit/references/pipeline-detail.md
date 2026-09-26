# Pipeline de auditoría de dependancias — detalle

Detalle operativo de las 7 etapas del pipeline de `/deps`. Para cada etapa: qué hace,
entradas, salidas y criterios de decisión.

## Etapa 1 — Reconocimiento

**Qué hace**: identifica el ecosistema y el árbol de dependencias (directas vs transitivas).

**Entradas**: `package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, `pom.xml`,
`build.gradle`, `composer.json`, `Gemfile` _(ejemplos: ficheros del proyecto auditado)_.

**Salidas**: ecosistema detectado, lista de dependencias directas con rango de versiones,
lockfile presente o ausente.

**Criterios de decisión**:
- Más de un ecosistema presente → ejecutar las etapas correspondientes a cada uno y fusionar en la Etapa 7.
- Lockfile ausente → marcar como riesgo de build no reproducible y recomendar generarlo antes de auditar.
- Dependencias directas con rangos amplios (`^`, `>=`, `latest`) → fijar versiones exactas en la recomendación.

## Etapa 2 — npm audit

**Qué hace**: escanea el árbol npm contra la base de datos de vulnerabilidades.

**Entradas**: `package.json` + `package-lock.json`.

**Salidas**: JSON con vulnerabilidades clasificadas por severidad (critical, high, moderate, low).

**Criterios de decisión**:
- Critical/high → fix prioritario antes de cualquier otra labor.
- Fix con breaking changes → revisar changelog primero; nunca `npm audit fix --force` a ciegas.
- Vulnerabilidad solo en dependencia transitiva → evaluar actualización del paquete padre.

## Etapa 3 — Socket.dev scan

**Qué hace**: análisis de comportamiento de paquetes: malware, typosquatting, scripts de
instalación sospechosos, telemetría no declarada, mantenimiento abandonado.

**Entradas**: nombres y versiones de las dependencias directas.

**Salidas**: flags de riesgo por paquete (typosquat, postinstall peligroso, telemetría, etc.).

**Criterios de decisión**:
- Typosquatting confirmado → sustituir el paquete por el legítimo y purgar de lockfile + CI.
- Script de instalación sospechoso → no instalar; buscar alternativa o vendorizar con revisión.
- Paquete sin mantenimiento (sin releases > 12 meses) con flags → plan de migración.

## Etapa 4 — Depcheck

**Qué hace**: cruza dependencias declaradas contra imports reales del código.

**Entradas**: ficheros de declaración + fuente del proyecto.

**Salidas**: dos listas — dependencias declaradas no usadas y dependencias usadas no declaradas.

**Criterios de decisión**:
- Declarada y no usada → candidata a eliminación (regla de oro: menos es más).
- Usada y no declarada → declarar con versión fijada; si es transitiva directa, añadir a directas.
- Falsos positivos en ficheros de test/build → verificar uso en runtime antes de eliminar.

## Etapa 5 — Python (uv/pip)

**Qué hace**: audita el ecosistema Python con `pip-audit`, `safety check` y `deptry .`.

**Entradas**: `pyproject.toml`, `requirements.txt`, `uv.lock` _(ejemplos)_.

**Salidas**: vulnerabilidades por CVE con severidad, y dependencias huérfanas (deptry).

**Criterios de decisión**:
- CVE con fix disponible → actualizar a la versión mínima que resuelve el CVE.
- Paquete solo en entornos de desarrollo → mover a grupo de dev para reducir superficie.
- Dependencias huérfanas → eliminar o justificar con comentario en `pyproject.toml`.

## Etapa 6 — Rust (cargo)

**Qué hace**: audita el ecosistema Rust con `cargo audit`, `cargo outdated` y
`cargo +nightly udeps`.

**Entradas**: `Cargo.toml` + `Cargo.lock`.

**Salidas**: CVEs conocidas, dependencias desactualizadas, dependencias no usadas (udeps).

**Criterios de decisión**:
- CVE crítica en crate → actualizar de inmediato; evaluar `cargo update -p <crate>`.
- Major version disponible → revisar changelog y planificar ventana de actualización.
- Crate sin uso (udeps) → eliminar de `[dependencies]` o mover a `[dev-dependencies]` si aplica.

## Etapa 7 — Reporte unificado

**Qué hace**: consolida todos los hallazgos en un informe accionable en español.

**Entradas**: salidas de las Etapas 1–6.

**Salidas**: informe con resumen ejecutivo, vulnerabilidades por severidad, issues de
socket, dependencias no usadas y recomendaciones ordenadas por prioridad.

**Criterios de decisión**:
- Cada hallazgo debe tener: severidad, evidencia (CVE o salida de herramienta), acción concreta y esfuerzo estimado.
- Ordenar primero critical/high, después limpieza (no usadas, outdated).
- Si un ecosistema no aplica, declararlo explícitamente en el informe en lugar de omitirlo.
