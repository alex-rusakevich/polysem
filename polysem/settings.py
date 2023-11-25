import os
import sys
from pathlib import Path

RESOURCE_PATH = Path(getattr(sys, "_MEIPASS", os.path.abspath(".")))
THE_WORD = "теплый"
