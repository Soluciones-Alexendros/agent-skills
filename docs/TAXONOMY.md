# Taxonomía de dominios

Son 18 skills en 7 dominios. El campo `metadata.dominio` del frontmatter de `SKILL.md` manda; el prefijo del nombre es orientativo (p. ej. `email-proton` y `protonpass` pertenecen a `integraciones`, `upstash` a `datos`). La taxonomía es cerrada: toda skill nueva debe encajar en un dominio existente o proponer uno nuevo en la PR (ver [CONTRIBUTING.md](CONTRIBUTING.md)).

| Dominio | Ámbito | Skills |
|---|---|---|
| `alignux` | Constitución ALIGNUX | alignux-constitucion |
| `codigo` | Calidad y arquitectura del código | codigo-arquitectura · codigo-typescript |
| `datos` | Bases de datos y backends serverless | upstash (router + 7 modos: `redis`, `vector`, `search`, `queue`, `ratelimit`, `blob`, `box`) |
| `integraciones` | Servicios externos (correo, gestores de secretos) | email-proton · protonpass |
| `linux` | Mantenimiento y seguridad defensiva de sistemas Linux | linux-mantenimiento · linux-seguridad |
| `repo` | Ciclo de vida del repositorio: audit, hooks, release | repo-audit · repo-hooks · repo-release · repo-lifecycle (enrutador audit/hooks/release) |
| `web` | Auditoría, diseño, seguridad, rendimiento y compliance web | web-compliance · web-performance · web-fullaudit (orquestador) · web-seguridad · web-design-system · web-diseno |

## Reglas

1. El `name` del frontmatter de `SKILL.md` es idéntico al nombre de la carpeta.
2. El campo `metadata.dominio` del frontmatter refleja esta tabla (manda sobre el prefijo).
3. El `description` del frontmatter declara alcance y límites con referencias cruzadas (`→ otra-skill`) cuando hay solape.
4. Idioma de descripciones y docs del repo: español (`metadata.idioma: es`); se preservan términos técnicos en inglés.
