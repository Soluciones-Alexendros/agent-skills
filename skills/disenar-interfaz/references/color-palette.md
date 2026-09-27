# Paleta de Colores (Color Palette)

## Estructura: 4-6 Hex Nombrados

```css
:root {
  /* Brand / Primary */
  --color-brand: #1a73e8;
  --color-brand-hover: #1557b0;
  --color-brand-light: #dbeafe;
  --color-brand-muted: #93c5fd;

  /* Accent / Secondary */
  --color-accent: #f59e0b;
  --color-accent-hover: #d97706;
  --color-accent-light: #fef3c7;

  /* Semantic */
  --color-success: #10b981;
  --color-success-light: #d1fae5;
  --color-warning: #f59e0b;
  --color-warning-light: #fef3c7;
  --color-error: #ef4444;
  --color-error-light: #fee2e2;

  /* Neutral / Surface */
  --color-surface: #ffffff;
  --color-surface-muted: #f3f4f6;
  --color-surface-elevated: #ffffff;
  --color-border: #e5e7eb;
  --color-border-strong: #d1d5db;

  /* Text */
  --color-text: #111827;
  --color-text-muted: #6b7280;
  --color-text-inverse: #ffffff;
  --color-text-link: #1a73e8;
}
```

## Dark Mode
```css
@media (prefers-color-scheme: dark) {
  :root {
    --color-brand: #3b82f6;
    --color-brand-hover: #60a5fa;
    --color-brand-light: #1e3a5f;
    --color-brand-muted: #1e40af;

    --color-accent: #fbbf24;
    --color-accent-hover: #f59e0b;
    --color-accent-light: #422006;

    --color-success: #34d399;
    --color-success-light: #064e3b;
    --color-warning: #fbbf24;
    --color-warning-light: #422006;
    --color-error: #f87171;
    --color-error-light: #7f1d1d;

    --color-surface: #111827;
    --color-surface-muted: #1f2937;
    --color-surface-elevated: #1f2937;
    --color-border: #374151;
    --color-border-strong: #4b5563;

    --color-text: #f9fafb;
    --color-text-muted: #9ca3af;
    --color-text-inverse: #111827;
    --color-text-link: #60a5fa;
  }
}
```

## Contraste WCAG AA/AAA

| Elemento | Ratio AA | Ratio AAA |
|----------|----------|-----------|
| Texto normal (≥16px) | 4.5:1 | 7:1 |
| Texto grande (≥18px bold, ≥24px) | 3:1 | 4.5:1 |
| UI Components (bordes, iconos) | 3:1 | 4.5:1 |
| Focus indicator | 3:1 | 4.5:1 |

## Verificación Rápida
```bash
# Contrast checker
# https://webaim.org/resources/contrastchecker/
# Input: foreground (text) + background
```

## Uso Semántico (No Color-Only)
```tsx
// ❌ MALO: Solo color
<button style={{color: 'red'}}>Eliminar</button>

// ✅ BUENO: Color + icono + texto
<button aria-label="Eliminar elemento">
  <TrashIcon aria-hidden="true" />
  Eliminar
</button>

// ✅ BUENO: Estados de formulario
<input aria-invalid="true" aria-describedby="error-msg" />
<span id="error-msg" role="alert">Email inválido</span>
```

## Paletas de Ejemplo por Tipo de Producto

### SaaS B2B (Confianza + Profesional)
```css
--brand: #1e40af;    /* Azul profundo */
--accent: #059669;   /* Verde esmeralda */
--surface: #f8fafc;
```

### Creative/Portfolio (Expresivo + Personal)
```css
--brand: #7c3aed;    /* Púrpura vibrante */
--accent: #f59e0b;   /* Ámbar cálido */
--surface: #fafafa;
```

### E-commerce (Conversión + Confianza)
```css
--brand: #dc2626;    /* Rojo urgencia controlada */
--accent: #ea580c;   /* Naranja acción */
--surface: #fff;
```

### Developer Tools (Técnico + Limpio)
```css
--brand: #0891b2;    /* Cian técnico */
--accent: #64748b;   /* Slate neutro */
--surface: #0f172a;  /* Dark default */
```