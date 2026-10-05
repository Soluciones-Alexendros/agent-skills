# Proceso de Diseño en 2 Pasadas (Design Process)

## Pasada 1: Brainstorm & Plan (Brainstorm → Plan)

### 1. Definir el Sujeto Concreto
- **¿Qué es?** Nombra una cosa concreta (no "dashboard", sí "panel de control de ventas B2B SaaS")
- **¿Para quién?** Audiencia específica (no "usuarios", sí "gestores de ventas 30-50 años, uso diario")
- **¿Cuál es el trabajo único de la página?** Una sola métrica de éxito

### 2. Token System Compacto

#### Color (4-6 hex nombrados)
```css
--color-brand: #1a73e8;      /* Primary actions, links */
--color-brand-hover: #1557b0;
--color-accent: #f59e0b;     /* Highlights, warnings */
--color-success: #10b981;
--color-error: #ef4444;
--color-surface: #ffffff;    /* Backgrounds */
--color-surface-muted: #f3f4f6;
--color-text: #111827;       /* Primary text */
--color-text-muted: #6b7280; /* Secondary text */
```

#### Tipografía (2-3 roles)
```css
--font-display: "Syne", sans-serif;     /* Headlines, characterful, restraint */
--font-body: "Inter", sans-serif;       /* Body text, readable, versatile */
--font-mono: "JetBrains Mono", monospace; /* Code, data, utility */
--font-size-scale: 1.25;                /* Major third ratio */
--line-height-body: 1.6;
--line-height-heading: 1.2;
```

#### Layout (Concepto en una frase)
> "Two-column asymmetric layout with fixed sidebar navigation and fluid content area that stacks on mobile"

#### Signature Element (El elemento único)
> "Animated gradient border on primary CTA that responds to scroll position — embodies 'dynamic growth' metaphor"

### 3. ASCII Wireframes
```
┌─────────────────────────────────────────────────┐
│  [Logo]                    [Nav] [User]         │
├──────────┬──────────────────────────────────────┤
│          │  Hero: Headline + CTA (signature)   │
│ Sidebar  │  ─────────────────────────────────  │
│ (fixed)  │  [Card Grid: 3-col desktop, 1-col]  │
│          │  [Metrics Row]                       │
└──────────┴──────────────────────────────────────┘
Mobile: Stack → [Hero] [Metrics] [Cards 1-col] [Sidebar → drawer]
```

## Pasada 2: Review contra Brief → Build

### Checklist de Unicidad (Anti-Default)
- [ ] ¿La paleta podría ser de cualquier otro proyecto? → Cambiar
- [ ] ¿La tipografía es la misma que usarías en otro brief? → Cambiar
- [ ] ¿Los numbered markers (01/02/03) tienen sentido semántico? → Solo si secuencia real
- [ ] ¿El motion es "orchestrated moment" o "scattered effects"? → Orchestrated
- [ ] ¿El signature element embodies el brief? → Sí/No → Iterar

### Decisiones Documentadas
| Decisión | Alternativa considerada | Por qué esta |
|----------|------------------------|--------------|
| Paleta azul/ámbar | Verde/rosa, monocromo | Brief: "confianza + energía" |
| Syne + Inter | Solo Inter, system fonts | Display characterful para headlines |
| Asymmetric 2-col | Simétrico 50/50 | Jerarquía visual: sidebar < content |

## Calidad Mínima (Quality Floor)
- [ ] Responsive: mobile (320) → tablet (768) → desktop (1024) → wide (1440)
- [ ] Focus visible: outline 2px, offset 2px, contrast 3:1
- [ ] Reduced motion: @media (prefers-reduced-motion: reduce) → 0.01ms
- [ ] Touch targets: 44x44px mínimo, 8px gap
- [ ] Contraste: 4.5:1 texto, 3:1 UI components