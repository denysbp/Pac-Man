from typing import Any


class LoaderError(Exception):
    """
    This class will be call when something went wrong with the loader
    """
    def __init__(self, *args: Any) -> None:
        super().__init__(*args)
