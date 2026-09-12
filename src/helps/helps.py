from pathlib import Path
from PIL import Image

BASE_DIR = Path(__file__).parent
NEW_DIR = BASE_DIR / "new"

NEW_DIR.mkdir(exist_ok=True)

for i in range(1, 5):
    right = Image.open(BASE_DIR / f"right-{i}.png")
    left = Image.open(BASE_DIR / f"left-{i}.png")
    top = Image.open(BASE_DIR / f"top-{i}.png")
    down = Image.open(BASE_DIR / f"down-{i}.png")

    right = right.resize((52, 52), Image.Resampling.NEAREST)
    left = left.resize((52, 52), Image.Resampling.NEAREST)
    top = top.resize((52, 52), Image.Resampling.NEAREST)
    down = down.resize((52, 52), Image.Resampling.NEAREST)

    right.save(NEW_DIR / f"right-{i}.png")
    left.save(NEW_DIR / f"left-{i}.png")
    top.save(NEW_DIR / f"top-{i}.png")
    down.save(NEW_DIR / f"down-{i}.png")