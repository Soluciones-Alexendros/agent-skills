#!/usr/bin/env python3
"""Informe de cierre dual web-fullaudit: dictamen compliance + veredicto e2e.

Entrada: JSON de scoring (core/scoring/score.py).
Salida: Markdown (+ HTML y CSV opcionales vía --outdir).

Uso:
    python3 report.py scoring.json [--md informe.md]
    python3 report.py scoring.json --outdir output/  # REPORT.md + REPORT.html + issues.csv
    python3 report.py resultados.json --from-checks [--md informe.md]
"""
import argparse
import csv
import datetime
import html
import importlib.util
import json
import logging
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SCORING_PATH = os.path.join(HERE, "..", "scoring", "score.py")
_score_spec = importlib.util.spec_from_file_location("fullaudit_scoring_score", SCORING_PATH)
if _score_spec is None or _score_spec.loader is None:
    raise ImportError(f"Could not load score from {SCORING_PATH}")
_score_module = importlib.util.module_from_spec(_score_spec)
_score_spec.loader.exec_module(_score_module)
score = _score_module.score

logger = logging.getLogger("fullaudit.report")

ICONO = {"PASS": "✅", "FAIL": "❌", "WARN": "⚠️", "NA": "➖", "N/A": "➖", "PENDING": "🔎"}
SEMAFORO = {"VERDE": "🟢", "AMBAR": "🟠", "ROJO": "🔴", "SIN DATOS": "⚪"}


def render_md(sc):
    fecha = datetime.date.today().isoformat()
    L = ["# INFORME DE CIERRE — FULLAUDIT", "",
         f"**Objetivo:** {sc.get('target') or '(sin especificar)'}  ",
         f"**Fecha:** {fecha}  ",
         "**Estándares:** WCAG 2.2 AA · EN 301 549 · CWV (LCP/INP/CLS) · Consent Mode v2 · RGPD", "",
         "## 1. Resumen ejecutivo", "",
         f"- **Dictamen compliance: {sc['dictamen']}** — {sc['motivo_dictamen']}",
         f"- **Veredicto e2e: {sc['veredicto_e2e']}** — {sc['motivo_e2e']}"]
    pct = sc["pct_global"]
    L.append(f"- Cumplimiento global: **{pct}%**" if pct is not None else "- Cumplimiento global: SIN DATOS")
    if sc.get("pct_e2e") is not None:
        L.append(f"- Cumplimiento e2e: **{sc['pct_e2e']}%**")
    L.append(f"- FAIL críticos: **{sc['fails_criticos']}** · Hallazgos totales: {sc['total_hallazgos']}"
             f" · Pendientes: {sc['pendientes']}")
    L.append(f"- Deuda técnica estimada: **~{sc['deuda_horas_estimada']} h**\n")
    L += ["## 2. Semáforo por dominio", "",
          "| Dominio | PASS | FAIL | N/A | Pend. | % | Semáforo |",
          "|---|---|---|---|---|---|---|"]
    for dom, d in sc["dominios"].items():
        pct_txt = f"{d['pct']}%" if d["pct"] is not None else "—"
        L.append(f"| {dom} | {d['pass']} | {d['fail']} | {d['na']} "
                 f"| {d['pending']} | {pct_txt} | {SEMAFORO[d['semaforo']]} {d['semaforo']} |")
    L += ["", "## 3. Top hallazgos (ordenados por RICE)", ""]
    if not sc["hallazgos"]:
        L.append("Sin hallazgos FAIL/WARN. ✅\n")
    for h in sc["hallazgos"][:15]:
        L.append(f"### {ICONO[h['resultado']]} {h['id']} — {h['criterio']}")
        L.append(f"- **Severidad:** {h['severidad']} · **Dominio:** {h['dominio']} · "
                 f"**Sprint:** {h['sprint']} ({h['plazo']}) · **RICE:** {h['rice']['score']}")
        if h.get("url"):
            L.append(f"- **URL:** {h['url']}")
        if h.get("estandar"):
            L.append(f"- **Estándar:** {h['estandar']}")
        if h["evidencia"] and not isinstance(h["evidencia"], dict):
            L.append(f"- **Evidencia:** {h['evidencia']}")
        elif isinstance(h.get("evidencia"), dict) and h["evidencia"].get("locator"):
            L.append(f"- **Locator:** `{h['evidencia']['locator']}`")
        if h.get("accion"):
            L.append(f"- **Acción correctiva:** {h['accion']}")
        if h.get("esfuerzo_h"):
            L.append(f"- **Esfuerzo estimado:** ~{h['esfuerzo_h']} h")
        L.append("")
    L += ["## 4. Plan de remediación (sprints RICE)", ""]
    sprints = {}
    for h in sc["hallazgos"]:
        sprints.setdefault(h["sprint"], []).append(h)
    for sprint in sorted(sprints):
        hs = sprints[sprint]
        L.append(f"### {sprint} ({hs[0]['plazo']}) — {len(hs)} tareas")
        for h in hs:
            L.append(f"- [ ] **{h['id']}** ({h['severidad']}, RICE {h['rice']['score']}): "
                     f"{h['criterio']} — {h.get('accion', '')}")
        L.append("")
    L += ["## 5. Verificación de cierre", "",
          "| Verificación | Resultado |", "|---|---|",
          f"| 0 FAIL críticos | {'✅' if sc['fails_criticos'] == 0 else '❌'} |",
          f"| **Dictamen compliance** | **{sc['dictamen']}** |",
          f"| **Veredicto e2e** | **{sc['veredicto_e2e']}** |", "",
          "## 6. Próximos pasos", "",
          "1. Ejecutar Sprint 0 (FAIL críticos) y re-auditar de forma parcial.",
          "2. Completar checks 🔎 PENDING con los protocolos manuales de core/references/.",
          "3. Aplicar roadmap RICE completo (4 sprints) y mejoras proactivas.",
          "4. Fijar re-auditoría trimestral y declaración de accesibilidad (EN 301 549)."]
    return "\n".join(L) + "\n"


def render_html(sc, target):
    rows = []
    for h in sc["hallazgos"]:
        ev = h.get("evidencia") if isinstance(h.get("evidencia"), dict) else {}
        rows.append(
            f"<tr data-sev='{html.escape(h['severity'] if 'severity' in h else h['severidad'])}'>"
            f"<td>{html.escape(h['id'])}</td><td>{html.escape(h['dominio'])}</td>"
            f"<td>{html.escape(h['criterio'])}</td><td>{html.escape(h['resultado'])}</td>"
            f"<td>{html.escape(h['severidad'])}</td><td>{h['rice']['score']}</td>"
            f"<td>{html.escape(h['sprint'])}</td>"
            f"<td>{html.escape(str(ev.get('locator', '')))}</td>"
            f"<td>{html.escape(h.get('accion', ''))}</td></tr>")
    pct = sc["pct_global"] if sc["pct_global"] is not None else "—"
    return f"""<!DOCTYPE html>
<html lang="es"><head><meta charset="utf-8">
<title>Fullaudit — {html.escape(target)}</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body{{font-family:system-ui,sans-serif;margin:2rem;color:#1a1a1a}}
table{{border-collapse:collapse;width:100%;font-size:.85rem}}
th,td{{border:1px solid #ddd;padding:.4rem;text-align:left}}
th{{background:#f3f4f6;position:sticky;top:0}}
</style></head><body>
<h1>Fullaudit — {html.escape(target)}</h1>
<p>Dictamen: <strong>{html.escape(sc['dictamen'])}</strong> ·
Veredicto e2e: <strong>{html.escape(sc['veredicto_e2e'])}</strong> ·
Global: <strong>{pct}%</strong> · FAIL críticos: <strong>{sc['fails_criticos']}</strong></p>
<table><thead><tr><th>ID</th><th>Dominio</th><th>Criterio</th><th>Estado</th>
<th>Severidad</th><th>RICE</th><th>Sprint</th><th>Locator</th><th>Acción</th></tr></thead>
<tbody>{''.join(rows)}</tbody></table></body></html>"""


def write_csv(sc, path):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["id", "url", "dominio", "criterio", "resultado", "severidad",
                    "sprint", "rice_score", "estandar", "accion"])
        for h in sc["hallazgos"]:
            w.writerow([h["id"], h.get("url", ""), h["dominio"], h["criterio"],
                        h["resultado"], h["severidad"], h["sprint"], h["rice"]["score"],
                        h.get("estandar") or "", h.get("accion", "")])


def main(argv=None) -> int:
    logging.basicConfig(stream=sys.stderr, level=logging.WARNING,
                        format="%(levelname)s %(name)s: %(message)s")
    ap = argparse.ArgumentParser(description="Informe de cierre dual web-fullaudit")
    ap.add_argument("entrada", help="JSON de scoring (o de checks con --from-checks)")
    ap.add_argument("--from-checks", action="store_true")
    ap.add_argument("--config", help="Directorio de configs")
    ap.add_argument("--md", help="Guardar informe Markdown")
    ap.add_argument("--outdir", help="Generar REPORT.md + REPORT.html + issues.csv en DIR")
    ap.add_argument("--target", help="URL objetivo (cabecera del informe)")
    args = ap.parse_args(argv)

    try:
        with open(args.entrada, encoding="utf-8") as fh:
            data = json.load(fh)
    except OSError as e:
        logger.error("no se pudo leer %s: %s: %s", args.entrada, type(e).__name__, e)
        return 2
    except json.JSONDecodeError as e:
        logger.error("JSON inválido en %s: %s", args.entrada, e)
        return 2
    try:
        if args.from_checks:
            checks = data.get("checks", []) if isinstance(data, dict) else data
            if not isinstance(checks, list):
                raise ValueError("con --from-checks la entrada debe traer array de checks")
            sc = score(checks, config_dir=args.config)
            sc["target"] = data.get("target") if isinstance(data, dict) else None
        else:
            if not isinstance(data, dict):
                raise ValueError("el JSON de scoring debe ser un objeto")
            sc = data
            for clave in ("dictamen", "veredicto_e2e", "dominios", "hallazgos"):
                if clave not in sc:
                    raise ValueError(f"el JSON de scoring no trae '{clave}' (¿olvidaste --from-checks?)")
        md = render_md(sc)
    except (ValueError, KeyError, TypeError, AttributeError) as e:
        logger.error("no se pudo generar el informe: %s: %s", type(e).__name__, e)
        return 1
    except RuntimeError as e:
        logger.error("%s", e)
        return 2
    if args.target:
        sc["target"] = args.target
    if args.outdir:
        try:
            os.makedirs(args.outdir, exist_ok=True)
            target = sc.get("target") or "(sin especificar)"
            with open(os.path.join(args.outdir, "REPORT.md"), "w", encoding="utf-8") as fh:
                fh.write(md)
            with open(os.path.join(args.outdir, "REPORT.html"), "w", encoding="utf-8") as fh:
                fh.write(render_html(sc, target))
            write_csv(sc, os.path.join(args.outdir, "issues.csv"))
        except OSError as e:
            logger.error("no se pudo escribir en %s: %s: %s", args.outdir, type(e).__name__, e)
            print(md)
            return 2
        print(f"Generados en {args.outdir}: REPORT.md, REPORT.html, issues.csv")
        return 0
    if args.md:
        try:
            with open(args.md, "w", encoding="utf-8") as fh:
                fh.write(md)
        except OSError as e:
            logger.error("no se pudo escribir %s: %s: %s", args.md, type(e).__name__, e)
            print(md)
            return 2
    try:
        print(md)
    except BrokenPipeError:
        pass
    return 0


if __name__ == "__main__":
    sys.exit(main())
