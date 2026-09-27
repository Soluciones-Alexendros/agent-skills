#!/usr/bin/env python3
"""Entry script modo local: guía (sin servidor no hay ejecución) o scoring.

Uso:
    python3 modes/local/run.py --target http://localhost:5173
    python3 modes/local/run.py --checks flujo.json [--outdir output/]
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..",
                                "core", "utils"))

from orchestrator import main as orch_main  # noqa: E402

if __name__ == "__main__":
    sys.exit(orch_main(["--mode", "local", *sys.argv[1:]]))
