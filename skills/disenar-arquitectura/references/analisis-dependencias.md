# Análisis de dependencias: dependency-cruiser y madge

Tooling 2024-26 para el mapa objetivo de dependencias que alimenta la fase «Explorar» del SKILL. Ambas herramientas trabajan sobre imports estáticos, sin ejecutar el código.

## dependency-cruiser

[dependency-cruiser](https://github.com/sverweij/dependency-cruiser) valida reglas de dependencia y emite grafos. Es la herramienta de **gobierno** (rules-as-code); madge es la de **visualización rápida**.

```bash
npx dependency-cruiser --init          # genera .dependency-cruiser.json
npx dependency-cruiser src --validate .dependency-cruiser.json
npx dependency-cruiser src --output-type dot | dot -T svg > deps.svg
```

Reglas útiles para detectar fricción arquitectónica:

| Regla | Qué detecta |
|---|---|
| `no-circular` | Ciclos entre módulos (candidatos a fusión o a seam nuevo) |
| `no-orphans` | Módulos huérfanos (nadie los importa: ¿código muerto o seam sin usar?) |
| `not-to-unresolvable` / `no-duplicate-dep-types` | Imports rotos y tipos duplicados |
| `not-to-test` / `not-to-spec` | Fugas de código de test a producción |
| Restricciones por carpeta (`from`/`to` con `path`) | Capas que se saltan (p. ej. `ui/` importando `db/` directamente = leak across the seam) |

Ejemplo de regla de capas (la interfaz no se salta):

```jsonc
// .dependency-cruiser.json (extracto)
{
  "forbidden": [
    {
      "name": "ui-no-db-directo",
      "severity": "error",
      "from": { "path": "^src/ui" },
      "to": { "path": "^src/db" },
    },
    { "name": "sin-ciclos", "severity": "error", "from": {}, "to": { "circular": true } },
  ],
}
```

Integra la validación en CI (`verificar-hooks`/`operar-release`): un ciclo nuevo rompe el build igual que un test.

## madge

[madge](https://github.com/pahen/madge) genera el grafo de dependencias y detecta ciclos con un solo comando. Es la herramienta de **exploración rápida** antes de configurar reglas:

```bash
npx madge --circular src/        # lista ciclos
npx madge --image graph.svg src/ # grafo visual
npx madge --orphans src/         # módulos sin importadores
```

Soporta TypeScript, JSX y alias de paths (lee `tsconfig.json`). Úsalo en la primera pasada de «Explorar»; cuando un hallazgo deba perdurar, conviértelo en regla de dependency-cruiser.

## Flujo recomendado

1. `madge --circular` + `--orphans`: fricción visible en 1 minuto.
2. Convierte cada hallazgo estructural en regla `forbidden` de dependency-cruiser.
3. Adjunta el SVG del grafo (antes/después) a la tarjeta del candidato en el informe HTML.
4. Registra la decisión de fronteras en un ADR (`plantilla-adr.md`).
