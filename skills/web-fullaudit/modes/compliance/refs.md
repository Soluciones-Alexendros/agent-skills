# Refs modo compliance

## WCAG 2.2 AA (protocolos manuales obligatorios)

- Teclado: todo accionable con Tab/Shift+Tab, foco visible, sin trampas; test con lector (NVDA/VoiceOver).
- Zoom 200% y 320px: sin scroll horizontal ni solapes; contraste con `core/reporting/contrast.py`
  (4.5:1 normal, 3:1 grande/componentes).
- Formularios: `<label>` asociado, errores con `role="alert"`, instrucciones persistentes.
- Daltonismo y `prefers-reduced-motion`: sin información solo por color; motion esencial desactivable.

## Legal web (RGPD / Consent Mode v2)

- Banner: consentimiento previo, granular y revocable; sin dark patterns; `ad_storage`/`analytics_storage`
  en `denied` por defecto hasta consentimiento (Consent Mode v2).
- Aviso legal + privacidad + cookies accesibles desde todas las páginas; registro del consentimiento.
- EN 301 549: declaración de accesibilidad publicada y mecanismo de reclamación.

## SEM y analítica

- Google Ads: estructura campaña→grupo→anuncio, QS/CTR por industria, landing con mensaje congruente
  y un solo CTA; sin campañas activas → SEM N/A justificado.
- GA4/GTM: eventos clave, Consent Mode efectivo, sin PII en hits.

## Umbrales

Dictamen POSITIVO: 0 FAIL Críticos, ACC ≥90%, TEC ≥85%, global ≥85%. Ver
`core/configs/thresholds.json` → `dictamen`.
