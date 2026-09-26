"""CLI: --help exit 0 y args inválidos exit 2 en los 5 scripts (sin red)."""
import pytest

import discovery
import measure_analyze
import report as report_mod
import score as score_mod
import validate_compliance


@pytest.mark.parametrize("mod,args", [
    (discovery, ["--help"]),
    (measure_analyze, ["--help"]),
    (score_mod, ["--help"]),
    (report_mod, ["--help"]),
    (validate_compliance, ["--help"]),
])
def test_help_exit_0(mod, args, capsys):
    with pytest.raises(SystemExit) as e:
        mod.main(args)
    assert e.value.code == 0


def test_discovery_sin_args_exit_2(capsys):
    with pytest.raises(SystemExit) as e:
        discovery.main([])
    assert e.value.code == 2


def test_measure_sin_args_exit_2(capsys):
    with pytest.raises(SystemExit) as e:
        measure_analyze.main([])
    assert e.value.code == 2


def test_score_sin_args_exit_2(capsys):
    with pytest.raises(SystemExit) as e:
        score_mod.main([])
    assert e.value.code == 2


def test_report_sin_args_exit_2(capsys):
    with pytest.raises(SystemExit) as e:
        report_mod.main([])
    assert e.value.code == 2


def test_validate_sin_args_exit_2(capsys):
    with pytest.raises(SystemExit) as e:
        validate_compliance.main([])
    assert e.value.code == 2


def test_discovery_dir_inexistente_exit_2(capsys):
    assert discovery.main(["--root-dir", "/no/existe-xyz"]) == 2


def test_measure_fichero_inexistente_exit_2(capsys):
    assert measure_analyze.main(["/no/existe-xyz.json"]) == 2


def test_score_fichero_inexistente_exit_2(capsys):
    assert score_mod.main(["/no/existe-xyz.json"]) == 2


def test_report_fichero_inexistente_exit_2(capsys):
    assert report_mod.main(["/no/existe-xyz.json"]) == 2


def test_validate_fichero_inexistente_exit_2(capsys):
    assert validate_compliance.main(["/no/existe-xyz.json"]) == 2
