"""Unit: scoring dual (dictamen compliance + veredicto e2e)."""
import sys

score_mod = sys.modules["web_fullaudit_scoring_score"]


def test_score_dual_basico():
    out = score_mod.score([
        {"id": "ACC-01", "resultado": "PASS"},
        {"id": "RT-01", "status": "PASS", "url": "https://ejemplo.test/"},
    ])
    assert out["dictamen"] in ("POSITIVO", "PARCIAL", "NEGATIVO", "SIN DATOS")
    assert out["veredicto_e2e"] in ("APTO", "APTO CON OBSERVACIONES", "NO APTO", "SIN DATOS")
    assert out["pct_global"] is not None


def test_fail_critico_fuerza_negativo_y_no_apto():
    out = score_mod.score([
        {"id": "ACC-01", "resultado": "FAIL", "evidencia": "x"},
        {"id": "RT-01", "status": "FAIL", "severity": "Crítica", "url": "https://ejemplo.test/"},
    ])
    # RT-01 es severidad Crítica en registry -> NO APTO; ACC-01 es Alto -> no fuerza NEGATIVO solo
    assert out["veredicto_e2e"] == "NO APTO"
    assert out["fails_criticos"] >= 1


def test_registry_93_checks_unicos():
    reg, th = score_mod.load_configs()
    assert len(reg["checks"]) == 93
    ids = [c["id"] for c in reg["checks"]]
    assert len(ids) == len(set(ids))
    assert th["semaforo"] == {"verde": 90, "ambar": 70}