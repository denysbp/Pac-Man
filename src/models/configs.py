from pathlib import Path
import sys

if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
    BASE_DIR = Path(sys._MEIPASS) / "src" / "models"
else:
    BASE_DIR = Path(__file__).parent

BASE_DIR = Path(__file__).parent
NEW_DIR = BASE_DIR / "assets" / "player"


RIGHT = []
TOP = []
LEFT = []
DOWN = []

for i in range(1, 5):
    RIGHT.append(NEW_DIR / f"right-{i}.png")
    LEFT.append(NEW_DIR / f"left-{i}.png")
    TOP.append(NEW_DIR / f"top-{i}.png")
    DOWN.append(NEW_DIR / f"down-{i}.png")
