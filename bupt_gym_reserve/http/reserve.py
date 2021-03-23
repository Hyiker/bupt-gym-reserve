from .session import GymSession
from ..config_loader import GymConfig
from ..exception import PageFormatException
from bs4 import BeautifulSoup
import re
from Crypto.Cipher import AES
import base64
import execjs
import time as timelib
from .magics import period_list, error_reason, req_config
__all__ = (
    'Reserve',
    'Reserver'
)


class Reserve:
    def __init__(self, year: int, mon: int, day: int, period: int,
                 total: int, reserved: int, has_reserved: bool) -> None:
        self.year = year
        self.mon = mon
        self.day = day
        # 0, 1, 2
        self.period = period
        self.total = total
        self.reserved = reserved
        self.has_reserved = has_reserved
        self.reservable = (reserved < total) and not has_reserved

    def __str__(self) -> str:
        return f'''时间：{self.year}/{self.mon}/{self.day}\n时段：{period_list[self.period]}'''


class Reserver:
    def __init__(self, config: GymConfig, session: GymSession) -> None:
        self.config = config
        self.session = session

    def get_reserves(self, index_cache: str = None) -> list:
        reservation_list = list()
        if index_cache is None:
            index_page = self.session.get(req_config['urls']['index']).text
        else:
            index_page = index_cache
        index_soup = BeautifulSoup(index_page, 'html.parser')
        lis = index_soup.select('.collapsible.popout>li')
        for li in lis:
            body = li.select_one('.collapsible-body')
            date = body['id']
            try:
                year = int(date[0:4])
                mon = int(date[4:6])
                day = int(date[6:len(date)])
            except ValueError:
                raise PageFormatException(msg=f'无法正确从文本 "{date}" 中获取预约日期')
            for i, time in enumerate(body.select('.timeBox')):
                right_text = time.select_one('.rightBox').get_text().strip()
                has_reserved = '已预约' in right_text
                # 寻找文本中出现的所有数字
                reserve_match = re.findall(r'\d+', right_text)
                if len(reserve_match) < 2:
                    raise PageFormatException(msg=f'无法正确从文本 "{right_text}" 中获取预约人数')
                reserved = reserve_match[0]
                total = reserve_match[1]
                reservation_list.append(Reserve(year, mon, day, i + 1, total, reserved, has_reserved))
        return reservation_list

    def reserve(self, reservable: Reserve) -> str:
        print(f'{reservable}')
        payload = {'blob': self._get_blob(reservable.year, reservable.mon,
                                          reservable.day, reservable.period, int(round(timelib.time()*1000)))}

        status = self.session.post(req_config['urls']['order'], data=payload).text.rstrip()
        if status == '1':
            print('预约成功！')
        elif status in error_reason:
            print(f'预约失败！失败理由：{error_reason[status]}')
        else:
            print(f'服务器异常，返回code：{status}')
        return status.rstrip()

    def reserve_all(self, reserve_list: list) -> tuple:
        success_list = list()
        fail_list = list()
        for i, r in enumerate(reserve_list):
            print(f'正在预约第{i+1}个...')
            suc = self.reserve(r)
            if suc == '1':
                success_list.append(r)
            else:
                fail_list.append((r, error_reason[suc] if suc in error_reason else '未知错误'))
            # 休眠1.5秒，以防服务器认定为trash
            timelib.sleep(1.5)

        return (success_list, fail_list)

    def _get_blob(self, year: int, mon: int, day: int, period: int, time: int):
        raw = execjs.eval('''JSON.stringify(
                    {{
                        date: '{}',
                        time: '{}',
                        timemill: {}
                    }}
                )'''.format('{:04d}{:02d}{:02d}'.format(year, mon, day), period, time))
        oraw = ''
        i = 0
        while i < len(raw):
            oraw += raw[i]+raw[len(raw)-1-i]
            i += 1

        def pad(m):
            return m+chr(16-len(m) % 16)*(16-len(m) % 16)
        oraw = pad(oraw).encode('utf-8')
        ekey = self.config['username'] * 2
        key = ekey[0:16].encode('utf-8')
        iv = ekey[2:18].encode('utf-8')
        cipher = AES.new(key, AES.MODE_CBC, iv)
        return base64.b64encode(bytes(cipher.encrypt(oraw)))
