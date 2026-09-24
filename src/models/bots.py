from mlx import Mlx
from typing import Any, Union
from mazegenerator.mazegenerator import MazeGenerator
from collections import deque
from src.models.metadata import Rect


class Bot:
    def __init__(
        self,
        spam_x: int,
        spam_y: int,
        maze: MazeGenerator,
        mlx: Mlx,
        mlx_ptr: Any,
        bot_id: int = 0,
        pixel_data: dict[str, int] = {}
    ) -> None:
        self.images: list[str] = [
            "src/models/assets/ghost_images/orange.png",
            "src/models/assets/ghost_images/pink.png",
            "src/models/assets/ghost_images/red.png",
            "src/models/assets/ghost_images/blue.png",
            ]
        self.id = bot_id
        self.img, self.img_width, self.img_height = mlx.mlx_png_file_to_image(
            mlx_ptr,
            self.images[self.id % len(self.images)]
            )
        self.spam_x = spam_x
        self.spam_y = spam_y

        self.x = spam_x
        self.y = spam_y
        self.pixel_data = pixel_data
        self.maze = maze
        self.i = 0
        self.goal_coord = (11, 11)
        self.grid: list[list[int]] = []
        self.path: list[str] | None = []
        self.pixel = 0
        self.dead = False
        margin = 4
        self.HEAT_BOX_BOT_X = self.img_width // 2 + margin
        self.HEAT_BOX_BOT_Y = self.img_height // 2 + margin
        self.BOT_TIME_DEAD = 5
        self.bot_respaw: float | int = 0

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
        return False

    def call_bfs(self) -> None:
        self.grid = self.maze.maze
        self.path = self.bfs(self.get_coord_to_maze_grid(
            (self.x, self.y)), (self.goal_coord)
        )

    def get_valid_cells(self, current_position: tuple[int, int]) -> list:
        valid_cells = []
        x, y = current_position

        cell = self.grid[y][x]
        if self.can_advance(cell, "N"):
            valid_cells.append(("N", (x, y - 1)))

        if self.can_advance(cell, "E"):
            valid_cells.append(("E", (x + 1, y)))

        if self.can_advance(cell, "S"):
            valid_cells.append(("S", (x, y + 1)))

        if self.can_advance(cell, "W"):
            valid_cells.append(("W", (x - 1, y)))

        return valid_cells

    def bfs(
        self,
        bot_coord: tuple[int, int],
        goal_coord: tuple[int, int]
    ) -> Any | None:
        if bot_coord == goal_coord:
            return []

        visited = {bot_coord}
        queue: deque = deque([(bot_coord, [])])

        while queue:
            current_position, path = queue.popleft()
            if current_position == goal_coord:
                return path

            for direction, next_cell in self.get_valid_cells(current_position):
                if next_cell not in visited:
                    visited.add(next_cell)
                    queue.append((next_cell, path + [direction]))

        return None

    def next_position(self) -> tuple[Union[str, None], int, int]:
        if not self.path or self.i >= len(self.path):
            return None, self.x, self.y
        direction = self.path[self.i % len(self.path)]

        bx, by = self.x, self.y
        if direction == "N":
            by -= self.pixel_data["SPEED"]
        elif direction == "E":
            bx += self.pixel_data["SPEED"]
        elif direction == "S":
            by += self.pixel_data["SPEED"]
        elif direction == "W":
            bx -= self.pixel_data["SPEED"]
        return direction, bx, by

    def move_bot(self) -> None:
        direction, dx, dy = self.next_position()
        self.x, self.y = dx, dy
        self.current_direction = direction

    def recalculate_rote(
        self,
        bot_coord: tuple[int, int],
        goal_coord: tuple[int, int],
        respaw: bool = False
    ) -> None:
        if respaw:
            self.x, self.y = self.spam_x, self.spam_y
            new = self.bfs(
                self.get_coord_to_maze_grid(bot_coord),
                self.get_coord_to_maze_grid((self.spam_x, self.spam_y))
            )
        else:
            new = self.bfs(
                self.get_coord_to_maze_grid(bot_coord),
                self.get_coord_to_maze_grid(goal_coord)
            )
        if new is not None:
            self.path = new
            self.i = 0
            self.pixel = 0

    def scape(self, player_cordintaes: tuple[int, int]) -> None:
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
        if new is not None:
            self.path = new
            self.i = 0
            self.pixel = 0

    def powerup_img(self, mlx: Mlx, mlx_ptr: Any) -> None:
        self.img, self.width, self.height = mlx.mlx_png_file_to_image(
            mlx_ptr,
            "src/models/assets/ghost_images/powerup.png"
        )

    def kill_bot(self, mlx: Mlx, mlx_ptr: Any) -> None:
        self.img, self.width, self.height = mlx.mlx_png_file_to_image(
            mlx_ptr,
            "src/models/assets/ghost_images/dead.png"
        )
        self.dead = True

    def reset_img(self, mlx: Mlx, mlx_ptr: Any) -> None:
        self.img, self.width, self.height = mlx.mlx_png_file_to_image(
            mlx_ptr, self.images[self.id % len(self.images)]
        )

    def get_coord_to_maze_grid(
        self,
        coord: tuple[int, int]
    ) -> tuple[int, int]:
        x = (
            coord[0] - self.pixel_data["OFFSET_X"]
        ) // self.pixel_data["CELL_W"]
        y = (
            coord[1] - self.pixel_data["OFFSET_Y"]
        ) // self.pixel_data["CELL_H"]
        return (x, y)

    def can_reset(self) -> bool:
        return (self.x, self.y) == (self.spam_x, self.spam_y)

    @property
    def rect(self) -> Rect:
        return Rect(self.x, self.y, self.width, self.height)
