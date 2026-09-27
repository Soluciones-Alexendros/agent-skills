#!/usr/bin/env python3
"""Orquestador verificar-fullaudit: pipeline scoring→informe por modo.

Modos:
  compliance   Matriz compliance SEO/A11y/SEM/legal (audit_page + score + report).
  e2e          QA E2E con evidencias (discovery/measure/validate + score + report).
  performance  CWV/Lighthouse/rendering/caching (delegado a skill verificar-performance).
  local        App local en localhost (Playwright, flujos UI, capturas).
  full         compliance + e2e fusionados (merge_results + dictamen dual).

Uso:
    python3 orchestrator.py --mode compliance --checks resultados.json --outdir output/
    python3 orchestrator.py --mode full --checks a.json b.json --outdir output/
    python3 orchestrator.py --mode e2e --compliance compliance.json --outdir output/
    python3 orchestrator.py --mode local --url http://localhost:5173 --outdir output/
    python3 orchestrator.py --list-modes
"""
import argparse
import importlib.util
import json
import logging
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CORE_DIR = os.path.join(HERE, "..")

def _load_core_module(name, subdir):
    path = os.path.join(CORE_DIR, subdir, f"{name}.py")
    spec = importlib.util.spec_from_file_location(f"fullaudit_{subdir}_{name}", path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load {name} from {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[f"fullaudit_{subdir}_{name}"] = module
    spec.loader.exec_module(module)
    return module

merge_results = _load_core_module("merge_results", "utils")
report_mod = _load_core_module("report", "reporting")
score_mod = _load_core_module("score", "scoring")

logger = logging.getLogger("fullaudit.orchestrator")

MODES = ("compliance", "e2e", "performance", "local", "full")

GUIDE = {
    "compliance": "Ejecutar audit_page.py por plantilla, puntuar con score.py e informar con report.py.",
    "e2e": "Requiere Playwright: discovery → loop auditor (assets/auditor.agent.ts) → "
           "validate_compliance → score → report. Sin Playwright, modo degradado (crawler + estáticos).",
    "performance": "Delegado a la skill verificar-performance: Lighthouse 12, CWV lab+field, rendering, caching.",
    "local": "Requiere servidor dev arriba: script Playwright corto (networkidle), flujos y capturas.",
    "full": "Ejecuta compliance + e2e, fusiona con merge_results e informa dictamen dual.",
}


def list_modes():
    return [{"mode": m, "guia": g} for m, g in GUIDE.items()]


def _checks_from(paths):
    listas = []
    for p in paths:
        with open(p, encoding="utf-8") as fh:
            data = json.load(fh)
        if isinstance(data, dict):
            listas.append((data.get("target"), data.get("checks", [])))
        elif isinstance(data, list):
            listas.append((None, data))
        else:
            raise ValueError(f"formato inválido en {p}")
    return listas


def run(mode, checks=(), compliance=None, outdir=".", target=None, config=None):
    """Ejecuta el pipeline del modo; devuelve el dict de scoring."""
    if mode not in MODES:
        raise ValueError(f"modo desconocido: {mode} (válidos: {', '.join(MODES)})")
    if mode == "performance" and not checks:
        return {"mode": "performance", "guia": GUIDE["performance"],
                "nota": "Sin --checks: aplicar skill verificar-performance. Con --checks PF-*: se puntúan."}
    if mode == "local":
        return {"mode": "local", "guia": GUIDE["local"], "target": target,
                "nota": "Sin scripts propios: script Playwright ad-hoc contra la URL local."}
    if mode == "e2e" and compliance:
        with open(compliance, encoding="utf-8") as fh:
            data = json.load(fh)
        items = data if isinstance(data, list) else data.get("checks", [])
        out = score_mod.score(items, config_dir=config)
        out["target"] = (data.get("target") if isinstance(data, dict) else None) or target
    else:
        if not checks:
            raise ValueError(f"el modo {mode} requiere --checks (o --compliance en modo e2e)")
        target_m, merged = merge_results.merge(_checks_from(list(checks)))
        out = score_mod.score(merged, config_dir=config)
        out["target"] = target or target_m
    out["mode"] = mode
    os.makedirs(outdir, exist_ok=True)
    with open(os.path.join(outdir, "score.json"), "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=2)
    md = report_mod.render_md(out)
    with open(os.path.join(outdir, "REPORT.md"), "w", encoding="utf-8") as fh:
        fh.write(md)
    report_mod.write_csv(out, os.path.join(outdir, "issues.csv"))
    with open(os.path.join(outdir, "REPORT.html"), "w", encoding="utf-8") as fh:
        fh.write(report_mod.render_html(out, out.get("target") or "(sin especificar)"))
    return out


def main(argv=None) -> int:
    logging.basicConfig(stream=sys.stderr, level=logging.WARNING,
                        format="%(levelname)s %(name)s: %(message)s")
    ap = argparse.ArgumentParser(description="Orquestador verificar-fullaudit")
    ap.add_argument("--mode", choices=MODES, help="Modo de auditoría")
    ap.add_argument("--list-modes", action="store_true", help="Lista modos y sale")
    ap.add_argument("--checks", nargs="*", default=[], help="JSON de checks a puntuar/fusionar")
    ap.add_argument("--compliance", help="compliance.json (modo e2e directo)")
    ap.add_argument("--outdir", default=".", help="Directorio de salida")
    ap.add_argument("--target", help="URL objetivo")
    ap.add_argument("--config", help="Directorio de configs")
    args = ap.parse_args(argv)

    if args.list_modes:
        print(json.dumps(list_modes(), ensure_ascii=False, indent=2))
        return 0
    if not args.mode:
        ap.error("se requiere --mode (o --list-modes)")
    try:
        out = run(args.mode, checks=args.checks, compliance=args.compliance,
                  outdir=args.outdir, target=args.target, config=args.config)
    except (ValueError, RuntimeError, OSError) as e:
        logger.error("%s: %s", type(e).__name__, e)
        return 2
    except (KeyError, TypeError, AttributeError) as e:
        logger.error("datos inválidos: %s: %s", type(e).__name__, e)
        return 1
    print(json.dumps({k: out[k] for k in
                      ("mode", "target", "dictamen", "veredicto_e2e", "pct_global",
                       "pct_e2e", "fails_criticos", "total_hallazgos") if k in out},
                     ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
