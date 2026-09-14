from mlx import Mlx
from typing import Any, Union
from mazegenerator.mazegenerator import MazeGenerator
from collections import deque


class Bot:
    def __init__(
        self,
        img: Union[Any | None],
        img_width: int,
        img_height: int,
        spam_x: int,
        spam_y: int,
        maze: MazeGenerator,
        mlx : Mlx = False,
        mlx_ptr: Any = False
    ):
        # self.img = img
        # self.height = img_height
        # self.width = img_width
        self.x = spam_x
        self.y = spam_y
        self.maze = maze
        maze.generate()
        self.grid = maze.maze
        self.bfs((spam_x, spam_y), (10, 10))
        print(bin(maze.maze[3][7])[2:])

    def can_advance(binare: int, direction: str) -> bool:
        if direction == "N":
            if binare in {111, 110, 100, 0000}:
                return (True)
            else:
                return(False)
        elif direction == "E":
            if binare in {1011, 10, 1010, 0000}:
                return (True)
            else:
                return(False)
        elif direction == "S":
            if binare in {1101, 1100, 1001, 0000}:
                return (True)
            else:
                return(False)
        elif direction == "W":
            if binare in {1110, 110, 10, 0000}:
                return (True)
            else:
                return(False)

    def get_valid_cells(self, x, y: tuple[int, int]):
        valid_cells = []

        if self.can_advance(bin(self.grid[x][y]), "N"):
            valid_cells.append("N", (x, y - 1))

        if self.can_advance(bin(self.grid[x][y]), "E"):
            valid_cells.append("E", (x + 1, y))

        if self.can_advance(bin(self.grid[x][y]), "S"):
            valid_cells.append("S", (x, y + 1))

        if self.can_advance(bin(s.grid[x][y]), "W"):
            valid_cells.append("W", (x - 1, y))

        return valid_cells

    def bfs(self, bot_coord: tuple[int, int], goal_coord: tuple[int, int]):
        visited: set[tuple[int]] = {bot_coord}
        queue: deque[tuple[tuple[int, int], list[str]]] = deque()
        queue = (bot_coord, [])

        while queue:
            if self.grid[bot_coord[0]]
        




    def move_bot(s):
        pass