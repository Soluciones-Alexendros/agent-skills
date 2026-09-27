#!/usr/bin/env python3
"""Selftest web-fullaudit: smoke ejecutable sin dependencias (exit 0/1).

Valida configs unificados, fixtures, cada módulo core y el pipeline
(merge → score → report) en los 5 modos del orquestador.
Ejecutar tras cualquier cambio:  python3 core/utils/selftest.py

No importar desde pytest (los @test se ejecutan en importación por diseño).
"""
import importlib.util
import json
import logging
import os
import sys
import tempfile

logger = logging.getLogger("fullaudit.selftest")

HERE = os.path.dirname(os.path.abspath(__file__))
CORE_DIR = os.path.join(HERE, "..")
ROOT = os.path.join(CORE_DIR, "..")
FIXTURES = os.path.join(ROOT, "tests", "fixtures")

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
orchestrator = _load_core_module("orchestrator", "utils")
report_mod = _load_core_module("report", "reporting")
rice = _load_core_module("rice", "scoring")
score_mod = _load_core_module("score", "scoring")

RESULTADOS = []


def test(nombre):
    def deco(fn):
        try:
            fn()
            RESULTADOS.append((nombre, True, ""))
        except Exception as e:  # noqa: BLE001
            RESULTADOS.append((nombre, False, f"{type(e).__name__}: {e}"))
        return fn
    return deco


@test("configs unificados válidos: 93 checks, IDs únicos, 4 sprints RICE")
def _():
    reg, th = score_mod.load_configs()
    assert len(reg["checks"]) == 93, f"se esperaban 93 checks, hay {len(reg['checks'])}"
    ids = [c["id"] for c in reg["checks"]]
    assert len(ids) == len(set(ids)), "IDs duplicados"
    assert len(th["rice"]["sprints"]) == 4, "RICE debe tener 4 sprints"
    assert th["semaforo"] == {"verde": 90, "ambar": 70}


@test("rice: score y sprint por severidad (ES normalizada)")
def _():
    r = rice.rice_score("Crítico")
    assert r["score"] == 9 * 9 * 8 // 3
    assert rice.sprint_for("Crítica")[0] == "Sprint 0"
    assert rice.sprint_for("Bajo")[0] == "Sprint 3"
    assert rice.normalizar_severidad("Alta") == "Alto"


@test("merge: FAIL no pisado por PASS + dual compliance/e2e")
def _():
    t, checks = merge_results.merge([
        (None, [{"id": "ACC-01", "resultado": "FAIL", "evidencia": "sin alt"}]),
        (None, [{"id": "ACC-01", "resultado": "PASS"}]),
        (None, [{"id": "RT-01", "status": "PASS", "url": "https://ejemplo.test/"}]),
    ])
    por_id = {c["id"]: c for c in checks}
    assert (por_id["ACC-01"].get("resultado") or por_id["ACC-01"].get("status")) == "FAIL"
    assert len(checks) == 2


@test("score dual: dictamen compliance + veredicto e2e")
def _():
    out = score_mod.score([
        {"id": "ACC-01", "resultado": "PASS"},
        {"id": "RT-01", "status": "PASS", "url": "https://ejemplo.test/"},
        {"id": "UI-01", "status": "FAIL", "severity": "Alta",
         "url": "https://ejemplo.test/", "evidence": {"locator": "button.buy"}},
    ])
    assert out["dictamen"] in ("POSITIVO", "PARCIAL", "NEGATIVO", "SIN DATOS")
    assert out["veredicto_e2e"] in ("APTO", "APTO CON OBSERVACIONES", "NO APTO", "SIN DATOS")
    assert any(h["rice"]["score"] > 0 and h["sprint"] for h in out["hallazgos"])


@test("report: md/html/csv desde scoring")
def _():
    out = score_mod.score([{"id": "ACC-01", "resultado": "PASS"}])
    out["target"] = "https://ejemplo.test"
    md = report_mod.render_md(out)
    assert "Dictamen compliance" in md and "Veredicto e2e" in md
    assert "Fullaudit" in report_mod.render_html(out, out["target"])
    with tempfile.TemporaryDirectory() as d:
        report_mod.write_csv(out, os.path.join(d, "issues.csv"))


@test("orchestrator: 5 modos (3 ejecutables + 2 guiados)")
def _():
    assert [m["mode"] for m in orchestrator.list_modes()] == \
        ["compliance", "e2e", "performance", "local", "full"]
    with tempfile.TemporaryDirectory() as d:
        fx = os.path.join(FIXTURES, "compliance_valid.json")
        out = orchestrator.run("full", checks=[fx], outdir=d, target="https://ejemplo.test")
        assert out["mode"] == "full"
        for f in ("score.json", "REPORT.md", "REPORT.html", "issues.csv"):
            assert os.path.exists(os.path.join(d, f)), f"falta {f}"
        g = orchestrator.run("performance")
        assert g["mode"] == "performance" and "guia" in g
        loc = orchestrator.run("local", target="http://localhost:5173")
        assert loc["mode"] == "local"
        try:
            orchestrator.run("pepe")
        except ValueError:
            pass
        else:
            raise AssertionError("modo inválido debería fallar")


def main() -> int:
    fails = 0
    for nombre, ok, detalle in RESULTADOS:
        print(f"{'PASS' if ok else 'FAIL'}  {nombre}" + (f" — {detalle}" if detalle else ""))
        fails += not ok
    print(f"\n{len(RESULTADOS) - fails}/{len(RESULTADOS)} tests PASS")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
