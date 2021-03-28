from typing import Tuple
from bupt_gym_reserve.config_loader.base import GymConfig
import time as timelib
import sys
from bupt_gym_reserve import PageFormatException, CommandLineLoader, \
    JsonLoader, SeverChanNotifier, ConfigException, merge_configs, GymSession, Reserver


def roll_the_dice(chance: int) -> bool:
    if chance == 100:
        return True
    import random
    random.seed(int(10*timelib.time()+114514))
    res = random.randint(0, 100)
    return chance >= res


def load_config() -> Tuple:
    command_line_loader = CommandLineLoader()
    config = command_line_loader.load_config()

    json_loader = JsonLoader(config_path=config.config_path)
    if not json_loader.load_status:
        json_config = None
        try:
            json_loader.load_config()
        except ConfigException as ce:
            sys.stderr.write(f'读取json配置文件出现错误：{ce}\n')
            sys.exit()
        merge_configs([config, json_config])
    return (json_loader, config)


if __name__ == '__main__':
    print('********** {} **********'.format(
        timelib.strftime('%Y-%m-%d %H:%M:%S', timelib.localtime(timelib.time())))
    )
    (json_loader, config) = load_config()
    print('正在摇D100... _(:з」∠)_')
    roll_result = roll_the_dice(config.chance)
    print('怎么又要干活o(￣ヘ￣o＃)' if roll_result else '好耶，是摸鱼时间！(๑•̀ㅂ•́)و✧')
    if not roll_result:
        sys.exit()

    notifier = SeverChanNotifier(sckey=config.sckey)
    session = GymSession(config=config)
    reserver = Reserver(config=config, session=session)
    reserves = list()
    try:
        reserves = reserver.get_reserves(index_cache=session.index_cache)
    except PageFormatException as e:
        sys.stderr.write(f'捕获到错误：{e.msg}\n')
        notifier.send_msg('预约出现错误', f'捕获到错误：{e.msg}')
        sys.exit()

    reservable = [_reserve for _reserve in reserves if _reserve.reservable]
    print(f'当前可预约有{len(reservable)} / {len(reserves)}个')
    if len(reservable) > 0:
        success_list, fail_list = reserver.reserve_all(reservable)
        if len(fail_list) != 0:
            print(f'失败{len(fail_list)}个，正在尝试重新预约')
            new_fail_list = list()
            for _reserve, _ in fail_list:
                new_fail_list.append(_reserve)
            sl, fl = reserver.reserve_all(new_fail_list)
            success_list += sl
            fail_list = fl
        if config.notify_enabled:
            title = f'成功预约{len(success_list)}个健身房时段，失败{len(fail_list)}个'
            content = '以下时段预约成功：'
            for suc in success_list:
                content += str(suc) + '   '
            content += '以下时段预约失败：'
            for failure, reason in fail_list:
                content += f'{str(failure)}+  失败原因：{reason}'
            if not notifier.send_msg(title, content):
                sys.stderr.write('推送消息至微信失败')
    else:
        print('无可用时段，退出中...')
    session.save()
    if json_loader.load_status:
        config.save()
        pass
