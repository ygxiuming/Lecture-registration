# -*- coding: utf-8 -*-
# __author__:xiuming
# __QQ__:1365337879
# 2022/4/7 16:31


import base64
import datetime
import json
import threading
from tkinter import *
from tkinter import messagebox

import cv2
import requests


def prints(data):
    output.insert('end', '\n')
    output.insert('end',data)
    output.see(END)

root = Tk()
root.title('微信讲座抢购报名脚本（测试版)')
root.geometry('1000x500')
root.resizable(width=True, height=True)
#获取屏幕尺寸以计算布局参数，使窗口居屏幕中央
screenwidth = root.winfo_screenwidth()
screenheight = root.winfo_screenheight()

tittle_label= Label(root, text='微信讲座抢购报名脚本（测试版)', font=('黑体', 18), width=30, height=2)
tittle_label.pack()
beizhu = Button(root, text='姓名：', font=('Arial', 12), width=30, height=2)
Label(root, text='姓名:', width=15, font=('黑体', 15)).place(x=1, y=100)
names = Entry(root, width=20,font=('黑体', 15))
names.place(x=110, y=100)
Label(root, text='学号:', width=15, font=('黑体', 15)).place(x=1, y=150)
xuehaos = Entry(root, width=20, font=('黑体', 15))
xuehaos.place(x=110, y=150)
Label(root, text='讲座eid:', width=12, font=('黑体', 15)).place(x=1, y=200)
eids = Entry(root, width=20, font=('黑体', 15))
eids.place(x=110, y=200)



output = Text(root, width=65, height=15,font=('黑体', 12))
output.place(x = 450, y = 80)
output.insert('1.0', '使用说明：\nGitee：https://gitee.com/ygxiu/lecture-registration\nGitHub：https://github.com/ygxiuming/Lecture-registration')
Label(root, text='备注：', bg="yellow" , width=5, font=('黑体', 15)).place(x=1, y=300)
myText = "    请填入以上所有参数，其中eid可以从讲座分享的H5链接中获取"
msg = Message(root,text=myText,font=('黑体', 15), width=400)
msg.place(x=1, y = 330)
auto = Message(root,text="作者：修明\n邮箱：lzmpt@qq.com\n有任何问题请联系邮箱！",font=('黑体', 15), width=400)
auto.place(x=450, y = 330)
war = Message(root,text="警告：\n仅供交流学习！\n\n  禁止违法使用！\n\n    一切违法行为与本人无关！",fg="red",font = ('黑体', 15), width=400)
war.place(x=700, y = 330)
cgitb = Message(root,text="Gitee：https://gitee.com/ygxiu/lecture-registration\nGitHub：https://github.com/ygxiuming/Lecture-registration",font=('黑体', 15), width=600)
cgitb.place(x=1, y =450)


def post(name,xuehao,eid,token):
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
    except Exception as e:
        prints(e)
    t = response.text
    #print(response.text)
    jsonData = json.loads(t)
    if jsonData['msg'] == 'invalid parameter':
        prints('token出错，请关闭程序，重新运行登录！！！')
    prints(jsonData)
    s = jsonData['sta']
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
    prints("请使用微信扫码登录，扫完关闭二维码！")
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
    prints(response.text)
    response = json.loads(response.text)
    msg = response["msg"]
    if msg!='ok':
        token = ''
    else:
        token = response['data']['access_token']
    return token

def main():
    name = names.get()
    xuehao = xuehaos.get()
    eid = eids.get()

    token = login()

    ttime = time_now()
    prints(name)
    if name=="" or xuehao=="" or eid == "" or token=="":
        prints(str(ttime) + "    请完善配置，配置未配置正确！")

    else:
        i = 1
        while(i>0):
            ttime = time_now()
            t = post(name,xuehao,eid,token)
            if t == 0:
                i = 0
                prints("  报名成功！")
            else:
                i = i + 1

                prints(str(ttime) + "请查看response，刷新中... 刷新第".format(str(msg)) + str((i-1)) + "次" + "\n")

                # time.sleep(1)
def login():
    # 获取登录token
    while (1):
        code = get_codeimage()
        token = check(code)
        if token != '':
            prints('获取token成功！token:' + str(token))
            break
        else:
            prints('token获取失败，请重新扫码！')
    return token

def thread_it(func):
  '''将函数打包进线程'''
  # 创建
  t = threading.Thread(target=func)
  # 守护 !!!
  t.setDaemon(True)
  # 启动
  t.start()
  # 阻塞--卡死界面！
  # t.join()

Button(root, text="开始抢讲座", font=('黑体', 20), command=lambda :thread_it(main)).place(x=125, y=250)
# Button(root, text="一键登录", font=('黑体', 15), command=lambda :thread_it(login)).place(x=325, y=100)
def on_closing():
    if messagebox.askokcancel("Quit", "你是想退出吗?"):
        root.destroy()

# WM_DELETE_WINDOW 不能改变，这是捕获命令
root.protocol('WM_DELETE_WINDOW', on_closing)
root.mainloop()




