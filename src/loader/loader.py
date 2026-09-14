import json
from ..exceptions import LoaderError
from typing import Dict, Any

COMMENTS = (
    "#",
    "//"
)

# ESTA CLASSE FAZ O LOADER DAS CONFIG DO JSON FILE
class ConfigLoader:
    def __init__(
        self,
        *,
        path: str
    ):
        _, type = path.split(".", 1)
        if type != "json":
            raise LoaderError(
                f"Expecting 'json' got '{type}'."
            )
        self.path: str = path
        self.configs: Dict[str, Any]

    # RESPONSAVEL POR REMOVER COMENTARIOS DAS LINHAS
    def _split_comments(self, lines: str) -> str:
        json_str = ""
        for line in lines:
            if line.strip().startswith(COMMENTS):
                continue
            json_str += line
        return json_str

    # ELE VERIFICA SE CADA HEIGHT E WIDTH SAO NUMEROS
    def _ensure_levels_values(self) -> None:
        for config in self.configs["level"]:
            if not isinstance(config, dict):
                raise LoaderError(
                    f"Expecting 'dict' got '{
                        config.__class__.__name__
                    }'."
                )
            height, width = config["height"], config["width"]
            if height <= 14 or width <= 14:
                raise LoaderError(
                    "LIMITS: >= 14 <= 17."
                )
        return True

    # VERIFICA SE TODOS NUMEROS SAO POSITIVOS E VALIDOS
    def _ensure_numbers(self) -> None:
        all_numbers = [
            self.configs["lives"],
            self.configs["pacgum"],
            self.configs["level_max_time"],
            self.configs["points_per_pacgum"],
            self.configs["points_per_super_pacgum"],
            self.configs["points_per_ghost"],
        ]
        if self.configs["seed"] < 0:
            self.configs["seed"] = None
        if self.configs["seed"] in (True, False):
            raise LoaderError(
                "WE DON'T ACCEPT BOOLEAN."
            )
        if any(number < 0 for number in all_numbers):
            raise LoaderError(
                f"WE DON'T ACCEPT NEGATIVE VALUES."
            )

        if any(isinstance(number, bool) for number in all_numbers):
            raise LoaderError(
                "WE DON'T ACCEPT BOOLEAN."
            )


    # VALIDA TODAS OS VALORES
    def _ensure_values(self) -> None:
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
                f"We detected unknown keys."
            )
        if not isinstance(self.configs["highscore_filename"], str):
            raise LoaderError(
                f"Expecting 'str' got '{
                    self.configs["highscore_filename"].__class__.__name__
                }'."
            )
        if not isinstance(self.configs["lives"], int):
            raise LoaderError(
                f"Expecting 'int' got '{
                    self.configs["lives"].__class__.__name__
                }'"
            )
        if not isinstance(self.configs["pacgum"], int):
            raise LoaderError(
                f"Expecting 'int' got '{
                    self.configs["pacgum"].__class__.__name__
                }'"
            )
        if not isinstance(self.configs["points_per_pacgum"], int):
            raise LoaderError(
                f"Expecting 'int' got '{
                    self.configs["points_per_pacgum"].__class__.__name__
                }'"
            )
        if not isinstance(self.configs["points_per_super_pacgum"], int):
            raise LoaderError(
                f"Expecting 'int' got '{
                    self.configs["points_per_super_pacgum"].__class__.__name__
                }'"
            )
        if not isinstance(self.configs["points_per_ghost"], int):
            raise LoaderError(
                f"Expecting 'int' got '{
                    self.configs["points_per_ghost"].__class__.__name__
                }'"
            )
        if not isinstance(self.configs["level_max_time"], int):
            raise LoaderError(
                f"Expecting 'int' got '{
                    self.configs["level_max_time"].__class__.__name__
                }'"
            )
        if not isinstance(self.configs["level"], list):
            raise LoaderError(
                f"Expecting 'int' got '{
                    self.configs["level"].__class__.__name__
                }'"
            )
        self._ensure_numbers()
        if not isinstance(self.configs["seed"], (int, type(None))):
            raise LoaderError(
                f"Expecting 'int' got '{
                    self.configs["seed"].__class__.__name__
                }'"
            )
        self._ensure_levels_values()

    # DEPOIS DE VALIDAR SE TUDO DER CERTO ELE SALVA OS MAMBOS
    def load_json(self) -> None:
        with open(self.path, "r+", encoding="UTF-8") as file:
            lines = file.readlines()
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
