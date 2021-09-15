import requests
from ..config_loader import GymConfig
import json
import sys
from .magics import req_config
from bs4 import BeautifulSoup as bs
__all__ = (
    'GymSession',
)


class GymSession(requests.Session):
    def __init__(self, config: GymConfig) -> None:
        super().__init__()
        self.config = config
        # 最近一次登录结果
        self._login_flag = False
        # 尝试登录的次数
        self._login_attemption = 0
        self.cookie_path = config.cookie_path
        self.headers.update(req_config['headers'])
        self._recover_or_create_session()
        self.index_cache = None

    def save(self):
        print('正在保存session...')
        with open(self.cookie_path, 'w+') as foo:
            json.dump(self.cookies.get_dict(), foo)

    def has_login(self, force_request=False) -> bool:
        # 如果登录的flag为假 或者 用户目前没有尝试过登录
        # 则会请求访问index来检查是否登录
        # 否则返回缓存的login_flag
        if (self._login_attemption == 0 and not self._login_flag) or force_request:
            response_text = self.get(req_config['urls']['index']).text
            self._login_flag = '点击下方可用时间段进行预订' in response_text
            if self._login_flag:
                self.index_cache = response_text
        return self._login_flag

    def _recover_or_create_session(self):
        try:
            with open(self.cookie_path) as foo:
                # 存在cookie，直接从文件中加载
                cookies = json.load(foo)
                for k in cookies:
                    self.cookies.set(k, cookies[k])
                print('存在session，检测是否已经登录...')
                if self.has_login():
                    print('已经登录！')
                else:
                    print('用户未登录，正在尝试登录...')
                    self.cookies.clear()
                    self.login(self.config['username'], self.config['password'])
        except (json.decoder.JSONDecodeError, FileNotFoundError):
            # 不存在cookie，创建cookie并登录
            print('不存在session, 登录中...')
            self.login(self.config['username'], self.config['password'])

    # 返回登录成功状态
    def login(self, username: str, password: str) -> bool:
        login_session = self.get(req_config['urls']['index'], headers=req_config['headers'])
        pre_login_page = bs(login_session.content, "html.parser")
        lt = pre_login_page.find('input',{'name':'lt'})['value']
        execution = pre_login_page.find('input', {'name':'execution'})['value']
        if not username or not password:
            sys.stderr.write('用户名以及密码不能为空\n')
            sys.exit()
        payload = {
            'username': username,
            'password': password,
            'lt': lt,
            'execution': execution,
            '_eventId': 'submit',
            'rmShown' : 1
            # 'submit': '%E7%99%BB%E5%BD%95'
            # 'usertype': 0,
            # 'action': None
        }
        self.post(req_config['urls']['loginT'], data=payload)
        login_res = self.has_login()
        self._login_attemption += 1
        self._login_flag = login_res
        print('登录成功！'if login_res else '登录失败！请检查用户名/密码是否正确')
        return login_res
