"""Unit: merge_results (FAIL no pisado, dual compliance+e2e)."""
import sys

merge_results = sys.modules["web_fullaudit_utils_merge_results"]


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


# --- merge_results additional tests for coverage ---

def test_merge_warn_no_pisado_por_pass():
    _, checks = merge_results.merge([
        (None, [{"id": "ACC-01", "resultado": "WARN", "evidencia": "contraste bajo"}]),
        (None, [{"id": "ACC-01", "resultado": "PASS"}]),
    ])
    assert len(checks) == 1
    assert (checks[0].get("resultado") or checks[0].get("status")) == "WARN"


def test_merge_fail_pisado_por_fail_con_mejor_evidencia():
    _, checks = merge_results.merge([
        (None, [{"id": "ACC-01", "resultado": "FAIL", "evidencia": "corta"}]),
        (None, [{"id": "ACC-01", "resultado": "FAIL", "evidencia": "evidencia mucho mas completa y detallada"}]),
    ])
    assert len(checks) == 1
    assert checks[0]["evidencia"] == "evidencia mucho mas completa y detallada"


def test_merge_warn_pisado_por_warn_con_mejor_evidencia():
    _, checks = merge_results.merge([
        (None, [{"id": "ACC-01", "resultado": "WARN", "evidencia": "corta"}]),
        (None, [{"id": "ACC-01", "resultado": "WARN", "evidencia": "evidencia mucho mas completa"}]),
    ])
    assert len(checks) == 1
    assert checks[0]["evidencia"] == "evidencia mucho mas completa"


def test_merge_diferentes_ids():
    _, checks = merge_results.merge([
        (None, [{"id": "ACC-01", "resultado": "PASS"}]),
        (None, [{"id": "RT-01", "status": "PASS", "url": "https://ejemplo.test/"}]),
    ])
    assert {c["id"] for c in checks} == {"ACC-01", "RT-01"}


def test_merge_orden_preservado():
    _, checks = merge_results.merge([
        (None, [{"id": "ACC-01", "resultado": "PASS"}]),
        (None, [{"id": "ACC-02", "resultado": "FAIL"}]),
        (None, [{"id": "ACC-03", "resultado": "WARN"}]),
    ])
    assert [c["id"] for c in checks] == ["ACC-01", "ACC-02", "ACC-03"]


def test_merge_script_key_fallback():
    _, checks = merge_results.merge([
        (None, [{"script_key": "ACC-01", "resultado": "PASS"}]),
        (None, [{"script_key": "ACC-01", "resultado": "FAIL"}]),
    ])
    assert len(checks) == 1
    assert (checks[0].get("resultado") or checks[0].get("status")) == "FAIL"


def test_merge_na_normalizado():
    # NA -> PASS se sobreescribe (NA no es FAIL/WARN)
    _, checks = merge_results.merge([
        (None, [{"id": "ACC-01", "resultado": "NA"}]),
        (None, [{"id": "ACC-01", "resultado": "PASS"}]),
    ])
    assert len(checks) == 1
    assert (checks[0].get("resultado") or checks[0].get("status")) == "PASS"


def test_merge_evidence_evidencia_alias():
    # segundo item con 'evidencia' pisa al primero con 'evidence' (comportamiento actual)
    _, checks = merge_results.merge([
        (None, [{"id": "ACC-01", "resultado": "FAIL", "evidence": "test"}]),
        (None, [{"id": "ACC-01", "resultado": "FAIL", "evidencia": "otro"}]),
    ])
    assert len(checks) == 1
    assert checks[0].get("evidencia") == "otro"


def test_merge_items_sin_id_saltados():
    _, checks = merge_results.merge([
        (None, [{"resultado": "PASS"}]),  # sin id
        (None, [{"id": "ACC-01", "resultado": "FAIL"}]),
    ])
    assert len(checks) == 1
    assert checks[0]["id"] == "ACC-01"


def test_merge_lista_vacia():
    target, checks = merge_results.merge([])
    assert target is None
    assert checks == []


def test_merge_main_help():
    import subprocess
    import sys
    import os
    script_path = os.path.join(os.path.dirname(__file__), "..", "..", "core", "utils", "merge_results.py")
    r = subprocess.run([sys.executable, script_path, "--help"],
                       capture_output=True, text=True)
    assert r.returncode == 0