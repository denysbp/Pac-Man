from src.models.bots import Bot
from mazegenerator.mazegenerator import MazeGenerator
import os

os.system("clear")
maze = MazeGenerator((15, 15), perfect=False, entry_cell=(0, 0), exit_cell=(10, 10), seed=1)
ghost = Bot(img=None, spam_x = 2, spam_y = 3, maze=maze, bot_id=2)
print(maze.shortest_path)
