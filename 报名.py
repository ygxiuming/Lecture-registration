# -*- coding: utf-8 -*-
# __author__:xiuming
# __QQ__:1365337879
# 2022/4/7 16:31

import requests
import json
import time

###################################配置#################
name = ''#姓名
xuehao = ''#学号
eid = ""#小程序eid
token = ""#自己微信的token，自己抓包获得
#########################################################
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

def post(payload):
    url = "http://api-xcx-qunsou.weiyoubot.cn/xcx/enroll/v5/enroll"
    headers = {
      'Host': 'api-xcx-qunsou.weiyoubot.cn',
      'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat',
      'content-type': 'application/json',
      'Referer': 'https://servicewechat.com/wxfaa08012777a431e/773/page-frame.html',
      'Cookie': 'tgw_l7_route=05fc80284c7b2840a1683128310f0d09'
    }

    response = requests.request("POST", url, headers=headers, data=payload,verify=False)
    t = response.text
    #print(response.text)
    jsonData = json.loads(t)
    print(jsonData)
    s = jsonData['sta']
    return s

def time_now():

    # 打印当前时间
    time = datetime.datetime.now()
    return time
    # 打印按指定格式排版的时间
    #time2 = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    #print(time2)

def main():
    time = time_now()
    if name=="" or xuehao=="" or eid == "" or token=="":
        print(str(time) + "    请完善配置，配置未配置正确！")

    else:
        i = 1
        while(i>0):
            time = time_now()
            t = post(payload)
            if t == 0:
                i = 0
                print(str(time) + "  报名成功！")
            else:
                i = i + 1
                print(str(time) + "  还未报名，刷新中...   刷新第" + str((i-1)) + "次")
                time.sleep(1)

if __name__ == '__main__':
    main()



