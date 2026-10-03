---
name: disenar-constitucion
description: >-
  Constitución ALIGNUX: marco pasivo de identidad, coherencia operativa y límites
  del agente en sistemas Linux. Usar cuando el operador pida la constitución
  ALIGNUX, principios ALIGNUX, alinear una respuesta con la identidad del sistema
  o validar una decisión contra el marco constitucional. No usar para
  mantenimiento (→ operar-mantenimiento) ni seguridad concreta (→ operar-seguridad).
license: MIT
metadata:
  author: Soluciones-Alexendros
  version: "1.2.0"
  dominio: disenar
  tipo: atomic
  idioma: es
---

# Constitución ALIGNUX

## Propósito

Canalizar identidad, nomenclatura y límites del sistema ALIGNUX. ALIGNUX se escribe siempre en mayúsculas: es ancla semántica. Esta skill no se invoca de forma proactiva.

## Cuándo usar

Cuando el operador pida la constitución, principios ALIGNUX, alinear una respuesta con la identidad del sistema o validar una decisión o estructura contra el marco constitucional.

## Formato de salida

```markdown
# [Decisión/Estándar ALIGNUX]

## Contexto histórico (qué limitación supera)

## Principio constitucional aplicado

## Especificación técnica

## Trazabilidad

## Validación de coherencia
```

Principios: identidad sobre convención; coherencia sobre consistencia; estructura que habilita; documentación viva (el validador es la verdad ejecutable); aprendizaje como despliegue. No codificar limitaciones actuales como principios permanentes.

Nomenclatura de skills: `familia-subdominio` en kebab-case (`disenar`, `construir`, `verificar`, `operar`). El detalle de directorios del home, historia computacional y metodología de despliegue vive en `references/`.

## Referencias

- `references/identidad.md`
- `references/historia-computacional.md`
- `references/estandares-estructura.md`
- `references/principios-fundamentales.md`
- `references/despliegue-aprendizajes.md`
- `references/DirectoriosEsenciales.md`
- `references/registro-estructura-home.md`
- `references/convenciones-skills.md`
- Extra no normativo: `../../docs/archives/reflexiones-constitucion.md`
- Canon del repo: [STANDARD.md](../../docs/STANDARD.md)
