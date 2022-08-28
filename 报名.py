# -*- coding: utf-8 -*-
# __author__:xiuming
# __QQ__:1365337879
# 2022/4/7 16:31

import base64
import json

import cv2
import requests

###################################配置#################
name = ''#姓名
xuehao = ''#学号
eid = ""#小程序eid
#########################################################


def post(token,xuehao,name):
    data = [
        {
            "field_name": "姓名",
            "field_value": name,
            "field_key": 1
        },
        {
            "field_name": "学号",
            "field_value": xuehao,
            "field_key": 13
        }
    ]
    payload = json.dumps({
        "access_token": token,
        "eid": eid,
        "info": data,
        "on_behalf": 0,
        "items": [],
        "referer": "",
        "fee_type": ""
    })
    try:
        url = "http://api-xcx-qunsou.weiyoubot.cn/xcx/enroll/v5/enroll"
        headers = {
          'Host': 'api-xcx-qunsou.weiyoubot.cn',
          'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat',
          'content-type': 'application/json',
          'Referer': 'https://servicewechat.com/wxfaa08012777a431e/773/page-frame.html',
          'Cookie': 'tgw_l7_route=05fc80284c7b2840a1683128310f0d09'
        }

        response = requests.request("POST", url, headers=headers, data=payload,verify=False,timeout=2)
        t = response.text
        #print(response.text)
        jsonData = json.loads(t)
        print(jsonData)
        s = jsonData['sta']
    except Exception as e:
        print(e)
    return s

def time_now():

    # 打印当前时间
    time = datetime.datetime.now()
    return time
    # 打印按指定格式排版的时间
    #time2 = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    #print(time2)


#获取二维码
def get_codeimage():
    url = "https://api-xcx-qunsou.weiyoubot.cn/xcx/enroll_web/v1/pc_code"
    payload={}
    headers = {
      'Accept': '*/*',
      'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
      'Connection': 'keep-alive',
      'DNT': '1',
      'If-None-Match': 'W/"dca076a0e10683920f8a758fc500c825ac2426f0"',
      'Origin': 'http://www.baominggongju.com',
      'Referer': 'http://www.baominggongju.com/',
      'Sec-Fetch-Dest': 'empty',
      'Sec-Fetch-Mode': 'cors',
      'Sec-Fetch-Site': 'cross-site',
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36 Edg/104.0.1293.70',
      'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Microsoft Edge";v="104"',
      'sec-ch-ua-mobile': '?0',
      'sec-ch-ua-platform': '"Windows"',
      # 'Cookie': 'tgw_l7_route=05fc80284c7b2840a1683128310f0d09'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    response = json.loads(response.text)
    # print(response.text)
    code = response["data"]["code"]
    qrcode = response["data"]["qrcode"]
    img_imf = qrcode.replace('data:image/jpg;base64,', '')

    # 将data:image/jpg;base64格式的数据转化为图片
    page_content = base64.b64decode(img_imf)
    file_path = './login.jpg'
    with open(file_path, 'wb') as f:
        f.write(page_content)
    img = cv2.imread('login.jpg')
    cv2.imshow('image', img)
    cv2.waitKey(0)
    return code

#识别二维码
def check(code):
    import requests

    url = "https://api-xcx-qunsou.weiyoubot.cn/xcx/enroll_web/v1/pc_login?code={}".format(code)
    payload = {}
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Connection': 'keep-alive',
        'DNT': '1',
        'Origin': 'http://www.baominggongju.com',
        'Referer': 'http://www.baominggongju.com/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36 Edg/104.0.1293.70',
        'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Microsoft Edge";v="104"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        # 'Cookie': 'tgw_l7_route=05fc80284c7b2840a1683128310f0d09'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    print(response.text)
    response = json.loads(response.text)
    msg = response["msg"]
    if msg!='ok':
        token = ''
    else:
        token = response['data']['access_token']
    return token

def main():
    # 获取登录token
    while (1):
        code = get_codeimage()
        token = check(code)
        if token != '':
            print('获取token成功！token:' + str(token))
            break
        else:
            print('token获取失败，请重新扫码！')

    time = time_now()
    if name=="" or xuehao=="" or eid == "":
        print(str(time) + "    请完善配置，配置未配置正确！")

    else:
        i = 1
        while(i>0):
            time = time_now()
            t = post(token,xuehao,name)
            if t == 0:
                i = 0
                print(str(time) + "  报名成功！")
            else:
                i = i + 1
                print(str(time) + "  还未报名，刷新中...   刷新第" + str((i-1)) + "次")
                time.sleep(1)

if __name__ == '__main__':
    main()



