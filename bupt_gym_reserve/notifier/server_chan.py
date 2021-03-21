__all__ = (
    'SeverChanNotifier',
)

import json
import requests


class SeverChanNotifier:
    def __init__(self, sckey) -> None:
        self.config = {
            'sckey': sckey,
            'url': 'https://sc.ftqq.com/'
        }

    def send_msg(self, title: str, content: str) -> tuple:
        payload = {
            'text': title,
            'desp': content
        }
        resp = requests.post(url=f"{self.config['url']}{self.config['sckey']}.send", data=payload)
        if resp.status_code != 200:
            return (False, '请求服务器出错')
        json_resp = json.loads(resp.text)
        return (json_resp['errno'] == 0, json_resp['errmsg'])
