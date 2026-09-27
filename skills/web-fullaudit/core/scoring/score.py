#!/usr/bin/env python3
"""Scoring unificado web-fullaudit: % por dominio, semáforo y dictamen dual.

Acepta ambas formas de entrada (se pueden mezclar en una lista):
- Formato compliance (web-compliance): {"id": "ACC-01", "resultado": "PASS|FAIL|WARN|NA|PENDING", ...}
  o salidas de audit_page.py (por script_key).
- Formato e2e (web-playwright): {"id": "RT-01", "status": "PASS|FAIL|WARN|N/A", ...}

Salida: pct_global, semáforo por dominio, dictamen compliance
(POSITIVO/PARCIAL/NEGATIVO), veredicto e2e (APTO/APTO CON OBSERVACIONES/NO APTO),
hallazgos con RICE + sprint y deuda en horas.

Uso:
    python3 score.py resultados.json [--config DIR] [--json salida.json]
    # resultados.json: {"target": ..., "checks": [...]} o [...] directo
"""
import argparse
import json
import logging
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rice import deuda_horas, normalizar_severidad, rice_score, sprint_for  # noqa: E402

logger = logging.getLogger("fullaudit.score")

RESULTADOS_VALIDOS = {"PASS", "FAIL", "WARN", "NA", "N/A", "PENDING"}


def _load_json(path):
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except OSError as e:
        raise RuntimeError(f"no se pudo leer {path}: {type(e).__name__}: {e}") from e
    except json.JSONDecodeError as e:
        raise RuntimeError(f"JSON inválido en {path}: {e}") from e


def load_configs(config_dir=None):
    base = config_dir or os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "configs")
    checks = _load_json(os.path.join(base, "checks.json"))
    thresholds = _load_json(os.path.join(base, "thresholds.json"))
    return checks, thresholds


def normalizar(resultados, registry):
    """Devuelve {check_id: item} fusionando por id o script_key (formato compliance)."""
    by_key = {c["script_key"]: c["id"] for c in registry["checks"] if c.get("script_key")}
    mapa = {}
    for item in resultados:
        if not isinstance(item, dict):
            continue
        cid = item.get("id") or by_key.get(item.get("script_key"))
        if not cid:
            continue
        estado = (item.get("resultado") or item.get("status") or "PENDING").upper()
        if estado == "N/A":
            estado = "NA"
        if estado not in RESULTADOS_VALIDOS:
            estado = "PENDING"
        prev = mapa.get(cid)
        if prev and prev["resultado"] in ("FAIL", "WARN") and estado == "PASS":
            continue
        mapa[cid] = {
            "id": cid,
            "resultado": estado,
            "evidencia": item.get("evidencia") or item.get("evidence") or "",
            "accion": item.get("accion") or item.get("recommendation") or item.get("detalle", ""),
            "url": item.get("url", ""),
            "rice_in": item.get("rice"),
        }
    return mapa


def _es_e2e(cid):
    return cid.split("-")[0] in ("RT", "FN", "FM", "UI", "AC", "PF", "SE", "SG", "MO")


def score(resultados, config_dir=None):
    registry, thresholds = load_configs(config_dir)
    mapa = normalizar(resultados, registry)
    reg_by_id = {c["id"]: c for c in registry["checks"]}
    sev_orden = {"Crítico": 0, "Alto": 1, "Medio": 2, "Bajo": 3}

    dominios = {}
    hallazgos = []
    fails_criticos = 0
    for cid, c in reg_by_id.items():
        r = mapa.get(cid, {"resultado": "PENDING", "evidencia": "", "accion": "", "url": ""})
        sev = normalizar_severidad(c["severidad"])
        dom = c.get("dominio", "?")
        d = dominios.setdefault(dom, {"pass": 0, "fail": 0, "pending": 0, "na": 0})
        estado = r["resultado"]
        if estado == "PASS":
            d["pass"] += 1
        elif estado == "NA":
            d["na"] += 1
        elif estado == "PENDING":
            d["pending"] += 1
        else:  # FAIL o WARN
            d["fail"] += 1
            if estado == "FAIL" and sev == "Crítico":
                fails_criticos += 1
            rice = rice_score(sev, r.get("rice_in"))
            sprint, plazo = sprint_for(sev, thresholds)
            hallazgos.append({
                "id": cid, "dominio": dom,
                "criterio": c.get("criterio", ""),
                "estandar": c.get("estandar"), "origen": c.get("origen"),
                "severidad": sev, "resultado": estado,
                "url": r.get("url", ""), "evidencia": r.get("evidencia", ""),
                "accion": r.get("accion", ""),
                "esfuerzo_h": c.get("esfuerzo_h"),
                "rice": rice, "sprint": sprint, "plazo": plazo,
            })

    por_dominio = {}
    g_pass = g_eval = 0
    for dom, d in dominios.items():
        evaluables = d["pass"] + d["fail"]
        pct = round(100 * d["pass"] / evaluables) if evaluables else None
        por_dominio[dom] = {
            **d, "pct": pct,
            "semaforo": ("SIN DATOS" if pct is None else
                         "VERDE" if pct >= thresholds["semaforo"]["verde"] else
                         "AMBAR" if pct >= thresholds["semaforo"]["ambar"] else "ROJO"),
        }
        g_pass += d["pass"]
        g_eval += evaluables
    pct_global = round(100 * g_pass / g_eval) if g_eval else None

    # Dictamen compliance (origen web-compliance)
    reglas = thresholds["dictamen"]["positivo"]
    crit_comp = [h for h in hallazgos
                 if h["origen"] == "web-compliance" and h["severidad"] == "Crítico"
                 and h["resultado"] == "FAIL"]
    acc = por_dominio.get("ACC", {}).get("pct")
    tec = por_dominio.get("TEC", {}).get("pct")
    if crit_comp:
        dictamen = "NEGATIVO"
        motivo = f"{len(crit_comp)} FAIL crítico(s) compliance: " + ", ".join(h["id"] for h in crit_comp)
    elif pct_global is None:
        dictamen = "SIN DATOS"
        motivo = "No hay checks evaluables"
    elif pct_global >= reglas["min_pct_global"] and (acc is None or acc >= 90) \
            and (tec is None or tec >= 85):
        dictamen = "POSITIVO"
        motivo = "0 FAIL críticos compliance y umbrales ACC/TEC superados"
    elif pct_global >= thresholds["dictamen"]["parcial"]["min_pct_global"]:
        dictamen = "PARCIAL"
        motivo = f"Global {pct_global}% bajo umbral {reglas['min_pct_global']}%"
    else:
        dictamen = "NEGATIVO"
        motivo = f"Cumplimiento global {pct_global}% bajo mínimo"

    # Veredicto e2e (origen web-playwright)
    vrules = thresholds["veredicto_e2e"]
    e2e_items = [h for h in hallazgos if h["origen"] == "web-playwright"]
    e2e_eval = sum(1 for cid, c in reg_by_id.items()
                   if c.get("origen") == "web-playwright"
                   and mapa.get(cid, {}).get("resultado") not in ("NA", "PENDING", None)
                   and mapa.get(cid, {}).get("resultado") is not None
                   and mapa.get(cid, {"resultado": "PENDING"})["resultado"] != "PENDING")
    e2e_pass = sum(1 for cid, c in reg_by_id.items()
                   if c.get("origen") == "web-playwright"
                   and mapa.get(cid, {"resultado": "PENDING"})["resultado"] == "PASS")
    pct_e2e = round(100 * e2e_pass / e2e_eval) if e2e_eval else None
    crit_e2e = [h for h in e2e_items if h["severidad"] == "Crítico" and h["resultado"] == "FAIL"]
    if crit_e2e:
        veredicto = "NO APTO"
        motivo_e2e = f"{len(crit_e2e)} FAIL de severidad Crítica e2e"
    elif pct_e2e is None:
        veredicto = "SIN DATOS"
        motivo_e2e = "Sin checks e2e evaluables"
    elif pct_e2e >= vrules["apto"]["min_pct_global"]:
        veredicto = "APTO"
        motivo_e2e = "0 FAIL críticas e2e y cumplimiento >=90%"
    elif pct_e2e >= vrules["apto_con_observaciones"]["min_pct_global"]:
        veredicto = "APTO CON OBSERVACIONES"
        motivo_e2e = f"Cumplimiento e2e {pct_e2e}% (70-89%): requiere plan de remediación"
    else:
        veredicto = "NO APTO"
        motivo_e2e = f"Cumplimiento e2e {pct_e2e}% bajo mínimo 70%"

    hallazgos.sort(key=lambda h: (-h["rice"]["score"], sev_orden.get(h["severidad"], 9), h["id"]))

    return {
        "target": None,
        "dictamen": dictamen, "motivo_dictamen": motivo,
        "veredicto_e2e": veredicto, "motivo_e2e": motivo_e2e,
        "pct_global": pct_global, "pct_e2e": pct_e2e,
        "dominios": por_dominio,
        "fails_criticos": fails_criticos,
        "total_hallazgos": len(hallazgos),
        "deuda_horas_estimada": deuda_horas(hallazgos, thresholds),
        "pendientes": sum(d["pending"] for d in dominios.values()),
        "hallazgos": hallazgos,
    }


def main(argv=None) -> int:
    logging.basicConfig(stream=sys.stderr, level=logging.WARNING,
                        format="%(levelname)s %(name)s: %(message)s")
    ap = argparse.ArgumentParser(description="Scoring unificado web-fullaudit + RICE")
    ap.add_argument("resultados", help="JSON con checks evaluados (objeto con 'checks' o array)")
    ap.add_argument("--config", help="Directorio de configs (por defecto ../configs)")
    ap.add_argument("--json", help="Guardar scoring en JSON")
    args = ap.parse_args(argv)

    try:
        data = _load_json(args.resultados)
    except RuntimeError as e:
        logger.error("%s", e)
        print(json.dumps({"error": str(e)}, ensure_ascii=False))
        return 2
    checks = data.get("checks", []) if isinstance(data, dict) else data
    if not isinstance(checks, list):
        logger.error("formato inválido en %s: se esperaba objeto con 'checks' o array", args.resultados)
        print(json.dumps({"error": "Formato inválido: se esperaba objeto con 'checks' o array"},
                         ensure_ascii=False))
        return 2
    try:
        out = score(checks, config_dir=args.config)
    except RuntimeError as e:
        logger.error("%s", e)
        print(json.dumps({"error": str(e)}, ensure_ascii=False))
        return 2
    except (KeyError, TypeError, AttributeError) as e:
        logger.error("configs o resultados inválidos: %s: %s", type(e).__name__, e)
        print(json.dumps({"error": f"Datos inválidos: {type(e).__name__}: {e}"}, ensure_ascii=False))
        return 2
    out["target"] = data.get("target") if isinstance(data, dict) else None
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
