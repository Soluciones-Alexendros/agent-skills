# Plantilla ADR (Architecture Decision Record)

Plantilla para registrar las decisiones del bucle de grilling y los rechazos con razón de peso. Un ADR por fichero en `docs/adr/` del proyecto objetivo: `docs/adr/NNNN-titulo-corto.md`.

```markdown
# ADR-NNNN: <título corto de la decisión>

Fecha: AAAA-MM-DD · Estado: propuesta | aceptada | rechazada | superseded-by ADR-MMMM

## Contexto

Qué fricción la motiva y qué módulos/ficheros toca. Enlaza el informe
`architecture-review-<timestamp>.html` y la tarjeta candidata si existe.

## Decisión

Qué se decidió, en una o dos frases, con vocabulario de dominio
(`CONTEXT.md`) y de arquitectura (módulo, interfaz, seam, adapter).

## Alternativas consideradas

1. <alternativa> — descartada porque <razón de peso>.
2. <alternativa> — descartada porque <razón de peso>.

## Consecuencias

- Positivas: <locality/leverage/testabilidad ganada>.
- Negativas: <coste, acoplamiento aceptado, deuda reconocida>.
- Reglas de dependency-cruiser que la protegen (ver `analisis-dependencias.md`).
```

## Convenciones

- **Numeración**: secuencial `0001, 0002…`; nunca reutilizar números.
- **Estado**: `propuesta` hasta que el usuario la apruebe; entonces `aceptada`. Un rechazo con razón de peso se registra como `rechazada` (evita que futuras revisiones la re-sugieran).
- **Idioma**: español; términos de glosario en su forma canónica.
- **Tamaño**: 1 página; si necesita más, la decisión no está madura: vuelve al grilling.
