import json
from ..exceptions import LoaderError
from typing import Dict, Any
from time import sleep

COMMENTS = (
    "#",
    "//"
)

DEFAULT = {
    "highscore_filename": "pacman.db",
    "lives": 3,
    "pacgum": 80,
    "points_per_pacgum": 10,
    "points_per_super_pacgum": 50,
    "points_per_ghost": 250,
    "level": [
        {
            "width": 15,
            "height": 15
        },
        {
            "width": 15,
            "height": 16
        },
        {
            "width": 16,
            "height": 16
        },
        {
            "width": 16,
            "height": 17
        },
        {
            "width": 17,
            "height": 15
        },
        {
            "width": 16,
            "height": 16
        },
        {
            "width": 17,
            "height": 17
        },
        {
            "width": 18,
            "height": 18
        },
        {
            "width": 19,
            "height": 19
        },
        {
            "width": 20,
            "height": 20
        }
    ],
    "level_max_time": 120,
    "seed": 2
}

VALID_KEYS = {
    "highscore_filename",
    "lives",
    "pacgum",
    "seed",
    "level_max_time",
    "points_per_pacgum",
    "points_per_super_pacgum",
    "points_per_ghost",
    "level"
}


class ConfigLoader:
    """
    Responsible to load the JSON config file

    Attributes
    ____________
    path: str
        represent the path for the provide file
    configs: dict
        store the processed values from the config file

    Methods
    ____________
    _split_comments():
        parse lines ignoring lines that start with comments
    _ensure_levels_values():
        parse the levels dicts to ensure its well formated
    _ensure_numbers():
        verify if any of the values are bool
    _ensure_values():
        verify if the values are int objects
    load_json():
        load the file, call the private parser methods and save the configs
    """
    def __init__(
        self,
        *,
        path: str
    ) -> None:
        """
        Before creating the class the constructor will ensure it's a JSON file
        Args:
            path: str
                the provider path for the config file
        """
        if path:
            if '.' not in path:
                raise LoaderError(
                    "You're supposed to pass a file."
                )
            _, type = path.split(".", 1)
            if type != "json":
                raise LoaderError(
                    f"Expecting 'json' got '{type}'."
                )
        self.path: str = path
        self.configs: Dict[str, Any]
        self.keys_received: set[str] = set()

    def _split_comments(self, lines: list[str]) -> str:
        """
        Responsible for detect line that start with comments.
        This method use a list containing the comments types
        and if a line star with it, we ignore before concatenate.
        Args:
            lines: list
                List containing each line of the provider config file
        Returns:
            The str containing only valid lines
        """
        json_str = ""
        for line in lines:

            if line.strip().startswith(COMMENTS):
                continue

            if any(
                line.split(
                    ":", 1)[0].replace(
                    '"', "").strip() == k for k in VALID_KEYS
                    ):
                key = line.split(":", 1)[0].replace('"', "").strip()

                if key in self.keys_received:
                    print(
                        f"Warning: Duplicade key '{key}',"
                        "the program will receive the first key showed!"
                    )
                    continue
                self.keys_received.add(key)
            json_str += line

        return json_str

    def _ensure_levels_values(self) -> None:
        """
        Verify if the level config follow the standard.

        Returns:
            None.
        """
        for config in self.configs["level"]:
            if not isinstance(config, dict):
                raise LoaderError(
                    f"Expecting 'dict' got '{config.__class__.__name__}'."
                )
            height, width = config["height"], config["width"]
            if height <= 14 or width <= 14:
                raise LoaderError(
                    "Error: The maze must to has limits greater the 14!"
                )
            if height >= 30 or width >= 30:
                raise LoaderError(
                    "Error: The maze must to has limits greater the 14!"
                )
        return

    def _ensure_numbers(self) -> None:
        """
        Verify if it's a real number and not a bool
        Returns:
            None.
        """
        all_numbers = [
            self.configs["lives"],
            self.configs["pacgum"],
            self.configs["level_max_time"],
            self.configs["points_per_pacgum"],
            self.configs["points_per_super_pacgum"],
            self.configs["points_per_ghost"],
        ]
        if self.configs["seed"] <= 0:
            self.configs["seed"] = None
        if isinstance(self.configs["seed"], bool):
            raise LoaderError(
                "WE DON'T ACCEPT BOOLEAN."
            )
        if any(number > 1000 for number in all_numbers):
            print("::::BUGS MAY OCCUR DURING GRAPHICAL VISUALIZATION::::")
            sleep(1)
        if any(number < 0 for number in all_numbers):
            raise LoaderError(
                "WE DON'T ACCEPT NEGATIVE VALUES."
            )

        if any(isinstance(number, bool) for number in all_numbers):
            raise LoaderError(
                "WE DON'T ACCEPT BOOLEAN."
            )

        if self.configs["lives"] == 0:
            raise LoaderError(
                "Live must be >= 1, How can you play with 0 lives?"
            )

    def _ensure_values(self) -> None:
        """The parser, ensure if all the values are correct for the keys."""
        valid_keys = [
            "highscore_filename",
            "lives",
            "pacgum",
            "points_per_pacgum",
            "points_per_super_pacgum",
            "points_per_ghost",
            "level",
            "level_max_time",
            "seed"
        ]
        if any(key for key in valid_keys if key not in self.configs.keys()):
            missing = [
                k for k in valid_keys if k not in self.configs.keys()
            ]
            for k in missing:
                value = DEFAULT[k]
                print(f"Missing {k} using default: {value}")
                self.configs[k] = value
        if len(self.configs) != 9:
            invalids = [
                k for k in self.configs.keys() if k not in valid_keys
            ]
            print(f"We detected unknown keys. {invalids}")
            print("::::Rejected with sucess:::::")
        if not isinstance(self.configs["highscore_filename"], str):
            raise LoaderError(
                "Expecting 'str' got "
                f"'{self.configs['highscore_filename'].__class__.__name__}'."
            )
        if not isinstance(self.configs["lives"], int):
            raise LoaderError(
                "Expecting 'int' got "
                f"'{self.configs['lives'].__class__.__name__}'"
            )
        if not isinstance(self.configs["pacgum"], int):
            raise LoaderError(
                "Expecting 'int' got "
                f"'{self.configs['pacgum'].__class__.__name__}'"
            )
        if not isinstance(self.configs["points_per_pacgum"], int):
            raise LoaderError(
                "Expecting 'int' got "
                f"'{self.configs['points_per_pacgum'].__class__.__name__}'"
            )
        if not isinstance(self.configs["points_per_super_pacgum"], int):
            erro = self.configs['points_per_super_pacgum']
            raise LoaderError(
                "Expecting 'int' got "
                f"'{erro.__class__.__name__}'"
            )
        if not isinstance(self.configs["points_per_ghost"], int):
            raise LoaderError(
                "Expecting 'int' got "
                f"'{self.configs['points_per_ghost'].__class__.__name__}'"
            )
        if not isinstance(self.configs["level_max_time"], int):
            raise LoaderError(
                f"Expecting 'int' got "
                f"'{self.configs['level_max_time'].__class__.__name__}'"
            )
        if not self.configs["level"]:
            raise LoaderError("Error: Level cannot be empty!")
        if not isinstance(self.configs["level"], list):
            raise LoaderError(
                "Expecting 'int' got "
                f"'{self.configs['level'].__class__.__name__}'"
            )
        self._ensure_numbers()
        if not isinstance(self.configs["seed"], (int, type(None))):
            raise LoaderError(
                "Expecting 'int' got "
                f"'{self.configs['seed'].__class__.__name__}'"
            )
        self._ensure_levels_values()

    def load_json(self) -> None:
        """Open the config file and validate the args."""
        if self.path:
            with open(self.path, "r+", encoding="UTF-8") as file:
                lines = file.readlines()
                if lines:
                    json_str = self._split_comments(lines)
                    self.configs = json.loads(json_str)
                else:
                    self.configs = {}
        else:
            self.configs = {}
        self._ensure_values()


if __name__ == "__main__":
    try:
        loader = ConfigLoader(
            path="config.json"
        )
        loader.load_json()
    except LoaderError as e:
        print(e)
