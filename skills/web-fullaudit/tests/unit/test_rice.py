"""Unit: RICE y sprints (4 sprints, severidad ES normalizada)."""
import rice


def test_rice_score_critico():
    r = rice.rice_score("Crítico")
    assert r["score"] == round(9 * 9 * 8 / 3)


def test_sprints_cuatro():
    assert rice.sprint_for("Crítico")[0] == "Sprint 0"
    assert rice.sprint_for("Alto")[0] == "Sprint 1"
    assert rice.sprint_for("Medio")[0] == "Sprint 2"
    assert rice.sprint_for("Bajo")[0] == "Sprint 3"


def test_normaliza_femenino_legacy():
    assert rice.normalizar_severidad("Crítica") == "Crítico"
    assert rice.normalizar_severidad("Alta") == "Alto"
