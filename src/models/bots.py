from mlx import Mlx
from typing import Any, Union
from mazegenerator.mazegenerator import MazeGenerator
from collections import deque
from src.models.metadata import Rect
from random import randint


class Bot:
    def __init__(
        self,
        spam_x: int,
        spam_y: int,
        maze: MazeGenerator,
        mlx : Mlx,
        mlx_ptr: Any,
        bot_id: int = 0,
        pixel_data: dict[str, int] = {}
    ):
        self.images: list[str] = [
            "src/models/assets/ghost_images/orange.png",
            "src/models/assets/ghost_images/pink.png",
            "src/models/assets/ghost_images/red.png",
            "src/models/assets/ghost_images/blue.png",
            ]
        self.id = bot_id
        self.img, self.width, self.height = mlx.mlx_png_file_to_image(
            mlx_ptr,
            self.images[self.id % len(self.images)]
            )
        self.x = spam_x
        self.y = spam_y
        self.pixel_data = pixel_data
        self.maze = maze
        self.i = 0
        self.goal_coord = (11, 11)
        self.grid = []
        self.path = []
        self.pixel = 0
        self.dead = False
        self.HEAT_BOX_BOT = 70
        self.BOT_TIME_DEAD = 8
        self.bot_respaw = 0

    @staticmethod
    def can_advance(cell: int, direction: str) -> bool:
        if direction == "N":
            return not (cell & 0b0001)
        elif direction == "E":
            return not (cell & 0b0010)
        elif direction == "S":
            return not (cell & 0b0100)
        elif direction == "W":
            return not (cell & 0b1000)

    def call_bfs(self):
        self.grid = self.maze.maze
        self.path = self.bfs(self.get_coord_to_maze_grid((self.x, self.y)), (self.goal_coord))

    def get_valid_cells(self, current_position):
        valid_cells = []
        x, y = current_position

        height = len(self.grid)
        width = len(self.grid[0])
        if not (0 <= x < width and 0 <= y < height):
            return []

        cell = self.grid[y][x]
        if y > 0 and self.can_advance(cell, "N"):
            valid_cells.append(("N", (x, y - 1)))

        if x < width - 1 and self.can_advance(cell, "E"):
            valid_cells.append(("E", (x + 1, y)))

        if y < height - 1 and self.can_advance(cell, "S"):
            valid_cells.append(("S", (x, y + 1)))

        if x > 0 and self.can_advance(cell, "W"):
            valid_cells.append(("W", (x - 1, y)))

        return valid_cells

    def bfs(self, bot_coord: tuple[int, int], goal_coord: tuple[int, int]):
        visited = {bot_coord}
        queue = deque([(bot_coord, [])])

        while queue:
            current_position, path = queue.popleft()

            if current_position == goal_coord:
                return path

            for direction, next_cell in self.get_valid_cells(current_position):
                if next_cell not in visited:
                    visited.add(next_cell)
                    queue.append((next_cell, path + [direction]))

        return []

    def next_position(self):
                            # se chegou no goal
        if not self.path or self.i > len(self.path):
            return None, self.x, self.y
        direction = self.path[self.i % len(self.path)]

        bx, by = self.x, self.y
        if direction == "N":
            by -= self.pixel_data.get("SPEED")
        elif direction == "E":
            bx += self.pixel_data.get("SPEED")
        elif direction == "S":
            by += self.pixel_data.get("SPEED")
        elif direction == "W":
            bx -= self.pixel_data.get("SPEED")
        return direction, bx, by


    def move_bot(self):
        direction, dx, dy = self.next_position()
        self.x, self.y = dx, dy
        self.current_direction = direction

    def recalculate_rote(self, bot_coord: tuple[int, int], goal_coord: tuple[int, int] = False, calcule_to_midle: bool = False):
        if calcule_to_midle:
            new = self.bfs(self.get_coord_to_maze_grid(bot_coord), (self.maze._width // 2, self.maze._height // 2))
        else:
            new = self.bfs(self.get_coord_to_maze_grid(bot_coord), self.get_coord_to_maze_grid(goal_coord))
        if new:
            self.path = new
            self.i = 0
            self.pixel = 0

    def scape(self, player_cordintaes: tuple[int, int]):
        bot = self.get_coord_to_maze_grid((self.x, self.y))
        player = self.get_coord_to_maze_grid(player_cordintaes)

        valid_cells = self.get_valid_cells(bot)

        if not valid_cells:
            return

        px, py = player

        _, escape_cell = max(
            valid_cells,
            key=lambda item: (
                abs(item[1][0] - px) +
                abs(item[1][1] - py)
            )
        )
        new = self.bfs(bot, escape_cell)

        if new:
            self.path = new
            self.i = 0
            self.pixel = 0

    def powerup_img(self, mlx: Mlx, mlx_ptr):
        self.img, self.width, self.height = mlx.mlx_png_file_to_image(
            mlx_ptr,
            "src/models/assets/ghost_images/powerup.png"
        )

    def kill_bot(self, mlx: Mlx, mlx_ptr):
        self.img, self.width, self.height = mlx.mlx_png_file_to_image(
            mlx_ptr,
            "src/models/assets/ghost_images/dead.png"
        )
        self.dead = True


    def reset_img(self, mlx: Mlx, mlx_ptr):
        self.img, self.width, self.height = mlx.mlx_png_file_to_image(
            mlx_ptr, self.images[self.id % len(self.images)]
        )

    def get_coord_to_maze_grid(self, coord: tuple[int, int]):
        x = (coord[0] - self.pixel_data.get("OFFSET_X")) // self.pixel_data.get("CELL_W") # calculo para tirar de pixels e se encaixar na grid em cordenadas
        y = (coord[1] - self.pixel_data.get("OFFSET_Y")) // self.pixel_data.get("CELL_H") # calculo para tirar de pixels e se encaixar na grid em cordenadas
        return (x, y)

    @property
    def rect(self):
        return Rect(self.x, self.y, self.width, self.height)