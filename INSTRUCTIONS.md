### Running the game
```bash
python3 pac-man.py <config.json> or make run
```
The program only supports JSON files. If the loader detects a non-JSON file
(or a malformed one), it raises a `LoaderError`.

### Controls
| Key | Action |
|-----|--------|
| Arrow keys | Move the player |
| WASD | Move the player |
| 1 | Super speed |
| 2 | Invincibility |
| 3 | Extra lives |
| 4 | Skip level |
| 5 | Freeze bots |
| 6 | Intangibility |

## Configuration

The config file is a JSON file (path passed as a CLI argument, e.g.
`config.json`) loaded by `ConfigLoader`. Lines starting with `#` or `//` are
treated as comments and stripped before parsing, so the JSON file can contain
inline comments. `ConfigLoader.load_json()` reads the file, strips comments,
parses the JSON, and validates every field through `_ensure_values()`,
`_ensure_numbers()` and `_ensure_levels_values()`; any invalid value raises a
`LoaderError` with a descriptive message.

The file must contain **exactly** these 9 keys  extra or missing keys raise
a `LoaderError`:

| Key | Type | Description |
|-----|------|--------------|
| `highscore_filename` | `str` | Path/filename of the SQLite database used to store high scores |
| `lives` | `int` (≥ 1) | Starting number of player lives |
| `pacgum` | `int` | Number of small pellets ("pacgums") placed in each maze |
| `points_per_pacgum` | `int` | Points awarded for eating a small pellet |
| `points_per_super_pacgum` | `int` | Points awarded for eating a big/power pellet |
| `points_per_ghost` | `int` | Points awarded for eating a bot while powered up |
| `level` | `list[dict]` | One `{"width": int, "height": int}` entry per level each dimension must be `> 14` and `<= 17` |
| `level_max_time` | `int` | Time limit (seconds) allotted to clear a level |
| `seed` | `int \| null` | Seed passed to `mazegenerator`; a value `<= 0` is treated as `None` (random seed) |

None of the numeric values may be negative or boolean (booleans are
explicitly rejected even though `bool` is a subtype of `int` in Python).
There is no separate CLI-flag or environment-variable override all tuning
is done by editing the JSON config file passed on the command line.

Cell size (`CELL_W` / `CELL_H`) is **not** part of the config file: it is
computed at runtime from the window size and the current level's maze
dimensions (see Maze Generation below).