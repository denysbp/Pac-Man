import json
from ..exceptions import LoaderError
from typing import Dict, Any

COMMENTS = (
    "#",
    "//"
)


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
                    "LIMITS: >= 14 <= 17."
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
        if any(key not in valid_keys for key in self.configs.keys()):
            missing = [
                k for k in valid_keys if k not in self.configs.keys()
            ]
            raise LoaderError(
                f"Missing keys {missing}."
            )
        if len(self.configs) != 9:
            raise LoaderError(
                "We detected unknown keys."
            )
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
        with open(self.path, "r+", encoding="UTF-8") as file:
            lines = file.readlines()
            if not lines:
                raise LoaderError(
                    "The provide file is empty."
                )
            json_str = self._split_comments(lines)
        self.configs = json.loads(json_str)
        self._ensure_values()


if __name__ == "__main__":
    try:
        loader = ConfigLoader(
            path="config.json"
        )
        loader.load_json()
        print(loader.configs)
    except LoaderError as e:
        print(e)
