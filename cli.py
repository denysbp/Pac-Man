from src import (
    Render,
    ConfigLoader,
    alocate_levels,
    create_config,
    LoaderError,
    ScoreSpriteGenerator
)
from mlx.mlx import Mlx
from sys import argv, exit

def main():
    if len(argv) != 2:
        print(
            "Program usage: "
            "pac-man.py <file_name>.json"
        )
        exit(1)
    try:
        points = ScoreSpriteGenerator()
        data = ConfigLoader(path=argv[1])
        data.load_json()
        config = create_config(data)
        name = points.generate_for_value(
            config.points_per_ghost
        )
        mlx = Mlx()
        _ , w, h = mlx.mlx_get_screen_size(
            mlx.mlx_init()
        )
        game = Render(
            w,
            h,
            alocate_levels(data),
            config,
            name._str
        )
        game.run()
    except LoaderError as e:
        print(e)
    except ValueError as e:
        print(e)
    except Exception as e:
        print(e)