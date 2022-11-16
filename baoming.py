# -*- coding: utf-8 -*-
# __author__:xiuming
# __QQ__:1365337879
# 2022/4/7 16:31


import base64
import datetime
import json
import threading
import time
import tkinter as tk
import tkinter.ttk as ttk
import webbrowser
from tkinter import *
from tkinter import END, messagebox
import requests
from PIL import Image, ImageTk


def prints(data):
    output.insert('end', '\n')
    output.insert('end',data)
    output.see(END)

root = tk.Tk()
root.title('微信讲座抢购报名脚本（测试版)')
root.geometry('1000x500')
root.iconbitmap("assets/favicon.ico")
root.resizable(width = True, height = True)
# 获取屏幕尺寸以计算布局参数，使窗口居屏幕中央
screenwidth = root.winfo_screenwidth()
screenheight = root.winfo_screenheight()
# frmLogin= Frame(root)
# Label(frmLogin, text="账号：").grid(row=0, column=0)
# Label(frmLogin, text="密码：").grid(row=1, column=0)
# frmLogin.pack()


#tab
style = ttk.Style()
style.configure('TNotebook.Tab', font=('微软雅黑','15','bold'), padding=[130 , 5])
tab=ttk.Notebook(root)
tab.place(relwidth=0.6, relheight=0.80, relx=1, rely=0, anchor='ne')
frame1=tk.Frame(tab,width=1500,height=150,relief='groove',bd=1)
tab1=tab.add(frame1,text = "主界面")
frame2 = tk.Frame(tab,width=100,height=50,relief='groove',bd=1)
tab2 = tab.add(frame2, text = "捐赠")
frame3= tk.Frame(tab)
tab3 = tab.add(frame3, text = "更新升级")
tab.pack(expand = True, fill = tk.BOTH)


#frame1
Warn = tk.Label(frame1,text="警告：   仅供交流学习！    禁止违法使用！   一切违法行为与本人无关！",fg="red",font = ('黑体', 15)).pack()
tittle_label= tk.Label(frame1, text='微信讲座抢购报名脚本（测试版)', font=('黑体', 18), width=30, height=2).pack()
beizhu = tk.Button(frame1, text='姓名：', font=('Arial', 12), width=30, height=2)
tk.Label(frame1, text='姓名:', width=15, font=('黑体', 15)).place(x=1, y=100)
names = tk.Entry(frame1, width=20,font=('黑体', 15))
names.place(x=110, y=100)
tk.Label(frame1, text='学号:', width=15, font=('黑体', 15)).place(x=1, y=150)
xuehaos = tk.Entry(frame1, width=20, font=('黑体', 15))
xuehaos.place(x=110, y=150)
tk.Label(frame1, text='讲座eid:', width=12, font=('黑体', 15)).place(x=1, y=200)
eids = tk.Entry(frame1, width=20, font=('黑体', 15))
eids.place(x=110, y=200)

output = tk.Text(frame1, width=75, height=15,font=('黑体', 12))
output.place(x=400, y = 80)
output.insert('1.0', '使用说明：\nGitee：https://gitee.com/ygxiu/lecture-registration\nGitHub：https://github.com/ygxiuming/Lecture-registration\n目前该程序适用于景德镇陶瓷大学讲座，如有问题请截图发邮件联系作者！')
tk.Label(frame1, text='备注：', bg="yellow" , width=5, font=('黑体', 15)).place(x=1, y=310)
myText = "    请填入以上所有参数，其中eid可以从讲座分享的H5链接中获取\n 程序完全开源免费，仅供交流学习\n"
tk.Message(frame1,text=myText,font=('黑体', 15), width=700).place(x=1, y = 340)

# tk.Message(frame2,text="作者：修明\n邮箱：lzmpt@qq.com\n有任何问题请联系邮箱！",font=('黑体', 15), width=1000).pack(side='bottom')
tk.Message(frame1,text = '如果有帮助到您，并且也使您感到开心的话，可以慷慨的为我买杯coffee吗?',fg = 'green',font=('黑体', 15),width=800).place(x=1, y = 410)




#frame2
tk.Label(frame2,text = '如果有帮助到您，并且也使您感到开心的话，可以慷慨的为我买杯coffee吗?',font=('黑体', 15),fg = 'green').grid(row=0, column =0,columnspan=2)

tk.Label(frame2,text = '微信捐赠',font=('黑体', 15)).grid(row=1, column =0)
tk.Label(frame2,text = '支付宝捐赠',font=('黑体', 15)).grid(row=1, column =1)

img1 = Image.open('assets//wechat.png')
photo1 = ImageTk.PhotoImage(img1)
tk.Label(frame2, image=photo1).grid(row=2, column =0,sticky=N+W+W+E,ipadx=100)

img2 = Image.open('assets//zfb.jpg')
photo2 = ImageTk.PhotoImage(img2)
tk.Label(frame2, image=photo2).grid(row=2, column =1,sticky=N+W+W+E,ipadx=100)

tk.Label(frame2, text = '感谢捐赠，您的激励将会投入更多的改进',font=('黑体', 15)).grid(row = 3,column = 0,sticky=N+W+W+E,ipadx=50)
tk.Label(frame2, text = '感谢捐赠，您的激励将会投入更多的改进',font=('黑体', 15)).grid(row = 3,column = 1,sticky=N+W+W+E,ipadx=50)
tk.Label(frame2, text = '作者：修明  邮箱：lzmpt@qq.com',font=('黑体', 15)).grid(row = 4,column = 0,columnspan = 2,sticky=N+W+W+E,ipadx=50)

#frame3
version = tk.Label(frame3, text = 'Version: 1.5.0   更新日期: 2022-09-21 \n 访问密码：8888' ,font=('黑体', 20)).pack(side="top",pady = '160')




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
        print("请求受阻，重新发起请求！！！")
    t = response.text
    #print(response.text)
    jsonData = json.loads(t)
    if jsonData['msg'] == 'invalid parameter':
        prints('参数出错，请检查输入参数请关闭程序，重新运行登录！！！或者联系作者！！！')
        return 8
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
    file_path = './assets/login.jpg'
    with open(file_path, 'wb') as f:
        f.write(page_content)
    img = Image.open('./assets/login.jpg')
    # 自己的图片地址，文件开头是数字要打两个‘\’
    img.show()
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

    response = requests.request("GET", url, headers=headers, data=payload,timeout = 1)
    # prints(response.text)
    response = json.loads(response.text)
    msg = response["msg"]
    if msg!='ok':
        token = ''
    else:
        token = response['data']['access_token']
    return token




def version_request(versionold):
    url = "https://gitee.com/ygxiu/lecture-registration/raw/master/version"
    payload = {}
    headers = {
        'Accept'                   : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language'          : 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en-US;q=0.7,en;q=0.6',
        'Cache-Control'            : 'max-age=0',
        'Connection'               : 'keep-alive',
        'Referer'                  : 'https://gitee.com/ygxiu/lecture-registration/edit/master/version',
        'Sec-Fetch-Dest'           : 'document',
        'Sec-Fetch-Mode'           : 'navigate',
        'Sec-Fetch-Site'           : 'same-origin',
        'Sec-Fetch-User'           : '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent'               : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
        'sec-ch-ua'                : '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
        'sec-ch-ua-mobile'         : '?0',
        'sec-ch-ua-platform'       : '"Windows"'
    }
    response = requests.request("GET", url, headers = headers, data = payload)
    version = response.text[8:]
    if version != versionold:
        messageversion = '当前有更新版本，请尽快前往更新界面进行更新！'
    else:
        messageversion = '当前为最新版本！'
    return version,messageversion



def juanzeng():
    tk.messagebox.showinfo('捐赠','请点击上方标签捐赠进行捐赠和联系作者\n如有其他需求也可联系作者')

def main():
    versionold = '1.5.0'
    version,messageversion = version_request(versionold)
    prints(f'\n版本信息检测中。。。。。。。\n当前版本：{versionold}\n最新版本：{version}\n状态{messageversion}\n')
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
                prints('如果有帮助到您，并且也使您感到开心的话，可以慷慨的为我买杯coffee吗?')
            elif t==8:
                break
            else:
                i = i + 1
                prints(str(ttime) + "请查看response，刷新中... 刷新第" + str((i-1)) + "次" + "\n")
                time.sleep(1)
def login():
    # 获取登录token
    time.sleep(2)
    code = get_codeimage()
    while (1):
        token = check(code)
        if token != '':
            prints('获取token成功！token:' + str(token))
            break
    return token

def newversion(url):
    webbrowser.open(url)


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



tk.Button(frame1, text="开始抢讲座",bg='lightblue', font=('黑体', 20), command=lambda :thread_it(main)).place(x=80, y=250)


tk.Button(frame1, text="使用说明Gitee",bg='lightblue', font=('黑体', 12), command=lambda :newversion(url = 'https://gitee.com/ygxiu/lecture-registration')).place(x=30, y=50)
tk.Button(frame1, text="使用说明Github",bg='lightblue', font=('黑体', 12), command=lambda :newversion(url = 'https://github.com/ygxiuming/Lecture-registration')).place(x=180, y=50)
tk.Button(frame1, text="反馈BUG",bg='lightblue', font=('黑体', 12), command=lambda :newversion(url = 'https://www.yuque.com/docs/share/ce70d550-d2bd-41bc-a8cb-cc1a6d8e6001?')).place(x=800, y=350)


tk.Button(frame1, text="请作者喝杯咖啡",bg='lightblue', font=('黑体', 12), command=lambda :thread_it(juanzeng)).place(x=250, y=260)
tk.Button(frame3, text="一键更新",bg='lightblue', font=('黑体', 20), command=lambda :newversion(url = 'https://wwd.lanzoum.com/b01pvee8j')).pack(side="top")


def on_closing():
    if messagebox.askokcancel("Quit", "你是想退出吗?"):
        root.destroy()

# WM_DELETE_WINDOW 不能改变，这是捕获命令
root.protocol('WM_DELETE_WINDOW', on_closing)
root.mainloop()
