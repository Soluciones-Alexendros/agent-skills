#!/usr/bin/env python3
"""Entry script modo compliance: puntúa matriz compliance e informa.

Uso:
    python3 modes/compliance/run.py --checks resultados.json [--outdir output/] [--target URL]
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..",
                                "core", "utils"))

from orchestrator import main as orch_main  # noqa: E402

if __name__ == "__main__":
    sys.exit(orch_main(["--mode", "compliance", *sys.argv[1:]]))
