from json.decoder import JSONDecodeError
from .base import ConfigLoader, GymConfig, create_config_from_json
import json
import os
from ..exception import ConfigException


class JsonLoader(ConfigLoader):
    def __init__(self, config_path='./config.json') -> None:
        self.config_path = config_path

    def load_status(self) -> bool:
        return os.path.exists(self.config_path)

    def load_config(self) -> GymConfig:
        try:
            with open(self.config_path, 'r') as foo:
                config = create_config_from_json(json.load(foo))
        except FileNotFoundError:
            raise ConfigException('JSON配置未找到')
        except JSONDecodeError:
            raise ConfigException('JSON配置格式有误，请仔细阅读说明文档')
        return config
