from mlx.mlx import Mlx
from mazegenerator.mazegenerator import MazeGenerator
from random import randint
import ctypes
from ..models import Player, Memory, Rect, Level, ConfigData
from time import sleep
from src import (
    colision,
    drawlineH,
    drawlineV,
    blit_into_buffer
)



# ESSA CLASSE NOS GERA A VISUALIZACAO, APENAS FAZ RUN
class Render:

    def __init__(
        self,
        w,
        h,
        levels,
        data
    ):
        self.OFFSET_X = 30
        self.OFFSET_Y = 50
        self.WIDTH = w
        self.HEIGHT = h
        self.maze_width = 0
        self.data: ConfigData = data
        self.levels: list[Level] = levels
        self.index: int = 0
        self.points = -10
        self.maze_height = 0
        self.map_width = 0
        self.map_height = 0
        self.color = 0xFF0000FF
        self.heated_small = []
        self.heated_big = []
        self.reload = False
        self.start = True
        self.coodown = 200
        self.victory = False
        self.SPEED = 20
        self.H = 2
        self.V = 1
        self.N = 1
        self.E = 2
        self.S = 4
        self.W = 8
        self.CELL_W: int
        self.CELL_H: int
        self.gum_position: list[(int, int)] = []
        self.mlx = Mlx()
        self.app = self.mlx.mlx_init()
        self.window = self.mlx.mlx_new_window(
            self.app,
            self.WIDTH,
            self.HEIGHT,
            "PAC Man"
        )
        self.buffer = self.mlx.mlx_new_image(
            self.app,
            self.WIDTH,
            self.HEIGHT
        )
        self.memory: Memory = Memory()
        self.memory.save(
            self.mlx.mlx_get_data_addr,
            self.buffer
        )
        self.small_gun, self.m_w, self.m_h  = self.mlx.mlx_png_file_to_image(
            self.app,
            "src/models/assets/gums/pacgum-small.png"
        )
        self.small_gun_memory: Memory = Memory()
        self.small_gun_memory.save(
            self.mlx.mlx_get_data_addr,
            self.small_gun
        )
        self.big_gum, self.b_w, self.b_h  = self.mlx.mlx_png_file_to_image(
            self.app,
            "src/models/assets/gums/pacgum-big.png"
        )
        self.big_gum_memory: Memory = Memory()
        self.big_gum_memory.save(
            self.mlx.mlx_get_data_addr,
            self.big_gum
        )
        img, w, h= self.mlx.mlx_png_file_to_image(
            self.app,
            "src/models/assets/player/right-3.png"
        )
        self.player: Player = Player(
            span_x= 0,
            span_y= 0,
            image=img,
            width=w,
            height=h,
            mlx_ptr=self.app,
            mlx=self.mlx,
            lives=self.data.lives
        )
        self.maze: MazeGenerator
        self.start_img, _, _ = self.mlx.mlx_png_file_to_image(
            self.app,
            "src/ui/start-game.png"
        )
        self.img_controls, _, _ = self.mlx.mlx_png_file_to_image(
            self.app,
            "src/ui/controls.png"
        )
        self.victory_img, _, _ = self.mlx.mlx_png_file_to_image(
            self.app,
            "src/ui/victory.png"
        )
        self.cornes: list = []

    def find_spawn_below_42(self):
        rows_with_42 = [i for i, row in enumerate(self.maze.maze) if 15 in row]
        last_row = max(rows_with_42)

        cols_with_42 = set()
        for i in rows_with_42:
            for j, val in enumerate(self.maze.maze[i]):
                if val == 15:
                    cols_with_42.add(j)

        min_col = min(cols_with_42)
        max_col = max(cols_with_42)
        spawn_col = (min_col + max_col) // 2
        spawn_row = last_row + 1
        return spawn_row, spawn_col

    def clear_buffer(self):
        self.memory.data[:] = b'\x00' * len(self.memory.data)


    def start_level(self):
        level = self.levels[self.index % len(self.levels)]
        width, height = level.width, level.height
        if self.data.seed is None:
            self.data.seed = 0
        self.maze = MazeGenerator(
            (width, height),
            seed=self.data.seed
        )
        self.maze.generate()
        self.maze_height = height
        self.maze_width = width
        self.CELL_W = (self.WIDTH - 2 * self.OFFSET_X) // self.maze_width
        self.CELL_H = (self.HEIGHT - 2 * self.OFFSET_Y) // self.maze_height
        self.CELL_W = (self.CELL_W // self.SPEED) * self.SPEED
        self.CELL_H = (self.CELL_H // self.SPEED) * self.SPEED
        self.map_height = self.CELL_H * self.maze_height
        self.map_width = self.CELL_W * self.maze_width
        self.heated_small.clear()
        self.heated_big.clear()
        margin_x = round(self.CELL_W * 0.5)
        margin_y = round(self.CELL_H * 0.5)
        self.cornes.extend(
            [
                (
                    self.OFFSET_X  + margin_x,
                    self.OFFSET_Y + margin_y),
                (
                    self.OFFSET_X + self.maze_width * self.CELL_W - margin_x,
                    self.OFFSET_Y + margin_y
                ),
                (
                    self.OFFSET_X + margin_x,
                    self.OFFSET_Y + self.maze_height * self.CELL_H - margin_y
                ),
                (
                    self.OFFSET_X + self.maze_width * self.CELL_W - margin_x,
                    self.OFFSET_Y + self.maze_height * self.CELL_H - margin_y
                )
            ]
        )
        self.gum_position.extend(self.cornes)

        for i in range(len(self.maze.maze)):
            for j in range(len(self.maze.maze[i])):
                x, y = self.cell_position(i, j)
                cell = self.maze.maze[i][j]
                if self.is_walkable(cell):
                    small_gum_x = x + (self.CELL_W - self.m_w) // 2
                    small_gum_y = y + (self.CELL_H -self.m_h) // 2
                    self.gum_position.append(
                        (small_gum_y, small_gum_x)
                    )
        row, col = self.find_spawn_below_42()
        self.player.x = self.OFFSET_X + col * self.CELL_W + 25
        self.player.y = self.OFFSET_Y + row * self.CELL_H - 150

    def cell_position(self, row, col):
        x = self.OFFSET_X + col * self.CELL_W
        y = self.OFFSET_Y + row * self.CELL_H
        return x, y

    def is_walkable(self, cell: int):

        return (
            not (cell & self.N) or
            not (cell & self.E) or
            not (cell & self.S) or
            not (cell & self.W)
        )

    def get_wall_rects(self, row, col):
        if not (0 <= row < self.maze_height and 0 <= col < self.maze_width):
            return []
        x, y = self.cell_position(row, col)
        cell = self.maze.maze[row][col]
        thickness = 4
        walls = []
        if cell & self.N:
            walls.append(
                Rect(x, y - thickness // 2, self.CELL_W, thickness)
            )
        if cell & self.S:
            walls.append(
                Rect(x, y + self.CELL_H - thickness // 2,
                    self.CELL_W, thickness)
            )
        if cell & self.W:
            walls.append(
                Rect(x - thickness // 2, y, thickness, self.CELL_H)
            )
        if cell & self.E:
            walls.append(
                Rect(x + self.CELL_W - thickness // 2,
                    y, thickness, self.CELL_H)
            )
        return walls

    def check_colision(self, dx, dy) -> bool:
        w = self.player.img_width
        h = self.player.img_height
        dest_rect = Rect(dx, dy, w, h)

        corners = [
            (dx, dy),
            (dx + w - 1, dy),
            (dx, dy + h - 1),
            (dx + w - 1, dy + h - 1)
        ]
        cells = set()
        for cx, cy in corners:
            col = (cx - self.OFFSET_X) // self.CELL_W
            row = (cy - self.OFFSET_Y) // self.CELL_H
            cells.add((row, col))

        for row, col in cells:
            for wall in self.get_wall_rects(row, col):
                if dest_rect.colliderect(wall):
                    return False
        return True

    def blip(self):
        self.mlx.mlx_put_image_to_window(
            self.app,
            self.window,
            self.buffer,
            0,
            0
        )

    def close(self, param):
        self.mlx.mlx_do_key_autorepeaton(self.app)
        self.mlx.mlx_destroy_window(self.app, self.window)
        self.mlx.mlx_loop_exit(self.app)
        return 0

    def key_press(self, keycode, param):
        if self.victory:
            return
        return self.controls(keycode, param)

    def  frames(self, x, y):
        self.mlx.mlx_clear_window(self.app, self.window)
        if self.reload:
            self.clear_buffer()
            self.draw_board()
            self.reload = False

        self.blip()
        self.draw_information()
        self.mlx.mlx_put_image_to_window(self.app, self.window, self.player.img, x, y)
        if len(self.heated_big + self.heated_small) == len(self.gum_position):
            self.coodown = 200
            self.victory = True
            self.gum_position.clear()
    def controls(self, key, param):
        if key ==  0xff1b:
            self.close(param)

        if key in (65362, 119):
            # up
            self.player.update_img("UP", self.mlx, self.app)
            self.frames(self.player.x, self.player.y)

        if key in (65361, 97):
            # left
            self.player.update_img("LEFT", self.mlx, self.app)
            self.frames(self.player.x, self.player.y)
        if key in (65363, 100):
            # right
            self.player.update_img("RIGHT", self.mlx, self.app)
            self.frames(self.player.x, self.player.y)

        if key in (65364,115):
            # down
            self.player.update_img("DOWN", self.mlx, self.app)
            self.frames(self.player.x, self.player.y)

        return 0

    def draw_board(self):
        for i in range(len(self.maze.maze)):
            for j in range(len(self.maze.maze[i])):
                cell = self.maze.maze[i][j]

                x, y = self.cell_position(i, j)
                if cell & self.N:
                    drawlineH(
                        self.memory.data,
                        self.memory.bpp,
                        self.memory.size_line,
                        x,
                        y,
                        x + self.CELL_W,
                        y,
                        self.color
                    )
                if cell & self.S:
                    drawlineH(
                        self.memory.data,
                        self.memory.bpp,
                        self.memory.size_line,
                        x,
                        y + self.CELL_H,
                        x + self.CELL_W,
                        y + self.CELL_H,
                        self.color
                    )
                if cell & self.W:
                    drawlineV(
                        self.memory.data,
                        self.memory.bpp,
                        self.memory.size_line,
                        x,
                        y,
                        x,
                        y + self.CELL_H,
                        self.color)
                if cell & self.E:
                    drawlineV(
                        self.memory.data,
                        self.memory.bpp,
                        self.memory.size_line,
                        x + self.CELL_W,
                        y,
                        x + self.CELL_W,
                        y + self.CELL_H,
                        self.color)

                if self.is_walkable(cell):
                    small_gum_x = x + (self.CELL_W - self.m_w) // 2
                    small_gum_y = y + (self.CELL_H -self.m_h) // 2
                    if (small_gum_y, small_gum_x) in self.heated_small:
                       continue
                    blit_into_buffer(
                        self.memory.data,
                        self.memory.bpp,
                        self.memory.size_line,
                        self.WIDTH,
                        self.HEIGHT,
                        self.small_gun_memory.data,
                        self.small_gun_memory.bpp,
                        self.small_gun_memory.size_line,
                        self.m_w,
                        self.m_h,
                        small_gum_x,
                        small_gum_y
                    )
        for x, y in self.cornes:
            if (x, y) in self.heated_big:
                continue
            blit_into_buffer(
                self.memory.data,
                self.memory.bpp,
                self.memory.size_line,
                self.WIDTH,
                self.HEIGHT,
                self.big_gum_memory.data,
                self.big_gum_memory.bpp,
                self.big_gum_memory.size_line,
                self.b_w,
                self.b_h,
                x - self.b_w // 2,
                y - self.b_h // 2
            )

    def render_loop(self, param):
        if self.victory:
            self.coodown -= 1

            if self.coodown <= 0:
                self.victory = False
                self.coodown = 200
                self.start_level()
                self.draw_board()
            else:
                self.level_win()

        else:
            self.move(self.player)

            self.frames(
                self.player.x,
                self.player.y
            )

        return 0

    def level_win(self):
        self.mlx.mlx_put_image_to_window(
            self.app,
            self.window,
            self.victory_img,
            round((self.WIDTH // 2) * 0.50),
            round((self.HEIGHT // 2) * 0.95)
        )

    def move(self, param) -> None:
        if self.player._direction in "UP":
            dy = self.player.y - self.SPEED
            dx = self.player.x
            if self.check_colision(dx, dy):
                self.player.y -= self.SPEED
            if colision(
                param,
                self.OFFSET_X,
                self.OFFSET_X + self.map_width,
                self.OFFSET_Y,
                self.OFFSET_Y + self.map_height,
                self.V,
                self.H
            ):
                self.player.y += self.SPEED

        if self.player._direction in "LEFT":
            dy = self.player.y
            dx = self.player.x - self.SPEED
            if self.check_colision(dx, dy):
                self.player.x -= self.SPEED
            if colision(
                param,
                self.OFFSET_X,
                self.OFFSET_X + self.map_width,
                self.OFFSET_Y,
                self.OFFSET_Y + self.map_height,
                self.V,
                self.H
            ):
                self.player.x += self.SPEED

        if self.player._direction in "RIGHT":
            dy = self.player.y
            dx = self.player.x + self.SPEED
            if self.check_colision(dx, dy):
                self.player.x += self.SPEED
            if colision(
                param,
                self.OFFSET_X,
                self.OFFSET_X + self.map_width,
                self.OFFSET_Y,
                self.OFFSET_Y + self.map_height,
                self.V,
                self.H
            ):
                self.player.x -= self.SPEED
        if self.player._direction in "DOWN":
            dy = self.player.y + self.SPEED
            dx = self.player.x
            if self.check_colision(dx, dy):
                self.player.y += self.SPEED
            if colision(
                param,
                self.OFFSET_X,
                self.OFFSET_X + self.map_width,
                self.OFFSET_Y,
                self.OFFSET_Y + self.map_height,
                self.V,
                self.H
            ):
                self.player.y -= self.SPEED
        gum = self.player.hit_gum(
            self.gum_position,
            self.OFFSET_X,
            self.OFFSET_Y,
            self.CELL_W,
            self.CELL_H,
            self.m_w,
            self.m_h,
        )

        big = None

        player_rect = Rect(
            self.player.x,
            self.player.y,
            self.player.img_width,
            self.player.img_height
        )

        for x, y in self.cornes:
            big_rect = Rect(
                x - self.b_w // 2,
                y - self.b_h // 2,
                self.b_w,
                self.b_h
            )

            if player_rect.colliderect(big_rect):
                big = (x, y)
                break

        if gum is not None and gum not in self.heated_small:
            self.heated_small.append(gum)
            self.points += self.data.points_per_pacgum
            self.reload = True

        if big is not None and big not in self.heated_big:
            self.heated_big.append(big)
            self.points -= self.data.points_per_pacgum
            self.points += self.data.points_per_super_pacgum
            self.reload = True

        self.player.update_img(self.player._direction, self.mlx, self.app)
        self.frames(self.player.x, self.player.y)

    def draw_information(self) -> None:
        margin_x = round(self.WIDTH * 0.02)
        margin_y = round(self.HEIGHT * 0.85)
        self.mlx.mlx_string_put(
            self.app,
            self.window,
            margin_x,
            margin_y + 50,
            150,
            "Points: " + str(self.points)
        )
        if self.data.lives <= 32:
            for i in range(0, self.data.lives):
                self.mlx.mlx_put_image_to_window(
                    self.app,
                    self.window,
                    self.player.static,
                    (margin_x + 150) + (i * 50),
                    margin_y + 40
                )
        else:
            self.mlx.mlx_string_put(
                self.app,
                self.window,
                margin_x,
                margin_y + 10,
                150,
                "Lives: " + str(self.data.lives)
            )

    def mouse_handler(self, mouse_code: int, x: int, y: int, param):
        pass

    def start_game(self, keycode, param):
        if keycode == 32:
            self.start = False
            self.mlx.mlx_loop_exit(self.app)

        if keycode ==  0xff1b:
            self.mlx.mlx_destroy_window(self.app, self.window)
            self.mlx.mlx_loop_exit(self.app)

    def run(self):
        if self.start:
            self.mlx.mlx_put_image_to_window(
                self.app,
                self.window,
                self.start_img,
                round((self.WIDTH // 2) * 0.45),
                0
            )
            self.mlx.mlx_put_image_to_window(
                self.app,
                self.window,
                self.img_controls,
                round((self.WIDTH // 2) * 0.03),
                round((self.HEIGHT // 2) * 1.10)
            )
            self.mlx.mlx_hook(self.window, 2, 1 << 0, self.start_game, None)
            self.mlx.mlx_loop(self.app)

        if not self.start:
            self.start_level()
            self.draw_board()
            self.mlx.mlx_do_key_autorepeatoff(self.app)
            self.mlx.mlx_mouse_move
            self.mlx.mlx_hook(self.window, 2, 1 << 0, self.key_press, self.player)
            self.mlx.mlx_hook(self.window, 17, 1 << 0, self.close, "None")
            self.mlx.mlx_loop_hook(self.app, self.render_loop, None)
            self.mlx.mlx_loop(self.app)
