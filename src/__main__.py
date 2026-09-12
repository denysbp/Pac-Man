import mlx
from mazegenerator.mazegenerator import MazeGenerator
from random import randint


WIDTH = 900
HEIGHT = 800
SPEED = 10
class Bot:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.img = None
        self.img_w = None
        self.img_h = None
        self.moving = False





N, E, S, W = 1, 2, 4, 8

mlx = mlx.mlx.Mlx()

def close(param):
    mlx.mlx_destroy_window(app, window)
    mlx.mlx_loop_exit(app)
    return 0
def key_press(keycode, param):
    return controls(keycode, param)

def frames(x, y):
    mlx.mlx_clear_window(app, window)
    mlx.mlx_put_image_to_window(app, window, bot.img, x, y)
    bot.moving = False


def colision():
    left = bot.x
    right = bot.x + bot.img_w
    top = bot.y
    bottom = bot.y + bot.img_h

    if left < 0 or right > WIDTH or top < 0 or bottom > HEIGHT:
        print("HEIGHT: ", bot.y + bot.img_h)
        print("WIDTH: ", bot.x + bot.img_w)
        return True

    print("WIDTH: ", bot.x + bot.img_w)
    print("HEIGHT: ", bot.y + bot.img_h)
    return False

def update(img):
    bot.img, bot.img_w, bot.img_h = mlx.mlx_png_file_to_image(app, img)


def controls(key, param):

    if key ==  0xff1b:
        mlx.mlx_destroy_window(app, window)
        mlx.mlx_loop_exit(app)

    if key == 65362:
        # up
        bot.y -= SPEED
        if colision():
            bot.y += 5
        update("./pacman-up.png")
        frames(bot.x, bot.y)

    if key == 65361:
        # left
        bot.x -= SPEED
        if colision():
            bot.x += SPEED
        update("./pacman-left.png")
        frames(bot.x, bot.y)
    if key == 65363:
        # right
        bot.x += SPEED
        if colision():
            bot.x -= SPEED
        update("./pacman.png")
        frames(bot.x, bot.y)

    if key == 65364:
        # down
        bot.y += SPEED
        if colision():
            bot.y -= SPEED
        update("./pacman-down.png")
        frames(bot.x, bot.y)


    return 0
app = mlx.mlx_init()
window = mlx.mlx_new_window(app, WIDTH, HEIGHT, "teste")
bot = Bot()
update("./pacman.png")
mlx.mlx_put_image_to_window(app, window, bot.img, bot.x, bot.y)
mlx.mlx_hook(window, 2, 1 << 0, key_press, None)
mlx.mlx_hook(window, 17, 0, close, None)
mlx.mlx_loop(app)
