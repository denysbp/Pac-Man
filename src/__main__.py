from mlx.mlx import Mlx
from mazegenerator.mazegenerator import MazeGenerator
from random import randint
from src import Player


WIDTH = 900
HEIGHT = 800
SPEED = 15
H = 9
V = 3
class Bot:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.img = None
        self.img_width = None
        self.img_height = None
        self.moving = False

mobs = [
    (randint(HEIGHT - 300, WIDTH - 300), randint(HEIGHT - 300, WIDTH - 300)) for _ in range(40)
]



N, E, S, W = 1, 2, 4, 8

mlx = Mlx()

app = mlx.mlx_init()
window = mlx.mlx_new_window(app, WIDTH, HEIGHT, "teste")
bot = Bot()
img, w, h= mlx.mlx_png_file_to_image(app, "/home/denys/Documentos/42/pacman/src/models/assets/player_images/new/right-3.png")
player = Player(
    span_x= WIDTH // 2,
    span_y= HEIGHT // 2,
    image=img,
    width=w,
    height=h
)
def close(param):
    mlx.mlx_destroy_window(app, window)
    mlx.mlx_loop_exit(app)
    return 0
def key_press(keycode, param):
    return controls(keycode, param)

def frames(x, y):
    mlx.mlx_clear_window(app, window)
    for coord in mobs:
        row, col = coord
        mlx.mlx_string_put(app, window, col, row, 0xFFFFFF, ".")
    mlx.mlx_put_image_to_window(app, window, player.img, x, y)
    # draw_bbox(mlx, app, window, player, 0xFF0000)
    player.moving = False

def draw_bbox(mlx: Mlx, app, window, player: Player, color=0xFFFFFF):
    rect = player.rect
    left, right = rect.left, rect.right
    top, bottom = rect.top, rect.bottom

    # linhas horizontais (topo e base)
    for x in range(left, right + 1):
        mlx.mlx_string_put(app, window, x, top - H, color, "-")
        mlx.mlx_string_put(app, window, x, bottom - H, color, "-")

    # linhas verticais (esquerda e direita)
    for y in range(top, bottom + 1):
        mlx.mlx_string_put(app, window, left - V , y,  color, "|")
        mlx.mlx_string_put(app, window, right - V, y, color,  "|")

def colision(player):
    player = player.rect
    if (player.left + V) < 0 or (player.right - V) > WIDTH or (player.top - H) < 0 or (player.bottom - H) > HEIGHT:
        return True
    return False

def heat(player):
    rect = player.rect
    for i in range(len(mobs)):
        if isinstance(mobs[i], int):
            continue
        row, col = mobs[i]
        if rect.left + V <= col <= rect.right - V and rect.top - H <= row <= rect.bottom - H:
            mobs[i] = 0
    mobs[:] = [m for m in mobs if not isinstance(m, int)]
def update(img):
    player.img, player.img_width, player.img_height = mlx.mlx_png_file_to_image(app, img)


def controls(key, param):
    if key ==  0xff1b:
        mlx.mlx_destroy_window(app, window)
        mlx.mlx_loop_exit(app)

    if key == 65362:
        # up
        player.y -= SPEED
        if colision(param):
            player.y += SPEED
        heat(player)
        player.update_img("UP", mlx, app)
        frames(player.x, player.y)

    if key == 65361:
        # left
        player.x -= SPEED
        if colision(param):
            player.x += SPEED
        heat(player)
        player.update_img("LEFT", mlx, app)
        frames(player.x, player.y)
    if key == 65363:
        # right
        player.x += SPEED
        if colision(param):
            player.x -= SPEED
        heat(player)
        player.update_img("RIGHT", mlx, app)
        frames(player.x, player.y)

    if key == 65364:
        # down
        player.y += SPEED
        if colision(param):
            player.y -= SPEED
        heat(player)
        player.update_img("DOWN", mlx, app)
        frames(player.x, player.y)


    return 0
mlx.mlx_put_image_to_window(app, window, player.img, player.x, player.y)
for coord in mobs:
        row, col = coord
        mlx.mlx_string_put(app, window, col, row, 0xFFFFFF, ".")
# draw_bbox(mlx, app, window, player)
mlx.mlx_hook(window, 2, 1 << 0, key_press, player)
mlx.mlx_loop(app)
