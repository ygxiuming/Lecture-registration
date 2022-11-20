#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/11/18 9:43
# @Author  : 修明
# @File    : Registration_tool_assistance.py
# @Description :


import base64
import json
import os
import threading
import time
from datetime import datetime

import cv2
import requests
from deta import Deta
from rich import pretty
from rich import print as print
from rich.console import Console as console
from rich.table import Table

pretty.install()
requests.packages.urllib3.disable_warnings()#清除出现https安全警告



class login():
    def __init__(self):
        self.url = 'https://api-xcx-qunsou.weiyoubot.cn/xcx/enroll_web'
        self.headers = {
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
            'sec-ch-ua-platform': '"Windows"'
        }
        self.code = ''
        self.token = ''


    # 获取二维码
    def get_codeimage(self):
        response = requests.request("GET", self.url + '/v1/pc_code', headers=self.headers)
        response = json.loads(response.text)
        self.code = response["data"]["code"]
        qrcode = (response["data"]["qrcode"]).replace('data:image/jpg;base64,', '')
        page_content = base64.b64decode(qrcode)
        file_path = './login.jpg'
        with open(file_path, 'wb') as f:
            f.write(page_content)
    # 识别二维码
    def check(self):
        response = requests.request("GET", self.url + '/v1/pc_login?code=%s'%self.code, headers=self.headers)
        response = json.loads(response.text)
        msg = response["msg"]
        if msg != 'ok':
            token = ''
        else:
            token = response['data']['access_token']
            self.token = token
            # print("token:",token)
        return token

    def image_show(self,):
        img = cv2.imread('login.jpg')
        cv2.imshow('image', img)
        cv2.waitKey(0)

    def login(self):
        console.rule('登录模块')
        self.get_codeimage()
        console.log("请使用微信扫描二维码进行登录，扫完后关闭窗口！")
        thead = threading.Thread(target=self.image_show)
        thead.start()
        while (1):
            token = self.check()
            if token != '':
                console.log("登陆成功！")
                console.log("获取token成功！\ntoken:" + token)
                break
            else:
                with console.status(f'还未登录，请等待！', spinner='line'):
                    time.sleep(2)
        return self.token


class Lecture(object):
    def __init__(self,):
        self.url = 'https://api-xcx-qunsou.weiyoubot.cn/xcx/enroll'
        self.post_url = 'https://api-xcx-qunsou.weiyoubot.cn/xcx/enroll/v5/enroll'
        self.headers = headers = {
            'Host': 'api-xcx-qunsou.weiyoubot.cn',
            'Connection': 'keep-alive',
            'content-type': 'application/json',
            'Accept-Encoding': 'gzip,compress,br,deflate',
            'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.26(0x18001a31) NetType/WIFI Language/zh_CN',
            'Referer': 'https://servicewechat.com/wxfaa08012777a431e/830/page-frame.html',
        }
        self.token = ''
        self.eid = ''
        self.infos = {}
        self.registration_eid = []
        self.registration_map = {}

    def time_now(self,):
        # 打印当前时间
        timenow = datetime.now()
        return timenow
        # 打印按指定格式排版的时间
        # time2 = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # print(time2)

    def all_registration(self,):
        url = 'https://api-xcx-qunsou.weiyoubot.cn/xcx/enroll/v1/user/history?access_token=%s' % self.token
        ret = requests.get(self.url + '/v1/user/history?access_token=%s' % self.token, headers=self.headers).json()
        # status:1 进行中 2结束
        index = 1
        for i in ret['data']:
            if i['status'] == 0 or i['status'] == 1:
            # 已满
                if i['count'] >= i['limit']:
                    continue
                print("编号：%d 讲座：%s" % (index, i["title"]))
                index += 1
                self.registration_eid.append(i['eid'])
                self.registration_map[i['eid']] = i["title"]
        # print( self.registration_map)

     #获取开始时间
    def get_time(self,):
        index = int(console.input("请选择(填编号):"))
        self.eid = self.registration_eid[index-1]
        response = requests.request("GET", self.url + f'/v1/detail?eid={self.registration_eid[index-1]}&access_token={self.token}&admin=0&from=detail&referer=', headers=self.headers)
        data = response.json()
        timestep = data['data']['start_time']
        timeStamp = float(timestep)
        timeArray = time.localtime(timeStamp)
        timegep = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        console.log('讲座开始时间:' + str(timegep))
        console.rule(f'当前选择讲座名称：{self.registration_map[self.registration_eid[index - 1]]}')
        return timestep,data,timegep

    #获取相关参数
    def get_optioninfo(self,data):
        # print(data["data"]["req_info"])
        info = data["data"]["req_info"]
        index = 0
        namelist = []
        typelist = []
        optionslist = []
        options = []
        keys = []
        for i in info:
            namelist.append(i["field_name"])
            typelist.append(i["type_text"])
            keys.append(i["field_key"])
            if i["type_text"] == '多项选择':
                optionslist.append(i["options"])
                options.append(i["new_options"])
            elif i["type_text"] == '单项选择':
                option_name = []
                # print(i["options"])
                for option in i["options"]:
                    option_name.append(option['text'])
                options.append(i["new_options"])
                optionslist.append(option_name)
            else:
                optionslist.append(0)
                options.append(0)


        # console.log(namelist)
        # console.log(typelist)
        # console.log(optionslist)
        # console.log(options)

        #输出所需讲座信息全部内容
        table = Table(show_header=True, header_style="bold magenta")
        table.title = "讲座需要填写的信息"
        table.add_column("信息标题", style="dim", width=12, justify="center")
        table.add_column("信息类型", justify="center")
        table.add_column("选项信息", justify="center")

        for i in range(len(namelist)):
            name = str(namelist[i])
            type = str(typelist[i])
            if optionslist[i] == 0:
                option = "需要手动填写信息"
            else:
                option = str(optionslist[i])
            table.add_row(
                name,
                type,
                option
            )
            table.add_row("","","")
        console.print(table)

        console.rule("讲座信息参数填写")
        infoes = []

        for i in range(len(namelist)):
            if typelist[i] != '单项选择' and typelist[i] != '多项选择':
                console.print(f'参数{i+1}：' + namelist[i])
                console.print(f'参数{namelist[i]}类别：' + typelist[i])
                name = console.input(f'请输入参数{namelist[i]}的内容：')
                date = {"field_name": namelist[i], "field_value": name, "field_key": keys[i], "ignore": 0}
                infoes.append(date)
                console.print(f'输入成功！，参数{i+1}设置成功')
                console.rule()
            elif typelist[i] == '单项选择':
                console.print(f'参数{i + 1}：' + namelist[i])
                console.print(f'参数{namelist[i]}类别：' + typelist[i])
                console.print('选项内容：')
                index = 1
                for option in optionslist[i]:
                    console.print(f'        {index}：{option}')
                    index += 1
                xuanze = int(console.input(f'请输入参数{namelist[i]}的选项(注意是{typelist[i]}哦)：'))
                value = options[i][xuanze-1]['key']
                date = {"field_name": namelist[i],
                        "field_value": optionslist[i][xuanze-1],
                        "field_key": keys[i],
                        "new_field_value": value,
                        "ignore": 0}
                infoes.append(date)
                # print(date)
                console.print(f'输入成功！，参数{i + 1}设置成功')
                console.rule()
            elif typelist[i] == '多项选择':
                console.print(f'参数{i + 1}：' + namelist[i])
                console.print(f'参数{namelist[i]}类别：' + typelist[i])
                console.print('选项内容：')
                index = 1
                for option in optionslist[i]:
                    console.print(f'        {index}：{option}')
                    index += 1
                value = []
                field_value = []
                while True:
                    xuanze = int(console.input(f'请输入参数{namelist[i]}的选项(注意是{typelist[i]}哦,依次输入，输入0进行退出)：'))
                    if xuanze == 0:
                        break
                    else:
                        value.append(options[i][xuanze - 1]['key'])
                        field_value.append(optionslist[i][xuanze-1])


                date = {"field_name": namelist[i],
                        "field_value": field_value,
                        "field_key": keys[i],
                        "new_field_value": value,
                        "ignore": 0}
                infoes.append(date)
                # print(date)
                console.print(f'输入成功！，参数{i + 1}设置成功')
                console.rule()
            else:
                console.print('该程序目前仅仅支持文本，选择，其他待开发，如有需求请联系作者，lzmpt@qq.com')
        console.print('请仔细检查自己所填写字段')
        console.print(infoes)
        return infoes

    def post(self,payload):
        try:
            console.print()
            response = requests.request("POST", self.post_url, headers=self.headers, data=payload, verify=False, timeout=1)
            t = response.text
            jsonData = json.loads(t)
            console.print(jsonData)
            if jsonData['msg'] == '报名人数已满或项目数量不足' or jsonData['msg'] == '提交次数超过限制' or jsonData['msg'] == 'invalid parameter' or jsonData['msg'] == '' or jsonData['msg'] == '活动期间，只允许提交1次':
                console.print()
                console.print(jsonData['msg'])
                return 0,jsonData['msg']
            else:
                return 1,jsonData['msg']
        except Exception as e:
            console.print("请求受阻，重新发起请求")

    def personal(self,):
        url = 'https://gitee.com/ygxiu/lecture-registration/raw/master/README.assets/Snipaste_2022-11-20_11-08-44.png'
        os.system('"C:\Program Files\internet explorer\iexplore.exe" https://gitee.com/ygxiu/lecture-registration/raw/master/README.assets/Snipaste_2022-11-20_11-08-44.png')


    def run(self,):
        timenow = self.time_now()
        console.rule("微信历史讲座信息")
        self.all_registration()
        start_time, data, timegep = self.get_time()
        info = self.get_optioninfo(data)
        data = {"eid": "", "info": info, "on_behalf": 0, "items": [], "access_token": ""}
        data["eid"] = self.eid
        data["access_token"] = self.token
        payload = json.dumps(data)
        console.rule("预约报名模块")
        console.print(f'讲座开始时间：{timegep}')
        while True:
            timenow = self.time_now()
            time_loss = start_time - int(time.time())
            with console.status(f'距离开始时间还有{time_loss}秒',spinner= 'dots'):
                if time_loss <=3:
                    t, message = self.post(payload)
                    if t == 0:
                        if message == '' or message == '提交次数超过限制':
                            console.log("报名成功！")
                            console.log("如果对您有帮助的话，可以帮忙点个star吗？")
                            self.personal()
                        elif message == '报名人数已满或项目数量不足' or message == 'invalid parameter':
                            console.log('很尴尬，未抢到或者程序出错，请检查自己的微信！')
                        break
                    else:
                        console.log("还未报名，刷新中...")
                        time.sleep(1)
                time.sleep(1)

def version_request(versionold):
    url = "https://gitee.com/ygxiu/lecture-registration/raw/master/version"
    url2 = 'https://gitee.com/ygxiu/lecture-registration/raw/master/tittler'
    payload = {}
    headers = {
        'Accept'                   : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language'          : 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en-US;q=0.7,en;q=0.6',
        'Referer'                  : 'https://gitee.com/ygxiu/lecture-registration/edit/master/version',
        'Sec-Fetch-Dest'           : 'document',
    }
    response = requests.request("GET", url, headers = headers, data = payload)
    responses = requests.request("GET", url2, headers = headers, data = payload).text
    version = response.text[8:]
    console.rule(f"版本：{versionold}")
    if version != versionold:
        console.print(f"当前版本：{versionold}   最新版本：{version}")
        messageversion = '当前有更新版本，请尽快前往更新界面进行更新！'
        return 1
    else:
        console.print(f"当前版本：{versionold}   最新版本：{version}")
        messageversion = '当前为最新版本！'
    return 0

if __name__ == '__main__':
    version = '2.0.0'
    console = console(color_system='256', style=None)
    console.rule("报名工具多参数测试版本")
    tittle = '''
        author:修明
        object:微信小程序 报名工具
        function：
            1.扫码登陆
            2.自主选择讲座
            3.输出所需要填写信息及条件
            4.支持填空参数以及选择参数，其他参数后续开发
        GitHub：https://github.com/ygxiuming/Lecture-registration
        Gitee：https://gitee.com/ygxiu/lecture-registration
    '''
    console.print(tittle)
    t = version_request(version)
    if t == 0 :
        infos = {}
        token = login().login()
        # token = '79be2cb2d8b44ed98f8484ba990f94b1'
        lecture = Lecture()
        lecture.token = token
        lecture.infos = infos
        lecture.run()
        time.sleep(600)
    else:
        console.print("请尽快更新最新版本！")
        time.sleep(600)