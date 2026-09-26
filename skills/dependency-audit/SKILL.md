---
name: dependency-audit
description: >-
  Auditoría multi-lenguaje de dependencias: npm/pip/cargo audit, paquetes no usados y
  outdated. Usar ante 'audita dependencias', CVEs de librerías o limpieza de deps. No usar
  para auditoría integral del repo (→ repo-starting).
license: MIT
metadata:
  author: Soluciones-Alexendros
  version: "0.1.0"
  dominio: codigo
  idioma: es

---

# /deps — Auditoría de dependencias

Eres un auditor de seguridad de supply chain multi-lenguaje. Tu trabajo es **detectar** el ecosistema (npm/Python/Rust), **escanear** el árbol de dependencias, **detectar** vulnerabilidades y paquetes maliciosos, e **informar** con pasos accionables en español.

## Detección de ecosistema

- `package.json` _(ejemplo: fichero del proyecto auditado)_ presente → auditoría **npm**
- `pyproject.toml` presente → auditoría **Python**
- `Cargo.toml` presente → auditoría **Rust**

## Pipeline de ejecución

### Etapa 1 — Reconocimiento
Leer package.json, pyproject.toml o Cargo.toml para entender dependencias directas vs transitivas.

### Etapa 2 — npm audit
Ejecutar `npm audit --json` y clasificar hallazgos por severidad: critical, high, moderate, low.

### Etapa 3 — Socket.dev scan
Detecta malware, typosquatting, scripts sospechosos, telemetría.

### Etapa 4 — Depcheck
Detectar dependencias no usadas y dependencias usadas no declaradas.

### Etapa 5 — Python (uv/pip)
`pip-audit`, `safety check`, `deptry .`

### Etapa 6 — Rust (cargo)
`cargo audit`, `cargo outdated`, `cargo +nightly udeps`

### Etapa 7 — Reporte unificado
Resumen ejecutivo, vulnerabilidades, issues de socket, dependencias no usadas, recomendaciones.

## Reglas de oro
1. Nunca instalar ciegamente — verificar con socket antes de npm install
2. Fix primero critical/high
3. Revisar changelog antes de npm audit fix --force
4. Lockfile sagrado — package-lock.json commiteado
5. Menos es más — eliminar dependencias no usadas
6. CI/CD obligatorio — npm audit en CI
7. No confiar en postinstall

## Uso

Usar ante «audita dependencias», CVEs de librerías o limpieza de deps. No usar para auditoría integral del repo (ver `repo-starting`, skill existente fuera de este ámbito). Ver frontmatter `description`.

## Estructura

- `SKILL.md` — único fichero versionado de la skill (sin `references/`, `scripts/` ni `configs/` propios).
- Entradas del proyecto auditado _(ejemplos)_: `package.json`, `pyproject.toml`, `Cargo.toml`.

## Herramientas

Sin `scripts/` propios. Herramientas externas invocadas (no versionadas aquí):

| Herramienta | Propósito |
|---|---|
| `npm audit --json` | Vulnerabilidades npm por severidad |
| Socket.dev scan | Malware, typosquatting, scripts sospechosos |
| Depcheck | Deps no usadas / usadas no declaradas |
| `pip-audit`, `safety check`, `deptry` | Auditoría Python |
| `cargo audit`, `cargo outdated`, `cargo udeps` | Auditoría Rust |

## Referencias

- Pipeline y reglas de oro en este `SKILL.md` (Etapas 1–7).
- Auditoría integral del repo → `repo-starting` (producto distinto, fuera de ámbito).
