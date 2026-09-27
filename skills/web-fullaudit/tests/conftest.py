"""Fixtures compartidos: core/* en sys.path (sin importar selftest)."""
import os
import sys

ROOT = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, os.path.join(ROOT, "core", "scoring"))
sys.path.insert(0, os.path.join(ROOT, "core", "reporting"))
sys.path.insert(0, os.path.join(ROOT, "core", "utils"))
