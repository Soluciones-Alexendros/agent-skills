#!/usr/bin/env python3
"""RICE unificado: score de priorización y asignación de sprint.

Fusión de verificar-compliance (deuda en horas por severidad) y web-playwright
(RICE reach×impact×confidence/effort + sprints). Stdlib puro.

Uso como librería:
    from rice import rice_score, sprint_for, deuda_horas
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))

RICE_DEFAULTS = {"Crítico": {"reach": 9, "impact": 9, "confidence": 8, "effort": 3},
                 "Crítica": {"reach": 9, "impact": 9, "confidence": 8, "effort": 3},
                 "Alto": {"reach": 7, "impact": 7, "confidence": 8, "effort": 4},
                 "Alta": {"reach": 7, "impact": 7, "confidence": 8, "effort": 4},
                 "Medio": {"reach": 5, "impact": 5, "confidence": 7, "effort": 5},
                 "Media": {"reach": 5, "impact": 5, "confidence": 7, "effort": 5},
                 "Bajo": {"reach": 3, "impact": 3, "confidence": 7, "effort": 3},
                 "Baja": {"reach": 3, "impact": 3, "confidence": 7, "effort": 3}}

SEV_NORM = {"Crítica": "Crítico", "Alta": "Alto", "Media": "Medio", "Baja": "Bajo",
            "Crítico": "Crítico", "Alto": "Alto", "Medio": "Medio", "Bajo": "Bajo"}


def load_thresholds():
    path = os.path.join(HERE, "..", "configs", "thresholds.json")
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def normalizar_severidad(sev):
    return SEV_NORM.get(sev, "Bajo")


def rice_score(severidad, rice=None):
    """Score RICE = reach × impact × confidence / effort (redondeado)."""
    sev = normalizar_severidad(severidad)
    r = dict(RICE_DEFAULTS.get(sev, RICE_DEFAULTS["Bajo"]))
    if rice:
        r.update({k: v for k, v in rice.items() if k in r and isinstance(v, (int, float))})
    return {**r, "score": round(r["reach"] * r["impact"] * r["confidence"] / max(r["effort"], 1))}


def sprint_for(severidad, thresholds=None):
    """Devuelve (nombre_sprint, plazo) para una severidad normalizada."""
    th = thresholds or load_thresholds()
    sev = normalizar_severidad(severidad)
    for sp in th["rice"]["sprints"]:
        if sev in sp["severidades"]:
            return sp["nombre"], sp["plazo"]
    return "Backlog", "—"


def deuda_horas(hallazgos, thresholds=None):
    """Deuda estimada en horas (tabla severidad_horas_defecto)."""
    th = thresholds or load_thresholds()
    tabla = th["severidad_horas_defecto"]
    return sum(h.get("esfuerzo_h") or tabla.get(normalizar_severidad(h.get("severidad")), 4)
               for h in hallazgos)
