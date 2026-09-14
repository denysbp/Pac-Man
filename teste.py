from src.models.bots import Bot
from mazegenerator.mazegenerator import MazeGenerator
import os

os.system("clear")
maze = MazeGenerator((15, 15), 0)
ghost = Bot(img=None, img_width=1, img_height=None, spam_x = 2, spam_y = 3, maze=maze)
