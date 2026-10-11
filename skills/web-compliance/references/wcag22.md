# Accesibilidad WCAG 2.2 AA — criterios y protocolos manuales

Leer al ejecutar el pilar ACC. Método: ~50% automatizado (`scripts/audit_page.py`, Axe, WAVE, Lighthouse) + **50% manual obligatorio**: las herramientas automáticas solo cubren ~30–40% de los criterios.

## Criterios por principio POUR (checks ACC-01 a ACC-16)

### Perceptible
- **1.1.1 No textual (A)** — alt significativo; decorativas con `alt=""`; iconos funcionales con nombre accesible; gráficos complejos con descripción extendida. *(script: cobertura de alt)*
- **1.2.2 Subtítulos (A) / 1.2.5 Audiodescripción (AA)** — subtítulos sincronizados y revisados (no auto-generados sin revisión); audiodescripción o alternativa textual.
- **1.3.1 Info y relaciones (A)** — landmarks (`header/nav/main/footer`), jerarquía de encabezados sin saltos, listas y tablas semánticas (`<th>`), `<label>` asociados.
- **1.3.2 Secuencia significativa (A)** — orden DOM = orden visual; cuidado con `order` en flex/grid.
- **1.3.3 Características sensoriales (A)** — instrucciones no dependen solo de color/forma/sonido.
- **1.4.1 Uso del color (A)** — enlaces en párrafo subrayados o con otro indicador; errores con icono/texto además del color.
- **1.4.3 Contraste mínimo (AA)** — texto normal ≥4.5:1; grande ≥3:1. Verificar con `scripts/contrast.py` o CCA.
- **1.4.4 Redimensionar (AA) / 1.4.10 Reflow (AA)** — zoom 200% sin pérdida; 320px/400% sin scroll bidireccional.
- **1.4.11 Contraste no textual (AA)** — bordes de controles, indicador de foco, iconos ≥3:1.
- **1.4.13 Contenido en hover/focus (AA)** — tooltips/menús descartables, persistentes y hoverables.

### Operable
- **2.1.1 Teclado (A) / 2.1.2 Sin trampas (A)** — toda función operable sin ratón; modales cerrables con ESC; sin trampas en carruseles/iframes.
- **2.1.4 Atajos de tecla (A)** — atajos de carácter único desactivables/remapeables.
- **2.2.1 Tiempo ajustable (A) / 2.2.2 Pausar/detener/ocultar (A)** — timeouts con aviso y extensión; carruseles automáticos pausables.
- **2.3.1 Destellos (A)** — nada parpadea >3 veces/segundo.
- **2.4.1 Saltar bloques (A)** — skip link visible al foco + landmarks. *(script)*
- **2.4.2 Título de página (A)** — único y descriptivo (cruce con ONP-02).
- **2.4.3 Orden de foco (A)** — secuencia lógica.
- **2.4.4 Propósito de enlaces (A)** — texto descriptivo, no "clic aquí".
- **2.4.7 Foco visible (AA) / 2.4.11 Foco no oculto (AA, 2.2)** — indicador ≥3:1; nunca cubierto por sticky headers, banners de cookies o modales; jamás `outline:none` sin sustituto.
- **2.5.3 Etiqueta en el nombre (A)** — accessible name contiene la etiqueta visible.
- **2.5.8 Tamaño del objetivo (AA, 2.2)** — ≥24×24 px CSS (objetivo recomendado: 44–48px).

### Comprensible
- **3.1.1 Idioma de la página (A) / 3.1.2 Idioma de partes (AA)** — `<html lang>` válido. *(script)*
- **3.2.1 Al recibir foco / 3.2.2 Al introducir datos (A)** — sin cambios de contexto inesperados.
- **3.2.3 Navegación consistente (AA)** — menús repetidos en orden consistente.
- **3.2.6 Ayuda consistente (A, 2.2)** — mecanismos de ayuda en la misma posición relativa.
- **3.3.1 Identificación de errores (A) / 3.3.3 Sugerencias (AA)** — errores en texto (no solo color), con cómo corregir; `aria-invalid` + `aria-describedby` + `role="alert"`.
- **3.3.8 Autenticación accesible (AA, 2.2)** — sin tests cognitivos/transcripción obligatorios salvo excepción (passkeys, pegado en campos de contraseña permitido).

### Robusto
- **4.1.2 Nombre, rol, valor (A)** — componentes custom con ARIA correcto y estados comunicados; primera regla de ARIA: preferir HTML nativo.
- **4.1.3 Mensajes de estado (AA)** — `aria-live`/`role="status|alert"` en notificaciones dinámicas.

## Protocolos de testing manual

### Teclado (10 min por plantilla)
Tab desde el inicio registrando cada elemento enfocado; Shift+Tab inverso; ESC cierra modales; flechas en menús. FAIL si algo requiere ratón/hover o hay trampa.

### Lector de pantalla (NVDA+Chrome / VoiceOver+Safari)
Recorrer flujos críticos (home, navegación, formulario, checkout/registro): título anunciado, enlaces legibles (Insert+F7), encabezados (tecla H), labels de formulario, errores anunciados, landmarks. Grabar ~30 s por plantilla crítica como evidencia.

### Zoom y reflow
Zoom 200%: sin solapes, botones operables, formularios completos. Viewport 320px: sin scroll horizontal.

### Daltonismo
DevTools → Rendering → Emulate vision deficiencies (protanopia, deuteranopia, tritanopia): enlaces, estados de error/éxito y gráficos comprensibles sin color.

### Formularios
Enviar vacío: errores anunciados por lector, foco al primer campo con error, descripción de cómo corregir, `aria-invalid="true"`, `aria-describedby` enlazando el mensaje.

## Declaración de accesibilidad (EN 301 549 / RD 1112/2018)
Página `/accesibilidad` con: estado de conformidad, excepciones, fecha de revisión, canal de feedback, compatibilidad con AT. Obligatoria en sector público ES y recomendada en general (ACC-16).
