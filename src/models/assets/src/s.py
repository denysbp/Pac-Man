from PIL import Image
import os

PACMAN_FOLDER = "src/models/assets/player_images/new"
GHOST_FOLDER = "src/models/assets/ghost_images"

reference_path = os.path.join(PACMAN_FOLDER, "right-1.png")
ref_img = Image.open(reference_path)
target_size = (ref_img.width, ref_img.height)
print(f"Tamanho de referência (Pac-Man): {target_size}")

ghost_files = ["blue.png", "dead.png", "orange.png",
               "pink.png", "powerup.png", "red.png"]

for filename in ghost_files:
    path = os.path.join(GHOST_FOLDER, filename)
    if not os.path.exists(path):
        print(f"Aviso: {path} não encontrado, a saltar")
        continue

    img = Image.open(path)
    resized = img.resize(target_size, Image.LANCZOS)
    resized.save(path)
    print(f"{path}: {img.width}x{img.height} -> {target_size[0]}x{target_size[1]}")