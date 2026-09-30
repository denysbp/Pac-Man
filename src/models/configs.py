from pathlib import Path


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
