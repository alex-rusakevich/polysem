import os
import sys
from pathlib import Path

RESOURCE_PATH = Path(getattr(sys, "_MEIPASS", os.path.abspath(".")))

with open(
    os.path.join(RESOURCE_PATH, "data", "theword.txt"), "r", encoding="utf-8"
) as f:
    THE_WORD = f.read().strip()
