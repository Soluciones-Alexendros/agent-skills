# Taxonomía de familias

Son 17 skills en 4 familias. El campo `metadata.dominio` del frontmatter de `SKILL.md` refleja esta tabla y el prefijo del nombre es la familia (normativo, no orientativo). La taxonomía es cerrada: toda skill nueva debe encajar en una familia existente o proponer una nueva en la PR (ver [CONTRIBUTING.md](CONTRIBUTING.md)).

Las familias se alinean con las fases de ciclo de vida de ISO/IEC/IEEE 12207: diseño (`disenar`), implementación (`construir`), verificación (`verificar`) y operación (`operar`).

| Familia | Ámbito | Skills |
|---|---|---|
| `disenar` | Estructura, identidad y experiencia antes de escribir código | disenar-arquitectura · disenar-constitucion · disenar-design-system · disenar-interfaz |
| `construir` | Implementación: tipado, datos, integraciones | construir-typescript · construir-upstash · construir-proton-suite (correo Proton Mail + secretos Proton Pass) |
| `verificar` | Quality gates y auditorías | verificar-compliance · verificar-performance · verificar-owasp · verificar-fullaudit (orquestador) · verificar-repo · verificar-hooks |
| `operar` | Publicación y operación continua | operar-release · operar-lifecycle · operar-mantenimiento · operar-seguridad |

## Reglas

1. El `name` del frontmatter de `SKILL.md` es idéntico al nombre de la carpeta.
2. El campo `metadata.dominio` del frontmatter refleja esta tabla — el prefijo del nombre ES la familia (normativo, no orientativo): toda skill se nombra `<familia>-<slug>` en kebab-case sin tildes.
3. El `description` del frontmatter declara alcance y límites con referencias cruzadas (`→ otra-skill`) cuando hay solape.
4. Idioma de descripciones y docs del repo: español (`metadata.idioma: es`); se preservan términos técnicos en inglés.
