# -*- coding: UTF-8 -*-
"""
常量定义模块
包含所有API端点、URL、状态码等常量
"""

# API配置
API_BASE_URL = "https://api-xcx-qunsou.weiyoubot.cn"

# API端点
API_ENDPOINTS = {
    'pc_code': '/xcx/enroll_web/v1/pc_code',
    'pc_login': '/xcx/enroll_web/v1/pc_login',
    'userinfo': '/xcx/enroll/v1/userinfo',
    'user_history': '/xcx/enroll/v1/user/history',
    'req_detail': '/xcx/enroll/v1/req_detail',
    'enroll': '/xcx/enroll/v5/enroll',
    'extra_info': '/xcx/enroll/v1/extra_info',
}

# 请求头
HEADERS = {
    'login': {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'no-cache',
        'dnt': '1',
        'origin': 'https://p.baominggongju.com',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'sec-ch-ua': '"Microsoft Edge";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0'
    },
    'submit': {
        'authority': 'api-xcx-qunsou.weiyoubot.cn',
        'accept': '*/*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'content-type': 'application/json',
        'referer': 'https://servicewechat.com/wxfaa08012777a431e/1173/page-frame.html',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a13) XWEB/8555',
        'xweb_xhr': '1'
    }
}

# 活动状态
ACTIVITY_STATUS = {
    1: "进行中",
    2: "结束",
}

# 提交结果消息
SUCCESS_MESSAGES = ['', '提交次数超过限制', '活动期间，只允许提交1次']
FAILURE_MESSAGES = ['报名人数已满或项目数量不足', 'invalid parameter']

# 默认延迟时间（毫秒）
DEFAULT_DELAY_MS = 0

# 二维码图片路径
QR_CODE_PATH = './login.jpg'

# 个人页面URL
PERSONAL_PAGE_URL = 'https://ygxiuming.github.io/Lecture-registration/'
