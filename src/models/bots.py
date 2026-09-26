from mlx import Mlx
from typing import Any, Union
from mazegenerator.mazegenerator import MazeGenerator
from collections import deque
from src.models.metadata import Rect


class Bot:
    """
    Responsible for managing the bot position, movement, images and
    pathfinding through the maze

    Attributes
    __________
    images: list[str]
        store the paths to the images used by the bots
    id: int
        identify the bot and determine its image
    img: Any
        store the current bot image
    img_width: int
        represent the width of the current bot image
    img_height: int
        represent the height of the current bot image
    spam_x: int
        represent the horizontal spawn position of the bot
    spam_y: int
        represent the vertical spawn position of the bot
    x: int
        represent the current horizontal position of the bot
    y: int
        represent the current vertical position of the bot
    pixel_data: dict[str, int]
        store the map and movement values used by the bot
    maze: MazeGenerator
        store the maze used for pathfinding
    i: int
        store the current position in the movement path
    goal_coord: tuple[int, int]
        represent the default goal position in the maze
    grid: list[list[int]]
        store the maze grid used for pathfinding
    path: list[str] | None
        store the directions calculated by the pathfinding algorithm
    pixel: int
        store the current pixel progress during movement
    dead: bool
        indicate whether the bot has been killed
    HEAT_BOX_BOT_X: int
        represent the horizontal size of the bot collision area
    HEAT_BOX_BOT_Y: int
        represent the vertical size of the bot collision area
    BOT_TIME_DEAD: int
        represent the amount of time the bot remains dead
    bot_respaw: float | int
        store the time associated with the bot respawn

    Methods
    _______
    can_advance():
        verify if the bot can move in a given direction
    call_bfs():
        calculate a path from the bot position to the goal position
    get_valid_cells():
        return the cells that can be reached from a given position
    bfs():
        find the shortest path between two cells in the maze
    next_position():
        calculate the next bot position according to its current path
    move_bot():
        update the bot position using the next movement direction
    recalculate_rote():
        calculate a new path for the bot
    scape():
        calculate a path that moves the bot away from the player
    powerup_img():
        change the bot image to the power-up state
    kill_bot():
        change the bot image and mark it as dead
    reset_img():
        restore the bot's original image
    get_coord_to_maze_grid():
        convert pixel coordinates into maze grid coordinates
    can_reset():
        verify if the bot has returned to its spawn position
    rect:
        return a rectangle representing the bot position and size
    """
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
        """
        Check if movement is possible from a cell in a given direction.

        Args:
            cell: Integer representing the walls of the current maze cell.
            direction: Direction to check. Can be N, E, S or W.

        Returns:
            True if there is no wall blocking the given direction,
            otherwise False.
        """
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
        """
        Calculate a path from the bot's current position to its goal.

        The maze grid is obtained from the maze generator and the bot's
        pixel coordinates are converted into maze coordinates before
        running the BFS algorithm.
        """
        self.grid = self.maze.maze
        self.path = self.bfs(self.get_coord_to_maze_grid(
            (self.x, self.y)), (self.goal_coord)
        )

    def get_valid_cells(self, current_position: tuple[int, int]) -> list:
        """
        Get the cells that can be reached from a given maze position.

        Args:
            current_position: X and Y coordinates of the current cell.

        Returns:
            A list containing the available directions and the
            corresponding maze coordinates.
        """
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
        """
        Find a path between two maze cells using breadth-first search.

        Args:
            bot_coord: X and Y coordinates of the starting cell.
            goal_coord: X and Y coordinates of the target cell.

        Returns:
            A list of directions representing the shortest path, or
            None if the target cell cannot be reached.
        """
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
        """
        Calculate the bot's next position from its current path.

        The position is changed by the configured movement speed in
        the direction stored at the current path index.

        Returns:
            A tuple containing the movement direction and the next
            X and Y coordinates. If there is no path, the current
            position is returned with None as the direction.
        """
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
        """
        Move the bot to the next position in its current path.
        """
        direction, dx, dy = self.next_position()
        self.x, self.y = dx, dy
        self.current_direction = direction

    def recalculate_rote(
        self,
        bot_coord: tuple[int, int],
        goal_coord: tuple[int, int],
        respaw: bool = False
    ) -> None:
        """
        Recalculate the bot's path to a given goal or its spawn position.

        Args:
            bot_coord: Current bot coordinates in pixels.
            goal_coord: Target coordinates in pixels.
            respaw: If True, calculate a path back to the bot's spawn
                position instead of the given goal.
        """
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
        """
        Calculate a path that moves the bot away from the player.

        The available neighbouring cells are compared using their
        Manhattan distance from the player's position. The cell with
        the greatest distance is selected as the escape target.

        Args:
            player_cordintaes: Player coordinates in pixels.
        """
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
        """
        Change the bot image to the power-up image.

        Args:
            mlx: MLX wrapper used to load the image.
            mlx_ptr: Pointer to the MLX instance.
        """
        self.img, self.width, self.height = mlx.mlx_png_file_to_image(
            mlx_ptr,
            "src/models/assets/ghost_images/powerup.png"
        )

    def kill_bot(self, mlx: Mlx, mlx_ptr: Any) -> None:
        """
        Change the bot image to the dead image and mark it as dead.

        Args:
            mlx: MLX wrapper used to load the image.
            mlx_ptr: Pointer to the MLX instance.
        """
        self.img, self.width, self.height = mlx.mlx_png_file_to_image(
            mlx_ptr,
            "src/models/assets/ghost_images/dead.png"
        )
        self.dead = True

    def reset_img(self, mlx: Mlx, mlx_ptr: Any) -> None:
        """
        Restore the original image associated with the bot.

        Args:
            mlx: MLX wrapper used to load the image.
            mlx_ptr: Pointer to the MLX instance.
        """
        self.img, self.width, self.height = mlx.mlx_png_file_to_image(
            mlx_ptr, self.images[self.id % len(self.images)]
        )

    def get_coord_to_maze_grid(
        self,
        coord: tuple[int, int]
    ) -> tuple[int, int]:
        """
        Convert pixel coordinates into maze grid coordinates.

        Args:
            coord: X and Y coordinates in pixels.

        Returns:
            A tuple containing the X and Y coordinates of the
            corresponding maze cell.
        """
        x = (
            coord[0] - self.pixel_data["OFFSET_X"]
        ) // self.pixel_data["CELL_W"]
        y = (
            coord[1] - self.pixel_data["OFFSET_Y"]
        ) // self.pixel_data["CELL_H"]
        return (x, y)

    def can_reset(self) -> bool:
        """
        Check if the bot has returned to its spawn position.

        Returns:
            True if the bot is at its original spawn coordinates,
            otherwise False.
        """
        return (self.x, self.y) == (self.spam_x, self.spam_y)

    @property
    def rect(self) -> Rect:
        """
        Return the rectangle representing the bot.

        Returns:
            A Rect containing the bot's current position and dimensions.
        """
        return Rect(self.x, self.y, self.width, self.height)
