from utils.module_map import ModuleMap
from typing import Dict, Any
from abc import ABC, abstractmethod
from pathlib import Path


class ConfigLoader(ABC):
    def __init__(self, config_dict):
        super(ConfigLoader, self).__init__()

        self._config_dict = config_dict

    @classmethod
    @abstractmethod
    def is_public(cls):
        return True

    @classmethod
    @abstractmethod
    def load(cls, path) -> 'ConfigLoader':
        ...

    @abstractmethod
    def __getitem__(self, item):
        return self._config_dict[item]

    def __setitem__(self, key, value):
        pass

    def __delitem__(self, key):
        pass


class ConfigsMap:
    CONFIG_PATH = Path('config')
    PRIVATE_CONFIG_PATH = Path('private_configs')
    loaded_configs: Dict[str, ConfigLoader] = {}

    class ConfigLoadersMap(ModuleMap, base_class=ConfigLoader, package=__package__, file=__file__):
        pass

    def __class_getitem__(cls, item):
        if item in cls.loaded_configs.keys():
            return cls.loaded_configs[item]

        return cls._setup_config(item)

    @classmethod
    def _setup_config(cls, item) -> ConfigLoader:
        config_loader_cls = cls.ConfigLoadersMap[item][0]
        config_loader = config_loader_cls.load(cls.CONFIG_PATH if config_loader_cls.is_public()
                                                else cls.CONFIG_PATH / cls.PRIVATE_CONFIG_PATH)

        cls.loaded_configs[item] = config_loader
        return config_loader