# Troubleshooting — problemas conocidos y resolución

Registro de incidencias detectadas durante el desarrollo y testeo de la skill, y guía para fallos en ejecución. Ejecutar `python3 scripts/selftest.py` para diagnosticar (exit 0 = todo OK).

## Incidencias resueltas en desarrollo (v2.0.0)

1. **Dato de referencia erróneo heredado del material fuente.** El pack original afirmaba que el contraste `#767676` sobre `#FFFF00` era 2.59:1; la fórmula oficial WCAG (luminancia relativa sRGB) da **4.23:1**. Corregido en los tests de `contrast.py`. Lección: validar cualquier "ratio conocido" con el cálculo, no con la memoria del material.
2. **Registry desalineado con la implementación.** El check ONP-05 declaraba `script_key: og_tags` sin check implementado en `audit_page.py`. Detectado por el test "script_key sin implementación" y resuelto implementando `check_og_tags`. Regla: todo `script_key` del registry debe tener un check que lo emita.
3. **WARN vs. FAIL en dictamen.** WARN se contabiliza como incumplimiento parcial (afecta a % y dictamen) pero no bloquea como FAIL crítico. Documentado en `score.py` para evitar interpretaciones divergentes.

## Fallos de ejecución habituales

| Síntoma | Causa probable | Resolución |
|---|---|---|
| `audit_page.py` exit 2, `error: URLError/timeout` | Red caída, DNS, WAF bloqueando bots | Reintentar; si hay WAF, usar `--file` con HTML descargado manualmente o crawl con navegador real |
| Checks `robots_txt`/`sitemap` en WARN en staging | Entorno con bloqueo intencionado | Marcar N/A justificado o auditar en producción |
| `img_alt_coverage` PASS pero hay imágenes sin texto | El check exige atributo `alt` presente; `alt=""` decorativo cuenta como conforme | Revisión manual del significado del alt (WCAG 1.1.1 no es automatizable al 100%) |
| `jsonld` FAIL con JSON válido visualmente | Comas finales o comillas simples en el bloque | Validar el bloque con `json.loads` aislado; el error indica el bloque concreto |
| `score.py` dice "SIN DATOS" | Todos los checks llegaron como PENDING/NA | Alimentar resultados desde `audit_page.py` o evaluar manualmente con `id` + `resultado` |
| El dictamen sale NEGATIVO con pocos fallos | Un FAIL de severidad Crítico fuerza NEGATIVO por diseño | Ver `motivo_dictamen` en el JSON de scoring para identificar el check bloqueante |
| `selftest.py` ERROR (no FAIL) en un test | Excepción no controlada en el código probado | El detalle indica el tipo de excepción; corregir el script afectado antes de usarlo |
| HTML con `charset` distinto de UTF-8 | El parser decodifica como UTF-8 con `replace` | Los checks de texto pueden degradarse; se emite WARN en `charset` |

## Convenciones de los scripts

- Stdlib puro: sin `pip install` necesario; funcionan en cualquier Python ≥3.9.
- Nunca interrumpen por errores de red/parseo: devuelven JSON con `status`/`error` y código de salida controlado (0 OK, 1 tests fallidos, 2 error de obtención/entrada).
- Un FAIL registrado nunca es sobrescrito por un PASS posterior del mismo check (ver `score.normalizar`).
