#!/usr/bin/env python3
"""Scoring de compliance E2E: % por categoría, semáforo, RICE y sprints.

Entrada: compliance.json (validado por validate_compliance.py).
Salida: score.json con % global y por categoría, veredicto APTO /
APTO CON OBSERVACIONES / NO APTO, hallazgos con score RICE y sprint.

Uso: python3 score.py compliance.json [--json score.json]
"""
import argparse
import json
import logging
import os
import sys

logger = logging.getLogger("e2e.score")

HERE = os.path.dirname(os.path.abspath(__file__))

RICE_DEFAULTS = {"Crítica": {"reach": 9, "impact": 9, "confidence": 8, "effort": 3},
                 "Alta": {"reach": 7, "impact": 7, "confidence": 8, "effort": 4},
                 "Media": {"reach": 5, "impact": 5, "confidence": 7, "effort": 5},
                 "Baja": {"reach": 3, "impact": 3, "confidence": 7, "effort": 3}}


def load_configs():
    base = os.path.join(HERE, "..", "configs")
    try:
        with open(os.path.join(base, "checks.json"), encoding="utf-8") as fh:
            checks = json.load(fh)
        with open(os.path.join(base, "thresholds.json"), encoding="utf-8") as fh:
            thresholds = json.load(fh)
    except OSError as e:
        raise RuntimeError(f"no se pudieron leer configs en {base}: {type(e).__name__}: {e}") from e
    except json.JSONDecodeError as e:
        raise RuntimeError(f"JSON inválido en configs de {base}: {e}") from e
    return checks, thresholds


def rice_score(severidad, rice=None):
    r = dict(RICE_DEFAULTS.get(severidad, RICE_DEFAULTS["Baja"]))
    if rice:
        r.update({k: v for k, v in rice.items() if k in r and isinstance(v, (int, float))})
    score = round(r["reach"] * r["impact"] * r["confidence"] / max(r["effort"], 1))
    return {**r, "score": score}


def sprint_for(severidad, thresholds):
    for nombre, meta in thresholds["rice_sprints"].items():
        if severidad in meta["severidades"]:
            return nombre, meta["plazo"]
    return "Sprint 3", "Semana 3"


def score(compliance):
    checks_cfg, thresholds = load_configs()
    vrules = thresholds["veredicto"]

    por_cat = {}
    hallazgos = []
    fails_criticas = 0
    for item in compliance:
        cat = item.get("category")
        st = item.get("status")
        c = por_cat.setdefault(cat, {"pass": 0, "fail": 0, "warn": 0, "na": 0})
        if st == "PASS":
            c["pass"] += 1
        elif st == "N/A":
            c["na"] += 1
        elif st in ("FAIL", "WARN"):
            c["fail" if st == "FAIL" else "warn"] += 1
            if st == "FAIL" and item.get("severity") == "Crítica":
                fails_criticas += 1
            rice = rice_score(item.get("severity", "Baja"), item.get("rice"))
            sprint, plazo = sprint_for(item.get("severity", "Baja"), thresholds)
            hallazgos.append({
                "id": item.get("id"), "url": item.get("url"), "category": cat,
                "check": item.get("check"), "status": st,
                "severity": item.get("severity"), "evidence": item.get("evidence", {}),
                "recommendation": item.get("recommendation", ""),
                "wcag_ref": item.get("wcag_ref"), "rice": rice,
                "sprint": sprint, "plazo": plazo,
            })

    resumen_cat = {}
    g_pass = g_eval = 0
    for cat, c in por_cat.items():
        evaluables = c["pass"] + c["fail"] + c["warn"]
        pct = round(100 * c["pass"] / evaluables) if evaluables else None
        resumen_cat[cat] = {**c, "pct": pct,
                            "semaforo": ("SIN DATOS" if pct is None else
                                         "VERDE" if pct >= thresholds["semaforo"]["verde"] else
                                         "AMBAR" if pct >= thresholds["semaforo"]["ambar"] else "ROJO")}
        g_pass += c["pass"]
        g_eval += evaluables
    pct_global = round(100 * g_pass / g_eval) if g_eval else None

    if fails_criticas:
        veredicto = "NO APTO"
        motivo = f"{fails_criticas} FAIL de severidad Crítica"
    elif pct_global is None:
        veredicto = "SIN DATOS"
        motivo = "Sin checks evaluables"
    elif pct_global >= vrules["apto"]["min_pct_global"]:
        veredicto = "APTO"
        motivo = "0 FAIL críticas y cumplimiento >=90%"
    elif pct_global >= vrules["apto_con_observaciones"]["min_pct_global"]:
        veredicto = "APTO CON OBSERVACIONES"
        motivo = f"Cumplimiento {pct_global}% (70-89%): requiere plan de remediación"
    else:
        veredicto = "NO APTO"
        motivo = f"Cumplimiento global {pct_global}% bajo mínimo 70%"

    hallazgos.sort(key=lambda h: -h["rice"]["score"])
    return {
        "veredicto": veredicto, "motivo": motivo,
        "pct_global": pct_global, "fails_criticas": fails_criticas,
        "total_checks": len(compliance), "total_hallazgos": len(hallazgos),
        "categorias": resumen_cat, "hallazgos": hallazgos,
    }


def main(argv=None) -> int:
    logging.basicConfig(stream=sys.stderr, level=logging.WARNING,
                        format="%(levelname)s %(name)s: %(message)s")
    ap = argparse.ArgumentParser(description="Scoring E2E + RICE")
    ap.add_argument("compliance", help="compliance.json")
    ap.add_argument("--json", help="Guardar score.json")
    args = ap.parse_args(argv)
    try:
        with open(args.compliance, encoding="utf-8") as fh:
            data = json.load(fh)
    except OSError as e:
        logger.error("no se pudo leer %s: %s: %s", args.compliance, type(e).__name__, e)
        return 2
    except json.JSONDecodeError as e:
        logger.error("JSON inválido en %s: %s", args.compliance, e)
        return 2
    if not isinstance(data, list):
        logger.error("formato inválido en %s: se esperaba array de checks", args.compliance)
        return 2
    try:
        out = score(data)
    except RuntimeError as e:
        logger.error("%s", e)
        return 2
    except (KeyError, TypeError, AttributeError) as e:
        logger.error("configs o compliance inválidos: %s: %s", type(e).__name__, e)
        return 2
    txt = json.dumps(out, ensure_ascii=False, indent=2)
    if args.json:
        try:
            with open(args.json, "w", encoding="utf-8") as fh:
                fh.write(txt)
        except OSError as e:
            logger.error("no se pudo escribir %s: %s: %s", args.json, type(e).__name__, e)
            print(txt)
            return 2
    print(txt)
    return 0


if __name__ == "__main__":
    sys.exit(main())
