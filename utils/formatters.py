# -*- coding: UTF-8 -*-
"""
格式化模块
负责数据格式化和显示
"""
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple

from rich.console import Console
from rich.table import Table

console = Console(color_system='256', style=None)


def format_registration_field(item: Dict[str, Any]) -> Tuple[str, str, Any, str]:
    """
    格式化报名字段信息
    Args:
        item: 报名字段数据

    Returns:
        (字段名, 字段类型, 选项信息, 备注信息)
    """
    field_name = item.get("field_name", "")
    field_type = item.get("type_text", "")

    # 格式化选项
    if item.get("type_text") == '多项选择':
        options = item.get("options", [])
    elif item.get("type_text") == '单项选择':
        options = [option['text'] for option in item.get("options", [])]
    else:
        options = "需要手动填写信息"

    # 获取备注
    if item.get("field_name") == "验证数字":
        note = f"输入{item.get('min_value', '')}-{item.get('max_value', '')}之间的数字"
    else:
        note = "无"

    return field_name, field_type, str(options), note


def format_options(item: Dict[str, Any]) -> Any:
    """格式化选项信息"""
    if item.get("type_text") == '多项选择':
        return item.get("options", [])
    elif item.get("type_text") == '单项选择':
        return [option['text'] for option in item.get("options", [])]
    return "需要手动填写信息"


def get_field_note(item: Dict[str, Any]) -> str:
    """获取字段注释"""
    if item.get("field_name") == "验证数字":
        return f"输入{item.get('min_value', '')}-{item.get('max_value', '')}之间的数字"
    return "无"


def format_timestamp(timestamp: float, fmt: str = '%Y-%m-%d %H:%M:%S') -> str:
    """
    格式化时间戳
    Args:
        timestamp: 时间戳
        fmt: 格式字符串

    Returns:
        格式化后的时间字符串
    """
    return datetime.fromtimestamp(timestamp).strftime(fmt)


def create_history_table(history_items: List[Dict[str, Any]]) -> Table:
    """
    创建活动历史表格
    Args:
        history_items: 历史活动列表

    Returns:
        Rich Table对象
    """
    table = Table(show_header=True, header_style="bold magenta")
    table.title = "历史活动信息"
    table.add_column("序号", style="dim", width=5)
    table.add_column("活动标题", style="dim", width=50)
    table.add_column("开始时间", style="dim", width=20)
    table.add_column("活动状态", style="dim", width=8)
    table.add_column("eid", style="dim", width=25)
    table.add_column("报名人数", style="dim", width=10)

    for index, item in enumerate(history_items, start=1):
        start_time = format_timestamp(item['start_time'])
        status = "进行中" if item.get('status') == 1 else "未开始"
        table.add_row(
            str(index),
            item.get('title', ''),
            start_time,
            status,
            str(item.get('eid', '')),
            str(item.get('limit', ''))
        )

    return table


def create_registration_info_table(info: List[Dict[str, Any]], extra_info: Dict[str, str]) -> Table:
    """
    创建报名信息表格
    Args:
        info: 报名信息字段列表
        extra_info: 预填信息字典

    Returns:
        Rich Table对象
    """
    table = Table(show_header=True, header_style="bold magenta")
    table.title = "讲座需要填写的信息"
    table.add_column("信息标题", style="dim", width=12, justify="center")
    table.add_column("信息类型", justify="center")
    table.add_column("选项信息", justify="center")
    table.add_column("备注信息", justify="center")
    table.add_column("匹配字段", justify="center")
    table.add_column("匹配内容", justify="center")

    for item in info:
        field_name = item.get("field_name", "")
        field_type = item.get("type_text", "")
        options = format_options(item)
        note = get_field_note(item)

        # 匹配预填信息
        matched_key, matched_value = match_field_for_display(field_name, extra_info)

        table.add_row(
            field_name,
            field_type,
            str(options),
            note,
            matched_key,
            matched_value
        )
        table.add_row("", "", "", "", "", "")

    return table


def match_field_for_display(field_name: str, extra_info: Dict[str, str]) -> Tuple[str, str]:
    """
    为字段匹配预填信息并返回显示值
    Args:
        field_name: 表单字段名
        extra_info: 预填信息字典

    Returns:
        (匹配的字段名, 匹配的值)
    """
    from utils.validators import match_field_name

    matched_key, matched_value = match_field_name(field_name, extra_info)

    if matched_key and matched_value:
        return matched_key, matched_value

    # 尝试计算表达式
    try:
        expression = field_name.replace('=', '')
        result = eval(expression)
        return "验证计算", str(result)
    except:
        return "未匹配到字段", "1"


def create_extra_info_table(extra_info: Dict[str, str]) -> Table:
    """
    创建预填信息表格
    Args:
        extra_info: 预填信息字典

    Returns:
        Rich Table对象
    """
    table = Table(show_header=True, header_style="bold magenta")
    table.title = "预填信息预览"
    table.add_column("字段", style="dim", width=5)
    table.add_column("值", style="dim", width=50)

    for key, value in extra_info.items():
        table.add_row(key, value)

    return table
