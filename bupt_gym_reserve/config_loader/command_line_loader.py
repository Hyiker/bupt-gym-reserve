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
        parser.add_argument('--dumpconf', '-d', type=bool,
                            help='是否保存配置文件，默认为否', required=False, dest='dumpconf')
        parser.add_argument('--blacklist', '-b', type=str,
                            help='不需要预约的时段，使用正则匹配，格式如year/mon/day/period', required=False, dest='blacklist')
        args = parser.parse_args()
        config = GymConfig(args.username, args.password)
        if args.sckey is not None:
            config.notify_enabled = True
            config.sckey = args.sckey
        if args.chance is not None:
            config.chance = args.chance
        if args.config_path is not None:
            config.config_path = args.config_path
        if args.dumpconf is not None:
            config.dumpconf = args.dumpconf
        if args.blacklist is not None:
            config.blacklist = args.blacklist
        return config
