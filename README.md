*This project has been created as part
of the 42 curriculum by deferrei, dosorio-.*

<h1 style="text-align:center;">PAC MAN</h1>

## Description

This project is a Pac-Man clone written in Python, built on top of an MLX-style
(minilibx) graphics library. The player navigates procedurally generated mazes,
eats pellets/mobs, and must avoid (or be avoided by) bots that hunt using
pathfinding. The goal is to reproduce the classic Pac-Man gameplay loop 
movement, collision, power-ups, levels, and scoring  while exploring low-level
graphics rendering and AI-driven ghost behavior.

Core gameplay features:
- Player movement with arrow keys and wall/screen-boundary collision detection
- Mob-eating mechanics
- Bots (ghosts) that move via BFS pathfinding toward the player
- A power-up ("super pac") that lets the player temporarily eat bots, sending
  them back to their spawn point
- Multiple levels, each with a freshly generated maze
- A start screen with a name-entry field and a persisted list of high scores

## Instructions

### Requirements
- Python 3.x
- `mazegenerator` package (A-Maze-ing)
- MLX / minilibx-style Python bindings used for rendering
- `Pillow` (used by the score-sprite generator)
- `sqlite3` (standard library, used for the high-score database)

### Installation
```bash
git clone <https://github.com/denysbp/Pac-Man>
cd Pac-Man
make run
```

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

## Highscore

High scores are persisted in a SQLite database (`data_base/db.py`,
`DATA_BASE` class), whose file path comes from the `highscore_filename` config
key. On startup, `Render.__init__` creates the `player` table if it doesn't
exist (`id`, `name`, `score`) and loads the current scores.

- **Persistence**: a `player` SQL table, one row per name.
- **Insert/update logic**: `insert_on_table()` looks up the existing scores
  first  if a row with the same name already exists and the new score is
  higher, it updates that row (`update_score()`); otherwise it inserts a new
  row. A `skip` flag (set when the entered name is blank, defaulting to
  `"UNKNOWN"`) bypasses the update check and always inserts.
- **Ordering / limit**: `get_scores()` runs
  `SELECT name, score FROM player ORDER BY score DESC LIMIT 10`, so only the
  top 10 entries are ever fetched and displayed.
- **Display**: the start screen's high-score view (`Render.high_scores()`)
  draws each `(name, score)` pair with `mlx_string_put`, formatted as
  `"name - score"`.
- **Why SQLite**: it avoids any external DB dependency (single file,
  stdlib `sqlite3`) while still giving simple querying/sorting for the
  top-10 list, and needs no extra service running alongside the game.

## Maze Generation

Mazes are produced using the assigned **A-Maze-ing** package
(`mazegenerator.mazegenerator.MazeGenerator`). At the start of each level,
`Render.start_level()` instantiates a new `MazeGenerator((width, height),
seed=self.data.seed)` and calls `.generate()`, so a fresh maze is generated
per level using that level's `width`/`height` from the config's `level` list
and the global `seed` config value (or a random seed if `seed` is `None`).

- The generated maze is exposed as `maze.maze`, a 2D grid where each cell is
  an integer bitmask of blocked directions: `N=1`, `E=2`, `S=4`, `W=8`
  (a cell value combining several of these means several walls are present).
  A special value of `15` marks cells that form the "42" logo drawn inside
  the maze (see `fill_42()` / `find_spawn_below_42()`).
- Because maze dimensions differ per level, `calcule_maze_dimetions()`
  recomputes `CELL_W`/`CELL_H` from the window size and the new
  `maze_width`/`maze_height` on every `start_level()` call, then derives the
  gum positions, the four "big gum"/bot-spawn corners, and the player's spawn
  point (just below the "42" structure) from the new grid.
- Small gum ("pacgum") positions are chosen by picking `data.pacgum` random
  walkable cells from the maze plus the four corner ("big gum") positions;
  bots spawn at those same four corners.

## Implementation

Technical summary:
- **Rendering**: an MLX (minilibx-style) wrapper (`Mlx`) is used to draw the
  maze, player, bots, and UI text/images directly into an off-screen image
  buffer (`Memory`), which is then blitted to the window each frame
  (`blip()`/`frames()`). Low-level pixel/line drawing (`put_pixel`,
  `drawlineH`, `drawlineV`, `blit_into_buffer`) lives in `src/helps.py`.
- **Config loading**: `ConfigLoader` reads and validates the JSON config
  (see Configuration above); `create_config()`/`alocate_levels()` convert the
  raw dict into typed `ConfigData`/`Level` dataclasses used by the rest of
  the game.
- **Player**: a `Player` class tracks x/y position, movement direction,
  animation frame index, and lives, and exposes a computed `Rect` property
  used for bounding-box collision checks against walls and gums
  (`hit_gum()`).
- **Bots (ghosts)**: each `Bot` computes a path to the player using BFS
  (`bfs()`/`call_bfs()`) over the maze grid. Movement along that path is
  interpolated in pixels via a `BOT_SPEED` step counter (`bot.pixel`) rather
  than jumping cell-to-cell, so motion appears smooth. When the player is
  powered up, bots instead flee using `scape()`, which picks the reachable
  neighboring cell with the greatest Manhattan distance from the player.
  Collision between the player and bots is checked via
  `check_bot_player_collision()` in `move_bots()`.
- **Power-up ("super pac")**: eating a big gum flips `self.super_pac` on for
  `time_super_pac` (8) seconds; while active, bots flee and can be "killed"
  (`kill_bot()`), awarding `points_per_ghost` and sending them back to their
  spawn after a `BOT_TIME_DEAD` (5s) respawn timer.
- **Score persistence**: handled by `DATA_BASE` (see Highscore above);
  `ScoreSpriteGenerator` additionally renders numeric score pop-ups
  (`+<value>`) as small bitmap sprites using a hand-rolled 3x5 pixel font.
- **Level transitions**: `start_level()` resets per-level bot state
  (`bot.i`, `bot.pixel`, `bot.path`, `bot.dead`) and reassigns
  `bot.maze` / `bot.pixel_data`, then recomputes BFS paths via `call_bfs()`.
  The render buffer is cleared (`clear_buffer()`) on level transition to avoid
  stale frames.
- **Pause/resume**: `pause_game()`/`resume_game()` snapshot and restore the
  remaining level time (`level_deadline`) so the countdown timer doesn't lose
  time spent paused.
- **Debug/cheat keys**: keys `1`–`6` toggle speed boost, invincibility, an
  extra life, a level skip, frozen bots, and intangibility respectively
  (handled in `controls()`), each flashing a small power-up icon.

## General Software Architecture

```
pac-man.py                 # entry point (reads config path arg, builds Render, calls run())
src/
├── helps.py                # put_pixel, drawlineH/V, blit_into_buffer, colision (low-level drawing/collision)
├── exceptions/
│   └── exceptions.py        # LoaderError
├── loader/
│   ├── loader.py             # ConfigLoader (JSON config loading + validation)
│   └── points.py             # ScoreSpriteGenerator (3x5 pixel-font score sprites)
├── data_base/
│   └── db.py                 # DATA_BASE (SQLite high-score persistence)
├── models/
│   ├── metadata.py           # ConfigData, Level, Memory, Rect, alocate_levels(), create_config()
│   ├── configs.py            # RIGHT/LEFT/TOP/DOWN player animation-frame path lists
│   ├── player.py              # Player class (position, animation, Rect, hit_gum())
│   └── bots.py                # Bot class (BFS pathfinding, movement, scape(), dead/spawn state)
└── render/
    └── render.py              # Render class: game loop, menus, input, drawing, scoring
```

Relationships (high level):
- `pac-man.py` loads the config via `ConfigLoader`, builds `ConfigData`/
  `Level` objects, and hands them to `Render`, which owns the game loop.
- `Render` creates one `Player` and four `Bot` instances, and asks
  `mazegenerator.MazeGenerator` for a new maze at the start of each level.
- `Render` reads `Player`/`Bot` state each frame to draw the scene
  (`draw_board()`, `frames()`) and detect collisions (`check_colision()`,
  `check_bot_player_collision()`).
- `Render` also owns the `DATA_BASE` instance used to load/save high scores,
  and drives the start screen / name-entry UI (`start_screen()`,
  `get_user_name()`).

## Resources

> - [MLX / minilibx documentation](https://harm-smits.github.io/42docs/libs/minilibx)
> - [Pac-Man ghost-AI article consulted](https://aighost.co.uk/how-pac-man-ghost-ai-works-the-classic-chase-algorithms/)
> - [Pac-Man Dowload](https://denysbp.itch.io/pac-man42)
> - [Signal documentation](https://docs.python.org/3/library/signal.html)

### AI usage
> AI was used 0% as a code generator, but rather as an advisor, in terms of optimization.

## Project Management

> - The development responsibilities were divided between the two members.
   according to the main components of the project.
> - Each member was responsible for implementing and testing their
   own changes before submitting them for review.
> - [FOLDER](./project_management)