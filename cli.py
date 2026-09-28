from src import (
    Render,
    ConfigLoader,
    alocate_levels,
    create_config,
    LoaderError,
    ScoreSpriteGenerator
)
from sys import argv, exit


def main() -> int:
    path = ""
    if len(argv) > 2:
        print(
            "Program usage: "
            "pac-man.py <file_name>.json"
        )
        exit(1)
    if len(argv) == 2:
        path = argv[1]
    try:
        points = ScoreSpriteGenerator()
        data = ConfigLoader(path=path)
        data.load_json()
        config = create_config(data)
        name = points.generate_for_value(
            config.points_per_ghost
        )
        w, h = 1920, 1080
        game = Render(
            w,
            h,
            alocate_levels(data),
            config,
            str(name)
        )
        game.run()
    except LoaderError as e:
        print(e)
    except ValueError as e:
        print(e)
    except Exception as e:
        print(f"Something when wrong: {e}")
    return 0
