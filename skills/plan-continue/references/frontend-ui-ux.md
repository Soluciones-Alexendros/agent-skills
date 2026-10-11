# Pulido de frontend: checklist UI/UX

Aplicar en la Fase 6 cuando el repositorio tiene interfaz de usuario. Verificar visualmente (capturas con navegador) siempre que sea posible: el CSS que se lee bien puede renderizarse mal.

## Contenido

- [Accesibilidad (WCAG 2.2 AA)](#accesibilidad)
- [Estados de interfaz](#estados-de-interfaz)
- [Consistencia visual](#consistencia-visual)
- [Responsive y layout](#responsive-y-layout)
- [Rendimiento percibido](#rendimiento-percibido)
- [Interacción y feedback](#interaccion-y-feedback)
- [Contenido y microcopy](#contenido-y-microcopy)
- [Puente al informe](#puente-al-informe)

## Accesibilidad

- Contraste de texto ≥4.5:1 (≥3:1 en texto grande); no depender solo del color para transmitir estado.
- Navegación completa por teclado: orden de tabulación lógico, foco visible, skip-link al contenido.
- Semántica HTML real (`button` para acciones, `a` para navegación, `main/nav/header`, headings jerárquicos sin saltos).
- Formularios: `label` asociado a cada control, errores anunciados (`aria-describedby`), validación que no depende solo de placeholder.
- Imágenes con `alt` significativo (vacío si decorativas); iconos interactivos con nombre accesible (`aria-label`).
- Objetivos táctiles ≥24×24 px (ideal 44px); respetar `prefers-reduced-motion`.
- Auditoría automática: axe-core, Lighthouse, pa11y — **corregir errores**; las advertencias se anotan y solo se tocan si el arreglo es local y de bajo riesgo.

## Estados de interfaz

Todo componente con datos remotos o asíncronos debe cubrir los cinco estados, y todos deben verse bien:

1. **Loading**: skeleton/spinner con layout estable (sin saltos de contenido, CLS≈0).
2. **Empty**: mensaje útil con acción siguiente, no un hueco en blanco.
3. **Error**: mensaje comprensible, sin trazas técnicas, con opción de reintentar.
4. **Success/datos**: el caso feliz.
5. **Parcial/degradado**: qué pasa con datos incompletos o campos nulos.

## Consistencia visual

- Tokens de diseño centralizados (colores, espaciado, radios, tipografía) en variables CSS/Tailwind config; eliminar valores mágicos sueltos (`#3b82f6` repetido en 12 ficheros → token).
- Escala de espaciado coherente (múltiplos de 4/8); alineación a una retícula.
- Tipografía: escala modular limitada (≤6 tamaños), pesos consistentes, altura de línea legible (1.4–1.7 en cuerpo).
- Un solo sistema: no mezclar frameworks CSS o librerías de componentes duplicadas.
- Modo oscuro si el sistema de tokens lo soporta trivialmente; si no, no improvisarlo (puede ser propuesta disruptiva).

## Responsive y layout

- Mobile-first; probar 360px, 768px, 1280px y 1920px como mínimo.
- Sin scroll horizontal no intencionado; tablas con estrategia (scroll, columnas prioritarias, tarjetas).
- Touch: gestos con alternativa visible; hover nunca como única vía de información.

## Rendimiento percibido

- Core Web Vitals como objetivo: LCP <2.5s, INP <200ms, CLS <0.1.
- Imágenes: dimensiones explícitas, `loading="lazy"` bajo el fold, formatos modernos (webp/avif) con fallback.
- Fuentes: `font-display: swap`, subconjuntos, pocas variantes.
- JS: code-splitting por ruta, dependencias pesadas auditadas (¿moment? → date-fns/dayjs; ¿lodash entero? → imports por función).
- Evitar re-renderizados masivos: keys estables en listas, memoización donde se mida que importa.

## Interacción y feedback

- Toda acción con confirmación visual inmediata (optimista o spinner inline).
- Acciones destructivas: confirmación + deshacer cuando sea posible.
- Focus trap en modales; Escape cierra; devolver el foco al disparador.
- Transiciones cortas (150–300ms), con easing consistente; nada que bloquee la interacción.
- Debounce en búsquedas/inputs que disparan red.

## Contenido y microcopy

- Mensajes de error que dicen qué pasó y qué hacer; sin jerga técnica de cara al usuario.
- Consistencia de idioma y tono en toda la UI; fechas/números/moneda localizados (`Intl`).
- Textos reales en diseño (nada de "lorem ipsum" comprometido en el repo).

## Puente al informe

En la sección 9 de `plantilla-informe.md` reportar de forma concreta:

- Errores de axe/Lighthouse/pa11y corregidos vs. advertencias solo anotadas.
- Estados de interfaz que faltaban y cuáles se cubrieron.
- Anchos comprobados (360 / 768 / 1280 / 1920) y hallazgos por viewport.

Si el repo no tiene UI: en el informe escribir exactamente **"Sin interfaz de usuario"** (excepción a la regla "Sin hallazgos" de otras secciones).

## Nota sobre el alcance

El pulido se limita a mejoras compatibles con la estructura existente. Rediseños completos, cambio de framework, migración a un design system nuevo o rebranding son **propuestas disruptivas**: documentarlas en el informe, no implementarlas aquí.
