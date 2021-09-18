# 北京邮电大学沙河校区健身房预约脚本

该脚本用于预约北京邮电大学沙河校区健身房，引用/使用请遵循 GPLv3 开源协议。

## 依赖

- Python 3.8.5 (开发环境)
- requests：发送 HTTP 请求
- BeautifulSoup4：解析 html 页面
- ExecJs：用于执行页面上的 JavaScript 脚本
- PyCryptoDome：AES 加密
- NodeJs：提供 JS 运行时
- Poetry：管理项目依赖

## 特性

- 高可用性，在大部分环境下均可部署使用
- 高可拓展性，方便二次开发
- (可选) 使用 Server 酱进行消息推送

## 更新日志 Changelog

**2020/11/25** 添加 [Server 酱](http://sc.ftqq.com/3.version)提示功能，添加概率启动功能(用于防止被服务器 ban 掉)

**2020/11/26** 解决十点无法预约的 bug

**2020/11/27** 现在如果发生预约失败，将会将失败的元素重新遍历一次进行预约；加入主页 cache，如果检测到已经登录，则会直接利用检测留下的页面进行预约的查询

**2021/3/28** 添加黑名单功能，现在可以用正则表达式匹配自己不想要的时段啦~

**2021/9/18** 修复json配置文件不生效的问题；使用poetry管理项目依赖

## 部署

可以使用校内或者校外的服务器进行部署，具体流程：

1. `git clone git@github.com:Hyiker/bupt-gym-reserve.git` 将代码仓库克隆到本地或者下载 zip 包
2. `cd bupt-gym-reserve` 进入项目文件夹
3. `pip install poetry && poetry install` 使用[poetry](https://python-poetry.org/)直接下载项目的所有依赖
4. `poetry run python main.py -u 信息门户用户名 -p 信息门户登录密码 -k server酱的SCKEY`
5. (可选)将脚本执行命令添加到`crontab`中

## 参数说明

### 命令行配置

|                命令行参数                |                                                               说明                                                               |
| :--------------------------------------: | :------------------------------------------------------------------------------------------------------------------------------: |
| --username -u (若使用 json 配置则可选) |                                                               学号                                                               |
| --password -p (若使用 json 配置则可选) |                                                           信息门户密码                                                           |
|           --sckey -k (可选)            |                                         server 酱提供的 SCKEY，如果不需要推送通知则留空                                          |
|           --chance -c (可选)           |                      输入一个整数 k，如果填写，则脚本只有 k% 的概率会实际运行，随机变量为离散的，默认为 100                      |
|           --config -f (可选)           |                                        json 配置文件的目录，默认为根目录下的 config.json                                         |
|          --blacklist -b (可选)           | 黑名单时段，使用正则表达式匹配例如我不想要任何时间的 6-7 的预约，便使用"\d{4}/\d{1,2}/\d{1,2}/1"，匹配的目标格式为`YYYY/m(m)/d(d)/p`，其中 p=1,2,3 |

### json 配置

如果根目录下存在 config.json，会自动读取该配置文件并且使用其中的配置(优先级低于命令行配置，留空的会被命令行配置覆盖)，
如果目录下不存在 config.json 文件，程序将根据命令行参数自动 dump 一份下来，如果希望禁止这样的行为，请自行注释`main.py`的`config.save()`

```json
{
    "username": "用户名(学号)",
    "password": "用户密码",
    "notify_enabled": true,
    "sckey": "Server酱的key",
    "cookie_path": "./cookie.json",
    "config_path": "./config.json",
    "chance": 80
}
```

以下一个用于演示的 example

```bash
python3 main.py -u 2019114514 -p 1919810 --dumpconf true -b "\d{4}/\d{1,2}/\d{1,2}/1"
```

## 免责声明

该脚本仅用于北京邮电大学校内学生交流学习使用，遵循 GPLv3 开源协议，本人不对脚本使用产生的后果负任何责任
