#!/usr/bin/env python3
"""Analiza mediciones del navegador (assets/measure.js) y emite checks UI-01..UI-07.

Entrada: JSON con {"url", "viewport": {"w","h"}, "elements": [...]} o lista de
páginas. Cada element: {selector, tag, w, h, x, y, fontSize?, lineHeight?,
naturalW?, naturalH?, clickable?, text?}

Uso:
    python3 measure_analyze.py measurements.json [--json checks.json]
"""
import argparse
import json
import logging
import os
import sys

logger = logging.getLogger("e2e.measure_analyze")

HERE = os.path.dirname(os.path.abspath(__file__))


def load_ui():
    path = os.path.join(HERE, "..", "configs", "thresholds.json")
    try:
        with open(path, encoding="utf-8") as fh:
            data = json.load(fh)
        return data["ui"]
    except OSError as e:
        raise RuntimeError(f"no se pudo leer {path}: {type(e).__name__}: {e}") from e
    except (json.JSONDecodeError, KeyError, TypeError) as e:
        raise RuntimeError(f"thresholds inválidos en {path}: {type(e).__name__}: {e}") from e


def _entry(check_id, url, check, status, severity, evidence, recommendation, wcag=None):
    return {"id": check_id, "url": url, "category": "UI/UX", "check": check,
            "method": "measure_analyze", "status": status, "severity": severity,
            "evidence": evidence, "recommendation": recommendation, "wcag_ref": wcag}


def analyze_page(page, ui):
    url = page.get("url", "unknown")
    vw = page.get("viewport", {}).get("w", 1440)
    checks = []
    els = [e for e in page.get("elements", []) if e.get("w", 0) > 0 and e.get("h", 0) > 0]

    # UI-01 touch targets (elementos clickables)
    clickables = [e for e in els if e.get("clickable")]
    small = [e for e in clickables
             if e["w"] < ui["touch_target_min_px"] or e["h"] < ui["touch_target_min_px"]]
    hard = [e for e in small
            if e["w"] < ui["touch_target_hard_min_px"] or e["h"] < ui["touch_target_hard_min_px"]]
    if clickables:
        if hard:
            checks.append(_entry("UI-01", url, "Touch targets >=44px (mín. 24px WCAG 2.5.8)",
                                 "FAIL", "Crítica",
                                 {"count": len(hard),
                                  "ejemplos": [{"locator": e["selector"], "box": {"w": e["w"], "h": e["h"]}}
                                               for e in hard[:5]]},
                                 "Aumentar a >=44x44px (mínimo absoluto 24x24px)", "2.5.5/2.5.8"))
        elif small:
            checks.append(_entry("UI-01", url, "Touch targets >=44px (mín. 24px WCAG 2.5.8)",
                                 "WARN", "Alta",
                                 {"count": len(small),
                                  "ejemplos": [{"locator": e["selector"], "box": {"w": e["w"], "h": e["h"]}}
                                               for e in small[:5]]},
                                 "Elevar targets de 24-44px al objetivo 44px", "2.5.5"))
        else:
            checks.append(_entry("UI-01", url, "Touch targets >=44px", "PASS", "Alta",
                                 {"count": len(clickables)}, ""))
    else:
        checks.append(_entry("UI-01", url, "Touch targets", "N/A", "Alta",
                             {"nota": "sin elementos clickables medidos"}, ""))

    # UI-02 tipografía
    def _px(v):
        try:
            return float(str(v).replace("px", ""))
        except (TypeError, ValueError):
            return None

    texts = [e for e in els if e.get("fontSize")]
    bad_font = [e for e in texts if (_px(e["fontSize"]) or 99) < ui["font_size_min_px"]]
    bad_lh = []
    for e in texts:
        fs, lh = _px(e["fontSize"]), _px(e.get("lineHeight"))
        if fs and lh and lh / fs < ui["line_height_min"]:
            bad_lh.append(e)
    if texts:
        if bad_font or bad_lh:
            checks.append(_entry("UI-02", url, "font-size >=12px y line-height >=1.4",
                                 "FAIL" if bad_font else "WARN", "Media",
                                 {"font_pequena": [{"locator": e["selector"], "fontSize": e["fontSize"]}
                                                   for e in bad_font[:5]],
                                  "line_height_bajo": [{"locator": e["selector"], "lineHeight": e["lineHeight"]}
                                                       for e in bad_lh[:5]]},
                                 "Subir cuerpo a >=12px y line-height >=1.4"))
        else:
            checks.append(_entry("UI-02", url, "Tipografía legible", "PASS", "Media",
                                 {"count": len(texts)}, ""))

    # UI-03 grid 8pt
    meas = [e for e in els if e.get("w") and e.get("h")]
    off_grid = [e for e in meas if (round(e["w"]) % ui["grid_pt"] != 0 or round(e["h"]) % ui["grid_pt"] != 0)]
    if meas:
        ratio = len(off_grid) / len(meas)
        st = "PASS" if ratio <= 0.2 else "WARN"
        checks.append(_entry("UI-03", url, "Componentes alineados a grid 8pt", st, "Baja",
                             {"off_grid_pct": round(ratio * 100),
                              "ejemplos": [e["selector"] for e in off_grid[:5]]},
                             "" if st == "PASS" else "Revisar tokens de espaciado (múltiplos de 8)"))

    # UI-04 distorsión de imágenes (robusto a naturalW/H ausentes o cero)
    imgs = [e for e in els if e.get("naturalW") and e.get("naturalH") and e.get("w") and e.get("h")]
    distorted = []
    for e in imgs:
        try:
            natural = float(e["naturalW"]) / float(e["naturalH"])
            rendered = float(e["w"]) / float(e["h"])
        except (TypeError, ValueError, ZeroDivisionError) as exc:
            logger.debug("UI-04 %s: dimensiones no numéricas (%s)", e.get("selector"), exc)
            continue
        if abs(natural - rendered) / natural > 0.05:
            distorted.append(e)
    if imgs:
        st = "FAIL" if distorted else "PASS"
        checks.append(_entry("UI-04", url, "Imágenes sin distorsión de proporción", st, "Media",
                             {"count": len(distorted),
                              "ejemplos": [{"locator": e["selector"],
                                            "natural": f"{e['naturalW']}x{e['naturalH']}",
                                            "rendered": f"{round(e['w'])}x{round(e['h'])}"}
                                           for e in distorted[:5]]},
                             "Usar object-fit: cover/contain o reservar aspect-ratio"))

    # UI-05 overflow horizontal
    doc_w = page.get("documentWidth")
    if doc_w is not None:
        overflow = doc_w > vw + 1
        checks.append(_entry("UI-05", url, "Sin overflow horizontal", "FAIL" if overflow else "PASS",
                             "Crítica",
                             {"scrollWidth": doc_w, "innerWidth": vw},
                             "Localizar elemento desbordado (outline en DevTools) y corregir layout",
                             "1.4.10"))

    # UI-06 proporción header
    header = next((e for e in els if e.get("tag") == "HEADER"), None)
    vh = page.get("viewport", {}).get("h")
    if header and vh:
        pct = 100 * header["h"] / vh
        st = "PASS" if pct <= ui["header_max_viewport_pct"] else "WARN"
        checks.append(_entry("UI-06", url, "Header <=25% del viewport", st, "Media",
                             {"header_pct": round(pct, 1)},
                             "" if st == "PASS" else "Reducir altura del header o hacerlo no-sticky"))

    return checks


def analyze(data):
    if not isinstance(data, (dict, list)):
        raise TypeError(f"mediciones inválidas: se esperaba objeto o lista, llegó {type(data).__name__}")
    ui = load_ui()
    pages = data if isinstance(data, list) else [data]
    checks = []
    for p in pages:
        if not isinstance(p, dict):
            logger.warning("página ignorada: no es objeto (%r)", type(p).__name__)
            continue
        try:
            checks.extend(analyze_page(p, ui))
        except (KeyError, TypeError, AttributeError) as e:
            logger.warning("página %r degradada: %s: %s", p.get("url"), type(e).__name__, e)
    return checks


def main(argv=None) -> int:
    logging.basicConfig(stream=sys.stderr, level=logging.WARNING,
                        format="%(levelname)s %(name)s: %(message)s")
    ap = argparse.ArgumentParser(description="Análisis de mediciones UI")
    ap.add_argument("measurements", help="JSON generado con assets/measure.js")
    ap.add_argument("--json", help="Guardar checks en JSON")
    args = ap.parse_args(argv)
    try:
        with open(args.measurements, encoding="utf-8") as fh:
            data = json.load(fh)
    except OSError as e:
        logger.error("no se pudo leer %s: %s: %s", args.measurements, type(e).__name__, e)
        return 2
    except json.JSONDecodeError as e:
        logger.error("JSON inválido en %s: %s", args.measurements, e)
        return 2
    try:
        checks = analyze(data)
    except (TypeError, RuntimeError) as e:
        logger.error("no se pudo analizar %s: %s", args.measurements, e)
        return 2
    out = json.dumps(checks, ensure_ascii=False, indent=2)
    if args.json:
        try:
            with open(args.json, "w", encoding="utf-8") as fh:
                fh.write(out)
        except OSError as e:
            logger.error("no se pudo escribir %s: %s: %s", args.json, type(e).__name__, e)
            print(out)
            return 2
    print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
