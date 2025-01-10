# -*- coding: UTF-8 -*-
'''
@File    ：event.py
@IDE     ：PyCharm 
@Author  ：修明
@Email   ：lzmpt@qq.com
@Date    ：2024/12/31 0031 22:46 
@Detail  ：
'''
import base64
import hashlib
import json
import os
import random
import string
import threading
import time
from datetime import datetime

import cv2
import requests
from rich import pretty
from rich import print as print
from rich.console import Console
from rich.table import Table

pretty.install()
requests.packages.urllib3.disable_warnings()#清除出现https安全警告


class Login():
    '''
    报名工具登录类
    '''
    def __init__(self):
        self.base_url = "https://api-xcx-qunsou.weiyoubot.cn"

        self.login_headers = {
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
        self.code = "e5ff76cdcc334efa8582f77debed26d5"
        self.qrcode = ""
        self.token = ""
        self.debug_status = False
        self.personal_info = ""
        self.extra_info = {}
        self.login()

    def get_login_code_image(self):
        '''
        获取登录验证的二维码及二维码对应的唯一标识符code
        Returns:code , qrcode
        code: 二维码的唯一标识符
        qrcode: 二维码的base64编码格式
        '''
        # url = config.api_prod + config.Config['api_login_code']
        url = f"{self.base_url}/xcx/enroll_web/v1/pc_code"
        response = requests.request("GET", url, headers=self.login_headers)
        response_data = json.loads(response.text)
        if response.status_code == 200:
            self.code = response_data['data']['code']
            self.qrcode = response_data["data"]["qrcode"]
            return self.code, self.qrcode
        else:
            return None, None

    def get_token(self,code:str):
        '''
        获取网页登录token
        Args:
            code: 二维码的唯一标识符

        Returns: token
        token : 用户登录凭证
        '''
        # url = config.api_prod + config.Config['api_pc_login']
        url = f"{self.base_url}/xcx/enroll_web/v1/pc_login"
        response = requests.request("GET",
                                    url,
                                    params={"code": code, "source": "h5"},
                                    headers=self.login_headers)
        response = json.loads(response.text)
        msg = response["msg"]
        if msg != 'ok':
            return None
        else:
            self.token = response['data']['access_token']
        return self.token

    def get_personal_info(self):
        url = f"{self.base_url}/xcx/enroll/v1/userinfo"
        response = requests.request("GET",
                                    url,
                                    params={"access_token": self.token},
                                    headers=self.login_headers)
        response_data = json.loads(response.text)
        if response_data['msg'] != 'ok':
            return None
        else:
            self.personal_info = response_data['data']
        return self.personal_info


    def _save_and_show_qrcode(self, qrcode):
        """保存并显示登录二维码"""
        # 从base64字符串中提取图片数据
        qrcode_data = qrcode.replace('data:image/jpg;base64,', '')
        image_data = base64.b64decode(qrcode_data)

        # 保存为临时文件
        with open('./login.jpg', 'wb') as f:
            f.write(image_data)

        # 显示二维码
        threading.Thread(target=self._show_qrcode).start()

    def _show_qrcode(self):
        """显示二维码图片"""
        img = cv2.imread('login.jpg')
        cv2.imshow('login image', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        if os.path.exists('login.jpg'):
            os.remove('login.jpg')

    def verify_token(self):
        personal_info = self.get_personal_info()
        if personal_info is None:
            return False
        else:
            print("----------登录信息----------")
            name = personal_info['name']
            phone = personal_info['phone']
            print(f"姓名：{name}\n电话：{phone}")
            print("----------预填信息----------")
            extra_infos = personal_info['extra_info']
            if len(extra_infos) > 0:
                for extra_info in extra_infos:
                    self.extra_info[extra_info['name'][0]] = extra_info['value']
                    print(f"{extra_info['name'][0]}: {extra_info['value']}" )
            print("---------------------------")
            return True


    def login(self):
        console.rule("报名工具登录模块")
        if self.debug_status:
            self.verify_token()
        else:
            # 获取登录二维码
            code, qrcode = self.get_login_code_image()
            if not code or not qrcode:
                print("获取登录二维码失败！")
                return None

            # 保存并显示二维码
            self._save_and_show_qrcode(qrcode)
            print("请使用微信扫描二维码进行登录，扫完后请手动关闭二维码窗口！")

            verify_status = False
            # 等待扫码登录
            while True and verify_status is False:
                token = self.get_token(code)
                if token:
                    verify_status = self.verify_token()
                    if verify_status:
                        print("登录成功！")
                        print(f"获取token成功！\ntoken: {token}")
                    return token

def personal():
    url = 'https://gitee.com/ygxiu/lecture-registration/raw/master/README.assets/Snipaste_2022-11-20_11-08-44.png'
    os.system(
        '"C:\Program Files\internet explorer\iexplore.exe" https://gitee.com/ygxiu/lecture-registration/raw/master/README.assets/Snipaste_2022-11-20_11-08-44.png')


class Lecture(Login):
    def __init__(self):
        super().__init__()
        self.history_item = []
        self.history_item_index = {}


    def get_history_registration(self):
        '''
        获取用户浏览过的历史讲座
        Args:
            token: 用户登录凭证

        Returns: 历史讲座信息
        '''
        url = f"{self.base_url}/xcx/enroll/v1/user/history"
        response = requests.request("GET", url, params={"access_token": self.token}, headers=self.login_headers)
        response_data = response.json()
        if response.status_code == 200:
            data = response_data["data"]
            # print(data)
            # return response_data['data']
            # status:1 进行中 2结束

            for history_item in data:
                if history_item.get("status") == 1:
                    history_data = {}
                    history_data["title"] = history_item.get("title")                   # 活动标题
                    history_data["start_time"] = history_item.get("start_time")         # 活动开始时间，此处为时间戳 1735724700
                    history_data["status"] = history_item.get("status")                 # 活动状态，status:1 进行中 2结束或者未开始
                    history_data["eid"] = history_item.get("eid")                       # 活动唯一标识eid
                    history_data["limit"] = history_item.get("limit")                   # 活动报名数量
                    self.history_item.append(history_data)
                else:
                    current_timestamp = time.time()
                    item_start_time = history_item.get("start_time")
                    if item_start_time > current_timestamp:
                        history_data = {}
                        history_data["title"] = history_item.get("title")  # 活动标题
                        history_data["start_time"] = history_item.get("start_time")  # 活动开始时间，此处为时间戳 1735724700
                        history_data["status"] = history_item.get("status")  # 活动状态，status:1 进行中 2结束或者未开始
                        history_data["eid"] = history_item.get("eid")  # 活动唯一标识eid
                        history_data["limit"] = history_item.get("limit")  # 活动报名数量
                        self.history_item.append(history_data)
            # return self.history_item
            # 初始化表格
            table = Table(show_header=True, header_style="bold magenta")
            # 添加列名
            table.add_column("序号", style="dim", width=5)
            table.add_column("活动标题", style="dim", width=50)
            table.add_column("开始时间", style="dim", width=20)
            table.add_column("活动状态", style="dim", width=8)
            table.add_column("eid", style="dim", width=25)
            table.add_column("报名人数", style="dim", width=10)
            table.title = "历史活动信息"

            # 遍历历史活动信息
            for index, history_item in enumerate(self.history_item, start=1):
                self.history_item_index[str(index)] = history_item
                start_time = datetime.fromtimestamp(history_item['start_time']).strftime('%Y-%m-%d %H:%M:%S')
                if history_item['status'] == 1:
                    status = "进行中"
                else:
                    status = "未开始"
                # 添加行数据
                table.add_row(str(index), history_item['title'], str(start_time), status,
                              str(history_item['eid']), str(history_item['limit']))
            # 输出表格
            console.print(table)

    def get_registration_info(self, eid: str):
        '''
        获取报名所需的信息
        Args:
            token: 用户登录凭证
            eid: 讲座ID

        Returns: 报名所需的信息
        '''
        url = f"{self.base_url}/xcx/enroll/v1/req_detail"
        response = requests.get(
            url,
            params={"access_token": self.token, "eid": eid},
            headers=self.login_headers
        )
        if response.status_code == 200:
            return response.json().get('data', {}).get('req_info', [])
        else:
            print("获取报名信息失败")
            return None
    def _format_options(self, item):
        """格式化选项信息"""
        if item["type_text"] == '多项选择':
            return item["options"]
        elif item["type_text"] == '单项选择':
            return [option['text'] for option in item["options"]]
        return "需要手动填写信息"

    def _get_field_note(self, item):
        """获取字段注释"""
        if item["field_name"] == "验证数字":
            return f"输入{item['min_value']}-{item['max_value']}之间的数字"
        return "无"

    def _get_field_value(self, item):
        """获取字段值"""
        field_name = item["field_name"]
        field_name_set = set(field_name)
        # 从配置文件中获取值
        for key, value in self.extra_info.items():
            key_set = set(key)
            if key_set.issubset(field_name_set):
                return key,value

        # 尝试计算表达式
        try:
            expression = field_name.replace('=', '')
            result = eval(expression)
            return "验证计算",str(result)
        except:
            return "未匹配到字段","1"  # 默认值
    def get_registration_info_main(self, eid):
        """获取报名所需的信息"""
        info = self.get_registration_info(eid)
        if not info:
            return None

        # 创建表格显示报名信息
        table = Table(show_header=True, header_style="bold magenta")
        table.title = "讲座需要填写的信息"
        table.add_column("信息标题", style="dim", width=12, justify="center")
        table.add_column("信息类型", justify="center")
        table.add_column("选项信息", justify="center")
        table.add_column("备注信息", justify="center")
        table.add_column("匹配字段", justify="center")
        table.add_column("匹配内容", justify="center")

        infoes = []
        for item in info:
            field_name = item["field_name"]
            field_type = item["type_text"]
            options = self._format_options(item)
            note = self._get_field_note(item)

            # 处理字段值
            field_name_key,field_value = self._get_field_value(item)
            if field_value:
                infoes.append({
                    "field_name": field_name,
                    "field_value": field_value,
                    "field_key": item["field_key"],
                    "ignore": 0
                })
            table.add_row(field_name, field_type, str(options), note, field_name_key,field_value)
            table.add_row("", "", "")

        console.print(table)
        return infoes


    def generate_signature(self,token: str, eid: str):
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

    def submit_registration(self,token: str, eid: str, info: list):
        '''
        提交讲座报名
        Args:
            token: 用户登录凭证
            eid: 讲座ID
            info: 报名信息

        Returns: (bool, str) - (是否成功, 消息)
        '''
        url = f'{self.base_url}/xcx/enroll/v5/enroll'
        data = {
            "access_token": token,
            "eid": eid,
            "info": info,
            "on_behalf": 0,
            "items": [],
            "referer": "",
            "fee_type": "",
            "from": "xcx",
            "_a": self.generate_signature(token, eid),
            "_s": int(time.time() * 1000)
        }

        try:
            response = requests.post(
                url,
                headers=self.login_headers,
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

    def add_user_info(self, token: str, name: str, value: str):
        '''
        添加用户信息
        Args:
            token: 用户登录凭证
            name: 添加字段
            value: 添加内容

        Returns: (bool, str) - (是否成功, 消息)
        '''
        name_list = [name]
        url = f"{self.base_url}/xcx/enroll/v1/extra_info"
        data = {
            "access_token": token,
            "name": name_list,
            "value": value
        }
        try:
            response = requests.post(
                url,
                headers=self.login_headers,
                data=json.dumps(data),
                verify=False,
                timeout=1
            )
            result = response.json()
            if len(result['data']) > 0:
                return True, result['msg']
            return False, result['msg']
        except Exception as e:
            return False, str(e)

    def delete_user_info(self, token: str, key: str):
        '''
        删除用户信息
        Args:
            token: 用户登录凭证
            key: 删除字段的id

        Returns: (bool, str) - (是否成功, 消息)
        '''
        url = f"{self.base_url}/xcx/enroll/v1/extra_info"
        data = {
            "access_token": token,
            "name": key
        }
        response = requests.post(
            url,
            headers=self.login_headers,
            data=json.dumps(data),
            verify=False,
            timeout=1
        )
        result = response.json()

    def submit_main(self,index,eid):
        # 初始化表格
        table = Table(show_header=True, header_style="bold magenta")
        # 添加列名
        table.add_column("字段", style="dim", width=5)
        table.add_column("值", style="dim", width=50)
        table.title = "预填信息预览"

        for key, value in self.extra_info.items():
            # print(key,value)
            # 添加行数据
            table.add_row(key, value)
        console.print(table)
        print("备注：预填信息在 <https://p.baominggongju.com/personalInfo> 中进行增加修改，点击 添加快速填写信息 按钮即可\n若需要增加延迟提交，可增加字段 延迟时间，对应的字段值为毫秒；例如：需要延迟2秒提交，增加字段  延迟时间：2000")
        print("预填信息匹配规则：采用子集匹配规则；\n例如：预填信息为 姓名：修明，若报名信息中同时存在姓和名两个字，则认定匹配成功！以下是匹配姓名成功示例\n？姓！名\n姓      名\n名  …… ### 姓")
        console.rule("")
        print(f'活动标题：{self.history_item_index[str(index[1])]["title"]}   开始时间：{datetime.fromtimestamp(self.history_item_index[str(index[1])]["start_time"]).strftime("%Y-%m-%d %H:%M:%S")}')
        if self.extra_info.get("延迟时间") is not None:delay_time = int(self.extra_info.get("延迟时间"))
        else:delay_time = 0
        start_time = self.history_item_index[str(index[1])]['start_time']
        timenow = time.time()
        if timenow >= start_time:
            print(
                f"当前时间：{datetime.fromtimestamp(timenow).strftime('%Y-%m-%d %H:%M:%S')}，活动开始时间：{datetime.fromtimestamp(self.history_item_index[str(index[1])]['start_time']).strftime('%Y-%m-%d %H:%M:%S')}，开始报名")
            info = self.get_registration_info_main(eid)
            success, msg = self.submit_registration(self.token, eid, info)
            # 打印提交信息
            console.rule("提交结果")
            console.print(f"Success: {success}")
            console.print(f"Message: {msg}")

            if success:
                console.print("报名成功！程序将在10秒后退出...")
                personal()
                time.sleep(10)
            elif msg in ['报名人数已满或项目数量不足', 'invalid parameter']:
                console.print("报名失败，程序将在10秒后退出...")
                time.sleep(10)

        while True:
            timenow = time.time()
            with console.status(f'当前时间：{datetime.fromtimestamp(timenow).strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]}，距离开始时间还有{start_time - timenow}秒', spinner='dots'):
                if (start_time - timenow) <= 3:
                    info = self.get_registration_info_main(eid)
                if (start_time - timenow) <= 0 and (timenow - start_time) >= (delay_time/1000):
                    if not info:continue
                    success, msg = self.submit_registration(self.token, eid, info)
                    # 打印提交信息
                    console.rule("提交结果")
                    console.print(f"Success: {success}")
                    console.print(f"Message: {msg}")

                    if success:
                        console.print("恭喜您！报名成功！")
                        console.print("希望得到您的赞助，将会给予作者继续更新维护的动力")
                        console.print("程序将在10秒后退出...")
                        personal()
                        time.sleep(100)
                        break
                    elif msg in ['报名人数已满或项目数量不足', 'invalid parameter']:
                        console.print("报名失败，程序将在10秒后退出...")
                        time.sleep(100)
                        break
                    else:
                        console.print("还未报名，刷新中...")
                time.sleep(0.5)




    def run(self):
        console.rule("历史活动信息")
        # 获取历史活动信息
        self.get_history_registration()
        index= console,input("请输入需要选择的活动序号：")
        eid = self.history_item_index[str(index[1])]['eid']
        print(f"当前选择序号{index[1]}的活动，eid为：{eid}")
        console.rule("活动报名")
        # print(self.extra_info)
        self.submit_main(index,eid)











if __name__ == '__main__':
    console = Console(color_system='256', style=None)
    console.rule("报名工具辅助工具")
    tittle = '''
            author:修明
            object:微信小程序 报名工具
            function：
                1.扫码登陆
                2.自主选择活动
                3.快速匹配活动填写信息
                4.支持填空参数以及选择参数，其他参数后续开发
            GitHub：https://github.com/ygxiuming/Lecture-registration
            Gitee：https://gitee.com/ygxiu/lecture-registration
        '''
    console.print(tittle)
    lecture = Lecture()
    lecture.run()
