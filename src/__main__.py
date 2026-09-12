from mlx.mlx import Mlx
# from mazegenerator.mazegenerator import MazeGenerator
# from random import randint
# from src import Player
# from src import colision, drawlineH, drawlineV


WIDTH = 900
HEIGHT = 800
# SPEED = 15
# H = 9
# V = 3
# pacgum_positions = []
# class Bot:
#     def __init__(self):
#         self.x = WIDTH // 2
#         self.y = HEIGHT // 2
#         self.img = None
#         self.img_width = None
#         self.img_height = None
#         self.moving = False

# mobs = [
#     (randint(HEIGHT - 300, WIDTH - 300), randint(HEIGHT - 300, WIDTH - 300)) for _ in range(20)
# ]



# N, E, S, W = 1, 2, 4, 8

mlx = Mlx()
# maze = MazeGenerator((15, 15))
# maze.generate()
# OFFSET_X = 30
# OFFSET_Y = 50

# CELL_W = (WIDTH - 2 * OFFSET_X) // maze._width
# CELL_H = (HEIGHT - 2 * OFFSET_Y) // maze._height
# print(maze.maze)
# app = mlx.mlx_init()
# window = mlx.mlx_new_window(app, WIDTH, HEIGHT, "teste")
# bot = Bot()
# img, w, h= mlx.mlx_png_file_to_image(
#     app,
#     "/home/denys/Documentos/42/"
#     "pacman/src/models/assets/player_images/new/right-3.png"
# )

# mob, m_w, m_h  = mlx.mlx_png_file_to_image(app, "/home/denys/Documentos/42/pacman/src/pacgum-small.png")
# big, b_w, b_h  = mlx.mlx_png_file_to_image(app, "/home/denys/Documentos/42/pacman/src/pacgum-big.png")
# player = Player(
#     span_x= WIDTH // 2,
#     span_y= HEIGHT // 2,
#     image=img,
#     width=w,
#     height=h
# )

# def cell_position(row, col):
#     x = OFFSET_X + col * CELL_W
#     y = OFFSET_Y + row * CELL_H
#     return x, y

# def is_walkable(row, col):
#     cell = maze.maze[row][col]

#     return (
#         not (cell & N) or
#         not (cell & E) or
#         not (cell & S) or
#         not (cell & W)
#     )


# def draw_board():
#     num1 = ((maze._height - 50) // 32)
#     num2 = (maze._width // 30)
#     for i in range(len(maze.maze)):
#         for j in range(len(maze.maze[i])):
#             cell = maze.maze[i][j]
#             if is_walkable(i, j):
#                 x, y = cell_position(i, j)

#                 x += (CELL_W - m_w) // 2
#                 y += (CELL_H - m_h) // 2

#                 mlx.mlx_put_image_to_window(
#                     app,
#                     window,
#                     mob,
#                     x,
#                     y
#                 )
#             if cell == 2:
#                 x, y = cell_position(i, j)

#                 x += (CELL_W - b_w) // 2
#                 y += (CELL_H - b_h) // 2

#                 mlx.mlx_put_image_to_window(
#                     app,
#                     window,
#                     big,
#                     x,
#                     y
#                 )

#             if cell == (N | S):
#                 x, y = cell_position(i, j)

#                 x += CELL_W // 2
#                 drawlineV(
#                     x,
#                     y,
#                     x,
#                     y + CELL_H,
#                     mlx,
#                     app,
#                     window
#                 )
#             if cell == (N | S):
#                 # |
#                 pass
#             if cell == (E | W):
#                 # ─
#                 pass
#             if cell == (N | E):
#                 # canto
#                 pass
#             if cell == (S | E):
#                 # outro canto
#                 pass

# def close(param):
#     mlx.mlx_destroy_window(app, window)
#     mlx.mlx_loop_exit(app)
#     return 0

# def key_press(keycode, param):
#     return controls(keycode, param)

# def frames(x, y):
#     mlx.mlx_clear_window(app, window)
#     draw_board()
#     mlx.mlx_put_image_to_window(app, window, player.img, x, y)
#     # draw_bbox(mlx, app, window, player, 0xFF0000)
#     player.moving = False

# def draw_bbox(mlx: Mlx, app, window, player: Player, color=0xFFFFFF):
#     rect = player.rect
#     left, right = rect.left, rect.right
#     top, bottom = rect.top, rect.bottom

#     # linhas horizontais (topo e base)
#     for x in range(left, right + 1):
#         mlx.mlx_string_put(app, window, x, top - H, color, "-")
#         mlx.mlx_string_put(app, window, x, bottom - H, color, "-")

#     # linhas verticais (esquerda e direita)
#     for y in range(top, bottom + 1):
#         mlx.mlx_string_put(app, window, left - V , y,  color, "|")
#         mlx.mlx_string_put(app, window, right - V, y, color,  "|")

# def heat(player):
#     rect = player.rect
#     for i in range(len(mobs)):
#         if isinstance(mobs[i], int):
#             continue
#         row, col = mobs[i]
#         if rect.left - 5 <= col <= rect.right + 5 and rect.top - 5 <= row <= rect.bottom + 5:
#             mobs[i] = 0
#     mobs[:] = [m for m in mobs if not isinstance(m, int)]

# def controls(key, param):
#     if key ==  0xff1b:
#         mlx.mlx_destroy_window(app, window)
#         mlx.mlx_loop_exit(app)

#     if key == 65362:
#         # up
#         player.y -= SPEED
#         if colision(
#             param,
#             WIDTH,
#             HEIGHT,
#             V,
#             H
#         ):
#             player.y += SPEED
#         heat(player)
#         player.update_img("UP", mlx, app)
#         frames(player.x, player.y)

#     if key == 65361:
#         # left
#         player.x -= SPEED
#         if colision(
#             param,
#             WIDTH,
#             HEIGHT,
#             V,
#             H
#         ):
#             player.x += SPEED
#         heat(player)
#         player.update_img("LEFT", mlx, app)
#         frames(player.x, player.y)
#     if key == 65363:
#         # right
#         player.x += SPEED
#         if colision(
#             param,
#             WIDTH,
#             HEIGHT,
#             V,
#             H
#         ):
#             player.x -= SPEED
#         heat(player)
#         player.update_img("RIGHT", mlx, app)
#         frames(player.x, player.y)

#     if key == 65364:
#         # down
#         player.y += SPEED
#         if colision(
#             param,
#             WIDTH,
#             HEIGHT,
#             V,
#             H
#         ):
#             player.y -= SPEED
#         heat(player)
#         player.update_img("DOWN", mlx, app)
#         frames(player.x, player.y)


#     return 0
# mlx.mlx_put_image_to_window(app, window, player.img, player.x, player.y)
# # draw_board()
# for x in range(100, 200):
#     mlx.mlx_pixel_put(app, window, x, 100, 0xFFFFFF)
# # draw_bbox(mlx, app, window, player)
# mlx.mlx_hook(window, 2, 1 << 0, key_press, player)
# mlx.mlx_loop(app)

app = mlx.mlx_init()

window = mlx.mlx_new_window(
    app,
    WIDTH,
    HEIGHT,
    "teste"
)

for y in range(100, 200):
    for x in range(100, 200):
        ret = mlx.mlx_pixel_put(
            app,
            window,
            x,
            y,
            0xFFFFFF
        )

print("último ret:", ret)

mlx.mlx_loop(app)