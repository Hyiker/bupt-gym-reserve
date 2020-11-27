__all__ = (
    'SeverChanNotifier',
)

import json
import requests


class SeverChanNotifier:
    def __init__(self, sckey) -> None:
        self.config = {
            'sckey': sckey,
            'url': 'https://sc.ftqq.com/SCU129706T96bb814b7a12079eec2691ea2cd563055fbdf1566ba58.send'
        }

    def send_msg(self, title: str, content: str) -> tuple:
        payload = {
            'text': title,
            'desp': content
        }
        resp = requests.post(url=self.config['url'], data=payload)
        if resp.status_code != 200:
            return (False, '请求服务器出错')
        json_resp = json.loads(resp.text)
        return (json_resp['errno'] == 0, json_resp['errmsg'])
