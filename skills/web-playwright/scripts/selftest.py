#!/usr/bin/env python3
"""Suite de tests integrada de playwright-e2e-audit.

Cubre: configs, crawler (fixture offline), medición UI, validación de schema,
scoring/RICE y generación de informes. Ejecutar tras cualquier cambio:
    python3 scripts/selftest.py
Exit 0 = todo PASS · 1 = algún FAIL (ver references/troubleshooting.md).

NOTA DE DISEÑO (hardening 2026): se mantiene como *smoke ejecutable* con exit
codes 0/1 y logging a stderr, sin dependencia de pytest. Los tests pytest
reales (asserts granulares, fixtures dorados, errores simulados sin red)
viven en tests/test_*.py. No importar este módulo desde pytest: los
decoradores @test se ejecutan en tiempo de importación por diseño.
"""
import argparse
import json
import logging
import os
import subprocess
import sys
import tempfile

logger = logging.getLogger("e2e.selftest")

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
FIX = os.path.join(ROOT, "tests", "fixtures")
sys.path.insert(0, HERE)

import discovery  # noqa: E402
import measure_analyze  # noqa: E402
import report as report_mod  # noqa: E402
import score as score_mod  # noqa: E402
import validate_compliance  # noqa: E402

RESULTADOS = []


def test(nombre):
    def deco(fn):
        try:
            fn()
            RESULTADOS.append((nombre, "PASS", ""))
        except AssertionError as e:
            logger.warning("FAIL %s: %s", nombre, e)
            RESULTADOS.append((nombre, "FAIL", str(e)))
        except Exception as e:  # un test nunca interrumpe la suite
            logger.warning("ERROR %s: %s: %s", nombre, type(e).__name__, e)
            RESULTADOS.append((nombre, "ERROR", f"{type(e).__name__}: {e}"))
    return deco


# ---------------------------------------------------------------- configs

@test("configs: checks.json válido, IDs únicos, pesos = 1.0")
def _():
    checks, th = score_mod.load_configs()
    ids = [c["id"] for c in checks["checks"]]
    assert len(ids) == len(set(ids)), "IDs duplicados"
    for c in checks["checks"]:
        assert c["categoria"] in checks["categorias"], f"{c['id']} categoría desconocida"
        assert c["severidad"] in checks["severidades"], f"{c['id']} severidad inválida"
        assert c["id"].startswith(checks["categorias"][c["categoria"]]["prefijo"]), \
            f"{c['id']} no usa el prefijo de su categoría"
    peso = sum(v["peso"] for v in checks["categorias"].values())
    assert abs(peso - 1.0) < 0.001, f"pesos suman {peso}"


# ---------------------------------------------------------------- discovery

@test("discovery: minisite offline — mapa, 404, formularios y anti-trampas")
def _():
    cfg = discovery.load_thresholds()
    nodes, errors = discovery.crawl_offline(os.path.join(FIX, "minisite"), cfg)
    urls = {n["url"] for n in nodes}
    assert "local://site/" in urls and "local://site/about.html" in urls
    assert "local://site/contacto.html" in urls
    roto = next(n for n in nodes if n["url"].endswith("/roto.html"))
    assert roto["status"] == 404, "enlace roto no detectado"
    form = next(n for n in nodes if n["url"].endswith("/contacto.html"))
    assert form["type"] == "form" and form["discoveredElements"] >= 2
    # anti-trampas: paginación cortada a 5, ?page=6/7/abc fuera, logout/admin fuera
    assert not any("page=6" in u or "page=7" in u or "page=abc" in u for u in urls), urls
    assert not any("/logout" in u or "/admin" in u for u in urls), urls
    pages = [u for u in urls if "page=" in u]
    assert len(pages) == 5, f"paginación: {pages}"


@test("discovery: normalize_url canoniza fragmentos, query y trailing slash")
def _():
    a = discovery.normalize_url("https://X.com/path/?b=2&a=1#frag")
    b = discovery.normalize_url("https://x.com/path?a=1&b=2")
    assert a == b, f"{a} != {b}"
    assert discovery.normalize_url("https://x.com/") == "https://x.com/"


@test("discovery: CLI offline genera site-map.json y exit 0; dir inexistente exit 2")
def _():
    with tempfile.TemporaryDirectory() as td:
        out = os.path.join(td, "site-map.json")
        rc = discovery.main(["--root-dir", os.path.join(FIX, "minisite"), "--out", out])
        assert rc == 0 and os.path.isfile(out)
        data = json.load(open(out, encoding="utf-8"))
        assert data["pages_error"] >= 1 and data["forms_found"] == 1
    assert discovery.main(["--root-dir", "/no/existe"]) == 2


# ---------------------------------------------------------------- measure

@test("measure_analyze: fixture sucio detecta UI-01 duro, UI-02, UI-04, UI-05, UI-06")
def _():
    data = json.load(open(os.path.join(FIX, "measurements_sample.json"), encoding="utf-8"))
    checks = {c["id"]: c for c in measure_analyze.analyze(data)}
    assert checks["UI-01"]["status"] == "FAIL" and checks["UI-01"]["severity"] == "Crítica"
    assert checks["UI-02"]["status"] == "FAIL"   # font 10px
    assert checks["UI-04"]["status"] == "FAIL"   # 1200x1200 render 400x200
    assert checks["UI-05"]["status"] == "FAIL"   # 412 > 390
    assert checks["UI-06"]["status"] == "WARN"   # header 240/844 = 28%


@test("measure_analyze: fixture limpio pasa todos los checks")
def _():
    data = json.load(open(os.path.join(FIX, "measurements_clean.json"), encoding="utf-8"))
    checks = measure_analyze.analyze(data)
    malos = [c for c in checks if c["status"] in ("FAIL", "WARN")]
    assert not malos, [f"{c['id']}:{c['status']}" for c in malos]


@test("measure_analyze: página sin clickables -> UI-01 N/A (no inventa PASS)")
def _():
    checks = measure_analyze.analyze({"url": "https://x.test", "viewport": {"w": 1440, "h": 900},
                                      "elements": []})
    ui01 = next(c for c in checks if c["id"] == "UI-01")
    assert ui01["status"] == "N/A"


# ---------------------------------------------------------------- validate

@test("validate_compliance: fixture válido pasa; inválido enumera errores")
def _():
    assert validate_compliance.main([os.path.join(FIX, "compliance_valid.json")]) == 0
    assert validate_compliance.main([os.path.join(FIX, "compliance_invalid.json")]) == 1
    errors = validate_compliance.validate(
        json.load(open(os.path.join(FIX, "compliance_invalid.json"), encoding="utf-8")))
    assert any("category" in e for e in errors)
    assert any("severity" in e for e in errors)
    assert any("URI" in e or "url" in e for e in errors)
    assert any("falta campo requerido 'id'" in e for e in errors)


@test("validate_compliance: FAIL sin evidencia es rechazado (regla de oro)")
def _():
    bad = [{"id": "FN-01", "url": "https://x.test", "category": "Funcional",
            "check": "c", "status": "FAIL", "severity": "Alta"}]
    assert any("evidencia" in e for e in validate_compliance.validate(bad))
    good = [dict(bad[0], method="trial-click")]
    assert validate_compliance.validate(good) == []


# ---------------------------------------------------------------- score

@test("score: FAIL crítica => NO APTO; sin críticas y >=90% => APTO")
def _():
    comp = json.load(open(os.path.join(FIX, "compliance_valid.json"), encoding="utf-8"))
    sc = score_mod.score(comp)
    assert sc["veredicto"] in ("APTO", "APTO CON OBSERVACIONES")
    assert sc["categorias"]["Motion"]["semaforo"] == "SIN DATOS"  # solo N/A
    comp_crit = comp + [{"id": "FM-03", "url": "https://ejemplo.test/c", "category": "Formularios",
                         "check": "submit 500", "status": "FAIL", "severity": "Crítica",
                         "evidence": {"console": ["500 POST /enviar"]}}]
    assert score_mod.score(comp_crit)["veredicto"] == "NO APTO"


@test("score: RICE calculado y sprints asignados por severidad")
def _():
    comp = [{"id": "X1", "url": "https://x.test", "category": "Funcional", "check": "c",
             "status": "FAIL", "severity": "Crítica", "evidence": {"locator": "b"}},
            {"id": "X2", "url": "https://x.test", "category": "SEO", "check": "c",
             "status": "WARN", "severity": "Baja", "evidence": {"locator": "t"}}]
    sc = score_mod.score(comp)
    h = {x["id"]: x for x in sc["hallazgos"]}
    assert h["X1"]["sprint"] == "Sprint 0" and h["X1"]["rice"]["score"] == 216
    assert h["X2"]["sprint"] == "Sprint 3"
    assert sc["pct_global"] == 0


# ---------------------------------------------------------------- report

@test("report: genera REPORT.md, REPORT.html e issues.csv coherentes")
def _():
    with tempfile.TemporaryDirectory() as td:
        comp = json.load(open(os.path.join(FIX, "compliance_valid.json"), encoding="utf-8"))
        sc = score_mod.score(comp)
        spath = os.path.join(td, "score.json")
        json.dump(sc, open(spath, "w", encoding="utf-8"))
        assert report_mod.main([spath, "--outdir", td, "--target", "https://ejemplo.test"]) == 0
        md = open(os.path.join(td, "REPORT.md"), encoding="utf-8").read()
        assert "Veredicto" in md and "RICE" in md and "Sprint" in md and "❌" in md
        html = open(os.path.join(td, "REPORT.html"), encoding="utf-8").read()
        assert "<table" in html and "Filtrar severidad" in html
        csv_txt = open(os.path.join(td, "issues.csv"), encoding="utf-8").read()
        assert "UI-01" in csv_txt


# ---------------------------------------------------------------- main

def main(argv=None) -> int:
    logging.basicConfig(stream=sys.stderr, level=logging.WARNING,
                        format="%(levelname)s %(name)s: %(message)s")
    ap = argparse.ArgumentParser(description="Smoke test integrado de playwright-e2e-audit (exit 0/1)")
    ap.parse_args(argv)
    print("=" * 64)
    print("SELFTEST playwright-e2e-audit")
    print("=" * 64)
    fallos = 0
    for nombre, estado, detalle in RESULTADOS:
        icono = {"PASS": "✅", "FAIL": "❌", "ERROR": "💥"}[estado]
        print(f"{icono} {estado:5} {nombre}" + (f" — {detalle}" if detalle else ""))
        if estado != "PASS":
            fallos += 1
    print("=" * 64)
    print(f"{len(RESULTADOS) - fallos}/{len(RESULTADOS)} tests superados")
    return 1 if fallos else 0


if __name__ == "__main__":
    sys.exit(main())
