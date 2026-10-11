# Sistema Tipográfico (Typography System)

## Roles y Families

| Role | Family | Uso | Peso | Tamaño base |
|------|--------|-----|------|-------------|
| **Display** | Syne / Calibre / Fraunces | Headlines, hero, números grandes | 600-700 | clamp(2.5rem, 5vw, 4.5rem) |
| **Heading** | Syne / Display family | h1-h4, section titles | 600 | clamp(1.5rem, 3vw, 2.5rem) |
| **Body** | Inter / Source Sans / DM Sans | Paragraphs, UI text, forms | 400-500 | 1rem (16px) |
| **Caption/Utility** | JetBrains Mono / Fira Code | Code, data, labels, timestamps | 400-500 | 0.875rem |

## Type Scale (Major Third = 1.25)

```css
:root {
  --scale: 1.25;
  --text-xs: 0.75rem;      /* 12px */
  --text-sm: 0.875rem;     /* 14px */
  --text-base: 1rem;       /* 16px */
  --text-lg: 1.125rem;     /* 18px */
  --text-xl: 1.25rem;      /* 20px */
  --text-2xl: 1.563rem;    /* 25px */
  --text-3xl: 1.953rem;    /* 31px */
  --text-4xl: 2.441rem;    /* 39px */
  --text-5xl: 3.052rem;    /* 49px */
  --text-6xl: 3.815rem;    /* 61px */
}
```

## Weights & Usage
- **Light (300)**: Solo display grande, evitar en body
- **Regular (400)**: Body text, paragraphs, UI labels
- **Medium (500)**: Emphasis inline, button text, form labels
- **Semibold (600)**: Headings, strong emphasis, card titles
- **Bold (700)**: Display, hero numbers, primary CTAs

## Line Height & Spacing
```css
--leading-tight: 1.1;      /* Display, headlines */
--leading-snug: 1.25;      /* Headings */
--leading-normal: 1.5;     /* Body text */
--leading-relaxed: 1.625;  /* Long-form reading */
--leading-loose: 2;        /* Captions, metadata */
```

## Letter Spacing
```css
--tracking-tighter: -0.05em;  /* Display large */
--tracking-tight: -0.025em;   /* Headlines */
--tracking-normal: 0;         /* Body */
--tracking-wide: 0.025em;     /* Captions, labels */
--tracking-wider: 0.05em;     /* Uppercase, button text */
```

## Responsive Clamp Examples
```css
/* Display hero */
font-size: clamp(2.5rem, 5vw + 1rem, 5rem);
letter-spacing: -0.03em;

/* Section heading */
font-size: clamp(1.5rem, 2vw + 1rem, 2.5rem);
letter-spacing: -0.015em;

/* Body responsive */
font-size: clamp(0.875rem, 0.9vw + 0.75rem, 1.125rem);
```

## Dark Mode Adjustments
```css
@media (prefers-color-scheme: dark) {
  --font-smoothing: antialiased;
  /* Slight weight increase for readability on dark */
  .text-body { font-weight: 400; } /* not 300 */
}
```

## Font Loading Optimization
```html
<!-- Preload critical fonts -->
<link rel="preload" href="/fonts/syne-600.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/fonts/inter-400.woff2" as="font" type="font/woff2" crossorigin>

<!-- font-display: swap for non-critical -->
@font-face {
  font-family: 'Syne';
  src: url('/fonts/syne-600.woff2') format('woff2');
  font-weight: 600;
  font-display: swap;
}
```

## Anti-Patterns
- ❌ 3+ font families
- ❌ Light weight (300) para body text
- ❌ Line height < 1.5 en body text
- ❌ Letter-spacing positivo en body text
- ❌ Más de 3 pesos en uso simultáneo
- ❌ Font-size fija en px sin clamp()