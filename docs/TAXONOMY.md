# Taxonomía de dominios

El prefijo del nombre de cada skill indica su dominio. La taxonomía es cerrada: toda skill nueva debe encajar en un dominio existente o proponer uno nuevo en la PR (ver [CONTRIBUTING.md](CONTRIBUTING.md)).

| Dominio | Ámbito | Skills |
|---|---|---|
| `alignux` | Constitución, higiene y seguridad defensiva de sistemas Linux (metodología ALIGNUX) | alignux-constitucion · alignux-mantenimiento · alignux-seguridad |
| `codigo` | Calidad, seguridad y arquitectura del código | codigo-arquitectura · codigo-seguridad · dependency-audit · typescript-avanzado |
| `datos` | Bases de datos y backends serverless | datos-postgres · upstash |
| `integraciones` | Servicios externos (correo, gestores de secretos) | email-proton · protonpass |
| `proceso` | Metodologías de trabajo del agente (planificación, releases) | planificacion-archivos |
| `repo` | Ciclo de vida del repositorio: inicio, hooks, cierre | git-hooks · repo-ending · repo-starting |
| `web` | Auditoría, diseño, testing y accesibilidad web | auditoria-360-web · design-system · playwright-e2e-audit · web-audit · web-diseno · webapp-testing |

## Reglas

1. El `name` del frontmatter de `SKILL.md` es idéntico al nombre de la carpeta.
2. El campo `metadata.dominio` del frontmatter refleja esta tabla.
3. El `description` del frontmatter declara alcance y límites con referencias cruzadas (`→ otra-skill`) cuando hay solape.
4. Idioma de descripciones y docs del repo: español (`metadata.idioma: es`); se preservan términos técnicos en inglés.
