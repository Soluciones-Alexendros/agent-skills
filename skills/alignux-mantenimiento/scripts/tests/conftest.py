"""conftest: añade scripts/ al sys.path para importar módulos."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
