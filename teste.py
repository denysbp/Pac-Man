from src.models.bots import Bot
from mazegenerator.mazegenerator import MazeGenerator
import os

os.system("clear")
#maze = MazeGenerator((15, 15), perfect=False, entry_cell=(0, 0), exit_cell=(10, 10), seed=1)
#ghost = Bot(img=None, spam_x = 2, spam_y = 3, maze=maze, bot_id=2)
#print(maze.shortest_path)



        self.bots: list[Bot] = []
        for i in range(4):
            self.bots.append(Bot(spam_x = 2, spam_y = 3, maze=self.maze, bot_id=i))












from mlx import Mlx
from typing import Any, Union
from mazegenerator.mazegenerator import MazeGenerator
from collections import deque
from .metadata import Rect

class Bot:
    def __init__(
        self,
        spam_x: int,
        spam_y: int,
        maze: MazeGenerator,
        mlx : Mlx = False,
        mlx_ptr: Any = False,
        bot_id: int = 0,
        OFFSET_X: int = 1,
        OFFSET_Y: int = 1,
        CELL_W: int = 1,
        CELL_H: int = 1,
        SPEED: int = 1
    ):
        images: list[str] = [
            "src/models/assets/ghost_images/orange.png",
            "src/models/assets/ghost_images/pink.png",
            "src/models/assets/ghost_images/red.png",
            "src/models/assets/ghost_images/blue.png",
            ]
        self.OFFSET_X = OFFSET_X
        self.OFFSET_Y = OFFSET_Y
        self.CELL_W = CELL_W
        self.CELL_H = CELL_H
        self.SPEED = SPEED
    
        self.img, self.width, self.height = mlx.mlx_png_file_to_image(mlx_ptr, images[bot_id % len(images)])
        self.goal_coord: tuple[int, int] = (10, 10)

        self.x = spam_x
        self.y = spam_y
        self.current_coord = (spam_x, spam_y) # pixel
        self.maze = maze
        self.grid = maze.maze
        #self.path = self.bfs(self.current_coord, (self.goal_coord))
  
        self.running = True
        self.i = 0

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

    def get_valid_cells(self, current_position: tuple[int, int]):
        valid_cells = []
        x, y = self.get_coord_to_maze_grid(current_position)
        col, row = current_position
        cell = self.grid[y][x]
        if self.can_advance(cell, "N"):
            valid_cells.append(("N", (col, row - 1)))

        if self.can_advance(cell, "E"):
            valid_cells.append(("E", (col + 1, row)))

        if self.can_advance(cell, "S"):
            valid_cells.append(("S", (col, row + 1)))

        if self.can_advance(cell, "W"):
            valid_cells.append(("W", (col - 1, row)))

        return valid_cells

    def bfs(self, bot_coord: tuple[int, int], goal_coord:tuple[int, int]):
        visited = {bot_coord}
        queue = deque([(bot_coord, [])])

        while queue:
            current_position, path = queue.popleft()
            if current_position == self.get_pixel_to_vizualization(goal_coord):
                return path

            for direction, next_cell in self.get_valid_cells(current_position):
                if next_cell not in visited:
                    visited.add(next_cell)
                    queue.append((next_cell, path + [direction]))
        return []

    def get_coord_to_maze_grid(self, coord):
        x = (coord[0] - self.OFFSET_X) // self.CELL_W # calculo para tirar de pixels e se encaixar na grid em cordenadas
        y = (coord[1]- self.OFFSET_Y) // self.CELL_H # calculo para tirar de pixels e se encaixar na grid em cordenadas
        return x, y

    def get_pixel_to_vizualization(self, coord):
        x = (coord[0] + self.OFFSET_X) * self.CELL_W # calculo para tirar de pixels e se encaixar na grid em cordenadas
        y = (coord[1] + self.OFFSET_Y) * self.CELL_H # calculo para tirar de pixels e se encaixar na grid em cordenadas
        return x, y

    def move_bot(self):
        x, y = self.current_coord

        if self.path[self.i % len(self.path)] == "N":
            self.current_coord = self.current_coord[0] - self.SPEED
        elif self.path[self.i % len(self.path)] == "E":
            self.current_coord = self.current_coord[1] + self.SPEED
        elif self.path[self.i % len(self.path)] == "S":
            self.current_coord = self.current_coord[0] + self.SPEED
        elif self.path[self.i % len(self.path)] == "W":
            self.current_coord = self.current_coord[1] - self.SPEED
        self.i += 1
            
#
        #center_x = self.x + self.img_width // 2
        #center_y = self.y + self.img_height // 2
#
        #col = (center_x - OFFSET_X) // CELL_W
        #row = (center_y - OFFSET_Y) // CELL_H
#
        #gum_x = OFFSET_X + col * CELL_W + (CELL_W - m_w) // 2
        #gum_y = OFFSET_Y + row * CELL_H + (CELL_H - m_h) // 2
 for i in range(4):
            self.bots.append(Bot(spam_x = 0,SPEED=self.SPEED, spam_y=0, CELL_W=self.CELL_W, CELL_H=self.CELL_H, OFFSET_X=self.OFFSET_X, OFFSET_Y=self.OFFSET_Y, mlx_ptr=self.app, mlx=self.mlx, maze=self.maze, bot_id=i))
            #self.bots.append(Bot(spam_x = self.cornes[i][0],SPEED=self.SPEED, spam_y=self.cornes[i][1], CELL_W=self.CELL_W, CELL_H=self.CELL_H, OFFSET_X=self.OFFSET_X, OFFSET_Y=self.OFFSET_Y, mlx_ptr=self.app, mlx=self.mlx, maze=self.maze, bot_id=i))