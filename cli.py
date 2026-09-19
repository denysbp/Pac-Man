from src import (
    Render,
    ConfigLoader,
    alocate_levels,
    create_config,
    LoaderError
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
        data = ConfigLoader(path=argv[1])
        data.load_json()

        mlx = Mlx()
        _ , w, h = mlx.mlx_get_screen_size(
            mlx.mlx_init()
        )
        game = Render(
            w,
            h,
            alocate_levels(data),
            create_config(data)
        )
        game.run()
    except LoaderError as e:
        print(e)
    except ValueError as e:
        print(e)
    except Exception as e:
        print(e)