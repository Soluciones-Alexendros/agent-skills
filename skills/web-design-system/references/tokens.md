# Tokens de diseño — DTCG, Style Dictionary, Figma/Tokens Studio

Pipeline de tokens: diseñar en Figma, exportar en formato DTCG (`tokens.json`),
transformar con Style Dictionary (o `design-tokens` CLI) a `tokens.css` / `tokens.ts`,
consumir desde Tailwind v4 (`@theme`) y componentes.

## Formato DTCG (`tokens.json`)

```json
{
  "color": {
    "primary": { "$value": "oklch(55% 0.15 264)", "$type": "color" },
    "background": { "$value": "{color.neutral.50}", "$type": "color" }
  },
  "spacing": {
    "md": { "$value": "1rem", "$type": "dimension" }
  }
}
```

- Claves `$value` / `$type`; referencias con `{grupo.token}`.
- Tokens **semánticos** (`color.background`, `color.foreground`) sobre **primitivos**
  (`color.neutral.50`): retematizar = cambiar el mapeo, no los componentes.
- Nada hardcodeado en componentes: todo vía token o utilidad Tailwind que lo consuma.

## Style Dictionary

- Origen: uno o varios JSON DTCG; destinos: CSS (`:root` + `.dark`), TS, JSON plano.
- Comandos típicos (proyecto consumidor, no de esta skill):
  `npx style-dictionary build --config sd.config.json`.
- Reglas: nombres `kebab-case` en CSS (`--color-primary`), `camelCase` en TS;
  documentar en `DESIGN.md` _(ejemplo: artefacto generado)_ qué token alimenta a qué utilidad.

## Figma Tokens / Tokens Studio

- Fuente de verdad visual: sets `global` (primitivos) + `semantic` (light/dark).
- Sync: Tokens Studio → GitHub (`tokens.json` en el repo); la CI regenera `tokens.css`.
- Ante conflicto Figma ↔ código: manda el JSON versionado en el repo; Figma se re-sincroniza.

## `design-tokens` CLI

- Alternativa ligera a Style Dictionary para extraer/validar/transformar `tokens.json`.
- Uso: validar DTCG en CI (`design-tokens validate`), exportar a CSS/TS por plataforma.
- Si el proyecto no lo tiene instalado, documentarlo como dependencia propuesta, no inventar flags.

## Consumo en Tailwind v4

```css
@import "tailwindcss";

@theme inline {
  --color-primary: var(--color-primary);
  --spacing-md: var(--spacing-md);
}
```

Ver `references/modern-css.md` para el setup completo con `@tailwindcss/vite`.

## Gate de accesibilidad

Verificar contraste WCAG AA en cada par semántico (texto/fondo) con la matriz de
`web-compliance` (`scripts/contrast.py` como referencia de cálculo). 0 violaciones
AA antes de entregar el set de tokens.
