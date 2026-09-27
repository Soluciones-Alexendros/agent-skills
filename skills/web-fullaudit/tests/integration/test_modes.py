"""Integration: 1 test por modo via orchestrator/score (sin red)."""
import os

import orchestrator
import score as score_mod

FIX = os.path.join(os.path.dirname(__file__), "..", "fixtures")


def test_modo_compliance():
    out = orchestrator.run("compliance", checks=[os.path.join(FIX, "sample_compliance.json")],
                           outdir=os.path.join("/tmp", "fa-compliance"),
                           target="https://ejemplo.test")
    assert out["mode"] == "compliance" and "dictamen" in out


def test_modo_e2e():
    out = orchestrator.run("e2e", compliance=os.path.join(FIX, "compliance_valid.json"),
                           outdir=os.path.join("/tmp", "fa-e2e"),
                           target="https://ejemplo.test")
    assert out["mode"] == "e2e" and "veredicto_e2e" in out


def test_modo_performance():
    out = score_mod.score([{"id": "PF-01", "status": "PASS", "url": "https://ejemplo.test/"}])
    assert "PF" in out["dominios"] or out["pct_global"] is not None
    guia = orchestrator.run("performance")
    assert guia["mode"] == "performance" and "guia" in guia


def test_modo_local():
    out = orchestrator.run("local", target="http://localhost:5173")
    assert out["mode"] == "local" and "guia" in out


def test_modo_full_dual():
    out = orchestrator.run("full",
                           checks=[os.path.join(FIX, "sample_compliance.json"),
                                   os.path.join(FIX, "compliance_valid.json")],
                           outdir=os.path.join("/tmp", "fa-full"),
                           target="https://ejemplo.test")
    assert out["mode"] == "full"
    assert "dictamen" in out and "veredicto_e2e" in out
    assert os.path.exists(os.path.join("/tmp", "fa-full", "REPORT.md"))
