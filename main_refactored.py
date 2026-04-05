# -*- coding: UTF-8 -*-
"""
微信小程序报名工具
重构版本 - 保持所有原有功能，优化代码结构

author: 修明
email: lzmpt@qq.com
GitHub: https://github.com/ygxiuming/Lecture-registration
Gitee: https://gitee.com/ygxiu/lecture-registration
"""
import logging
import os
import sys
import time

from rich.console import Console
from rich import pretty
from typing import Optional

# 初始化rich
pretty.install()

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.api_client import APIClient
from utils.constants import PERSONAL_PAGE_URL
from utils.validators import validate_token, is_valid_index
from utils.validators import match_field_name
from utils.formatters import format_timestamp
from services.auth_service import AuthService
from services.lecture_service import LectureService

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('app.log', encoding='utf-8')
    ]
)

# 禁用不安全请求警告
import requests
requests.packages.urllib3.disable_warnings()

console = Console(color_system='256', style=None)
logger = logging.getLogger(__name__)


def open_personal_page():
    """打开个人页面"""
    try:
        os.startfile(PERSONAL_PAGE_URL.replace('/', '\\'))
    except Exception:
        console.print("[yellow]无法打开浏览器，请手动访问以下网址：[/yellow]")
        console.print(f"[cyan]{PERSONAL_PAGE_URL}[/cyan]")


def display_banner():
    """显示欢迎横幅"""
    banner = """
            author: 修明
            object: 微信小程序 报名工具
            function：
                1. 扫码登陆
                2. 自主选择活动
                3. 快速匹配活动填写信息
                4. 支持填空参数以及选择参数，其他参数后续开发
            GitHub：https://github.com/ygxiuming/Lecture-registration
            Gitee：https://gitee.com/ygxiu/lecture-registration
        """
    console.rule("报名工具辅助工具")
    console.print(f"[cyan]{banner}[/cyan]")


def get_token_from_user() -> Optional[str]:
    """
    从用户输入获取token
    Returns:
        token字符串，失败返回None
    """
    console.print("[yellow]注意：往常的网页登录获取的token已被封禁，现只能使用小程序登录[/yellow]")
    console.print("[yellow]请使用抓包工具获取小程序登录token，输入token进行后续操作！[/yellow]")
    console.print("[yellow]抓包工具推荐使用 ProxyPin，配置教程：暂时未定，后续会更新。[/yellow]")

    try:
        token = input("请输入token: ").strip()
        return token if token else None
    except (EOFError, KeyboardInterrupt):
        console.print("\n[yellow]输入被取消，程序退出[/yellow]")
        return None


def display_lecture_selection_prompt(auth_service: AuthService, lecture_service: LectureService):
    """
    显示活动选择提示
    Returns:
        选择的活动信息
    """
    console.rule("历史活动信息")

    # 获取历史活动
    activities = lecture_service.get_history_activities()
    if not activities:
        console.print("[red]获取活动列表失败[/red]")
        return None

    if not lecture_service.display_history_activities():
        return None

    # 获取用户选择
    index = input("请输入需要选择的活动序号：").strip()

    activity = lecture_service.get_activity_by_index(index)
    if not activity:
        console.print(f"[red]无效的活动序号: {index}[/red]")
        return None

    console.print(
        f"[green]当前选择序号{index}的活动，eid为：{activity['eid']}[/green]"
    )

    return activity


def perform_registration(
    activity: dict,
    auth_service: AuthService,
    lecture_service: LectureService
) -> bool:
    """
    执行报名流程
    Args:
        activity: 活动信息
        auth_service: 认证服务
        lecture_service: 活动服务

    Returns:
        是否成功
    """
    console.rule("活动报名")

    eid = activity.get('eid')
    extra_info = auth_service.get_extra_info()

    # 显示预填信息
    lecture_service.display_extra_info(extra_info)

    console.print(
        f"[cyan]活动标题：{activity.get('title')}   "
        f"开始时间：{format_timestamp(activity.get('start_time'))}[/cyan]"
    )

    # 获取报名字段
    fields = lecture_service.get_registration_fields(eid)
    if not fields:
        console.print("[red]获取报名字段失败[/red]")
        return False

    # 准备报名数据
    registration_data = lecture_service.prepare_registration_data(fields, extra_info)

    # 提报名
    success, msg = lecture_service.submit_registration_with_timing(
        activity,
        registration_data,
        extra_info
    )

    # 显示结果
    console.rule("提交结果")
    console.print(f"[bold green]Success: {success}[/bold green]")
    console.print(f"[bold green]Message: {msg}[/bold green]")

    if success:
        console.print("[bold green]恭喜您！报名成功！[/bold green]")
        console.print("[yellow]希望得到您的赞助，将会给予作者继续更新维护的动力[/yellow]")
        open_personal_page()
        console.print("[cyan]程序将在10秒后退出...[/cyan]")
        time.sleep(10)
        return True
    elif msg in ['报名人数已满或项目数量不足', 'invalid parameter']:
        console.print("[red]报名失败，程序将在10秒后退出...[/red]")
        time.sleep(10)
        return False
    else:
        console.print("[yellow]还未报名，刷新中...[/yellow]")
        return False


def main():
    """主函数"""
    display_banner()

    # 获取token
    token = get_token_from_user()
    if not token or not validate_token(token):
        console.print("[red]无效的token，程序退出[/red]")
        sys.exit(1)

    # 初始化服务
    auth_service = AuthService()
    if not auth_service.set_token(token):
        console.print("[red]token验证失败，程序退出[/red]")
        sys.exit(1)

    lecture_service = LectureService(auth_service.api_client)

    # 主循环
    try:
        activity = display_lecture_selection_prompt(auth_service, lecture_service)
        if not activity:
            sys.exit(1)

        success = perform_registration(activity, auth_service, lecture_service)
        sys.exit(0 if success else 1)

    except KeyboardInterrupt:
        console.print("\n[yellow]用户中断，程序退出[/yellow]")
        sys.exit(0)
    except Exception as e:
        logger.exception(f"未处理的异常: {e}")
        console.print(f"[red]程序异常: {e}[/red]")
        sys.exit(1)


if __name__ == '__main__':
    main()
