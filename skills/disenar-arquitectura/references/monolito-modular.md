# Patrones de monolito modular

Patrones 2024-26 para profundizar módulos **sin** saltar a microservicios. El monolito modular es el destino por defecto de la mayoría de candidatos: fronteras explícitas, despliegue único.

## Principios

1. **Un módulo = un concepto de dominio** (`CONTEXT.md` le da nombre). Si no puedes nombrarlo con el glosario, no es un módulo todavía.
2. **Toda comunicación inter-módulo pasa por la interfaz pública** del módulo (`index.ts` / `__init__.py` / `api/`). Imports profundos (`from orders.internals.x import …`) = leak across the seam.
3. **La BBDD no es la interfaz**: compartir tablas entre módulos es acoplamiento oculto. Cada módulo posee sus tablas; lo demás va por API de módulo o eventos.
4. **Un adapter hipotético no justifica un seam** («one adapter = hypothetical seam, two = real»): no crees puertos para un futuro que no existe.

## Patrones

### Módulo con fachada (default)

```
orders/
├── api.py            # interfaz pública: lo único importable desde fuera
├── models.py         # dominio interno
├── service.py        # implementación
└── tests/            # tests contra api.py (la interfaz es la superficie de test)
```

Regla dependency-cruiser: prohibir imports a `orders/*` excepto `orders/api.py`.

### Eventos de dominio (desacoplar escrituras)

Cuando dos módulos necesitan reaccionar al mismo hecho sin llamarse:

```python
# orders/api.py publica; billing se suscribe. Ni billing importa orders,
# ni orders importa billing: el evento es el seam.
bus.publish(OrderPaid(order_id=..., amount=...))
```

Empieza en proceso (bus en memoria, un adapter). Extraer a broker (segundo adapter) solo cuando el volumen o el despliegue lo exijan: dos adapters = seam real.

### Shared kernel mínimo (excepción, no norma)

Solo tipos-valor inmutables y ubicuos (Money, Email, IDs). Nada con comportamiento de dominio. Si el kernel crece, es señal de conceptos sin nombrar: vuelve a `CONTEXT.md`.

### Rutas de escape (cuándo NO modularizar)

- Prototipo desechable: el test de borrado dice que todo es somero → no modularices, borra.
- Dos módulos con releases siempre sincronizados y un solo equipo: una carpeta bien nombrada basta; el seam puede esperar al segundo adapter.

## Antipatrones

| Síntoma | Diagnóstico |
|---|---|
| `utils/` o `common/` importado por todos | Conceptos sin nombrar; reparte por dominio o borra |
| Imports circulares entre módulos | Un solo módulo disfrazado de dos: fusiona (verifica con `madge --circular`) |
| Tests que mockean 5 módulos internos | Interfaz somera; profundiza hasta testear por la fachada |
| Tablas compartidas «por rendimiento» | Deuda explícita: registra ADR con el coste y el plan de pago |
