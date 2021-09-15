__all__ = (
    'req_config',
    'period_list',
    'error_reason',
)
req_config = {
    'headers': {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
        'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.04280.66 Safari/537.36',
        'accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
    },
    'urls': {
        'index': 'https://gym.byr.moe/index.php',
        # Original login page outdated
        # 'login': 'https://gym.byr.moe/login.php',
        'order': 'https://gym.byr.moe/newOrder.php',
        # Updated new login site Sep15
        'loginT': 'https://auth.bupt.edu.cn/authserver/login?service=https%3A%2F%2Fgym.byr.moe%2Fcaslogin.php%3FredirectUrl%3Dhttps%253A%252F%252Fgym.byr.moe%252Findex.php'
    }
}

period_list = ('', '18:40 - 19:40', '19:40 - 20:40', '20:40 - 21:40')
error_reason = {
    '1': '预约成功',
    '2': '非法请求！',
    '3': '本时间段人数已满!',
    '4': '您已预约本时段健身房!',
    '5': '参数错误!请勿作死!',
    '6': '近两周内有不良预约记录!请反省',
    'dont spam': '服务器将访问识别为垃圾信息'
}
