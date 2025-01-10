# -*- coding: UTF-8 -*-
'''
@File    ：method.py
@IDE     ：PyCharm 
@Author  ：修明
@Email   ：lzmpt@qq.com
@Date    ：2024/12/25 0025 21:30 
@Detail  ：请求执行函数
'''
import hashlib
import json
import random
import string
import time
import requests

base_url = "https://api-xcx-qunsou.weiyoubot.cn"

login_headers = {
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
        }

def get_login_code_image():
    '''
    获取登录验证的二维码及二维码对应的唯一标识符code
    Returns:code , qrcode
    code: 二维码的唯一标识符
    qrcode: 二维码的base64编码格式
    '''
    # url = config.api_prod + config.Config['api_login_code']
    url = f"{base_url}/xcx/enroll_web/v1/pc_code"
    response = requests.request("GET", url, headers=login_headers)
    response_data = json.loads(response.text)
    if response.status_code == 200:
        code = response_data['data']['code']
        qrcode = response_data["data"]["qrcode"]
        return code, qrcode
    else:
        return None, None

def get_login_token(code):
    '''
    获取网页登录token
    Args:
        code: 二维码的唯一标识符

    Returns: token
    token : 用户登录凭证
    '''
    # url = config.api_prod + config.Config['api_pc_login']
    url = f"{base_url}/xcx/enroll_web/v1/pc_login"
    response = requests.request("GET",
                            url,
                            params={"code": code, "source": "h5"},
                            headers=login_headers)
    response = json.loads(response.text)
    msg = response["msg"]
    if msg != 'ok':
        return None
    else:
        token = response['data']['access_token']
    return token

def get_history_registration(token: str):
    '''
    获取用户浏览过的历史讲座
    Args:
        token: 用户登录凭证

    Returns: 历史讲座信息
    '''
    # url = config.api_prod + config.Config["api_user_history"]
    url = f"{base_url}/xcx/enroll/v1/user/history"
    response = requests.request("GET", url, params={"access_token": token}, headers=login_headers)
    response_data = response.json()
    if response.status_code == 200:
        print(response_data)
        return response_data['data']
        # status:1 进行中 2结束
    else:
        return None

def get_lecture_detail(token: str, eid: str):
    '''
    获取讲座详细信息
    Args:
        token: 用户登录凭证
        eid: 讲座ID

    Returns: 讲座详细信息
    '''
    # url = f'{config.api_prod}{config.Config["api_detail"]}'
    url = f"{base_url}/xcx/enroll/v3/detail"
    response = requests.get(
        url,
        params={"access_token": token, "eid": eid},
        headers=login_headers
    )
    if response.status_code == 200:
        return response.json().get('data')
    return None

def get_registration_info(token: str, eid: str):
    '''
    获取报名所需的信息
    Args:
        token: 用户登录凭证
        eid: 讲座ID

    Returns: 报名所需的信息
    '''
    # url = f'{config.api_prod}{config.Config["api_req_detail"]}'
    url = f"{base_url}/xcx/enroll/v1/req_detail"
    response = requests.get(
        url,
        params={"access_token": token, "eid": eid},
        headers=login_headers
    )
    if response.status_code == 200:
        return response.json().get('data', {}).get('req_info', [])
    return None

def generate_signature(token: str, eid: str):
    '''
    生成提交报名时需要的签名
    Args:
        token: 用户登录凭证
        eid: 讲座ID

    Returns: 签名字符串
    '''
    def random_key(length=4):
        chars = string.ascii_letters + string.digits
        return ''.join(random.choice(chars) for _ in range(length))

    T = random_key() + token[:2]
    I = hashlib.md5(eid.encode()).hexdigest()
    b = str(int(time.time() * 1000))
    M = T + hashlib.md5((I + b + "qwrq2w").encode()).hexdigest()
    return M

def submit_registration(token: str, eid: str, info: list):
    '''
    提交讲座报名
    Args:
        token: 用户登录凭证
        eid: 讲座ID
        info: 报名信息

    Returns: (bool, str) - (是否成功, 消息)
    '''
    url = f'{base_url}/xcx/enroll/v5/enroll'
    data = {
        "access_token": token,
        "eid": eid,
        "info": info,
        "on_behalf": 0,
        "items": [],
        "referer": "",
        "fee_type": "",
        "from": "xcx",
        "_a": generate_signature(token, eid),
        "_s": int(time.time() * 1000)
    }
    
    try:
        response = requests.post(
            url,
            headers=login_headers,
            data=json.dumps(data),
            verify=False,
            timeout=1
        )
        result = response.json()
        
        if result['msg'] in ['', '提交次数超过限制', '活动期间，只允许提交1次']:
            return True, result['msg']
        return False, result['msg']
    except Exception as e:
        return False, str(e)


def get_user_info(token: str):
    """
    获取用户信息
    """
    url = f"{base_url}/xcx/enroll/v1/userinfo"
    user_extra_info = {}

    try:
        response = requests.request("GET", url, params={"access_token": token}, headers=login_headers)
        user_info = response.json()
        
        if 'data' not in user_info or 'extra_info' not in user_info['data']:
            return {}
            
        for item in user_info['data']['extra_info']:
            names = item['name'] if isinstance(item['name'], list) else [item['name']]
            for name in names:
                user_extra_info[name] = item['value']
                
        return user_extra_info
    except Exception as e:
        print(f"Error getting user info: {str(e)}")
        return {}

def add_user_info(token: str, name: str, value: str):
    '''
    添加用户信息
    Args:
        token: 用户登录凭证
        name: 添加字段
        value: 添加内容

    Returns: (bool, str) - (是否成功, 消息)
    '''
    name_list = [name]
    url = f"{base_url}/xcx/enroll/v1/extra_info"
    data = {
        "access_token": token,
        "name": name_list,
        "value": value
    }
    try:
        response = requests.post(
            url,
            headers=login_headers,
            data=json.dumps(data),
            verify=False,
            timeout=1
        )
        result = response.json()
        if len(result['data']) >0:
            return True, result['msg']
        return False, result['msg']
    except Exception as e:
        return False, str(e)


def delete_user_info(token: str, key: str):
    '''
    删除用户信息
    Args:
        token: 用户登录凭证
        key: 删除字段的id

    Returns: (bool, str) - (是否成功, 消息)
    '''
    url = f"{base_url}/xcx/enroll/v1/extra_info"
    data = {
        "access_token": token,
        "name": key
    }
    response = requests.post(
        url,
        headers=login_headers,
        data=json.dumps(data),
        verify=False,
        timeout=1
    )
    result = response.json()

