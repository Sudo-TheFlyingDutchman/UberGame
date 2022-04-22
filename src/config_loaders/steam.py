from yaml import safe_load
from pathlib import Path

from . import ConfigLoader

class SteamConfigLoader(ConfigLoader):
    @classmethod
    def is_public(cls):
        return False

    @classmethod
    def load(cls, path: Path):
        with open(str(path / Path('steam.yaml')), 'r') as steam:
            return safe_load(steam)
