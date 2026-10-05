# Layout & Motion (Layout & Motion)

## Layout Concept (En una frase)
> "Describe el concepto de layout en una frase: ej. 'Two-column asymmetric con sidebar fija y content fluido que apila en mobile'"

## ASCII Wireframes (Mobile → Desktop)

### Mobile First (320px+)
```
┌─────────────────────┐
│ [Logo] [Menu]       │  Header
├─────────────────────┤
│                     │
│   Hero: Headline    │  Hero section
│   Subheadline       │
│   [CTA Primary]     │
│                     │
├─────────────────────┤
│  [Métrica 1]        │  Metrics row
│  [Métrica 2]        │
│  [Métrica 3]        │
├─────────────────────┤
│  Card 1             │  Cards stack
│  Card 2             │
│  Card 3             │
├─────────────────────┤
│  Footer             │
└─────────────────────┘
```

### Tablet (768px+)
```
┌─────────────────────────────────────┐
│ [Logo]              [Nav] [User]    │
├─────────────────────────────────────┤
│ Hero: Headline + Sub + [CTA]        │
├─────────────────────────────────────┤
│ [Met1] [Met2] [Met3] [Met4]         │  Metrics 4-col
├─────────────────────────────────────┤
│ Card 1    Card 2    Card 3          │  Cards 3-col
├─────────────────────────────────────┤
│ Footer                              │
└─────────────────────────────────────┘
```

### Desktop (1024px+)
```
┌──────────┬──────────────────────────────────┐
│ Sidebar  │ Hero: Headline + Sub + [CTA]     │
│ (fixed)  │ ──────────────────────────────── │
│          │ [Met1] [Met2] [Met3] [Met4]      │
│          │ ──────────────────────────────── │
│          │ Card 1  Card 2  Card 3  Card 4   │  4-col
│          │ Card 5  Card 6                   │
└──────────┴──────────────────────────────────┘
```

## Grid System
```css
:root {
  --container-max: 1200px;
  --container-wide: 1400px;
  --gutter: 1.5rem;        /* 24px */
  --gutter-sm: 1rem;       /* 16px */
  --columns: 12;
}

/* Container */
.container {
  width: 100%;
  max-width: var(--container-max);
  margin: 0 auto;
  padding: 0 var(--gutter);
}

.container-wide {
  max-width: var(--container-wide);
}

/* Grid utility */
.grid {
  display: grid;
  gap: var(--gutter);
}

.grid-cols-1 { grid-template-columns: 1fr; }
.grid-cols-2 { grid-template-columns: repeat(2, 1fr); }
.grid-cols-3 { grid-template-columns: repeat(3, 1fr); }
.grid-cols-4 { grid-template-columns: repeat(4, 1fr); }

/* Responsive */
@media (max-width: 768px) {
  .grid-cols-2, .grid-cols-3, .grid-cols-4 { grid-template-columns: 1fr; }
}
```

## Breakpoints
```css
/* Mobile First */
--bp-sm: 640px;    /* Large phones */
--bp-md: 768px;    /* Tablets */
--bp-lg: 1024px;   /* Desktop */
--bp-xl: 1280px;   /* Large desktop */
--bp-2xl: 1536px;  /* Wide */

/* Media queries (mobile-first) */
@media (min-width: 640px) { /* sm */ }
@media (min-width: 768px) { /* md */ }
@media (min-width: 1024px) { /* lg */ }
@media (min-width: 1280px) { /* xl */ }
```

## Motion (Animación)

### Stack moderno

- **motion-one** (Motion One): API mínima (`animate`, `scroll`, `inView`) para microinteracciones y motion por scroll con poco JS. Preferirla para one-shots y reveals.
- **framer-motion v11** (Motion): layouts animados (`layoutId`), gestos (`whileHover`/`whileTap`), `AnimatePresence` y `useScroll`/`useTransform` en stacks React.
- **Scroll-driven Animations** (CSS nativo): `animation-timeline: scroll() | view()` + `animation-range` para parallax, progress bars y reveals sin JS. Fallback: IntersectionObserver + clase.
- **View Transitions API**: `document.startViewTransition()` para transiciones de página/vista SPA y MPA (`@view-transition`); envolver en `@supports` y respetar `prefers-reduced-motion`.
- **Anchor Positioning**: tooltips/popovers anclados en CSS puro (`anchor-name`, `position-anchor`); ver `build-design-system`.
- **Color moderno**: OKLCH, `color-mix()`, color relativo `oklch(from …)` para escalas y estados sin multiplicar tokens.

### Duraciones Estándar
```css
:root {
  --duration-instant: 0ms;      /* No animation */
  --duration-fast: 100ms;       /* Hover, tap feedback */
  --duration-normal: 200ms;     /* Transitions, fade */
  --duration-slow: 300ms;       /* Complex, modal enter */
  --duration-page: 500ms;       /* Page transitions */
}
```

### Easing
```css
:root {
  --ease-linear: linear;
  --ease-out: cubic-bezier(0.25, 0.46, 0.45, 0.94);    /* Default */
  --ease-in: cubic-bezier(0.55, 0.055, 0.675, 0.19);
  --ease-in-out: cubic-bezier(0.42, 0, 0.58, 1);
  --ease-bounce: cubic-bezier(0.68, -0.55, 0.265, 1.55); /* Playful */
}
```

### Motion Principles
- **Propósito**: Cada animación tiene razón (feedback, orientación, deleite)
- **Performance**: Solo `transform` y `opacity` para 60fps
- **Duración**: Proporcional a distancia/complejidad
- **Orquestación**: Un momento coreografiado > efectos dispersos

### Reduced Motion
```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

## Signature Element Motion (Ejemplo)
```css
/* Signature: Gradient border que responde a scroll */
.cta-signature {
  position: relative;
  border: 2px solid transparent;
  background: linear-gradient(var(--surface), var(--surface)) padding-box,
              linear-gradient(90deg, var(--brand), var(--accent)) border-box;
  transition: border-image-source var(--duration-normal) var(--ease-out);
}

.cta-signature.scrolled {
  border-image-source: linear-gradient(90deg, var(--accent), var(--brand));
}

/* JS: Toggle class on scroll threshold */
```