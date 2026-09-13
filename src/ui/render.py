from mlx.mlx import Mlx
from mazegenerator.mazegenerator import MazeGenerator
from random import randint
from ..models import Player, Memory
from src import (
    colision,
    drawlineH,
    drawlineV,
    blit_into_buffer
)

# ESSA CLASSE NOS GERA A VISUALIZACAO, APENAS FAZ RUN
class Render:

    def __init__(self):
        self.OFFSET_X = 30
        self.OFFSET_Y = 50
        self.WIDTH = 1200
        self.HEIGHT = 1000
        self.maze_width = 0
        self.maze_height = 0
        self.color = 0xFF0000FF
        self.SPEED = 15
        self.H = 9
        self.V = 3
        self.N = 1
        self.E = 2
        self.S = 4
        self.W = 8
        self.CELL_W: int
        self.CELL_H: int
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
            span_x= round((self.WIDTH // 2) * 1.20),
            span_y= round((self.HEIGHT // 2) * 0.83),
            image=img,
            width=w,
            height=h,
            mlx_ptr=self.app,
            mlx=self.mlx
        )
        self.maze: MazeGenerator

    def start_level(self, width, height, seed):
        self.maze = MazeGenerator(
            (width, height),
            seed=seed
        )
        self.maze.generate()
        print(self.maze.maze)
        self.maze_height = height
        self.maze_width = width
        self.CELL_W = (self.WIDTH - 2 * self.OFFSET_X) // self.maze_width
        self.CELL_H = (self.HEIGHT - 2 * self.OFFSET_Y) // self.maze_height

    def cell_position(self, row, col):
        x = self.OFFSET_X + col * self.CELL_W
        y = self.OFFSET_Y + row * self.CELL_H
        return x, y

    def is_walkable(self, cell):

        return (
            not (cell & self.N) or
            not (cell & self.E) or
            not (cell & self.S) or
            not (cell & self.W)
        )

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

        if key == 65362:
            # up
            self.player.y -= self.SPEED
            if colision(
                param,
                self.WIDTH,
                self.HEIGHT,
                self.V,
                self.H
            ):
                self.player.y += self.SPEED
            self.player.update_img("UP", self.mlx, self.app)
            self.frames(self.player.x, self.player.y)

        if key == 65361:
            # left
            self.player.x -= self.SPEED
            if colision(
                param,
                self.WIDTH,
                self.HEIGHT,
                self.V,
                self.H
            ):
                self.player.x += self.SPEED
            self.player.update_img("LEFT", self.mlx, self.app)
            self.frames(self.player.x, self.player.y)
        if key == 65363:
            # right
            self.player.x += self.SPEED
            if colision(
                param,
                self.WIDTH,
                self.HEIGHT,
                self.V,
                self.H
            ):
               self.player.x -= self.SPEED
            self.player.update_img("RIGHT", self.mlx, self.app)
            self.frames(self.player.x, self.player.y)

        if key == 65364:
            # down
            self.player.y += self.SPEED
            if colision(
                param,
                self.WIDTH,
                self.HEIGHT,
                self.V,
                self.H
            ):
                self.player.y -= self.SPEED
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

    def render_loop(self, param):
        self.frames(self.player.x, self.player.y)
        return 0

    def run(self):
        self.start_level(15, 15, 0)
        self.draw_board()
        self.mlx.mlx_loop_hook(self.app, self.render_loop, None)
        self.mlx.mlx_hook(self.window, 2, 1 << 0, self.key_press, self.player)
        self.mlx.mlx_loop(self.app)
