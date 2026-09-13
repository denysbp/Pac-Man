from src import Render
from mlx.mlx import Mlx

if __name__ == "__main__":
    mlx = Mlx()
    _ , w, h = mlx.mlx_get_screen_size(mlx.mlx_init())
    game = Render(w, h)
    game.run()