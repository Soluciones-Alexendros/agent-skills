# CSS moderno para design systems — Tailwind v4, Layers, Queries, Anchor

## Tailwind v4 + Oxc + `@tailwindcss/vite`

- Configuración CSS-first: `@theme` en CSS sustituye a `tailwind.config.ts`.
- Plugin Vite oficial: `@tailwindcss/vite` (compilación con Oxc, sin PostCSS dedicado).
- Dark mode por clase: `@custom-variant dark (&:where(.dark, .dark *));`.
- Animaciones: `@keyframes` dentro de `@theme` + variables `--animate-*`;
  `@starting-style` para transiciones de entrada.
- Migración v3 → v4: ver guía oficial de upgrade (externo); no inventar codemods.

## CSS Cascade Layers

```css
@layer tokens, reset, base, components, utilities;
```

- Orden explícito: tokens < reset < base < componentes < utilidades.
- Tailwind v4 emite sus capas (`theme`, `base`, `components`, `utilities`); importar
  estilos propios en capas posteriores para no luchar en especificidad.
- Regla: ningún `!important` para ganar a una utilidad; reordenar capas en su lugar.

## Container Queries

```css
.card { container-type: inline-size; }
@container (min-width: 24rem) {
  .card-body { display: grid; grid-template-columns: 1fr 1fr; }
}
```

- En Tailwind v4: `@container` / `@md:` sobre el contenedor marcado.
- Usar para componentes que se reutilizan en superficies de distinto ancho
  (sidebar vs main, grid vs lista); los media queries globales no sirven ahí.

## Anchor Positioning

```css
#trigger { anchor-name: --menu; }
#menu {
  position: absolute;
  position-anchor: --menu;
  top: anchor(bottom);
  left: anchor(left);
}
```

- Para tooltips, popovers, menús y dropdowns del sistema sin JS de posicionado.
- Fallback: `@supports (position-anchor: --x)`; sin soporte, posicionado absoluto clásico.
- Respetar `prefers-reduced-motion` en cualquier animación de apertura.

## OKLCH y color relativo

- Paletas en OKLCH (ya usadas en `references/tailwind-source.md`): perceptual,
  gamut P3, interpolación uniforme para escalas y estados hover.
- `color-mix(in oklch, var(--color-primary) 90%, transparent)` para estados
  sin multiplicar tokens; color relativo `oklch(from …)` para derivados.
