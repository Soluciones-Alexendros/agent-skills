# Modelado C4 con Structurizr

Modelado 2024-26 para comunicar la arquitectura antes/después sin dibujar cajas a mano. El modelo C4 vive como código (versionable, diffable); Structurizr lo renderiza.

## Niveles C4 (solo los que aporten)

| Nivel | Alcance | Cuándo usarlo en esta skill |
|---|---|---|
| **Context** | Sistema + actores + sistemas externos | Para situar el módulo profundizado en su entorno |
| **Container** | Apps, BBDD, servicios ejecutables | Para fugas entre contenedores (el seam duele aquí) |
| **Component** | Módulos dentro de un contenedor | Nivel de trabajo habitual de los candidatos |
| **Code** | Clases/funciones | Solo si el deepening baja hasta aquí |

No dibujes los 4 niveles por defecto: la mayoría de candidatos viven en **Component** con contexto de **Container**.

## Structurizr DSL (ejemplo mínimo)

[Structurizr DSL](https://structurizr.com/dsl) define modelo + vistas en texto:

```dsl
workspace {
    model {
        user = person "Usuario"
        shop = softwareSystem "Tienda" {
            web = container "Web" {
                intake = component "Order intake" "Recibe pedidos"
                pricing = component "Pricing" "Calcula precios"
            }
            db = container "Postgres" "Pedidos y precios"
        }
        intake -> pricing "usa"
        intake -> db "lee/escribe"
    }
    views {
        component shop web {
            include *
            autolayout lr
        }
    }
}
```

Renderiza con Structurizr Lite (`docker run structurizr/lite`) o exporta SVG/PNG para incrustar en el informe HTML de la skill.

## Alternativas sin servidor

- **Mermaid** (ya usado en el informe): `flowchart`/`C4Context` para diagramas rápidos inline.
- **PlantUML + C4-PlantUML**: si el equipo ya usa PlantUML en docs.
- **Structurizr**: cuando el modelo deba evolucionar con el código (un DSL versionado gana a PNGs sueltos).

## Regla de uso

Un diagrama C4 por informe como máximo (nivel Container del antes/después de la recomendación principal). Los candidatos individuales usan los patrones de `html-report.md`; C4 es para el marco, no para cada tarjeta.
