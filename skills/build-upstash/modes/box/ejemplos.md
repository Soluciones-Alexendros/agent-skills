# Ejemplos Box (ES)

> Ejemplos mínimos del modo `box`. Detalle en `references/box.md`.

## Crear box y ejecutar shell

```typescript
import { Box } from "@upstash/box";

const box = await Box.create({ name: "dev-1", runtime: "node", size: "small" });
const out = await box.shell.exec("node --version && ls");
console.log(out.stdout);
```

## Snapshot y recreación

```typescript
const snap = await box.snapshot.create("base-limpia");
// ... experimentar ...
await box.snapshot.restore(snap.id);
```

## Python (espejo snake_case)

```python
from upstash_box import Box

box = Box.create(name="dev-1", runtime="python", size="small")
out = box.shell.exec("python --version")
print(out.stdout)
```
