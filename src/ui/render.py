from mlx.mlx import Mlx
from mazegenerator.mazegenerator import MazeGenerator
from random import randint, choice
from ..models import Player, Memory, Rect, Level, ConfigData, Bot
from ..data_base import DATA_BASE
from typing import Any
import time
from src import (
    colision,
    drawlineH,
    drawlineV,
    blit_into_buffer,
    put_pixel,
)

keyboard: dict[int, str] = {
    65509: "capslock!",
    97: "a",
    98: "b",
    99: "c",
    100: "d",
    101: "e",
    102: "f",
    103: "g",
    104: "h",
    105: "i",
    106: "j",
    107: "k",
    108: "l",
    109: "m",
    110: "n",
    111: "o",
    112: "p",
    113: "q",
    114: "r",
    115: "s",
    116: "t",
    117: "u",
    118: "v",
    119: "w",
    120: "x",
    121: "y",
    122: "z",
    32: " "
}


class Render:

    def __init__(
        self,
        w: int,
        h: int,
        levels: list[Level],
        data: ConfigData,
        name: str
    ) -> None:
        self.data: ConfigData = data
        self.set_global_positions_sizes(w, h)
        self.path_img = name
        self.mlx = Mlx()
        self.db = DATA_BASE(self.data.highscore_filename)
        self.db.create_table()
        self.scores = self.db.get_scores()
        self.app = self.mlx.mlx_init()
        self.levels: list[Level] = levels
        self.set_images()
        self.create_classes_and_classes_atributes()

    def set_global_positions_sizes(self, w: int, h: int) -> None:
        self.H = 2
        self.V = 1
        self.N = 1
        self.E = 2
        self.S = 4
        self.W = 8
        self.CELL_W: int
        self.CELL_H: int
        self.OFFSET_X = 30
        self.OFFSET_Y = 50
        self.HUD_HEIGHT = 120
        self.WIDTH = w
        self.HEIGHT = h
        self.cell_len = 0
        self.maze_width = 0
        self.maze_height = 0
        self.map_width = 0
        self.map_height = 0
        self.cornes: list = []
        self.index: int = 0
        self.points = self.data.points_per_pacgum
        self.coodown = 200
        self.color = 0xFF0000FF
        self.victory = False
        self.reload = False
        self.start = True
        self.gameover = False
        self.capslock = False
        self.menu: list[tuple] = []
        self.pause_imgs: list[tuple] = []
        self.enter_imgs: list[tuple] = []
        self.eaten_popups: list[tuple[int, int, float]] = []
        self.power_imgs: dict[str, tuple] = {}
        self.enter_deadline: float | int = 0
        self.pause_index: int = 0
        self.img_index: int = 0
        self.new_game_input: bool = False
        self.high_scores_input: bool = False
        self.show_controls_input: bool = False
        self.show_modes: bool = False
        self.gamewin: bool = False
        self.PAUSE: bool = False
        self.quit = False
        self.end_until: float = 0
        self.exit: bool = False
        self.initial_lives = self.data.lives

    def set_images(self) -> None:
        menu_imgs = [
            "new-game",
            "scores",
            "controls",
            "exit"
        ]
        self.window = self.mlx.mlx_new_window(
            self.app,
            self.WIDTH,
            self.HEIGHT,
            "PAC Man"
        )
        self.small_gun, self.m_w, self.m_h = self.mlx.mlx_png_file_to_image(
            self.app,
            "src/models/assets/gums/pacgum-small.png")
        self.player_img, self.pl_w, self.pl_h = self.mlx.mlx_png_file_to_image(
            self.app,
            "src/models/assets/player/right-3.png"
        )
        self.img_controls, self.c_w, _ = self.mlx.mlx_png_file_to_image(
            self.app,
            "src/ui/menu/keys.png")
        self.victory_img, self.v_w, _ = self.mlx.mlx_png_file_to_image(
            self.app,
            "src/ui/menu/victory.png")
        self.big_gum, self.b_w, self.b_h = self.mlx.mlx_png_file_to_image(
            self.app,
            "src/models/assets/gums/pacgum-big.png")
        self.buffer = self.mlx.mlx_new_image(
            self.app,
            self.WIDTH,
            self.HEIGHT)
        self.gameover_img, self.over_w, _ = self.mlx.mlx_png_file_to_image(
            self.app,
            "src/ui/menu/gameover.png"
        )
        self.names_img, self.n_w, _ = self.mlx.mlx_png_file_to_image(
            self.app,
            "src/ui/menu/names.png"
        )

        self.win_img, self.win_w, self.win_h = self.mlx.mlx_png_file_to_image(
            self.app,
            "src/ui/menu/gamewin.png"
        )
        self.enter_imgs.append(self.mlx.mlx_png_file_to_image(
            self.app,
            "src/ui/menu/enter-00.png"
        ))
        self.enter_imgs.append(self.mlx.mlx_png_file_to_image(
            self.app,
            "src/ui/menu/enter-01.png"
        ))

        self.pause_imgs.append(
            self.mlx.mlx_png_file_to_image(
                self.app,
                "src/ui/menu/main-menu.png"
            )
        )
        self.pause_imgs.append(
            self.mlx.mlx_png_file_to_image(
                self.app,
                "src/ui/menu/resume.png"
            )
        )

        self.spam, self.spam_w, self.spam_h = self.mlx.mlx_png_file_to_image(
            self.app,
            self.path_img
        )

        for name in (
            "freeze_bots",
            "intangibility",
            "invincibility",
            "level_plus1",
            "lives_plus1",
            "speed"
        ):
            self.power_imgs[name] = self.mlx.mlx_png_file_to_image(
                self.app,
                f"src/ui/power/{name}.png"
            )

        for img in menu_imgs:
            information = self.mlx.mlx_png_file_to_image(
                self.app,
                f"src/ui/menu/{img}.png"
            )
            self.menu.append(
                information
            )

    def get_image(self) -> tuple[Any | None, int, int]:
        return self.menu[self.img_index % len(self.menu)]

    def get_pause_image(self) -> tuple[Any | None, int, int]:
        return self.pause_imgs[self.pause_index % len(self.pause_imgs)]

    def get_enter_image(self) -> tuple[Any | None, int, int]:
        self.enter_index += 1
        return self.enter_imgs[self.enter_index % len(self.enter_imgs)]

    def create_classes_and_classes_atributes(self) -> None:
        self.player: Player = Player(
            span_x=0,
            span_y=0,
            image=self.player_img,
            width=self.pl_w,
            height=self.pl_h,
            mlx_ptr=self.app,
            mlx=self.mlx,
            lives=self.data.lives)
        self.player_sheat: dict = {
            "intangibility": False,
            "invincibility": False,
            "freeze_bots": False
        }
        self.PLAYER_SPEED = 10
        self.super_pac_deadline: float | int = 0
        self.time_super_pac = 8
        self.TIME: int = self.data.level_max_time
        self.PAUSED_TIME: float | int = 0
        self.INPUT: bool = False
        self.level_deadline = time.monotonic() + self.TIME
        self.super_pac = False
        self.name_player = ""
        self.name_already_set = False
        self.POWER: bool = False
        self.EATED: bool = False
        self.location_x = 0
        self.location_y = 0
        self.power_deadline: float | int = 0
        self.player_deadline: float | int = 0
        self.spam_deadline = 0
        self.current_power: tuple = ()
        self.power_index = 0
        self.pacgums: int = 0
        self.enter_index = 0

        self.bots: list[Bot] = []
        for i in range(4):
            self.bots.append(
                Bot(
                    spam_x=0,
                    spam_y=0,
                    mlx_ptr=self.app,
                    mlx=self.mlx,
                    maze=[],
                    bot_id=i,
                    pixel_data={}
                )
            )
        self.BOT_SPEED = 8

        self.memory: Memory = Memory()
        self.memory.save(
            self.mlx.mlx_get_data_addr,
            self.buffer
        )

        self.gum_position: list[tuple[int, int]] = []
        self.heated_small: list[tuple] = []
        self.small_gun_memory: Memory = Memory()
        self.small_gun_memory.save(
            self.mlx.mlx_get_data_addr,
            self.small_gun
        )

        self.heated_big: list[tuple] = []
        self.big_gum_memory: Memory = Memory()
        self.big_gum_memory.save(
            self.mlx.mlx_get_data_addr,
            self.big_gum
        )
        if self.data.seed is None:
            self.data.seed = 0

    def find_spawn_below_42(self) -> tuple[int, int]:
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

    def clear_buffer(self) -> None:
        self.memory.data[:] = b'\x00' * len(self.memory.data)

    def calcule_maze_dimetions(self, height: int, width: int) -> None:
        self.cornes.clear()
        self.gum_position.clear()
        self.maze_height = height
        self.maze_width = width
        self.CELL_W = (self.WIDTH - 2 * self.OFFSET_X) // self.maze_width
        self.CELL_H = (
            self.HEIGHT - self.OFFSET_Y - self.HUD_HEIGHT) // self.maze_height
        self.map_height = self.CELL_H * self.maze_height
        self.map_width = self.CELL_W * self.maze_width
        margin_x = round(self.CELL_W * 0.5)
        margin_y = round(self.CELL_H * 0.5)
        self.cornes.extend(
            [
                (
                    self.OFFSET_X + margin_x,
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
        for i in range(len(self.maze.maze)):
            for j in range(len(self.maze.maze[i])):
                x, y = self.cell_position(i, j)
                cell = self.maze.maze[i][j]
                if self.is_walkable(cell):
                    small_gum_x = x + (self.CELL_W - self.m_w) // 2
                    small_gum_y = y + (self.CELL_H - self.m_h) // 2
                    self.gum_position.append(
                        (small_gum_y, small_gum_x)
                    )

        temp: list[tuple] = []
        while len(temp) < self.data.pacgum:
            gum = choice(self.gum_position)
            self.gum_position.remove(gum)
            temp.append(gum)
        self.gum_position = temp
        self.gum_position.extend(self.cornes)
        row, col = self.find_spawn_below_42()
        self.player.x = self.OFFSET_X + col * self.CELL_W + 25
        self.player.y = self.OFFSET_Y + row * self.CELL_H - 150

    def start_level(self, next_level: bool = True) -> None:
        if next_level:
            if self.index == len(self.levels):
                self.gamewin = True
                return
            self.clear_buffer()
            self.level_deadline = time.monotonic() + self.TIME
            self.index += 1
            level = self.levels[self.index % len(self.levels)]
            width, height = level.width, level.height
            self.maze = MazeGenerator(
                (width, height),
                seed=self.data.seed
            )

            self.heated_small.clear()
            self.heated_big.clear()
            self.maze.generate()
            self.pacgums = 0
            self.calcule_maze_dimetions(self.maze._height, self.maze._width)
            pixel_data = {
                "SPEED": self.BOT_SPEED,
                "OFFSET_X": self.OFFSET_X,
                "OFFSET_Y": self.OFFSET_Y,
                "CELL_W": self.CELL_W,
                "CELL_H": self.CELL_H
            }
            for i in range(4):
                bot = self.bots[i]

                bot.spam_x = self.cornes[i][0]
                bot.spam_y = self.cornes[i][1]

                bot.x = self.cornes[i][0]
                bot.y = self.cornes[i][1]

                bot.maze = self.maze
                bot.pixel_data = pixel_data

                bot.i = 0
                bot.pixel = 0
                bot.path = []

                bot.dead = False

                bot.call_bfs()

        self.player_sheat["intangibility"] = False
        self.player_sheat["invincibility"] = False
        self.player_sheat["invincibility"] = False
        self.PLAYER_SPEED = 10
        row, col = self.find_spawn_below_42()
        self.player.x = self.OFFSET_X + col * self.CELL_W + 25
        self.player.y = self.OFFSET_Y + row * self.CELL_H - 150

    def cell_position(self, row: int, col: int) -> tuple[int, int]:
        x = self.OFFSET_X + col * self.CELL_W
        y = self.OFFSET_Y + row * self.CELL_H
        return x, y

    def is_walkable(self, cell: int) -> bool:
        return (
            not (cell & self.N) or
            not (cell & self.E) or
            not (cell & self.S) or
            not (cell & self.W)
        )

    def get_wall_rects(self, row: int, col: int) -> list:
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
                Rect(
                    x, y + self.CELL_H - thickness // 2,
                    self.CELL_W, thickness)
            )
        if cell & self.W:
            walls.append(
                Rect(x - thickness // 2, y, thickness, self.CELL_H)
            )
        if cell & self.E:
            walls.append(
                Rect(
                    x + self.CELL_W - thickness // 2, y, thickness,
                    self.CELL_H)
            )
        return walls

    def check_colision(self, dx: int, dy: int) -> bool:
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

    def check_colision_to_bot(self, bot: Bot, dx: int, dy: int) -> bool:
        w = bot.img_width
        h = bot.img_height
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

    def blip(self) -> None:
        self.mlx.mlx_put_image_to_window(
            self.app,
            self.window,
            self.buffer,
            0,
            0
        )

    def close(self, param: Any) -> None:
        self.quit = True
        self.mlx.mlx_do_key_autorepeaton(self.app)
        self.mlx.mlx_destroy_window(self.app, self.window)
        self.mlx.mlx_loop_exit(self.app)
        return

    def key_press(self, keycode: int, param: Any) -> None:
        if self.victory:
            return
        return self.controls(keycode, param)

    def power(self) -> None:
        if self.power_deadline == 0:
            self.power_deadline = time.monotonic() + 1
            self.power_index = 0
        if time.monotonic() >= self.power_deadline:
            self.POWER = False
            self.power_deadline = 0
        img, img_w, img_h = self.current_power
        x = (self.WIDTH - img_w) // 2
        y = (self.WIDTH - img_h) // 2
        self.mlx.mlx_put_image_to_window(
            self.app,
            self.window,
            img,
            x,
            y - self.power_index
        )
        self.power_index += 15

    def frames(self, x: int, y: int) -> None:
        self.mlx.mlx_clear_window(self.app, self.window)
        if self.reload:
            self.clear_buffer()
            self.draw_board()
            self.reload = False
        self.blip()
        self.draw_information()
        self.mlx.mlx_put_image_to_window(
            self.app,
            self.window,
            self.player.img,
            x,
            y
        )
        if self.pacgums == len(self.gum_position):
            self.coodown = 200
            self.victory = True
            self.gum_position.clear()
        for b in self.bots:
            self.mlx.mlx_put_image_to_window(
                self.app,
                self.window,
                b.img,
                b.x,
                b.y
            )
        if self.POWER:
            self.power()
        now = time.monotonic()
        self.eaten_popups = [
            p for p in self.eaten_popups if p[2] > now
        ]
        for x, y, _ in self.eaten_popups:
            self.mlx.mlx_put_image_to_window(
                self.app,
                self.window,
                self.spam,
                x,
                y
            )

    def controls(self, key: int, param: Any) -> None:
        if self.INPUT:
            if key == 65293:
                self.name_already_set = True

            elif key == 65288 and not self.name_already_set:
                # Backspace
                if len(self.name_player) > 0:
                    self.name_player = self.name_player[:-1]

            elif not self.name_already_set:
                self.set_name_player(key)
            return
        if self.gameover or self.gamewin:
            return
        if key == 32:
            # space
            self.pause_game()
            return

        if self.PAUSE:
            if key == 65362:
                self.pause_index += 1

            if key == 65364:
                self.pause_index -= 1
            if key == 65293 and self.pause_index == 0:
                self.back_to_menu()
            if key == 65293 and self.pause_index == 1:
                self.resume_game()

        if not self.PAUSE:
            if key == 49:
                # tecla 1
                if not self.PLAYER_SPEED == 15:
                    self.PLAYER_SPEED = 15
                    self.current_power = self.power_imgs["speed"]
                    self.POWER = True
                else:
                    self.PLAYER_SPEED = 10

            if key == 50:
                # tecla 2
                if not self.player_sheat["invincibility"]:
                    self.player_sheat["invincibility"] = True
                    self.current_power = self.power_imgs["invincibility"]
                    self.POWER = True
                else:
                    self.player_sheat["invincibility"] = False

            if key == 51:
                # tecla 3
                if not self.POWER:
                    self.data.lives += 1
                    self.current_power = self.power_imgs["lives_plus1"]
                    self.POWER = True

            if key == 52:
                # tecla 4
                if not self.POWER:
                    self.start_level(next_level=True)
                    self.reload = True
                    self.current_power = self.power_imgs["level_plus1"]
                    self.POWER = True

            if key == 53:
                # tecla 5
                if not self.player_sheat["freeze_bots"]:
                    self.player_sheat["freeze_bots"] = True
                    self.current_power = self.power_imgs["freeze_bots"]
                    self.POWER = True
                else:
                    self.player_sheat["freeze_bots"] = False

            if key == 54:
                # tecla 6
                if not self.player_sheat["intangibility"]:
                    self.player_sheat["intangibility"] = True
                    self.current_power = self.power_imgs["intangibility"]
                    self.POWER = True
                else:
                    self.player_sheat["intangibility"] = False

            if key in (65362, 119):
                # up
                self.player.update_img("UP")
            if key in (65361, 97):
                # left
                self.player.update_img("LEFT")
            if key in (65363, 100):
                # right
                self.player.update_img("RIGHT")

            if key in (65364, 115):
                # down
                self.player.update_img("DOWN")
        return

    def pac_gums(self, cell: int, x: int, y: int) -> None:
        if self.is_walkable(cell):
            small_gum_x = x + (self.CELL_W - self.m_w) // 2
            small_gum_y = y + (self.CELL_H - self.m_h) // 2

            if (small_gum_y, small_gum_x) not in self.gum_position:
                return

            if (small_gum_y, small_gum_x) in self.heated_small:
                return
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

    def draw_cell_walls(self, cell: int, x: int, y: int) -> None:
        if cell & self.N:
            drawlineH(
                self.memory.data,
                self.memory.size_line,
                x, y,
                x + self.CELL_W, y,
                self.color
            )

        if cell & self.S:
            drawlineH(
                self.memory.data,
                self.memory.size_line,
                x, y + self.CELL_H,
                x + self.CELL_W, y + self.CELL_H,
                self.color
            )

        if cell & self.W:
            drawlineV(
                self.memory.data,
                self.memory.size_line,
                x, y,
                x, y + self.CELL_H,
                self.color
            )

        if cell & self.E:
            drawlineV(
                self.memory.data,
                self.memory.size_line,
                x + self.CELL_W, y,
                x + self.CELL_W, y + self.CELL_H,
                self.color
            )

    def fill_42(self) -> None:
        for i in range(len(self.maze.maze)):
            for j in range(len(self.maze.maze[i])):
                cell = self.maze.maze[i][j]

                if cell == 15:
                    x, y = self.cell_position(i, j)

                    center_x = x + self.CELL_W // 2
                    center_y = y + self.CELL_H // 2

                    put_pixel(
                        self.memory.data,
                        self.memory.size_line,
                        center_x,
                        center_y,
                        0xFFFFFFFF
                    )

    def draw_board(self) -> None:
        self.fill_42()
        for i in range(len(self.maze.maze)):
            for j in range(len(self.maze.maze[i])):
                cell = self.maze.maze[i][j]

                x, y = self.cell_position(i, j)
                self.draw_cell_walls(cell, x, y)
                self.pac_gums(cell, x, y)

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

    def end_screen(self) -> None:
        if self.end_until == 0:
            self.end_until = time.monotonic() + 3
            if self.gameover:
                self.game_over()
            else:
                self.game_win()
            return
        if time.monotonic() >= self.end_until:
            self.get_user_name()

    def get_user_name(self) -> None:
        x = (self.WIDTH - self.n_w) // 2
        self.mlx.mlx_clear_window(
            self.app,
            self.window
        )
        self.mlx.mlx_put_image_to_window(
            self.app,
            self.window,
            self.names_img,
            x,
            0,
        )
        self.mlx.mlx_string_put(
            self.app,
            self.window,
            round((self.WIDTH // 2) * 0.80),
            round((self.HEIGHT // 2) * 0.98),
            0x00FFFFFF,
            self.name_player
        )
        self.mlx.mlx_string_put(
            self.app,
            self.window,
            round((self.WIDTH // 2) * 1.05),
            round((self.HEIGHT // 2) * 0.63),
            0x00FFFFFF,
            str(self.points)
        )
        self.INPUT = True
        if self.name_already_set:
            skip = False
            if not self.name_player.strip():
                self.name_player = "UNKNOWN"
                skip = True
            self.db.insert_on_table(
                self.name_player.strip(),
                self.points,
                skip
            )
            self.back_to_menu()

    def back_to_menu(self) -> None:
        self.reset_game()
        self.start = True
        self.mlx.mlx_clear_window(self.app, self.window)
        self.mlx.mlx_loop_exit(self.app)

    def reset_game(self) -> None:
        self.eaten_popups = []
        self.gameover = False
        self.gamewin = False
        self.victory = False
        self.INPUT = False
        self.PAUSE = False
        self.index = 0
        self.data.lives = self.initial_lives
        self.PLAYER_SPEED = 10
        self.points = 0
        self.super_pac = False
        self.super_pac_deadline = 0
        self.end_until = 0
        for k in self.player_sheat:
            self.player_sheat[k] = False
        self.gum_position.clear()
        self.heated_small.clear()
        self.heated_big.clear()
        for b in self.bots:
            b.dead = False
            b.reset_img(self.mlx, self.app)
        self.name_player = ""
        self.name_already_set = False
        self.new_game_input = False
        self.high_scores_input = False
        self.show_controls_input = False
        self.img_index = 0
        self.pacgums = 0
        self.pause_index = 0
        self.enter_index = 0
        self.reload = False
        self.power_deadline = 0
        self.player_deadline = 0
        self.scores = self.db.get_scores()

    def render_loop(self, param: Any) -> int:
        if self.start:
            return 0
        elif self.gameover or self.gamewin:
            self.end_screen()
            return 0
        elif self.victory:
            self.coodown -= 1

            if self.coodown <= 0:
                self.victory = False
                self.coodown = 100
                self.start_level()
                self.draw_board()
            else:
                self.level_win()

        elif self.PAUSE:
            self.frames(
                self.player.x,
                self.player.y
            )
            self.pause()

        else:
            self.move(self.player)

            self.frames(
                self.player.x,
                self.player.y
            )
        return 0

    def level_win(self) -> None:
        x = (self.WIDTH - self.v_w) // 2
        self.mlx.mlx_put_image_to_window(
            self.app,
            self.window,
            self.victory_img,
            x,
            round((self.HEIGHT // 2) * 0.95)
        )

    def game_win(self) -> None:
        self.mlx.mlx_clear_window(
            self.app,
            self.window
        )
        x = (self.WIDTH - self.win_w) // 2
        self.mlx.mlx_put_image_to_window(
            self.app,
            self.window,
            self.win_img,
            x,
            round((self.HEIGHT // 2) * 0.95)
        )

    def game_over(self) -> None:
        self.mlx.mlx_clear_window(self.app, self.window)
        x = (self.WIDTH - self.over_w) // 2
        self.mlx.mlx_put_image_to_window(
            self.app,
            self.window,
            self.gameover_img,
            x,
            round((self.HEIGHT // 2) * 0.95)
        )

    def pause(self) -> None:
        pause_img, pause_w, pause_h = self.get_pause_image()
        self.pause_index = self.pause_index % len(self.pause_imgs)
        x = (self.WIDTH - pause_w) // 2
        y = (self.HEIGHT - pause_h) // 2
        self.mlx.mlx_put_image_to_window(
            self.app,
            self.window,
            pause_img,
            x,
            y
        )

    def is_near_player(self, bot: Bot, player: Player, distance: int) -> bool:
        dx = bot.x - player.x
        dy = bot.y - player.y
        return dx * dx + dy * dy <= distance * distance

    def check_bot_player_collision(
        self,
        bot: Bot,
        invencible: bool = False
    ) -> bool:
        if invencible:
            return False
        player_rect = Rect(
            self.player.x,
            self.player.y,
            self.player.img_width,
            self.player.img_height
        )
        bot_center_x = bot.x + bot.img_width // 2
        bot_center_y = bot.y + bot.img_height // 2
        bot_rect = Rect(
            bot_center_x - bot.HEAT_BOX_BOT_X,
            bot_center_y - bot.HEAT_BOX_BOT_Y,
            bot.HEAT_BOX_BOT_X * 2,
            bot.HEAT_BOX_BOT_Y * 2
        )
        return player_rect.colliderect(bot_rect)

    def move_bots(self) -> None:
        if self.super_pac and time.time() >= self.super_pac_deadline:
            self.super_pac = False
            for bot in self.bots:
                bot.reset_img(self.mlx, self.app)
        for b in self.bots:
            if time.time() >= b.bot_respaw and b.dead:
                b.dead = False
                b.reset_img(self.mlx, self.app)

            invincible = self.player_sheat["invincibility"]
            touching = self.check_bot_player_collision(
                b,
                invencible=invincible
            )
            if b.dead:
                continue

            if self.super_pac:
                if not b.path or b.i >= len(b.path) and not b.dead:
                    b.scape((self.player.x, self.player.y))
                if touching and not b.dead:
                    self.eaten_popups.clear()
                    self.eaten_popups.append((
                        b.x + b.img_width // 2 - self.spam_w // 2,
                        b.y + b.img_height // 2 - self.spam_h // 2,
                        time.monotonic() + 0.9
                    ))
                    b.recalculate_rote((b.x, b.y), (0, 0), respaw=True)
                    b.kill_bot(self.mlx, self.app)
                    self.points += self.data.points_per_ghost
                    b.bot_respaw = time.time() + b.BOT_TIME_DEAD

            elif touching and not invincible:
                if not self.data.lives > 1:
                    self.gameover = True
                else:
                    self.data.lives -= 1
                    self.start_level(next_level=False)

            else:
                if not b.path or b.i >= len(b.path):
                    if self.is_near_player(
                        b,
                        self.player,
                        250
                    ):
                        b.recalculate_rote(
                            (b.x, b.y),
                            (self.player.x, self.player.y)
                        )
                    else:
                        x = randint(0, self.player.x)
                        y = randint(0, self.player.y)
                        b.recalculate_rote(
                            (b.x, b.y),
                            (x, y)
                        )

            direction, dx, dy = b.next_position()
            if self.check_colision_to_bot(b, dx, dy):
                b.move_bot()
                b.pixel += self.BOT_SPEED
                cell_size = self.CELL_H if direction in (
                    "N", "S") else self.CELL_W
                while b.pixel >= cell_size:
                    b.pixel -= cell_size
                    b.i += 1
            else:
                b.i += 1
                b.pixel = 0

    def gums(self) -> None:
        gum = self.player.hit_gum(
            self.gum_position,
            self.OFFSET_X,
            self.OFFSET_Y,
            self.CELL_W,
            self.CELL_H,
            self.m_w,
            self.m_h,
        )

        player_rect = Rect(
            self.player.x,
            self.player.y,
            self.player.img_width,
            self.player.img_height
        )
        big = None
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
            self.pacgums += 1
            self.reload = True

        if big is not None and big not in self.heated_big:
            self.heated_big.append(big)
            self.points -= self.data.points_per_pacgum
            self.points += self.data.points_per_super_pacgum
            self.pacgums += 1
            self.reload = True
            self.super_pac_deadline = time.time() + self.time_super_pac
            self.super_pac = True
            for bot in self.bots:
                if not bot.dead:
                    bot.scape((self.player.x, self.player.y))
                    bot.powerup_img(self.mlx, self.app)

    def try_move_step(
        self,
        dx_dir: int,
        dy_dir: int,
        step: int,
        intangibility: bool
    ) -> bool:
        self.player.x = dx = self.player.x + dx_dir * step
        self.player.y = dy = self.player.y + dy_dir * step

        if colision(
            self.player,
            self.OFFSET_X,
            self.OFFSET_X + self.map_width,
            self.OFFSET_Y,
            self.OFFSET_Y + self.map_height,
        ):
            self.player.x -= dx_dir * step
            self.player.y -= dy_dir * step
            return False
        if intangibility:
            return True
        if not self.check_colision(dx, dy):
            self.player.x -= dx_dir * step
            self.player.y -= dy_dir * step
            return False
        return True

    def move(self, param: Any) -> None:
        direction_vectors = {
            "UP":    (0, -1),
            "DOWN":  (0, 1),
            "LEFT":  (-1, 0),
            "RIGHT": (1, 0),
        }
        direction = self.player._direction
        if direction in direction_vectors:
            dx_dir, dy_dir = direction_vectors[direction]
            MAX_STEP = 4
            remaining = self.PLAYER_SPEED
            while remaining > 0:
                step = min(MAX_STEP, remaining)
                moved = self.try_move_step(
                    dx_dir,
                    dy_dir,
                    step,
                    self.player_sheat["intangibility"]
                )
                remaining -= step
                if not moved:
                    break

        self.gums()
        if self.player_deadline == 0:
            self.player_deadline = time.monotonic() + 0.05
        if time.monotonic() >= self.player_deadline:
            self.player.update_img(
                self.player._direction,
            )
            self.player_deadline = 0
        if not self.player_sheat["freeze_bots"]:
            self.move_bots()
        self.frames(self.player.x, self.player.y)

    def draw_information(self) -> None:
        hud_top = self.HEIGHT - self.HUD_HEIGHT
        margin_x = round(self.WIDTH * 0.02)

        self.mlx.mlx_string_put(
            self.app,
            self.window,
            margin_x,
            hud_top - 10,
            0x00FFFFFF,
            "Points: " + str(self.points)
        )
        self.mlx.mlx_string_put(
            self.app,
            self.window,
            margin_x,
            hud_top + 10,
            0x00FFFFFF,
            "Level: " + str(self.index)
        )
        if not self.PAUSE:
            remaining = max(0, self.level_deadline - time.monotonic())
            if remaining <= 0:
                self.gameover = True
            self.mlx.mlx_string_put(
                self.app,
                self.window,
                margin_x + 160,
                hud_top + 10,
                0x00FFFFFF,
                "Time: " + str(round(remaining))
            )
        self.mlx.mlx_string_put(
            self.app,
            self.window,
            margin_x + 160,
            hud_top - 10,
            0x00FFFFFF,
            "Lives: " + str(self.data.lives)
        )

    def new_game(self, param: Any) -> None:
        if not self.new_game_input:
            return
        if self.enter_deadline == 0:
            self.enter_deadline = time.monotonic() + 0.5
        if time.monotonic() >= self.enter_deadline:
            enter_img, w, _ = self.get_enter_image()
            x = (self.WIDTH - w) // 2
            self.mlx.mlx_clear_window(
                self.app,
                self.window
            )
            self.mlx.mlx_put_image_to_window(
                self.app,
                self.window,
                enter_img,
                x,
                0
            )
            self.enter_deadline = 0

    def high_scores(self) -> None:
        if self.scores:

            x = round((self.WIDTH // 2) * 0.90)
            y = round((self.HEIGHT // 2) * 0.75)
            space_line = 40

            for i, (name, score) in enumerate(self.scores):
                self.mlx.mlx_string_put(
                    self.app,
                    self.window,
                    x,
                    y + i * space_line,
                    0xFFFFFF,
                    f"{name} - {score}"
                )

    def show_controls(self) -> None:
        x = (self.WIDTH - self.c_w) // 2
        self.mlx.mlx_put_image_to_window(
            self.app,
            self.window,
            self.img_controls,
            x,
            0
        )

    def redraw_start_screen(self) -> None:
        self.mlx.mlx_clear_window(self.app, self.window)
        self.start_screen()

    def start_game(self, keycode: int, param: Any) -> None:
        if keycode == 0xff1b and any(
            [
                self.new_game_input,
                self.high_scores_input,
                self.show_controls_input
            ]
        ):
            self.new_game_input = False
            self.high_scores_input = False
            self.show_controls_input = False

        elif keycode == 0xff1b:
            self.close(param)
            return

        elif self.new_game_input:
            if keycode == 32:
                # Space
                self.start = False
                self.mlx.mlx_loop_exit(self.app)
                return
        elif keycode == 65293 and self.img_index == 0:
            self.new_game_input = True
        elif keycode == 65293 and self.img_index == 1:
            self.high_scores_input = True
        elif keycode == 65293 and self.img_index == 2:
            self.show_controls_input = True
        elif keycode == 65293 and self.img_index == 3:
            self.exit = True

        elif keycode == 65362:
            self.img_index -= 1
            self.img_index = self.img_index % len(self.menu)

        elif keycode == 65364:
            self.img_index += 1
            self.img_index = self.img_index % len(self.menu)

        self.redraw_start_screen()

    def set_name_player(self, keycode: int) -> None:
        if keycode not in keyboard.keys():
            return
        k: str = keyboard[keycode]
        if len(self.name_player) > 15:
            return
        if k == "capslock!":
            self.capslock = not self.capslock
        if k.isalpha() or k == " ":
            self.name_player += (k.upper() if self.capslock else k.lower())

    def start_screen(self) -> None:
        if self.new_game_input:
            enter_img, w, _ = self.get_enter_image()
            x = (self.WIDTH - w) // 2
            self.mlx.mlx_clear_window(
                self.app,
                self.window
            )
            self.mlx.mlx_put_image_to_window(
                self.app,
                self.window,
                enter_img,
                x,
                0
            )
            self.mlx.mlx_loop_hook(
                self.app,
                self.new_game,
                None
            )
            return
        elif self.high_scores_input:
            self.high_scores()
            return
        elif self.show_controls_input:
            self.show_controls()
            return
        elif self.exit:
            self.close(None)
            return

        img, img_width, _ = self.get_image()

        x = (self.WIDTH - img_width) // 2

        self.mlx.mlx_put_image_to_window(
            self.app,
            self.window,
            img,
            x - 100,
            0
        )

    def pause_game(self) -> None:
        if not self.PAUSE:
            self.PAUSED_TIME = max(
                0,
                self.level_deadline - time.monotonic()
            )
            self.PAUSE = True

    def resume_game(self) -> None:
        if self.PAUSE:
            self.level_deadline = time.monotonic() + self.PAUSED_TIME
            self.PAUSE = False

    def game_menu(self) -> None:
        self.start_screen()
        self.mlx.mlx_hook(self.window, 2, 1 << 0, self.start_game, None)
        self.mlx.mlx_loop(self.app)

    def run(self) -> None:
        self.mlx.mlx_do_key_autorepeatoff(self.app)
        while not self.quit:
            self.game_menu()
            if self.quit:
                break
            self.start_level()
            self.clear_buffer()
            self.draw_board()
            self.mlx.mlx_hook(
                self.window,
                2,
                1 << 0,
                self.key_press,
                self.player
            )
            self.mlx.mlx_loop_hook(self.app, self.render_loop, None)
            self.mlx.mlx_loop(self.app)
