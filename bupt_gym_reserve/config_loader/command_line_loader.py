from .base import ConfigLoader, GymConfig
import argparse


class CommandLineLoader(ConfigLoader):
    def load_config(self) -> GymConfig:
        parser = argparse.ArgumentParser(description='输入脚本所需的用户信息')
        parser.add_argument('--username', '-u', type=str,
                            help='登录用户名', required=False, dest='username')
        parser.add_argument('--password', '-p', type=str,
                            help='登录密码', required=False, dest='password')
        parser.add_argument('--sckey', '-k', type=str,
                            help='server酱的sckey', required=False, dest='sckey')
        parser.add_argument('--chance', '-c', type=int,
                            help='脚本实际运行的概率，默认为100', required=False, dest='chance')
        parser.add_argument('--config', '-f', type=int,
                            help='配置文件的路径，默认为"./config.json"', required=False, dest='config_path')
        args = parser.parse_args()
        config = GymConfig(args.username, args.password)
        if args.sckey is not None:
            config.notify_enabled = True
            config.sckey = args.sckey
        if args.chance is not None:
            config.chance = args.chance
        if args.config_path is not None:
            config.config_path = args.config_path
        return config
