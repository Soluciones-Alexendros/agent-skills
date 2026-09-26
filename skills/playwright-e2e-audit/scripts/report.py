#!/usr/bin/env python3
"""Genera entregables de la auditoría: REPORT.md, REPORT.html e issues.csv.

Entrada: score.json (de scripts/score.py).

Uso: python3 report.py score.json --outdir output/
"""
import argparse
import csv
import datetime
import html
import json
import logging
import os
import sys

logger = logging.getLogger("e2e.report")

ICONO = {"PASS": "✅", "FAIL": "❌", "WARN": "⚠️", "N/A": "➖"}
SEMAFORO = {"VERDE": "🟢", "AMBAR": "🟠", "ROJO": "🔴", "SIN DATOS": "⚪"}
VERD_ICON = {"APTO": "✅", "APTO CON OBSERVACIONES": "⚠️", "NO APTO": "❌", "SIN DATOS": "⚪"}


def render_md(sc, target):
    fecha = datetime.date.today().isoformat()
    L = ["# REPORT.md — Auditoría E2E Playwright", "",
         f"**Objetivo:** {target}  ",
         f"**Fecha:** {fecha}  ",
         f"**Framework:** Playwright E2E Audit v2 · WCAG 2.2 AA · Core Web Vitals", "",
         "## Resumen ejecutivo", "",
         f"- **Veredicto: {VERD_ICON.get(sc['veredicto'], '')} {sc['veredicto']}** — {sc['motivo']}",
         f"- Cumplimiento global: **{sc['pct_global']}%**" if sc["pct_global"] is not None
         else "- Cumplimiento global: SIN DATOS",
         f"- FAIL críticas: **{sc['fails_criticas']}** · Hallazgos: {sc['total_hallazgos']}"
         f" de {sc['total_checks']} checks", "",
         "## Semáforo por categoría", "",
         "| Categoría | PASS | FAIL | WARN | N/A | % | Semáforo |", "|---|---|---|---|---|---|---|"]
    for cat, c in sc["categorias"].items():
        pct = f"{c['pct']}%" if c["pct"] is not None else "—"
        L.append(f"| {cat} | {c['pass']} | {c['fail']} | {c['warn']} | {c['na']} "
                 f"| {pct} | {SEMAFORO[c['semaforo']]} {c['semaforo']} |")
    L += ["", "## Top hallazgos (ordenados por RICE)", ""]
    for h in sc["hallazgos"][:10]:
        L.append(f"### {ICONO[h['status']]} {h['id']} — {h['check']}")
        L.append(f"- **Severidad:** {h['severity']} · **Categoría:** {h['category']} · "
                 f"**Sprint:** {h['sprint']} ({h['plazo']}) · **RICE:** {h['rice']['score']}")
        L.append(f"- **URL:** {h['url']}")
        ev = h.get("evidence") or {}
        if ev.get("locator"):
            L.append(f"- **Locator:** `{ev['locator']}`")
        if ev.get("screenshot"):
            L.append(f"- **Evidencia:** {ev['screenshot']}")
        if ev.get("console"):
            L.append(f"- **Consola:** {'; '.join(str(x)[:100] for x in ev['console'][:3])}")
        if h.get("wcag_ref"):
            L.append(f"- **WCAG:** {h['wcag_ref']}")
        if h.get("recommendation"):
            L.append(f"- **Recomendación:** {h['recommendation']}")
        L.append("")
    L += ["## Plan de remediación (sprints RICE)", ""]
    sprints = {}
    for h in sc["hallazgos"]:
        sprints.setdefault(h["sprint"], []).append(h)
    for sprint in sorted(sprints):
        hs = sprints[sprint]
        L.append(f"### {sprint} ({hs[0]['plazo']}) — {len(hs)} tareas")
        for h in hs:
            L.append(f"- [ ] **{h['id']}** ({h['severity']}, RICE {h['rice']['score']}): "
                     f"{h['check']} — {h.get('recommendation', '')}")
        L.append("")
    L.append("## Verificación de cierre")
    L.append("")
    L.append("| Verificación | Resultado |")
    L.append("|---|---|")
    L.append(f"| 0 FAIL críticas | {'✅' if sc['fails_criticas'] == 0 else '❌'} |")
    for cat, c in sc["categorias"].items():
        if c["pct"] is not None:
            L.append(f"| {cat}: {c['pct']}% | {'✅' if c['semaforo'] == 'VERDE' else '❌'} |")
    L.append(f"| **Veredicto global** | **{VERD_ICON.get(sc['veredicto'], '')} {sc['veredicto']}** |")
    return "\n".join(L) + "\n"


def render_html(sc, target):
    rows = []
    for h in sc["hallazgos"]:
        ev = h.get("evidence") or {}
        rows.append(
            f"<tr data-sev='{html.escape(h['severity'])}' data-cat='{html.escape(h['category'])}'>"
            f"<td>{html.escape(h['id'])}</td><td>{html.escape(h['category'])}</td>"
            f"<td>{html.escape(h['check'])}</td><td>{html.escape(h['status'])}</td>"
            f"<td>{html.escape(h['severity'])}</td><td>{h['rice']['score']}</td>"
            f"<td>{html.escape(h['sprint'])}</td>"
            f"<td>{html.escape(str(ev.get('locator', '')))}</td>"
            f"<td>{html.escape(h.get('recommendation', ''))}</td></tr>")
    pct = sc["pct_global"] if sc["pct_global"] is not None else "—"
    return f"""<!DOCTYPE html>
<html lang="es"><head><meta charset="utf-8">
<title>Auditoría E2E — {html.escape(target)}</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body{{font-family:system-ui,sans-serif;margin:2rem;color:#1a1a1a}}
.badge{{padding:.3rem .8rem;border-radius:1rem;font-weight:700;color:#fff}}
.APTO{{background:#15803d}}.NO.APTO,.NOAPTO{{background:#b91c1c}}
table{{border-collapse:collapse;width:100%;font-size:.85rem}}
th,td{{border:1px solid #ddd;padding:.4rem;text-align:left}}
th{{background:#f3f4f6;position:sticky;top:0}}
select{{margin:.3rem .5rem .3rem 0;padding:.3rem}}
</style></head><body>
<h1>Auditoría E2E — {html.escape(target)}</h1>
<p>Veredicto: <strong>{html.escape(sc['veredicto'])}</strong> · Cumplimiento: <strong>{pct}%</strong> ·
FAIL críticas: <strong>{sc['fails_criticas']}</strong> · Hallazgos: {sc['total_hallazgos']}</p>
<div>
<label>Filtrar severidad <select id="fsev"><option value="">Todas</option>
<option>Crítica</option><option>Alta</option><option>Media</option><option>Baja</option></select></label>
<label>Categoría <select id="fcat"><option value="">Todas</option>
{''.join(f'<option>{html.escape(c)}</option>' for c in sc['categorias'])}</select></label>
</div>
<table id="t"><thead><tr><th>ID</th><th>Categoría</th><th>Check</th><th>Estado</th>
<th>Severidad</th><th>RICE</th><th>Sprint</th><th>Locator</th><th>Recomendación</th></tr></thead>
<tbody>{''.join(rows)}</tbody></table>
<script>
const f=()=>{{const s=document.getElementById('fsev').value,c=document.getElementById('fcat').value;
document.querySelectorAll('#t tbody tr').forEach(r=>{{
r.style.display=((!s||r.dataset.sev===s)&&(!c||r.dataset.cat===c))?'':'none';}});}};
document.getElementById('fsev').onchange=f;document.getElementById('fcat').onchange=f;
</script></body></html>"""


def write_csv(sc, path):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["id", "url", "categoria", "check", "status", "severidad",
                    "sprint", "rice_score", "locator", "wcag_ref", "recomendacion"])
        for h in sc["hallazgos"]:
            w.writerow([h["id"], h["url"], h["category"], h["check"], h["status"],
                        h["severity"], h["sprint"], h["rice"]["score"],
                        (h.get("evidence") or {}).get("locator", ""),
                        h.get("wcag_ref") or "", h.get("recommendation", "")])


def main(argv=None) -> int:
    logging.basicConfig(stream=sys.stderr, level=logging.WARNING,
                        format="%(levelname)s %(name)s: %(message)s")
    ap = argparse.ArgumentParser(description="Genera REPORT.md/html + issues.csv")
    ap.add_argument("score", help="score.json de scripts/score.py")
    ap.add_argument("--outdir", default=".")
    ap.add_argument("--target", help="URL objetivo (cabecera del informe)")
    args = ap.parse_args(argv)
    try:
        with open(args.score, encoding="utf-8") as fh:
            sc = json.load(fh)
    except OSError as e:
        logger.error("no se pudo leer %s: %s: %s", args.score, type(e).__name__, e)
        return 2
    except json.JSONDecodeError as e:
        logger.error("JSON inválido en %s: %s", args.score, e)
        return 2
    if not isinstance(sc, dict):
        logger.error("formato inválido en %s: se esperaba objeto score", args.score)
        return 1
    for clave in ("veredicto", "categorias", "hallazgos"):
        if clave not in sc:
            logger.error("el score de %s no trae '%s'", args.score, clave)
            return 1
    target = args.target or sc.get("target") or "(sin especificar)"
    try:
        os.makedirs(args.outdir, exist_ok=True)
    except OSError as e:
        logger.error("no se pudo crear %s: %s: %s", args.outdir, type(e).__name__, e)
        return 2
    try:
        md = render_md(sc, target)
        html_txt = render_html(sc, target)
    except (KeyError, TypeError, AttributeError) as e:
        logger.error("no se pudo renderizar el informe: %s: %s", type(e).__name__, e)
        return 1
    try:
        with open(os.path.join(args.outdir, "REPORT.md"), "w", encoding="utf-8") as fh:
            fh.write(md)
        with open(os.path.join(args.outdir, "REPORT.html"), "w", encoding="utf-8") as fh:
            fh.write(html_txt)
        write_csv(sc, os.path.join(args.outdir, "issues.csv"))
    except OSError as e:
        logger.error("no se pudo escribir en %s: %s: %s", args.outdir, type(e).__name__, e)
        return 2
    print(f"Generados en {args.outdir}: REPORT.md, REPORT.html, issues.csv")
    return 0


if __name__ == "__main__":
    sys.exit(main())
