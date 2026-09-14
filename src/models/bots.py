from mlx import Mlx
from typing import Any, Union
from mazegenerator.mazegenerator import MazeGenerator
from collections import deque


class Bot:
    def __init__(
        self,
        spam_x: int,
        spam_y: int,
        maze: MazeGenerator,
        mlx : Mlx = False,
        mlx_ptr: Any = False,
        bot_id: int = 0
    ):
        images: list[str] = [
            "src/models/assets/ghost_images/orange.png",
            "src/models/assets/ghost_images/pink.png",
            "src/models/assets/ghost_images/red.png",
            "src/models/assets/ghost_images/blue.png",
            ]
        self.img, self.width, self.height = mlx.mlx_png_file_to_image(mlx_ptr, images[bot_id % len(images)])
        self.x = spam_x
        self.y = spam_y
        self.maze = maze
        maze.generate()
        self.grid = maze.maze
        self.running = False


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

    def get_valid_cells(self, current_position):
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

    def bfs(self, bot_coord, goal_coord):
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

    def move_bot(s):
        pass #while