"""Fixtures compartidos: core/* cargados via importlib para aislamiento."""
import os
import sys
import importlib.util

ROOT = os.path.join(os.path.dirname(__file__), "..")

def _load_core_module(name, subdir):
    path = os.path.join(ROOT, "core", subdir, f"{name}.py")
    spec = importlib.util.spec_from_file_location(f"web_fullaudit_{subdir}_{name}", path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load {name} from {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[f"web_fullaudit_{subdir}_{name}"] = module
    spec.loader.exec_module(module)
    return module

# Cargar módulos core explícitamente
score = _load_core_module("score", "scoring")
report = _load_core_module("report", "reporting")
rice = _load_core_module("rice", "scoring")
orchestrator = _load_core_module("orchestrator", "utils")
merge_results = _load_core_module("merge_results", "utils")
selftest = _load_core_module("selftest", "utils")
contrast = _load_core_module("contrast", "reporting")