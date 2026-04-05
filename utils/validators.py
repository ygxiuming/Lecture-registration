# -*- coding: UTF-8 -*-
"""
数据验证模块
包含各种验证函数
"""
import re
from typing import Optional, Tuple, List, Dict, Any


def validate_token(token: str) -> bool:
    """验证token格式"""
    if not token or not isinstance(token, str):
        return False
    # 简单验证：非空字符串
    return len(token.strip()) > 0


def validate_eid(eid: str) -> bool:
    """验证活动ID格式"""
    if not eid or not isinstance(eid, str):
        return False
    return len(eid.strip()) > 0


def match_field_name(field_name: str, extra_info: Dict[str, str]) -> Tuple[Optional[str], Optional[str]]:
    """
    使用子集匹配规则匹配字段名
    Args:
        field_name: 报名表单中的字段名
        extra_info: 预填信息字典 {字段名: 值}

    Returns:
        (匹配的预填字段名, 对应的值)，未匹配返回 (None, None)

    Example:
        >>> extra_info = {"姓名": "修明"}
        >>> match_field_name("?姓！名", extra_info)
        ('姓名', '修明')
    """
    if not field_name or not extra_info:
        return None, None

    field_name_set = set(field_name)

    for key, value in extra_info.items():
        key_set = set(key)
        # 子集匹配：预填字段的所有字符都出现在表单字段中
        # 例如：预填"姓名"，表单"?姓！名" -> {'姓', '名'}.issubset({'?', '姓', '！', '名'})
        if key_set.issubset(field_name_set):
            return key, value

    return None, None


def parse_delay_time(extra_info: Dict[str, str]) -> int:
    """
    从预填信息中解析延迟时间
    Args:
        extra_info: 预填信息字典

    Returns:
        延迟时间（毫秒），未设置返回0
    """
    delay_str = extra_info.get("延迟时间", "0")
    try:
        return int(delay_str)
    except (ValueError, TypeError):
        return 0


def is_valid_phone(phone: str) -> bool:
    """验证手机号格式"""
    pattern = r'^1[3-9]\d{9}$'
    return bool(re.match(pattern, phone))


def is_valid_index(index_str: str, max_index: int) -> bool:
    """验证活动序号是否有效"""
    try:
        index = int(index_str)
        return 1 <= index <= max_index
    except (ValueError, TypeError):
        return False
