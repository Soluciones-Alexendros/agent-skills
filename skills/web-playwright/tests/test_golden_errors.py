"""Dorados (valores congelados del código actual) + errores controlados sin red.

Exit codes: 0 OK · 1 inválido · 2 uso/IO.
Degradación documentada: timeout/HTTP en crawl degrada el nodo (status 0/código)
sin abortar; medidas con dimensiones no numéricas se omiten en UI-04.
"""
import json
import os
import urllib.error

import discovery
import measure_analyze
import report as report_mod
import score as score_mod
import validate_compliance
import pytest

FIX = os.path.join(os.path.dirname(__file__), "fixtures")

# ---------------------------------------------------------------- discovery

def test_discovery_minisite_dorado():
    cfg = discovery.load_thresholds()
    nodes, errors = discovery.crawl_offline(os.path.join(FIX, "minisite"), cfg)
    assert len(nodes) == 10
    assert errors == []
    by_url = {n["url"]: n for n in nodes}
    assert by_url["local://site/"]["status"] == 200
    assert by_url["local://site/contacto.html"]["type"] == "form"
    assert by_url["local://site/roto.html"]["status"] == 404
    paginadas = sorted(u for u in by_url if "page=" in u)
    assert paginadas == [f"local://site/productos?page={i}" for i in (1, 2, 3, 4, 5)]
    assert not any("/logout" in u or "/admin" in u for u in by_url)


def test_discovery_cli_offline_dorado(tmp_path, capsys):
    out = tmp_path / "site-map.json"
    assert discovery.main(["--root-dir", os.path.join(FIX, "minisite"),
                           "--out", str(out)]) == 0
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["total_pages"] == 10
    assert data["pages_ok"] == 4
    assert data["pages_error"] == 6
    assert data["forms_found"] == 1
    assert data["truncated"] is False


def test_discovery_timeout_simulado_degrada_nodo(monkeypatch):
    import urllib.request
    def _boom(req, timeout=None):
        raise TimeoutError("timed out (simulado)")
    monkeypatch.setattr(urllib.request, "urlopen", _boom)
    cfg = discovery.load_thresholds()
    nodes, errors = discovery.crawl_online("https://ejemplo.test/", cfg)
    assert len(nodes) == 1 and nodes[0]["status"] == 0
    assert len(errors) == 1 and "TimeoutError" in errors[0]["error"]


def test_discovery_http500_simulado_no_aborta(monkeypatch):
    import urllib.request
    def _boom(req, timeout=None):
        raise urllib.error.HTTPError(req.full_url, 500, "Server Error", {}, None)
    monkeypatch.setattr(urllib.request, "urlopen", _boom)
    cfg = discovery.load_thresholds()
    nodes, errors = discovery.crawl_online("https://ejemplo.test/", cfg)
    assert nodes[0]["status"] == 500 and "HTTP 500" in errors[0]["error"]

# ---------------------------------------------------------------- measure

def test_measure_sample_dorado():
    data = json.load(open(os.path.join(FIX, "measurements_sample.json"), encoding="utf-8"))
    checks = {c["id"]: c for c in measure_analyze.analyze(data)}
    assert checks["UI-01"]["status"] == "FAIL" and checks["UI-01"]["severity"] == "Crítica"
    assert checks["UI-01"]["evidence"]["count"] == 1
    assert checks["UI-01"]["evidence"]["ejemplos"][0]["locator"] == "button.more"
    assert checks["UI-02"]["status"] == "FAIL"
    assert checks["UI-03"]["status"] == "WARN" and checks["UI-03"]["evidence"]["off_grid_pct"] == 50
    assert checks["UI-04"]["status"] == "FAIL" and checks["UI-04"]["evidence"]["count"] == 1
    assert checks["UI-05"]["status"] == "FAIL"
    assert checks["UI-05"]["evidence"] == {"scrollWidth": 412, "innerWidth": 390}
    assert checks["UI-06"]["status"] == "WARN" and checks["UI-06"]["evidence"]["header_pct"] == 28.4


def test_measure_clean_dorado():
    data = json.load(open(os.path.join(FIX, "measurements_clean.json"), encoding="utf-8"))
    checks = measure_analyze.analyze(data)
    assert len(checks) == 6
    assert {c["id"] for c in checks} == {"UI-01", "UI-02", "UI-03", "UI-04", "UI-05", "UI-06"}
    assert all(c["status"] == "PASS" for c in checks)


def test_measure_dimensiones_raras_no_rompen():
    data = json.load(open(os.path.join(FIX, "measurements_edge.json"), encoding="utf-8"))
    checks = {c["id"]: c for c in measure_analyze.analyze(data)}
    assert checks["UI-04"]["status"] == "PASS"  # elementos no numéricos omitidos
    assert checks["UI-04"]["evidence"]["count"] == 0


def test_measure_json_invalido_exit_2(capsys):
    assert measure_analyze.main([os.path.join(FIX, "invalid.json")]) == 2


def test_measure_raiz_no_objeto_exit_2(tmp_path, capsys):
    p = tmp_path / "n.json"
    p.write_text("42", encoding="utf-8")
    assert measure_analyze.main([str(p)]) == 2

# ---------------------------------------------------------------- validate

def test_validate_fixtures_exit_codes(capsys):
    assert validate_compliance.main([os.path.join(FIX, "compliance_valid.json")]) == 0
    assert validate_compliance.main([os.path.join(FIX, "compliance_invalid.json")]) == 1


def test_validate_json_invalido_exit_2(capsys):
    assert validate_compliance.main([os.path.join(FIX, "invalid.json")]) == 2


def test_validate_fail_sin_evidencia_rechazado():
    bad = [{"id": "FN-01", "url": "https://x.test", "category": "Funcional",
            "check": "c", "status": "FAIL", "severity": "Alta"}]
    assert any("evidencia" in e for e in validate_compliance.validate(bad))

# ---------------------------------------------------------------- score

def test_score_valid_dorado():
    comp = json.load(open(os.path.join(FIX, "compliance_valid.json"), encoding="utf-8"))
    sc = score_mod.score(comp)
    assert sc["veredicto"] == "APTO CON OBSERVACIONES"
    assert sc["pct_global"] == 75
    assert sc["fails_criticas"] == 0
    assert sc["total_hallazgos"] == 1 and sc["total_checks"] == 5
    assert sc["categorias"]["Motion"]["semaforo"] == "SIN DATOS"
    h = sc["hallazgos"][0]
    assert h["id"] == "UI-01" and h["rice"]["score"] == 98
    assert h["sprint"] == "Sprint 1" and h["plazo"] == "Semana 1"


def test_score_rice_unidades_doradas():
    assert score_mod.rice_score("Crítica", None)["score"] == 216
    assert score_mod.rice_score("Baja", None)["score"] == 21


def test_score_critica_no_apto_dorado():
    comp = json.load(open(os.path.join(FIX, "compliance_valid.json"), encoding="utf-8"))
    comp = comp + [{"id": "FM-03", "url": "https://ejemplo.test/c", "category": "Formularios",
                    "check": "submit 500", "status": "FAIL", "severity": "Crítica",
                    "evidence": {"console": ["500 POST /enviar"]}}]
    assert score_mod.score(comp)["veredicto"] == "NO APTO"


def test_score_json_invalido_exit_2(capsys):
    assert score_mod.main([os.path.join(FIX, "invalid.json")]) == 2


def test_score_no_lista_exit_2(tmp_path, capsys):
    p = tmp_path / "obj.json"
    p.write_text('{"a": 1}', encoding="utf-8")
    assert score_mod.main([str(p)]) == 2

# ---------------------------------------------------------------- report

def test_report_happy_path_dorado(tmp_path, capsys):
    comp = json.load(open(os.path.join(FIX, "compliance_valid.json"), encoding="utf-8"))
    spath = tmp_path / "score.json"
    spath.write_text(json.dumps(score_mod.score(comp)), encoding="utf-8")
    assert report_mod.main([str(spath), "--outdir", str(tmp_path),
                            "--target", "https://ejemplo.test"]) == 0
    md = (tmp_path / "REPORT.md").read_text(encoding="utf-8")
    assert "APTO CON OBSERVACIONES" in md and "UI-01" in md
    assert "<table" in (tmp_path / "REPORT.html").read_text(encoding="utf-8")
    assert "UI-01" in (tmp_path / "issues.csv").read_text(encoding="utf-8")


def test_report_score_incompleto_exit_1(tmp_path, capsys):
    p = tmp_path / "casi.json"
    p.write_text('{"veredicto": "APTO"}', encoding="utf-8")
    assert report_mod.main([str(p), "--outdir", str(tmp_path)]) == 1


def test_report_json_invalido_exit_2(capsys):
    assert report_mod.main([os.path.join(FIX, "invalid.json"),
                            "--outdir", "/tmp"]) == 2
