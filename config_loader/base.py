__all__ = (
    'GymConfig',
    'ConfigLoader'
)


from abc import ABCMeta, abstractmethod
import json


class GymConfig(dict):
    def __setattr__(self, name: str, value: any) -> None:
        super().__setattr__(name, value)
        self[name] = value

    def __init__(self, username: str, password: str, notify_enabled: bool = False, sckey: str = '', chance: int = 100) -> None:
        super(GymConfig, self).__init__()
        self.username = username
        self.password = password
        self.notify_enabled = notify_enabled
        self.sckey = sckey
        self.cookie_path = './cookie.json'
        self.config_path = './config.json'
        self.chance = chance

    def save(self):
        '''
            将配置文件保存回文件中
            :param path:保存的目录
        '''
        with open(self.config_path, 'w+') as foo:
            json.dump(self, foo)


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
