__all__ = (
    'GymConfig',
    'ConfigLoader',
    'merge_configs',
    'create_config_from_json',
)


from abc import ABCMeta, abstractmethod
import json
from dataclasses import dataclass


@dataclass
class GymConfig(dict):
    username: str = None
    password: str = None
    notify_enabled: bool = False
    sckey: str = '',
    chance: int = 100
    dumpconf: bool = False
    blacklist: str = None
    cookie_path: str = './cookie.json'
    config_path: str = './config.json'

    def __setattr__(self, name: str, value: any) -> None:
        super().__setattr__(name, value)
        self[name] = value

    def save(self):
        '''
            将配置文件保存回文件中
            :param path:保存的目录
        '''
        with open(self.config_path, 'w+') as foo:
            json.dump(self, foo)
        print('正在保存配置文件...')


def create_config_from_json(json_dict: dict) -> GymConfig:
    config = GymConfig()
    for key in json_dict:
        setattr(config, key, json_dict[key])


def merge_configs(configs: list) -> GymConfig:
    '''
        合并多份配置文件，遵循先来后到
        真值优先的原则
    '''
    if len(configs) == 0:
        return None
    ret = configs[0]
    for i in range(1, len(configs)):
        for k in ret:
            setattr(ret, k, ret[k] if ret[k] else configs[i][k])
    return ret


class ConfigLoader(metaclass=ABCMeta):
    @abstractmethod
    def load_config(self) -> GymConfig:
        '''
            加载配置文件
            :return 配置文件
        '''
