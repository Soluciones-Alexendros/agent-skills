# Taxonomía de dominios

El prefijo del nombre de cada skill indica su dominio. La taxonomía es cerrada: toda skill nueva debe encajar en un dominio existente o proponer uno nuevo en la PR (ver [CONTRIBUTING.md](CONTRIBUTING.md)).

| Dominio | Ámbito | Skills |
|---|---|---|
| `alignux` | Constitución ALIGNUX | alignux-constitucion |
| `codigo` | Calidad y arquitectura del código | codigo-arquitectura · typescript-avanzado |
| `datos` | Bases de datos y backends serverless | upstash |
| `integraciones` | Servicios externos (correo, gestores de secretos) | email-proton · protonpass |
| `linux` | Mantenimiento y seguridad defensiva de sistemas Linux | linux-mantenimiento · linux-seguridad |
| `repo` | Ciclo de vida del repositorio: inicio, hooks, cierre | repo-ending · repo-precommit · repo-starting |
| `web` | Auditoría, diseño, testing, seguridad, rendimiento y accesibilidad web | web-compliance · web-diseno · web-playwright · web-rendimiento · web-seguridad · webapp-testing · design-system |

## Reglas

1. El `name` del frontmatter de `SKILL.md` es idéntico al nombre de la carpeta.
2. El campo `metadata.dominio` del frontmatter refleja esta tabla.
3. El `description` del frontmatter declara alcance y límites con referencias cruzadas (`→ otra-skill`) cuando hay solape.
4. Idioma de descripciones y docs del repo: español (`metadata.idioma: es`); se preservan términos técnicos en inglés.