"""Unit: merge_results (FAIL no pisado, dual compliance+e2e)."""
import merge_results


def test_fail_no_pisado_por_pass():
    _, checks = merge_results.merge([
        (None, [{"id": "ACC-01", "resultado": "FAIL", "evidencia": "sin alt"}]),
        (None, [{"id": "ACC-01", "resultado": "PASS"}]),
    ])
    assert len(checks) == 1
    assert (checks[0].get("resultado") or checks[0].get("status")) == "FAIL"


def test_merge_dual_formatos():
    target, checks = merge_results.merge([
        ("https://ejemplo.test", [{"id": "ACC-01", "resultado": "PASS"}]),
        (None, [{"id": "RT-01", "status": "PASS", "url": "https://ejemplo.test/"}]),
    ])
    assert target == "https://ejemplo.test"
    assert {c["id"] for c in checks} == {"ACC-01", "RT-01"}
