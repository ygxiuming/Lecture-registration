# -*- coding: UTF-8 -*-
"""
活动服务模块
处理活动查询、选择、报名等业务逻辑
"""
import logging
import time
from datetime import datetime
from typing import Optional, Dict, Any, List

from rich.console import Console

from utils.api_client import APIClient
from utils.validators import parse_delay_time, is_valid_index, match_field_name
from utils.formatters import (
    create_history_table,
    create_registration_info_table,
    create_extra_info_table,
    format_timestamp as format_ts
)


def format_timestamp(timestamp: float, fmt: str = '%Y-%m-%d %H:%M:%S') -> str:
    """
    格式化时间戳（对外暴露的函数）
    Args:
        timestamp: 时间戳
        fmt: 格式字符串

    Returns:
        格式化后的时间字符串
    """
    return format_ts(timestamp, fmt)

console = Console(color_system='256', style=None)
logger = logging.getLogger(__name__)


class LectureService:
    """活动服务类"""

    def __init__(self, api_client: APIClient):
        self.api_client = api_client
        self.history_items: List[Dict[str, Any]] = []
        self.history_items_index: Dict[str, Dict[str, Any]] = {}

    def get_history_activities(self) -> Optional[List[Dict[str, Any]]]:
        """
        获取历史活动
        Returns:
            活动列表，失败返回None
        """
        activities = self.api_client.get_user_history()
        if not activities:
            return None

        self.history_items.clear()
        self.history_items_index.clear()

        current_timestamp = time.time()

        for activity in activities:
            # 筛选进行中和即将开始的活动
            if activity.get("status") == 1:
                self._add_activity_to_history(activity)
            elif activity.get("start_time", 0) > current_timestamp:
                self._add_activity_to_history(activity)

        return self.history_items

    def _add_activity_to_history(self, activity: Dict[str, Any]):
        """添加活动到历史记录"""
        history_data = {
            "title": activity.get("title", ""),
            "start_time": activity.get("start_time", 0),
            "status": activity.get("status", 0),
            "eid": activity.get("eid", ""),
            "limit": activity.get("limit", 0)
        }
        self.history_items.append(history_data)

    def display_history_activities(self) -> bool:
        """
        显示历史活动
        Returns:
            是否成功
        """
        if not self.history_items:
            console.print("[yellow]暂无可用活动[/yellow]")
            return False

        table = create_history_table(self.history_items)
        console.print(table)

        # 构建索引
        for index, item in enumerate(self.history_items, start=1):
            self.history_items_index[str(index)] = item

        return True

    def get_activity_by_index(self, index_str: str) -> Optional[Dict[str, Any]]:
        """
        根据序号获取活动
        Args:
            index_str: 活动序号字符串

        Returns:
            活动信息，无效返回None
        """
        if not is_valid_index(index_str, len(self.history_items)):
            return None
        return self.history_items_index.get(index_str)

    def get_registration_fields(self, eid: str) -> Optional[List[Dict[str, Any]]]:
        """
        获取报名字段
        Args:
            eid: 活动ID

        Returns:
            报名字段列表，失败返回None
        """
        return self.api_client.get_registration_requirements(eid)

    def prepare_registration_data(
        self,
        fields: List[Dict[str, Any]],
        extra_info: Dict[str, str]
    ) -> List[Dict[str, Any]]:
        """
        准备报名数据
        Args:
            fields: 报名字段列表
            extra_info: 预填信息

        Returns:
            格式化的报名数据
        """
        registration_data = []

        for item in fields:
            field_name = item.get("field_name", "")
            field_key = item.get("field_key", "")

            # 尝试匹配预填信息
            matched_value = self._match_field_value(field_name, extra_info)

            if matched_value:
                registration_data.append({
                    "field_name": field_name,
                    "field_value": matched_value,
                    "field_key": field_key,
                    "ignore": 0
                })

        return registration_data

    def _match_field_value(self, field_name: str, extra_info: Dict[str, str]) -> Optional[str]:
        """
        匹配字段值
        Args:
            field_name: 字段名
            extra_info: 预填信息

        Returns:
            匹配的字段值，未匹配返回None
        """
        from ..utils.validators import match_field_name

        matched_key, matched_value = match_field_name(field_name, extra_info)
        if matched_value:
            return matched_value

        # 尝试计算表达式
        try:
            expression = field_name.replace('=', '')
            result = eval(expression)
            return str(result)
        except:
            return None

    def display_registration_info(
        self,
        fields: List[Dict[str, Any]],
        extra_info: Dict[str, str]
    ):
        """
        显示报名信息
        Args:
            fields: 报名字段列表
            extra_info: 预填信息
        """
        table = create_registration_info_table(fields, extra_info)
        console.print(table)

    def display_extra_info(self, extra_info: Dict[str, str]):
        """
        显示预填信息
        Args:
            extra_info: 预填信息
        """
        if extra_info:
            table = create_extra_info_table(extra_info)
            console.print(table)

        console.print(
            "[yellow]备注：预填信息在 <https://p.baominggongju.com/personalInfo> 中进行增加修改，"
            "点击 添加快速填写信息 按钮即可\n"
            "若需要增加延迟提交，可增加字段 延迟时间，对应的字段值为毫秒；"
            "例如：需要延迟2秒提交，增加字段  延迟时间：2000[/yellow]"
        )
        console.print(
            "[yellow]预填信息匹配规则：采用子集匹配规则；\n"
            "例如：预填信息为 姓名：修明，若报名信息中同时存在姓和名两个字，则认定匹配成功！"
            "以下是匹配姓名成功示例\n"
            "？姓！名\n"
            "姓      名\n"
            "名  …… ### 姓[/yellow]"
        )

    def submit_registration_with_timing(
        self,
        activity: Dict[str, Any],
        registration_data: List[Dict[str, Any]],
        extra_info: Dict[str, str]
    ) -> tuple[bool, str]:
        """
        带时序控制的报名提交
        Args:
            activity: 活动信息
            registration_data: 报名数据
            extra_info: 预填信息

        Returns:
            (是否成功, 消息)
        """
        eid = activity.get('eid', '')
        start_time = activity.get('start_time', 0)
        delay_time = parse_delay_time(extra_info)

        current_time = time.time()

        # 如果已经开始，立即尝试提交
        if current_time >= start_time:
            console.print(
                f"[cyan]当前时间：{format_timestamp(current_time)}，"
                f"活动开始时间：{format_timestamp(start_time)}，开始报名[/cyan]"
            )
            return self._attempt_submit(eid, registration_data)

        # 等待到开始时间
        console.print(
            f"[cyan]活动开始时间：{format_timestamp(start_time)}，等待中...[/cyan]"
        )

        with console.status(
            f'[cyan]当前时间：{format_timestamp(time.time())}，'
            f'距离开始时间还有{start_time - time.time():.1f}秒[/cyan]',
            spinner='dots'
        ):
            while time.time() < start_time:
                time.sleep(0.5)

        # 到达开始时间后，等待延迟时间
        actual_start_time = start_time + (delay_time / 1000.0)

        while time.time() < actual_start_time:
            time.sleep(0.1)

        # 尝试提交
        return self._attempt_submit(eid, registration_data)

    def _attempt_submit(
        self,
        eid: str,
        registration_data: List[Dict[str, Any]]
    ) -> tuple[bool, str]:
        """
        尝试提交报名
        Args:
            eid: 活动ID
            registration_data: 报名数据

        Returns:
            (是否成功, 消息)
        """
        max_retries = 10
        retry_count = 0

        while retry_count < max_retries:
            success, msg = self.api_client.submit_registration(eid, registration_data)

            if success:
                return True, msg
            elif msg in ['报名人数已满或项目数量不足', 'invalid parameter']:
                return False, msg
            else:
                retry_count += 1
                console.print(f"[yellow]还未报名，刷新中... (尝试 {retry_count}/{max_retries})[/yellow]")
                time.sleep(0.5)

        return False, "超过最大重试次数"
