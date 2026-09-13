from mlx.mlx import Mlx
from mazegenerator.mazegenerator import MazeGenerator
from random import randint
from ..models import Player, Memory, Rect
from src import (
    colision,
    drawlineH,
    drawlineV,
    blit_into_buffer
)

# ESSA CLASSE NOS GERA A VISUALIZACAO, APENAS FAZ RUN
class Render:

    def __init__(self, w, h):
        self.OFFSET_X = 30
        self.OFFSET_Y = 50
        self.WIDTH = w
        self.HEIGHT = h
        self.maze_width = 0
        self.maze_height = 0
        self.map_width = 0
        self.map_height = 0
        self.color = 0xFF0000FF
        self.heated = []
        self.SPEED = 15
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
        self.player_colision = 0
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
            "/home/denys/Documentos/42/pacman/src/pacgum-small.png"
        )
        self.small_gun_memory: Memory = Memory()
        self.small_gun_memory.save(
            self.mlx.mlx_get_data_addr,
            self.small_gun
        )
        self.big_gum, self.b_w, self.b_h  = self.mlx.mlx_png_file_to_image(
            self.app,
            "/home/denys/Documentos/42/pacman/src/pacgum-big.png"
        )
        self.big_gum_memory: Memory = Memory()
        self.big_gum_memory.save(
            self.mlx.mlx_get_data_addr,
            self.big_gum
        )
        img, w, h= self.mlx.mlx_png_file_to_image(
            self.app,
            "/home/denys/Documentos/42/"
            "pacman/src/models/assets/player_images/new/right-3.png"
        )
        self.player: Player = Player(
            span_x= 0,
            span_y= 0,
            image=img,
            width=w,
            height=h,
            mlx_ptr=self.app,
            mlx=self.mlx
        )
        self.maze: MazeGenerator
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

    def start_level(self, width, height, seed):
        self.maze = MazeGenerator(
            (width, height),
            seed=seed
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
        self.cornes.extend(
            [
                (self.OFFSET_X, self.OFFSET_Y),
                (self.OFFSET_X + self.maze_width * self.CELL_W, self.OFFSET_Y),
                (self.OFFSET_X, self.OFFSET_Y + self.maze_height * self.CELL_H),
                (self.OFFSET_X + self.maze_width * self.CELL_W,
                self.OFFSET_Y + self.maze_height * self.CELL_H)
            ]
        )

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
            walls.append(Rect(x, y - thickness // 2, self.CELL_W, thickness))
        if cell & self.S:
            walls.append(Rect(x, y + self.CELL_H - thickness // 2, self.CELL_W, thickness))
        if cell & self.W:
            walls.append(Rect(x - thickness // 2, y, thickness, self.CELL_H))
        if cell & self.E:
            walls.append(Rect(x + self.CELL_W - thickness // 2, y, thickness, self.CELL_H))
        return walls

    def check_colision(self, dx, dy, position: str) -> bool:
        w = self.player.img_width
        h = self.player.img_height
        dest_rect = Rect(dx, dy, w, h)

        corners = [(dx, dy), (dx + w - 1, dy), (dx, dy + h - 1), (dx + w - 1, dy + h - 1)]
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
        self.mlx.mlx_destroy_window(self.app, self.window)
        self.mlx.mlx_loop_exit(self.app)
        return 0

    def key_press(self, keycode, param):
        return self.controls(keycode, param)

    def frames(self, x, y):
        self.mlx.mlx_clear_window(self.app, self.window)
        self.blip()
        self.mlx.mlx_put_image_to_window(self.app, self.window, self.player.img, x, y)



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

                # if self.is_walkable(cell):
                #     small_gum_x = x + (self.CELL_W - self.m_w) // 2
                #     small_gum_y = y + (self.CELL_H -self.m_h) // 2
                #     blit_into_buffer(
                #         self.memory.data,
                #         self.memory.bpp,
                #         self.memory.size_line,
                #         self.WIDTH,
                #         self.HEIGHT,
                #         self.small_gun_memory.data,
                #         self.small_gun_memory.bpp,
                #         self.small_gun_memory.size_line,
                #         self.m_w,
                #         self.m_h,
                #         small_gum_x,
                #         small_gum_y
                #     )
                # if self.is_walkable(cell) and cell & (self.N | self.W):
                #     small_gum_x = x + (self.CELL_W - self.m_w) // 2
                #     small_gum_y = y + (self.CELL_H -self.m_h) // 2

                #     if (small_gum_x, small_gum_y) in self.cornes:
                #         continue
                #     blit_into_buffer(
                #         self.memory.data,
                #         self.memory.bpp,
                #         self.memory.size_line,
                #         self.WIDTH,
                #         self.HEIGHT,
                #         self.big_gum_memory.data,
                #         self.big_gum_memory.bpp,
                #         self.big_gum_memory.size_line,
                #         self.b_w,
                #         self.b_h,
                #         self.OFFSET_X,
                #         self.OFFSET_Y
                #     )

    def render_loop(self, param):
        self.move(self.player)
        self.frames(self.player.x, self.player.y)
        return 0

    def reload_board(self, arg: Rect) -> None:
        for rect in arg:
            if self.player.hit_gum(rect):
                self.heated.append(rect.x)
                self.reload = True
        if self.reload:
            self.frames(self.player.x, self.player.y)
            self.draw_board()
            self.reload = False

    def move(self, param) -> None:
        if self.player._direction in "UP":
            dy = self.player.y - self.SPEED
            dx = self.player.x
            if self.check_colision(dx, dy, "UP"):
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
            if self.check_colision(dx, dy, "LEFT"):
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
            if self.check_colision(dx, dy, "RIGHT"):
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
            if self.check_colision(dx, dy, "DOWN"):
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
        self.player.update_img(self.player._direction, self.mlx, self.app)
        self.frames(self.player.x, self.player.y)

    def run(self):
        self.start_level(15, 15, 0)
        row, col = self.find_spawn_below_42()
        self.player.x = self.OFFSET_X + col * self.CELL_W + 25
        self.player.y = self.OFFSET_Y + row * self.CELL_H - 150
        self.draw_board()
        # self.mlx.mlx_loop_hook(self.app, self.reload_board, self.gum_position)
        self.mlx.mlx_hook(self.window, 2, 1 << 0, self.key_press, self.player)
        self.mlx.mlx_loop_hook(self.app, self.render_loop, None)
        self.mlx.mlx_loop(self.app)
