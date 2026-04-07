from pathlib import Path
import sys
from importlib import import_module

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

run = import_module("src.exercises.ex1").run


if __name__ == "__main__":
    run()